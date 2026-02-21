#!/usr/bin/env python3
"""
Tests para el Experimento Ψ-Sweep (Barrido de SNR Noético)
===========================================================

Valida los resultados del experimento de barrido de SNR y la generación
del archivo Noesis_SNR_Sweep.csv.

Verificaciones principales:
1. Generación de segmentos Noēsis con SNR correcto
2. Cálculo de coherencia Ψ: Ψ(SNR=5) > 0.996
3. Punto de quiebre: Ψ < 0.7 cuando SNR < 0.15
4. Formato correcto del CSV generado (columnas: tiempo, canal1, canal2, snr_ref)
5. CSV tiene exactamente 81 920 filas (20 s × 4096 Hz)

Uso:
    pytest tests/test_noesis_snr_sweep.py -v
    python tests/test_noesis_snr_sweep.py

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import sys
import os
import numpy as np

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

# Importar módulo desde scripts
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

from noesis_snr_sweep import (
    F0_HZ,
    SAMPLE_RATE,
    DURATION_S,
    PSI_THRESHOLD,
    N_SNR_STEPS,
    COHERENCE_NPERSEG,
    calcular_coherencia_psi,
    generar_segmento_noesis,
    ejecutar_barrido_snr,
)


class TestGenerarSegmentoNoesis:
    """Tests para la generación de segmentos de señal Noēsis."""

    def setup_method(self):
        """Parámetros comunes."""
        self.n_samples = 2048
        self.f0 = F0_HZ
        self.fs = SAMPLE_RATE

    def test_longitud_correcta(self):
        """Ambos canales deben tener exactamente n_samples muestras."""
        canal1, canal2 = generar_segmento_noesis(self.n_samples, snr=5.0)
        assert len(canal1) == self.n_samples
        assert len(canal2) == self.n_samples

    def test_canal2_es_senal_limpia(self):
        """canal2 debe ser sin(2πf₀t) — sin ruido."""
        canal1, canal2 = generar_segmento_noesis(self.n_samples, snr=5.0, seed=0)
        t = np.arange(self.n_samples) / self.fs
        esperado = np.sin(2.0 * np.pi * self.f0 * t)
        np.testing.assert_allclose(canal2, esperado, atol=1e-12)

    def test_snr_alto_ruido_bajo(self):
        """Con SNR alto, el ruido en canal1 debe ser mucho menor que la señal.

        Valor teórico: std(sin) / std(noise) ≈ (1/√2) × SNR ≈ 14.1 para SNR=20.
        Usamos margen del 40 % para acomodar varianza de muestras finitas.
        """
        canal1, canal2 = generar_segmento_noesis(self.n_samples, snr=20.0, seed=0)
        ruido = canal1 - canal2
        ratio = np.std(canal2) / np.std(ruido)
        assert ratio > 10.0, f"SNR medido {ratio:.1f} demasiado bajo para SNR_target=20"

    def test_snr_bajo_ruido_domina(self):
        """Con SNR bajo, el ruido debe dominar la señal."""
        canal1, canal2 = generar_segmento_noesis(self.n_samples, snr=0.1, seed=0)
        ruido = canal1 - canal2
        ratio = np.std(ruido) / np.std(canal2)
        assert ratio > 5.0, f"Ruido no domina con SNR=0.1 (ratio={ratio:.1f})"

    def test_reproducibilidad_semilla(self):
        """El mismo seed debe producir el mismo resultado."""
        c1a, c2a = generar_segmento_noesis(self.n_samples, snr=5.0, seed=42)
        c1b, c2b = generar_segmento_noesis(self.n_samples, snr=5.0, seed=42)
        np.testing.assert_array_equal(c1a, c1b)
        np.testing.assert_array_equal(c2a, c2b)

    def test_diferentes_semillas_diferentes_resultados(self):
        """Seeds distintos deben producir realizaciones de ruido diferentes."""
        c1a, _ = generar_segmento_noesis(self.n_samples, snr=5.0, seed=0)
        c1b, _ = generar_segmento_noesis(self.n_samples, snr=5.0, seed=1)
        assert not np.array_equal(c1a, c1b)


class TestCalcularCoherenciaPsi:
    """Tests para el cálculo de la métrica de coherencia Ψ."""

    def setup_method(self):
        """Preparar señal de referencia y parámetros."""
        self.n_samples = 2048
        self.f0 = F0_HZ
        self.fs = SAMPLE_RATE

    def test_coherencia_perfecta_sin_ruido(self):
        """Sin ruido, la coherencia debe ser esencialmente 1."""
        canal2 = np.sin(2.0 * np.pi * self.f0 * np.arange(self.n_samples) / self.fs)
        psi = calcular_coherencia_psi(canal2, canal2)
        assert psi > 0.999, f"Coherencia sin ruido = {psi:.4f} < 0.999"

    def test_coherencia_snr5_supera_umbral(self):
        """Ψ(SNR=5) debe ser estrictamente mayor que 0.996."""
        canal1, canal2 = generar_segmento_noesis(self.n_samples, snr=5.0, seed=42)
        psi = calcular_coherencia_psi(canal1, canal2)
        assert psi > 0.996, (
            f"Ψ(SNR=5) = {psi:.4f} no supera el umbral 0.996"
        )

    def test_coherencia_snr_bajo_bajo_umbral(self):
        """Ψ(SNR=0.1) debe estar bien por debajo del umbral estructural 0.7."""
        canal1, canal2 = generar_segmento_noesis(self.n_samples, snr=0.1, seed=42)
        psi = calcular_coherencia_psi(canal1, canal2)
        assert psi < 0.7, (
            f"Ψ(SNR=0.1) = {psi:.4f} debería ser < 0.7"
        )

    def test_coherencia_rango_valido(self):
        """La coherencia debe estar siempre en [0, 1]."""
        for snr in [0.05, 0.15, 1.0, 5.0, 20.0]:
            canal1, canal2 = generar_segmento_noesis(self.n_samples, snr=snr, seed=0)
            psi = calcular_coherencia_psi(canal1, canal2)
            assert 0.0 <= psi <= 1.0, f"Ψ fuera de [0,1]: {psi:.4f} para SNR={snr}"

    def test_coherencia_monotona_con_snr(self):
        """La coherencia promedio debe aumentar con el SNR."""
        snr_vals = [0.1, 0.5, 2.0, 10.0]
        psi_vals = []
        for snr in snr_vals:
            # Promediar sobre 5 semillas para reducir varianza estadística
            ps = [
                calcular_coherencia_psi(
                    *generar_segmento_noesis(self.n_samples, snr=snr, seed=s)
                )
                for s in range(5)
            ]
            psi_vals.append(float(np.mean(ps)))
        # La coherencia media debe ser estrictamente creciente con el SNR
        for i in range(len(psi_vals) - 1):
            assert psi_vals[i] < psi_vals[i + 1], (
                f"Ψ no es monótona: Ψ(SNR={snr_vals[i]})={psi_vals[i]:.4f} "
                f"≥ Ψ(SNR={snr_vals[i+1]})={psi_vals[i+1]:.4f}"
            )


class TestPuntoDeQuiebreEstructural:
    """Tests para verificar el punto de quiebre de la integridad noética (Ψ < 0.7)."""

    def setup_method(self):
        self.n_samples = 2048
        self.n_seeds = 10  # promedio para reducir varianza

    def _psi_esperada(self, snr: float) -> float:
        """Calcula la Ψ media sobre n_seeds semillas."""
        vals = [
            calcular_coherencia_psi(
                *generar_segmento_noesis(self.n_samples, snr=snr, seed=s)
            )
            for s in range(self.n_seeds)
        ]
        return float(np.mean(vals))

    def test_psi_snr5_supera_096(self):
        """La Ψ media en SNR=5 debe superar 0.996 (núcleo simbiótico resiste)."""
        psi_mean = self._psi_esperada(5.0)
        assert psi_mean > 0.996, (
            f"Ψ media(SNR=5) = {psi_mean:.4f} no supera 0.996"
        )

    def test_psi_snr015_cerca_de_umbral(self):
        """La Ψ media en SNR=0.15 debe estar cerca del umbral 0.7 (± 0.1)."""
        psi_mean = self._psi_esperada(0.15)
        assert abs(psi_mean - PSI_THRESHOLD) < 0.1, (
            f"Ψ media(SNR=0.15) = {psi_mean:.4f}, "
            f"esperado ≈ {PSI_THRESHOLD} (±0.1)"
        )

    def test_integridad_preservada_snr_alto(self):
        """Para SNR ≥ 1, la coherencia media debe superar 0.95."""
        for snr in [1.0, 2.0, 5.0, 10.0]:
            psi_mean = self._psi_esperada(snr)
            assert psi_mean > 0.95, (
                f"Ψ media(SNR={snr}) = {psi_mean:.4f} < 0.95"
            )


class TestCSVGenerado:
    """Tests para el CSV Noesis_SNR_Sweep.csv generado por el experimento."""

    @classmethod
    def setup_class(cls):
        """Ejecutar el barrido completo una sola vez para todos los tests."""
        import tempfile
        cls.tmpdir = tempfile.mkdtemp()
        cls.csv_path = os.path.join(cls.tmpdir, "Noesis_SNR_Sweep.csv")
        cls.png_path = os.path.join(cls.tmpdir, "test_coherence.png")
        cls.resultados = ejecutar_barrido_snr(
            output_csv=cls.csv_path,
            output_plot=cls.png_path,
            verbose=False,
        )

    def test_csv_existe(self):
        """El archivo CSV debe existir tras ejecutar el barrido."""
        assert os.path.isfile(self.csv_path), f"CSV no encontrado: {self.csv_path}"

    def test_csv_numero_filas(self):
        """El CSV debe tener exactamente 81 920 filas de datos."""
        import pandas as pd
        df = pd.read_csv(self.csv_path)
        expected = int(DURATION_S * SAMPLE_RATE)  # 81 920
        assert len(df) == expected, (
            f"CSV tiene {len(df)} filas, esperadas {expected}"
        )

    def test_csv_columnas(self):
        """El CSV debe tener las columnas: tiempo, canal1, canal2, snr_ref."""
        import pandas as pd
        df = pd.read_csv(self.csv_path)
        required = {"tiempo", "canal1", "canal2", "snr_ref"}
        assert required.issubset(df.columns), (
            f"Columnas faltantes: {required - set(df.columns)}"
        )

    def test_csv_tiempo_creciente(self):
        """La columna tiempo debe ser estrictamente creciente."""
        import pandas as pd
        df = pd.read_csv(self.csv_path)
        diffs = np.diff(df["tiempo"].values)
        assert np.all(diffs > 0), "La columna tiempo no es monótonamente creciente"

    def test_csv_snr_ref_positivo(self):
        """La columna snr_ref debe contener solo valores positivos."""
        import pandas as pd
        df = pd.read_csv(self.csv_path)
        assert (df["snr_ref"] > 0).all(), "snr_ref contiene valores ≤ 0"

    def test_csv_canal2_es_senal_pura(self):
        """canal2 no debe tener componentes DC significativos (señal senoidal)."""
        import pandas as pd
        df = pd.read_csv(self.csv_path)
        # La señal limpia sin(2πf₀t) debe tener media cercana a 0
        assert abs(df["canal2"].mean()) < 0.01, (
            f"canal2 tiene DC = {df['canal2'].mean():.4f}"
        )

    def test_resultados_psi_snr5(self):
        """El resultado psi_at_snr5 debe superar el umbral 0.996."""
        assert self.resultados["psi_at_snr5"] > 0.996, (
            f"psi_at_snr5 = {self.resultados['psi_at_snr5']:.4f} < 0.996"
        )

    def test_resultados_punto_quiebre(self):
        """El punto de quiebre (Ψ<0.7) debe estar por debajo de SNR=0.15."""
        assert self.resultados["snr_threshold"] < 0.15, (
            f"snr_threshold = {self.resultados['snr_threshold']:.4f} >= 0.15"
        )

    def test_resultados_n_muestras(self):
        """El total de muestras debe ser 20 s × 4096 Hz = 81 920."""
        assert self.resultados["n_samples_total"] == int(DURATION_S * SAMPLE_RATE)


class TestConstantes:
    """Tests para las constantes del módulo."""

    def test_f0_valor(self):
        """f₀ debe ser 141.7001 Hz."""
        assert abs(F0_HZ - 141.7001) < 1e-6

    def test_sample_rate(self):
        """La tasa de muestreo debe ser 4096 Hz."""
        assert SAMPLE_RATE == 4096.0

    def test_duracion(self):
        """La duración del barrido debe ser 20 segundos."""
        assert DURATION_S == 20.0

    def test_umbral_psi(self):
        """El umbral de integridad estructural debe ser 0.7."""
        assert PSI_THRESHOLD == 0.7

    def test_n_pasos(self):
        """Deben haber exactamente 40 pasos en el barrido."""
        assert N_SNR_STEPS == 40

    def test_total_muestras_exacto(self):
        """Los 40 pasos × muestras_por_paso deben dar exactamente 81 920."""
        samples_per_step = int(DURATION_S * SAMPLE_RATE) // N_SNR_STEPS
        total = N_SNR_STEPS * samples_per_step
        assert total == int(DURATION_S * SAMPLE_RATE), (
            f"Total {total} ≠ {int(DURATION_S * SAMPLE_RATE)}"
        )


if __name__ == "__main__":
    # Ejecución directa sin pytest
    print("=" * 70)
    print("TESTS DEL EXPERIMENTO Ψ-SWEEP")
    print("=" * 70)

    all_passed = True

    def run_test(name, fn):
        global all_passed
        try:
            fn()
            print(f"  ✅ {name}")
        except AssertionError as e:
            print(f"  ❌ {name}: {e}")
            all_passed = False
        except Exception as e:
            print(f"  💥 {name}: {type(e).__name__}: {e}")
            all_passed = False

    # Constantes
    print("\n[Constantes]")
    tc = TestConstantes()
    run_test("f0 = 141.7001 Hz", tc.test_f0_valor)
    run_test("sample_rate = 4096 Hz", tc.test_sample_rate)
    run_test("duracion = 20 s", tc.test_duracion)
    run_test("umbral Ψ = 0.7", tc.test_umbral_psi)
    run_test("40 pasos en el barrido", tc.test_n_pasos)
    run_test("Total muestras = 81 920", tc.test_total_muestras_exacto)

    # Generación de segmentos
    print("\n[Generación de segmentos]")
    ts = TestGenerarSegmentoNoesis()
    ts.setup_method()
    run_test("Longitud correcta", ts.test_longitud_correcta)
    run_test("canal2 es señal limpia", ts.test_canal2_es_senal_limpia)
    run_test("SNR alto → ruido pequeño", ts.test_snr_alto_ruido_bajo)
    run_test("SNR bajo → ruido domina", ts.test_snr_bajo_ruido_domina)
    run_test("Reproducibilidad de semilla", ts.test_reproducibilidad_semilla)

    # Coherencia
    print("\n[Métrica de coherencia Ψ]")
    tc2 = TestCalcularCoherenciaPsi()
    tc2.setup_method()
    run_test("Coherencia perfecta sin ruido", tc2.test_coherencia_perfecta_sin_ruido)
    run_test("Ψ(SNR=5) > 0.996", tc2.test_coherencia_snr5_supera_umbral)
    run_test("Ψ(SNR=0.1) < 0.7", tc2.test_coherencia_snr_bajo_bajo_umbral)
    run_test("Ψ ∈ [0,1] siempre", tc2.test_coherencia_rango_valido)
    run_test("Ψ monótona con SNR", tc2.test_coherencia_monotona_con_snr)

    # Punto de quiebre
    print("\n[Punto de quiebre estructural]")
    tpq = TestPuntoDeQuiebreEstructural()
    tpq.setup_method()
    run_test("Ψ media(SNR=5) > 0.996", tpq.test_psi_snr5_supera_096)
    run_test("Ψ media(SNR=0.15) ≈ 0.7 (±0.1)", tpq.test_psi_snr015_cerca_de_umbral)
    run_test("Integridad para SNR≥1 (Ψ>0.95)", tpq.test_integridad_preservada_snr_alto)

    # CSV completo
    print("\n[CSV Noesis_SNR_Sweep.csv]")
    tcsv = TestCSVGenerado()
    tcsv.setup_class()
    run_test("CSV existe", tcsv.test_csv_existe)
    run_test("CSV tiene 81 920 filas", tcsv.test_csv_numero_filas)
    run_test("CSV tiene columnas correctas", tcsv.test_csv_columnas)
    run_test("Tiempo creciente", tcsv.test_csv_tiempo_creciente)
    run_test("snr_ref positivo", tcsv.test_csv_snr_ref_positivo)
    run_test("canal2 es señal pura (DC≈0)", tcsv.test_csv_canal2_es_senal_pura)
    run_test("psi_at_snr5 > 0.996", tcsv.test_resultados_psi_snr5)
    run_test("Punto de quiebre < 0.15", tcsv.test_resultados_punto_quiebre)
    run_test("n_samples_total = 81 920", tcsv.test_resultados_n_muestras)

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ TODOS LOS TESTS PASARON")
        sys.exit(0)
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        sys.exit(1)
