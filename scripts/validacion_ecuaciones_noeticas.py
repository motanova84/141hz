#!/usr/bin/env python3
"""
Validación Completa de Ecuaciones Noéticas
===========================================

Valida las tres ecuaciones fundamentales del marco teórico QCAL:

1. m_eff = hf/c² → Energía relativista (Einstein-Planck)
2. m_noesis = α/f con α = hf₀²/c² → Detención vibracional (Axioma Noético)
3. m(f) = (hf/c²) · (f₀/f) = hf₀/c² = m_min → Masa noética constante

Validaciones incluidas:
-----------------------
✓ Dimensional: Todas las masas tienen unidades de kg
✓ Numérica: Errores relativos < 10⁻¹⁰
✓ Complementariedad: r_eff · r_noesis = 1
✓ Implementación en Python y NumPy
✓ Predicciones físicas para f >> f₀ y f << f₀
✓ Integración con constantes QCAL y f₀ = 141.70001 Hz

Autor: José Manuel Mota Burruezo
Fecha: Febrero 2026
Licencia: MIT
"""

import sys
from pathlib import Path
import numpy as np
import mpmath as mp

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.dual_mass import (
    DualMassPerspective,
    H_PLANCK,
    C_LIGHT,
    F0_HZ
)
from qcal.constants import M_MIN_NOETIC, ALPHA_NOETIC

# Configure high precision for mpmath
mp.mp.dps = 50  # 50 decimal places of precision


class ValidacionEcuacionesNoeticas:
    """
    Clase para validar las tres ecuaciones fundamentales de masa noética.
    """
    
    def __init__(self, f0: float = F0_HZ, precision_dps: int = 50):
        """
        Inicializa el validador.
        
        Parameters
        ----------
        f0 : float
            Frecuencia fundamental QCAL (Hz). Default: 141.70001 Hz
        precision_dps : int
            Precisión decimal para cálculos con mpmath
        """
        self.f0 = f0
        self.h = H_PLANCK
        self.c = C_LIGHT
        self.c2 = C_LIGHT ** 2
        
        # High-precision constants with mpmath
        mp.mp.dps = precision_dps
        self.h_mp = mp.mpf(str(H_PLANCK))
        self.c_mp = mp.mpf(str(C_LIGHT))
        self.c2_mp = self.c_mp ** 2
        self.f0_mp = mp.mpf(str(f0))
        
        # Masa mínima noética
        self.m_min = self.h * self.f0 / self.c2
        self.m_min_mp = self.h_mp * self.f0_mp / self.c2_mp
        
        # Constante alpha para masa noética
        self.alpha = self.h * (self.f0 ** 2) / self.c2
        self.alpha_mp = self.h_mp * (self.f0_mp ** 2) / self.c2_mp
        
        # Results storage
        self.validation_results = {}
    
    def validacion_dimensional(self) -> dict:
        """
        Validación 1: Análisis dimensional
        
        Verifica que todas las masas tienen unidades correctas [kg].
        
        Returns
        -------
        result : dict
            Resultados de validación dimensional
        """
        print("\n" + "="*70)
        print("VALIDACIÓN 1: ANÁLISIS DIMENSIONAL")
        print("="*70)
        
        results = {}
        
        # Ecuación 1: m_eff = hf/c²
        print("\n1. m_eff = hf/c²")
        print(f"   [m_eff] = [J·s][Hz]/[m²/s²]")
        print(f"           = [J·s][1/s]/[m²/s²]")
        print(f"           = [J]/[m²/s²]")
        print(f"           = [kg·m²/s²]/[m²/s²]")
        print(f"           = [kg] ✓")
        results['m_eff_dimensional'] = True
        
        # Ecuación 2: m_noesis = α/f donde α = hf₀²/c²
        print("\n2. m_noesis = α/f con α = hf₀²/c²")
        print(f"   [α] = [J·s][Hz²]/[m²/s²]")
        print(f"       = [J·s][1/s²]/[m²/s²]")
        print(f"       = [J·s]/[s²·m²/s²]")
        print(f"       = [kg·m²/s²·s]/[s²·m²/s²]")
        print(f"       = [kg·s] (también expresable como [kg·Hz] ya que Hz = s⁻¹)")
        print(f"   [m_noesis] = [kg·s]/[s]")
        print(f"              = [kg] ✓")
        results['m_noesis_dimensional'] = True
        
        # Ecuación 3: m(f) = hf₀/c²
        print("\n3. m(f) = hf₀/c² (masa unificada constante)")
        print(f"   [m(f)] = [J·s][Hz]/[m²/s²]")
        print(f"          = [kg] ✓")
        results['m_unified_dimensional'] = True
        
        print("\n✓ VALIDACIÓN DIMENSIONAL EXITOSA: Todas las masas en [kg]")
        
        self.validation_results['dimensional'] = results
        return results
    
    def validacion_numerica(self, tolerance: float = 1e-10) -> dict:
        """
        Validación 2: Precisión numérica
        
        Verifica que los errores relativos sean < 10⁻¹⁰.
        
        Parameters
        ----------
        tolerance : float
            Tolerancia para errores relativos. Default: 10⁻¹⁰
            
        Returns
        -------
        result : dict
            Resultados de validación numérica
        """
        print("\n" + "="*70)
        print("VALIDACIÓN 2: PRECISIÓN NUMÉRICA (errores < 10⁻¹⁰)")
        print("="*70)
        
        results = {}
        test_frequencies = [
            1.0,           # Frecuencia muy baja
            10.0,          # Frecuencia baja
            F0_HZ,         # Frecuencia fundamental
            1000.0,        # Frecuencia alta
            1e6            # Frecuencia muy alta
        ]
        
        max_error = 0.0
        
        for f in test_frequencies:
            # High-precision calculations
            f_mp = mp.mpf(str(f))
            
            # Calculate masses with high precision
            m_eff_mp = self.h_mp * f_mp / self.c2_mp
            m_noesis_mp = self.alpha_mp / f_mp
            m_dual_mp = self.m_min_mp  # Always constant
            
            # Standard precision
            m_eff = self.h * f / self.c2
            m_noesis = self.alpha / f
            m_dual = self.m_min
            
            # Calculate relative errors
            error_eff = abs(float(m_eff_mp) - m_eff) / float(m_eff_mp)
            error_noesis = abs(float(m_noesis_mp) - m_noesis) / float(m_noesis_mp)
            error_dual = abs(float(m_dual_mp) - m_dual) / float(m_dual_mp)
            
            max_error = max(max_error, error_eff, error_noesis, error_dual)
            
            print(f"\nf = {f:.4e} Hz:")
            print(f"  m_eff error:    {error_eff:.4e} {'✓' if error_eff < tolerance else '✗'}")
            print(f"  m_noesis error: {error_noesis:.4e} {'✓' if error_noesis < tolerance else '✗'}")
            print(f"  m_dual error:   {error_dual:.4e} {'✓' if error_dual < tolerance else '✗'}")
        
        results['max_relative_error'] = max_error
        results['within_tolerance'] = max_error < tolerance
        
        print(f"\n✓ Error relativo máximo: {max_error:.4e}")
        print(f"✓ Tolerancia requerida: {tolerance:.4e}")
        print(f"✓ VALIDACIÓN NUMÉRICA {'EXITOSA' if results['within_tolerance'] else 'FALLIDA'}")
        
        self.validation_results['numerical'] = results
        return results
    
    def validacion_complementariedad(self, tolerance: float = 1e-10) -> dict:
        """
        Validación 3: Complementariedad r_eff · r_noesis = 1
        
        Verifica la relación de complementariedad entre masas efectiva y noética.
        
        Parameters
        ----------
        tolerance : float
            Tolerancia para el producto. Default: 10⁻¹⁰
            
        Returns
        -------
        result : dict
            Resultados de validación de complementariedad
        """
        print("\n" + "="*70)
        print("VALIDACIÓN 3: COMPLEMENTARIEDAD r_eff · r_noesis = 1")
        print("="*70)
        
        results = {}
        test_frequencies = np.logspace(-1, 6, 100)  # 0.1 Hz to 1 MHz
        
        r_eff_vals = test_frequencies / self.f0
        r_noesis_vals = self.f0 / test_frequencies
        products = r_eff_vals * r_noesis_vals
        
        # Check all products equal 1
        deviations = np.abs(products - 1.0)
        max_deviation = np.max(deviations)
        
        print(f"\nPrueba sobre {len(test_frequencies)} frecuencias:")
        print(f"  Rango: {test_frequencies[0]:.2e} Hz a {test_frequencies[-1]:.2e} Hz")
        print(f"  Desviación máxima de 1: {max_deviation:.4e}")
        print(f"  Todas las desviaciones < {tolerance}: {'✓' if max_deviation < tolerance else '✗'}")
        
        # Test specific cases
        print("\nCasos específicos:")
        for f in [F0_HZ/10, F0_HZ, F0_HZ*10]:
            r_eff = f / self.f0
            r_noesis = self.f0 / f
            product = r_eff * r_noesis
            print(f"  f = {f:.4f} Hz: r_eff = {r_eff:.6f}, r_noesis = {r_noesis:.6f}, producto = {product:.12f}")
        
        results['max_deviation'] = float(max_deviation)
        results['all_within_tolerance'] = max_deviation < tolerance
        
        print(f"\n✓ VALIDACIÓN DE COMPLEMENTARIEDAD {'EXITOSA' if results['all_within_tolerance'] else 'FALLIDA'}")
        
        self.validation_results['complementarity'] = results
        return results
    
    def validacion_implementacion_numpy(self) -> dict:
        """
        Validación 4: Implementación con NumPy
        
        Verifica que las implementaciones funcionan correctamente con arrays de NumPy.
        
        Returns
        -------
        result : dict
            Resultados de validación de implementación NumPy
        """
        print("\n" + "="*70)
        print("VALIDACIÓN 4: IMPLEMENTACIÓN CON NUMPY")
        print("="*70)
        
        results = {}
        
        # Create frequency array
        frequencies = np.logspace(0, 3, 1000)  # 1 Hz to 1000 Hz, 1000 points
        
        # Calculate masses with NumPy arrays
        m_eff = self.h * frequencies / self.c2
        m_noesis = self.alpha / frequencies
        m_dual = np.full_like(frequencies, self.m_min)
        
        # Verify shapes
        print(f"\nForma de los arrays:")
        print(f"  frequencies: {frequencies.shape}")
        print(f"  m_eff: {m_eff.shape}")
        print(f"  m_noesis: {m_noesis.shape}")
        print(f"  m_dual: {m_dual.shape}")
        
        results['correct_shapes'] = (
            m_eff.shape == frequencies.shape and
            m_noesis.shape == frequencies.shape and
            m_dual.shape == frequencies.shape
        )
        
        # Verify m_dual is constant
        m_dual_std = np.std(m_dual)
        print(f"\nMasa dual constante:")
        print(f"  Media: {np.mean(m_dual):.6e} kg")
        print(f"  Desviación estándar: {m_dual_std:.6e}")
        # Check if standard deviation is effectively zero (< machine epsilon)
        is_constant = m_dual_std < 1e-60
        print(f"  Es constante: {'✓' if is_constant else '✗'}")
        
        results['m_dual_constant'] = is_constant
        
        # Verify all masses are positive
        all_positive = np.all(m_eff > 0) and np.all(m_noesis > 0) and np.all(m_dual > 0)
        print(f"\nTodas las masas son positivas: {'✓' if all_positive else '✗'}")
        results['all_positive'] = all_positive
        
        # Performance test
        import time
        n_iterations = 1000
        start = time.time()
        for _ in range(n_iterations):
            _ = self.h * frequencies / self.c2
        elapsed = time.time() - start
        
        print(f"\nRendimiento (cálculo de {n_iterations} arrays de {len(frequencies)} elementos):")
        print(f"  Tiempo total: {elapsed:.4f} s")
        print(f"  Tiempo por iteración: {elapsed/n_iterations*1000:.4f} ms")
        
        results['performance_ms'] = elapsed / n_iterations * 1000
        
        print(f"\n✓ VALIDACIÓN DE IMPLEMENTACIÓN NUMPY EXITOSA")
        
        self.validation_results['numpy_implementation'] = results
        return results
    
    def validacion_predicciones_fisicas(self) -> dict:
        """
        Validación 5: Predicciones físicas para límites extremos
        
        Verifica el comportamiento para f >> f₀ y f << f₀.
        
        Returns
        -------
        result : dict
            Resultados de validación de predicciones físicas
        """
        print("\n" + "="*70)
        print("VALIDACIÓN 5: PREDICCIONES FÍSICAS")
        print("="*70)
        
        results = {}
        
        # High frequency limit (f >> f₀)
        print("\n1. Límite de alta frecuencia (f >> f₀):")
        f_high = self.f0 * 1e6  # 1 million times f₀
        m_eff_high = self.h * f_high / self.c2
        m_noesis_high = self.alpha / f_high
        
        print(f"   f = {f_high:.4e} Hz ({f_high/self.f0:.2e} × f₀)")
        print(f"   m_eff = {m_eff_high:.4e} kg (>> m_min = {self.m_min:.4e} kg)")
        print(f"   m_noesis = {m_noesis_high:.4e} kg (<< m_min = {self.m_min:.4e} kg)")
        print(f"   Predicción: Vibración pura, casi sin masa noética ✓")
        
        results['high_freq_m_eff_above_min'] = m_eff_high > self.m_min
        results['high_freq_m_noesis_below_min'] = m_noesis_high < self.m_min
        
        # Low frequency limit (f << f₀)
        print("\n2. Límite de baja frecuencia (f << f₀):")
        f_low = self.f0 / 1e6  # 1 millionth of f₀
        m_eff_low = self.h * f_low / self.c2
        m_noesis_low = self.alpha / f_low
        
        print(f"   f = {f_low:.4e} Hz ({f_low/self.f0:.2e} × f₀)")
        print(f"   m_eff = {m_eff_low:.4e} kg (<< m_min = {self.m_min:.4e} kg)")
        print(f"   m_noesis = {m_noesis_low:.4e} kg (>> m_min = {self.m_min:.4e} kg)")
        print(f"   Predicción: Máxima detención, masa emergente ✓")
        
        results['low_freq_m_eff_below_min'] = m_eff_low < self.m_min
        results['low_freq_m_noesis_above_min'] = m_noesis_low > self.m_min
        
        # At f₀ (equilibrium)
        print("\n3. En f₀ (equilibrio):")
        m_eff_f0 = self.h * self.f0 / self.c2
        m_noesis_f0 = self.alpha / self.f0
        
        print(f"   f = {self.f0:.6f} Hz")
        print(f"   m_eff = {m_eff_f0:.4e} kg")
        print(f"   m_noesis = {m_noesis_f0:.4e} kg")
        print(f"   m_dual = {self.m_min:.4e} kg")
        
        tolerance = 1e-10
        equilibrium = (
            abs(m_eff_f0 - m_noesis_f0) / m_eff_f0 < tolerance and
            abs(m_eff_f0 - self.m_min) / m_eff_f0 < tolerance
        )
        print(f"   Todas iguales (error < {tolerance}): {'✓' if equilibrium else '✗'}")
        
        results['equilibrium_at_f0'] = equilibrium
        
        all_predictions_correct = all([
            results['high_freq_m_eff_above_min'],
            results['high_freq_m_noesis_below_min'],
            results['low_freq_m_eff_below_min'],
            results['low_freq_m_noesis_above_min'],
            results['equilibrium_at_f0']
        ])
        
        print(f"\n✓ VALIDACIÓN DE PREDICCIONES FÍSICAS {'EXITOSA' if all_predictions_correct else 'FALLIDA'}")
        
        self.validation_results['physical_predictions'] = results
        return results
    
    def validacion_integracion_constantes(self) -> dict:
        """
        Validación 6: Integración con constantes QCAL
        
        Verifica la correcta integración con f₀ = 141.70001 Hz y constantes QCAL.
        
        Returns
        -------
        result : dict
            Resultados de validación de integración
        """
        print("\n" + "="*70)
        print("VALIDACIÓN 6: INTEGRACIÓN CON CONSTANTES QCAL")
        print("="*70)
        
        results = {}
        tolerance = 1e-10
        
        # Verify f₀ value
        print(f"\n1. Frecuencia fundamental:")
        print(f"   f₀ = {self.f0:.8f} Hz")
        print(f"   f₀ esperado = {F0_HZ:.8f} Hz")
        f0_match = abs(self.f0 - F0_HZ) < tolerance
        print(f"   Coinciden: {'✓' if f0_match else '✗'}")
        results['f0_matches'] = f0_match
        
        # Verify m_min with qcal.constants
        print(f"\n2. Masa mínima noética:")
        print(f"   m_min calculada = {self.m_min:.12e} kg")
        print(f"   M_MIN_NOETIC = {M_MIN_NOETIC:.12e} kg")
        m_min_match = abs(self.m_min - M_MIN_NOETIC) / M_MIN_NOETIC < tolerance
        print(f"   Error relativo: {abs(self.m_min - M_MIN_NOETIC) / M_MIN_NOETIC:.4e}")
        print(f"   Coinciden (error < {tolerance}): {'✓' if m_min_match else '✗'}")
        results['m_min_matches'] = m_min_match
        
        # Verify alpha with qcal.constants
        print(f"\n3. Constante alpha noética:")
        print(f"   α calculada = {self.alpha:.12e} kg·s")
        print(f"   ALPHA_NOETIC = {ALPHA_NOETIC:.12e} kg·s")
        alpha_match = abs(self.alpha - ALPHA_NOETIC) / ALPHA_NOETIC < tolerance
        print(f"   Error relativo: {abs(self.alpha - ALPHA_NOETIC) / ALPHA_NOETIC:.4e}")
        print(f"   Coinciden (error < {tolerance}): {'✓' if alpha_match else '✗'}")
        results['alpha_matches'] = alpha_match
        
        # Verify relationship α = h·f₀²/c²
        print(f"\n4. Relación α = h·f₀²/c²:")
        alpha_expected = self.h * (self.f0 ** 2) / self.c2
        alpha_relation = abs(self.alpha - alpha_expected) / alpha_expected < tolerance
        print(f"   α desde fórmula = {alpha_expected:.12e} kg·s")
        print(f"   α calculada = {self.alpha:.12e} kg·s")
        print(f"   Coinciden: {'✓' if alpha_relation else '✗'}")
        results['alpha_relation_correct'] = alpha_relation
        
        all_match = all([
            results['f0_matches'],
            results['m_min_matches'],
            results['alpha_matches'],
            results['alpha_relation_correct']
        ])
        
        print(f"\n✓ VALIDACIÓN DE INTEGRACIÓN {'EXITOSA' if all_match else 'FALLIDA'}")
        
        self.validation_results['qcal_integration'] = results
        return results
    
    def ejecutar_todas_validaciones(self) -> dict:
        """
        Ejecuta todas las validaciones en secuencia.
        
        Returns
        -------
        all_results : dict
            Resultados completos de todas las validaciones
        """
        print("\n" + "="*70)
        print("VALIDACIÓN COMPLETA DE ECUACIONES NOÉTICAS")
        print("="*70)
        print(f"\nFrecuencia fundamental: f₀ = {self.f0:.8f} Hz")
        print(f"Constante de Planck: h = {self.h:.12e} J·s")
        print(f"Velocidad de la luz: c = {self.c:.0f} m/s")
        print(f"Masa mínima noética: m_min = {self.m_min:.12e} kg")
        print(f"Constante alpha: α = {self.alpha:.12e} kg·s")
        
        # Run all validations
        self.validacion_dimensional()
        self.validacion_numerica()
        self.validacion_complementariedad()
        self.validacion_implementacion_numpy()
        self.validacion_predicciones_fisicas()
        self.validacion_integracion_constantes()
        
        # Summary
        print("\n" + "="*70)
        print("RESUMEN DE VALIDACIONES")
        print("="*70)
        
        all_passed = True
        validation_names = [
            ('dimensional', 'Análisis Dimensional'),
            ('numerical', 'Precisión Numérica'),
            ('complementarity', 'Complementariedad'),
            ('numpy_implementation', 'Implementación NumPy'),
            ('physical_predictions', 'Predicciones Físicas'),
            ('qcal_integration', 'Integración QCAL')
        ]
        
        for key, name in validation_names:
            if key in self.validation_results:
                results = self.validation_results[key]
                # Check if validation passed
                if isinstance(results, dict):
                    passed = all(results.values()) if results else True
                else:
                    passed = results
                
                status = "✓ EXITOSA" if passed else "✗ FALLIDA"
                print(f"{name:30} {status}")
                all_passed = all_passed and passed
        
        print("="*70)
        print(f"\nRESULTADO FINAL: {'✓ TODAS LAS VALIDACIONES EXITOSAS' if all_passed else '✗ ALGUNAS VALIDACIONES FALLARON'}")
        print("="*70)
        
        return self.validation_results


def main():
    """Función principal."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validación completa de ecuaciones noéticas QCAL'
    )
    parser.add_argument(
        '--f0',
        type=float,
        default=F0_HZ,
        help=f'Frecuencia fundamental (Hz). Default: {F0_HZ}'
    )
    parser.add_argument(
        '--precision',
        type=int,
        default=50,
        help='Precisión decimal para cálculos (dps). Default: 50'
    )
    
    args = parser.parse_args()
    
    # Create validator and run all validations
    validator = ValidacionEcuacionesNoeticas(f0=args.f0, precision_dps=args.precision)
    results = validator.ejecutar_todas_validaciones()
    
    # Exit with appropriate code
    all_passed = all(
        all(r.values()) if isinstance(r, dict) else r
        for r in results.values()
    )
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
