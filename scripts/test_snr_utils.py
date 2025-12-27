#!/usr/bin/env python3
"""
Tests para el módulo snr_utils
===============================

Verifica que las funciones de formateo de SNR manejan correctamente
arrays de numpy y evitan el TypeError.
"""
import sys
import os

# Core dependency (numpy) assumed available
import numpy as np

try:
    import pytest
except ImportError:
    print("⚠️ pytest not installed, skipping tests")
    print("Install with: pip install pytest")
    sys.exit(0)

# Ajustar path antes de importar (necesario para imports locales)
sys.path.insert(0, os.path.dirname(__file__))

# Asegurar que podemos importar snr_utils
from snr_utils import (  # noqa: E402
    safe_format_snr,
    format_snr_string,
    calculate_snr_safe,
    print_snr_result
)


class TestSafeFormatSNR:
    """Tests para safe_format_snr"""
    
    def test_scalar_float(self):
        """Test con float escalar"""
        snr = 7.5
        result = safe_format_snr(snr)
        assert isinstance(result, float)
        assert abs(result - 7.5) < 1e-10
    
    def test_scalar_int(self):
        """Test con int escalar"""
        snr = 7
        result = safe_format_snr(snr)
        assert isinstance(result, float)
        assert abs(result - 7.0) < 1e-10
    
    def test_numpy_array_single_element(self):
        """Test con array de numpy con un solo elemento"""
        snr = np.array([7.5])
        result = safe_format_snr(snr)
        assert isinstance(result, float)
        assert abs(result - 7.5) < 1e-10
    
    def test_numpy_array_multiple_elements(self):
        """Test con array de numpy con múltiples elementos"""
        snr = np.array([7.5, 8.2, 6.3])
        result = safe_format_snr(snr)
        assert isinstance(result, float)
        assert abs(result - 7.5) < 1e-10  # Debe retornar el primer elemento
    
    def test_numpy_scalar(self):
        """Test con escalar de numpy (np.float64, etc.)"""
        snr = np.float64(7.5)
        result = safe_format_snr(snr)
        assert isinstance(result, float)
        assert abs(result - 7.5) < 1e-10
    
    def test_empty_array(self):
        """Test con array vacío"""
        snr = np.array([])
        result = safe_format_snr(snr)
        assert isinstance(result, float)
        assert result == 0.0
    
    def test_formatting_no_error(self):
        """Test que el resultado puede ser formateado sin error"""
        snr = np.array([7.5])
        result = safe_format_snr(snr)
        # Esto no debe lanzar TypeError
        formatted = f"{result:.2f}"
        assert formatted == "7.50"


class TestFormatSNRString:
    """Tests para format_snr_string"""
    
    def test_snr_only(self):
        """Test con solo valor de SNR"""
        snr = np.array([7.5])
        result = format_snr_string(snr)
        assert "7.50" in result
        assert "SNR" in result
    
    def test_snr_with_detector(self):
        """Test con detector especificado"""
        snr = 7.5
        result = format_snr_string(snr, detector='H1')
        assert "7.50" in result
        assert "H1" in result
    
    def test_snr_with_frequency(self):
        """Test con frecuencia especificada"""
        snr = 7.5
        result = format_snr_string(snr, frequency=141.7)
        assert "7.50" in result
        assert "141.70" in result
    
    def test_snr_with_detector_and_frequency(self):
        """Test con detector y frecuencia"""
        snr = np.array([7.5])
        result = format_snr_string(snr, detector='H1', frequency=141.7)
        assert "7.50" in result
        assert "H1" in result
        assert "141.70" in result
    
    def test_custom_decimals(self):
        """Test con número personalizado de decimales"""
        snr = 7.567
        result = format_snr_string(snr, decimals=3)
        assert "7.567" in result


class TestCalculateSNRSafe:
    """Tests para calculate_snr_safe"""
    
    def test_scalar_inputs(self):
        """Test con inputs escalares"""
        F_eff = 0.5
        h_rss = 1e-21
        Sn_f0 = 1e-46
        
        snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)
        
        # SNR = (0.5 * 1e-21) / sqrt(1e-46) = (0.5 * 1e-21) / 1e-23 = 50
        expected = (F_eff * h_rss) / np.sqrt(Sn_f0)
        assert abs(snr - expected) < 1e-10
    
    def test_array_inputs(self):
        """Test con inputs como arrays"""
        F_eff = np.array([0.5])
        h_rss = np.array([1e-21])
        Sn_f0 = np.array([1e-46])
        
        snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)
        
        assert isinstance(snr, np.ndarray)
        expected = (F_eff * h_rss) / np.sqrt(Sn_f0)
        assert np.abs(snr - expected).max() < 1e-10
    
    def test_mixed_inputs(self):
        """Test con inputs mixtos (escalares y arrays)"""
        F_eff = 0.5
        h_rss = np.array([1e-21])
        Sn_f0 = 1e-46
        
        snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)
        
        expected = (F_eff * h_rss) / np.sqrt(Sn_f0)
        assert np.abs(snr - expected).max() < 1e-10
    
    def test_result_can_be_formatted(self):
        """Test que el resultado puede ser formateado sin error"""
        F_eff = np.array([0.5])
        h_rss = np.array([1e-21])
        Sn_f0 = np.array([1e-46])
        
        snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)
        
        # Esto no debe lanzar TypeError
        formatted = f"{safe_format_snr(snr):.2f}"
        assert isinstance(formatted, str)


class TestPrintSNRResult:
    """Tests para print_snr_result"""
    
    def test_print_with_array(self, capsys):
        """Test impresión con array de numpy"""
        snr = np.array([7.5])
        print_snr_result(snr, 'H1', 141.7)
        
        captured = capsys.readouterr()
        assert "7.50" in captured.out
        assert "H1" in captured.out
        assert "141.70" in captured.out
    
    def test_print_with_scalar(self, capsys):
        """Test impresión con escalar"""
        snr = 8.2
        print_snr_result(snr, 'L1', 141.7)
        
        captured = capsys.readouterr()
        assert "8.20" in captured.out
        assert "L1" in captured.out
        assert "141.70" in captured.out
    
    def test_print_default_frequency(self, capsys):
        """Test impresión con frecuencia por defecto"""
        snr = 7.5
        print_snr_result(snr, 'H1')
        
        captured = capsys.readouterr()
        assert "141.70" in captured.out


class TestOriginalErrorCase:
    """Test que reproduce el error original del problem statement"""
    
    def test_original_error_pattern_fixed(self):
        """
        Test que reproduce el caso del error original:
        snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
        print(f"SNR esperada a 141.7 Hz en {ifo}: {snr:.2f}")
        
        Esto causaba: TypeError: unsupported format string passed to numpy.ndarray.__format__
        """
        # Simular el caso original
        F_eff = np.array([0.5])
        h_rss = np.array([1e-21])
        Sn_f0 = np.array([1e-46])
        ifo = "H1"
        
        # Cálculo SNR (esto produce un array)
        snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
        
        # Verificar que es un array (esto causaría el error)
        assert isinstance(snr, np.ndarray)
        
        # Solución 1: Usar safe_format_snr
        snr_safe = safe_format_snr(snr)
        formatted = f"SNR esperada a 141.7 Hz en {ifo}: {snr_safe:.2f}"
        assert "SNR esperada a 141.7 Hz en H1:" in formatted
        assert isinstance(formatted, str)
        
        # Solución 2: Usar print_snr_result
        # (no lanza error)
        print_snr_result(snr, ifo, 141.7)
        
        # Solución 3: Usar calculate_snr_safe + safe_format_snr
        snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)
        snr_safe = safe_format_snr(snr)
        formatted = f"SNR esperada a 141.7 Hz en {ifo}: {snr_safe:.2f}"
        assert isinstance(formatted, str)
    
    def test_original_error_would_fail(self):
        """
        Test que demuestra que el patrón original fallaría sin la corrección
        """
        # Simular el caso original
        F_eff = np.array([0.5])
        h_rss = np.array([1e-21])
        Sn_f0 = np.array([1e-46])
        
        snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
        
        # Esto causaría TypeError sin safe_format_snr
        with pytest.raises(TypeError):
            _ = f"{snr:.2f}"  # TypeError esperado


def test_integration_example():
    """
    Test de integración que muestra el uso completo del módulo
    """
    # Parámetros de ejemplo
    F_eff = np.array([0.5])
    h_rss = np.array([1e-21])
    Sn_f0 = np.array([1e-46])
    
    # Calcular SNR
    snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)
    
    # Formatear de varias formas
    snr_value = safe_format_snr(snr)
    assert isinstance(snr_value, float)
    
    snr_string = format_snr_string(snr, 'H1', 141.7)
    assert isinstance(snr_string, str)
    assert "H1" in snr_string
    
    # Imprimir (sin error)
    print_snr_result(snr, 'L1', 141.7)


if __name__ == "__main__":
    # Ejecutar tests con pytest
    pytest.main([__file__, "-v", "--tb=short"])
