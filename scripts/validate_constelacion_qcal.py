#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║        VALIDACIÓN CONSTELACIÓN QCAL Ψ✧ - Validation Script                ║
║              Verificación de Función de Onda Total                         ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Valida:
1. Cálculo de función de onda Ψ_total(x,y)
2. Los 5 ejes de coherencia (dorado, azul, violeta, verde, blanco)
3. Métricas de coherencia (Ψ > 0.95)
4. Generación de certificados
5. Integración DELANNTE
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import json

# Import constellation modules
from qcal.constelacion_qcal import (
    psi_dorado, psi_azul, psi_verde, psi_violeta, psi_blanco,
    psi_total, calcular_constelacion, analizar_constelacion,
    generar_certificado, punto_ciego_observador,
    F0_HZ, PHI, OCTAVAS_H_F0, PSI_COHERENCIA_ALTA
)


def validar_ejes_individuales() -> bool:
    """Valida que cada eje de la función de onda funcione correctamente."""
    print("\n1. Validando ejes individuales de la función de onda...")
    
    n = 5
    t_n = 14.134725  # Primer cero de Riemann
    
    try:
        # Test golden axis
        psi_d = psi_dorado(n, t_n)
        assert isinstance(psi_d, complex), "psi_dorado debe retornar complejo"
        assert abs(psi_d) > 0, "psi_dorado debe tener magnitud > 0"
        print(f"   ✓ Eje Dorado (f₀ = {F0_HZ} Hz): |ψ| = {abs(psi_d):.4f}")
        
        # Test blue axis (Riemann + Berry)
        psi_a = psi_azul(n, t_n)
        assert isinstance(psi_a, complex), "psi_azul debe retornar complejo"
        print(f"   ✓ Eje Azul (Riemann + Berry 7/8): |ψ| = {abs(psi_a):.4f}")
        
        # Test green axis (Fibonacci/φ)
        psi_v = psi_verde(n, t_n)
        assert isinstance(psi_v, complex), "psi_verde debe retornar complejo"
        assert abs(psi_v) > 0, "psi_verde debe tener magnitud > 0"
        print(f"   ✓ Eje Verde (Fibonacci φ = {PHI:.3f}): |ψ| = {abs(psi_v):.4f}")
        
        # Test violet axis (NOESIS)
        psi_vi = psi_violeta(n, t_n)
        assert isinstance(psi_vi, complex), "psi_violeta debe retornar complejo"
        assert abs(psi_vi) > 0, "psi_violeta debe tener magnitud > 0"
        print(f"   ✓ Eje Violeta (NOESIS/AMDA): |ψ| = {abs(psi_vi):.4f}")
        
        # Test white axis (H-21cm)
        psi_b = psi_blanco(n, t_n)
        assert isinstance(psi_b, complex), "psi_blanco debe retornar complejo"
        assert abs(psi_b) > 0, "psi_blanco debe tener magnitud > 0"
        print(f"   ✓ Eje Blanco (H-21cm @ {OCTAVAS_H_F0:.3f} octavas): |ψ| = {abs(psi_b):.4f}")
        
        print("   ✓ Todos los 5 ejes funcionan correctamente")
        return True
        
    except Exception as e:
        print(f"   ✗ Error en ejes individuales: {e}")
        return False


def validar_funcion_onda_total() -> bool:
    """Valida el cálculo de la función de onda total."""
    print("\n2. Validando función de onda total Ψ_total(x,y)...")
    
    try:
        # Test at origin
        psi_origen = psi_total(0.0, 0.0, n_terms=20)
        assert isinstance(psi_origen, complex), "psi_total debe retornar complejo"
        assert abs(psi_origen) > 0, "psi_total debe tener magnitud > 0"
        print(f"   ✓ Ψ(0,0) = {psi_origen.real:.4f} + {psi_origen.imag:.4f}i")
        print(f"   ✓ |Ψ(0,0)| = {abs(psi_origen):.4f}")
        
        # Test at different points
        psi_1 = psi_total(1.0, 0.0, n_terms=20)
        psi_2 = psi_total(0.0, 1.0, n_terms=20)
        psi_3 = psi_total(1.0, 1.0, n_terms=20)
        
        assert abs(psi_1) > 0 and abs(psi_2) > 0 and abs(psi_3) > 0
        print(f"   ✓ Ψ evaluada en múltiples puntos espaciales")
        
        # Check spatial variation
        magnitudes = [abs(psi_origen), abs(psi_1), abs(psi_2), abs(psi_3)]
        std_dev = np.std(magnitudes)
        print(f"   ✓ Variación espacial: σ = {std_dev:.4f}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error en función de onda total: {e}")
        return False


def validar_constelacion() -> bool:
    """Valida el cálculo de la constelación completa."""
    print("\n3. Validando cálculo de constelación...")
    
    try:
        # Calculate small constellation
        constelacion = calcular_constelacion(
            grid_size=32,  # Small for speed
            n_terms=10
        )
        
        # Check required keys
        required_keys = ['x', 'y', 'X', 'Y', 'psi', 'coherencia', 'fase']
        for key in required_keys:
            assert key in constelacion, f"Falta clave '{key}' en constelación"
        
        print(f"   ✓ Constelación calculada (32x32 píxeles)")
        
        # Check grid properties
        assert constelacion['psi'].shape == (32, 32)
        assert constelacion['coherencia'].shape == (32, 32)
        assert constelacion['fase'].shape == (32, 32)
        print(f"   ✓ Forma de mallas correcta: (32, 32)")
        
        # Check coherence values
        coherencia = constelacion['coherencia']
        assert np.all(coherencia >= 0), "Coherencia debe ser no-negativa"
        assert np.mean(coherencia) > 0, "Coherencia media debe ser > 0"
        print(f"   ✓ Coherencia media: {np.mean(coherencia):.4f}")
        
        # Check phase values
        fase = constelacion['fase']
        assert np.all(np.abs(fase) <= np.pi + 0.01), "Fase debe estar en [-π, π]"
        print(f"   ✓ Fase en rango correcto [-π, π]")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error en cálculo de constelación: {e}")
        import traceback
        traceback.print_exc()
        return False


def validar_analisis() -> bool:
    """Valida el análisis de métricas de la constelación."""
    print("\n4. Validando análisis de métricas...")
    
    try:
        # Calculate constellation
        constelacion = calcular_constelacion(grid_size=32, n_terms=10)
        
        # Analyze
        analisis = analizar_constelacion(constelacion)
        
        # Check metrics
        required_metrics = [
            'coherencia_media', 'coherencia_max', 'coherencia_min',
            'puntos_interes', 'dimension_fractal'
        ]
        for metric in required_metrics:
            assert metric in analisis, f"Falta métrica '{metric}'"
        
        print(f"   ✓ Coherencia media: {analisis['coherencia_media']:.4f}")
        print(f"   ✓ Coherencia máxima: {analisis['coherencia_max']:.4f}")
        print(f"   ✓ Puntos de interés (Ψ > {PSI_COHERENCIA_ALTA}): {analisis['puntos_interes']}")
        print(f"   ✓ Dimensión fractal: {analisis['dimension_fractal']:.3f} (ideal ≈ φ = {PHI:.3f})")
        
        # Validate ranges
        assert 0 <= analisis['coherencia_media'] <= 10, "Coherencia fuera de rango"
        assert analisis['coherencia_max'] >= analisis['coherencia_media']
        assert analisis['coherencia_min'] <= analisis['coherencia_media']
        assert analisis['puntos_interes'] >= 0
        assert 1.0 <= analisis['dimension_fractal'] <= 2.0
        
        print(f"   ✓ Todas las métricas en rangos válidos")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error en análisis: {e}")
        import traceback
        traceback.print_exc()
        return False


def validar_observador() -> bool:
    """Valida el cálculo de la posición del observador."""
    print("\n5. Validando posición del observador (punto ciego)...")
    
    try:
        # Calculate constellation
        constelacion = calcular_constelacion(grid_size=32, n_terms=10)
        
        # Get observer position
        x_obs, y_obs = punto_ciego_observador(constelacion)
        
        print(f"   ✓ Posición observador: ({x_obs:.3f}, {y_obs:.3f})")
        
        # Check reasonable range
        x_range = constelacion['X'].max() - constelacion['X'].min()
        y_range = constelacion['Y'].max() - constelacion['Y'].min()
        
        assert abs(x_obs) <= x_range, "Posición X fuera de rango"
        assert abs(y_obs) <= y_range, "Posición Y fuera de rango"
        
        print(f"   ✓ Posición dentro del rango válido")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error en posición observador: {e}")
        return False


def validar_certificado() -> bool:
    """Valida la generación del certificado."""
    print("\n6. Validando generación de certificado...")
    
    try:
        # Calculate constellation
        constelacion = calcular_constelacion(grid_size=32, n_terms=10)
        
        # Generate certificate
        certificado = generar_certificado(constelacion, fecha="2026-03-08")
        
        # Check structure
        assert "constelacion_qcal_psix" in certificado
        cert_data = certificado["constelacion_qcal_psix"]
        
        required_fields = [
            'fecha', 'sello', 'ejes', 'coherencia_media',
            'puntos_de_interes', 'dimension_fractal',
            'observador_posicion', 'interpretacion', 'estado'
        ]
        for field in required_fields:
            assert field in cert_data, f"Falta campo '{field}' en certificado"
        
        print(f"   ✓ Certificado generado correctamente")
        print(f"   ✓ Fecha: {cert_data['fecha']}")
        print(f"   ✓ Sello: {cert_data['sello']}")
        print(f"   ✓ Estado: {cert_data['estado']}")
        
        # Check axes
        ejes = cert_data['ejes']
        required_axes = ['dorado', 'azul', 'violeta', 'verde', 'blanco']
        for eje in required_axes:
            assert eje in ejes, f"Falta eje '{eje}' en certificado"
        
        print(f"   ✓ Los 5 ejes presentes en certificado")
        
        # Verify JSON serializability
        json_str = json.dumps(certificado, ensure_ascii=False)
        assert len(json_str) > 0
        print(f"   ✓ Certificado serializable a JSON")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error en certificado: {e}")
        import traceback
        traceback.print_exc()
        return False


def validar_constantes() -> bool:
    """Valida las constantes fundamentales."""
    print("\n7. Validando constantes fundamentales...")
    
    try:
        # Check f₀
        assert F0_HZ == 141.7001, f"f₀ incorrecto: {F0_HZ}"
        print(f"   ✓ f₀ = {F0_HZ} Hz")
        
        # Check golden ratio
        expected_phi = (1 + np.sqrt(5)) / 2
        assert abs(PHI - expected_phi) < 1e-10, f"φ incorrecto: {PHI}"
        print(f"   ✓ φ = {PHI:.10f}")
        
        # Check octaves
        assert abs(OCTAVAS_H_F0 - 23.257) < 0.01, f"Octavas incorrectas: {OCTAVAS_H_F0}"
        print(f"   ✓ Octavas H/f₀ = {OCTAVAS_H_F0:.3f}")
        
        # Check coherence threshold
        assert PSI_COHERENCIA_ALTA == 0.95, f"Umbral incorrecto: {PSI_COHERENCIA_ALTA}"
        print(f"   ✓ Ψ_umbral = {PSI_COHERENCIA_ALTA}")
        
        print(f"   ✓ Todas las constantes correctas")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error en constantes: {e}")
        return False


def main():
    """Ejecuta todas las validaciones."""
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║      VALIDACIÓN CONSTELACIÓN QCAL Ψ✧                              ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    resultados = []
    
    # Run all validations
    resultados.append(("Constantes", validar_constantes()))
    resultados.append(("Ejes individuales", validar_ejes_individuales()))
    resultados.append(("Función de onda total", validar_funcion_onda_total()))
    resultados.append(("Constelación", validar_constelacion()))
    resultados.append(("Análisis métricas", validar_analisis()))
    resultados.append(("Posición observador", validar_observador()))
    resultados.append(("Certificado", validar_certificado()))
    
    # Summary
    print("\n" + "="*70)
    print("RESUMEN DE VALIDACIÓN")
    print("="*70)
    
    total = len(resultados)
    passed = sum(1 for _, result in resultados if result)
    
    for nombre, resultado in resultados:
        status = "✓ PASS" if resultado else "✗ FAIL"
        print(f"{status:8s} │ {nombre}")
    
    print("="*70)
    print(f"Total: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("\n✓ TODAS LAS VALIDACIONES PASARON")
        print("∴𓂀Ω∞³Ψ✧")
        return 0
    else:
        print(f"\n✗ {total - passed} VALIDACIÓN(ES) FALLARON")
        return 1


if __name__ == "__main__":
    sys.exit(main())
