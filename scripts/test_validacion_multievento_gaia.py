#!/usr/bin/env python3
"""
Test Suite para Validación Multi-evento + GAIA
===============================================

Tests unitarios para validar el correcto funcionamiento del
análisis multi-evento con comparación GAIA.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Noviembre 2025
"""

import unittest
import numpy as np
import pandas as pd
from pathlib import Path
import json
import sys
import os

# Importar el módulo a testear
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validacion_multievento_gaia import ValidacionMultieventoGaia


class TestValidacionMultieventoGaia(unittest.TestCase):
    """Tests para la clase ValidacionMultieventoGaia"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.validacion = ValidacionMultieventoGaia(f0=141.7001, tolerancia=0.6)
        self.temp_dir = Path('temp_test_output')
        self.temp_dir.mkdir(exist_ok=True)
    
    def tearDown(self):
        """Limpieza después de cada test"""
        # Limpiar archivos temporales
        if self.temp_dir.exists():
            for file in self.temp_dir.glob('*'):
                file.unlink()
            self.temp_dir.rmdir()
    
    def test_inicializacion(self):
        """Test de inicialización correcta de la clase"""
        self.assertEqual(self.validacion.f0, 141.7001)
        self.assertEqual(self.validacion.tolerancia, 0.6)
        self.assertEqual(len(self.validacion.eventos), 5)
        self.assertIn('Δf', self.validacion.eventos.columns)
    
    def test_eventos_data_structure(self):
        """Test de estructura correcta de datos de eventos"""
        eventos = self.validacion.eventos
        
        # Verificar columnas necesarias
        self.assertIn('Evento', eventos.columns)
        self.assertIn('f_pico', eventos.columns)
        self.assertIn('Δf', eventos.columns)
        
        # Verificar tipos de datos
        self.assertTrue(pd.api.types.is_string_dtype(eventos['Evento']))
        self.assertTrue(pd.api.types.is_numeric_dtype(eventos['f_pico']))
        self.assertTrue(pd.api.types.is_numeric_dtype(eventos['Δf']))
        
        # Verificar nombres de eventos
        expected_events = [
            'GW240109_050431',
            'GW240107_013215',
            'GW240105_151143',
            'GW240104_164932',
            'GW231231_154016'
        ]
        self.assertListEqual(eventos['Evento'].tolist(), expected_events)
    
    def test_calculo_delta_f(self):
        """Test de cálculo correcto de Δf"""
        eventos = self.validacion.eventos
        
        # Verificar que Δf se calcula correctamente
        for idx, row in eventos.iterrows():
            expected_delta = row['f_pico'] - self.validacion.f0
            self.assertAlmostEqual(row['Δf'], expected_delta, places=6)
    
    def test_calcular_estadisticas(self):
        """Test de cálculo de estadísticas"""
        resumen = self.validacion.calcular_estadisticas()
        
        # Verificar estructura del DataFrame
        self.assertIsInstance(resumen, pd.DataFrame)
        self.assertIn('Estadístico', resumen.columns)
        self.assertIn('Valor', resumen.columns)
        
        # Verificar que contiene todos los estadísticos necesarios
        estadisticos_esperados = [
            'Media Δf (Hz)',
            'Desviación estándar (Hz)',
            'IC 95% inferior (Hz)',
            'IC 95% superior (Hz)',
            't-statistic',
            'p-value',
            'Tamaño muestra',
            'Frecuencia referencia f₀ (Hz)'
        ]
        
        for est in estadisticos_esperados:
            self.assertIn(est, resumen['Estadístico'].values)
        
        # Verificar valores numéricos razonables
        media = resumen.loc[resumen['Estadístico'] == 'Media Δf (Hz)', 'Valor'].values[0]
        std = resumen.loc[resumen['Estadístico'] == 'Desviación estándar (Hz)', 'Valor'].values[0]
        n = resumen.loc[resumen['Estadístico'] == 'Tamaño muestra', 'Valor'].values[0]
        
        self.assertIsInstance(media, (int, float))
        self.assertIsInstance(std, (int, float))
        self.assertEqual(n, 5)
        self.assertGreater(std, 0)  # La desviación estándar debe ser positiva
    
    def test_comparacion_gaia(self):
        """Test de comparación con frecuencia GAIA"""
        comparacion = self.validacion.comparacion_gaia()
        
        # Verificar estructura del diccionario
        self.assertIn('f_gaia', comparacion)
        self.assertIn('tolerancia_hz', comparacion)
        self.assertIn('coincidencias', comparacion)
        self.assertIn('total_eventos', comparacion)
        self.assertIn('porcentaje_coincidencias', comparacion)
        self.assertIn('eventos_coincidentes', comparacion)
        
        # Verificar valores
        self.assertEqual(comparacion['f_gaia'], 141.7001)
        self.assertEqual(comparacion['tolerancia_hz'], 0.6)
        self.assertEqual(comparacion['total_eventos'], 5)
        self.assertGreaterEqual(comparacion['coincidencias'], 0)
        self.assertLessEqual(comparacion['coincidencias'], 5)
        self.assertGreaterEqual(comparacion['porcentaje_coincidencias'], 0)
        self.assertLessEqual(comparacion['porcentaje_coincidencias'], 100)
        self.assertIsInstance(comparacion['eventos_coincidentes'], list)
    
    def test_calculo_coincidencias(self):
        """Test de cálculo correcto de coincidencias"""
        comparacion = self.validacion.comparacion_gaia()
        
        # Contar manualmente las coincidencias
        coincidencias_manual = 0
        for idx, row in self.validacion.eventos.iterrows():
            if abs(row['Δf']) < self.validacion.tolerancia:
                coincidencias_manual += 1
        
        self.assertEqual(comparacion['coincidencias'], coincidencias_manual)
        
        # Verificar porcentaje
        porcentaje_esperado = 100 * coincidencias_manual / 5
        self.assertAlmostEqual(
            comparacion['porcentaje_coincidencias'], 
            porcentaje_esperado, 
            places=2
        )
    
    def test_exportar_resultados(self):
        """Test de exportación de resultados"""
        archivos = self.validacion.exportar_resultados(self.temp_dir)
        
        # Verificar que devuelve un diccionario con las rutas
        self.assertIn('eventos', archivos)
        self.assertIn('resumen', archivos)
        self.assertIn('gaia', archivos)
        
        # Verificar que los archivos existen
        self.assertTrue(archivos['eventos'].exists())
        self.assertTrue(archivos['resumen'].exists())
        self.assertTrue(archivos['gaia'].exists())
        
        # Verificar contenido del CSV de eventos
        eventos_df = pd.read_csv(archivos['eventos'])
        self.assertEqual(len(eventos_df), 5)
        self.assertIn('Evento', eventos_df.columns)
        self.assertIn('f_pico', eventos_df.columns)
        self.assertIn('Δf', eventos_df.columns)
        
        # Verificar contenido del CSV de resumen
        resumen_df = pd.read_csv(archivos['resumen'])
        self.assertGreater(len(resumen_df), 0)
        self.assertIn('Estadístico', resumen_df.columns)
        self.assertIn('Valor', resumen_df.columns)
        
        # Verificar contenido del JSON de GAIA
        with open(archivos['gaia'], 'r') as f:
            gaia_data = json.load(f)
        self.assertIn('f_gaia', gaia_data)
        self.assertIn('coincidencias', gaia_data)
    
    def test_generar_visualizacion(self):
        """Test de generación de visualización"""
        plot_file = self.validacion.generar_visualizacion(self.temp_dir)
        
        # Verificar que el archivo existe
        self.assertTrue(plot_file.exists())
        self.assertEqual(plot_file.suffix, '.png')
        
        # Verificar que el archivo tiene contenido (no está vacío)
        self.assertGreater(plot_file.stat().st_size, 1000)
    
    def test_valores_especificos_eventos(self):
        """Test de valores específicos de los eventos O4"""
        eventos = self.validacion.eventos
        
        # Verificar valores conocidos
        gw240109 = eventos.loc[eventos['Evento'] == 'GW240109_050431']
        self.assertAlmostEqual(gw240109['f_pico'].values[0], 140.95, places=2)
        
        gw240107 = eventos.loc[eventos['Evento'] == 'GW240107_013215']
        self.assertAlmostEqual(gw240107['f_pico'].values[0], 140.77, places=2)
        
        gw240105 = eventos.loc[eventos['Evento'] == 'GW240105_151143']
        self.assertAlmostEqual(gw240105['f_pico'].values[0], 141.20, places=2)
    
    def test_intervalo_confianza(self):
        """Test de cálculo correcto del intervalo de confianza"""
        resumen = self.validacion.calcular_estadisticas()
        
        ic_inf = resumen.loc[resumen['Estadístico'] == 'IC 95% inferior (Hz)', 'Valor'].values[0]
        ic_sup = resumen.loc[resumen['Estadístico'] == 'IC 95% superior (Hz)', 'Valor'].values[0]
        media = resumen.loc[resumen['Estadístico'] == 'Media Δf (Hz)', 'Valor'].values[0]
        
        # El IC inferior debe ser menor que el superior
        self.assertLess(ic_inf, ic_sup)
        
        # La media debe estar dentro del IC
        self.assertGreaterEqual(media, ic_inf)
        self.assertLessEqual(media, ic_sup)
    
    def test_test_t_student(self):
        """Test de estadístico t y p-value"""
        resumen = self.validacion.calcular_estadisticas()
        
        t_stat = resumen.loc[resumen['Estadístico'] == 't-statistic', 'Valor'].values[0]
        p_value = resumen.loc[resumen['Estadístico'] == 'p-value', 'Valor'].values[0]
        
        # Verificar que son valores numéricos válidos
        self.assertIsInstance(t_stat, (int, float))
        self.assertIsInstance(p_value, (int, float))
        
        # p-value debe estar entre 0 y 1
        self.assertGreaterEqual(p_value, 0)
        self.assertLessEqual(p_value, 1)


class TestIntegracion(unittest.TestCase):
    """Tests de integración para el flujo completo"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.temp_dir = Path('temp_integration_test')
        self.temp_dir.mkdir(exist_ok=True)
    
    def tearDown(self):
        """Limpieza después de cada test"""
        if self.temp_dir.exists():
            for file in self.temp_dir.glob('*'):
                file.unlink()
            self.temp_dir.rmdir()
    
    def test_flujo_completo(self):
        """Test del flujo completo de análisis"""
        # Crear validación
        validacion = ValidacionMultieventoGaia()
        
        # Exportar resultados
        archivos = validacion.exportar_resultados(self.temp_dir)
        
        # Generar visualización
        plot_file = validacion.generar_visualizacion(self.temp_dir)
        
        # Verificar que todos los archivos se crearon
        self.assertTrue(archivos['eventos'].exists())
        self.assertTrue(archivos['resumen'].exists())
        self.assertTrue(archivos['gaia'].exists())
        self.assertTrue(plot_file.exists())
        
        # Verificar coherencia entre archivos
        eventos_df = pd.read_csv(archivos['eventos'])
        resumen_df = pd.read_csv(archivos['resumen'])
        
        with open(archivos['gaia'], 'r') as f:
            gaia_data = json.load(f)
        
        # El número de eventos debe ser consistente
        n_eventos_csv = len(eventos_df)
        n_eventos_resumen = resumen_df.loc[
            resumen_df['Estadístico'] == 'Tamaño muestra', 'Valor'
        ].values[0]
        n_eventos_gaia = gaia_data['total_eventos']
        
        self.assertEqual(n_eventos_csv, n_eventos_resumen)
        self.assertEqual(n_eventos_csv, n_eventos_gaia)


def run_tests():
    """Ejecuta todos los tests y muestra resultados"""
    print()
    print("=" * 70)
    print("   TEST SUITE: VALIDACIÓN MULTI-EVENTO + GAIA")
    print("=" * 70)
    print()
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar casos de test
    suite.addTests(loader.loadTestsFromTestCase(TestValidacionMultieventoGaia))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracion))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✅ TODOS LOS TESTS PASARON")
        print(f"   Total: {result.testsRun} tests")
        print(f"   Errores: {len(result.errors)}")
        print(f"   Fallos: {len(result.failures)}")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print(f"   Total: {result.testsRun} tests")
        print(f"   Errores: {len(result.errors)}")
        print(f"   Fallos: {len(result.failures)}")
    print("=" * 70)
    print()
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
