# pruebas_entropia_informativa.py — Tests unitarios de EntropiaInformativa

# Licencia: CERN-OHL-P v2 - Hardware Libre + MIT (software)

# Autor: JMMB — José Manuel Mota Burruezo

# ∴𓂀Ω∞³

"""Tests unitarios para el módulo entropia_informativa."""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.entropia_informativa import (
    EntropiaInformativa,
    F0,
    NC,
    C_LUZ,
    HBAR,
    PHI,
    GAMMA_1,
    CEROS_RIEMANN,
    PSI_OPTIMO,
    PSI_CRITICO,
)


class PruebasConstantesFundamentales(unittest.TestCase):

    """Verifica que las constantes importadas son coherentes con qcal_lib."""

    def test_f0_valor(self):
        """F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(F0, 141.7001, places=4)

    def test_nc_escala(self):
        """NC debe ser 10^52."""
        self.assertAlmostEqual(math.log10(NC), 52.0, places=3)

    def test_c_luz(self):
        """Velocidad de la luz debe ser 299 792 458 m/s."""
        self.assertEqual(C_LUZ, 299792458)

    def test_hbar(self):
        """ℏ debe ser ≈ 1.0546e-34 J·s."""
        self.assertAlmostEqual(HBAR, 1.054571817e-34, places=40)

    def test_phi(self):
        """φ debe ser (1 + √5) / 2 ≈ 1.6180."""
        self.assertAlmostEqual(PHI, (1 + math.sqrt(5)) / 2, places=12)

    def test_gamma1(self):
        """γ₁ debe ser ≈ 14.1347."""
        self.assertAlmostEqual(GAMMA_1, 14.134725141734693, places=9)

    def test_ceros_riemann_longitud(self):
        """Deben definirse exactamente 10 ceros de Riemann."""
        self.assertEqual(len(CEROS_RIEMANN), 10)

    def test_ceros_riemann_ordenados(self):
        """Los ceros de Riemann deben estar ordenados de forma creciente."""
        for i in range(len(CEROS_RIEMANN) - 1):
            self.assertLess(CEROS_RIEMANN[i], CEROS_RIEMANN[i + 1])


class PruebasInicializacion(unittest.TestCase):

    """Verifica la inicialización del objeto EntropiaInformativa."""

    def test_defaults(self):
        """Los valores por defecto deben coincidir con las constantes del módulo."""
        ei = EntropiaInformativa()
        self.assertEqual(ei.f0, F0)
        self.assertEqual(ei.nc, NC)
        self.assertEqual(ei.psi, PSI_OPTIMO)

    def test_parametros_personalizados(self):
        """El constructor debe aceptar parámetros personalizados."""
        ei = EntropiaInformativa(f0=200.0, nc=1e50, psi=0.9)
        self.assertEqual(ei.f0, 200.0)
        self.assertEqual(ei.nc, 1e50)
        self.assertEqual(ei.psi, 0.9)

    def test_error_f0_no_positivo(self):
        """Debe lanzar ValueError si f0 ≤ 0."""
        with self.assertRaises(ValueError):
            EntropiaInformativa(f0=0.0)
        with self.assertRaises(ValueError):
            EntropiaInformativa(f0=-1.0)

    def test_error_nc_no_positivo(self):
        """Debe lanzar ValueError si nc ≤ 0."""
        with self.assertRaises(ValueError):
            EntropiaInformativa(nc=0.0)
        with self.assertRaises(ValueError):
            EntropiaInformativa(nc=-1e52)

    def test_error_psi_fuera_rango(self):
        """Debe lanzar ValueError si psi no está en [0, 1]."""
        with self.assertRaises(ValueError):
            EntropiaInformativa(psi=-0.1)
        with self.assertRaises(ValueError):
            EntropiaInformativa(psi=1.1)

    def test_psi_limites_validos(self):
        """psi = 0 y psi = 1 son valores frontera válidos."""
        ei_min = EntropiaInformativa(psi=0.0)
        ei_max = EntropiaInformativa(psi=1.0)
        self.assertEqual(ei_min.psi, 0.0)
        self.assertEqual(ei_max.psi, 1.0)


class PruebasKPsi(unittest.TestCase):

    """Verifica el cálculo de la constante de unificación K_Ψ."""

    def setUp(self):
        self.ei = EntropiaInformativa()

    def test_formula_k_psi(self):
        """K_Ψ = (f₀ × N_c) / (c × ℏ)."""
        esperado = (F0 * NC) / (C_LUZ * HBAR)
        self.assertAlmostEqual(self.ei.k_psi(), esperado, places=5)

    def test_k_psi_positivo(self):
        """K_Ψ debe ser siempre positivo."""
        self.assertGreater(self.ei.k_psi(), 0.0)

    def test_k_psi_escala_con_f0(self):
        """Duplicar f0 debe duplicar K_Ψ."""
        ei2 = EntropiaInformativa(f0=F0 * 2)
        self.assertAlmostEqual(ei2.k_psi(), self.ei.k_psi() * 2, places=5)

    def test_k_psi_cache(self):
        """K_Ψ debe retornar el mismo objeto en llamadas repetidas (caché)."""
        v1 = self.ei.k_psi()
        v2 = self.ei.k_psi()
        self.assertIs(v1, v2)

    def test_k_psi_magnitud(self):
        """K_Ψ para f₀ = 141.7001 Hz debe ser del orden 10^79."""
        k = self.ei.k_psi()
        self.assertGreater(math.log10(k), 75)
        self.assertLess(math.log10(k), 85)


class PruebasDensidadEntropia(unittest.TestCase):

    """Verifica el cálculo de la densidad de entropía informativa."""

    def setUp(self):
        self.ei = EntropiaInformativa(psi=PSI_OPTIMO)

    def test_densidad_base(self):
        """S(f₀) = K_Ψ × Ψ."""
        esperado = self.ei.k_psi() * PSI_OPTIMO
        self.assertAlmostEqual(self.ei.densidad_entropia(), esperado, places=5)

    def test_densidad_escala_lineal(self):
        """S(2·f₀) = 2 × S(f₀)."""
        s1 = self.ei.densidad_entropia(F0)
        s2 = self.ei.densidad_entropia(F0 * 2)
        self.assertAlmostEqual(s2, 2 * s1, places=5)

    def test_densidad_psi_cero(self):
        """Con psi = 0 la densidad es cero."""
        ei_cero = EntropiaInformativa(psi=0.0)
        self.assertEqual(ei_cero.densidad_entropia(), 0.0)

    def test_densidad_frecuencia_positiva(self):
        """Debe lanzar ValueError si la frecuencia no es positiva."""
        with self.assertRaises(ValueError):
            self.ei.densidad_entropia(0.0)
        with self.assertRaises(ValueError):
            self.ei.densidad_entropia(-100.0)

    def test_densidad_sin_argumento_usa_f0(self):
        """Sin argumento, densidad_entropia() usa f₀ por defecto."""
        self.assertAlmostEqual(
            self.ei.densidad_entropia(),
            self.ei.densidad_entropia(self.ei.f0),
            places=10,
        )


class PruebasSaltoEntropia(unittest.TestCase):

    """Verifica el salto de entropía asociado a los ceros de Riemann."""

    def setUp(self):
        self.ei = EntropiaInformativa()

    def test_salto_gamma1_es_cero(self):
        """ΔS(γ₁) = K_Ψ × ln(γ₁/γ₁) = 0."""
        self.assertAlmostEqual(self.ei.salto_entropia_riemann(GAMMA_1), 0.0, places=10)

    def test_salto_crece_con_gamma(self):
        """ΔS(γ_n) debe crecer con n (los ceros están ordenados)."""
        saltos = [self.ei.salto_entropia_riemann(g) for g in CEROS_RIEMANN]
        for i in range(len(saltos) - 1):
            self.assertLess(saltos[i], saltos[i + 1])

    def test_salto_negativo_invalido(self):
        """Debe lanzar ValueError si gamma_n ≤ 0."""
        with self.assertRaises(ValueError):
            self.ei.salto_entropia_riemann(0.0)
        with self.assertRaises(ValueError):
            self.ei.salto_entropia_riemann(-5.0)

    def test_salto_formula(self):
        """ΔS_n = K_Ψ × ln(γ_n / γ_1)."""
        gn = CEROS_RIEMANN[4]  # γ₅
        esperado = self.ei.k_psi() * math.log(gn / GAMMA_1)
        self.assertAlmostEqual(self.ei.salto_entropia_riemann(gn), esperado, places=5)


class PruebasEspectroEntropia(unittest.TestCase):

    """Verifica la generación del espectro entrópico completo."""

    def setUp(self):
        self.ei = EntropiaInformativa()

    def test_espectro_longitud_default(self):
        """El espectro por defecto debe tener 10 entradas."""
        esp = self.ei.espectro_entropia()
        self.assertEqual(len(esp), 10)

    def test_espectro_claves(self):
        """Cada entrada del espectro debe tener las claves correctas."""
        entrada = self.ei.espectro_entropia()[0]
        self.assertIn("gamma", entrada)
        self.assertIn("f_resonancia", entrada)
        self.assertIn("delta_S", entrada)
        self.assertIn("psi_relativa", entrada)

    def test_espectro_f_resonancia_gamma1(self):
        """Para γ₁, la frecuencia de resonancia debe ser f₀."""
        entrada = self.ei.espectro_entropia()[0]
        self.assertAlmostEqual(entrada["f_resonancia"], self.ei.f0, places=6)

    def test_espectro_delta_S_gamma1_cero(self):
        """Para γ₁, ΔS debe ser 0."""
        entrada = self.ei.espectro_entropia()[0]
        self.assertAlmostEqual(entrada["delta_S"], 0.0, places=8)

    def test_espectro_psi_relativa_valida(self):
        """Las coherencias relativas deben estar en (0, 1]."""
        for entrada in self.ei.espectro_entropia():
            self.assertGreater(entrada["psi_relativa"], 0.0)
            self.assertLessEqual(entrada["psi_relativa"], 1.0 + 1e-12)

    def test_espectro_ceros_invalidos(self):
        """Debe lanzar ValueError si algún cero es no positivo."""
        with self.assertRaises(ValueError):
            self.ei.espectro_entropia([14.13, -1.0])

    def test_espectro_personalizado(self):
        """Debe aceptar una lista de ceros personalizada."""
        esp = self.ei.espectro_entropia([GAMMA_1, CEROS_RIEMANN[1]])
        self.assertEqual(len(esp), 2)


class PruebasModoCoherencia(unittest.TestCase):

    """Verifica la clasificación del modo de coherencia."""

    def test_modo_creacion(self):
        """Ψ ≥ 0.888 → CREACIÓN."""
        ei = EntropiaInformativa(psi=0.9)
        self.assertEqual(ei.modo_coherencia(), "CREACIÓN")

    def test_modo_creacion_limite_exacto(self):
        """Ψ = 0.888 → CREACIÓN (umbral incluido)."""
        ei = EntropiaInformativa(psi=PSI_OPTIMO)
        self.assertEqual(ei.modo_coherencia(), "CREACIÓN")

    def test_modo_transicion(self):
        """0.666 ≤ Ψ < 0.888 → TRANSICIÓN."""
        ei = EntropiaInformativa(psi=0.75)
        self.assertEqual(ei.modo_coherencia(), "TRANSICIÓN")

    def test_modo_transicion_limite_inferior(self):
        """Ψ = 0.666 → TRANSICIÓN."""
        ei = EntropiaInformativa(psi=PSI_CRITICO)
        self.assertEqual(ei.modo_coherencia(), "TRANSICIÓN")

    def test_modo_purificacion(self):
        """Ψ < 0.666 → PURIFICACIÓN."""
        ei = EntropiaInformativa(psi=0.5)
        self.assertEqual(ei.modo_coherencia(), "PURIFICACIÓN")


class PruebasRatioAureo(unittest.TestCase):

    """Verifica la proporción áurea en el espectro entrópico."""

    def test_ratio_aureo_igual_phi_por_psi(self):
        """η = S(f₀·φ) / S(f₀) = PHI (Ψ se cancela en la división)."""
        psi = 0.9
        ei = EntropiaInformativa(psi=psi)
        self.assertAlmostEqual(ei.ratio_aureo_entropia(), PHI, places=8)

    def test_ratio_aureo_coherencia_perfecta(self):
        """Con Ψ = 1, el ratio debe ser exactamente φ."""
        ei = EntropiaInformativa(psi=1.0)
        self.assertAlmostEqual(ei.ratio_aureo_entropia(), PHI, places=8)

    def test_ratio_aureo_mayor_que_uno(self):
        """El ratio siempre debe ser mayor que 1 (φ > 1)."""
        ei = EntropiaInformativa(psi=0.8)
        self.assertGreater(ei.ratio_aureo_entropia(), 1.0)


class PruebasResumen(unittest.TestCase):

    """Verifica el resumen del sistema."""

    def setUp(self):
        self.ei = EntropiaInformativa()

    def test_resumen_claves_presentes(self):
        """El resumen debe contener todas las claves esperadas."""
        r = self.ei.resumen()
        for clave in ("f0_hz", "nc", "psi", "modo", "K_psi",
                      "densidad_entropia_base", "delta_S_gamma1", "ratio_aureo"):
            self.assertIn(clave, r)

    def test_resumen_delta_S_gamma1_cero(self):
        """El salto entrópico en γ₁ siempre debe ser 0."""
        self.assertAlmostEqual(self.ei.resumen()["delta_S_gamma1"], 0.0, places=8)

    def test_resumen_consistencia_k_psi(self):
        """K_Ψ en el resumen debe coincidir con k_psi()."""
        r = self.ei.resumen()
        self.assertAlmostEqual(r["K_psi"], self.ei.k_psi(), places=5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
