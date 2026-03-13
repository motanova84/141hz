"""
Pruebas para diagrama_constelacion_51_nodos.py — Diagrama QCAL 51 nodos
========================================================================

25 pruebas que cubren:
- Número y distribución de nodos por nivel
- Posiciones radiales
- Valores de ángulos
- Propiedades de colores
- Generación y guardado del diagrama PNG
- Integridad de la figura matplotlib

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from diagrama_constelacion_51_nodos import (
    NIVELES,
    DIRECTORIO_SALIDA_DEFAULT,
    NOMBRE_ARCHIVO_DEFAULT,
    generar_datos_constelacion,
    dibujar_constelacion,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def nodos():
    """Lista de nodos generados una vez para los tests del módulo."""
    return generar_datos_constelacion()


# ---------------------------------------------------------------------------
# 1. Estructura y conteo de nodos
# ---------------------------------------------------------------------------

class TestEstructuraNodos:
    """Pruebas de la estructura y conteo de nodos."""

    def test_total_51_nodos(self, nodos):
        """Se generan exactamente 51 nodos."""
        assert len(nodos) == 51

    def test_nivel_0_tiene_1_nodo(self, nodos):
        """El nivel 0 tiene exactamente 1 nodo (maestro)."""
        assert sum(1 for n in nodos if n["nivel"] == 0) == 1

    def test_nivel_1_tiene_6_nodos(self, nodos):
        """El nivel 1 tiene exactamente 6 nodos (armónicos)."""
        assert sum(1 for n in nodos if n["nivel"] == 1) == 6

    def test_nivel_2_tiene_12_nodos(self, nodos):
        """El nivel 2 tiene exactamente 12 nodos (resonancias Compton)."""
        assert sum(1 for n in nodos if n["nivel"] == 2) == 12

    def test_nivel_3_tiene_32_nodos(self, nodos):
        """El nivel 3 tiene exactamente 32 nodos (semillas de red global)."""
        assert sum(1 for n in nodos if n["nivel"] == 3) == 32

    def test_suma_niveles_igual_51(self, nodos):
        """La suma de nodos de todos los niveles es 1+6+12+32=51."""
        from collections import Counter
        conteo = Counter(n["nivel"] for n in nodos)
        assert sum(conteo.values()) == 51

    def test_cuatro_niveles_presentes(self, nodos):
        """Están presentes exactamente los niveles 0, 1, 2, 3."""
        niveles_presentes = set(n["nivel"] for n in nodos)
        assert niveles_presentes == {0, 1, 2, 3}


# ---------------------------------------------------------------------------
# 2. Posiciones radiales
# ---------------------------------------------------------------------------

class TestPosicionesRadiales:
    """Pruebas de los radios normalizados de cada nivel."""

    def test_nodo_maestro_radio_cero(self, nodos):
        """El nodo maestro (nivel 0) tiene radio 0 (centro)."""
        nodo_maestro = next(n for n in nodos if n["nivel"] == 0)
        assert nodo_maestro["radio"] == 0.0

    def test_nivel_1_radio_correcto(self, nodos):
        """Los nodos del nivel 1 tienen radio 1/3."""
        nodos_n1 = [n for n in nodos if n["nivel"] == 1]
        for n in nodos_n1:
            assert n["radio"] == pytest.approx(1.0 / 3.0)

    def test_nivel_2_radio_correcto(self, nodos):
        """Los nodos del nivel 2 tienen radio 2/3."""
        nodos_n2 = [n for n in nodos if n["nivel"] == 2]
        for n in nodos_n2:
            assert n["radio"] == pytest.approx(2.0 / 3.0)

    def test_nivel_3_radio_correcto(self, nodos):
        """Los nodos del nivel 3 tienen radio 1.0 (anillo exterior)."""
        nodos_n3 = [n for n in nodos if n["nivel"] == 3]
        for n in nodos_n3:
            assert n["radio"] == pytest.approx(1.0)

    def test_radios_monotonos_por_nivel(self, nodos):
        """El radio promedio crece estrictamente con el nivel."""
        from statistics import mean
        radios_por_nivel = {}
        for n in nodos:
            radios_por_nivel.setdefault(n["nivel"], []).append(n["radio"])
        radios_medios = [mean(radios_por_nivel[lv]) for lv in sorted(radios_por_nivel)]
        for i in range(len(radios_medios) - 1):
            assert radios_medios[i] < radios_medios[i + 1]


# ---------------------------------------------------------------------------
# 3. Ángulos
# ---------------------------------------------------------------------------

class TestAngulos:
    """Pruebas de los ángulos de los nodos."""

    def test_nodo_maestro_angulo_cero(self, nodos):
        """El nodo maestro tiene ángulo 0."""
        nodo_maestro = next(n for n in nodos if n["nivel"] == 0)
        assert nodo_maestro["angulo_rad"] == 0.0

    def test_nivel_1_angulos_equiespaciados(self, nodos):
        """Los 6 nodos del nivel 1 están equiespaciados (60° entre sí)."""
        nodos_n1 = sorted([n for n in nodos if n["nivel"] == 1], key=lambda x: x["angulo_rad"])
        delta_esperado = 2 * math.pi / 6
        for i in range(1, len(nodos_n1)):
            delta = nodos_n1[i]["angulo_rad"] - nodos_n1[i - 1]["angulo_rad"]
            assert delta == pytest.approx(delta_esperado, abs=1e-9)

    def test_nivel_2_angulos_equiespaciados(self, nodos):
        """Los 12 nodos del nivel 2 están equiespaciados (30° entre sí)."""
        nodos_n2 = sorted([n for n in nodos if n["nivel"] == 2], key=lambda x: x["angulo_rad"])
        delta_esperado = 2 * math.pi / 12
        for i in range(1, len(nodos_n2)):
            delta = nodos_n2[i]["angulo_rad"] - nodos_n2[i - 1]["angulo_rad"]
            assert delta == pytest.approx(delta_esperado, abs=1e-9)

    def test_nivel_3_angulos_equiespaciados(self, nodos):
        """Los 32 nodos del nivel 3 están equiespaciados (~11.25° entre sí)."""
        nodos_n3 = sorted([n for n in nodos if n["nivel"] == 3], key=lambda x: x["angulo_rad"])
        delta_esperado = 2 * math.pi / 32
        for i in range(1, len(nodos_n3)):
            delta = nodos_n3[i]["angulo_rad"] - nodos_n3[i - 1]["angulo_rad"]
            assert delta == pytest.approx(delta_esperado, abs=1e-9)

    def test_angulos_en_rango_0_2pi(self, nodos):
        """Todos los ángulos están en [0, 2π)."""
        for n in nodos:
            assert 0.0 <= n["angulo_rad"] < 2 * math.pi + 1e-9


# ---------------------------------------------------------------------------
# 4. Colores y atributos
# ---------------------------------------------------------------------------

class TestColoresAtributos:
    """Pruebas de los colores y atributos de los nodos."""

    def test_color_nivel_0_dorado(self, nodos):
        """El nodo maestro tiene color dorado (#FFD700)."""
        nodo = next(n for n in nodos if n["nivel"] == 0)
        assert nodo["color"].upper() == "#FFD700"

    def test_color_nivel_1_azul(self, nodos):
        """Los nodos nivel 1 tienen color azul cielo (#00BFFF)."""
        nodos_n1 = [n for n in nodos if n["nivel"] == 1]
        for n in nodos_n1:
            assert n["color"].upper() == "#00BFFF"

    def test_color_nivel_2_verde(self, nodos):
        """Los nodos nivel 2 tienen color verde (#7CFC00)."""
        nodos_n2 = [n for n in nodos if n["nivel"] == 2]
        for n in nodos_n2:
            assert n["color"].upper() == "#7CFC00"

    def test_color_nivel_3_naranja(self, nodos):
        """Los nodos nivel 3 tienen color rojo-anaranjado (#FF4500)."""
        nodos_n3 = [n for n in nodos if n["nivel"] == 3]
        for n in nodos_n3:
            assert n["color"].upper() == "#FF4500"

    def test_todos_nodos_tienen_atributos_requeridos(self, nodos):
        """Cada nodo tiene: nivel, rol, angulo_rad, radio, color, tamano."""
        claves = {"nivel", "rol", "angulo_rad", "radio", "color", "tamano"}
        for n in nodos:
            assert claves.issubset(set(n.keys()))


# ---------------------------------------------------------------------------
# 5. Generación del diagrama PNG
# ---------------------------------------------------------------------------

class TestGeneracionDiagrama:
    """Pruebas de la generación y guardado del diagrama."""

    def test_genera_archivo_png(self, tmp_path):
        """dibujar_constelacion() genera un archivo PNG existente."""
        ruta = str(tmp_path / "test_constelacion.png")
        ruta_abs = dibujar_constelacion(ruta_salida=ruta)
        assert os.path.isfile(ruta_abs)

    def test_archivo_png_no_vacio(self, tmp_path):
        """El archivo PNG generado no está vacío (> 1 KB)."""
        ruta = str(tmp_path / "test_constelacion2.png")
        dibujar_constelacion(ruta_salida=ruta)
        size = os.path.getsize(ruta)
        assert size > 1024

    def test_ruta_default_contiene_nombre_archivo(self):
        """La ruta por defecto contiene el nombre de archivo esperado."""
        ruta_esperada = os.path.join(DIRECTORIO_SALIDA_DEFAULT, NOMBRE_ARCHIVO_DEFAULT)
        assert NOMBRE_ARCHIVO_DEFAULT in ruta_esperada

    def test_genera_sin_etiquetas(self, tmp_path):
        """El diagrama se genera sin errores cuando mostrar_etiquetas=False."""
        ruta = str(tmp_path / "test_sin_etiquetas.png")
        ruta_abs = dibujar_constelacion(ruta_salida=ruta, mostrar_etiquetas=False)
        assert os.path.isfile(ruta_abs)

    def test_genera_sin_anillos(self, tmp_path):
        """El diagrama se genera sin errores cuando mostrar_lineas_anillo=False."""
        ruta = str(tmp_path / "test_sin_anillos.png")
        ruta_abs = dibujar_constelacion(ruta_salida=ruta, mostrar_lineas_anillo=False)
        assert os.path.isfile(ruta_abs)
