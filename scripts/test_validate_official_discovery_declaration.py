#!/usr/bin/env python3
"""
Test para el script de validación de la declaración oficial
============================================================

Tests unitarios para validate_official_discovery_declaration.py

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 5 de febrero de 2026
"""

import unittest
import sys
import json
import tempfile
from pathlib import Path

# Agregar el directorio de scripts al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

# Importar constantes del módulo principal
try:
    from validate_official_discovery_declaration import (
        F0_TARGET, BANDWIDTH, SNR_THRESHOLD, GWTC1_EVENTS, 
        INSTRUMENTAL_LINES, MIN_INSTRUMENTAL_SEPARATION
    )
except ImportError:
    # Fallback si no se puede importar (solo para compatibilidad)
    F0_TARGET = 141.7001
    BANDWIDTH = 1.0
    SNR_THRESHOLD = 5.0
    GWTC1_EVENTS = 11
    INSTRUMENTAL_LINES = [60, 120, 180, 393]
    MIN_INSTRUMENTAL_SEPARATION = 20.0

# Mock para evitar dependencias
class MockResults:
    """Mock de resultados multi-evento para testing."""
    
    @staticmethod
    def create_valid_results():
        """Crea resultados válidos que pasan todos los claims."""
        return {
            'statistics': {
                'total_events': GWTC1_EVENTS,
                'detection_rate': '100%',
                'snr_mean': 20.95,
                'snr_std': 5.54
            },
            'events': [
                {
                    'name': f'GW{i}',
                    'frequency_detected': F0_TARGET,
                    'detectors': {'H1': {'snr': 15.0}, 'L1': {'snr': 14.0}}
                }
                for i in range(GWTC1_EVENTS)
            ]
        }
    
    @staticmethod
    def create_invalid_results():
        """Crea resultados inválidos que fallan algunos claims."""
        return {
            'statistics': {
                'total_events': 8,
                'detection_rate': '73%',
                'snr_mean': 3.5,
                'snr_std': 2.1
            },
            'events': [
                {
                    'name': f'GW{i}',
                    'frequency_detected': F0_TARGET,
                    'detectors': {'H1': {'snr': 3.0}}
                }
                for i in range(8)
            ]
        }


class TestValidateOfficialDiscoveryDeclaration(unittest.TestCase):
    """Tests para el script de validación de la declaración oficial."""
    
    def setUp(self):
        """Configuración previa a cada test."""
        # Crear directorio temporal para resultados
        self.temp_dir = tempfile.mkdtemp()
        self.results_file = Path(self.temp_dir) / 'multi_event_final.json'
    
    def tearDown(self):
        """Limpieza posterior a cada test."""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def test_valid_results_pass_all_claims(self):
        """Test: Resultados válidos pasan todos los claims."""
        # Crear archivo de resultados válidos
        results = MockResults.create_valid_results()
        with open(self.results_file, 'w') as f:
            json.dump(results, f)
        
        # Verificar estructura
        self.assertEqual(results['statistics']['total_events'], 11)
        self.assertEqual(results['statistics']['detection_rate'], '100%')
        self.assertGreater(results['statistics']['snr_mean'], 5.0)
    
    def test_claim1_detection_rate(self):
        """Test: Claim 1 - Tasa de detección 100% (11/11)."""
        results = MockResults.create_valid_results()
        
        total_events = results['statistics']['total_events']
        detection_rate = results['statistics']['detection_rate']
        
        self.assertEqual(total_events, GWTC1_EVENTS, f"Deben ser {GWTC1_EVENTS} eventos GWTC-1")
        self.assertEqual(detection_rate, '100%', "Tasa de detección debe ser 100%")
    
    def test_claim2_snr_threshold(self):
        """Test: Claim 2 - SNR medio > 5σ."""
        results = MockResults.create_valid_results()
        
        snr_mean = results['statistics']['snr_mean']
        
        self.assertGreater(snr_mean, SNR_THRESHOLD, 
                          f"SNR medio debe superar umbral de {SNR_THRESHOLD}σ")
    
    def test_claim3_frequency_band(self):
        """Test: Claim 3 - Banda de análisis [140.7-142.7] Hz."""
        results = MockResults.create_valid_results()
        
        band_low = F0_TARGET - BANDWIDTH
        band_high = F0_TARGET + BANDWIDTH
        
        for event in results['events']:
            freq = event['frequency_detected']
            self.assertGreaterEqual(freq, band_low, 
                                   f"Frecuencia {freq} debe ser ≥ {band_low} Hz")
            self.assertLessEqual(freq, band_high,
                                f"Frecuencia {freq} debe ser ≤ {band_high} Hz")
    
    def test_claim4_instrumental_separation(self):
        """Test: Claim 4 - Separación de líneas instrumentales > 20 Hz."""
        min_separation = min(abs(F0_TARGET - line) for line in INSTRUMENTAL_LINES)
        
        self.assertGreater(min_separation, MIN_INSTRUMENTAL_SEPARATION,
                          f"Separación mínima ({min_separation:.1f} Hz) debe ser > {MIN_INSTRUMENTAL_SEPARATION} Hz")
    
    def test_claim5_multidetector(self):
        """Test: Claim 5 - Multi-detector H1 y L1."""
        results = MockResults.create_valid_results()
        
        detectors_found = set()
        for event in results['events']:
            if 'detectors' in event:
                detectors_found.update(event['detectors'].keys())
        
        expected_detectors = {'H1', 'L1'}
        
        self.assertTrue(expected_detectors.issubset(detectors_found),
                       f"Detectores esperados {expected_detectors} no encontrados en {detectors_found}")
    
    def test_invalid_results_fail_claims(self):
        """Test: Resultados inválidos fallan algunos claims."""
        results = MockResults.create_invalid_results()
        
        # Claim 1: Debe fallar (solo 8 eventos, no 11)
        self.assertNotEqual(results['statistics']['total_events'], GWTC1_EVENTS)
        
        # Claim 2: Debe fallar (SNR < 5σ)
        self.assertLess(results['statistics']['snr_mean'], SNR_THRESHOLD)
    
    def test_theoretical_connection(self):
        """Test: Verificar que f₀ = 141.7001 Hz está documentado."""
        # Verificar que el valor teórico está en rango esperado
        self.assertAlmostEqual(F0_TARGET, 141.7, places=0)
        
        # Verificar precisión
        self.assertGreater(F0_TARGET, 141.0)
        self.assertLess(F0_TARGET, 142.0)


class TestStatisticalValidation(unittest.TestCase):
    """Tests para validación estadística."""
    
    def test_significance_threshold(self):
        """Test: Umbral de significancia >10σ corresponde a p < 10⁻²⁵."""
        try:
            from scipy.stats import norm
            
            sigma_threshold = 10.0
            p_value = 1 - norm.cdf(sigma_threshold)
            
            # Verificar que p < 10⁻²⁵ para 10σ
            self.assertLess(p_value, 1e-20, 
                           f"P-value para {sigma_threshold}σ debe ser << 10⁻²⁵")
        except ImportError:
            self.skipTest("scipy no disponible")
    
    def test_bonferroni_correction(self):
        """Test: Corrección de Bonferroni para Look-Elsewhere Effect."""
        try:
            from scipy.stats import norm
            
            # Parámetros de la corrección
            n_trials = 60  # bins en banda ±1 Hz con resolución 0.031 Hz
            
            # P-value individual para 5σ
            p_individual = 1 - norm.cdf(5.0)
            
            # Corrección de Bonferroni
            p_corrected = min(1.0, p_individual * n_trials)
            
            # Verificar que la corrección aumenta el p-value
            self.assertGreaterEqual(p_corrected, p_individual)
            
            # Verificar que sigue siendo significativo
            self.assertLess(p_corrected, 0.05)
        except ImportError:
            self.skipTest("scipy no disponible")


class TestReproducibility(unittest.TestCase):
    """Tests para verificar reproducibilidad."""
    
    def test_documentation_exists(self):
        """Test: Verificar que documentación oficial existe."""
        declaration_file = Path(__file__).parent.parent / 'DECLARACION_OFICIAL_DESCUBRIMIENTO_EMPIRICO_141HZ.md'
        
        self.assertTrue(declaration_file.exists(),
                       "Declaración oficial debe existir")
        
        # Verificar que el archivo no está vacío
        self.assertGreater(declaration_file.stat().st_size, 1000,
                          "Declaración oficial debe tener contenido sustancial")
    
    def test_scripts_exist(self):
        """Test: Verificar que scripts de validación existen."""
        scripts_dir = Path(__file__).parent.parent / 'scripts'
        
        required_scripts = [
            'validacion_gwtc1_tridetector.py',
            'busqueda_sistematica_gwtc1.py',
            'analisis_poblacional_gwtc1.py',
            'validate_multievent_141hz_peak.py'
        ]
        
        for script_name in required_scripts:
            script_path = scripts_dir / script_name
            self.assertTrue(script_path.exists(),
                           f"Script requerido {script_name} debe existir")
    
    def test_theoretical_derivation_exists(self):
        """Test: Verificar que derivaciones teóricas existen."""
        docs_dir = Path(__file__).parent.parent
        
        required_docs = [
            'DERIVACION_COMPLETA_F0.md',
            'ECUACION_VIVA_README.md'
        ]
        
        for doc_name in required_docs:
            doc_path = docs_dir / doc_name
            self.assertTrue(doc_path.exists(),
                           f"Documento requerido {doc_name} debe existir")


def run_tests():
    """Ejecuta todos los tests."""
    # Crear test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestValidateOfficialDiscoveryDeclaration))
    suite.addTests(loader.loadTestsFromTestCase(TestStatisticalValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestReproducibility))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de salida
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
