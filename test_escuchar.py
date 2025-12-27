#!/usr/bin/env python3
"""
Tests para escuchar.py - Script interactivo del descubrimiento 141.7001 Hz
"""

import sys
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from io import StringIO

# Import the module to test
sys.path.insert(0, str(Path(__file__).parent))
import escuchar


class TestEscuchar(unittest.TestCase):
    """Tests para el script escuchar.py"""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.results_file = Path("multi_event_final.json")

    def test_colors_class_exists(self):
        """Test que la clase Colors está definida."""
        self.assertTrue(hasattr(escuchar, 'Colors'))
        self.assertTrue(hasattr(escuchar.Colors, 'OKGREEN'))
        self.assertTrue(hasattr(escuchar.Colors, 'WARNING'))
        self.assertTrue(hasattr(escuchar.Colors, 'ENDC'))

    def test_print_poem_runs(self):
        """Test que print_poem se ejecuta sin errores."""
        # Mock time.sleep to speed up tests
        with patch('escuchar.time.sleep'):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                escuchar.print_poem()
                output = fake_out.getvalue()
                self.assertIn("141.7001", output)
                self.assertIn("ESCUCHAR", output)

    def test_print_mathematical_whisper_runs(self):
        """Test que print_mathematical_whisper se ejecuta."""
        with patch('escuchar.input', return_value=''):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                escuchar.print_mathematical_whisper()
                output = fake_out.getvalue()
                self.assertIn("141.7001", output)
                self.assertIn("MATEMÁTICO", output)
                self.assertIn("0.551020", output)

    def test_print_universe_response_with_file(self):
        """Test que print_universe_response funciona con archivo JSON."""
        if self.results_file.exists():
            with patch('escuchar.time.sleep'):
                with patch('escuchar.input', return_value=''):
                    with patch('sys.stdout', new=StringIO()) as fake_out:
                        result = escuchar.print_universe_response()
                        output = fake_out.getvalue()
                        self.assertTrue(result)
                        self.assertIn("UNIVERSO", output)
                        self.assertIn("GW150914", output)
                        self.assertIn("11 eventos", output)
        else:
            self.skipTest("multi_event_final.json no encontrado")

    def test_print_universe_response_without_file(self):
        """Test que print_universe_response maneja archivo faltante."""
        # Temporalmente renombrar el archivo si existe
        temp_name = None
        if self.results_file.exists():
            temp_name = Path("multi_event_final.json.bak")
            self.results_file.rename(temp_name)

        try:
            with patch('sys.stdout', new=StringIO()) as fake_out:
                result = escuchar.print_universe_response()
                output = fake_out.getvalue()
                self.assertFalse(result)
                self.assertIn("Error", output)
        finally:
            # Restaurar el archivo
            if temp_name and temp_name.exists():
                temp_name.rename(self.results_file)

    def test_print_universe_response_corrupted_json(self):
        """Test que print_universe_response maneja JSON corrupto."""
        # Crear un archivo JSON corrupto temporalmente
        backup_file = None
        if self.results_file.exists():
            backup_file = Path("multi_event_final.json.backup")
            self.results_file.rename(backup_file)

        try:
            # Escribir JSON inválido
            with open(self.results_file, 'w') as f:
                f.write("{ invalid json }")

            with patch('sys.stdout', new=StringIO()) as fake_out:
                result = escuchar.print_universe_response()
                output = fake_out.getvalue()
                self.assertFalse(result)
                self.assertIn("corrupto", output.lower())
        finally:
            # Limpiar y restaurar
            if self.results_file.exists():
                self.results_file.unlink()
            if backup_file and backup_file.exists():
                backup_file.rename(self.results_file)


    def test_print_statistical_validation_runs(self):
        """Test que print_statistical_validation se ejecuta."""
        with patch('escuchar.input', return_value=''):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                escuchar.print_statistical_validation()
                output = fake_out.getvalue()
                self.assertIn("VALIDACIÓN", output)
                self.assertIn("10σ", output)
                self.assertIn("Multi-detector", output)

    def test_print_conclusion_runs(self):
        """Test que print_conclusion se ejecuta."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            escuchar.print_conclusion()
            output = fake_out.getvalue()
            self.assertIn("ESCUCHAR", output)
            self.assertIn("git clone", output)
            self.assertIn("multi_event_analysis.py", output)

    def test_print_menu_runs(self):
        """Test que print_menu se ejecuta."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            escuchar.print_menu()
            output = fake_out.getvalue()
            self.assertIn("Menú", output)
            self.assertIn("Experiencia completa", output)

    @patch('sys.argv', ['escuchar.py', '--auto'])
    def test_main_auto_mode(self):
        """Test modo automático."""
        if not self.results_file.exists():
            self.skipTest("multi_event_final.json no encontrado")

        with patch('escuchar.time.sleep'):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                result = escuchar.main()
                self.assertEqual(result, 0)
                output = fake_out.getvalue()
                self.assertIn("141.7001", output)

    @patch('sys.argv', ['escuchar.py'])
    def test_main_interactive_quit(self):
        """Test modo interactivo con salida inmediata."""
        with patch('escuchar.input', return_value='0'):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                result = escuchar.main()
                self.assertEqual(result, 0)
                output = fake_out.getvalue()
                self.assertIn("Menú", output)

    def test_json_file_structure(self):
        """Test que el archivo JSON tiene la estructura correcta."""
        if not self.results_file.exists():
            self.skipTest("multi_event_final.json no encontrado")

        with open(self.results_file) as f:
            data = json.load(f)

        # Verificar estructura principal
        self.assertIn("discovery", data)
        self.assertIn("statistics", data)
        self.assertIn("events", data)

        # Verificar discovery
        self.assertEqual(data["discovery"]["frequency_target_hz"], 141.7001)
        self.assertEqual(data["discovery"]["catalog"], "GWTC-1")

        # Verificar statistics
        stats = data["statistics"]
        self.assertEqual(stats["total_events"], 11)
        self.assertEqual(stats["detection_rate"], "100%")
        self.assertGreater(stats["snr_mean"], 15)
        self.assertLess(stats["snr_mean"], 25)

        # Verificar eventos
        events = data["events"]
        self.assertEqual(len(events), 11)

        # Verificar un evento específico
        gw150914 = events["GW150914"]
        self.assertEqual(gw150914["date"], "2015-09-14")
        self.assertIn("H1", gw150914["snr"])
        self.assertIn("L1", gw150914["snr"])
        self.assertTrue(gw150914["h1_above_threshold"])
        self.assertTrue(gw150914["l1_above_threshold"])


class TestIntegration(unittest.TestCase):
    """Tests de integración."""

    def test_full_auto_execution(self):
        """Test ejecución completa en modo automático."""
        results_file = Path("multi_event_final.json")
        if not results_file.exists():
            self.skipTest("multi_event_final.json no encontrado")

        with patch('escuchar.time.sleep'):
            with patch('sys.argv', ['escuchar.py', '--auto']):
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    result = escuchar.main()
                    self.assertEqual(result, 0)
                    output = fake_out.getvalue()

                    # Verificar que todas las secciones se ejecutaron
                    self.assertIn("SUSURRO MATEMÁTICO", output)
                    self.assertIn("GRITO DEL UNIVERSO", output)
                    self.assertIn("VALIDACIÓN ESTADÍSTICA", output)
                    self.assertIn("AHORA TE TOCA ESCUCHAR", output)

                    # Verificar contenido específico
                    self.assertIn("141.7001", output)
                    self.assertIn("11 eventos", output)
                    self.assertIn("100%", output)
                    self.assertIn("10σ", output)


def main():
    """Ejecuta todos los tests."""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()
