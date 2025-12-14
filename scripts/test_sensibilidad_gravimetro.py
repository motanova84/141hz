#!/usr/bin/env python3
"""
Test script para sensibilidad_gravimetro.py

Valida la lógica del análisis de sensibilidad sin ejecutar simulaciones completas.
Verifica que las funciones principales operan correctamente.
"""

import numpy as np
import sys
import os
import tempfile
from pathlib import Path

# Añadir el directorio scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from sensibilidad_gravimetro import simular_salida_gravimetro, ejecutar_analisis_sensibilidad

# Test constants
EXPECTED_SNR_AT_1E12 = 12.3  # Expected SNR for amplitude 1e-12 g
SNR_TOLERANCE = 3.0  # Tolerance for SNR comparison (accounts for stochastic variation)
LINEAR_SCALING_TOLERANCE = 0.2  # 20% tolerance for linear scaling check
MIN_DETECTION_RATE_AT_1E12 = 80.0  # Minimum detection rate (%) for 1e-12 g amplitude


def test_simular_salida_gravimetro():
    """Test: Simulación de salida del gravímetro genera SNR esperado."""
    print("\n[TEST] Simulación de salida del gravímetro...")
    
    # Probar con amplitud conocida
    amplitud = 1e-12  # g
    num_realizaciones = 100
    
    snrs = simular_salida_gravimetro(amplitud, num_realizaciones)
    
    # Verificaciones
    assert len(snrs) == num_realizaciones, "Debe generar número correcto de realizaciones"
    assert all(snr >= 0 for snr in snrs), "SNR no puede ser negativo"
    
    mean_snr = np.mean(snrs)
    
    assert abs(mean_snr - EXPECTED_SNR_AT_1E12) < SNR_TOLERANCE, \
        f"SNR medio ({mean_snr:.2f}) debe estar cerca de {EXPECTED_SNR_AT_1E12} ± {SNR_TOLERANCE}"
    
    print(f"  Amplitud: {amplitud:.2e} g")
    print(f"  SNR medio: {mean_snr:.2f}")
    print(f"  SNR esperado: {EXPECTED_SNR_AT_1E12:.2f}")
    print("✓ Simulación de salida: OK")


def test_escalamiento_snr():
    """Test: SNR debe escalar linealmente con la amplitud."""
    print("\n[TEST] Escalamiento lineal de SNR...")
    
    amplitudes = [1e-13, 5e-13, 1e-12]
    num_realizaciones = 50
    
    snrs_mean = []
    for amp in amplitudes:
        snrs = simular_salida_gravimetro(amp, num_realizaciones)
        snrs_mean.append(np.mean(snrs))
    
    # Verificar escalamiento lineal: SNR(a2)/SNR(a1) ≈ a2/a1
    ratio_snr = snrs_mean[1] / snrs_mean[0]
    ratio_amp = amplitudes[1] / amplitudes[0]
    
    assert abs(ratio_snr / ratio_amp - 1.0) < LINEAR_SCALING_TOLERANCE, \
        f"SNR debe escalar linealmente: ratio SNR={ratio_snr:.2f}, ratio amp={ratio_amp:.2f}"
    
    print(f"  Amplitudes: {amplitudes}")
    print(f"  SNR medios: {[f'{s:.2f}' for s in snrs_mean]}")
    print(f"  Ratio SNR / Ratio Amp: {ratio_snr/ratio_amp:.2f} (debe ≈ 1.0)")
    print("✓ Escalamiento lineal: OK")


def test_tasa_deteccion():
    """Test: Tasa de detección aumenta con amplitud."""
    print("\n[TEST] Tasa de detección vs amplitud...")
    
    umbral_snr = 5.0
    amplitudes = [1e-13, 1e-12]
    num_realizaciones = 100
    
    tasas_deteccion = []
    for amp in amplitudes:
        snrs = simular_salida_gravimetro(amp, num_realizaciones)
        tasa = np.mean(snrs > umbral_snr) * 100
        tasas_deteccion.append(tasa)
    
    # Verificar que la tasa aumenta con la amplitud
    assert tasas_deteccion[1] > tasas_deteccion[0], \
        "Tasa de detección debe aumentar con la amplitud"
    
    # Para 1e-12 g, debe ser alta (>80%)
    assert tasas_deteccion[1] > MIN_DETECTION_RATE_AT_1E12, \
        f"Tasa de detección para 1e-12 g debe ser >{MIN_DETECTION_RATE_AT_1E12}% (actual: {tasas_deteccion[1]:.1f}%)"
    
    print(f"  Amplitud {amplitudes[0]:.2e} g: {tasas_deteccion[0]:.1f}%")
    print(f"  Amplitud {amplitudes[1]:.2e} g: {tasas_deteccion[1]:.1f}%")
    print("✓ Tasa de detección: OK")


def test_analisis_completo():
    """Test: Análisis completo genera archivos esperados."""
    print("\n[TEST] Análisis completo...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Ejecutar análisis en directorio temporal
        results = ejecutar_analisis_sensibilidad(
            output_dir=tmpdir,
            save_plots=True,
            verbose=False
        )
        
        # Verificar que se generaron resultados
        assert results is not None, "Debe retornar resultados"
        assert len(results) > 0, "Debe tener al menos un resultado"
        
        # Verificar archivos generados
        output_path = Path(tmpdir)
        npz_file = output_path / 'sensibilidad_gravimetro.npz'
        json_file = output_path / 'sensibilidad_gravimetro.json'
        png_file = output_path / 'figures' / 'sensibilidad_gravimetro.png'
        
        assert npz_file.exists(), "Debe generar archivo .npz"
        assert json_file.exists(), "Debe generar archivo .json"
        assert png_file.exists(), "Debe generar archivo .png"
        
        # Verificar estructura de resultados
        for amp, res in results.items():
            assert 'SNR medio' in res, "Resultado debe incluir SNR medio"
            assert 'Tasa de detección (%)' in res, "Resultado debe incluir tasa de detección"
            assert res['SNR medio'] >= 0, "SNR medio debe ser no negativo"
            assert 0 <= res['Tasa de detección (%)'] <= 100, "Tasa debe estar en [0, 100]"
        
        print(f"  Archivos generados: {len(list(output_path.glob('**/*')))}")
        print(f"  Resultados: {len(results)} amplitudes")
        print("✓ Análisis completo: OK")


def run_all_tests():
    """Ejecuta todos los tests."""
    print("=" * 70)
    print("TEST SUITE: sensibilidad_gravimetro.py")
    print("=" * 70)
    
    tests = [
        test_simular_salida_gravimetro,
        test_escalamiento_snr,
        test_tasa_deteccion,
        test_analisis_completo
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: FAILED - {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: ERROR - {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"RESULTADOS: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
