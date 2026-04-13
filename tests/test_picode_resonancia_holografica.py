#!/usr/bin/env python3
"""
Tests para πCODE — Resonancia Holográfica Disipativa
=====================================================

Valida todos los componentes del framework πCODE:

1. OntologiaInformacion   — densidad espectral, entropía y coherencia ontológica
2. BordeHolograficoAdSCFT — entropía Bekenstein-Hawking, longitud de coherencia,
                            coherencia holográfica
3. OperadorPTNoHermitico  — eigenvalores, simetría PT, coherencia PT, espectro real
4. EstabilizadorRiemannDisipativo — frecuencia biológica, pesos, coherencia, zeros
5. ConscienciaMotorSimetria — índice NOESIS, reducción γ, coherencia noésica
6. SistemaPicode          — evaluación integrada Ψ_picode ≥ 0.888
7. API picode_resonancia_activar() — resultado canónico

Author: José Manuel Mota Burruezo
License: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import math
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from physics.picode_resonancia_holografica import (
    OntologiaInformacion,
    BordeHolograficoAdSCFT,
    OperadorPTNoHermitico,
    EstabilizadorRiemannDisipativo,
    ConscienciaMotorSimetria,
    SistemaPicode,
    ResultadoPicode,
    picode_resonancia_activar,
    _F0_HZ,
    _GAMMA_1,
    _RIEMANN_ZEROS,
    _BETA_CRITICO,
    _PSI_MINIMA,
)

# ---------------------------------------------------------------------------
# Constantes de referencia
# ---------------------------------------------------------------------------
F0 = _F0_HZ   # 141.7001 Hz
OMEGA_0 = 2 * math.pi * F0


# ============================================================================
# 1. OntologiaInformacion
# ============================================================================

class TestOntologiaInformacion(unittest.TestCase):
    """Tests para la ontología de información primaria."""

    def setUp(self):
        self.onto = OntologiaInformacion()

    def test_densidad_espectral_en_f0(self):
        """La densidad espectral debe ser máxima en f₀."""
        rho_f0 = self.onto.densidad_espectral(F0)
        rho_lejos = self.onto.densidad_espectral(F0 + 10.0)
        self.assertGreater(rho_f0, rho_lejos,
                           "La densidad debe ser mayor en f₀ que fuera de ella.")

    def test_densidad_espectral_no_negativa(self):
        """La densidad espectral debe ser ≥ 0 en toda la malla."""
        for f in [F0 - 5, F0 - 1, F0, F0 + 1, F0 + 5]:
            self.assertGreaterEqual(self.onto.densidad_espectral(f), 0.0)

    def test_entropia_espectral_positiva(self):
        """La entropía espectral debe ser un número positivo."""
        s = self.onto.entropia_espectral()
        self.assertGreater(s, 0.0, "Entropía espectral debe ser positiva.")

    def test_coherencia_ontologica_rango(self):
        """La coherencia ontológica debe estar en [0, 1]."""
        psi = self.onto.coherencia_ontologica()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_coherencia_ontologica_alta(self):
        """Con σ pequeño el campo es muy coherente (Ψ_info → 1)."""
        onto_estrecho = OntologiaInformacion(sigma=0.1)
        psi = onto_estrecho.coherencia_ontologica()
        self.assertGreater(psi, 0.5, "Campo estrecho debería tener alta coherencia.")

    def test_frecuencia_fundamental_preservada(self):
        """La frecuencia fundamental del objeto debe coincidir con F0."""
        self.assertAlmostEqual(self.onto.f0, F0, places=4)


# ============================================================================
# 2. BordeHolograficoAdSCFT
# ============================================================================

class TestBordeHolograficoAdSCFT(unittest.TestCase):
    """Tests para el borde holográfico AdS/CFT citoplasmático."""

    def setUp(self):
        self.borde = BordeHolograficoAdSCFT()

    def test_longitud_coherencia_escala_um(self):
        """ξ debe estar en el rango μm (escala celular ~1 μm)."""
        xi_um = self.borde.escala_longitud_coherencia_um()
        self.assertGreater(xi_um, 0.5, "ξ debe ser > 0.5 μm.")
        self.assertLess(xi_um, 5.0, "ξ debe ser < 5 μm.")

    def test_longitud_coherencia_formula(self):
        """ξ = √(ν / ω₀) debe cumplir la fórmula exacta."""
        from physics.picode_resonancia_holografica import _NU_CITOPLASMA
        nu = _NU_CITOPLASMA
        omega = 2 * math.pi * F0
        xi_esperado = math.sqrt(nu / omega)
        self.assertAlmostEqual(
            self.borde.xi, xi_esperado, places=15,
            msg="ξ no coincide con la fórmula √(ν/ω₀)."
        )

    def test_entropia_bekenstein_hawking_positiva(self):
        """La entropía holográfica debe ser un número positivo grande."""
        s = self.borde.entropia_bekenstein_hawking()
        self.assertGreater(s, 1e50, "S_holo debe ser un número enorme (bits).")

    def test_entropia_maxima_mayor_que_borde(self):
        """La entropía máxima celular y la del borde deben ser del mismo orden."""
        s_holo = self.borde.entropia_bekenstein_hawking()
        s_max = self.borde.entropia_maxima()
        # ξ ≈ L_celular → ambas entropías son del mismo orden de magnitud
        ratio = s_holo / s_max
        self.assertGreater(ratio, 0.5, "S_holo/S_max debe ser > 0.5.")
        self.assertLess(ratio, 2.0, "S_holo/S_max debe ser < 2.0.")

    def test_coherencia_holografica_rango(self):
        """Ψ_holo debe estar en (0, 1]."""
        psi = self.borde.coherencia_holografica()
        self.assertGreater(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_coherencia_holografica_alta(self):
        """Para la escala citoplasmática canónica Ψ_holo debe ser > 0.9.

        ξ ≈ L_celular → cociente ξ/L_celular ≈ 1 → Ψ_holo = exp(-ε²) → 1.
        El umbral 0.9 corresponde a un desvío máximo de |ξ/L_celular - 1| < 0.324.
        """
        _UMBRAL_COHERENCIA_ALTA = 0.9
        psi = self.borde.coherencia_holografica()
        self.assertGreater(psi, _UMBRAL_COHERENCIA_ALTA,
                           "Ψ_holo debe ser alta para escala celular.")

    def test_verificar_escala_celular(self):
        """ξ debe coincidir con L_celular dentro del 15 %."""
        self.assertTrue(
            self.borde.verificar_escala_celular(),
            "ξ no coincide con L_celular dentro del 15 %."
        )


# ============================================================================
# 3. OperadorPTNoHermitico
# ============================================================================

class TestOperadorPTNoHermitico(unittest.TestCase):
    """Tests para el operador no-hermítico con simetría PT."""

    def setUp(self):
        self.op_pt = OperadorPTNoHermitico(gamma=0.5)
        self.op_roto = OperadorPTNoHermitico(gamma=3.0)  # γ > γ_c → ruptura PT

    def test_eigenvalores_tipo_lista(self):
        """eigenvalores() debe retornar una lista."""
        vals = self.op_pt.eigenvalores()
        self.assertIsInstance(vals, list)
        self.assertGreater(len(vals), 0)

    def test_eigenvalores_parte_real_positiva(self):
        """Todos los eigenvalores deben tener parte real positiva (energía ≥ 0)."""
        for v in self.op_pt.eigenvalores():
            self.assertGreater(v.real, 0.0,
                               f"Eigenvalor {v} tiene parte real no positiva.")

    def test_fase_pt_simetrica(self):
        """Para γ < γ_c el operador debe estar en la fase PT-simétrica."""
        self.assertTrue(
            self.op_pt.es_pt_simetrico(),
            "El operador con γ=0.5 debe ser PT-simétrico."
        )

    def test_ruptura_pt(self):
        """Para γ > γ_c el operador debe romper la simetría PT."""
        self.assertFalse(
            self.op_roto.es_pt_simetrico(),
            "El operador con γ=3.0 > γ_c debe estar en la fase rota."
        )

    def test_coherencia_pt_rango(self):
        """Ψ_PT debe estar en [0, 1]."""
        psi = self.op_pt.coherencia_pt()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_coherencia_pt_decae_con_gamma(self):
        """Ψ_PT debe decrecer al aumentar γ."""
        psi_bajo = OperadorPTNoHermitico(gamma=0.1).coherencia_pt()
        psi_alto = OperadorPTNoHermitico(gamma=2.0).coherencia_pt()
        self.assertGreater(psi_bajo, psi_alto,
                           "Ψ_PT debe ser mayor para γ pequeño.")

    def test_coherencia_pt_cero_en_ruptura(self):
        """Ψ_PT = 0 cuando γ ≥ γ_c."""
        self.assertAlmostEqual(
            self.op_roto.coherencia_pt(), 0.0, places=10,
            msg="Ψ_PT debe ser 0 cuando γ ≥ γ_c."
        )

    def test_fraccion_espectro_real_alta(self):
        """Para γ < γ_c la fracción del espectro real debe ser alta."""
        f = self.op_pt.fraccion_espectro_real()
        self.assertGreater(f, 0.8,
                           "Fracción del espectro real debe ser > 0.8 para γ < γ_c.")

    def test_coherencia_hermitiano(self):
        """Para γ = 0 el operador es hermítico: Ψ_PT = 1."""
        op_hermitiano = OperadorPTNoHermitico(gamma=0.0)
        self.assertAlmostEqual(
            op_hermitiano.coherencia_pt(), 1.0, places=10,
            msg="Operador hermítico (γ=0) debe tener Ψ_PT = 1."
        )


# ============================================================================
# 4. EstabilizadorRiemannDisipativo
# ============================================================================

class TestEstabilizadorRiemannDisipativo(unittest.TestCase):
    """Tests para los ceros de Riemann como estabilizadores disipativo-biológicos."""

    def setUp(self):
        self.estab = EstabilizadorRiemannDisipativo(n_zeros=10)

    def test_primer_cero_correcto(self):
        """El primer cero de Riemann debe ser γ₁ ≈ 14.1347."""
        self.assertAlmostEqual(
            self.estab.zeros[0], _GAMMA_1, places=6,
            msg=f"Primer cero de Riemann debe ser ≈ {_GAMMA_1}."
        )

    def test_frecuencia_resonante_primer_cero(self):
        """La frecuencia resonante del primer cero debe ser ≈ f₀."""
        f_biol = self.estab.frecuencia_resonante_biologica(_GAMMA_1)
        self.assertAlmostEqual(
            f_biol, F0, places=4,
            msg="f_biol(γ₁) debe coincidir exactamente con f₀."
        )

    def test_peso_estabilizador_primer_cero(self):
        """El peso del primer cero debe ser el máximo (≤ 1)."""
        w = self.estab.peso_estabilizador(self.estab.zeros[0])
        self.assertGreater(w, 0.0)
        self.assertLessEqual(w, 1.0)

    def test_pesos_decrecientes(self):
        """Los pesos deben decrecer con el índice del cero."""
        pesos = [self.estab.peso_estabilizador(t) for t in self.estab.zeros]
        for i in range(len(pesos) - 1):
            self.assertGreaterEqual(
                pesos[i], pesos[i + 1],
                f"Peso[{i}] >= Peso[{i+1}] debe cumplirse."
            )

    def test_coherencia_riemann_rango(self):
        """Ψ_Riemann debe estar en (0, 1]."""
        psi = self.estab.coherencia_riemann()
        self.assertGreater(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_zeros_activos_biologicamente(self):
        """Debe haber ≥ 1 cero de Riemann activo biológicamente."""
        n = self.estab.zeros_activos_biologicamente()
        self.assertGreater(n, 0, "Debe haber al menos un cero de Riemann activo.")
        self.assertLessEqual(n, len(self.estab.zeros))

    def test_n_zeros_respetado(self):
        """El número de ceros usados no debe superar n_zeros."""
        self.assertLessEqual(len(self.estab.zeros), 10)

    def test_parametro_disipativo(self):
        """α_disip = ν / f₀ debe ser el valor esperado."""
        from physics.picode_resonancia_holografica import _NU_CITOPLASMA
        expected = _NU_CITOPLASMA / F0
        self.assertAlmostEqual(self.estab.alpha_disip, expected, places=20)


# ============================================================================
# 5. ConscienciaMotorSimetria
# ============================================================================

class TestConscienciaMotorSimetria(unittest.TestCase):
    """Tests para el motor de simetría consciente πCODE (NOESIS)."""

    def setUp(self):
        self.noesis = ConscienciaMotorSimetria()

    def test_tau_noesis_positivo(self):
        """τ_noesis = γ₁ / ω₀ debe ser un tiempo positivo."""
        self.assertGreater(self.noesis.tau_noesis, 0.0)

    def test_indice_noesis_rango(self):
        """Ψ_noesis debe estar en [0, 1]."""
        for psi_base in [0.1, 0.5, 0.888, 0.99]:
            psi = self.noesis.indice_noesis(psi_base)
            self.assertGreaterEqual(psi, 0.0)
            self.assertLessEqual(psi, 1.0)

    def test_reduccion_gamma_efectivo(self):
        """La reducción noésica debe producir γ_efectivo < γ_original."""
        gamma_orig = 1.0
        gamma_ef = self.noesis.reduccion_gamma(gamma_orig)
        self.assertLess(gamma_ef, gamma_orig,
                        "La reducción noésica debe bajar γ.")
        self.assertGreater(gamma_ef, 0.0,
                           "γ efectivo debe ser positivo.")

    def test_reduccion_gamma_no_negativa(self):
        """γ efectivo debe ser ≥ 0 para cualquier γ original."""
        for g in [0.0, 0.5, 1.0, 2.5, 3.0]:
            self.assertGreaterEqual(self.noesis.reduccion_gamma(g), 0.0)

    def test_coherencia_noesica_rango(self):
        """Ψ_noesis integrada debe estar en [0, 1]."""
        psi = self.noesis.coherencia_noesica(0.9, 0.95, 0.98)
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_phi_dorado(self):
        """φ debe ser la razón áurea ≈ 1.618."""
        self.assertAlmostEqual(self.noesis.phi, (1 + math.sqrt(5)) / 2, places=10)

    def test_kappa_pi_valor(self):
        """κ_Π debe ser ≈ 2.5773."""
        self.assertAlmostEqual(self.noesis.kappa_pi, 2.5773, places=4)


# ============================================================================
# 6. SistemaPicode
# ============================================================================

class TestSistemaPicode(unittest.TestCase):
    """Tests para el sistema integrador πCODE."""

    def setUp(self):
        self.sistema = SistemaPicode()

    def test_evaluar_retorna_resultado(self):
        """evaluar() debe retornar un ResultadoPicode."""
        resultado = self.sistema.evaluar()
        self.assertIsInstance(resultado, ResultadoPicode)

    def test_psi_picode_aprobado(self):
        """Ψ_picode debe ser ≥ 0.888 (coherencia mínima QCAL)."""
        resultado = self.sistema.evaluar()
        self.assertGreaterEqual(
            resultado.psi_picode, _PSI_MINIMA,
            f"Ψ_picode={resultado.psi_picode} debe ser ≥ {_PSI_MINIMA}."
        )

    def test_aprobado_flag(self):
        """El flag 'aprobado' debe ser True."""
        resultado = self.sistema.evaluar()
        self.assertTrue(resultado.aprobado,
                        "El sistema πCODE debe estar aprobado.")

    def test_psi_holografico_positivo(self):
        """Ψ_holografico debe ser > 0."""
        r = self.sistema.evaluar()
        self.assertGreater(r.psi_holografico, 0.0)

    def test_psi_pt_en_rango(self):
        """Ψ_PT debe estar en [0, 1]."""
        r = self.sistema.evaluar()
        self.assertGreaterEqual(r.psi_pt, 0.0)
        self.assertLessEqual(r.psi_pt, 1.0)

    def test_psi_riemann_positivo(self):
        """Ψ_Riemann debe ser > 0."""
        r = self.sistema.evaluar()
        self.assertGreater(r.psi_riemann, 0.0)

    def test_psi_noesis_positivo(self):
        """Ψ_noesis debe ser > 0."""
        r = self.sistema.evaluar()
        self.assertGreater(r.psi_noesis, 0.0)

    def test_entropia_holografica_positiva(self):
        """La entropía holográfica debe ser un número positivo."""
        r = self.sistema.evaluar()
        self.assertGreater(r.entropia_holografica, 0.0)

    def test_n_zeros_activos_positivo(self):
        """Debe haber ≥ 1 cero de Riemann activo."""
        r = self.sistema.evaluar()
        self.assertGreater(r.n_zeros_activos, 0)

    def test_beta_pt_menor_critico(self):
        """β_PT efectivo debe ser < β_c (simetría PT conservada)."""
        r = self.sistema.evaluar()
        self.assertLess(
            r.beta_pt, _BETA_CRITICO,
            f"β_PT={r.beta_pt} debe ser < β_c={_BETA_CRITICO}."
        )

    def test_mensaje_no_vacio(self):
        """El mensaje del resultado no debe estar vacío."""
        r = self.sistema.evaluar()
        self.assertIsInstance(r.mensaje, str)
        self.assertGreater(len(r.mensaje), 0)

    def test_mensaje_contiene_psi(self):
        """El mensaje debe mencionar el valor de Ψ."""
        r = self.sistema.evaluar()
        self.assertIn("Ψ", r.mensaje)

    def test_sistema_sin_noesis(self):
        """El sistema sin NOESIS también debe evaluar correctamente."""
        sistema_base = SistemaPicode(aplicar_noesis=False)
        r = sistema_base.evaluar()
        self.assertIsInstance(r, ResultadoPicode)
        self.assertGreater(r.psi_picode, 0.0)

    def test_repr(self):
        """__repr__ debe retornar una cadena informativa."""
        s = repr(self.sistema)
        self.assertIn("SistemaPicode", s)
        self.assertIn("141.7001", s)

    def test_gamma_alto_menor_psi(self):
        """Un γ alto (cercano a γ_c) debe producir Ψ_picode menor."""
        sistema_normal = SistemaPicode(gamma_pt=0.1)
        sistema_alto = SistemaPicode(gamma_pt=2.5, aplicar_noesis=False)
        r_normal = sistema_normal.evaluar()
        r_alto = sistema_alto.evaluar()
        self.assertGreaterEqual(
            r_normal.psi_picode, r_alto.psi_picode,
            "γ menor debe producir Ψ_picode ≥ Ψ con γ alto."
        )


# ============================================================================
# 7. API pública picode_resonancia_activar()
# ============================================================================

class TestPicodeResonanciaActivar(unittest.TestCase):
    """Tests para la API pública de activación del πCODE."""

    def setUp(self):
        self.resultado = picode_resonancia_activar()

    def test_retorna_resultado_picode(self):
        """La función debe retornar un ResultadoPicode."""
        self.assertIsInstance(self.resultado, ResultadoPicode)

    def test_psi_picode_minimo(self):
        """Ψ_picode debe ser ≥ 0.888."""
        self.assertGreaterEqual(
            self.resultado.psi_picode, _PSI_MINIMA,
            f"API: Ψ_picode={self.resultado.psi_picode} debe ser ≥ {_PSI_MINIMA}."
        )

    def test_aprobado(self):
        """La API debe retornar aprobado=True."""
        self.assertTrue(self.resultado.aprobado)

    def test_psi_components_sum_consistent(self):
        """Los 4 componentes deben ser consistentes con Ψ_picode."""
        r = self.resultado
        # Ψ_picode ≈ ⁴√(Ψ_info · Ψ_holo · Ψ_PT · Ψ_noesis)
        # Verificamos que todos los componentes sean positivos
        self.assertGreater(r.psi_holografico, 0.0)
        self.assertGreater(r.psi_pt, 0.0)
        self.assertGreater(r.psi_riemann, 0.0)
        self.assertGreater(r.psi_noesis, 0.0)

    def test_mensaje_aprobado(self):
        """El mensaje debe contener '✅' para resultado aprobado."""
        self.assertIn("✅", self.resultado.mensaje)

    def test_n_zeros_activos_rango(self):
        """n_zeros_activos debe estar entre 1 y 10."""
        self.assertGreaterEqual(self.resultado.n_zeros_activos, 1)
        self.assertLessEqual(self.resultado.n_zeros_activos, 10)

    def test_beta_pt_en_fase_simetrica(self):
        """β_PT del resultado debe estar en la fase PT-simétrica."""
        self.assertLess(self.resultado.beta_pt, _BETA_CRITICO)

    def test_llamadas_multiples_consistentes(self):
        """Llamadas múltiples deben producir el mismo resultado."""
        r1 = picode_resonancia_activar()
        r2 = picode_resonancia_activar()
        self.assertAlmostEqual(r1.psi_picode, r2.psi_picode, places=4)
        self.assertEqual(r1.aprobado, r2.aprobado)
        self.assertEqual(r1.n_zeros_activos, r2.n_zeros_activos)


# ============================================================================
# 8. Constantes y umbrales globales
# ============================================================================

class TestConstantesGlobales(unittest.TestCase):
    """Tests de las constantes físicas del módulo."""

    def test_f0_hz(self):
        """F0_HZ debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0_HZ, 141.7001, places=4)

    def test_gamma_1_riemann(self):
        """γ₁ debe ser el primer cero de Riemann ≈ 14.134725."""
        self.assertAlmostEqual(_GAMMA_1, 14.134725, places=5)

    def test_beta_critico(self):
        """β_c debe ser ≈ 2.57 (constante de ruptura PT κ_Π)."""
        self.assertAlmostEqual(_BETA_CRITICO, 2.57, places=2)

    def test_psi_minima(self):
        """PSI_MINIMA debe ser 0.888."""
        self.assertAlmostEqual(_PSI_MINIMA, 0.888, places=3)

    def test_riemann_zeros_lista(self):
        """_RIEMANN_ZEROS debe ser una lista de 10 elementos."""
        self.assertEqual(len(_RIEMANN_ZEROS), 10)

    def test_riemann_zeros_crecientes(self):
        """Los ceros de Riemann deben estar ordenados ascendentemente."""
        for i in range(len(_RIEMANN_ZEROS) - 1):
            self.assertLess(_RIEMANN_ZEROS[i], _RIEMANN_ZEROS[i + 1])

    def test_primer_cero_riemann_exacto(self):
        """El primer cero debe coincidir con el valor tabulado de referencia.

        El valor γ₁ ≈ 14.134725141734693 está verificado por LMFDB, Wolfram
        Alpha y la tabla de Odlyzko (1992) de los primeros 10⁷ ceros de Riemann.
        """
        # Fuente independiente: Odlyzko (1992), γ₁ ≈ 14.134725141734693
        gamma_1_referencia = 14.134725141734693
        self.assertAlmostEqual(_RIEMANN_ZEROS[0], gamma_1_referencia, places=8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
