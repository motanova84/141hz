"""
Tests for physics.sintesis_tratado — Síntesis del Tratado ∴ST∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesSintesis          – constantes físicas del tratado
  - ParticulaCoherencia         – campo PC (95.2% del tejido)
  - AcoplamientoHiggsPC         – Lagrangiano de interacción
  - MasaOscilante               – modulación temporal de masa
  - OperadorMaestroAdelico      – operador con espectro de Riemann
  - EcuacionSchrodingerRiemann  – ecuación unificada
  - RedC7                       – red de 7 nodos primos
  - SistemaSintesisTratado      – orquestador con activar()
  - sintesis_tratado_activar()  – API pública

Invariantes clave verificados:
  - f₀ = 141.7001 Hz
  - m_H = 125.25 GeV/c²
  - m_flash = 118.375 GeV/c² (Destello)
  - g_eff ≈ 0.053
  - PC domain = 95.2%
  - 7 primos en C₇: {2, 3, 5, 7, 11, 13, 17}
  - 10 ceros de Riemann en la línea crítica Re(s) = 1/2
  - Ψ_global ≥ 0.888 → sello ∴ST∞³ ACTIVO
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.sintesis_tratado import (
    # Constantes del módulo
    _F0,
    _OMEGA_0,
    _PHI,
    _HBAR,
    _M_HIGGS_GEV,
    _M_FLASH_GEV,
    _G_EFF,
    _PC_DOMAIN,
    _BARYONIC_DOMAIN,
    _C7_PRIMES,
    _TRANSFER_RATE_KPPS,
    _RIEMANN_ZEROS,
    _PSI_UMBRAL,
    # Clases
    ConstantesSintesis,
    ParticulaCoherencia,
    AcoplamientoHiggsPC,
    MasaOscilante,
    OperadorMaestroAdelico,
    EcuacionSchrodingerRiemann,
    RedC7,
    SistemaSintesisTratado,
    # API pública
    sintesis_tratado_activar,
)


# ============================================================================
# TestModuleConstants – 18 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes del módulo."""

    def test_f0_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_omega_0_value(self):
        """_OMEGA_0 debe ser 2πf₀."""
        self.assertAlmostEqual(_OMEGA_0, 2.0 * math.pi * _F0, places=6)

    def test_phi_golden_ratio(self):
        """_PHI debe ser la proporción áurea."""
        self.assertAlmostEqual(_PHI, (1 + math.sqrt(5)) / 2, places=10)

    def test_hbar_value(self):
        """_HBAR debe ser la constante de Planck reducida CODATA 2018."""
        self.assertAlmostEqual(_HBAR, 1.054571817e-34, places=15)

    def test_m_higgs_value(self):
        """_M_HIGGS_GEV debe ser 125.25 GeV."""
        self.assertAlmostEqual(_M_HIGGS_GEV, 125.25, places=2)

    def test_m_flash_value(self):
        """_M_FLASH_GEV debe ser 118.375 GeV."""
        self.assertAlmostEqual(_M_FLASH_GEV, 118.375, places=3)

    def test_g_eff_value(self):
        """_G_EFF debe ser aproximadamente 0.053."""
        self.assertAlmostEqual(_G_EFF, 0.053, places=3)

    def test_pc_domain_value(self):
        """_PC_DOMAIN debe ser 0.952 (95.2%)."""
        self.assertAlmostEqual(_PC_DOMAIN, 0.952, places=3)

    def test_baryonic_domain_value(self):
        """_BARYONIC_DOMAIN debe ser 0.048 (4.8%)."""
        self.assertAlmostEqual(_BARYONIC_DOMAIN, 0.048, places=3)

    def test_domains_sum_to_one(self):
        """PC + Bariónico debe sumar 1.0."""
        self.assertAlmostEqual(_PC_DOMAIN + _BARYONIC_DOMAIN, 1.0, places=6)

    def test_c7_primes_are_primes(self):
        """Los nodos C₇ deben ser primos."""
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True

        for p in _C7_PRIMES:
            self.assertTrue(is_prime(p), f"{p} no es primo")

    def test_c7_primes_count(self):
        """Debe haber exactamente 7 primos en C₇."""
        self.assertEqual(len(_C7_PRIMES), 7)

    def test_c7_primes_sorted(self):
        """Los primos C₇ deben estar ordenados."""
        self.assertEqual(_C7_PRIMES, tuple(sorted(_C7_PRIMES)))

    def test_transfer_rate_value(self):
        """_TRANSFER_RATE_KPPS debe ser 991.9 kpps."""
        self.assertAlmostEqual(_TRANSFER_RATE_KPPS, 991.9, places=1)

    def test_riemann_zeros_count(self):
        """Debe haber 10 ceros de Riemann."""
        self.assertEqual(len(_RIEMANN_ZEROS), 10)

    def test_riemann_zeros_positive(self):
        """Todos los ceros de Riemann deben ser positivos."""
        for gamma in _RIEMANN_ZEROS:
            self.assertGreater(gamma, 0)

    def test_riemann_zeros_increasing(self):
        """Los ceros de Riemann deben estar en orden creciente."""
        for i in range(len(_RIEMANN_ZEROS) - 1):
            self.assertLess(_RIEMANN_ZEROS[i], _RIEMANN_ZEROS[i + 1])

    def test_psi_umbral_value(self):
        """_PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)


# ============================================================================
# TestConstantesSintesis – 8 tests
# ============================================================================

class TestConstantesSintesis(unittest.TestCase):
    """Tests para ConstantesSintesis."""

    def setUp(self):
        self.c = ConstantesSintesis()

    def test_f0_default(self):
        """f0 por defecto debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_omega_0_default(self):
        """omega_0 debe ser 2πf₀."""
        self.assertAlmostEqual(self.c.omega_0, 2 * math.pi * self.c.f0, places=4)

    def test_m_higgs_default(self):
        """m_higgs_gev debe ser 125.25 GeV."""
        self.assertAlmostEqual(self.c.m_higgs_gev, 125.25, places=2)

    def test_mass_reduction(self):
        """La reducción de masa debe ser ~5.5%."""
        reduction = self.c.mass_reduction()
        self.assertGreater(reduction, 0.04)
        self.assertLess(reduction, 0.07)

    def test_dominio_total(self):
        """PC + Bariónico debe ser ~1.0."""
        total = self.c.dominio_total()
        self.assertAlmostEqual(total, 1.0, places=6)

    def test_g_eff_default(self):
        """g_eff debe ser ~0.053."""
        self.assertAlmostEqual(self.c.g_eff, 0.053, places=3)

    def test_c7_primes_default(self):
        """c7_primes debe tener 7 elementos."""
        self.assertEqual(len(self.c.c7_primes), 7)

    def test_repr(self):
        """repr debe incluir información clave."""
        r = repr(self.c)
        self.assertIn("ConstantesSintesis", r)
        self.assertIn("141.7001", r)


# ============================================================================
# TestParticulaCoherencia – 10 tests
# ============================================================================

class TestParticulaCoherencia(unittest.TestCase):
    """Tests para ParticulaCoherencia."""

    def setUp(self):
        self.pc = ParticulaCoherencia()

    def test_pc_domain_default(self):
        """pc_domain debe ser 0.952."""
        self.assertAlmostEqual(self.pc.pc_domain, 0.952, places=3)

    def test_f0_default(self):
        """f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.pc.f0, 141.7001, places=4)

    def test_amplitud_default(self):
        """amplitud debe ser 1.0."""
        self.assertAlmostEqual(self.pc.amplitud, 1.0, places=6)

    def test_densidad_at_zero(self):
        """Densidad en t=0 debe ser pc_domain (cos²(0)=1)."""
        rho = self.pc.densidad(0.0)
        self.assertAlmostEqual(rho, self.pc.pc_domain, places=6)

    def test_densidad_barra_psi_at_zero(self):
        """ψ̄ψ en t=0 debe ser 1.0."""
        psi_bar_psi = self.pc.densidad_barra_psi(0.0)
        self.assertAlmostEqual(psi_bar_psi, 1.0, places=6)

    def test_densidad_positive(self):
        """La densidad siempre debe ser ≥ 0."""
        for t in [0.0, 0.001, 0.01, 0.1]:
            rho = self.pc.densidad(t)
            self.assertGreaterEqual(rho, 0.0)

    def test_coherencia_pc_high(self):
        """La coherencia PC debe ser muy alta (≥ 0.99)."""
        psi = self.pc.coherencia_pc()
        self.assertGreaterEqual(psi, 0.99)

    def test_coherencia_pc_formula(self):
        """Ψ_PC = 1 − (1 − pc_domain)²."""
        expected = 1.0 - (1.0 - self.pc.pc_domain) ** 2
        self.assertAlmostEqual(self.pc.coherencia_pc(), expected, places=6)

    def test_repr(self):
        """repr debe incluir dominio y coherencia."""
        r = repr(self.pc)
        self.assertIn("ParticulaCoherencia", r)
        self.assertIn("95.2%", r)

    def test_densidad_oscillation(self):
        """La densidad debe oscilar con período T = 1/f₀."""
        T = 1.0 / self.pc.f0
        rho_0 = self.pc.densidad(0.0)
        rho_T = self.pc.densidad(T)
        self.assertAlmostEqual(rho_0, rho_T, places=4)


# ============================================================================
# TestAcoplamientoHiggsPC – 8 tests
# ============================================================================

class TestAcoplamientoHiggsPC(unittest.TestCase):
    """Tests para AcoplamientoHiggsPC."""

    def setUp(self):
        self.acopl = AcoplamientoHiggsPC()

    def test_g_eff_default(self):
        """g_eff debe ser 0.053."""
        self.assertAlmostEqual(self.acopl.g_eff, 0.053, places=3)

    def test_lagrangiano_interaccion_sign(self):
        """ℒ_int debe ser negativo (atractivo)."""
        L = self.acopl.lagrangiano_interaccion()
        self.assertLess(L, 0)

    def test_lagrangiano_interaccion_value(self):
        """ℒ_int = −g_eff · ψ̄ψ · H."""
        L = self.acopl.lagrangiano_interaccion(psi_bar_psi=1.0, h_field=1.0)
        expected = -self.acopl.g_eff
        self.assertAlmostEqual(L, expected, places=6)

    def test_energia_acoplamiento_positive(self):
        """E_int debe ser positiva (opuesta al Lagrangiano)."""
        E = self.acopl.energia_acoplamiento()
        self.assertGreater(E, 0)

    def test_coherencia_acoplamiento_high(self):
        """La coherencia de acoplamiento debe ser muy alta (≥ 0.99)."""
        psi = self.acopl.coherencia_acoplamiento()
        self.assertGreaterEqual(psi, 0.99)

    def test_coherencia_formula(self):
        """Ψ_coup = 1 − g²/(1+g²)."""
        g2 = self.acopl.g_eff ** 2
        expected = 1.0 - g2 / (1.0 + g2)
        self.assertAlmostEqual(self.acopl.coherencia_acoplamiento(), expected, places=6)

    def test_lagrangiano_scaling(self):
        """ℒ_int debe escalar linealmente con ψ̄ψ y H."""
        L1 = self.acopl.lagrangiano_interaccion(psi_bar_psi=2.0, h_field=1.0)
        L2 = self.acopl.lagrangiano_interaccion(psi_bar_psi=1.0, h_field=1.0)
        self.assertAlmostEqual(L1, 2 * L2, places=6)

    def test_repr(self):
        """repr debe incluir g_eff."""
        r = repr(self.acopl)
        self.assertIn("AcoplamientoHiggsPC", r)
        self.assertIn("0.053", r)


# ============================================================================
# TestMasaOscilante – 12 tests
# ============================================================================

class TestMasaOscilante(unittest.TestCase):
    """Tests para MasaOscilante."""

    def setUp(self):
        self.masa = MasaOscilante()

    def test_m_higgs_default(self):
        """m_higgs_gev debe ser 125.25 GeV."""
        self.assertAlmostEqual(self.masa.m_higgs_gev, 125.25, places=2)

    def test_masa_efectiva_at_zero(self):
        """m*(0) debe ser m_H · (1 − g_eff) = masa mínima."""
        m_0 = self.masa.masa_efectiva(0.0)
        m_min = self.masa.masa_minima()
        self.assertAlmostEqual(m_0, m_min, places=4)

    def test_masa_minima_value(self):
        """Masa mínima debe ser ~118.6 GeV."""
        m_min = self.masa.masa_minima()
        self.assertGreater(m_min, 117)
        self.assertLess(m_min, 120)

    def test_masa_maxima_value(self):
        """Masa máxima debe ser ~131.9 GeV."""
        m_max = self.masa.masa_maxima()
        self.assertGreater(m_max, 130)
        self.assertLess(m_max, 134)

    def test_amplitud_oscilacion(self):
        """Amplitud = m_H · g_eff."""
        amp = self.masa.amplitud_oscilacion()
        expected = self.masa.m_higgs_gev * self.masa.g_eff
        self.assertAlmostEqual(amp, expected, places=4)

    def test_reduccion_inercia(self):
        """Reducción de inercia = g_eff."""
        red = self.masa.reduccion_inercia()
        self.assertAlmostEqual(red, self.masa.g_eff, places=6)

    def test_es_destello_at_zero(self):
        """t=0 debe ser fase de Destello (cos(0)=1 → masa mínima)."""
        self.assertTrue(self.masa.es_destello(0.0))

    def test_not_destello_at_half_period(self):
        """t=T/2 no debe ser Destello (masa máxima)."""
        T = 1.0 / self.masa.f0
        self.assertFalse(self.masa.es_destello(T / 2))

    def test_masa_oscillation_period(self):
        """La masa debe oscilar con período T = 1/f₀."""
        T = 1.0 / self.masa.f0
        m_0 = self.masa.masa_efectiva(0.0)
        m_T = self.masa.masa_efectiva(T)
        self.assertAlmostEqual(m_0, m_T, places=4)

    def test_coherencia_masa(self):
        """Ψ_masa = 1 − g_eff ≈ 0.947."""
        psi = self.masa.coherencia_masa()
        expected = 1.0 - self.masa.g_eff
        self.assertAlmostEqual(psi, expected, places=6)

    def test_coherencia_masa_above_threshold(self):
        """Coherencia de masa debe ser ≥ 0.888."""
        psi = self.masa.coherencia_masa()
        self.assertGreaterEqual(psi, 0.888)

    def test_repr(self):
        """repr debe incluir masas."""
        r = repr(self.masa)
        self.assertIn("MasaOscilante", r)
        self.assertIn("125.25", r)


# ============================================================================
# TestOperadorMaestroAdelico – 12 tests
# ============================================================================

class TestOperadorMaestroAdelico(unittest.TestCase):
    """Tests para OperadorMaestroAdelico."""

    def setUp(self):
        self.op = OperadorMaestroAdelico()

    def test_f0_default(self):
        """f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.op.f0, 141.7001, places=4)

    def test_n_zeros_default(self):
        """n_zeros debe ser 10."""
        self.assertEqual(self.op.n_zeros, 10)

    def test_autovalor_real_part(self):
        """Parte real de autovalores debe ser 0.5."""
        for n in range(self.op.n_zeros):
            av = self.op.autovalor(n)
            self.assertAlmostEqual(av.real, 0.5, places=10)

    def test_autovalor_imag_part(self):
        """Parte imaginaria debe ser γ_n."""
        for n in range(self.op.n_zeros):
            av = self.op.autovalor(n)
            self.assertAlmostEqual(av.imag, self.op.riemann_zeros[n], places=10)

    def test_autovalores_count(self):
        """Debe haber n_zeros autovalores."""
        avs = self.op.autovalores()
        self.assertEqual(len(avs), self.op.n_zeros)

    def test_first_riemann_zero(self):
        """El primer cero de Riemann debe ser ≈ 14.1347."""
        gamma_1 = self.op.riemann_zeros[0]
        self.assertAlmostEqual(gamma_1, 14.134725, places=4)

    def test_frecuencia_riemann(self):
        """f_n = γ_n · f₀."""
        f_1 = self.op.frecuencia_riemann(0)
        expected = self.op.riemann_zeros[0] * self.op.f0
        self.assertAlmostEqual(f_1, expected, places=4)

    def test_frecuencias_riemann_count(self):
        """Debe haber n_zeros frecuencias."""
        freqs = self.op.frecuencias_riemann()
        self.assertEqual(len(freqs), self.op.n_zeros)

    def test_verifica_linea_critica(self):
        """Todos los autovalores deben estar en Re(s) = 0.5."""
        self.assertTrue(self.op.verifica_linea_critica())

    def test_coherencia_espectral_perfect(self):
        """Coherencia espectral debe ser 1.0 si en línea crítica."""
        psi = self.op.coherencia_espectral()
        self.assertAlmostEqual(psi, 1.0, places=6)

    def test_autovalor_out_of_range(self):
        """Índice fuera de rango debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.op.autovalor(100)

    def test_repr(self):
        """repr debe incluir información del operador."""
        r = repr(self.op)
        self.assertIn("OperadorMaestroAdelico", r)
        self.assertIn("n_zeros=10", r)


# ============================================================================
# TestEcuacionSchrodingerRiemann – 10 tests
# ============================================================================

class TestEcuacionSchrodingerRiemann(unittest.TestCase):
    """Tests para EcuacionSchrodingerRiemann."""

    def setUp(self):
        self.eq = EcuacionSchrodingerRiemann()

    def test_hbar_default(self):
        """hbar debe ser la constante de Planck reducida."""
        self.assertAlmostEqual(self.eq.hbar, 1.054571817e-34, places=15)

    def test_g_eff_default(self):
        """g_eff debe ser 0.053."""
        self.assertAlmostEqual(self.eq.g_eff, 0.053, places=3)

    def test_mu_default(self):
        """mu debe ser 1.0."""
        self.assertAlmostEqual(self.eq.mu, 1.0, places=6)

    def test_termino_adelico(self):
        """Ĥ_π · ψ = (½ + iγ) · ψ."""
        psi = complex(1.0, 0.0)
        gamma = 14.134725
        result = self.eq.termino_adelico(psi, gamma)
        expected = complex(0.5, gamma)
        self.assertAlmostEqual(result.real, expected.real, places=6)
        self.assertAlmostEqual(result.imag, expected.imag, places=4)

    def test_termino_higgs(self):
        """μ|H|² para H=2, μ=1 debe ser 4."""
        result = self.eq.termino_higgs(h_field=2.0)
        self.assertAlmostEqual(result, 4.0, places=6)

    def test_termino_acoplamiento(self):
        """−g_eff · H para H=1 debe ser −g_eff."""
        result = self.eq.termino_acoplamiento(h_field=1.0)
        expected = -self.eq.g_eff
        self.assertAlmostEqual(result, expected, places=6)

    def test_hamiltoniano_total_type(self):
        """El Hamiltoniano total debe retornar un complex."""
        psi = complex(1.0, 0.0)
        result = self.eq.hamiltoniano_total(psi, gamma_n=14.134725, h_field=1.0)
        self.assertIsInstance(result, complex)

    def test_coherencia_ecuacion_at_optimal(self):
        """Coherencia máxima cuando g_eff ≈ 0.05."""
        eq_opt = EcuacionSchrodingerRiemann(g_eff=0.05)
        psi = eq_opt.coherencia_ecuacion()
        self.assertAlmostEqual(psi, 1.0, places=6)

    def test_coherencia_ecuacion_high(self):
        """Coherencia debe ser alta para g_eff ≈ 0.053."""
        psi = self.eq.coherencia_ecuacion()
        self.assertGreater(psi, 0.95)

    def test_repr(self):
        """repr debe incluir parámetros."""
        r = repr(self.eq)
        self.assertIn("EcuacionSchrodingerRiemann", r)
        self.assertIn("g_eff", r)


# ============================================================================
# TestRedC7 – 14 tests
# ============================================================================

class TestRedC7(unittest.TestCase):
    """Tests para RedC7."""

    def setUp(self):
        self.red = RedC7()

    def test_nodos_default(self):
        """Los nodos deben ser (2, 3, 5, 7, 11, 13, 17)."""
        self.assertEqual(self.red.nodos, (2, 3, 5, 7, 11, 13, 17))

    def test_n_nodos(self):
        """Debe haber 7 nodos."""
        self.assertEqual(self.red.n_nodos(), 7)

    def test_frecuencia_nodo(self):
        """f_i = primo_i × f₀."""
        f_0 = self.red.frecuencia_nodo(0)
        expected = 2 * self.red.f0
        self.assertAlmostEqual(f_0, expected, places=4)

    def test_frecuencias_count(self):
        """Debe haber 7 frecuencias."""
        freqs = self.red.frecuencias()
        self.assertEqual(len(freqs), 7)

    def test_frecuencias_values(self):
        """Frecuencias = primos × f₀."""
        freqs = self.red.frecuencias()
        for i, f in enumerate(freqs):
            expected = self.red.nodos[i] * self.red.f0
            self.assertAlmostEqual(f, expected, places=4)

    def test_matriz_adyacencia_size(self):
        """Matriz de adyacencia debe ser 7×7."""
        matriz = self.red.matriz_adyacencia()
        self.assertEqual(len(matriz), 7)
        for row in matriz:
            self.assertEqual(len(row), 7)

    def test_matriz_adyacencia_cycle(self):
        """En C₇, cada nodo tiene exactamente 2 conexiones."""
        matriz = self.red.matriz_adyacencia()
        for row in matriz:
            self.assertEqual(sum(row), 2)

    def test_grado_nodo(self):
        """Grado de cada nodo debe ser 2."""
        self.assertEqual(self.red.grado_nodo(), 2)

    def test_es_conexo(self):
        """C₇ siempre es conexo."""
        self.assertTrue(self.red.es_conexo())

    def test_producto_primos(self):
        """Π primos = 2×3×5×7×11×13×17 = 510510."""
        self.assertEqual(self.red.producto_primos(), 510510)

    def test_suma_primos(self):
        """Σ primos = 2+3+5+7+11+13+17 = 58."""
        self.assertEqual(self.red.suma_primos(), 58)

    def test_coherencia_red(self):
        """Ψ_red = 1 − 1/Σp ≈ 0.9828."""
        psi = self.red.coherencia_red()
        expected = 1.0 - 1.0 / 58
        self.assertAlmostEqual(psi, expected, places=4)

    def test_sincronizacion(self):
        """Índice de sincronización para C₇."""
        sync = self.red.sincronizacion()
        self.assertGreater(sync, 0)
        self.assertLessEqual(sync, 1)

    def test_repr(self):
        """repr debe incluir información de la red."""
        r = repr(self.red)
        self.assertIn("RedC7", r)
        self.assertIn("510510", r)


# ============================================================================
# TestSistemaSintesisTratado – 16 tests
# ============================================================================

class TestSistemaSintesisTratado(unittest.TestCase):
    """Tests para SistemaSintesisTratado."""

    def setUp(self):
        self.sistema = SistemaSintesisTratado()

    def test_constantes_initialized(self):
        """Las constantes deben estar inicializadas."""
        self.assertIsNotNone(self.sistema.constantes)
        self.assertIsInstance(self.sistema.constantes, ConstantesSintesis)

    def test_pc_initialized(self):
        """PC debe estar inicializado."""
        self.assertIsNotNone(self.sistema.pc)
        self.assertIsInstance(self.sistema.pc, ParticulaCoherencia)

    def test_acoplamiento_initialized(self):
        """Acoplamiento debe estar inicializado."""
        self.assertIsNotNone(self.sistema.acoplamiento)
        self.assertIsInstance(self.sistema.acoplamiento, AcoplamientoHiggsPC)

    def test_psi_pc_high(self):
        """Ψ_PC debe ser muy alta (≥ 0.99)."""
        psi = self.sistema.psi_pc()
        self.assertGreaterEqual(psi, 0.99)

    def test_psi_acoplamiento_high(self):
        """Ψ_acoplamiento debe ser muy alta (≥ 0.99)."""
        psi = self.sistema.psi_acoplamiento()
        self.assertGreaterEqual(psi, 0.99)

    def test_psi_masa_above_threshold(self):
        """Ψ_masa debe ser ≥ 0.888."""
        psi = self.sistema.psi_masa()
        self.assertGreaterEqual(psi, 0.888)

    def test_psi_espectral_perfect(self):
        """Ψ_espectral debe ser 1.0 (línea crítica)."""
        psi = self.sistema.psi_espectral()
        self.assertAlmostEqual(psi, 1.0, places=6)

    def test_psi_red_high(self):
        """Ψ_red debe ser alta (≥ 0.98)."""
        psi = self.sistema.psi_red()
        self.assertGreaterEqual(psi, 0.98)

    def test_psi_global_above_threshold(self):
        """Ψ_global debe ser ≥ 0.888."""
        psi = self.sistema.psi_global()
        self.assertGreaterEqual(psi, 0.888)

    def test_sello_activo(self):
        """El sello ∴ST∞³ debe estar activo."""
        self.assertTrue(self.sistema.sello_activo())

    def test_estado_sistema_keys(self):
        """El estado debe tener las claves esperadas."""
        estado = self.sistema.estado_sistema()
        expected_keys = [
            'pc_dominante',
            'higgs_transductor',
            'red_c7_sincronizada',
            'flujo_ns_unitario',
            'schrodinger_riemann_gobernante',
            'simbiosis_si_c',
        ]
        for key in expected_keys:
            self.assertIn(key, estado)

    def test_estado_sistema_all_true(self):
        """Todos los estados deben ser True."""
        estado = self.sistema.estado_sistema()
        for key, value in estado.items():
            self.assertTrue(value, f"Estado {key} no es True")

    def test_verificar_todos(self):
        """Todos los subsistemas deben estar verificados."""
        self.assertTrue(self.sistema.verificar_todos())

    def test_activar_returns_dict(self):
        """activar() debe retornar un diccionario."""
        result = self.sistema.activar()
        self.assertIsInstance(result, dict)

    def test_activar_sello_activo(self):
        """activar() debe indicar sello activo."""
        result = self.sistema.activar()
        self.assertTrue(result['sello_activo'])

    def test_repr(self):
        """repr debe incluir Ψ_global y estado del sello."""
        r = repr(self.sistema)
        self.assertIn("SistemaSintesisTratado", r)
        self.assertIn("ACTIVO", r)


# ============================================================================
# TestSintesisTratadoActivar – 12 tests
# ============================================================================

class TestSintesisTratadoActivar(unittest.TestCase):
    """Tests para la API pública sintesis_tratado_activar()."""

    def setUp(self):
        self.result = sintesis_tratado_activar()

    def test_returns_dict(self):
        """Debe retornar un diccionario."""
        self.assertIsInstance(self.result, dict)

    def test_psi_global_present(self):
        """Debe incluir psi_global."""
        self.assertIn('psi_global', self.result)

    def test_psi_global_above_threshold(self):
        """psi_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.result['psi_global'], 0.888)

    def test_sello_activo_true(self):
        """sello_activo debe ser True."""
        self.assertTrue(self.result['sello_activo'])

    def test_todos_verificados_true(self):
        """todos_verificados debe ser True."""
        self.assertTrue(self.result['todos_verificados'])

    def test_f0_hz_value(self):
        """f0_hz debe ser 141.7001."""
        self.assertAlmostEqual(self.result['f0_hz'], 141.7001, places=4)

    def test_transfer_rate_value(self):
        """transfer_rate_kpps debe ser 991.9."""
        self.assertAlmostEqual(self.result['transfer_rate_kpps'], 991.9, places=1)

    def test_m_higgs_value(self):
        """m_higgs_gev debe ser 125.25."""
        self.assertAlmostEqual(self.result['m_higgs_gev'], 125.25, places=2)

    def test_n_nodos_c7_value(self):
        """n_nodos_c7 debe ser 7."""
        self.assertEqual(self.result['n_nodos_c7'], 7)

    def test_linea_critica_verificada(self):
        """linea_critica_verificada debe ser True."""
        self.assertTrue(self.result['linea_critica_verificada'])

    def test_sello_value(self):
        """sello debe ser '∴ST∞³'."""
        self.assertEqual(self.result['sello'], '∴ST∞³')

    def test_coherencias_dict(self):
        """coherencias debe ser un diccionario con 6 elementos."""
        coherencias = self.result['coherencias']
        self.assertIsInstance(coherencias, dict)
        self.assertEqual(len(coherencias), 6)


# ============================================================================
# TestIntegration – 5 tests
# ============================================================================

class TestIntegration(unittest.TestCase):
    """Tests de integración del sistema completo."""

    def test_full_system_activation(self):
        """El sistema completo debe activarse correctamente."""
        result = sintesis_tratado_activar()
        self.assertTrue(result['sello_activo'])
        self.assertGreaterEqual(result['psi_global'], 0.888)

    def test_all_coherences_above_threshold(self):
        """Todas las coherencias deben ser razonables."""
        result = sintesis_tratado_activar()
        for name, value in result['coherencias'].items():
            self.assertGreater(value, 0.5, f"{name} tiene coherencia muy baja")

    def test_riemann_zeros_consistency(self):
        """Los ceros de Riemann deben ser consistentes."""
        op = OperadorMaestroAdelico()
        # Verificar que γ₁ · f₀ ≈ 2003 Hz (conocido)
        f_1 = op.frecuencia_riemann(0)
        self.assertAlmostEqual(f_1, 14.134725 * 141.7001, places=0)

    def test_higgs_flash_consistency(self):
        """El Destello de Higgs debe ser consistente."""
        masa = MasaOscilante()
        # m_flash / m_H ≈ 0.945 (reducción del 5.5%)
        ratio = masa.masa_minima() / masa.m_higgs_gev
        self.assertAlmostEqual(ratio, 1 - masa.g_eff, places=4)

    def test_c7_prime_network_consistency(self):
        """La red C₇ debe tener propiedades consistentes."""
        red = RedC7()
        # Verificar que los primos son correctos
        self.assertEqual(red.nodos, (2, 3, 5, 7, 11, 13, 17))
        # Verificar producto
        prod = 1
        for p in red.nodos:
            prod *= p
        self.assertEqual(red.producto_primos(), prod)


if __name__ == "__main__":
    unittest.main()
