"""
Tests for physics.red_ramsey_qcal — Red de Ramsey QCAL ∴RRQ∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesRedRamsey  – constantes físicas del sistema
  - NodoPrimo            – 7 nodos primos con frecuencias armónicas
  - RedRamsey            – grafo C₇, 21 aristas, coherencia
  - OperadorMaestroHPi   – autovalores, línea crítica, Ψ_espectro
  - SimbiosisHiggsPC     – m*, g_eff, cierre de masa
  - TasaSimbiotica       – R_symb verificación, cierre biológico
  - CoherenciaRedRamsey  – Ψ_global ponderada, 5 cierres
  - SistemaRedRamseyQCAL – integración completa
  - ResultadoRedRamseyQCAL – dataclass de resultados
  - red_ramsey_qcal_activar() – API pública end-to-end

Invariantes clave verificados:
  - f₀ = 141.7001 Hz
  - C₇ = {2, 3, 5, 7, 11, 13, 17}
  - f_p = f₀ · ln(p) para cada primo p
  - Todos los ρₙ = ½ + iγₙ en la línea crítica
  - m* = 125.0 · (1 − 0.053) = 118.375 GeV
  - R_symb = 7 × 141.7001 = 991.9007 kpps
  - Ψ_global ≥ 0.888 (umbral noético)
  - Sello ∴RRQ∞³ ACTIVO
  - RAM-LII-2026-RED-RAMSEY-QCAL
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.red_ramsey_qcal import (
    # Constantes de módulo
    _F0,
    _G_EFF,
    _M_HIGGS_GEV,
    _M_ESTRELLA_GEV,
    _N_NODOS,
    _R_SYMB_KPPS,
    _PSI_UMBRAL,
    _PRIMOS_C7,
    _GAMMA_7,
    _N_ARISTAS,
    _W_NODOS,
    _W_ESPECTRO,
    _W_HIGGS,
    _SELLO,
    _RAM,
    _VERSION,
    # Funciones auxiliares
    _es_primo,
    _frecuencia_armonica,
    # Clases
    ConstantesRedRamsey,
    NodoPrimo,
    RedRamsey,
    OperadorMaestroHPi,
    SimbiosisHiggsPC,
    TasaSimbiotica,
    CoherenciaRedRamsey,
    SistemaRedRamseyQCAL,
    ResultadoRedRamseyQCAL,
    # API pública
    red_ramsey_qcal_activar,
)


# ============================================================================
# TestConstantesRedRamsey – 20 tests
# ============================================================================

class TestConstantesRedRamsey(unittest.TestCase):
    """Tests para las constantes del módulo y la clase ConstantesRedRamsey."""

    def setUp(self):
        self.c = ConstantesRedRamsey()

    def test_f0_module_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_g_eff_module_value(self):
        """_G_EFF debe ser 0.053."""
        self.assertAlmostEqual(_G_EFF, 0.053, places=4)

    def test_m_higgs_module_value(self):
        """_M_HIGGS_GEV debe ser 125.0 GeV."""
        self.assertAlmostEqual(_M_HIGGS_GEV, 125.0, places=4)

    def test_m_estrella_module_value(self):
        """_M_ESTRELLA_GEV debe ser 118.375 GeV."""
        self.assertAlmostEqual(_M_ESTRELLA_GEV, 118.375, places=4)

    def test_n_nodos_module_value(self):
        """_N_NODOS debe ser 7."""
        self.assertEqual(_N_NODOS, 7)

    def test_r_symb_kpps_module_value(self):
        """_R_SYMB_KPPS debe ser 7 × 141.7001 ≈ 991.9007 kpps."""
        self.assertAlmostEqual(_R_SYMB_KPPS, 991.9007, places=3)

    def test_psi_umbral_module_value(self):
        """_PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    def test_n_aristas_module_value(self):
        """_N_ARISTAS debe ser C(7,2) = 21."""
        self.assertEqual(_N_ARISTAS, 21)

    def test_weights_sum_one(self):
        """w_nodos + w_espectro + w_higgs debe ser 1.0."""
        total = _W_NODOS + _W_ESPECTRO + _W_HIGGS
        self.assertAlmostEqual(total, 1.0, places=10)

    def test_sello_string(self):
        """_SELLO debe ser '∴RRQ∞³'."""
        self.assertEqual(_SELLO, "∴RRQ∞³")

    def test_ram_string(self):
        """_RAM debe contener 'RAM-LII-2026-RED-RAMSEY-QCAL'."""
        self.assertIn("RAM-LII-2026", _RAM)
        self.assertIn("RED-RAMSEY-QCAL", _RAM)

    def test_primos_c7_count(self):
        """_PRIMOS_C7 debe tener 7 elementos."""
        self.assertEqual(len(_PRIMOS_C7), 7)

    def test_primos_c7_values(self):
        """_PRIMOS_C7 debe ser (2, 3, 5, 7, 11, 13, 17)."""
        self.assertEqual(_PRIMOS_C7, (2, 3, 5, 7, 11, 13, 17))

    def test_gamma_7_count(self):
        """_GAMMA_7 debe tener 7 elementos."""
        self.assertEqual(len(_GAMMA_7), 7)

    def test_gamma_7_first(self):
        """_GAMMA_7[0] debe ser ≈ 14.135 (primer cero de Riemann)."""
        self.assertAlmostEqual(_GAMMA_7[0], 14.134725, places=5)

    def test_gamma_7_last(self):
        """_GAMMA_7[6] debe ser ≈ 40.919 (séptimo cero de Riemann)."""
        self.assertAlmostEqual(_GAMMA_7[6], 40.918719, places=5)

    def test_constants_class_f0(self):
        """ConstantesRedRamsey.f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_constants_class_m_estrella(self):
        """ConstantesRedRamsey.m_estrella_gev debe ser 118.375 GeV."""
        self.assertAlmostEqual(self.c.m_estrella_gev, 118.375, places=4)

    def test_delta_m_formula(self):
        """delta_m_gev() debe ser m_H × g_eff ≈ 6.625 GeV."""
        self.assertAlmostEqual(self.c.delta_m_gev(), 125.0 * 0.053, places=6)

    def test_es_perturbativo(self):
        """g_eff < 0.1 → régimen perturbativo."""
        self.assertTrue(self.c.es_perturbativo())


# ============================================================================
# TestNodoPrimo – 25 tests
# ============================================================================

class TestNodoPrimo(unittest.TestCase):
    """Tests para la clase NodoPrimo."""

    def test_create_nodo_primo_2(self):
        """NodoPrimo(2) debe crearse sin error."""
        n = NodoPrimo(2)
        self.assertEqual(n.primo, 2)

    def test_create_nodo_primo_7(self):
        """NodoPrimo(7) debe crearse sin error."""
        n = NodoPrimo(7)
        self.assertEqual(n.primo, 7)

    def test_create_nodo_primo_17(self):
        """NodoPrimo(17) debe crearse sin error."""
        n = NodoPrimo(17)
        self.assertEqual(n.primo, 17)

    def test_frecuencia_nodo_2(self):
        """f_2 = f₀ · ln(2) ≈ 98.219 Hz."""
        n = NodoPrimo(2)
        self.assertAlmostEqual(n.frecuencia_hz, 141.7001 * math.log(2), places=4)

    def test_frecuencia_nodo_3(self):
        """f_3 = f₀ · ln(3) ≈ 155.673 Hz."""
        n = NodoPrimo(3)
        self.assertAlmostEqual(n.frecuencia_hz, 141.7001 * math.log(3), places=4)

    def test_frecuencia_nodo_5(self):
        """f_5 = f₀ · ln(5) ≈ 228.058 Hz."""
        n = NodoPrimo(5)
        self.assertAlmostEqual(n.frecuencia_hz, 141.7001 * math.log(5), places=4)

    def test_frecuencia_nodo_7(self):
        """f_7 = f₀ · ln(7) ≈ 275.736 Hz."""
        n = NodoPrimo(7)
        self.assertAlmostEqual(n.frecuencia_hz, 141.7001 * math.log(7), places=4)

    def test_frecuencia_nodo_11(self):
        """f_11 = f₀ · ln(11) ≈ 339.782 Hz."""
        n = NodoPrimo(11)
        self.assertAlmostEqual(n.frecuencia_hz, 141.7001 * math.log(11), places=4)

    def test_frecuencia_nodo_13(self):
        """f_13 = f₀ · ln(13) ≈ 363.454 Hz."""
        n = NodoPrimo(13)
        self.assertAlmostEqual(n.frecuencia_hz, 141.7001 * math.log(13), places=4)

    def test_frecuencia_nodo_17(self):
        """f_17 = f₀ · ln(17) ≈ 401.467 Hz."""
        n = NodoPrimo(17)
        self.assertAlmostEqual(n.frecuencia_hz, 141.7001 * math.log(17), places=4)

    def test_es_primo_2(self):
        """NodoPrimo(2).es_primo() debe ser True."""
        self.assertTrue(NodoPrimo(2).es_primo())

    def test_es_primo_7(self):
        """NodoPrimo(7).es_primo() debe ser True."""
        self.assertTrue(NodoPrimo(7).es_primo())

    def test_es_primo_17(self):
        """NodoPrimo(17).es_primo() debe ser True."""
        self.assertTrue(NodoPrimo(17).es_primo())

    def test_no_es_primo_4(self):
        """NodoPrimo(4).es_primo() debe ser False."""
        self.assertFalse(NodoPrimo(4).es_primo())

    def test_no_es_primo_1(self):
        """NodoPrimo(1).es_primo() debe ser False."""
        self.assertFalse(NodoPrimo(1).es_primo())

    def test_coherencia_nodo_primo_es_uno(self):
        """coherencia_nodo() debe ser 1.0 para un primo válido."""
        for p in (2, 3, 5, 7, 11, 13, 17):
            self.assertAlmostEqual(NodoPrimo(p).coherencia_nodo(), 1.0)

    def test_coherencia_nodo_no_primo_es_cero(self):
        """coherencia_nodo() debe ser 0.0 para un número no primo."""
        self.assertAlmostEqual(NodoPrimo(4).coherencia_nodo(), 0.0)

    def test_noetic_desc_2(self):
        """NodoPrimo(2).funcion_noetica debe contener 'Dualidad'."""
        self.assertIn("Dualidad", NodoPrimo(2).funcion_noetica)

    def test_noetic_desc_7(self):
        """NodoPrimo(7).funcion_noetica debe contener 'Septenario'."""
        self.assertIn("Septenario", NodoPrimo(7).funcion_noetica)

    def test_noetic_desc_17(self):
        """NodoPrimo(17).funcion_noetica debe contener 'Puerta'."""
        self.assertIn("Puerta", NodoPrimo(17).funcion_noetica)

    def test_frecuencia_positiva_todos_primos(self):
        """Todos los nodos C₇ deben tener frecuencia positiva."""
        for p in _PRIMOS_C7:
            self.assertGreater(NodoPrimo(p).frecuencia_hz, 0)

    def test_frecuencia_armonica_helper(self):
        """_frecuencia_armonica(p, f0) debe ser f0 × ln(p)."""
        for p in _PRIMOS_C7:
            expected = 141.7001 * math.log(p)
            self.assertAlmostEqual(_frecuencia_armonica(p), expected, places=6)

    def test_ln_primo_2(self):
        """NodoPrimo(2).ln_primo() debe ser ln(2)."""
        self.assertAlmostEqual(NodoPrimo(2).ln_primo(), math.log(2), places=12)

    def test_nodo_repr_contains_hz(self):
        """repr(NodoPrimo(7)) debe contener 'Hz'."""
        self.assertIn("Hz", repr(NodoPrimo(7)))

    def test_es_primo_helper_small_primes(self):
        """_es_primo(p) debe ser True para todos los primos de C₇."""
        for p in _PRIMOS_C7:
            self.assertTrue(_es_primo(p))


# ============================================================================
# TestRedRamsey – 22 tests
# ============================================================================

class TestRedRamsey(unittest.TestCase):
    """Tests para la clase RedRamsey."""

    def setUp(self):
        self.red = RedRamsey()

    def test_create_red_ramsey(self):
        """RedRamsey() debe crearse sin error."""
        r = RedRamsey()
        self.assertIsNotNone(r)

    def test_n_nodos_7(self):
        """La red debe tener 7 nodos."""
        self.assertEqual(self.red.n_nodos, 7)

    def test_nodos_son_primos(self):
        """Todos los nodos deben ser primos."""
        for nodo in self.red.nodos:
            self.assertTrue(nodo.es_primo(), f"p={nodo.primo} no es primo")

    def test_n_aristas_posibles_21(self):
        """C(7,2) = 21 aristas potenciales."""
        self.assertEqual(self.red.n_aristas_posibles, 21)

    def test_frecuencias_positivas(self):
        """Todas las frecuencias deben ser positivas."""
        for f in self.red.frecuencias_hz():
            self.assertGreater(f, 0)

    def test_primos_correctos(self):
        """Los primos deben ser exactamente C₇ = {2,3,5,7,11,13,17}."""
        self.assertEqual(self.red.primos(), _PRIMOS_C7)

    def test_psi_nodos_uno(self):
        """Ψ_nodos debe ser 1.0 (todos los 7 nodos son primos válidos)."""
        self.assertAlmostEqual(self.red.psi_nodos(), 1.0, places=10)

    def test_psi_nodos_gte_umbral(self):
        """Ψ_nodos debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.red.psi_nodos(), 0.888)

    def test_cierre_nodos_true(self):
        """cierre_nodos() debe retornar True."""
        self.assertTrue(self.red.cierre_nodos())

    def test_frecuencias_ordenadas(self):
        """Las frecuencias deben estar en orden creciente (ln creciente)."""
        freqs = self.red.frecuencias_hz()
        for i in range(len(freqs) - 1):
            self.assertLess(freqs[i], freqs[i + 1])

    def test_nodo_2_frecuencia(self):
        """f_2 ≈ 98.219 Hz."""
        espectro = self.red.espectro_hz()
        self.assertAlmostEqual(espectro[2], 141.7001 * math.log(2), places=3)

    def test_nodo_17_frecuencia(self):
        """f_17 ≈ 401.467 Hz."""
        espectro = self.red.espectro_hz()
        self.assertAlmostEqual(espectro[17], 141.7001 * math.log(17), places=3)

    def test_espectro_hz_keys(self):
        """espectro_hz() debe contener todos los primos C₇ como claves."""
        espectro = self.red.espectro_hz()
        for p in _PRIMOS_C7:
            self.assertIn(p, espectro)

    def test_min_frecuencia(self):
        """La frecuencia mínima debe ser f_2 ≈ 98 Hz."""
        freqs = self.red.frecuencias_hz()
        self.assertAlmostEqual(min(freqs), 141.7001 * math.log(2), places=3)

    def test_max_frecuencia(self):
        """La frecuencia máxima debe ser f_17 ≈ 401 Hz."""
        freqs = self.red.frecuencias_hz()
        self.assertAlmostEqual(max(freqs), 141.7001 * math.log(17), places=3)

    def test_nodos_list_length(self):
        """red.nodos debe retornar una lista de 7 NodoPrimo."""
        nodos = self.red.nodos
        self.assertEqual(len(nodos), 7)

    def test_all_nodes_prime(self):
        """Todos los nodos deben ser instancias de NodoPrimo."""
        for nodo in self.red.nodos:
            self.assertIsInstance(nodo, NodoPrimo)

    def test_red_repr_contains_aristas(self):
        """repr(RedRamsey()) debe contener la info de aristas."""
        r = repr(self.red)
        self.assertIn("21", r)

    def test_frecuencias_rango_audible(self):
        """Las frecuencias deben estar en el rango [50, 500] Hz."""
        for f in self.red.frecuencias_hz():
            self.assertGreater(f, 50.0)
            self.assertLess(f, 500.0)

    def test_red_default_f0(self):
        """RedRamsey() debe usar f₀ = 141.7001 Hz por defecto."""
        self.assertAlmostEqual(self.red.f0, 141.7001, places=4)

    def test_red_custom_f0(self):
        """RedRamsey(f0=100.0) debe usar f₀ = 100.0 Hz."""
        r = RedRamsey(f0=100.0)
        self.assertAlmostEqual(r.f0, 100.0, places=10)

    def test_n_nodos_aristas_formula(self):
        """Para n=7: C(7,2) = 7×6/2 = 21."""
        n = self.red.n_nodos
        expected = n * (n - 1) // 2
        self.assertEqual(self.red.n_aristas_posibles, expected)


# ============================================================================
# TestOperadorMaestroHPi – 25 tests
# ============================================================================

class TestOperadorMaestroHPi(unittest.TestCase):
    """Tests para la clase OperadorMaestroHPi."""

    def setUp(self):
        self.op = OperadorMaestroHPi()

    def test_create_operador(self):
        """OperadorMaestroHPi() debe crearse sin error."""
        self.assertIsNotNone(self.op)

    def test_n_zeros_7(self):
        """El operador debe tener 7 ceros de Riemann."""
        self.assertEqual(self.op.n_zeros, 7)

    def test_autovalores_count(self):
        """autovalores() debe retornar 7 elementos."""
        self.assertEqual(len(self.op.autovalores()), 7)

    def test_autovalores_real_part_half(self):
        """Todos los autovalores deben tener parte real = ½."""
        for re, im in self.op.autovalores():
            self.assertAlmostEqual(re, 0.5, places=12)

    def test_autovalores_imag_part_positive(self):
        """Todos los autovalores deben tener parte imaginaria positiva."""
        for re, im in self.op.autovalores():
            self.assertGreater(im, 0)

    def test_es_autoadjunto(self):
        """El operador debe ser autoadjunto."""
        self.assertTrue(self.op.es_autoadjunto())

    def test_fraccion_linea_critica_uno(self):
        """Todos los autovalores deben estar en la línea crítica (= 1.0)."""
        self.assertAlmostEqual(self.op.fraccion_en_linea_critica(), 1.0, places=10)

    def test_psi_espectro_range(self):
        """Ψ_espectro debe estar en [0, 1]."""
        psi = self.op.psi_espectro()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_espectro_gte_umbral(self):
        """Ψ_espectro debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.op.psi_espectro(), 0.888)

    def test_cierre_espectro_true(self):
        """cierre_espectro() debe retornar True."""
        self.assertTrue(self.op.cierre_espectro())

    def test_gamma_1_value(self):
        """γ₁ ≈ 14.134725."""
        self.assertAlmostEqual(self.op.gamma_n(0), 14.134725, places=5)

    def test_gamma_7_value(self):
        """γ₇ ≈ 40.918719."""
        self.assertAlmostEqual(self.op.gamma_n(6), 40.918719, places=5)

    def test_gamma_2_value(self):
        """γ₂ ≈ 21.022039."""
        self.assertAlmostEqual(self.op.gamma_n(1), 21.022039, places=5)

    def test_gamma_4_value(self):
        """γ₄ ≈ 30.424876."""
        self.assertAlmostEqual(self.op.gamma_n(3), 30.424876, places=5)

    def test_zeros_increasing(self):
        """Los ceros deben estar en orden estrictamente creciente."""
        gammas = [self.op.gamma_n(i) for i in range(self.op.n_zeros)]
        for i in range(len(gammas) - 1):
            self.assertLess(gammas[i], gammas[i + 1])

    def test_zeros_all_positive(self):
        """Todos los γₙ deben ser positivos."""
        for i in range(self.op.n_zeros):
            self.assertGreater(self.op.gamma_n(i), 0)

    def test_rho_1_real_part(self):
        """ρ₁ = (0.5, γ₁) — parte real = 0.5."""
        re, im = self.op.autovalores()[0]
        self.assertAlmostEqual(re, 0.5, places=12)

    def test_rho_7_imag_part(self):
        """ρ₇ parte imaginaria ≈ 40.919."""
        re, im = self.op.autovalores()[6]
        self.assertAlmostEqual(im, 40.918719, places=5)

    def test_espaciado_medio_empirico_positive(self):
        """El espaciado medio empírico debe ser positivo."""
        self.assertGreater(self.op.espaciado_medio_empirico(), 0)

    def test_espaciado_medio_weyl_positive(self):
        """El espaciado medio de Weyl debe ser positivo y finito."""
        d = self.op.espaciado_medio_weyl()
        self.assertGreater(d, 0)
        self.assertFalse(math.isinf(d))

    def test_all_rho_on_critical_line(self):
        """Todos los ρₙ deben tener parte real = ½."""
        for re, im in self.op.autovalores():
            self.assertAlmostEqual(re, 0.5, places=10)

    def test_descripcion_espectral_string(self):
        """descripcion_espectral() debe retornar una cadena no vacía."""
        desc = self.op.descripcion_espectral()
        self.assertIsInstance(desc, str)
        self.assertGreater(len(desc), 0)

    def test_operador_repr(self):
        """repr(OperadorMaestroHPi()) debe contener info del operador."""
        r = repr(self.op)
        self.assertIn("OperadorMaestroHPi", r)

    def test_psi_espectro_high(self):
        """Ψ_espectro debe ser > 0.9 (espectro muy coherente)."""
        self.assertGreater(self.op.psi_espectro(), 0.9)

    def test_fraccion_linea_critica_completa(self):
        """fraccion_en_linea_critica() debe ser 1.0 exacto (7/7)."""
        self.assertEqual(self.op.fraccion_en_linea_critica(), 1.0)


# ============================================================================
# TestSimbiosisHiggsPC – 22 tests
# ============================================================================

class TestSimbiosisHiggsPC(unittest.TestCase):
    """Tests para la clase SimbiosisHiggsPC."""

    def setUp(self):
        self.s = SimbiosisHiggsPC()

    def test_create_simbiosis(self):
        """SimbiosisHiggsPC() debe crearse sin error."""
        self.assertIsNotNone(self.s)

    def test_m_higgs_value(self):
        """m_H debe ser 125.0 GeV/c²."""
        self.assertAlmostEqual(self.s.m_higgs_gev, 125.0, places=4)

    def test_g_eff_value(self):
        """g_eff debe ser 0.053."""
        self.assertAlmostEqual(self.s.g_eff, 0.053, places=4)

    def test_m_estrella_value(self):
        """m* debe ser 118.375 GeV/c²."""
        self.assertAlmostEqual(self.s.m_estrella_gev(), 118.375, places=4)

    def test_m_estrella_formula(self):
        """m* = m_H · (1 − g_eff) = 125.0 · 0.947 = 118.375."""
        expected = 125.0 * (1.0 - 0.053)
        self.assertAlmostEqual(self.s.m_estrella_gev(), expected, places=10)

    def test_delta_m_value(self):
        """Δm = m_H · g_eff = 125.0 · 0.053 = 6.625 GeV."""
        self.assertAlmostEqual(self.s.delta_m_gev(), 6.625, places=4)

    def test_m_estrella_lt_m_higgs(self):
        """m* debe ser menor que m_H."""
        self.assertLess(self.s.m_estrella_gev(), self.s.m_higgs_gev)

    def test_cierre_higgs_true(self):
        """cierre_higgs() debe retornar True."""
        self.assertTrue(self.s.cierre_higgs())

    def test_psi_higgs_uno(self):
        """Ψ_higgs debe ser 1.0 para el caso exacto."""
        self.assertAlmostEqual(self.s.psi_higgs(), 1.0, places=10)

    def test_psi_higgs_gte_umbral(self):
        """Ψ_higgs debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.s.psi_higgs(), 0.888)

    def test_es_perturbativo(self):
        """g_eff = 0.053 < 0.1 → régimen perturbativo."""
        self.assertTrue(self.s.es_perturbativo())

    def test_fraccion_modulacion(self):
        """fraccion_modulacion() debe ser g_eff = 0.053."""
        self.assertAlmostEqual(self.s.fraccion_modulacion(), 0.053, places=4)

    def test_fraccion_lt_10_percent(self):
        """La fracción de modulación debe ser < 10%."""
        self.assertLess(self.s.fraccion_modulacion(), 0.1)

    def test_lagrangiano_interaccion_negativo(self):
        """ℒ_int = −g_eff · |ψ|² · H debe ser negativo."""
        self.assertLess(self.s.lagrangiano_interaccion(), 0)

    def test_cierre_higgs_tolerancia(self):
        """cierre_higgs() con tolerancia 0.01 debe ser True."""
        self.assertTrue(self.s.cierre_higgs(tolerancia_gev=0.01))

    def test_simbiosis_custom_params(self):
        """SimbiosisHiggsPC(125.0, 0.053) debe dar m* = 118.375."""
        s = SimbiosisHiggsPC(m_higgs_gev=125.0, g_eff=0.053)
        self.assertAlmostEqual(s.m_estrella_gev(), 118.375, places=4)

    def test_delta_m_reduccion_5_3_percent(self):
        """La reducción Δm/m_H debe ser ≈ 5.3%."""
        frac = self.s.delta_m_gev() / self.s.m_higgs_gev
        self.assertAlmostEqual(frac, 0.053, places=4)

    def test_m_estrella_positiva(self):
        """m* debe ser positivo."""
        self.assertGreater(self.s.m_estrella_gev(), 0)

    def test_psi_higgs_range(self):
        """Ψ_higgs debe estar en [0, 1]."""
        psi = self.s.psi_higgs()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_simbiosis_repr(self):
        """repr(SimbiosisHiggsPC()) debe contener info."""
        r = repr(self.s)
        self.assertIn("SimbiosisHiggsPC", r)

    def test_m_estrella_gev_exacto(self):
        """_M_ESTRELLA_GEV debe coincidir con m_estrella_gev()."""
        self.assertAlmostEqual(self.s.m_estrella_gev(), _M_ESTRELLA_GEV, places=10)

    def test_delta_m_positivo(self):
        """Δm debe ser positivo."""
        self.assertGreater(self.s.delta_m_gev(), 0)


# ============================================================================
# TestTasaSimbiotitica – 22 tests
# ============================================================================

class TestTasaSimbiotitica(unittest.TestCase):
    """Tests para la clase TasaSimbiotica."""

    def setUp(self):
        self.t = TasaSimbiotica()

    def test_create_tasa(self):
        """TasaSimbiotica() debe crearse sin error."""
        self.assertIsNotNone(self.t)

    def test_n_nodos_7(self):
        """n_nodos debe ser 7."""
        self.assertEqual(self.t.n_nodos, 7)

    def test_f0_value(self):
        """f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.t.f0, 141.7001, places=4)

    def test_psi_coherencia_uno(self):
        """psi_coherencia por defecto debe ser 1.0."""
        self.assertAlmostEqual(self.t.psi_coherencia, 1.0, places=10)

    def test_r_symb_value(self):
        """R_symb debe ser 7 × 141.7001 ≈ 991.9007 kpps."""
        self.assertAlmostEqual(self.t.r_symb(), 991.9007, places=3)

    def test_r_symb_formula(self):
        """R_symb = N · f₀ · Ψ."""
        expected = 7 * 141.7001 * 1.0
        self.assertAlmostEqual(self.t.r_symb(), expected, places=6)

    def test_r_symb_kpps(self):
        """r_symb_kpps() debe coincidir con r_symb()."""
        self.assertAlmostEqual(self.t.r_symb_kpps(), self.t.r_symb(), places=12)

    def test_cierre_tasa_true(self):
        """cierre_tasa() debe retornar True."""
        self.assertTrue(self.t.cierre_tasa())

    def test_error_relativo_cero(self):
        """El error relativo con Ψ=1 debe ser ≈ 0."""
        self.assertAlmostEqual(self.t.error_relativo(), 0.0, places=8)

    def test_r_symb_gt_880(self):
        """R_symb debe ser > 880 kpps (por encima del umbral mínimo 0.888)."""
        self.assertGreater(self.t.r_symb(), 880.0)

    def test_psi_tasa_uno(self):
        """Ψ_tasa debe ser 1.0 para error_relativo = 0."""
        self.assertAlmostEqual(self.t.psi_tasa(), 1.0, places=8)

    def test_psi_tasa_gte_umbral(self):
        """Ψ_tasa debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.t.psi_tasa(), 0.888)

    def test_estado_optimo(self):
        """estado() debe ser 'ÓPTIMO' cuando error < 0.001."""
        self.assertEqual(self.t.estado(), "ÓPTIMO")

    def test_cierre_tasa_tolerancia_1percent(self):
        """cierre_tasa(0.01) con R_symb exacto debe ser True."""
        self.assertTrue(self.t.cierre_tasa(tolerancia=0.01))

    def test_tasa_custom_psi(self):
        """TasaSimbiotica(psi_coherencia=0.9) debe dar R_symb = 7×141.7001×0.9."""
        t = TasaSimbiotica(psi_coherencia=0.9)
        expected = 7 * 141.7001 * 0.9
        self.assertAlmostEqual(t.r_symb(), expected, places=6)

    def test_r_symb_module_constant(self):
        """r_symb() debe coincidir con _R_SYMB_KPPS."""
        self.assertAlmostEqual(self.t.r_symb(), _R_SYMB_KPPS, places=6)

    def test_tasa_repr(self):
        """repr(TasaSimbiotica()) debe contener 'kpps'."""
        self.assertIn("kpps", repr(self.t))

    def test_cierre_biologico(self):
        """cierre_tasa() representa el Cierre 4 — BIOLÓGICO."""
        self.assertTrue(self.t.cierre_tasa())

    def test_tasa_n_nodos_formula(self):
        """r_symb() = n_nodos × f0 × psi_coherencia."""
        r = self.t.r_symb()
        expected = self.t.n_nodos * self.t.f0 * self.t.psi_coherencia
        self.assertAlmostEqual(r, expected, places=10)

    def test_psi_tasa_range(self):
        """Ψ_tasa debe estar en [0, 1]."""
        psi = self.t.psi_tasa()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_tasa_cero_error_relativo(self):
        """Con Ψ=1.0, R_symb = 7×141.7001, error = 0."""
        self.assertLess(self.t.error_relativo(), 1e-6)

    def test_r_symb_aprox_992(self):
        """R_symb debe estar entre 990 y 993 kpps."""
        r = self.t.r_symb()
        self.assertGreater(r, 990.0)
        self.assertLess(r, 993.0)


# ============================================================================
# TestCoherenciaRedRamsey – 27 tests
# ============================================================================

class TestCoherenciaRedRamsey(unittest.TestCase):
    """Tests para la clase CoherenciaRedRamsey."""

    def setUp(self):
        self.c = CoherenciaRedRamsey()

    def test_create_coherencia(self):
        """CoherenciaRedRamsey() debe crearse sin error."""
        self.assertIsNotNone(self.c)

    def test_psi_global_range(self):
        """Ψ_global debe estar en [0, 1]."""
        psi = self.c.psi_global()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_global_gte_umbral(self):
        """Ψ_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.c.psi_global(), 0.888)

    def test_sello_activo(self):
        """sello_activo() debe retornar True."""
        self.assertTrue(self.c.sello_activo())

    def test_todos_los_cierres_true(self):
        """todos_los_cierres() debe retornar True."""
        self.assertTrue(self.c.todos_los_cierres())

    def test_cierre_1_aritmetico(self):
        """Cierre 1 — ARITMÉTICO debe estar activo."""
        self.assertTrue(self.c.cierre_1_aritmético())

    def test_cierre_2_hidrodinamico(self):
        """Cierre 2 — HIDRODINÁMICO debe estar activo."""
        self.assertTrue(self.c.cierre_2_hidrodinamico())

    def test_cierre_3_masa(self):
        """Cierre 3 — MASA debe estar activo."""
        self.assertTrue(self.c.cierre_3_masa())

    def test_cierre_4_biologico(self):
        """Cierre 4 — BIOLÓGICO debe estar activo."""
        self.assertTrue(self.c.cierre_4_biologico())

    def test_cierre_5_unificacion(self):
        """Cierre 5 — UNIFICACIÓN debe estar activo."""
        self.assertTrue(self.c.cierre_5_unificacion())

    def test_n_cierres_5(self):
        """El diccionario cierres() debe tener 5 entradas."""
        self.assertEqual(len(self.c.cierres()), 5)

    def test_cierres_all_true(self):
        """Todos los cierres en el diccionario deben ser True."""
        for nombre, estado in self.c.cierres().items():
            self.assertTrue(estado, f"Cierre '{nombre}' debe ser True")

    def test_psi_nodos_range(self):
        """Ψ_nodos debe estar en [0, 1]."""
        psi = self.c.psi_nodos()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_espectro_range(self):
        """Ψ_espectro debe estar en [0, 1]."""
        psi = self.c.psi_espectro()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_higgs_range(self):
        """Ψ_higgs debe estar en [0, 1]."""
        psi = self.c.psi_higgs()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_global_formula(self):
        """Ψ_global = 0.35·Ψ_n + 0.35·Ψ_e + 0.30·Ψ_h."""
        expected = (
            0.35 * self.c.psi_nodos()
            + 0.35 * self.c.psi_espectro()
            + 0.30 * self.c.psi_higgs()
        )
        self.assertAlmostEqual(self.c.psi_global(), expected, places=10)

    def test_coherencias_individuales_keys(self):
        """coherencias_individuales() debe contener las 4 claves esperadas."""
        cohs = self.c.coherencias_individuales()
        for key in ("psi_nodos", "psi_espectro", "psi_higgs", "psi_global"):
            self.assertIn(key, cohs)

    def test_coherencias_individuales_range(self):
        """Todas las coherencias individuales deben estar en [0, 1]."""
        for nombre, valor in self.c.coherencias_individuales().items():
            self.assertGreaterEqual(valor, 0.0, f"{nombre} < 0")
            self.assertLessEqual(valor, 1.0, f"{nombre} > 1")

    def test_validar_returns_dict(self):
        """validar() debe retornar un dict."""
        self.assertIsInstance(self.c.validar(), dict)

    def test_validar_sello_activo(self):
        """validar()['sello_activo'] debe ser True."""
        self.assertTrue(self.c.validar()["sello_activo"])

    def test_validar_todos_los_cierres(self):
        """validar()['todos_los_cierres'] debe ser True."""
        self.assertTrue(self.c.validar()["todos_los_cierres"])

    def test_validar_diferencia_umbral_positiva(self):
        """validar()['diferencia_umbral'] debe ser ≥ 0."""
        self.assertGreaterEqual(self.c.validar()["diferencia_umbral"], 0.0)

    def test_psi_global_high(self):
        """Ψ_global debe ser > 0.9."""
        self.assertGreater(self.c.psi_global(), 0.9)

    def test_pesos_w_nodos(self):
        """El peso de Ψ_nodos debe ser 0.35."""
        self.assertAlmostEqual(_W_NODOS, 0.35, places=10)

    def test_pesos_w_espectro(self):
        """El peso de Ψ_espectro debe ser 0.35."""
        self.assertAlmostEqual(_W_ESPECTRO, 0.35, places=10)

    def test_pesos_w_higgs(self):
        """El peso de Ψ_higgs debe ser 0.30."""
        self.assertAlmostEqual(_W_HIGGS, 0.30, places=10)

    def test_coherencia_repr(self):
        """repr(CoherenciaRedRamsey()) debe contener 'Ψ_global'."""
        r = repr(self.c)
        self.assertIn("Coherencia", r)


# ============================================================================
# TestSistemaRedRamseyQCAL – 25 tests
# ============================================================================

class TestSistemaRedRamseyQCAL(unittest.TestCase):
    """Tests para la clase SistemaRedRamseyQCAL."""

    def setUp(self):
        self.s = SistemaRedRamseyQCAL()
        self.r = self.s.activar()

    def test_create_sistema(self):
        """SistemaRedRamseyQCAL() debe crearse sin error."""
        self.assertIsNotNone(self.s)

    def test_sistema_has_constantes(self):
        """El sistema debe tener atributo 'constantes'."""
        self.assertIsInstance(self.s.constantes, ConstantesRedRamsey)

    def test_sistema_has_red(self):
        """El sistema debe tener atributo 'red'."""
        self.assertIsInstance(self.s.red, RedRamsey)

    def test_sistema_has_operador(self):
        """El sistema debe tener atributo 'operador'."""
        self.assertIsInstance(self.s.operador, OperadorMaestroHPi)

    def test_sistema_has_simbiosis(self):
        """El sistema debe tener atributo 'simbiosis'."""
        self.assertIsInstance(self.s.simbiosis, SimbiosisHiggsPC)

    def test_sistema_has_tasa(self):
        """El sistema debe tener atributo 'tasa'."""
        self.assertIsInstance(self.s.tasa, TasaSimbiotica)

    def test_sistema_has_coherencia(self):
        """El sistema debe tener atributo 'coherencia'."""
        self.assertIsInstance(self.s.coherencia, CoherenciaRedRamsey)

    def test_activar_returns_dict(self):
        """activar() debe retornar un diccionario."""
        self.assertIsInstance(self.r, dict)

    def test_activar_sello(self):
        """activar()['sello'] debe ser '∴RRQ∞³'."""
        self.assertEqual(self.r["sello"], "∴RRQ∞³")

    def test_activar_psi_global_gte_umbral(self):
        """activar()['psi_global'] debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.r["psi_global"], 0.888)

    def test_activar_estado_activo(self):
        """activar()['estado'] debe ser 'ACTIVO'."""
        self.assertEqual(self.r["estado"], "ACTIVO")

    def test_activar_r_symb_kpps(self):
        """activar()['r_symb_kpps'] debe ser ≈ 991.9007 kpps."""
        self.assertAlmostEqual(self.r["r_symb_kpps"], 991.9007, places=3)

    def test_activar_m_estrella(self):
        """activar()['m_estrella'] debe ser 118.375 GeV."""
        self.assertAlmostEqual(self.r["m_estrella"], 118.375, places=4)

    def test_activar_todos_los_cierres(self):
        """activar()['todos_los_cierres'] debe ser True."""
        self.assertTrue(self.r["todos_los_cierres"])

    def test_activar_ram(self):
        """activar()['ram'] debe ser 'RAM-LII-2026-RED-RAMSEY-QCAL'."""
        self.assertEqual(self.r["ram"], "RAM-LII-2026-RED-RAMSEY-QCAL")

    def test_activar_version(self):
        """activar()['version'] debe contener 'QCAL-SYMBIO-BRIDGE'."""
        self.assertIn("QCAL-SYMBIO-BRIDGE", self.r["version"])

    def test_activar_n_nodos(self):
        """activar()['n_nodos'] debe ser 7."""
        self.assertEqual(self.r["n_nodos"], 7)

    def test_activar_primos(self):
        """activar()['primos'] debe ser (2,3,5,7,11,13,17)."""
        self.assertEqual(self.r["primos"], (2, 3, 5, 7, 11, 13, 17))

    def test_activar_sello_activo(self):
        """activar()['sello_activo'] debe ser True."""
        self.assertTrue(self.r["sello_activo"])

    def test_activar_cierre_nodos(self):
        """activar()['cierre_nodos'] debe ser True."""
        self.assertTrue(self.r["cierre_nodos"])

    def test_activar_cierre_espectro(self):
        """activar()['cierre_espectro'] debe ser True."""
        self.assertTrue(self.r["cierre_espectro"])

    def test_activar_cierre_higgs(self):
        """activar()['cierre_higgs'] debe ser True."""
        self.assertTrue(self.r["cierre_higgs"])

    def test_activar_cierre_tasa(self):
        """activar()['cierre_tasa'] debe ser True."""
        self.assertTrue(self.r["cierre_tasa"])

    def test_activar_cierre_coherencia(self):
        """activar()['cierre_coherencia'] debe ser True."""
        self.assertTrue(self.r["cierre_coherencia"])

    def test_sistema_repr(self):
        """repr(SistemaRedRamseyQCAL()) debe contener '∴RRQ∞³'."""
        r = repr(self.s)
        self.assertIn("∴RRQ∞³", r)


# ============================================================================
# TestActivarRedRamseyQCAL – 35 tests
# ============================================================================

class TestActivarRedRamseyQCAL(unittest.TestCase):
    """Tests para la función API red_ramsey_qcal_activar()."""

    def setUp(self):
        self.r = red_ramsey_qcal_activar()

    def test_api_returns_dict(self):
        """red_ramsey_qcal_activar() debe retornar un dict."""
        self.assertIsInstance(self.r, dict)

    def test_api_sello(self):
        """'sello' debe ser '∴RRQ∞³'."""
        self.assertEqual(self.r["sello"], "∴RRQ∞³")

    def test_api_sello_activo(self):
        """'sello_activo' debe ser True."""
        self.assertTrue(self.r["sello_activo"])

    def test_api_psi_global_float(self):
        """'psi_global' debe ser un float."""
        self.assertIsInstance(self.r["psi_global"], float)

    def test_api_psi_global_gte_088(self):
        """'psi_global' debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.r["psi_global"], 0.888)

    def test_api_psi_global_range(self):
        """'psi_global' debe estar en [0, 1]."""
        self.assertGreaterEqual(self.r["psi_global"], 0.0)
        self.assertLessEqual(self.r["psi_global"], 1.0)

    def test_api_estado_activo(self):
        """'estado' debe ser 'ACTIVO'."""
        self.assertEqual(self.r["estado"], "ACTIVO")

    def test_api_estado_string(self):
        """'estado' debe ser un str."""
        self.assertIsInstance(self.r["estado"], str)

    def test_api_r_symb_kpps(self):
        """'r_symb_kpps' debe ser ≈ 991.9007 kpps."""
        self.assertAlmostEqual(self.r["r_symb_kpps"], 991.9007, places=3)

    def test_api_r_symb_kpps_float(self):
        """'r_symb_kpps' debe ser un float."""
        self.assertIsInstance(self.r["r_symb_kpps"], float)

    def test_api_m_estrella(self):
        """'m_estrella' debe ser 118.375 GeV."""
        self.assertAlmostEqual(self.r["m_estrella"], 118.375, places=4)

    def test_api_m_estrella_float(self):
        """'m_estrella' debe ser un float."""
        self.assertIsInstance(self.r["m_estrella"], float)

    def test_api_todos_los_cierres(self):
        """'todos_los_cierres' debe ser True."""
        self.assertTrue(self.r["todos_los_cierres"])

    def test_api_todos_los_cierres_bool(self):
        """'todos_los_cierres' debe ser un bool."""
        self.assertIsInstance(self.r["todos_los_cierres"], bool)

    def test_api_ram(self):
        """'ram' debe ser 'RAM-LII-2026-RED-RAMSEY-QCAL'."""
        self.assertEqual(self.r["ram"], "RAM-LII-2026-RED-RAMSEY-QCAL")

    def test_api_version(self):
        """'version' debe contener 'QCAL-SYMBIO-BRIDGE'."""
        self.assertIn("QCAL-SYMBIO-BRIDGE", self.r["version"])

    def test_api_n_nodos(self):
        """'n_nodos' debe ser 7."""
        self.assertEqual(self.r["n_nodos"], 7)

    def test_api_primos(self):
        """'primos' debe ser (2,3,5,7,11,13,17)."""
        self.assertEqual(self.r["primos"], (2, 3, 5, 7, 11, 13, 17))

    def test_api_f0(self):
        """'f0_hz' debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.r["f0_hz"], 141.7001, places=4)

    def test_api_g_eff(self):
        """'g_eff' debe ser 0.053."""
        self.assertAlmostEqual(self.r["g_eff"], 0.053, places=4)

    def test_api_cierre_nodos(self):
        """'cierre_nodos' debe ser True."""
        self.assertTrue(self.r["cierre_nodos"])

    def test_api_cierre_espectro(self):
        """'cierre_espectro' debe ser True."""
        self.assertTrue(self.r["cierre_espectro"])

    def test_api_cierre_higgs(self):
        """'cierre_higgs' debe ser True."""
        self.assertTrue(self.r["cierre_higgs"])

    def test_api_cierre_tasa(self):
        """'cierre_tasa' debe ser True."""
        self.assertTrue(self.r["cierre_tasa"])

    def test_api_cierre_coherencia(self):
        """'cierre_coherencia' debe ser True."""
        self.assertTrue(self.r["cierre_coherencia"])

    def test_api_psi_nodos(self):
        """'psi_nodos' debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.r["psi_nodos"], 0.888)

    def test_api_psi_espectro(self):
        """'psi_espectro' debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.r["psi_espectro"], 0.888)

    def test_api_psi_higgs(self):
        """'psi_higgs' debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.r["psi_higgs"], 0.888)

    def test_api_psi_nodos_range(self):
        """'psi_nodos' debe estar en [0, 1]."""
        self.assertGreaterEqual(self.r["psi_nodos"], 0.0)
        self.assertLessEqual(self.r["psi_nodos"], 1.0)

    def test_api_psi_espectro_range(self):
        """'psi_espectro' debe estar en [0, 1]."""
        self.assertGreaterEqual(self.r["psi_espectro"], 0.0)
        self.assertLessEqual(self.r["psi_espectro"], 1.0)

    def test_api_psi_higgs_range(self):
        """'psi_higgs' debe estar en [0, 1]."""
        self.assertGreaterEqual(self.r["psi_higgs"], 0.0)
        self.assertLessEqual(self.r["psi_higgs"], 1.0)

    def test_api_multiple_calls_consistent(self):
        """Dos llamadas a red_ramsey_qcal_activar() deben retornar los mismos valores."""
        r2 = red_ramsey_qcal_activar()
        self.assertAlmostEqual(self.r["psi_global"], r2["psi_global"], places=12)
        self.assertEqual(self.r["sello"], r2["sello"])
        self.assertEqual(self.r["todos_los_cierres"], r2["todos_los_cierres"])

    def test_api_sello_rrq(self):
        """'sello' debe contener 'RRQ'."""
        self.assertIn("RRQ", self.r["sello"])

    def test_api_ram_correct(self):
        """'ram' debe contener 'RED-RAMSEY'."""
        self.assertIn("RED-RAMSEY", self.r["ram"])

    def test_api_resultado_dataclass(self):
        """ResultadoRedRamseyQCAL debe poder construirse desde el resultado."""
        rd = ResultadoRedRamseyQCAL(
            sello=self.r["sello"],
            psi_global=self.r["psi_global"],
            estado=self.r["estado"],
            r_symb_kpps=self.r["r_symb_kpps"],
            m_estrella=self.r["m_estrella"],
            todos_los_cierres=self.r["todos_los_cierres"],
            ram=self.r["ram"],
            version=self.r["version"],
            n_nodos=self.r["n_nodos"],
            primos=self.r["primos"],
            sello_activo=self.r["sello_activo"],
            psi_nodos=self.r["psi_nodos"],
            psi_espectro=self.r["psi_espectro"],
            psi_higgs=self.r["psi_higgs"],
        )
        self.assertTrue(rd.sello_activo)
        self.assertGreaterEqual(rd.psi_global, 0.888)


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
