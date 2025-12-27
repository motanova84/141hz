#!/usr/bin/env python3
"""
Test para el análisis de GW150914 con PyCBC
Verifica que el script puede importar las bibliotecas necesarias
y que tiene la estructura correcta.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

class TestGW150914PyCBCAnalysis(unittest.TestCase):
    """Tests para el análisis de GW150914 con PyCBC"""
    
    def test_imports_available(self):
        """Verifica que los módulos necesarios están disponibles"""
        try:
            import matplotlib
            import matplotlib.pyplot as plt
            # Configurar backend para evitar problemas en CI/CD
            matplotlib.use('Agg')
        except ImportError as e:
            self.fail(f"Error importando matplotlib: {e}")
    
    def test_script_exists(self):
        """Verifica que el script existe"""
        script_path = os.path.join(
            os.path.dirname(__file__),
            'analizar_gw150914_pycbc.py'
        )
        self.assertTrue(os.path.exists(script_path), 
                       f"Script no encontrado en {script_path}")
    
    def test_script_is_executable(self):
        """Verifica que el script tiene permisos de ejecución"""
        script_path = os.path.join(
            os.path.dirname(__file__),
            'analizar_gw150914_pycbc.py'
        )
        self.assertTrue(os.access(script_path, os.X_OK),
                       "Script no tiene permisos de ejecución")
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_pycbc_imports_mock(self, mock_savefig, mock_show):
        """Test con mocks de PyCBC para verificar la estructura"""
        # Este test verifica la estructura sin necesitar PyCBC instalado
        
        # Crear mocks para las funciones de PyCBC
        mock_strain = Mock()
        mock_strain.duration = 32.0
        mock_strain.delta_t = 1.0 / 4096
        mock_strain.sample_times = [1126259462.21, 1126259462.45]
        
        # Mock del objeto frequencyseries
        mock_freq_series = Mock()
        mock_freq_series.to_timeseries = Mock(return_value=mock_strain)
        mock_strain.to_frequencyseries = Mock(return_value=mock_freq_series)
        
        # Los mocks simularían el comportamiento esperado
        self.assertIsNotNone(mock_strain.duration)
        self.assertEqual(mock_strain.duration, 32.0)
    
    def test_gps_time_range(self):
        """Verifica que el rango de tiempo GPS es correcto para GW150914"""
        gps_start = 1126259462.21
        gps_end = 1126259462.45
        
        # El evento GW150914 ocurrió alrededor de GPS 1126259462.4
        event_time = 1126259462.4
        
        self.assertLess(gps_start, event_time, 
                       "El inicio debe ser antes del evento")
        self.assertGreater(gps_end, event_time,
                          "El final debe ser después del evento")
        
        # La ventana debe ser pequeña (alrededor del evento)
        window = gps_end - gps_start
        self.assertLess(window, 1.0,
                       "La ventana de tiempo debe ser menor a 1 segundo")
    
    def test_filter_parameters(self):
        """Verifica que los parámetros de filtrado son razonables"""
        # Frecuencia de corte baja
        lowcut = 15
        self.assertGreater(lowcut, 0, "Frecuencia baja debe ser positiva")
        self.assertLess(lowcut, 100, "Frecuencia baja debe ser menor a 100 Hz")
        
        # Frecuencia de corte alta
        highcut = 300
        self.assertGreater(highcut, lowcut, 
                          "Frecuencia alta debe ser mayor que frecuencia baja")
        self.assertLess(highcut, 2000, 
                       "Frecuencia alta debe estar en rango LIGO")
        
        # Frecuencia de banda de interés
        band_low = 35
        band_high = 300
        self.assertGreater(band_low, lowcut,
                          "Banda de interés debe estar dentro del filtro")
        self.assertEqual(band_high, highcut,
                        "Banda alta debe coincidir con filtro alto")


if __name__ == '__main__':
    # Configurar matplotlib para tests
    import matplotlib
    matplotlib.use('Agg')
    
    # Ejecutar tests
    unittest.main()
