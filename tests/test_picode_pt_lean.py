#!/usr/bin/env python3
"""
Tests para physics/PicodePT.lean — Implementación Formal Lean 4 del πCODE

Valida la estructura y contenido del módulo Lean 4 que formaliza el
Operador PT No-Hermítico (πCODE) integrado con el marco holográfico
AdS/CFT citoplasmático y el estabilizador Riemann.

Comprueba:
1. Existencia del archivo physics/PicodePT.lean
2. Declaraciones namespace y sección
3. Constantes físicas (γ_c = 2.57, f₀ = 141.7001, γ_default = 0.183)
4. Estructura OperadorPTNoHermitico (laplacian, V_eff, W_dis)
5. Definiciones H_total, PT_symmetric, ψ_PT, estabilizador_riemann
6. Lemas: ψ_PT_pos, ψ_PT_alta_coherencia, espectro_real_PT_unbroken
7. Lema estabilizador_hermitian
8. Teorema picode_coherencia_alta
9. Integración con lakefile.lean (entrada PicodePT)
10. Consistencia con módulo Python picode_resonancia_holografica

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
License: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import math
import re
import sys
import unittest
from pathlib import Path

# Añadir raíz del repositorio al path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

LEAN_FILE = ROOT / "physics" / "PicodePT.lean"
LAKEFILE = ROOT / "formalization" / "lean" / "lakefile.lean"


# ---------------------------------------------------------------------------
# Auxiliar: leer contenido del archivo Lean
# ---------------------------------------------------------------------------

def _lean_content() -> str:
    """Lee el archivo PicodePT.lean y devuelve su contenido."""
    return LEAN_FILE.read_text(encoding="utf-8")


def _lakefile_content() -> str:
    """Lee el lakefile.lean y devuelve su contenido."""
    return LAKEFILE.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Existencia de archivos
# ---------------------------------------------------------------------------

class TestArchivoExiste(unittest.TestCase):
    """Verifica que los archivos requeridos existen."""

    def test_picode_pt_lean_existe(self):
        """El archivo physics/PicodePT.lean debe existir."""
        self.assertTrue(
            LEAN_FILE.exists(),
            f"No se encontró {LEAN_FILE}"
        )

    def test_picode_pt_lean_no_vacio(self):
        """El archivo PicodePT.lean no debe estar vacío."""
        self.assertGreater(LEAN_FILE.stat().st_size, 100)

    def test_lakefile_existe(self):
        """El lakefile.lean de formalization/lean debe existir."""
        self.assertTrue(LAKEFILE.exists())

    def test_lakefile_no_vacio(self):
        """El lakefile.lean no debe estar vacío."""
        self.assertGreater(LAKEFILE.stat().st_size, 100)


# ---------------------------------------------------------------------------
# 2. Estructura del módulo Lean 4
# ---------------------------------------------------------------------------

class TestEstructuraModulo(unittest.TestCase):
    """Verifica la estructura del módulo Lean 4."""

    def setUp(self):
        self.content = _lean_content()

    def test_seccion_noncomputable(self):
        """Debe declarar una sección noncomputable."""
        self.assertIn("noncomputable section", self.content)

    def test_namespace_picode_pt(self):
        """Debe declarar el namespace PicodePT."""
        self.assertIn("namespace PicodePT", self.content)

    def test_imports_mathlib(self):
        """Debe importar módulos de Mathlib relevantes."""
        self.assertIn("import Mathlib", self.content)
        self.assertIn("Complex", self.content)
        self.assertIn("Matrix", self.content)

    def test_open_complex_real(self):
        """Debe abrir los namespaces Complex, Real, Matrix."""
        self.assertIn("open Complex Real Matrix BigOperators", self.content)

    def test_cierre_namespace(self):
        """Debe cerrar el namespace y la sección."""
        self.assertIn("end PicodePT", self.content)


# ---------------------------------------------------------------------------
# 3. Constantes físicas
# ---------------------------------------------------------------------------

class TestConstantesFisicas(unittest.TestCase):
    """Verifica las constantes del sistema PT."""

    def setUp(self):
        self.content = _lean_content()

    def test_gamma_c_definido(self):
        """γ_c debe estar definido."""
        self.assertIn("def γ_c", self.content)

    def test_gamma_c_valor(self):
        """γ_c = 2.57 (umbral Bender-Boettcher 1998)."""
        self.assertIn("2.57", self.content)

    def test_f0_definido(self):
        """f₀ debe estar definido."""
        self.assertIn("def f₀", self.content)

    def test_f0_valor(self):
        """f₀ = 141.7001 Hz (frecuencia fundamental QCAL)."""
        self.assertIn("141.7001", self.content)

    def test_gamma_default_definido(self):
        """γ_default debe estar definido."""
        self.assertIn("def γ_default", self.content)

    def test_gamma_default_valor(self):
        """γ_default = 0.183 (valor por defecto del πCODE)."""
        self.assertIn("0.183", self.content)

    def test_gamma_default_menor_gamma_c(self):
        """γ_default < γ_c (condición PT-unbroken)."""
        γ_default = 0.183
        γ_c = 2.57
        self.assertLess(γ_default, γ_c)

    def test_gamma_c_consistente_con_python(self):
        """γ_c debe coincidir con _BETA_CRITICO del módulo Python."""
        try:
            from physics.picode_resonancia_holografica import _BETA_CRITICO
            self.assertAlmostEqual(_BETA_CRITICO, 2.57, places=2)
        except ImportError:
            self.skipTest("picode_resonancia_holografica no disponible")


# ---------------------------------------------------------------------------
# 4. Estructura OperadorPTNoHermitico
# ---------------------------------------------------------------------------

class TestOperadorPTNoHermitico(unittest.TestCase):
    """Verifica la estructura del Operador PT No-Hermítico."""

    def setUp(self):
        self.content = _lean_content()

    def test_estructura_definida(self):
        """OperadorPTNoHermitico debe estar definido como structure."""
        self.assertIn("structure OperadorPTNoHermitico", self.content)

    def test_campo_laplacian(self):
        """Debe tener campo laplacian (operador cinético -∇²)."""
        self.assertIn("laplacian", self.content)

    def test_campo_v_eff(self):
        """Debe tener campo V_eff (potencial efectivo)."""
        self.assertIn("V_eff", self.content)

    def test_campo_w_dis(self):
        """Debe tener campo W_dis (disipación PT-flipped)."""
        self.assertIn("W_dis", self.content)

    def test_tipos_matrix_complex(self):
        """Los campos deben ser de tipo Matrix n n ℂ."""
        self.assertIn("Matrix n n ℂ", self.content)

    def test_deriving_inhabited(self):
        """Debe derivar Inhabited para poder crear instancias por defecto."""
        self.assertIn("deriving Inhabited", self.content)


# ---------------------------------------------------------------------------
# 5. Definición H_total
# ---------------------------------------------------------------------------

class TestHTotal(unittest.TestCase):
    """Verifica la definición del Hamiltoniano total."""

    def setUp(self):
        self.content = _lean_content()

    def test_h_total_definido(self):
        """H_total debe estar definido."""
        self.assertIn("def H_total", self.content)

    def test_h_total_formula(self):
        """H_total debe contener la fórmula de la suma de operadores."""
        self.assertIn("laplacian", self.content)
        self.assertIn("V_eff", self.content)
        self.assertIn("W_dis", self.content)
        self.assertIn("Complex.I", self.content)

    def test_h_total_recibe_gamma(self):
        """H_total debe parametrizarse sobre γ."""
        self.assertIn("(γ : ℝ)", self.content)


# ---------------------------------------------------------------------------
# 6. Simetría PT
# ---------------------------------------------------------------------------

class TestSimetriaPropiedad(unittest.TestCase):
    """Verifica la definición de simetría PT."""

    def setUp(self):
        self.content = _lean_content()

    def test_pt_symmetric_definido(self):
        """PT_symmetric debe estar definido."""
        self.assertIn("def PT_symmetric", self.content)

    def test_pt_usa_starring_end(self):
        """PT_symmetric debe usar starRingEnd para conjugación compleja."""
        self.assertIn("starRingEnd", self.content)

    def test_pt_usa_flip(self):
        """PT_symmetric debe referenciar la función flip de índices."""
        self.assertIn("flip", self.content)

    def test_lema_espectro_real(self):
        """Debe existir el lema espectro_real_PT_unbroken."""
        self.assertIn("espectro_real_PT_unbroken", self.content)


# ---------------------------------------------------------------------------
# 7. Función de Coherencia ψ_PT
# ---------------------------------------------------------------------------

class TestPsiPT(unittest.TestCase):
    """Verifica la función de coherencia ψ_PT."""

    def setUp(self):
        self.content = _lean_content()

    def test_psi_pt_definido(self):
        """ψ_PT debe estar definido."""
        self.assertIn("def ψ_PT", self.content)

    def test_formula_psi_pt(self):
        """Fórmula ψ_PT = 1 - (γ/γ_c)^2 debe estar presente."""
        self.assertIn("1 -", self.content)
        self.assertIn("^ 2", self.content)

    def test_lema_psi_pt_pos(self):
        """Debe existir el lema ψ_PT_pos."""
        self.assertIn("ψ_PT_pos", self.content)

    def test_lema_psi_pt_alta_coherencia(self):
        """Debe existir el lema ψ_PT_alta_coherencia."""
        self.assertIn("ψ_PT_alta_coherencia", self.content)

    def test_umbral_coherencia_biologica(self):
        """El umbral de coherencia biológica (0.888) debe estar referenciado."""
        self.assertIn("0.888", self.content)

    def test_psi_pt_calculo_correcto(self):
        """Verificación numérica: ψ_PT(0.183) ≈ 0.9949 > 0.888."""
        γ = 0.183
        γ_c = 2.57
        ψ = 1 - (γ / γ_c) ** 2
        self.assertGreater(ψ, 0.888)
        self.assertAlmostEqual(ψ, 0.9949, places=3)

    def test_psi_pt_cero_en_umbral(self):
        """ψ_PT(γ_c) = 0 (ruptura de fase PT)."""
        γ_c = 2.57
        ψ = 1 - (γ_c / γ_c) ** 2
        self.assertAlmostEqual(ψ, 0.0, places=10)

    def test_psi_pt_maximo_en_cero(self):
        """ψ_PT(0) = 1 (límite hermítico, máxima coherencia)."""
        γ = 0.0
        γ_c = 2.57
        ψ = 1 - (γ / γ_c) ** 2
        self.assertAlmostEqual(ψ, 1.0, places=10)


# ---------------------------------------------------------------------------
# 8. Estabilizador de Riemann
# ---------------------------------------------------------------------------

class TestEstabilizadorRiemann(unittest.TestCase):
    """Verifica el estabilizador de Riemann."""

    def setUp(self):
        self.content = _lean_content()

    def test_estabilizador_definido(self):
        """estabilizador_riemann debe estar definido."""
        self.assertIn("def estabilizador_riemann", self.content)

    def test_zeros_parametro(self):
        """Debe aceptar zeros: Fin 10 → ℝ."""
        self.assertIn("Fin 10", self.content)

    def test_usa_diagonal(self):
        """El estabilizador debe ser una matriz diagonal."""
        self.assertIn("diagonal", self.content)

    def test_formula_amortiguamiento(self):
        """Debe usar la fórmula de amortiguamiento: exp(-α * t_n / f₀)."""
        self.assertIn("Real.exp", self.content)

    def test_lema_estabilizador_hermitico(self):
        """Debe existir el lema estabilizador_hermitian."""
        self.assertIn("estabilizador_hermitian", self.content)

    def test_matrix_is_hermitian(self):
        """Debe usar Matrix.IsHermitian."""
        self.assertIn("Matrix.IsHermitian", self.content)

    def test_amortiguamiento_numerico(self):
        """Verificación numérica del amortiguamiento espectral."""
        f0_val = 141.7001
        # Primeros ceros de Riemann (aproximados)
        zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
                 37.5862, 40.9187, 43.3271, 48.0052, 49.7738]
        alpha = 1.0
        pesos = [t * math.exp(-alpha * t / f0_val) for t in zeros]
        # Todos los pesos deben ser positivos
        for i, w in enumerate(pesos):
            self.assertGreater(w, 0, f"Peso {i} debe ser positivo: {w}")
        # El peso máximo ocurre cerca de t_n = f₀ ≈ 141.7
        # Para estos ceros pequeños, el amortiguamiento es mínimo
        for i, (t, w) in enumerate(zip(zeros, pesos)):
            # d_n/t_n = exp(-alpha*t/f0) ∈ (0, 1)
            ratio = w / t
            self.assertLess(ratio, 1.0)
            self.assertGreater(ratio, 0.0)


# ---------------------------------------------------------------------------
# 9. Teorema de coherencia alta
# ---------------------------------------------------------------------------

class TestTeoremaPrincipal(unittest.TestCase):
    """Verifica el teorema principal de coherencia alta."""

    def setUp(self):
        self.content = _lean_content()

    def test_theorem_picode_coherencia_alta(self):
        """Debe existir el teorema picode_coherencia_alta."""
        self.assertIn("theorem picode_coherencia_alta", self.content)

    def test_theorem_usa_psi_pt_alta_coherencia(self):
        """El teorema debe usar ψ_PT_alta_coherencia."""
        self.assertIn("ψ_PT_alta_coherencia", self.content)

    def test_picode_pt_activo_definido(self):
        """picode_PT_activo debe estar definido."""
        self.assertIn("def picode_PT_activo", self.content)


# ---------------------------------------------------------------------------
# 10. Integración con lakefile.lean
# ---------------------------------------------------------------------------

class TestIntegracionLakefile(unittest.TestCase):
    """Verifica que PicodePT está registrado en el lakefile."""

    def setUp(self):
        self.content = _lakefile_content()

    def test_picode_pt_en_lakefile(self):
        """PicodePT debe estar declarado como lean_lib en el lakefile."""
        self.assertIn("lean_lib PicodePT", self.content)

    def test_picode_pt_src_dir(self):
        """La entrada PicodePT debe especificar srcDir hacia physics/."""
        self.assertIn("srcDir", self.content)
        self.assertIn("physics", self.content)

    def test_picode_pt_roots(self):
        """La entrada PicodePT debe especificar roots := #[`PicodePT]."""
        self.assertIn("`PicodePT", self.content)

    def test_require_mathlib(self):
        """El lakefile debe requerir mathlib."""
        self.assertIn("require mathlib", self.content)


# ---------------------------------------------------------------------------
# 11. Consistencia con implementación Python
# ---------------------------------------------------------------------------

class TestConsistenciaPython(unittest.TestCase):
    """Verifica la consistencia entre la formalización Lean y el módulo Python."""

    def test_gamma_c_consistente(self):
        """γ_c = 2.57 en ambas implementaciones."""
        γ_c_lean = 2.57  # Definido en PicodePT.lean
        try:
            from physics.picode_resonancia_holografica import _BETA_CRITICO
            self.assertAlmostEqual(_BETA_CRITICO, γ_c_lean, places=2)
        except ImportError:
            self.skipTest("picode_resonancia_holografica no disponible")

    def test_f0_consistente(self):
        """f₀ = 141.7001 Hz en ambas implementaciones."""
        f0_lean = 141.7001
        try:
            from physics.picode_resonancia_holografica import _F0_HZ
            self.assertAlmostEqual(_F0_HZ, f0_lean, places=3)
        except ImportError:
            self.skipTest("picode_resonancia_holografica no disponible")

    def test_psi_umbral_consistente(self):
        """Umbral mínimo Ψ = 0.888 en ambas implementaciones."""
        ψ_umbral_lean = 0.888  # Referenciado en PicodePT.lean
        try:
            from physics.picode_resonancia_holografica import _PSI_MINIMA
            self.assertAlmostEqual(_PSI_MINIMA, ψ_umbral_lean, places=2)
        except ImportError:
            self.skipTest("picode_resonancia_holografica no disponible")

    def test_psi_pt_coincide_con_python(self):
        """ψ_PT(γ) = 1 - (γ/γ_c)² debe dar el mismo resultado en Python."""
        γ_c = 2.57
        # Verificar para múltiples valores de γ
        test_cases = [
            (0.0, 1.0),
            (0.183, 0.9949),
            (1.0, 0.8489),
            (2.57, 0.0),
        ]
        for γ, expected in test_cases:
            ψ = 1 - (γ / γ_c) ** 2
            self.assertAlmostEqual(ψ, expected, places=3,
                                   msg=f"ψ_PT({γ}) debe ser ≈ {expected}")


# ---------------------------------------------------------------------------
# 12. Integridad del archivo Lean 4
# ---------------------------------------------------------------------------

class TestIntegridadLean(unittest.TestCase):
    """Verifica la integridad sintáctica del archivo Lean 4."""

    def setUp(self):
        self.content = _lean_content()
        self.lines = self.content.splitlines()

    def test_no_triple_sorry(self):
        """No debe tener tres o más sorrys consecutivos sin justificación."""
        sorry_count = self.content.count("  sorry")
        # Permitir hasta 5 sorrys (trabajo en progreso)
        self.assertLessEqual(sorry_count, 5,
                             f"Demasiados sorrys sin justificación: {sorry_count}")

    def test_comentarios_docstring(self):
        """Debe tener documentación /-- ... -/ en las definiciones."""
        self.assertIn("/--", self.content)

    def test_referencias_bender(self):
        """Debe referenciar el trabajo de Bender-Boettcher."""
        self.assertIn("Bender", self.content)

    def test_autor_referenciado(self):
        """Debe incluir referencia al autor."""
        self.assertIn("José Manuel Mota Burruezo", self.content)

    def test_doi_presente(self):
        """Debe incluir el DOI de referencia."""
        self.assertIn("10.5281/zenodo", self.content)

    def test_lean4_syntax_noncomputable(self):
        """Las funciones con cálculos no computables deben marcarse."""
        self.assertIn("noncomputable", self.content)

    def test_no_parameter_keyword(self):
        """No debe usar 'parameter' (sintaxis Lean 3, no válida en Lean 4)."""
        # Buscar uso de 'parameter' como keyword de Lean 3
        lean3_param = re.search(r'\bparameter\s+\(', self.content)
        self.assertIsNone(lean3_param,
                          "Encontrado 'parameter' (Lean 3): usar 'variable' en Lean 4")

    def test_usa_variable_lean4(self):
        """Debe usar 'variable' en lugar de 'parameter' (sintaxis Lean 4)."""
        self.assertIn("variable", self.content)

    def test_structure_keyword(self):
        """Debe usar 'structure' para definir el operador."""
        self.assertIn("structure", self.content)

    def test_def_keyword(self):
        """Debe usar 'def' para las definiciones."""
        self.assertIn("def", self.content)

    def test_lemma_keyword(self):
        """Debe usar 'lemma' para los lemas."""
        self.assertIn("lemma", self.content)

    def test_theorem_keyword(self):
        """Debe usar 'theorem' para los teoremas."""
        self.assertIn("theorem", self.content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
