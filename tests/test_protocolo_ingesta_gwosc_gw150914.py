#!/usr/bin/env python3
"""
Tests para el Protocolo de Ingesta GWOSC – Fase 1 (GW150914)
=============================================================

Valida las funciones core del pipeline de ingesta y análisis de coherencia Ψ:
- Generación de strain simulado
- Blanqueo espectral
- Cálculo de Ψ via coherencia cruzada H1-L1
- Pipeline completo on-source / off-source
- Veredicto estadístico (Ψ_on / Ψ_off)
"""

import sys
import importlib.util
from pathlib import Path

import numpy as np
import pytest

# ── Importación del módulo bajo test ──────────────────────────────────────
_SCRIPT = Path(__file__).parent.parent / "scripts" / "protocolo_ingesta_gwosc_gw150914.py"
_spec = importlib.util.spec_from_file_location("protocolo_ingesta_gwosc_gw150914", _SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

ProtocoloIngestaGW150914 = _mod.ProtocoloIngestaGW150914
generar_strain_simulado = _mod.generar_strain_simulado
calcular_psi_gw = _mod.calcular_psi_gw
EVENT_TIME = _mod.EVENT_TIME
F0_CHIRP = _mod.F0_CHIRP
SAMPLE_RATE = _mod.SAMPLE_RATE
OFF_SOURCE_OFFSET = _mod.OFF_SOURCE_OFFSET


# ── Constantes de prueba ──────────────────────────────────────────────────

DURATION = 1.0           # ventana corta para tests rápidos
FS = float(SAMPLE_RATE)


# ══════════════════════════════════════════════════════════════════════════
# TestConstantes
# ══════════════════════════════════════════════════════════════════════════

class TestConstantes:
    """Verifica que las constantes del evento sean las publicadas oficialmente."""

    def test_gps_time_gw150914(self):
        """GPS time oficial de GW150914: 1126259462.4"""
        assert EVENT_TIME == pytest.approx(1126259462.4, rel=1e-6)

    def test_f0_chirp(self):
        """Frecuencia noésica f₀ = 141.7001 Hz"""
        assert F0_CHIRP == pytest.approx(141.7001, rel=1e-6)

    def test_sample_rate(self):
        """Tasa de muestreo estándar GWOSC = 4096 Hz"""
        assert SAMPLE_RATE == 4096

    def test_off_source_offset(self):
        """Offset off-source = 10 s antes del evento"""
        assert OFF_SOURCE_OFFSET == pytest.approx(10.0)


# ══════════════════════════════════════════════════════════════════════════
# TestStrainSimulado
# ══════════════════════════════════════════════════════════════════════════

class TestStrainSimulado:
    """Pruebas sobre la generación de strain sintético."""

    def test_longitud_correcta(self):
        """El array debe tener duration × sample_rate muestras."""
        strain = generar_strain_simulado("H1", DURATION, SAMPLE_RATE)
        assert len(strain) == int(DURATION * SAMPLE_RATE)

    def test_valores_finitos(self):
        """Todos los valores deben ser finitos."""
        strain = generar_strain_simulado("H1", DURATION, SAMPLE_RATE)
        assert np.all(np.isfinite(strain))

    def test_semillas_diferenciales(self):
        """H1 y L1 deben producir datos distintos (semillas distintas)."""
        h1 = generar_strain_simulado("H1", DURATION, SAMPLE_RATE)
        l1 = generar_strain_simulado("L1", DURATION, SAMPLE_RATE)
        # Los arrays no son idénticos elemento a elemento
        assert not np.array_equal(h1, l1)

    def test_reproducibilidad(self):
        """La misma llamada debe producir idénticos resultados."""
        a = generar_strain_simulado("H1", DURATION, SAMPLE_RATE)
        b = generar_strain_simulado("H1", DURATION, SAMPLE_RATE)
        assert np.allclose(a, b)

    def test_sin_senal_menor_amplitud(self):
        """Sin señal, la amplitud RMS debe ser menor."""
        con = generar_strain_simulado("H1", DURATION, SAMPLE_RATE, incluir_senal=True)
        sin = generar_strain_simulado("H1", DURATION, SAMPLE_RATE, incluir_senal=False)
        assert np.sqrt(np.mean(con ** 2)) >= np.sqrt(np.mean(sin ** 2))


# ══════════════════════════════════════════════════════════════════════════
# TestBlanqueo
# ══════════════════════════════════════════════════════════════════════════

class TestBlanqueo:
    """Pruebas sobre el blanqueo espectral."""

    def test_salida_misma_longitud(self):
        """El strain blanqueado debe tener la misma longitud que el original."""
        data = generar_strain_simulado("H1", DURATION, SAMPLE_RATE)
        blanqueado = ProtocoloIngestaGW150914._blanquear_array(data, FS)
        assert len(blanqueado) == len(data)

    def test_salida_finita(self):
        """El strain blanqueado no debe contener NaN ni Inf."""
        data = generar_strain_simulado("H1", DURATION, SAMPLE_RATE)
        blanqueado = ProtocoloIngestaGW150914._blanquear_array(data, FS)
        assert np.all(np.isfinite(blanqueado))

    def test_blanqueo_no_identidad(self):
        """El blanqueo debe modificar los datos (no ser la operación identidad)."""
        data = generar_strain_simulado("H1", DURATION, SAMPLE_RATE)
        blanqueado = ProtocoloIngestaGW150914._blanquear_array(data, FS)
        assert not np.allclose(data, blanqueado)


# ══════════════════════════════════════════════════════════════════════════
# TestCalculoPsi
# ══════════════════════════════════════════════════════════════════════════

class TestCalculoPsi:
    """Pruebas sobre el cálculo de la métrica Ψ."""

    def test_psi_es_finito(self):
        """Ψ debe ser un número finito."""
        h1 = generar_strain_simulado("H1", DURATION, SAMPLE_RATE)
        l1 = generar_strain_simulado("L1", DURATION, SAMPLE_RATE)
        psi = calcular_psi_gw(h1, l1, FS, F0_CHIRP)
        assert np.isfinite(psi)

    def test_psi_no_negativo(self):
        """Ψ debe ser no negativo (es potencia × coherencia²)."""
        h1 = generar_strain_simulado("H1", DURATION, SAMPLE_RATE)
        l1 = generar_strain_simulado("L1", DURATION, SAMPLE_RATE)
        psi = calcular_psi_gw(h1, l1, FS, F0_CHIRP)
        assert psi >= 0.0

    def test_psi_con_senal_mayor_que_sin_senal(self):
        """Ψ con señal presente debe superar Ψ con solo ruido."""
        h1_con = generar_strain_simulado("H1", DURATION, SAMPLE_RATE, incluir_senal=True)
        l1_con = generar_strain_simulado("L1", DURATION, SAMPLE_RATE, incluir_senal=True)
        h1_sin = generar_strain_simulado("H1", DURATION, SAMPLE_RATE, incluir_senal=False)
        l1_sin = generar_strain_simulado("L1", DURATION, SAMPLE_RATE, incluir_senal=False)

        psi_con = calcular_psi_gw(h1_con, l1_con, FS, F0_CHIRP)
        psi_sin = calcular_psi_gw(h1_sin, l1_sin, FS, F0_CHIRP)

        assert psi_con > psi_sin

    def test_psi_frecuencias_distintas(self):
        """Ψ evaluado en distintas frecuencias no debe dar el mismo valor."""
        h1 = generar_strain_simulado("H1", DURATION, SAMPLE_RATE)
        l1 = generar_strain_simulado("L1", DURATION, SAMPLE_RATE)
        psi_f0 = calcular_psi_gw(h1, l1, FS, F0_CHIRP)
        psi_100 = calcular_psi_gw(h1, l1, FS, 100.0)
        # Las potencias espectrales en frecuencias distintas difieren
        assert psi_f0 != psi_100


# ══════════════════════════════════════════════════════════════════════════
# TestPipelineSimulado
# ══════════════════════════════════════════════════════════════════════════

class TestPipelineSimulado:
    """Pruebas de integración del pipeline completo en modo simulado."""

    def setup_method(self):
        self.pipeline = ProtocoloIngestaGW150914(
            duration=DURATION,
            f_target=F0_CHIRP,
            simulated=True,
        )

    def test_analizar_on_source_devuelve_dict(self):
        """analizar_on_source debe devolver un diccionario con clave 'psi'."""
        resultado = self.pipeline.analizar_on_source()
        assert isinstance(resultado, dict)
        assert "psi" in resultado

    def test_analizar_on_source_psi_finito(self):
        """Ψ_on debe ser finito."""
        resultado = self.pipeline.analizar_on_source()
        assert np.isfinite(resultado["psi"])

    def test_analizar_off_source_devuelve_dict(self):
        """analizar_off_source debe devolver un diccionario con clave 'psi'."""
        resultado = self.pipeline.analizar_off_source()
        assert isinstance(resultado, dict)
        assert "psi" in resultado

    def test_analizar_off_source_psi_no_cero(self):
        """Ψ_off no debe ser exactamente cero (se aplica fallback a 1e-100)."""
        resultado = self.pipeline.analizar_off_source()
        assert resultado["psi"] != 0.0

    def test_tiempos_on_source_correctos(self):
        """Los tiempos GPS de on-source deben acotar el merger."""
        resultado = self.pipeline.analizar_on_source()
        t_start_esperado = EVENT_TIME - DURATION / 2.0
        assert resultado["t_start_gps"] == pytest.approx(t_start_esperado, rel=1e-9)
        assert resultado["t_end_gps"] == pytest.approx(t_start_esperado + DURATION, rel=1e-9)

    def test_tiempos_off_source_correctos(self):
        """Los tiempos GPS de off-source deben estar 10 s antes del evento."""
        resultado = self.pipeline.analizar_off_source()
        t_start_esperado = EVENT_TIME - OFF_SOURCE_OFFSET - DURATION
        assert resultado["t_start_gps"] == pytest.approx(t_start_esperado, rel=1e-9)

    def test_veredicto_contiene_campos_esperados(self):
        """El veredicto debe contener los campos necesarios."""
        self.pipeline.analizar_on_source()
        self.pipeline.analizar_off_source()
        veredicto = self.pipeline.calcular_veredicto()

        for campo in ("psi_on", "psi_off", "ratio", "umbral", "supera_umbral", "descripcion"):
            assert campo in veredicto

    def test_veredicto_ratio_positivo(self):
        """La razón Ψ_on / Ψ_off debe ser positiva."""
        self.pipeline.analizar_on_source()
        self.pipeline.analizar_off_source()
        veredicto = self.pipeline.calcular_veredicto()
        assert veredicto["ratio"] > 0.0

    def test_veredicto_supera_umbral_simulado(self):
        """
        Con señal sintética, Ψ_on (incluir_senal=True) debe superar a
        Ψ_off (incluir_senal=False), dando ratio > 1.
        """
        self.pipeline.analizar_on_source()
        self.pipeline.analizar_off_source()
        veredicto = self.pipeline.calcular_veredicto()
        # On-source con señal debe ser mayor que off-source sin señal
        assert veredicto["ratio"] > 1.0

    def test_ejecutar_devuelve_dict_completo(self):
        """ejecutar() debe devolver un dict con claves 'on_source', 'off_source', 'veredicto'."""
        resultados = self.pipeline.ejecutar()
        assert "on_source" in resultados
        assert "off_source" in resultados
        assert "veredicto" in resultados

    def test_exportar_crea_fichero(self, tmp_path):
        """exportar_resultados debe crear el fichero JSON en la ruta indicada."""
        self.pipeline.output_dir = tmp_path
        self.pipeline.analizar_on_source()
        self.pipeline.analizar_off_source()
        self.pipeline.calcular_veredicto()

        ruta = self.pipeline.exportar_resultados("test_output.json")
        assert ruta.exists()
        assert ruta.stat().st_size > 0

    def test_exportar_json_valido(self, tmp_path):
        """El fichero exportado debe ser JSON válido con los campos principales."""
        import json

        self.pipeline.output_dir = tmp_path
        self.pipeline.analizar_on_source()
        self.pipeline.analizar_off_source()
        self.pipeline.calcular_veredicto()

        ruta = self.pipeline.exportar_resultados("test_valid.json")
        with open(ruta, encoding="utf-8") as fp:
            datos = json.load(fp)

        assert datos["evento"] == "GW150914"
        assert datos["gps_time"] == pytest.approx(EVENT_TIME)
        assert "on_source" in datos
        assert "off_source" in datos
        assert "veredicto" in datos


# ══════════════════════════════════════════════════════════════════════════
# TestIntegracion
# ══════════════════════════════════════════════════════════════════════════

class TestIntegracion:
    """Pruebas de integración end-to-end con pipeline simulado."""

    def test_pipeline_completo_simulado(self):
        """El pipeline completo en modo simulado debe completarse sin errores."""
        pipeline = ProtocoloIngestaGW150914(
            duration=DURATION,
            f_target=F0_CHIRP,
            simulated=True,
        )
        resultados = pipeline.ejecutar()

        # Estructura completa
        assert resultados["evento"] == "GW150914"
        assert "on_source" in resultados
        assert "off_source" in resultados
        assert "veredicto" in resultados

        # Los valores Ψ son números finitos
        assert np.isfinite(resultados["on_source"]["psi"])
        assert np.isfinite(resultados["off_source"]["psi"])

        # El ratio es positivo
        assert resultados["veredicto"]["ratio"] > 0.0

    def test_modo_simulated_activa_cuando_gwpy_no_disponible(self, monkeypatch):
        """Si GWPY_AVAILABLE es False, el pipeline usa simulación automáticamente."""
        monkeypatch.setattr(_mod, "GWPY_AVAILABLE", False)

        pipeline = ProtocoloIngestaGW150914(
            duration=DURATION,
            f_target=F0_CHIRP,
            simulated=False,  # intenta real, pero GWPY no disponible
        )
        # No debe lanzar excepción
        resultados = pipeline.ejecutar()
        assert "on_source" in resultados


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
