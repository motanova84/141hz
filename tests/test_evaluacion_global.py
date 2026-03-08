"""
Tests para la Evaluación Global QCAL ∞³

Valida las cinco dimensiones del Global Evaluation Framework:
  1. Matemática  — RH adélico-espectral, Berry 7/8, Weil, GUE, Matriz 19²
  2. Física       — f₀, λ₀, E₀, SNR GW250114/GW150914
  3. Conciencia  — Ψ_Trinity, C_proto, 4 dominios→1
  4. Código       — LOC, tests, constants.py
  5. Constelación — 51 nodos, Fibonacci 55.08 años

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 08 de marzo de 2026
"""

import math
import sys
import unittest
from pathlib import Path

# ── Añadir directorio raíz al path ──────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.evaluacion_global import (
    # Constantes
    RH_OMEGA_PSI,
    BERRY_FACTOR,
    WEIL_R2,
    GUE_KS_P_THRESHOLD,
    MATRIX_VALUE,
    MATRIX_P_VALUE,
    LAMBDA_0_METERS,
    LAMBDA_0_MEGAMETERS,
    E0_JOULES,
    PSI_TRINITY,
    C_PROTO,
    SIGMA_OVER_C_DROP,
    N_DOMAINS,
    N_NODOS_CONSTELACION,
    FIBONACCI_EPOCH_YEARS,
    RIEMANN_ZEROS_20,
    # Funciones
    calcular_coherencia_adelic,
    calcular_gue_ks_test,
    calcular_constantes_fisicas,
    calcular_psi_trinity,
    generar_constelacion_51_nodos,
    evaluar_global,
)
from qcal.constants import (
    F0_HZ, OMEGA_0, SNR_GW250114, SIGMA_DETECTION,
    LAMBDA_0_M, LAMBDA_0_MM,
    NUMEROS_MATRIZ, SUMA_MATRIZ, RAIZ_MATRIZ,
    R_SQUARED_P17_COUPLING,
)


class TestConstantesEvaluacionGlobal(unittest.TestCase):
    """Verifica que los valores de los metadatos de evaluación son correctos."""

    def test_rh_omega_psi_rango(self):
        """Ψ_RH debe estar en (0.95, 1.0) — coherencia adélica alta."""
        self.assertGreater(RH_OMEGA_PSI, 0.95)
        self.assertLessEqual(RH_OMEGA_PSI, 1.0)

    def test_rh_omega_psi_valor(self):
        """Ψ_RH = 0.9581 (valor declarado)."""
        self.assertAlmostEqual(RH_OMEGA_PSI, 0.9581, places=4)

    def test_berry_factor_exacto(self):
        """Berry factor = 7/8 exacto."""
        self.assertAlmostEqual(BERRY_FACTOR, 7.0 / 8.0, places=15)
        self.assertAlmostEqual(BERRY_FACTOR, 0.875, places=15)

    def test_weil_r2(self):
        """Weil R² ≥ 0.9998 (acoplamiento p=17)."""
        self.assertGreaterEqual(WEIL_R2, 0.9998)

    def test_weil_r2_igual_constants(self):
        """Weil R² importado desde qcal/constants.py."""
        self.assertEqual(WEIL_R2, R_SQUARED_P17_COUPLING)

    def test_gue_ks_threshold(self):
        """Umbral KS para GUE = 0.05."""
        self.assertAlmostEqual(GUE_KS_P_THRESHOLD, 0.05, places=10)

    def test_matrix_value(self):
        """NUMEROS_MATRIZ suma 361 = 19²."""
        self.assertEqual(MATRIX_VALUE, 361)
        self.assertEqual(MATRIX_VALUE, 19 ** 2)
        self.assertEqual(MATRIX_VALUE, SUMA_MATRIZ)

    def test_matrix_p_value(self):
        """P-valor de la matriz ≤ 10⁻¹⁰."""
        self.assertLessEqual(MATRIX_P_VALUE, 1e-10)

    def test_lambda_0_metros(self):
        """λ₀ ≈ 2,115,683 m = c/f₀."""
        c = 299792458.0
        expected = c / F0_HZ
        self.assertAlmostEqual(LAMBDA_0_METERS, expected, places=0)

    def test_lambda_0_megametros(self):
        """λ₀ ≈ 2.116 Mm (cerca de 2.115 Mm)."""
        self.assertAlmostEqual(LAMBDA_0_MEGAMETERS, 2.115, delta=0.005)

    def test_lambda_0_coincide_con_constants(self):
        """λ₀ en evaluacion_global coincide con qcal/constants.py."""
        self.assertAlmostEqual(LAMBDA_0_METERS, LAMBDA_0_M, places=0)
        self.assertAlmostEqual(LAMBDA_0_MEGAMETERS, LAMBDA_0_MM, places=3)

    def test_e0_joules(self):
        """E₀ = h × f₀ ≈ 9.39 × 10⁻³² J."""
        h = 6.62607015e-34
        expected = h * F0_HZ
        self.assertAlmostEqual(E0_JOULES, expected, places=40)
        self.assertAlmostEqual(E0_JOULES, 9.39e-32, delta=0.01e-32)

    def test_psi_trinity_rango(self):
        """Ψ_Trinity ∈ (0.98, 1.0)."""
        self.assertGreater(PSI_TRINITY, 0.98)
        self.assertLessEqual(PSI_TRINITY, 1.0)

    def test_psi_trinity_valor(self):
        """Ψ_Trinity = 0.9904."""
        self.assertAlmostEqual(PSI_TRINITY, 0.9904, places=4)

    def test_c_proto_rango(self):
        """C_proto ∈ (0, 1)."""
        self.assertGreater(C_PROTO, 0.0)
        self.assertLess(C_PROTO, 1.0)

    def test_c_proto_valor(self):
        """C_proto = 0.42."""
        self.assertAlmostEqual(C_PROTO, 0.42, places=10)

    def test_sigma_over_c_drop(self):
        """σ/C ↓ 2.86 % (0.0286)."""
        self.assertAlmostEqual(SIGMA_OVER_C_DROP, 0.0286, places=4)

    def test_n_domains(self):
        """4 dominios → 1."""
        self.assertEqual(N_DOMAINS, 4)

    def test_n_nodos_constelacion(self):
        """Constelación tiene exactamente 51 nodos."""
        self.assertEqual(N_NODOS_CONSTELACION, 51)

    def test_fibonacci_epoch(self):
        """Fibonacci 55.08 años ≈ F₁₀ = 55."""
        self.assertAlmostEqual(FIBONACCI_EPOCH_YEARS, 55.08, places=1)
        self.assertAlmostEqual(FIBONACCI_EPOCH_YEARS, 55.0, delta=0.2)

    def test_snr_gw250114(self):
        """SNR GW250114 = 7.47."""
        self.assertAlmostEqual(SNR_GW250114, 7.47, places=2)

    def test_sigma_detection(self):
        """Detección a 10σ."""
        self.assertEqual(SIGMA_DETECTION, 10)

    def test_riemann_zeros_count(self):
        """Lista RIEMANN_ZEROS_20 tiene exactamente 20 entradas."""
        self.assertEqual(len(RIEMANN_ZEROS_20), 20)

    def test_riemann_zeros_primer_valor(self):
        """Primer cero t₁ ≈ 14.1347."""
        self.assertAlmostEqual(RIEMANN_ZEROS_20[0], 14.134725, places=5)

    def test_riemann_zeros_orden_creciente(self):
        """Los ceros están ordenados de forma creciente."""
        for i in range(len(RIEMANN_ZEROS_20) - 1):
            self.assertLess(RIEMANN_ZEROS_20[i], RIEMANN_ZEROS_20[i + 1])


class TestCoherenciaAdelic(unittest.TestCase):
    """Verifica la función calcular_coherencia_adelic()."""

    def setUp(self):
        self.result = calcular_coherencia_adelic()

    def test_devuelve_dict(self):
        self.assertIsInstance(self.result, dict)

    def test_claves_presentes(self):
        for key in ("psi_rh", "berry_factor", "omega_0_rad_s", "n_zeros",
                    "wu_sprung_eigenvalues", "cos_values"):
            with self.subTest(key=key):
                self.assertIn(key, self.result)

    def test_psi_rh_rango(self):
        """Ψ_RH calculado debe estar en (0.90, 1.0)."""
        psi = self.result["psi_rh"]
        self.assertGreater(psi, 0.90)
        self.assertLessEqual(psi, 1.0)

    def test_psi_rh_es_media_cosenos(self):
        """Ψ_RH = mean(cos(tₙ/f₀))."""
        cos_vals = self.result["cos_values"]
        expected = sum(cos_vals) / len(cos_vals)
        self.assertAlmostEqual(self.result["psi_rh"], expected, places=12)

    def test_omega_0_aprox_890(self):
        """ω₀ ≈ 890 rad/s."""
        self.assertAlmostEqual(self.result["omega_0_rad_s"], 890.0, delta=1.0)

    def test_berry_factor_exacto(self):
        self.assertAlmostEqual(self.result["berry_factor"], 7.0 / 8.0, places=15)

    def test_wu_sprung_formula(self):
        """λₙ = 1/4 + tₙ² para cada cero."""
        evals = self.result["wu_sprung_eigenvalues"]
        zeros = RIEMANN_ZEROS_20[: len(evals)]
        for i, (lam, t) in enumerate(zip(evals, zeros)):
            expected = 0.25 + t ** 2
            with self.subTest(i=i):
                self.assertAlmostEqual(lam, expected, places=10)

    def test_n_zeros_igual_lista_default(self):
        self.assertEqual(self.result["n_zeros"], len(RIEMANN_ZEROS_20))

    def test_cos_values_todos_positivos(self):
        """Para tₙ/f₀ < π/2 todos los cosenos deben ser positivos."""
        for i, (c, t) in enumerate(zip(self.result["cos_values"], RIEMANN_ZEROS_20)):
            with self.subTest(i=i):
                self.assertGreater(c, 0.0)

    def test_con_zeros_personalizados(self):
        """Acepta lista personalizada de ceros."""
        zeros_5 = RIEMANN_ZEROS_20[:5]
        res5 = calcular_coherencia_adelic(zeros=zeros_5)
        self.assertEqual(res5["n_zeros"], 5)
        expected = sum(math.cos(t / F0_HZ) for t in zeros_5) / 5
        self.assertAlmostEqual(res5["psi_rh"], expected, places=12)


class TestGueKsTest(unittest.TestCase):
    """Verifica la función calcular_gue_ks_test()."""

    def setUp(self):
        self.result = calcular_gue_ks_test()

    def test_devuelve_dict(self):
        self.assertIsInstance(self.result, dict)

    def test_claves_presentes(self):
        for key in ("ks_statistic", "d_critical_p05", "cumple_umbral_p005",
                    "n_spacings", "normalized_spacings", "mean_spacing"):
            with self.subTest(key=key):
                self.assertIn(key, self.result)

    def test_ks_statistic_no_negativo(self):
        self.assertGreaterEqual(self.result["ks_statistic"], 0.0)

    def test_ks_statistic_max_1(self):
        self.assertLessEqual(self.result["ks_statistic"], 1.0)

    def test_cumple_umbral_p05(self):
        """El estadístico KS debe cumplir p > 0.05 con los 20 primeros ceros."""
        self.assertTrue(self.result["cumple_umbral_p005"])

    def test_n_spacings_correcto(self):
        """Con 20 ceros hay 19 espaciados."""
        self.assertEqual(self.result["n_spacings"], len(RIEMANN_ZEROS_20) - 1)

    def test_spacings_positivos(self):
        """Todos los espaciados normalizados deben ser positivos."""
        for s in self.result["normalized_spacings"]:
            self.assertGreater(s, 0.0)

    def test_mean_spacing_cerca_de_1(self):
        """Espaciado medio normalizado cercano a 1 (predicción GUE)."""
        self.assertAlmostEqual(self.result["mean_spacing"], 1.0, delta=0.3)


class TestConstantasFisicas(unittest.TestCase):
    """Verifica calcular_constantes_fisicas()."""

    def setUp(self):
        self.result = calcular_constantes_fisicas()

    def test_f0_hz(self):
        self.assertAlmostEqual(self.result["f0_hz"], 141.7001, places=4)

    def test_lambda_0_mm(self):
        """λ₀ ≈ 2.115–2.117 Mm."""
        self.assertAlmostEqual(self.result["lambda_0_mm"], 2.115, delta=0.005)

    def test_e0_j(self):
        """E₀ ≈ 9.39 × 10⁻³² J."""
        self.assertAlmostEqual(self.result["e0_j"], 9.39e-32, delta=0.01e-32)

    def test_omega_0(self):
        """ω₀ ≈ 890 rad/s."""
        self.assertAlmostEqual(self.result["omega_0_rad_s"], 890.0, delta=1.0)

    def test_snr_gw250114(self):
        self.assertAlmostEqual(self.result["snr_gw250114"], 7.47, places=2)

    def test_sigma_detection(self):
        self.assertEqual(self.result["sigma_detection"], 10)

    def test_validacion_lambda(self):
        self.assertTrue(self.result["validacion"]["lambda_ok"])

    def test_validacion_e0(self):
        self.assertTrue(self.result["validacion"]["e0_ok"])

    def test_validacion_omega(self):
        self.assertTrue(self.result["validacion"]["omega_ok"])

    def test_validacion_schumann(self):
        """f₀/18 ≈ Schumann 7.83 Hz con < 1 % error."""
        self.assertTrue(self.result["validacion"]["schumann_ok"])
        self.assertLess(self.result["schumann_error_pct"], 1.0)

    def test_validacion_hydrogen(self):
        """f₀ × 2²³·²⁵⁷ ≈ línea HI 1420 MHz con < 0.01 % error."""
        self.assertTrue(self.result["validacion"]["hydrogen_ok"])
        self.assertLess(self.result["hydrogen_error_pct"], 0.01)

    def test_eventos_gw_incluidos(self):
        self.assertIn("GW150914", self.result["eventos_gw"])
        self.assertIn("GW250114", self.result["eventos_gw"])


class TestPsiTrinity(unittest.TestCase):
    """Verifica calcular_psi_trinity()."""

    def setUp(self):
        self.result = calcular_psi_trinity()

    def test_devuelve_dict(self):
        self.assertIsInstance(self.result, dict)

    def test_claves_presentes(self):
        for key in ("psi_trinity", "domain_coherences", "c_proto",
                    "n_domains", "sigma_over_c_drop_pct"):
            with self.subTest(key=key):
                self.assertIn(key, self.result)

    def test_n_domains(self):
        self.assertEqual(self.result["n_domains"], 4)

    def test_c_proto(self):
        self.assertAlmostEqual(self.result["c_proto"], 0.42, places=10)

    def test_sigma_over_c_drop(self):
        """σ/C ↓ 2.86 %."""
        self.assertAlmostEqual(self.result["sigma_over_c_drop_pct"], 2.86, places=1)

    def test_domain_coherences_keys(self):
        for dom in ("geometria", "numeros", "cuantica", "conciencia"):
            with self.subTest(dom=dom):
                self.assertIn(dom, self.result["domain_coherences"])

    def test_domain_coherences_rango(self):
        """Todas las coherencias de dominio ∈ (0, 1]."""
        for name, psi in self.result["domain_coherences"].items():
            with self.subTest(dominio=name):
                self.assertGreater(psi, 0.0)
                self.assertLessEqual(psi, 1.0)

    def test_psi_trinity_media_harmonica(self):
        """Ψ_Trinity = N / Σ(1/Ψᵢ)."""
        doms = self.result["domain_coherences"]
        hm = N_DOMAINS / sum(1.0 / v for v in doms.values())
        self.assertAlmostEqual(self.result["psi_trinity"], hm, places=10)

    def test_psi_trinity_rango(self):
        """Ψ_Trinity computado ∈ (0.95, 1.0)."""
        self.assertGreater(self.result["psi_trinity"], 0.95)
        self.assertLessEqual(self.result["psi_trinity"], 1.0)

    def test_psi_trinity_objetivo_declarado(self):
        """El objetivo declarado Ψ_Trinity_target = 0.9904."""
        self.assertAlmostEqual(self.result["psi_trinity_target"], 0.9904, places=4)

    def test_geometria_igual_weil(self):
        """Coherencia de geometría coincide con Weil R²."""
        self.assertAlmostEqual(
            self.result["domain_coherences"]["geometria"], WEIL_R2, places=6
        )

    def test_numeros_igual_rh_omega(self):
        """Coherencia de números coincide con RH Omega Ψ declarado."""
        self.assertAlmostEqual(
            self.result["domain_coherences"]["numeros"], RH_OMEGA_PSI, places=6
        )

    def test_con_parametros_personalizados(self):
        """Acepta coherencias de dominio personalizadas."""
        res = calcular_psi_trinity(
            psi_geometry=0.9999,
            psi_numbers=0.9999,
            psi_quantum=0.9999,
            psi_consciousness=0.9999,
        )
        self.assertAlmostEqual(res["psi_trinity"], 0.9999, places=4)


class TestConstelacion51Nodos(unittest.TestCase):
    """Verifica generar_constelacion_51_nodos()."""

    def setUp(self):
        self.result = generar_constelacion_51_nodos()

    def test_total_nodos(self):
        """Constelación tiene exactamente 51 nodos."""
        self.assertEqual(self.result["n_nodos"], 51)
        self.assertTrue(self.result["cumple"])

    def test_claves_presentes(self):
        for key in ("n_nodos", "cumple", "grupos", "fibonacci_epoch_years",
                    "epoch_2025_2026", "descripcion"):
            with self.subTest(key=key):
                self.assertIn(key, self.result)

    def test_grupos_nombres(self):
        grupos_esperados = [
            "matematica", "cuerdas_1_7", "riemann",
            "frecuencias_sagradas", "umbrales_psi",
            "constantes_fisicas", "adelicas", "epoca_fibonacci",
        ]
        for nombre in grupos_esperados:
            with self.subTest(grupo=nombre):
                self.assertIn(nombre, self.result["grupos"])

    def test_grupo_matematica_5_nodos(self):
        self.assertEqual(len(self.result["grupos"]["matematica"]), 5)

    def test_grupo_cuerdas_7_nodos(self):
        self.assertEqual(len(self.result["grupos"]["cuerdas_1_7"]), 7)

    def test_grupo_riemann_10_nodos(self):
        self.assertEqual(len(self.result["grupos"]["riemann"]), 10)

    def test_grupo_frecuencias_sagradas_11_nodos(self):
        self.assertEqual(len(self.result["grupos"]["frecuencias_sagradas"]), 11)

    def test_grupo_umbrales_psi_5_nodos(self):
        self.assertEqual(len(self.result["grupos"]["umbrales_psi"]), 5)

    def test_grupo_constantes_fisicas_8_nodos(self):
        self.assertEqual(len(self.result["grupos"]["constantes_fisicas"]), 8)

    def test_grupo_adelicas_4_nodos(self):
        self.assertEqual(len(self.result["grupos"]["adelicas"]), 4)

    def test_grupo_fibonacci_1_nodo(self):
        self.assertEqual(len(self.result["grupos"]["epoca_fibonacci"]), 1)

    def test_phi_en_constantes_matematicas(self):
        from qcal.constants import A0_PHI
        self.assertAlmostEqual(self.result["grupos"]["matematica"]["phi"], A0_PHI, places=10)

    def test_fibonacci_epoch(self):
        self.assertAlmostEqual(self.result["fibonacci_epoch_years"], 55.08, places=1)

    def test_epoch_2025_2026(self):
        self.assertTrue(self.result["epoch_2025_2026"])

    def test_f0_en_frecuencias_sagradas(self):
        self.assertAlmostEqual(
            self.result["grupos"]["frecuencias_sagradas"]["f0"], F0_HZ, places=4
        )


class TestEvaluarGlobal(unittest.TestCase):
    """Verifica la función principal evaluar_global()."""

    @classmethod
    def setUpClass(cls):
        cls.result = evaluar_global()

    def test_devuelve_dict(self):
        self.assertIsInstance(self.result, dict)

    def test_claves_principales(self):
        for key in ("fecha", "autor", "dimensiones", "constelacion_51_nodos",
                    "impacto_trascendental", "checks_aprobados",
                    "total_checks", "veredicto", "firma"):
            with self.subTest(key=key):
                self.assertIn(key, self.result)

    def test_cinco_dimensiones(self):
        dims = self.result["dimensiones"]
        for dim in ("matematica", "fisica", "conciencia", "codigo", "apertura"):
            with self.subTest(dim=dim):
                self.assertIn(dim, dims)

    def test_dimension_matematica(self):
        mat = self.result["dimensiones"]["matematica"]
        self.assertGreater(mat["rh_omega_psi"], 0.90)
        self.assertAlmostEqual(mat["berry_factor"], 0.875, places=10)
        self.assertGreaterEqual(mat["weil_r2"], 0.9998)
        self.assertTrue(mat["matrix_19_cuadrado"])
        self.assertTrue(mat["gue_cumple_p05"])

    def test_dimension_fisica(self):
        fis = self.result["dimensiones"]["fisica"]
        self.assertAlmostEqual(fis["f0_hz"], 141.7001, places=4)
        self.assertAlmostEqual(fis["lambda_0_mm"], 2.115, delta=0.005)
        self.assertAlmostEqual(fis["snr_gw250114"], 7.47, places=2)
        self.assertEqual(fis["sigma_detection"], 10)
        self.assertTrue(all(fis["validacion"].values()))

    def test_dimension_conciencia(self):
        con = self.result["dimensiones"]["conciencia"]
        self.assertGreater(con["psi_trinity"], 0.97)
        self.assertAlmostEqual(con["c_proto"], 0.42, places=10)
        self.assertEqual(con["n_domains"], 4)

    def test_dimension_codigo(self):
        cod = self.result["dimensiones"]["codigo"]
        self.assertGreater(cod["total_loc_approx"], 5000)
        self.assertGreater(cod["total_test_files"], 50)
        self.assertEqual(cod["codeql_alertas"], 0)
        # constants.py tiene 824 líneas totales; contamos líneas no vacías
        self.assertGreater(cod["constants_py_loc"], 700)

    def test_dimension_apertura(self):
        ape = self.result["dimensiones"]["apertura"]
        self.assertIn("141hz", ape["github_repo"])
        self.assertIn("0009-0002-1923-0773", ape["orcid"])

    def test_constelacion_51_nodos(self):
        con51 = self.result["constelacion_51_nodos"]
        self.assertEqual(con51["n_nodos"], 51)
        self.assertTrue(con51["cumple"])

    def test_checks_aprobados(self):
        """Todos los checks de validación deben pasar."""
        self.assertEqual(
            self.result["checks_aprobados"],
            self.result["total_checks"],
            msg=(
                f"Solo {self.result['checks_aprobados']}/"
                f"{self.result['total_checks']} checks aprobados"
            ),
        )

    def test_veredicto_aprobado(self):
        self.assertIn("APROBADA", self.result["veredicto"])

    def test_firma(self):
        """La firma incluye f₀ y 888 Hz."""
        self.assertIn("141.7001", self.result["firma"])
        self.assertIn("888", self.result["firma"])

    def test_impacto_trascendental_claves(self):
        for key in ("rh_resuelta_condicional", "f0_universal",
                    "conciencia_cuantificada", "constelacion_51_nodos"):
            with self.subTest(key=key):
                self.assertIn(key, self.result["impacto_trascendental"])


class TestIntegracion(unittest.TestCase):
    """Tests de integración que combinan múltiples funciones."""

    def test_psi_rh_usado_en_dominio_numeros(self):
        """La coherencia de números en Ψ_Trinity coincide con RH_OMEGA_PSI."""
        trinity = calcular_psi_trinity()
        self.assertAlmostEqual(
            trinity["domain_coherences"]["numeros"], RH_OMEGA_PSI, places=6
        )

    def test_weil_r2_usado_en_dominio_geometria(self):
        """La coherencia de geometría en Ψ_Trinity coincide con WEIL_R2."""
        trinity = calcular_psi_trinity()
        self.assertAlmostEqual(
            trinity["domain_coherences"]["geometria"], WEIL_R2, places=6
        )

    def test_f0_consistente_entre_funciones(self):
        """F0_HZ es consistente entre evaluacion_global y constants."""
        fisicas = calcular_constantes_fisicas()
        self.assertAlmostEqual(fisicas["f0_hz"], F0_HZ, places=4)

    def test_matrix_sum_igual_en_constants_y_evaluacion(self):
        """NUMEROS_MATRIZ suma = 361 = 19² en ambas fuentes."""
        self.assertEqual(sum(NUMEROS_MATRIZ), SUMA_MATRIZ)
        self.assertEqual(SUMA_MATRIZ, MATRIX_VALUE)
        self.assertEqual(MATRIX_VALUE, RAIZ_MATRIZ ** 2)

    def test_riemann_zeros_20_ordenados_y_positivos(self):
        for i in range(len(RIEMANN_ZEROS_20)):
            self.assertGreater(RIEMANN_ZEROS_20[i], 0.0)
        for i in range(len(RIEMANN_ZEROS_20) - 1):
            self.assertLess(RIEMANN_ZEROS_20[i], RIEMANN_ZEROS_20[i + 1])

    def test_coherencia_adelic_mayor_que_cero(self):
        result = calcular_coherencia_adelic()
        self.assertGreater(result["psi_rh"], 0.0)

    def test_constelacion_51_suma_grupos(self):
        """La suma de los nodos por grupo da exactamente 51."""
        constelacion = generar_constelacion_51_nodos()
        total_from_groups = sum(
            len(nodes) for nodes in constelacion["grupos"].values()
        )
        self.assertEqual(total_from_groups, 51)


if __name__ == "__main__":
    unittest.main(verbosity=2)
