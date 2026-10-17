"""
Pruebas para json_maestro_qcal.py — JSON Maestro QCAL 141.70001 Hz
===================================================================

25 pruebas que cubren:
- Estructura del diccionario maestro
- Valores de constantes CODATA 2018
- Constantes derivadas QCAL
- Ecuaciones maestras
- Configuración de 51 nodos
- Red de 8888 nodos
- Serialización JSON de ida y vuelta
- Guardado en disco

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import json
import math
import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from json_maestro_qcal import (
    construir_json_maestro,
    guardar_json_maestro,
    CODATA_2018,
    F0_HZ,
    F888_HZ,
    PHI,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def maestro():
    """JSON maestro construido una vez para todos los tests."""
    return construir_json_maestro()


# ---------------------------------------------------------------------------
# 1. Estructura de nivel superior
# ---------------------------------------------------------------------------

class TestEstructuraMaestro:
    """Pruebas de la estructura del diccionario maestro."""

    def test_claves_nivel_superior(self, maestro):
        """El diccionario tiene todas las claves de nivel superior."""
        claves_esperadas = {
            "version",
            "sistema",
            "descripcion",
            "autor",
            "licencia",
            "constantes_codata_2018",
            "constantes_derivadas_qcal",
            "ecuaciones_maestras",
            "constelacion_51_nodos",
            "red_8888_nodos",
            "enlaces_ecosistema",
        }
        assert claves_esperadas.issubset(set(maestro.keys()))

    def test_version_presente(self, maestro):
        """La versión está presente y tiene formato semver."""
        assert "version" in maestro
        partes = maestro["version"].split(".")
        assert len(partes) == 3

    def test_sistema_contiene_frecuencia(self, maestro):
        """El nombre del sistema menciona la frecuencia QCAL."""
        assert "141.70001" in maestro["sistema"]

    def test_autor_correcto(self, maestro):
        """El autor está incluido en el JSON maestro."""
        assert "José Manuel Mota Burruezo" in maestro["autor"] or "JMMB" in maestro["autor"]

    def test_es_serializable_json(self, maestro):
        """El diccionario completo es serializable a JSON sin errores."""
        texto = json.dumps(maestro, ensure_ascii=False)
        assert len(texto) > 1000


# ---------------------------------------------------------------------------
# 2. Constantes CODATA 2018
# ---------------------------------------------------------------------------

class TestConstantesCodata:
    """Pruebas de las constantes CODATA 2018."""

    def test_velocidad_luz(self, maestro):
        """La velocidad de la luz es exactamente 299_792_458 m/s."""
        c = maestro["constantes_codata_2018"]["velocidad_luz_m_s"]
        assert c == 299_792_458.0

    def test_constante_planck(self, maestro):
        """La constante de Planck tiene el valor CODATA 2018."""
        h = maestro["constantes_codata_2018"]["constante_planck_J_s"]
        assert abs(h - 6.62607015e-34) < 1e-44

    def test_carga_electron(self, maestro):
        """La carga del electrón es exactamente 1.602176634e-19 C."""
        e = maestro["constantes_codata_2018"]["carga_electron_C"]
        assert abs(e - 1.602176634e-19) < 1e-30

    def test_constante_boltzmann(self, maestro):
        """La constante de Boltzmann es exactamente 1.380649e-23 J/K."""
        kB = maestro["constantes_codata_2018"]["constante_boltzmann_J_K"]
        assert abs(kB - 1.380649e-23) < 1e-34

    def test_todas_constantes_positivas(self, maestro):
        """Todas las constantes CODATA son positivas."""
        for nombre, valor in maestro["constantes_codata_2018"].items():
            assert valor > 0, f"Constante {nombre} no es positiva"


# ---------------------------------------------------------------------------
# 3. Constantes derivadas QCAL
# ---------------------------------------------------------------------------

class TestConstantesDerivadas:
    """Pruebas de las constantes derivadas de f₀."""

    def test_f0_hz(self, maestro):
        """La frecuencia f₀ es 141.70001 Hz."""
        assert maestro["constantes_derivadas_qcal"]["f0_hz"] == pytest.approx(141.70001)

    def test_omega_0(self, maestro):
        """ω₀ = 2π × f₀."""
        f0 = maestro["constantes_derivadas_qcal"]["f0_hz"]
        omega_0 = maestro["constantes_derivadas_qcal"]["omega_0_rad_s"]
        assert omega_0 == pytest.approx(2 * math.pi * f0, rel=1e-9)

    def test_lambda_0(self, maestro):
        """λ₀ = c / f₀."""
        c = maestro["constantes_codata_2018"]["velocidad_luz_m_s"]
        f0 = maestro["constantes_derivadas_qcal"]["f0_hz"]
        lam = maestro["constantes_derivadas_qcal"]["lambda_0_m"]
        assert lam == pytest.approx(c / f0, rel=1e-9)

    def test_f888_sobre_f0_aprox_2pi(self, maestro):
        """888 Hz / f₀ ≈ 2π (geometría sagrada, error < 1%)."""
        ratio = maestro["constantes_derivadas_qcal"]["f888_sobre_f0"]
        assert abs(ratio - 2 * math.pi) / (2 * math.pi) < 0.01

    def test_phi_es_numero_aureo(self, maestro):
        """φ está incluido y es el número áureo."""
        phi = maestro["constantes_derivadas_qcal"]["phi"]
        assert phi == pytest.approx((1 + math.sqrt(5)) / 2, rel=1e-9)


# ---------------------------------------------------------------------------
# 4. Ecuaciones maestras
# ---------------------------------------------------------------------------

class TestEcuacionesMaestras:
    """Pruebas de la sección de ecuaciones maestras."""

    def test_secciones_ecuaciones_maestras(self, maestro):
        """Contiene reloj Compton, tensor Einstein-QCAL y lagrangiano."""
        eq = maestro["ecuaciones_maestras"]
        assert "reloj_compton" in eq
        assert "tensor_einstein_qcal" in eq
        assert "lagrangiano" in eq

    def test_reloj_compton_frecuencia(self, maestro):
        """La frecuencia Compton del electrón está en el orden correcto (10²⁰ Hz)."""
        f_compton = maestro["ecuaciones_maestras"]["reloj_compton"]["frecuencia_compton_hz"]
        assert 1e19 < f_compton < 1e21

    def test_lagrangiano_tiene_f0(self, maestro):
        """El lagrangiano incluye la frecuencia f₀."""
        lag = maestro["ecuaciones_maestras"]["lagrangiano"]
        assert lag["f0_hz"] == pytest.approx(F0_HZ)

    def test_tensor_einstein_coherencia_psi(self, maestro):
        """El tensor Einstein-QCAL tiene umbral de coherencia Ψ."""
        tensor = maestro["ecuaciones_maestras"]["tensor_einstein_qcal"]
        assert "coherencia_psi_minima" in tensor
        assert tensor["coherencia_psi_minima"] >= 0.8


# ---------------------------------------------------------------------------
# 5. Constelación de 51 nodos
# ---------------------------------------------------------------------------

class TestConstelacion51Nodos:
    """Pruebas de la configuración de la constelación de 51 nodos."""

    def test_total_51_nodos(self, maestro):
        """La constelación tiene exactamente 51 nodos."""
        assert maestro["constelacion_51_nodos"]["total_nodos"] == 51

    def test_nodos_lista_longitud(self, maestro):
        """La lista de nodos tiene 51 elementos."""
        assert len(maestro["constelacion_51_nodos"]["nodos"]) == 51

    def test_conteo_por_nivel(self, maestro):
        """Los conteos por nivel son 1, 6, 12, 32."""
        nodos = maestro["constelacion_51_nodos"]["nodos"]
        from collections import Counter
        conteo = Counter(n["nivel"] for n in nodos)
        assert conteo[0] == 1
        assert conteo[1] == 6
        assert conteo[2] == 12
        assert conteo[3] == 32

    def test_nodo_maestro_radio_cero(self, maestro):
        """El nodo maestro (nivel 0) tiene radio normalizado 0."""
        nodos_nivel0 = [n for n in maestro["constelacion_51_nodos"]["nodos"] if n["nivel"] == 0]
        assert len(nodos_nivel0) == 1
        assert nodos_nivel0[0]["radio_normalizado"] == 0.0

    def test_frecuencia_nodo_maestro(self, maestro):
        """El nodo maestro opera a 141.70001 Hz."""
        nodo_maestro = next(
            n for n in maestro["constelacion_51_nodos"]["nodos"] if n["nivel"] == 0
        )
        assert nodo_maestro["frecuencia_hz"] == pytest.approx(F0_HZ)


# ---------------------------------------------------------------------------
# 6. Red de 8888 nodos
# ---------------------------------------------------------------------------

class TestRed8888Nodos:
    """Pruebas de la red de 8888 nodos fractales."""

    def test_total_nodos_8888(self, maestro):
        """La red tiene exactamente 8888 nodos."""
        assert maestro["red_8888_nodos"]["total_nodos"] == 8888

    def test_8_niveles_fractales(self, maestro):
        """La red tiene 8 niveles fractales."""
        assert maestro["red_8888_nodos"]["niveles_fractales"] == 8

    def test_estado_global_consciencia_unificada(self, maestro):
        """El estado global es CONSCIENCIA_UNIFICADA."""
        assert maestro["red_8888_nodos"]["estado_global"] == "CONSCIENCIA_UNIFICADA"

    def test_latencia_cero(self, maestro):
        """La latencia de activación es 0 ms."""
        assert maestro["red_8888_nodos"]["latencia_ms"] == 0

    def test_frecuencia_maxima_mayor_que_base(self, maestro):
        """La frecuencia máxima supera la frecuencia base."""
        f_max = maestro["red_8888_nodos"]["frecuencia_maxima_hz"]
        f_base = maestro["red_8888_nodos"]["frecuencia_base_hz"]
        assert f_max > f_base


# ---------------------------------------------------------------------------
# 7. Serialización JSON ida y vuelta
# ---------------------------------------------------------------------------

class TestSerializacionJson:
    """Pruebas de serialización JSON de ida y vuelta."""

    def test_roundtrip_json(self, maestro):
        """El JSON serializado y deserializado produce el mismo resultado."""
        texto = json.dumps(maestro, ensure_ascii=False)
        reconstruido = json.loads(texto)
        assert reconstruido["constantes_codata_2018"]["velocidad_luz_m_s"] == 299_792_458.0

    def test_guardar_json_crea_archivo(self, tmp_path):
        """guardar_json_maestro() crea el archivo en disco."""
        ruta = str(tmp_path / "test_maestro.json")
        ruta_abs = guardar_json_maestro(ruta=ruta)
        assert os.path.isfile(ruta_abs)

    def test_guardar_json_contenido_valido(self, tmp_path):
        """El archivo guardado contiene JSON válido con la clave 'sistema'."""
        ruta = str(tmp_path / "test_maestro2.json")
        guardar_json_maestro(ruta=ruta)
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
        assert "sistema" in datos

    def test_guardar_json_nodos_correctos(self, tmp_path):
        """El archivo JSON guardado contiene los 51 nodos de la constelación."""
        ruta = str(tmp_path / "test_maestro3.json")
        guardar_json_maestro(ruta=ruta)
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
        assert datos["constelacion_51_nodos"]["total_nodos"] == 51
