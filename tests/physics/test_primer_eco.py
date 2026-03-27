"""
Tests for physics.primer_eco — 29 Décadas Cósmicas / Sistema Primer Eco ∴PE∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesPrimerEco  – constantes físicas y cósmicas
  - EspectroEco          – 12 armónicos áureos f_n = F₀·ϕⁿ
  - NivelesEnergia       – cuantización de Planck E_n = ℏω_P·(n+½)
  - OndaEco              – paquete de onda amortiguado Ψ_onda = exp(−π/N_d)
  - MatrizCoherencia     – C_ij = cos(|i−j|·φ₀); Ψ_matricial = λ_max/N
  - PropagadorCuantico   – traza de propagador de fase Ψ_propagacion
  - CoherenciaGlobal     – promedio ponderado → Ψ_global ≥ 0.888
  - SistemaPrimerEco     – orquestador con activar()
  - ResultadoPrimerEco   – dataclass de resultados
  - primer_eco_activar() – API pública

Invariantes clave verificados:
  - N_d = 29 décadas cósmicas
  - Pasos áureos ≈ 143
  - 12 frecuencias armónicas comenzando en 141.7001 Hz
  - Ψ_onda ≈ 0.897  (exp(−π/29))
  - Ψ_planck = 1.000
  - Ψ_espectral = 0.888 (umbral áureo)
  - Ψ_matricial ≥ 0.888 (λ_max/N de la matriz coseno)
  - Ψ_propagacion ≥ 0.888 (traza de propagador de fase)
  - Ψ_global ≥ 0.888 → sello ∴PE∞³ ACTIVO
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.primer_eco import (
    # Constantes de módulo
    _F0,
    _F_PLANCK,
    _PHI,
    _HBAR,
    _OMEGA_PLANCK,
    _N_ARMONICOS,
    _N_DECADAS,
    _PASOS_AUREOS,
    _PSI_UMBRAL,
    _GAMMA_COSMICO,
    _PHI_FASE,
    _FREQS,
    # Clases
    ConstantesPrimerEco,
    EspectroEco,
    NivelesEnergia,
    OndaEco,
    MatrizCoherencia,
    PropagadorCuantico,
    CoherenciaGlobal,
    SistemaPrimerEco,
    ResultadoPrimerEco,
    # API pública
    primer_eco_activar,
    # Utilidades internas
    _lambda_max_potencia,
    _eigenvalores_jacobi,
    _mv,
    _dot,
    _norm,
)


# ============================================================================
# TestModuleConstants – 14 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_f_planck_order(self):
        """_F_PLANCK debe estar en el orden 10^32."""
        self.assertGreater(_F_PLANCK, 1e31)
        self.assertLess(_F_PLANCK, 1e33)

    def test_phi_value(self):
        """_PHI debe ser la proporción áurea ≈ 1.618034."""
        self.assertAlmostEqual(_PHI, (1 + math.sqrt(5)) / 2, places=10)

    def test_phi_identity(self):
        """ϕ² = ϕ + 1 (identidad de la proporción áurea)."""
        self.assertAlmostEqual(_PHI ** 2, _PHI + 1.0, places=10)

    def test_hbar_value(self):
        """_HBAR debe ser la constante de Planck reducida CODATA 2018."""
        self.assertAlmostEqual(_HBAR, 1.054571817e-34, places=15)

    def test_omega_planck_positive(self):
        """_OMEGA_PLANCK debe ser positiva y grande."""
        self.assertGreater(_OMEGA_PLANCK, 1e42)

    def test_n_armonicos(self):
        """_N_ARMONICOS debe ser 12."""
        self.assertEqual(_N_ARMONICOS, 12)

    def test_n_decadas(self):
        """_N_DECADAS debe ser 29 = ⌊log₁₀(F_PLANCK/F0)⌋."""
        self.assertEqual(_N_DECADAS, 29)

    def test_n_decadas_consistency(self):
        """⌊log₁₀(F_PLANCK/F0)⌋ debe coincidir con _N_DECADAS."""
        computed = int(math.log10(_F_PLANCK / _F0))
        self.assertEqual(computed, _N_DECADAS)

    def test_pasos_aureos_approx(self):
        """_PASOS_AUREOS debe ser ≈ 143 pasos de proporción áurea."""
        self.assertGreaterEqual(_PASOS_AUREOS, 140)
        self.assertLessEqual(_PASOS_AUREOS, 150)

    def test_psi_umbral(self):
        """_PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    def test_gamma_cosmico(self):
        """_GAMMA_COSMICO debe ser π/29."""
        self.assertAlmostEqual(_GAMMA_COSMICO, math.pi / _N_DECADAS, places=12)

    def test_phi_fase(self):
        """_PHI_FASE debe ser π/(3·N) = π/36."""
        self.assertAlmostEqual(_PHI_FASE, math.pi / (3 * _N_ARMONICOS), places=12)

    def test_freqs_length(self):
        """_FREQS debe tener exactamente 12 elementos."""
        self.assertEqual(len(_FREQS), _N_ARMONICOS)


# ============================================================================
# TestConstantesPrimerEco – 8 tests
# ============================================================================

class TestConstantesPrimerEco(unittest.TestCase):
    """Tests para ConstantesPrimerEco."""

    def setUp(self):
        self.c = ConstantesPrimerEco()

    def test_f0_default(self):
        """f0 por defecto debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_phi_default(self):
        """phi debe ser la proporción áurea."""
        self.assertAlmostEqual(self.c.phi, (1 + math.sqrt(5)) / 2, places=10)

    def test_n_decadas_default(self):
        """n_decadas por defecto debe ser 29."""
        self.assertEqual(self.c.n_decadas, 29)

    def test_psi_umbral_default(self):
        """psi_umbral por defecto debe ser 0.888."""
        self.assertAlmostEqual(self.c.psi_umbral, 0.888, places=3)

    def test_ratio_cosmico(self):
        """ratio_cosmico() debe ser ≈ 30.0 (entre 29.9 y 30.1)."""
        r = self.c.ratio_cosmico()
        self.assertGreater(r, 29.9)
        self.assertLess(r, 30.1)

    def test_ratio_cosmico_formula(self):
        """ratio_cosmico() = log10(f_planck/f0)."""
        expected = math.log10(self.c.f_planck / self.c.f0)
        self.assertAlmostEqual(self.c.ratio_cosmico(), expected, places=10)

    def test_gamma_cosmico(self):
        """gamma_cosmico debe ser π/N_d."""
        self.assertAlmostEqual(
            self.c.gamma_cosmico,
            math.pi / self.c.n_decadas,
            places=12,
        )

    def test_repr_contains_f0(self):
        """__repr__ debe mencionar f0."""
        self.assertIn("141.7001", repr(self.c))


# ============================================================================
# TestEspectroEco – 10 tests
# ============================================================================

class TestEspectroEco(unittest.TestCase):
    """Tests para EspectroEco."""

    def setUp(self):
        self.e = EspectroEco()

    def test_frecuencias_length(self):
        """frecuencias() debe retornar 12 valores."""
        self.assertEqual(len(self.e.frecuencias()), 12)

    def test_frecuencia_cero(self):
        """f_0 = F₀ = 141.7001 Hz."""
        self.assertAlmostEqual(self.e.frecuencias()[0], 141.7001, places=4)

    def test_frecuencia_uno(self):
        """f_1 = F₀·ϕ ≈ 229.3 Hz."""
        f1 = self.e.frecuencias()[1]
        self.assertGreater(f1, 229.0)
        self.assertLess(f1, 230.0)

    def test_frecuencias_ratio_phi(self):
        """Cada armónico debe ser ϕ veces el anterior."""
        freqs = self.e.frecuencias()
        phi = _PHI
        for n in range(len(freqs) - 1):
            self.assertAlmostEqual(freqs[n + 1] / freqs[n], phi, places=10)

    def test_frecuencia_maxima(self):
        """frecuencia_maxima() = f_11 ≈ 28 199 Hz."""
        fmax = self.e.frecuencia_maxima()
        self.assertGreater(fmax, 28000.0)
        self.assertLess(fmax, 29000.0)

    def test_frecuencia_maxima_equals_last(self):
        """frecuencia_maxima() debe igualar la última frecuencia de la lista."""
        freqs = self.e.frecuencias()
        self.assertAlmostEqual(self.e.frecuencia_maxima(), freqs[-1], places=6)

    def test_anchura_espectral_positive(self):
        """anchura_espectral() debe ser positiva."""
        self.assertGreater(self.e.anchura_espectral(), 0.0)

    def test_anchura_espectral_formula(self):
        """anchura_espectral() = f_max − f_0."""
        expected = self.e.frecuencia_maxima() - self.e.f0
        self.assertAlmostEqual(self.e.anchura_espectral(), expected, places=6)

    def test_ratio_cosmico(self):
        """ratio_cosmico() debe estar en [29.9, 30.1]."""
        r = self.e.ratio_cosmico()
        self.assertGreater(r, 29.9)
        self.assertLess(r, 30.1)

    def test_repr(self):
        """__repr__ debe contener 'EspectroEco'."""
        self.assertIn("EspectroEco", repr(self.e))


# ============================================================================
# TestNivelesEnergia – 10 tests
# ============================================================================

class TestNivelesEnergia(unittest.TestCase):
    """Tests para NivelesEnergia."""

    def setUp(self):
        self.ne = NivelesEnergia()

    def test_energia_nivel_cero(self):
        """E_0 = ½ ℏ ω_P > 0."""
        e0 = self.ne.energia_nivel(0)
        self.assertGreater(e0, 0.0)

    def test_energia_nivel_cero_formula(self):
        """E_0 = ½ · ℏ · ω_P exactamente."""
        expected = 0.5 * self.ne.hbar * self.ne.omega_planck
        self.assertAlmostEqual(self.ne.energia_nivel(0), expected, places=15)

    def test_energia_punto_cero(self):
        """energia_punto_cero() == energia_nivel(0)."""
        self.assertAlmostEqual(
            self.ne.energia_punto_cero(),
            self.ne.energia_nivel(0),
            places=15,
        )

    def test_energia_nivel_uno(self):
        """E_1 = 3/2 · ℏ · ω_P = 3·E_0."""
        e0 = self.ne.energia_nivel(0)
        e1 = self.ne.energia_nivel(1)
        self.assertAlmostEqual(e1 / e0, 3.0, places=10)

    def test_energia_nivel_n_formula(self):
        """E_n = ℏ · ω_P · (n + ½) para n=5."""
        n = 5
        expected = self.ne.hbar * self.ne.omega_planck * (n + 0.5)
        self.assertAlmostEqual(self.ne.energia_nivel(n), expected, places=15)

    def test_energia_nivel_negativo_raises(self):
        """energia_nivel(n<0) debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.ne.energia_nivel(-1)

    def test_niveles_length(self):
        """niveles() debe retornar n_niveles valores."""
        self.assertEqual(len(self.ne.niveles()), self.ne.n_niveles)

    def test_niveles_ordenados(self):
        """Los niveles deben estar en orden estrictamente creciente."""
        niveles = self.ne.niveles()
        for k in range(len(niveles) - 1):
            self.assertLess(niveles[k], niveles[k + 1])

    def test_psi_planck_es_uno(self):
        """psi_planck() debe retornar exactamente 1.000."""
        self.assertEqual(self.ne.psi_planck(), 1.0)

    def test_repr(self):
        """__repr__ debe contener 'NivelesEnergia'."""
        self.assertIn("NivelesEnergia", repr(self.ne))


# ============================================================================
# TestOndaEco – 8 tests
# ============================================================================

class TestOndaEco(unittest.TestCase):
    """Tests para OndaEco."""

    def setUp(self):
        self.oe = OndaEco()

    def test_psi_onda_formula(self):
        """Ψ_onda = exp(−π/N_d) para N_d = 29."""
        expected = math.exp(-math.pi / _N_DECADAS)
        self.assertAlmostEqual(self.oe.psi_onda(), expected, places=10)

    def test_psi_onda_value(self):
        """Ψ_onda ≈ 0.897 (entre 0.895 y 0.900)."""
        psi = self.oe.psi_onda()
        self.assertGreater(psi, 0.895)
        self.assertLess(psi, 0.900)

    def test_amplitud_equals_psi_onda(self):
        """amplitud() debe igualar psi_onda()."""
        self.assertAlmostEqual(self.oe.amplitud(), self.oe.psi_onda(), places=12)

    def test_amplitud_in_zero_one(self):
        """La amplitud debe estar en (0, 1]."""
        a = self.oe.amplitud()
        self.assertGreater(a, 0.0)
        self.assertLessEqual(a, 1.0)

    def test_fase_acumulada(self):
        """fase_acumulada() = γ · N_d = π."""
        fa = self.oe.fase_acumulada()
        self.assertAlmostEqual(fa, math.pi, places=10)

    def test_fase_acumulada_formula(self):
        """fase_acumulada() = gamma_cosmico · n_decadas."""
        expected = self.oe.gamma_cosmico * self.oe.n_decadas
        self.assertAlmostEqual(self.oe.fase_acumulada(), expected, places=12)

    def test_custom_n_decadas(self):
        """Con N_d = 10: Ψ_onda = exp(−π/10)."""
        oe10 = OndaEco(n_decadas=10, gamma_cosmico=math.pi / 10)
        expected = math.exp(-math.pi / 10)
        self.assertAlmostEqual(oe10.psi_onda(), expected, places=10)

    def test_repr(self):
        """__repr__ debe contener 'OndaEco'."""
        self.assertIn("OndaEco", repr(self.oe))


# ============================================================================
# TestMatrizCoherencia – 12 tests
# ============================================================================

class TestMatrizCoherencia(unittest.TestCase):
    """Tests para MatrizCoherencia."""

    def setUp(self):
        self.mc = MatrizCoherencia()

    def test_matriz_size(self):
        """La matriz debe ser N×N = 12×12."""
        m = self.mc.matriz()
        self.assertEqual(len(m), 12)
        for row in m:
            self.assertEqual(len(row), 12)

    def test_diagonal_unos(self):
        """C_ii = 1.0 para todo i."""
        m = self.mc.matriz()
        for i in range(12):
            self.assertAlmostEqual(m[i][i], 1.0, places=10)

    def test_simetria(self):
        """C_ij = C_ji para todo i, j."""
        m = self.mc.matriz()
        for i in range(12):
            for j in range(12):
                self.assertAlmostEqual(m[i][j], m[j][i], places=12)

    def test_elemento_diagonal(self):
        """elemento(i, i) = 1.0."""
        for i in range(12):
            self.assertAlmostEqual(self.mc.elemento(i, i), 1.0, places=10)

    def test_elemento_adyacente(self):
        """C_01 = cos(φ₀) > 0.99."""
        c01 = self.mc.elemento(0, 1)
        self.assertGreater(c01, 0.99)
        self.assertLessEqual(c01, 1.0)

    def test_elemento_indices_invalidos(self):
        """elemento() con índices fuera de rango debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.mc.elemento(0, 12)
        with self.assertRaises(ValueError):
            self.mc.elemento(-1, 0)

    def test_lambda_max_positive(self):
        """λ_max(C) debe ser positivo."""
        self.assertGreater(self.mc.lambda_max(), 0.0)

    def test_lambda_max_at_most_n(self):
        """λ_max(C) ≤ N (acotación de Perron-Frobenius)."""
        self.assertLessEqual(self.mc.lambda_max(), 12.0 + 1e-6)

    def test_psi_matricial_formula(self):
        """Ψ_matricial = λ_max / N."""
        expected = self.mc.lambda_max() / 12
        self.assertAlmostEqual(self.mc.psi_matricial(), expected, places=8)

    def test_psi_matricial_above_threshold(self):
        """Ψ_matricial ≥ 0.888."""
        self.assertGreaterEqual(self.mc.psi_matricial(), _PSI_UMBRAL)

    def test_es_semidefinida_positiva(self):
        """La matriz C debe ser semidefinida positiva."""
        self.assertTrue(self.mc.es_semidefinida_positiva())

    def test_repr(self):
        """__repr__ debe contener 'MatrizCoherencia'."""
        self.assertIn("MatrizCoherencia", repr(self.mc))


# ============================================================================
# TestPropagadorCuantico – 8 tests
# ============================================================================

class TestPropagadorCuantico(unittest.TestCase):
    """Tests para PropagadorCuantico."""

    def setUp(self):
        self.pq = PropagadorCuantico()

    def test_traza_normalizada_in_zero_one(self):
        """traza_normalizada() ∈ [0, 1]."""
        t = self.pq.traza_normalizada()
        self.assertGreaterEqual(t, 0.0)
        self.assertLessEqual(t, 1.0 + 1e-10)

    def test_psi_propagacion_equals_traza(self):
        """psi_propagacion() debe igualar traza_normalizada()."""
        self.assertAlmostEqual(
            self.pq.psi_propagacion(),
            self.pq.traza_normalizada(),
            places=12,
        )

    def test_psi_propagacion_above_threshold(self):
        """Ψ_propagacion ≥ 0.888."""
        self.assertGreaterEqual(self.pq.psi_propagacion(), _PSI_UMBRAL)

    def test_traza_theta_zero(self):
        """En θ=0 (límite), traza_normalizada() → 1.0."""
        pq_zero = PropagadorCuantico(theta=1e-14)
        self.assertAlmostEqual(pq_zero.traza_normalizada(), 1.0, places=4)

    def test_traza_formula(self):
        """traza_normalizada() = |sin(N·θ/2)| / (N·sin(θ/2))."""
        N = self.pq.n_armonicos
        theta = self.pq.theta
        expected = abs(math.sin(N * theta / 2)) / (N * math.sin(theta / 2))
        self.assertAlmostEqual(self.pq.traza_normalizada(), expected, places=12)

    def test_custom_theta(self):
        """Con θ = π/2 y N=12: valor bien definido."""
        pq = PropagadorCuantico(theta=math.pi / 2)
        t = pq.traza_normalizada()
        self.assertGreaterEqual(t, 0.0)
        self.assertLessEqual(t, 1.0 + 1e-10)

    def test_n_armonicos_default(self):
        """n_armonicos por defecto debe ser 12."""
        self.assertEqual(self.pq.n_armonicos, 12)

    def test_repr(self):
        """__repr__ debe contener 'PropagadorCuantico'."""
        self.assertIn("PropagadorCuantico", repr(self.pq))


# ============================================================================
# TestCoherenciaGlobal – 12 tests
# ============================================================================

class TestCoherenciaGlobal(unittest.TestCase):
    """Tests para CoherenciaGlobal."""

    def _make_coherencia(
        self,
        psi_onda=0.897,
        psi_planck=1.0,
        psi_espectral=0.888,
        psi_matricial=0.914,
        psi_propagacion=0.930,
    ) -> CoherenciaGlobal:
        return CoherenciaGlobal(
            psi_onda=psi_onda,
            psi_planck=psi_planck,
            psi_espectral=psi_espectral,
            psi_matricial=psi_matricial,
            psi_propagacion=psi_propagacion,
        )

    def test_psi_global_formula(self):
        """Ψ_global = Σ(wᵢ·Ψᵢ)/Σwᵢ con pesos [1.0,1.5,2.0,2.0,1.5]."""
        coh = self._make_coherencia()
        ws = [1.0, 1.5, 2.0, 2.0, 1.5]
        psis = [0.897, 1.0, 0.888, 0.914, 0.930]
        expected = sum(w * p for w, p in zip(ws, psis)) / sum(ws)
        self.assertAlmostEqual(coh.psi_global(), expected, places=8)

    def test_psi_global_in_zero_one(self):
        """Ψ_global debe estar en [0, 1] para entradas válidas."""
        coh = self._make_coherencia()
        g = coh.psi_global()
        self.assertGreaterEqual(g, 0.0)
        self.assertLessEqual(g, 1.0)

    def test_sello_activo_true(self):
        """Sello activo cuando Ψ_global ≥ 0.888."""
        coh = self._make_coherencia()
        self.assertGreaterEqual(coh.psi_global(), 0.888)
        self.assertTrue(coh.sello_activo())

    def test_sello_inactivo_false(self):
        """Sello inactivo cuando Ψ_global < 0.888."""
        coh = CoherenciaGlobal(
            psi_onda=0.5,
            psi_planck=0.5,
            psi_espectral=0.5,
            psi_matricial=0.5,
            psi_propagacion=0.5,
        )
        self.assertFalse(coh.sello_activo())

    def test_sello_exactamente_umbral(self):
        """Sello activo cuando Ψ_global = 0.888 exactamente."""
        coh = CoherenciaGlobal(
            psi_onda=0.888,
            psi_planck=0.888,
            psi_espectral=0.888,
            psi_matricial=0.888,
            psi_propagacion=0.888,
        )
        self.assertAlmostEqual(coh.psi_global(), 0.888, places=10)
        self.assertTrue(coh.sello_activo())

    def test_resumen_keys(self):
        """resumen() debe contener las 6 claves esperadas."""
        coh = self._make_coherencia()
        keys = coh.resumen().keys()
        for k in [
            "psi_onda", "psi_planck", "psi_espectral",
            "psi_matricial", "psi_propagacion", "psi_global",
        ]:
            self.assertIn(k, keys)

    def test_resumen_psi_global(self):
        """resumen()['psi_global'] debe coincidir con psi_global()."""
        coh = self._make_coherencia()
        self.assertAlmostEqual(
            coh.resumen()["psi_global"], coh.psi_global(), places=12
        )

    def test_psi_planck_uno_aumenta_global(self):
        """Con Ψ_planck = 1.0, el promedio ponderado es mayor que sin él."""
        coh_alta = self._make_coherencia(psi_planck=1.0)
        coh_baja = self._make_coherencia(psi_planck=0.5)
        self.assertGreater(coh_alta.psi_global(), coh_baja.psi_global())

    def test_pesos_correctos(self):
        """Los pesos [1.0,1.5,2.0,2.0,1.5] suman 8.0."""
        coh = CoherenciaGlobal(
            psi_onda=1.0,
            psi_planck=1.0,
            psi_espectral=1.0,
            psi_matricial=1.0,
            psi_propagacion=1.0,
        )
        self.assertAlmostEqual(coh.psi_global(), 1.0, places=10)

    def test_psi_umbral_default(self):
        """psi_umbral por defecto = 0.888."""
        coh = self._make_coherencia()
        self.assertAlmostEqual(coh.psi_umbral, 0.888, places=3)

    def test_repr_sello_activo(self):
        """__repr__ debe indicar ACTIVO cuando el sello está activo."""
        coh = self._make_coherencia()
        self.assertIn("ACTIVO", repr(coh))

    def test_repr_sello_inactivo(self):
        """__repr__ debe indicar INACTIVO cuando el sello no está activo."""
        coh = CoherenciaGlobal(
            psi_onda=0.1,
            psi_planck=0.1,
            psi_espectral=0.1,
            psi_matricial=0.1,
            psi_propagacion=0.1,
        )
        self.assertIn("INACTIVO", repr(coh))


# ============================================================================
# TestSistemaPrimerEco – 12 tests
# ============================================================================

class TestSistemaPrimerEco(unittest.TestCase):
    """Tests para SistemaPrimerEco."""

    def setUp(self):
        self.sistema = SistemaPrimerEco()

    def test_f0_default(self):
        """f0 por defecto debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.sistema.f0, 141.7001, places=4)

    def test_f_planck_default(self):
        """f_planck por defecto debe ser 1.416784e32 Hz."""
        self.assertAlmostEqual(self.sistema.f_planck, 1.416784e32, places=20)

    def test_f0_negativo_raises(self):
        """f0 negativo o cero debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            SistemaPrimerEco(f0=0.0)
        with self.assertRaises(ValueError):
            SistemaPrimerEco(f0=-100.0)

    def test_f_planck_menor_f0_raises(self):
        """f_planck ≤ f0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            SistemaPrimerEco(f0=200.0, f_planck=100.0)

    def test_activar_retorna_resultado(self):
        """activar() debe retornar una instancia de ResultadoPrimerEco."""
        r = self.sistema.activar()
        self.assertIsInstance(r, ResultadoPrimerEco)

    def test_sello_activo(self):
        """El sello debe estar activo con parámetros por defecto."""
        r = self.sistema.activar()
        self.assertTrue(r.sello_activo)

    def test_psi_global_above_threshold(self):
        """Ψ_global debe ser ≥ 0.888."""
        r = self.sistema.activar()
        self.assertGreaterEqual(r.psi_global, _PSI_UMBRAL)

    def test_n_decadas_resultado(self):
        """n_decadas en el resultado debe ser 29."""
        r = self.sistema.activar()
        self.assertEqual(r.n_decadas, 29)

    def test_frecuencias_count(self):
        """Deben haber exactamente 12 frecuencias armónicas."""
        r = self.sistema.activar()
        self.assertEqual(len(r.frecuencias_armonicas), 12)

    def test_frecuencia_primera(self):
        """La primera frecuencia debe ser F₀ = 141.7001 Hz."""
        r = self.sistema.activar()
        self.assertAlmostEqual(r.frecuencias_armonicas[0], 141.7001, places=4)

    def test_mensaje_sello_activo(self):
        """El mensaje debe indicar ACTIVO ∴PE∞³."""
        r = self.sistema.activar()
        self.assertIn("∴PE∞³", r.mensaje)
        self.assertIn("ACTIVO", r.mensaje)

    def test_repr(self):
        """__repr__ debe contener 'SistemaPrimerEco'."""
        self.assertIn("SistemaPrimerEco", repr(self.sistema))


# ============================================================================
# TestResultadoPrimerEco – 8 tests
# ============================================================================

class TestResultadoPrimerEco(unittest.TestCase):
    """Tests para ResultadoPrimerEco (dataclass de resultados)."""

    def _make_resultado(self) -> ResultadoPrimerEco:
        return ResultadoPrimerEco(
            f0=141.7001,
            f_planck=1.416784e32,
            n_decadas=29,
            pasos_aureos=143,
            frecuencias_armonicas=list(_FREQS),
            psi_onda=0.897,
            psi_planck=1.0,
            psi_espectral=0.888,
            psi_matricial=0.914,
            psi_propagacion=0.931,
            psi_global=0.924,
            sello_activo=True,
            mensaje="TEST OK ∴PE∞³",
        )

    def test_campos_existentes(self):
        """ResultadoPrimerEco debe tener todos los campos esperados."""
        r = self._make_resultado()
        campos = [
            "f0", "f_planck", "n_decadas", "pasos_aureos",
            "frecuencias_armonicas",
            "psi_onda", "psi_planck", "psi_espectral",
            "psi_matricial", "psi_propagacion",
            "psi_global", "sello_activo", "mensaje",
        ]
        for campo in campos:
            self.assertTrue(hasattr(r, campo), f"Campo faltante: {campo}")

    def test_f0_almacenado(self):
        """f0 debe almacenarse exactamente."""
        r = self._make_resultado()
        self.assertAlmostEqual(r.f0, 141.7001, places=4)

    def test_n_decadas_almacenado(self):
        """n_decadas debe almacenarse exactamente."""
        r = self._make_resultado()
        self.assertEqual(r.n_decadas, 29)

    def test_sello_activo_bool(self):
        """sello_activo debe ser True en el resultado de prueba."""
        r = self._make_resultado()
        self.assertTrue(r.sello_activo)

    def test_psi_global_almacenado(self):
        """psi_global debe almacenarse con el valor dado."""
        r = self._make_resultado()
        self.assertAlmostEqual(r.psi_global, 0.924, places=3)

    def test_frecuencias_count(self):
        """frecuencias_armonicas debe tener 12 elementos."""
        r = self._make_resultado()
        self.assertEqual(len(r.frecuencias_armonicas), 12)

    def test_mensaje_almacenado(self):
        """mensaje debe almacenarse exactamente."""
        r = self._make_resultado()
        self.assertIn("TEST OK", r.mensaje)

    def test_pasos_aureos_almacenado(self):
        """pasos_aureos debe almacenarse exactamente."""
        r = self._make_resultado()
        self.assertEqual(r.pasos_aureos, 143)


# ============================================================================
# TestPrimerEcoActivar – 12 tests (API pública)
# ============================================================================

class TestPrimerEcoActivar(unittest.TestCase):
    """Tests para la función pública primer_eco_activar()."""

    def setUp(self):
        self.r = primer_eco_activar()

    def test_retorna_dict(self):
        """primer_eco_activar() debe retornar un dict."""
        self.assertIsInstance(self.r, dict)

    def test_claves_esperadas(self):
        """El dict debe contener todas las claves esperadas."""
        claves = [
            "f0_hz", "f_planck_hz", "n_decadas", "pasos_aureos",
            "ratio_cosmico", "frecuencias_armonicas",
            "psi_onda", "psi_planck", "psi_espectral",
            "psi_matricial", "psi_propagacion",
            "psi_global", "sello_activo", "mensaje",
        ]
        for c in claves:
            self.assertIn(c, self.r, f"Clave faltante: {c}")

    def test_f0_hz(self):
        """f0_hz debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.r["f0_hz"], 141.7001, places=4)

    def test_n_decadas(self):
        """n_decadas debe ser 29."""
        self.assertEqual(self.r["n_decadas"], 29)

    def test_sello_activo(self):
        """sello_activo debe ser True."""
        self.assertTrue(self.r["sello_activo"])

    def test_psi_global_above_threshold(self):
        """psi_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.r["psi_global"], _PSI_UMBRAL)

    def test_psi_planck_es_uno(self):
        """psi_planck debe ser 1.0."""
        self.assertAlmostEqual(self.r["psi_planck"], 1.0, places=10)

    def test_psi_espectral_es_umbral(self):
        """psi_espectral debe ser 0.888."""
        self.assertAlmostEqual(self.r["psi_espectral"], 0.888, places=3)

    def test_psi_onda_valor(self):
        """psi_onda ≈ 0.897 (exp(−π/29))."""
        expected = math.exp(-math.pi / 29)
        self.assertAlmostEqual(self.r["psi_onda"], expected, places=6)

    def test_frecuencias_count(self):
        """Deben haber 12 frecuencias armónicas."""
        self.assertEqual(len(self.r["frecuencias_armonicas"]), 12)

    def test_ratio_cosmico(self):
        """ratio_cosmico debe estar entre 29.9 y 30.1."""
        r = self.r["ratio_cosmico"]
        self.assertGreater(r, 29.9)
        self.assertLess(r, 30.1)

    def test_parametros_personalizados(self):
        """primer_eco_activar() con f0 distinto debe funcionar."""
        r2 = primer_eco_activar(f0=200.0, f_planck=2e32)
        self.assertIsInstance(r2["sello_activo"], bool)
        self.assertAlmostEqual(r2["f0_hz"], 200.0, places=4)


# ============================================================================
# TestUtilidades – 8 tests
# ============================================================================

class TestUtilidades(unittest.TestCase):
    """Tests para las utilidades internas de álgebra lineal."""

    def test_mv_identidad(self):
        """Multiplicar por la identidad 2×2 debe retornar el mismo vector."""
        I = [[1.0, 0.0], [0.0, 1.0]]
        v = [3.0, 7.0]
        result = _mv(I, v)
        self.assertAlmostEqual(result[0], 3.0, places=10)
        self.assertAlmostEqual(result[1], 7.0, places=10)

    def test_mv_escalado(self):
        """2·I · v debe retornar 2·v."""
        I2 = [[2.0, 0.0], [0.0, 2.0]]
        v = [1.5, 2.5]
        result = _mv(I2, v)
        self.assertAlmostEqual(result[0], 3.0, places=10)
        self.assertAlmostEqual(result[1], 5.0, places=10)

    def test_dot_ortogonales(self):
        """Producto punto de vectores ortogonales debe ser 0."""
        u = [1.0, 0.0, 0.0]
        v = [0.0, 1.0, 0.0]
        self.assertAlmostEqual(_dot(u, v), 0.0, places=12)

    def test_dot_paralelos(self):
        """Producto punto de [1,1,1] · [1,1,1] = 3."""
        v = [1.0, 1.0, 1.0]
        self.assertAlmostEqual(_dot(v, v), 3.0, places=12)

    def test_norm_unitario(self):
        """Norma de [1, 0, 0] debe ser 1.0."""
        self.assertAlmostEqual(_norm([1.0, 0.0, 0.0]), 1.0, places=12)

    def test_norm_formula(self):
        """Norma de [3, 4] debe ser 5.0."""
        self.assertAlmostEqual(_norm([3.0, 4.0]), 5.0, places=10)

    def test_lambda_max_matriz_2x2(self):
        """λ_max de [[2,1],[1,2]] debe ser 3.0."""
        mat = [[2.0, 1.0], [1.0, 2.0]]
        lam = _lambda_max_potencia(mat, 2)
        self.assertAlmostEqual(lam, 3.0, places=5)

    def test_jacobi_identidad(self):
        """Autovalores de la identidad 3×3 deben ser todos 1.0."""
        I = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        ev = sorted(_eigenvalores_jacobi(I))
        for e in ev:
            self.assertAlmostEqual(e, 1.0, places=6)


# ============================================================================
# TestIntegracion – 6 tests (integración del sistema completo)
# ============================================================================

class TestIntegracion(unittest.TestCase):
    """Tests de integración del sistema completo."""

    def test_flujo_completo(self):
        """El flujo completo (sistema → activar → resultado) debe funcionar."""
        s = SistemaPrimerEco()
        r = s.activar()
        self.assertIsInstance(r, ResultadoPrimerEco)
        self.assertTrue(r.sello_activo)

    def test_todas_coherencias_positivas(self):
        """Todas las coherencias en el resultado deben ser positivas."""
        r = primer_eco_activar()
        for key in [
            "psi_onda", "psi_planck", "psi_espectral",
            "psi_matricial", "psi_propagacion", "psi_global",
        ]:
            self.assertGreater(r[key], 0.0, f"{key} no es positivo")

    def test_frecuencias_crecientes(self):
        """Los armónicos deben estar en orden estrictamente creciente."""
        r = primer_eco_activar()
        freqs = r["frecuencias_armonicas"]
        for k in range(len(freqs) - 1):
            self.assertLess(freqs[k], freqs[k + 1])

    def test_frecuencias_ratio_phi(self):
        """Cada armónico debe ser ϕ veces el anterior."""
        r = primer_eco_activar()
        freqs = r["frecuencias_armonicas"]
        for k in range(len(freqs) - 1):
            self.assertAlmostEqual(freqs[k + 1] / freqs[k], _PHI, places=8)

    def test_sello_mensaje_coherente(self):
        """Si sello_activo=True, el mensaje debe indicar '∴PE∞³'."""
        r = primer_eco_activar()
        if r["sello_activo"]:
            self.assertIn("∴PE∞³", r["mensaje"])

    def test_psi_global_consistente(self):
        """psi_global del dict debe coincidir con el de ResultadoPrimerEco."""
        s = SistemaPrimerEco()
        resultado = s.activar()
        r_dict = primer_eco_activar()
        self.assertAlmostEqual(
            resultado.psi_global, r_dict["psi_global"], places=10
        )


if __name__ == "__main__":
    unittest.main()
