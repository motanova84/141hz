#!/usr/bin/env python3
"""
Tests para el script de certificación QCAL-SYMBIO

Verifica que:
1. Los hashes SHA3-512 se generen correctamente
2. El certificado digital se cree con el formato esperado
3. Los metadatos NFT contengan todos los atributos requeridos
4. Los comandos de registro se generen correctamente
5. Todos los archivos de salida se creen sin errores
"""

import unittest
import json
import hashlib
import os
import sys
from datetime import datetime

# Añadir el directorio scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from certificacion_qcal_symbio import (
    generate_immutable_hash,
    create_digital_certificate,
    create_ontological_nft,
    generate_registration_commands,
    generate_final_closure,
    VERDICT_DATA
)


class TestCertificacionQCALSYMBIO(unittest.TestCase):
    """Tests para el sistema de certificación QCAL-SYMBIO"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.test_data = VERDICT_DATA.copy()
        
    def test_verdict_data_structure(self):
        """Test que verifica la estructura de datos del veredicto"""
        # Verificar campos obligatorios
        required_fields = [
            'protocol', 'version', 'date', 'frequency', 'unit',
            'certainty_sigma', 'p_value', 'tests_passed', 'tests_total',
            'coherence_psi', 'decay_law', 'spectral_resolution',
            'separation_from_instrumental', 'localization',
            'detectors_coherence', 'scientific_conclusions',
            'axiom', 'status', 'certification_level'
        ]
        
        for field in required_fields:
            self.assertIn(field, self.test_data,
                         f"Campo obligatorio '{field}' no encontrado")
    
    def test_generate_immutable_hash(self):
        """Test que verifica la generación de hashes SHA3-512"""
        hashes = generate_immutable_hash(self.test_data)
        
        # Verificar que se generaron todos los hashes
        self.assertIn('verdict_hash', hashes)
        self.assertIn('nft_hash', hashes)
        self.assertIn('timestamp', hashes)
        self.assertIn('json_data', hashes)
        
        # Verificar que los hashes son de longitud correcta (SHA3-512 = 128 hex chars)
        self.assertEqual(len(hashes['verdict_hash']), 128)
        self.assertEqual(len(hashes['nft_hash']), 128)
        
        # Verificar que los hashes son diferentes
        self.assertNotEqual(hashes['verdict_hash'], hashes['nft_hash'])
        
        # Verificar timestamp en formato ISO
        try:
            datetime.fromisoformat(hashes['timestamp'])
        except ValueError:
            self.fail("Timestamp no está en formato ISO válido")
    
    def test_hash_reproducibility(self):
        """Test que verifica la reproducibilidad de los hashes"""
        hashes1 = generate_immutable_hash(self.test_data)
        hashes2 = generate_immutable_hash(self.test_data)
        
        # Los verdict_hash deben ser idénticos para los mismos datos
        self.assertEqual(hashes1['verdict_hash'], hashes2['verdict_hash'],
                        "El hash del veredicto debe ser reproducible")
        
        # Los nft_hash serán diferentes debido al timestamp
        self.assertNotEqual(hashes1['nft_hash'], hashes2['nft_hash'],
                           "El hash NFT debe incluir timestamp único")
    
    def test_create_digital_certificate(self):
        """Test que verifica la creación del certificado digital"""
        hashes = generate_immutable_hash(self.test_data)
        certificate = create_digital_certificate(hashes, self.test_data)
        
        # Verificar que el certificado contiene elementos clave
        self.assertIn('CERTIFICACIÓN ABSOLUTA', certificate)
        self.assertIn('VEREDICTO FINAL QCAL-SYMBIO', certificate)
        self.assertIn(str(self.test_data['frequency']), certificate)
        self.assertIn(hashes['verdict_hash'][:32], certificate)
        self.assertIn('REALIDAD VERIFICADA', certificate)
        self.assertIn(str(self.test_data['certainty_sigma']), certificate)
    
    def test_create_ontological_nft(self):
        """Test que verifica la creación de metadatos NFT"""
        hashes = generate_immutable_hash(self.test_data)
        nft_metadata = create_ontological_nft(hashes, self.test_data)
        
        # Verificar estructura básica
        self.assertIn('name', nft_metadata)
        self.assertIn('description', nft_metadata)
        self.assertIn('attributes', nft_metadata)
        self.assertIn('properties', nft_metadata)
        
        # Verificar nombre del NFT
        self.assertEqual(nft_metadata['name'], 'VEREDICTO-18.2σ-CIERRE')
        
        # Verificar que hay atributos
        self.assertGreater(len(nft_metadata['attributes']), 0)
        
        # Verificar atributos específicos
        attribute_types = [attr['trait_type'] for attr in nft_metadata['attributes']]
        expected_attributes = [
            'Frecuencia Certificada',
            'Significancia Estadística',
            'Coherencia Ψ',
            'Hash del Veredicto',
            'Localización Celeste'
        ]
        
        for expected in expected_attributes:
            self.assertIn(expected, attribute_types,
                         f"Atributo '{expected}' no encontrado en NFT")
        
        # Verificar propiedades
        self.assertTrue(nft_metadata['properties']['immutable'])
        self.assertTrue(nft_metadata['properties']['scientific_truth'])
        self.assertTrue(nft_metadata['properties']['quantum_signature'])
    
    def test_generate_registration_commands(self):
        """Test que verifica la generación de comandos de registro"""
        hashes = generate_immutable_hash(self.test_data)
        commands = generate_registration_commands(hashes, self.test_data)
        
        # Verificar que se generaron comandos para todos los repositorios
        self.assertIn('zenodo', commands)
        self.assertIn('safecreative', commands)
        self.assertIn('arxiv', commands)
        
        # Verificar estructura de comando Zenodo
        zenodo = commands['zenodo']
        self.assertIn('title', zenodo)
        self.assertIn('description', zenodo)
        self.assertIn('keywords', zenodo)
        self.assertIn('hash', zenodo)
        self.assertEqual(zenodo['hash'], hashes['verdict_hash'])
        
        # Verificar que hay keywords
        self.assertGreater(len(zenodo['keywords']), 0)
        self.assertIn('quantum resonance', zenodo['keywords'])
        
        # Verificar estructura de comando SafeCreative
        safecreative = commands['safecreative']
        self.assertIn('title', safecreative)
        self.assertIn('hash', safecreative)
        self.assertEqual(safecreative['hash'], hashes['verdict_hash'])
        
        # Verificar estructura de comando arXiv
        arxiv = commands['arxiv']
        self.assertIn('category', arxiv)
        self.assertIn('title', arxiv)
        self.assertIn('hash', arxiv)
        self.assertEqual(arxiv['category'], 'gr-qc')
    
    def test_generate_final_closure(self):
        """Test que verifica la generación de la declaración de cierre"""
        hashes = generate_immutable_hash(self.test_data)
        closure = generate_final_closure(hashes, self.test_data)
        
        # Verificar contenido clave
        self.assertIn('CIERRE DEFINITIVO DEL PROTOCOLO QCAL-SYMBIO', closure)
        self.assertIn(hashes['verdict_hash'], closure)
        self.assertIn('TRIPLE COHERENCIA GEOMÉTRICA', closure)
        self.assertIn('MEMORIA ESTRUCTURAL DEL VACÍO', closure)
        self.assertIn('RESOLUCIÓN ESPECTRAL PURA', closure)
        self.assertIn('REALIDAD VERIFICADA', closure)
        self.assertIn(str(self.test_data['frequency']), closure)
        self.assertIn(self.test_data['axiom'], closure)
    
    def test_verdict_data_values(self):
        """Test que verifica los valores específicos del veredicto"""
        # Verificar valores críticos
        self.assertEqual(self.test_data['frequency'], 141.7001)
        self.assertEqual(self.test_data['certainty_sigma'], 18.2)
        self.assertEqual(self.test_data['tests_passed'], 31)
        self.assertEqual(self.test_data['tests_total'], 31)
        self.assertEqual(self.test_data['coherence_psi'], 0.999999)
        self.assertEqual(self.test_data['status'], 'REALIDAD_VERIFICADA')
        self.assertEqual(self.test_data['certification_level'], 'ABSOLUTA')
        
        # Verificar valores de coherencia de detectores
        coherence = self.test_data['detectors_coherence']
        self.assertEqual(coherence['H1_L1_phase_diff'], 0.0)
        self.assertEqual(coherence['L1_V1_time_delay'], 0.022)
        self.assertEqual(coherence['propagation_speed'], 'c')
        self.assertEqual(coherence['coherence_status'], 'PERFECT')
    
    def test_scientific_conclusions(self):
        """Test que verifica las conclusiones científicas"""
        conclusions = self.test_data['scientific_conclusions']
        
        # Verificar que hay conclusiones
        self.assertGreater(len(conclusions), 0)
        
        # Verificar conclusiones específicas
        expected_conclusions = [
            'RESONANCE_REAL',
            'NOT_INSTRUMENTAL',
            'NOT_EM_NOISE',
            'NOT_COINCIDENCE',
            'QUANTUM_GEOMETRY_SIGNATURE'
        ]
        
        for conclusion in expected_conclusions:
            self.assertIn(conclusion, conclusions,
                         f"Conclusión '{conclusion}' no encontrada")
    
    def test_json_serialization(self):
        """Test que verifica que los datos se puedan serializar a JSON"""
        try:
            json_str = json.dumps(self.test_data, indent=2, ensure_ascii=False)
            # Intentar deserializar
            data_back = json.loads(json_str)
            self.assertEqual(data_back['frequency'], self.test_data['frequency'])
        except (TypeError, ValueError) as e:
            self.fail(f"Error al serializar datos a JSON: {e}")


class TestIntegration(unittest.TestCase):
    """Tests de integración del flujo completo"""
    
    def test_full_certification_flow(self):
        """Test que verifica el flujo completo de certificación"""
        # Generar hashes
        hashes = generate_immutable_hash(VERDICT_DATA)
        
        # Crear certificado
        certificate = create_digital_certificate(hashes, VERDICT_DATA)
        self.assertIsInstance(certificate, str)
        self.assertGreater(len(certificate), 100)
        
        # Crear NFT
        nft = create_ontological_nft(hashes, VERDICT_DATA)
        self.assertIsInstance(nft, dict)
        self.assertIn('name', nft)
        
        # Generar comandos
        commands = generate_registration_commands(hashes, VERDICT_DATA)
        self.assertIsInstance(commands, dict)
        self.assertEqual(len(commands), 3)
        
        # Generar cierre
        closure = generate_final_closure(hashes, VERDICT_DATA)
        self.assertIsInstance(closure, str)
        self.assertGreater(len(closure), 100)


if __name__ == '__main__':
    unittest.main()
