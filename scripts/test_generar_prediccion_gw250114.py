#!/usr/bin/env python3
"""
Test para generar_prediccion_gw250114.py
"""

import sys
import os
import json
import unittest
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generar_prediccion_gw250114 import generar_prediccion_gw250114, guardar_prediccion


class TestGenerarPrediccionGW250114(unittest.TestCase):
    
    def test_generar_prediccion_estructura(self):
        """Verificar que la predicción tiene la estructura correcta"""
        prediccion = generar_prediccion_gw250114()
        
        # Verificar secciones principales
        self.assertIn('metadata', prediccion)
        self.assertIn('predicciones_cuantitativas', prediccion)
        self.assertIn('criterios_validacion_global', prediccion)
        self.assertIn('resultados_posibles', prediccion)
        self.assertIn('contexto_comparativo', prediccion)
        self.assertIn('instrucciones_validacion', prediccion)
    
    def test_metadata_correcto(self):
        """Verificar metadata de la predicción"""
        prediccion = generar_prediccion_gw250114()
        metadata = prediccion['metadata']
        
        self.assertEqual(metadata['evento_target'], 'GW250114')
        self.assertEqual(metadata['estado'], 'PENDIENTE DE DATOS')
        self.assertTrue(metadata['falsable'])
        self.assertIn('Ψ = I × A²_eff', metadata['teoria_base'])
    
    def test_predicciones_cuantitativas(self):
        """Verificar que las predicciones son cuantitativas y falsables"""
        prediccion = generar_prediccion_gw250114()
        pred = prediccion['predicciones_cuantitativas']
        
        # Verificar frecuencia
        self.assertIn('frecuencia_fundamental', pred)
        self.assertEqual(pred['frecuencia_fundamental']['valor_esperado'], 141.7001)
        self.assertIn('criterio_falsacion', pred['frecuencia_fundamental'])
        
        # Verificar SNR
        self.assertIn('snr_h1', pred)
        self.assertGreater(pred['snr_h1']['minimo_esperado'], 0)
        self.assertIn('snr_l1', pred)
        self.assertGreater(pred['snr_l1']['minimo_esperado'], 0)
        
        # Verificar estadística bayesiana
        self.assertIn('estadistica_bayesiana', pred)
        self.assertEqual(pred['estadistica_bayesiana']['bayes_factor_minimo'], 10.0)
        
        # Verificar p-value
        self.assertIn('significancia_estadistica', pred)
        self.assertEqual(pred['significancia_estadistica']['p_value_maximo'], 0.01)
    
    def test_criterios_validacion(self):
        """Verificar que existen criterios claros de validación"""
        prediccion = generar_prediccion_gw250114()
        criterios = prediccion['criterios_validacion_global']
        
        self.assertIn('criterio_confirmacion', criterios)
        self.assertIn('criterio_refutacion', criterios)
        self.assertIn('criterio_inconclusivo', criterios)
        
        # Verificar que contienen lógica
        self.assertIn('BF', criterios['criterio_confirmacion'])
        self.assertIn('p', criterios['criterio_confirmacion'])
    
    def test_resultados_posibles(self):
        """Verificar que contempla todos los resultados posibles"""
        prediccion = generar_prediccion_gw250114()
        resultados = prediccion['resultados_posibles']
        
        # Debe tener los tres resultados posibles
        self.assertIn('CONFIRMADA', resultados)
        self.assertIn('REFUTADA', resultados)
        self.assertIn('INCONCLUSA', resultados)
        
        # Cada uno debe tener descripción, impacto y acción
        for resultado, info in resultados.items():
            self.assertIn('descripcion', info)
            self.assertIn('impacto', info)
            self.assertIn('accion', info)
    
    def test_guardar_prediccion(self):
        """Verificar que se puede guardar la predicción"""
        prediccion = generar_prediccion_gw250114()
        
        # Guardar en directorio temporal
        with tempfile.TemporaryDirectory() as tmpdir:
            json_file, md_file = guardar_prediccion(prediccion, tmpdir)
            
            # Verificar que se crearon los archivos
            self.assertTrue(os.path.exists(json_file))
            self.assertTrue(os.path.exists(md_file))
            
            # Verificar que el JSON es válido
            with open(json_file, 'r') as f:
                prediccion_loaded = json.load(f)
                self.assertEqual(prediccion_loaded['metadata']['evento_target'], 'GW250114')
            
            # Verificar que el markdown tiene contenido
            with open(md_file, 'r') as f:
                md_content = f.read()
                self.assertIn('PREDICCIÓN PÚBLICA', md_content)
                self.assertIn('141.7', md_content)
                self.assertIn('falsable', md_content.lower())


if __name__ == '__main__':
    unittest.main(verbosity=2)
