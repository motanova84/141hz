#!/usr/bin/env python3
"""
Tests para generar_cy_kappa_25773.py
=====================================

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Enero 2026
"""

import json
import math
import sys
import unittest
from pathlib import Path

# Añadir el directorio scripts al path
sys.path.insert(0, str(Path(__file__).parent))

from generar_cy_kappa_25773 import generar_cy_kappa_25773


class TestGenerarCY(unittest.TestCase):
    """Tests para la generación de variedades CY."""

    def test_numero_variedades(self):
        """Verifica que se generen 12 variedades para h11+h21=13."""
        cy_varieties = generar_cy_kappa_25773(target_N=13)
        self.assertEqual(len(cy_varieties), 12)

    def test_suma_hodge_numbers(self):
        """Verifica que h11 + h21 = 13 para todas las variedades."""
        cy_varieties = generar_cy_kappa_25773(target_N=13)
        for cy in cy_varieties:
            self.assertEqual(cy["h11"] + cy["h21"], 13)

    def test_euler_characteristic(self):
        """Verifica el cálculo de la característica de Euler."""
        cy_varieties = generar_cy_kappa_25773(target_N=13)
        for cy in cy_varieties:
            expected_chi = 2 * (cy["h11"] - cy["h21"])
            self.assertEqual(cy["chi_Euler"], expected_chi)

    def test_kappa_pi_value(self):
        """Verifica que κ_Π = log(13) para todas las variedades."""
        cy_varieties = generar_cy_kappa_25773(target_N=13)
        expected_kappa = round(math.log(13), 6)
        
        for cy in cy_varieties:
            self.assertAlmostEqual(cy["kappa_pi"], expected_kappa, places=6)
            # Verificar que el valor es aproximadamente 2.564949
            self.assertAlmostEqual(cy["kappa_pi"], 2.564949, places=6)

    def test_id_format(self):
        """Verifica el formato de los IDs."""
        cy_varieties = generar_cy_kappa_25773(target_N=13)
        for cy in cy_varieties:
            expected_id = f"CY_{cy['h11']}_{cy['h21']}"
            self.assertEqual(cy["ID"], expected_id)

    def test_specific_example(self):
        """Verifica el ejemplo específico CY_6_7 del problema."""
        cy_varieties = generar_cy_kappa_25773(target_N=13)
        
        # Buscar CY_6_7
        cy_6_7 = None
        for cy in cy_varieties:
            if cy["ID"] == "CY_6_7":
                cy_6_7 = cy
                break
        
        self.assertIsNotNone(cy_6_7)
        self.assertEqual(cy_6_7["h11"], 6)
        self.assertEqual(cy_6_7["h21"], 7)
        self.assertEqual(cy_6_7["chi_Euler"], -2)
        self.assertAlmostEqual(cy_6_7["kappa_pi"], 2.564949, places=6)

    def test_range_h11(self):
        """Verifica que h11 va de 1 a 12."""
        cy_varieties = generar_cy_kappa_25773(target_N=13)
        h11_values = [cy["h11"] for cy in cy_varieties]
        
        self.assertEqual(min(h11_values), 1)
        self.assertEqual(max(h11_values), 12)
        self.assertEqual(len(set(h11_values)), 12)  # Todos únicos

    def test_range_h21(self):
        """Verifica que h21 va de 1 a 12."""
        cy_varieties = generar_cy_kappa_25773(target_N=13)
        h21_values = [cy["h21"] for cy in cy_varieties]
        
        self.assertEqual(min(h21_values), 1)
        self.assertEqual(max(h21_values), 12)
        self.assertEqual(len(set(h21_values)), 12)  # Todos únicos

    def test_json_structure(self):
        """Verifica que la estructura JSON sea correcta."""
        cy_varieties = generar_cy_kappa_25773(target_N=13)
        
        for cy in cy_varieties:
            # Verificar que tenga exactamente 5 campos
            self.assertEqual(len(cy), 5)
            
            # Verificar que tenga los campos requeridos
            self.assertIn("ID", cy)
            self.assertIn("h11", cy)
            self.assertIn("h21", cy)
            self.assertIn("chi_Euler", cy)
            self.assertIn("kappa_pi", cy)
            
            # Verificar tipos
            self.assertIsInstance(cy["ID"], str)
            self.assertIsInstance(cy["h11"], int)
            self.assertIsInstance(cy["h21"], int)
            self.assertIsInstance(cy["chi_Euler"], int)
            self.assertIsInstance(cy["kappa_pi"], float)

    def test_different_target_N(self):
        """Verifica generación con diferente target_N."""
        # Probar con N=7
        cy_varieties = generar_cy_kappa_25773(target_N=7)
        self.assertEqual(len(cy_varieties), 6)  # h11 de 1 a 6
        
        for cy in cy_varieties:
            self.assertEqual(cy["h11"] + cy["h21"], 7)
            expected_kappa = round(math.log(7), 6)
            self.assertAlmostEqual(cy["kappa_pi"], expected_kappa, places=6)


class TestJSONFile(unittest.TestCase):
    """Tests para verificar el archivo JSON generado."""

    def setUp(self):
        """Ejecutar el script para generar el archivo JSON."""
        # El archivo ya debería estar generado, solo verificar su existencia
        base_dir = Path(__file__).parent.parent
        self.json_path = base_dir / "data" / "cy_kappa_25773_log13.json"

    def test_json_file_exists(self):
        """Verifica que el archivo JSON exista."""
        # Si no existe, intentar generarlo
        if not self.json_path.exists():
            self.skipTest("JSON file not generated yet")
        
        self.assertTrue(self.json_path.exists())

    def test_json_file_parseable(self):
        """Verifica que el archivo JSON sea válido."""
        if not self.json_path.exists():
            self.skipTest("JSON file not generated yet")
        
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 12)

    def test_json_file_content(self):
        """Verifica el contenido del archivo JSON."""
        if not self.json_path.exists():
            self.skipTest("JSON file not generated yet")
        
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Verificar primera entrada
        first = data[0]
        self.assertEqual(first["ID"], "CY_1_12")
        self.assertEqual(first["h11"], 1)
        self.assertEqual(first["h21"], 12)
        
        # Verificar última entrada
        last = data[-1]
        self.assertEqual(last["ID"], "CY_12_1")
        self.assertEqual(last["h11"], 12)
        self.assertEqual(last["h21"], 1)


if __name__ == "__main__":
    unittest.main()
