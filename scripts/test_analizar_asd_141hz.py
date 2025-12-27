#!/usr/bin/env python3
"""
Tests para el script de análisis de ASD en 141.7 Hz
====================================================

Este script prueba las funciones del análisis de ASD implementado
en analizar_asd_141hz.py.

Uso:
    pytest scripts/test_analizar_asd_141hz.py
    python scripts/test_analizar_asd_141hz.py
"""

import os
import sys
import tempfile
from unittest.mock import Mock, patch

try:
    import pytest
    parametrize = pytest.mark.parametrize
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    # Define a no-op parametrize decorator for standalone execution
    def parametrize(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

try:
    import numpy as np
except ImportError:
    print("⚠️  numpy no disponible, algunos tests pueden fallar")
    np = None

# Importar el módulo a testear
sys.path.insert(0, os.path.dirname(__file__))
try:
    import analizar_asd_141hz as asd_module
except ImportError as e:
    print(f"❌ Error importando analizar_asd_141hz: {e}")
    print("   Asegúrate de que el archivo existe y las dependencias están instaladas")
    sys.exit(1)


class TestConstants:
    """Test de constantes del módulo."""
    
    def test_gw150914_gps_time(self):
        """Verificar que el tiempo GPS de GW150914 es correcto."""
        assert asd_module.GW150914_GPS_TIME == 1126259462.423
        
    def test_target_frequency(self):
        """Verificar que la frecuencia objetivo es 141.7 Hz."""
        assert asd_module.TARGET_FREQUENCY == 141.7


class TestDownloadSegment:
    """Tests para la función download_segment."""
    
    @patch('analizar_asd_141hz.TimeSeries')
    def test_download_segment_success(self, mock_timeseries):
        """Test descarga exitosa de segmento."""
        # Mock del TimeSeries
        mock_data = Mock()
        mock_data.sample_rate = 4096
        mock_data.__len__ = Mock(return_value=4096 * 64)
        mock_timeseries.fetch_open_data.return_value = mock_data
        
        result = asd_module.download_segment('H1', 1126259430, 64, verbose=False)
        
        assert result is not None
        mock_timeseries.fetch_open_data.assert_called_once()
        
    @patch('analizar_asd_141hz.TimeSeries')
    def test_download_segment_failure(self, mock_timeseries):
        """Test manejo de error en descarga."""
        mock_timeseries.fetch_open_data.side_effect = Exception("Network error")
        
        result = asd_module.download_segment('H1', 1126259430, 64, verbose=False)
        
        assert result is None


class TestCalculateASD:
    """Tests para la función calculate_asd."""
    
    def test_calculate_asd_with_mock_data(self):
        """Test cálculo de ASD con datos simulados."""
        # Crear TimeSeries mock con datos sintéticos
        sample_rate = 4096
        duration = 64
        times = np.arange(0, duration, 1/sample_rate)
        
        # Señal sintética: ruido + señal senoidal
        noise = np.random.normal(0, 1e-21, len(times))
        signal = 1e-20 * np.sin(2 * np.pi * 141.7 * times)
        data_values = noise + signal
        
        # Mock TimeSeries
        mock_data = Mock()
        mock_data.value = data_values
        mock_data.sample_rate = sample_rate
        mock_data.dt = 1/sample_rate
        
        # Mock del método asd
        mock_asd = Mock()
        mock_asd.frequencies = Mock()
        mock_asd.frequencies.__getitem__ = Mock(side_effect=lambda i: i * 0.25)
        mock_asd.frequencies.__len__ = Mock(return_value=1000)
        mock_asd.__len__ = Mock(return_value=1000)
        mock_data.asd = Mock(return_value=mock_asd)
        
        result = asd_module.calculate_asd(mock_data, fftlength=4, verbose=False)
        
        assert result is not None
        mock_data.asd.assert_called_once()
        
    def test_calculate_asd_error_handling(self):
        """Test manejo de errores en cálculo de ASD."""
        mock_data = Mock()
        mock_data.asd = Mock(side_effect=Exception("Calculation error"))
        
        result = asd_module.calculate_asd(mock_data, verbose=False)
        
        assert result is None


class TestExtractASDAtFrequency:
    """Tests para la función extract_asd_at_frequency."""
    
    def test_extract_exact_frequency(self):
        """Test extracción de ASD en frecuencia exacta."""
        # Crear FrequencySeries mock
        freqs = np.linspace(10, 500, 1000)
        asd_values = np.ones(1000) * 1e-23
        
        mock_asd = Mock()
        mock_asd.frequencies = Mock()
        mock_asd.frequencies.value = freqs
        mock_asd.value = asd_values
        
        exact_freq, asd_value = asd_module.extract_asd_at_frequency(
            mock_asd, 141.7, verbose=False
        )
        
        assert isinstance(exact_freq, (float, np.floating))
        assert isinstance(asd_value, (float, np.floating))
        assert abs(exact_freq - 141.7) < 1.0  # Debe estar cerca
        
    def test_extract_frequency_close_match(self):
        """Test que encuentra la frecuencia más cercana."""
        # Frecuencias que no incluyen exactamente 141.7
        freqs = np.array([140.0, 141.5, 142.0, 143.0])
        asd_values = np.array([1e-23, 2e-23, 3e-23, 4e-23])
        
        mock_asd = Mock()
        mock_asd.frequencies = Mock()
        mock_asd.frequencies.value = freqs
        mock_asd.value = asd_values
        
        exact_freq, asd_value = asd_module.extract_asd_at_frequency(
            mock_asd, 141.7, verbose=False
        )
        
        # Debe elegir 141.5 (más cercano)
        assert exact_freq == 141.5
        assert asd_value == 2e-23


class TestAnalyzeDetectorPair:
    """Tests para la función analyze_detector_pair."""
    
    @patch('analizar_asd_141hz.calculate_asd')
    @patch('analizar_asd_141hz.extract_asd_at_frequency')
    def test_analyze_detector_pair_success(self, mock_extract, mock_calc_asd):
        """Test análisis exitoso de par de detectores."""
        # Mock data
        mock_h1_data = Mock()
        mock_l1_data = Mock()
        
        # Mock ASD calculation
        mock_asd = Mock()
        mock_calc_asd.return_value = mock_asd
        
        # Mock frequency extraction
        mock_extract.side_effect = [
            (141.7, 1e-23),  # H1
            (141.7, 1.5e-23)  # L1
        ]
        
        result = asd_module.analyze_detector_pair(
            mock_h1_data, mock_l1_data, 64, verbose=False
        )
        
        assert result is not None
        assert 'h1' in result
        assert 'l1' in result
        assert 'comparison' in result
        assert result['h1']['asd_value'] == 1e-23
        assert result['l1']['asd_value'] == 1.5e-23
        assert result['comparison']['ratio_l1_h1'] == 1.5
        
    @patch('analizar_asd_141hz.calculate_asd')
    def test_analyze_detector_pair_h1_failure(self, mock_calc_asd):
        """Test manejo de error al calcular ASD de H1."""
        mock_h1_data = Mock()
        mock_l1_data = Mock()
        
        # H1 falla, L1 no se intenta
        mock_calc_asd.return_value = None
        
        result = asd_module.analyze_detector_pair(
            mock_h1_data, mock_l1_data, 64, verbose=False
        )
        
        assert result is None


class TestPlotASDComparison:
    """Tests para la función plot_asd_comparison."""
    
    def test_plot_generation(self):
        """Test que las gráficas se generan correctamente."""
        # Crear directorio temporal
        with tempfile.TemporaryDirectory() as tmpdir:
            # Crear resultados mock
            freqs = np.linspace(10, 500, 1000)
            asd_values = np.ones(1000) * 1e-23
            
            mock_asd = Mock()
            mock_asd.frequencies = freqs
            mock_asd.value = asd_values
            
            results = [{
                'label': 'Test',
                'h1': {
                    'asd': mock_asd,
                    'freq': 141.7,
                    'asd_value': 1e-23
                },
                'l1': {
                    'asd': mock_asd,
                    'freq': 141.7,
                    'asd_value': 1.5e-23
                },
                'comparison': {
                    'ratio_l1_h1': 1.5,
                    'diff_percent': 50.0
                }
            }]
            
            # Generar gráficas
            asd_module.plot_asd_comparison(results, tmpdir, verbose=False)
            
            # Verificar que se crearon los archivos
            assert os.path.exists(os.path.join(tmpdir, 'asd_comparison_full.png'))
            assert os.path.exists(os.path.join(tmpdir, 'asd_comparison_zoom.png'))
            assert os.path.exists(os.path.join(tmpdir, 'noise_ratio_comparison.png'))


class TestSaveResultsToFile:
    """Tests para la función save_results_to_file."""
    
    def test_save_results(self):
        """Test que los resultados se guardan correctamente."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = [{
                'label': 'Test',
                'gps_start': 1126259430.423,
                'duration': 64,
                'h1': {
                    'freq': 141.7,
                    'asd_value': 1e-23
                },
                'l1': {
                    'freq': 141.7,
                    'asd_value': 1.5e-23
                },
                'comparison': {
                    'ratio_l1_h1': 1.5,
                    'diff_percent': 50.0
                }
            }]
            
            asd_module.save_results_to_file(results, tmpdir, verbose=False)
            
            output_file = os.path.join(tmpdir, 'asd_results.txt')
            assert os.path.exists(output_file)
            
            # Verificar contenido
            with open(output_file, 'r') as f:
                content = f.read()
                assert '141.7' in content
                assert 'Test' in content
                assert '1.000000e-23' in content


class TestIntegration:
    """Tests de integración (requieren datos reales o mocks complejos)."""
    
    @patch('analizar_asd_141hz.download_segment')
    @patch('analizar_asd_141hz.analyze_detector_pair')
    @patch('analizar_asd_141hz.plot_asd_comparison')
    @patch('analizar_asd_141hz.save_results_to_file')
    def test_analyze_gw150914_full_workflow(self, mock_save, mock_plot, 
                                            mock_analyze, mock_download):
        """Test del workflow completo de análisis."""
        # Mock download
        mock_data = Mock()
        mock_download.return_value = mock_data
        
        # Mock analysis
        mock_result = {
            'label': 'GW150914',
            'h1': {'asd_value': 1e-23},
            'l1': {'asd_value': 1.5e-23},
            'comparison': {'ratio_l1_h1': 1.5}
        }
        mock_analyze.return_value = mock_result
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = asd_module.analyze_gw150914(
                duration=64,
                control_days=[1],
                output_dir=tmpdir,
                make_plots=True,
                verbose=False
            )
            
            assert result is not None
            assert 'all_results' in result
            assert len(result['all_results']) > 0


def run_tests():
    """Ejecutar tests manualmente sin pytest."""
    print("🧪 Ejecutando tests de analizar_asd_141hz.py...")
    print("=" * 70)
    
    test_classes = [
        TestConstants,
        TestDownloadSegment,
        TestCalculateASD,
        TestExtractASDAtFrequency,
        TestAnalyzeDetectorPair,
        TestPlotASDComparison,
        TestSaveResultsToFile,
        TestIntegration
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        print(f"\n📋 {test_class.__name__}")
        print("-" * 70)
        
        test_instance = test_class()
        test_methods = [m for m in dir(test_instance) if m.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            method = getattr(test_instance, method_name)
            
            try:
                method()
                print(f"  ✅ {method_name}")
                passed_tests += 1
            except Exception as e:
                print(f"  ❌ {method_name}: {e}")
                failed_tests += 1
    
    print("\n" + "=" * 70)
    print(f"📊 Resultados: {passed_tests}/{total_tests} tests pasaron")
    
    if failed_tests > 0:
        print(f"⚠️  {failed_tests} tests fallaron")
        return 1
    else:
        print("✅ Todos los tests pasaron")
        return 0


if __name__ == '__main__':
    # Si pytest está disponible, usarlo; si no, ejecutar manualmente
    if PYTEST_AVAILABLE:
        sys.exit(pytest.main([__file__, '-v']))
    else:
        print("⚠️  pytest no disponible, ejecutando tests manualmente")
        sys.exit(run_tests())
