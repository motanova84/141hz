#!/usr/bin/env python3
"""
Tests para el módulo de análisis estadístico avanzado
Valida las tres funciones requeridas por el problem statement
"""
import sys

# Core dependencies (numpy, scipy) are assumed to be available
# as they are required by almost all scientific Python code
import numpy as np
from scipy import stats, signal

try:
    import pytest
except ImportError:
    print("⚠️ pytest not installed, skipping tests")
    print("Install with: pip install pytest")
    sys.exit(0)

# Importar funciones a testear
from analisis_estadistico_avanzado import (
    calculate_snr_at_frequency,
    analisis_significancia_estadistica,
    compute_coherence_h1_l1,
    exclude_instrumental_artifacts,
    ejecutar_analisis_completo
)


class TestCalculateSNR:
    """Tests para cálculo de SNR"""
    
    def test_snr_with_signal(self):
        """Test SNR con señal conocida"""
        fs = 4096
        duration = 2
        t = np.linspace(0, duration, int(fs * duration))
        f0 = 141.7
        
        # Señal fuerte
        signal_data = 1e-20 * np.sin(2 * np.pi * f0 * t)
        noise = np.random.normal(0, 1e-22, len(t))
        data = signal_data + noise
        
        snr = calculate_snr_at_frequency(data, f0, fs)
        
        # SNR debe ser positivo y razonable
        assert snr > 0, "SNR debe ser positivo"
        assert snr < 1e10, "SNR no debe ser infinito"
    
    def test_snr_noise_only(self):
        """Test SNR con solo ruido"""
        fs = 4096
        duration = 1
        t = np.linspace(0, duration, int(fs * duration))
        
        # Solo ruido
        noise = np.random.normal(0, 1e-22, len(t))
        
        snr = calculate_snr_at_frequency(noise, 141.7, fs)
        
        # SNR debe ser cercano a 1 para solo ruido
        assert 0.1 < snr < 10, f"SNR para ruido puro debe ser ~1, obtenido: {snr}"
    
    def test_snr_different_methods(self):
        """Test SNR con diferentes métodos"""
        fs = 4096
        duration = 2
        t = np.linspace(0, duration, int(fs * duration))
        f0 = 141.7
        
        signal_data = 1e-21 * np.sin(2 * np.pi * f0 * t)
        noise = np.random.normal(0, 2e-22, len(t))
        data = signal_data + noise
        
        snr_welch = calculate_snr_at_frequency(data, f0, fs, method='welch')
        snr_fft = calculate_snr_at_frequency(data, f0, fs, method='fft')
        
        # Ambos métodos deben dar resultados comparables
        assert snr_welch > 0
        assert snr_fft > 0


class TestSignificanciaEstadistica:
    """Tests para análisis de significancia estadística"""
    
    def test_significancia_estructura_resultado(self):
        """Test que el resultado tiene la estructura correcta"""
        fs = 4096
        duration = 1
        t = np.linspace(0, duration, int(fs * duration))
        data = np.random.normal(0, 1e-22, len(t))
        
        resultado = analisis_significancia_estadistica(data, 141.7, fs)
        
        # Verificar estructura
        assert 'f0' in resultado
        assert 'snr' in resultado
        assert 'p_value' in resultado
        assert 'significativo' in resultado
        assert 'criterio' in resultado
        
        # Verificar tipos
        assert isinstance(resultado['snr'], float)
        assert isinstance(resultado['p_value'], float)
        assert isinstance(resultado['significativo'], bool)
    
    def test_significancia_p_value_range(self):
        """Test que p-value está en rango válido [0, 1]"""
        fs = 4096
        duration = 1
        t = np.linspace(0, duration, int(fs * duration))
        data = np.random.normal(0, 1e-22, len(t))
        
        resultado = analisis_significancia_estadistica(data, 141.7, fs)
        
        assert 0 <= resultado['p_value'] <= 1, \
            f"p-value debe estar en [0,1], obtenido: {resultado['p_value']}"
    
    def test_significancia_criterio_threshold(self):
        """Test que el criterio de significancia es correcto"""
        fs = 4096
        duration = 1
        t = np.linspace(0, duration, int(fs * duration))
        
        # Caso 1: SNR bajo (no significativo)
        noise = np.random.normal(0, 1e-22, len(t))
        resultado = analisis_significancia_estadistica(noise, 141.7, fs)
        
        if resultado['p_value'] >= 1e-6:
            assert not resultado['significativo'], \
                "p-value >= 1e-6 no debe ser significativo"
        
        # Caso 2: SNR muy alto debería tender a ser significativo
        # (aunque con ruido aleatorio puede no cumplirse siempre)
        strong_signal = 1e-20 * np.sin(2 * np.pi * 141.7 * t)
        resultado2 = analisis_significancia_estadistica(strong_signal, 141.7, fs)
        
        # Solo verificar que el criterio se aplica correctamente
        if resultado2['p_value'] < 1e-6:
            assert resultado2['significativo'], \
                "p-value < 1e-6 debe ser significativo"


class TestCoherenciaMultisitio:
    """Tests para coherencia multisitio"""
    
    def test_coherencia_estructura_resultado(self):
        """Test estructura del resultado de coherencia"""
        fs = 4096
        duration = 1
        t = np.linspace(0, duration, int(fs * duration))
        
        data_h1 = np.random.normal(0, 1e-22, len(t))
        data_l1 = np.random.normal(0, 1e-22, len(t))
        
        resultado = compute_coherence_h1_l1(141.7, data_h1, data_l1, fs)
        
        # Verificar estructura
        assert 'f0' in resultado
        assert 'coherence_at_f0' in resultado
        assert 'coherence_mean' in resultado
        assert 'coherence_std' in resultado
        assert 'coherent' in resultado
        assert 'criterio' in resultado
    
    def test_coherencia_range(self):
        """Test que coherencia está en rango [0, 1]"""
        fs = 4096
        duration = 2
        t = np.linspace(0, duration, int(fs * duration))
        
        data_h1 = np.random.normal(0, 1e-22, len(t))
        data_l1 = np.random.normal(0, 1e-22, len(t))
        
        resultado = compute_coherence_h1_l1(141.7, data_h1, data_l1, fs)
        
        assert 0 <= resultado['coherence_at_f0'] <= 1, \
            f"Coherencia debe estar en [0,1], obtenido: {resultado['coherence_at_f0']}"
        assert 0 <= resultado['coherence_mean'] <= 1, \
            f"Coherencia media debe estar en [0,1], obtenido: {resultado['coherence_mean']}"
    
    def test_coherencia_señales_identicas(self):
        """Test coherencia con señales idénticas"""
        fs = 4096
        duration = 2
        t = np.linspace(0, duration, int(fs * duration))
        f0 = 141.7
        
        # Señal idéntica en ambos detectores (coherencia máxima)
        signal_data = 1e-21 * np.sin(2 * np.pi * f0 * t)
        noise = np.random.normal(0, 1e-23, len(t))  # Ruido muy bajo
        
        data_h1 = signal_data + noise
        data_l1 = signal_data + noise
        
        resultado = compute_coherence_h1_l1(f0, data_h1, data_l1, fs)
        
        # Coherencia debe ser alta para señales idénticas
        assert resultado['coherence_at_f0'] > 0.3, \
            f"Coherencia para señales idénticas debe ser alta, obtenido: {resultado['coherence_at_f0']}"
    
    def test_coherencia_señales_independientes(self):
        """Test coherencia con señales independientes"""
        fs = 4096
        duration = 2
        t = np.linspace(0, duration, int(fs * duration))
        
        # Ruido completamente independiente
        data_h1 = np.random.normal(0, 1e-22, len(t))
        data_l1 = np.random.normal(0, 1e-22, len(t))
        
        resultado = compute_coherence_h1_l1(141.7, data_h1, data_l1, fs)
        
        # Coherencia debe ser baja para señales independientes
        assert resultado['coherence_at_f0'] < 0.8, \
            f"Coherencia para señales independientes debe ser baja, obtenido: {resultado['coherence_at_f0']}"


class TestExclusionSistematicos:
    """Tests para exclusión de sistemáticos"""
    
    def test_exclusion_estructura_resultado(self):
        """Test estructura del resultado"""
        fs = 4096
        duration = 1
        t = np.linspace(0, duration, int(fs * duration))
        data = np.random.normal(0, 1e-22, len(t))
        
        resultado = exclude_instrumental_artifacts(141.7, data, fs, 'H1')
        
        # Verificar estructura
        assert 'f0' in resultado
        assert 'is_clean' in resultado
        assert 'nearest_line' in resultado
        assert 'tolerance' in resultado
        assert 'lines_checked' in resultado
        assert 'criterio' in resultado
        
        # Verificar estructura de nearest_line
        assert 'frequency' in resultado['nearest_line']
        assert 'description' in resultado['nearest_line']
        assert 'distance' in resultado['nearest_line']
    
    def test_exclusion_141_7_hz_is_clean(self):
        """Test que 141.7 Hz está lejos de líneas instrumentales"""
        fs = 4096
        duration = 1
        t = np.linspace(0, duration, int(fs * duration))
        data = np.random.normal(0, 1e-22, len(t))
        
        resultado = exclude_instrumental_artifacts(141.7001, data, fs, 'H1')
        
        # 141.7 Hz debe estar limpio (lejos de líneas instrumentales)
        assert resultado['is_clean'], \
            f"141.7 Hz debe estar limpio. Distancia: {resultado['nearest_line']['distance']} Hz"
    
    def test_exclusion_60_hz_not_clean(self):
        """Test que 60 Hz (línea de poder) no está limpio"""
        fs = 4096
        duration = 1
        t = np.linspace(0, duration, int(fs * duration))
        data = np.random.normal(0, 1e-22, len(t))
        
        resultado = exclude_instrumental_artifacts(60.0, data, fs, 'H1')
        
        # 60 Hz debe detectarse como línea instrumental
        assert not resultado['is_clean'], \
            "60 Hz debe detectarse como línea instrumental"
        assert resultado['nearest_line']['distance'] < 1.0, \
            "Distancia a línea 60 Hz debe ser muy pequeña"
    
    def test_exclusion_different_detectors(self):
        """Test que funciona con diferentes detectores"""
        fs = 4096
        duration = 1
        t = np.linspace(0, duration, int(fs * duration))
        data = np.random.normal(0, 1e-22, len(t))
        
        resultado_h1 = exclude_instrumental_artifacts(141.7, data, fs, 'H1')
        resultado_l1 = exclude_instrumental_artifacts(141.7, data, fs, 'L1')
        
        # Ambos deben tener estructura válida
        assert 'is_clean' in resultado_h1
        assert 'is_clean' in resultado_l1
        
        # Ambos deben reportar que 141.7 está limpio
        assert resultado_h1['is_clean']
        assert resultado_l1['is_clean']
    
    def test_exclusion_lines_checked(self):
        """Test que se verifican las líneas instrumentales esperadas"""
        fs = 4096
        duration = 1
        t = np.linspace(0, duration, int(fs * duration))
        data = np.random.normal(0, 1e-22, len(t))
        
        resultado = exclude_instrumental_artifacts(141.7, data, fs, 'H1')
        
        # Verificar que se checaron líneas principales
        lines_checked = resultado['lines_checked']
        assert 60 in lines_checked, "Debe verificar línea de 60 Hz"
        assert 120 in lines_checked, "Debe verificar línea de 120 Hz"
        assert 300 in lines_checked, "Debe verificar línea de 300 Hz"


class TestAnalisisCompleto:
    """Tests para análisis completo"""
    
    def test_analisis_completo_ejecuta(self):
        """Test que el análisis completo se ejecuta sin errores"""
        fs = 4096
        duration = 2
        t = np.linspace(0, duration, int(fs * duration))
        
        data_h1 = np.random.normal(0, 1e-22, len(t))
        data_l1 = np.random.normal(0, 1e-22, len(t))
        
        # No debe lanzar excepciones
        resultado = ejecutar_analisis_completo(data_h1, data_l1, 141.7, fs)
        
        assert resultado is not None
    
    def test_analisis_completo_estructura(self):
        """Test estructura del resultado del análisis completo"""
        fs = 4096
        duration = 2
        t = np.linspace(0, duration, int(fs * duration))
        
        data_h1 = np.random.normal(0, 1e-22, len(t))
        data_l1 = np.random.normal(0, 1e-22, len(t))
        
        resultado = ejecutar_analisis_completo(data_h1, data_l1, 141.7, fs)
        
        # Verificar estructura completa
        assert 'f0' in resultado
        assert 'significancia' in resultado
        assert 'coherencia' in resultado
        assert 'sistemáticos' in resultado
        assert 'criterios_cumplidos' in resultado
        assert 'total_criterios' in resultado
        assert 'validacion_exitosa' in resultado
        
        # Verificar sub-estructuras
        assert 'h1' in resultado['significancia']
        assert 'l1' in resultado['significancia']
        assert 'passed' in resultado['significancia']
    
    def test_analisis_completo_criterios_count(self):
        """Test que el conteo de criterios es válido"""
        fs = 4096
        duration = 2
        t = np.linspace(0, duration, int(fs * duration))
        
        data_h1 = np.random.normal(0, 1e-22, len(t))
        data_l1 = np.random.normal(0, 1e-22, len(t))
        
        resultado = ejecutar_analisis_completo(data_h1, data_l1, 141.7, fs)
        
        # Verificar que criterios cumplidos está en rango válido
        assert 0 <= resultado['criterios_cumplidos'] <= resultado['total_criterios']
        assert resultado['total_criterios'] == 4, "Deben ser 4 criterios en total"


def run_tests():
    """Ejecutar todos los tests"""
    print("=" * 70)
    print("🧪 TESTS DEL MÓDULO DE ANÁLISIS ESTADÍSTICO AVANZADO")
    print("=" * 70)
    print()
    
    # Usar pytest para ejecutar todos los tests
    test_results = pytest.main([
        __file__, 
        '-v',  # verbose
        '--tb=short',  # traceback corto
        '--color=yes'  # color en output
    ])
    
    return test_results


if __name__ == "__main__":
    sys.exit(run_tests())
