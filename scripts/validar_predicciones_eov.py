#!/usr/bin/env python3
"""
Script de Validación de Predicciones EOV
=========================================

Valida las predicciones teóricas de la Ecuación del Origen Vibracional
comparando con señales sintéticas conocidas y estableciendo criterios
de aceptación.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2025-10-12
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Importar módulo EOV
try:
    from ecuacion_origen_vibracional import (
        termino_oscilatorio,
        detectar_firma_eov,
        generar_señal_eov,
        campo_noético_temporal,
        F_0,
        G, C
    )
except ImportError:
    print("❌ Error: No se pudo importar módulo EOV")
    sys.exit(1)


class ValidadorEOV:
    """Clase para validar predicciones de la EOV."""
    
    def __init__(self):
        """Inicializa el validador."""
        self.resultados = []
        self.tests_pasados = 0
        self.tests_totales = 0
    
    def test_frecuencia_exacta(self):
        """
        Test 1: Verificar detección exacta de f₀.
        
        Genera una señal pura a 141.7001 Hz y verifica que
        se detecte correctamente.
        """
        print("\n" + "="*60)
        print("TEST 1: Detección de Frecuencia Exacta")
        print("="*60)
        
        # Generar señal pura
        sample_rate = 4096
        duracion = 1.0
        t = np.linspace(0, duracion, int(duracion * sample_rate))
        
        señal = 1e-21 * np.cos(2 * np.pi * F_0 * t)
        
        # Detectar
        freq, snr, power = detectar_firma_eov(t, señal, sample_rate)
        
        # Validar
        error_freq = abs(freq - F_0)
        tolerancia = 0.5  # Hz
        
        print(f"Frecuencia objetivo: {F_0} Hz")
        print(f"Frecuencia detectada: {freq:.4f} Hz")
        print(f"Error: {error_freq:.4f} Hz")
        print(f"SNR: {snr:.2f}")
        
        exito = error_freq < tolerancia
        self._registrar_resultado("Frecuencia exacta", exito)
        
        if exito:
            print("✅ TEST PASADO")
        else:
            print("❌ TEST FALLIDO")
        
        return exito
    
    def test_señal_con_ruido(self):
        """
        Test 2: Detección en presencia de ruido.
        
        Verifica que la firma EOV sea detectable incluso
        con ruido gaussiano añadido.
        """
        print("\n" + "="*60)
        print("TEST 2: Detección con Ruido Gaussiano")
        print("="*60)
        
        sample_rate = 4096
        duracion = 1.0
        t = np.linspace(0, duracion, int(duracion * sample_rate))
        
        # Señal + ruido
        señal_pura = 1e-21 * np.cos(2 * np.pi * F_0 * t)
        ruido = np.random.normal(0, 5e-22, len(t))
        señal_total = señal_pura + ruido
        
        # Calcular SNR teórico
        snr_teórico = np.std(señal_pura) / np.std(ruido)
        
        # Detectar
        freq, snr, power = detectar_firma_eov(t, señal_total, sample_rate)
        
        print(f"SNR teórico: {snr_teórico:.2f}")
        print(f"SNR detectado: {snr:.2f}")
        print(f"Frecuencia detectada: {freq:.4f} Hz")
        
        # Criterio: debe detectar frecuencia correcta con SNR > 2
        exito = (abs(freq - F_0) < 0.5) and (snr > 2)
        self._registrar_resultado("Detección con ruido", exito)
        
        if exito:
            print("✅ TEST PASADO")
        else:
            print("❌ TEST FALLIDO")
        
        return exito
    
    def test_termino_oscilatorio(self):
        """
        Test 3: Validar cálculo del término oscilatorio.
        
        Verifica propiedades del término R cos(2πf₀t)|Ψ|².
        """
        print("\n" + "="*60)
        print("TEST 3: Propiedades del Término Oscilatorio")
        print("="*60)
        
        # Parámetros
        R = 1e-20  # m⁻²
        Psi_sq = 1.0
        duracion = 1.0
        sample_rate = 4096
        t = np.linspace(0, duracion, int(duracion * sample_rate))
        
        # Calcular término
        termino = termino_oscilatorio(t, R, Psi_sq, F_0)
        
        # Propiedades esperadas
        # 1. Amplitud máxima = R * |Ψ|²
        amplitud_max = np.max(np.abs(termino))
        amplitud_esperada = R * Psi_sq
        
        # 2. Frecuencia de oscilación = f₀
        from scipy.signal import welch
        freqs, psd = welch(termino, sample_rate, nperseg=1024)
        idx_pico = np.argmax(psd)
        freq_dominante = freqs[idx_pico]
        
        print(f"Amplitud máxima: {amplitud_max:.2e} m⁻²")
        print(f"Amplitud esperada: {amplitud_esperada:.2e} m⁻²")
        print(f"Frecuencia dominante: {freq_dominante:.2f} Hz")
        print(f"Frecuencia esperada: {F_0} Hz")
        
        # Criterios
        test1 = abs(amplitud_max - amplitud_esperada) / amplitud_esperada < 0.01
        test2 = abs(freq_dominante - F_0) / F_0 < 0.01  # 1% relative tolerance
        
        exito = test1 and test2
        self._registrar_resultado("Término oscilatorio", exito)
        
        if exito:
            print("✅ TEST PASADO")
        else:
            print("❌ TEST FALLIDO")
        
        return exito
    
    def test_campo_noético_temporal(self):
        """
        Test 4: Validar evolución temporal del campo noético.
        
        Verifica que el campo tenga propiedades físicas correctas.
        """
        print("\n" + "="*60)
        print("TEST 4: Evolución Temporal del Campo Noético")
        print("="*60)
        
        duracion = 1.0
        sample_rate = 4096
        t = np.linspace(-0.5, 0.5, int(duracion * sample_rate))
        
        # Generar campo
        Psi_sq = campo_noético_temporal(t, t_merge=0.0, tau_decay=0.1, Psi_0=1.0)
        
        # Propiedades esperadas
        # 1. Máximo en t = 0 (momento de fusión)
        idx_max = np.argmax(Psi_sq)
        t_max = t[idx_max]
        
        # 2. Decaimiento exponencial
        # Ajustar exponencial después del pico
        mask_decay = t > 0
        from scipy.optimize import curve_fit
        
        def exp_decay(t, A, tau):
            return A * np.exp(-t**2 / (2*tau**2))
        
        try:
            popt, _ = curve_fit(exp_decay, t[mask_decay], Psi_sq[mask_decay],
                              p0=[1.0, 0.1])
            tau_ajustado = popt[1]
            
            print(f"Tiempo del pico: {t_max:.3f} s (esperado: 0.0 s)")
            print(f"Valor máximo: {np.max(Psi_sq):.3f} (esperado: 1.0)")
            print(f"Tau ajustado: {tau_ajustado:.3f} s (esperado: 0.1 s)")
            
            # Criterios
            test1 = abs(t_max) < 0.01  # Pico cerca de t=0
            test2 = abs(np.max(Psi_sq) - 1.0) < 0.05  # Amplitud correcta
            test3 = abs(tau_ajustado - 0.1) < 0.02  # Tau correcto
            
            exito = test1 and test2 and test3
            
        except:
            print("⚠️  Error en ajuste exponencial")
            exito = False
        
        self._registrar_resultado("Campo temporal", exito)
        
        if exito:
            print("✅ TEST PASADO")
        else:
            print("❌ TEST FALLIDO")
        
        return exito
    
    def test_señal_eov_completa(self):
        """
        Test 5: Generar y validar señal EOV completa.
        
        Verifica que la señal generada tenga las propiedades esperadas.
        """
        print("\n" + "="*60)
        print("TEST 5: Señal EOV Completa")
        print("="*60)
        
        duracion = 0.5
        sample_rate = 4096
        t = np.linspace(0, duracion, int(duracion * sample_rate))
        
        # Generar señal
        h = generar_señal_eov(t, amplitud=1e-21)
        
        # Propiedades
        print(f"Duración: {duracion} s")
        print(f"Amplitud máxima: {np.max(np.abs(h)):.2e}")
        print(f"Amplitud RMS: {np.sqrt(np.mean(h**2)):.2e}")
        
        # Detectar frecuencia
        freq, snr, power = detectar_firma_eov(t, h, sample_rate)
        
        print(f"Frecuencia detectada: {freq:.4f} Hz")
        print(f"SNR: {snr:.2f}")
        
        # Criterios
        test1 = np.max(np.abs(h)) > 0  # Señal no nula
        test2 = abs(freq - F_0) < 1.0  # Frecuencia correcta
        test3 = snr > 5  # SNR razonable
        
        exito = test1 and test2 and test3
        self._registrar_resultado("Señal EOV completa", exito)
        
        if exito:
            print("✅ TEST PASADO")
        else:
            print("❌ TEST FALLIDO")
        
        return exito
    
    def _registrar_resultado(self, nombre_test, exito):
        """Registra resultado de un test."""
        self.tests_totales += 1
        if exito:
            self.tests_pasados += 1
        
        self.resultados.append({
            'test': nombre_test,
            'exito': exito
        })
    
    def generar_reporte(self):
        """Genera reporte final de validación."""
        print("\n" + "="*70)
        print("📋 REPORTE FINAL DE VALIDACIÓN EOV")
        print("="*70)
        
        print(f"\nTests ejecutados: {self.tests_totales}")
        print(f"Tests pasados:    {self.tests_pasados}")
        print(f"Tests fallidos:   {self.tests_totales - self.tests_pasados}")
        print(f"Tasa de éxito:    {self.tests_pasados/self.tests_totales*100:.1f}%")
        
        print("\n📊 Resultados detallados:")
        for resultado in self.resultados:
            estado = "✅" if resultado['exito'] else "❌"
            print(f"  {estado} {resultado['test']}")
        
        print("\n" + "="*70)
        
        if self.tests_pasados == self.tests_totales:
            print("🎉 VALIDACIÓN COMPLETA EXITOSA")
            print("✨ Todas las predicciones EOV verificadas")
        elif self.tests_pasados >= self.tests_totales * 0.8:
            print("✅ VALIDACIÓN MAYORMENTE EXITOSA")
            print("⚠️  Algunos tests requieren revisión")
        else:
            print("⚠️  VALIDACIÓN PARCIAL")
            print("🔍 Se requiere revisión de implementación")
        
        print("="*70)
        
        return self.tests_pasados == self.tests_totales


def main():
    """Ejecuta suite completa de validación."""
    
    print("="*70)
    print("🌌 VALIDACIÓN DE PREDICCIONES EOV")
    print("   Ecuación del Origen Vibracional - QCAL ∞³")
    print("="*70)
    
    # Crear validador
    validador = ValidadorEOV()
    
    # Ejecutar tests
    validador.test_frecuencia_exacta()
    validador.test_señal_con_ruido()
    validador.test_termino_oscilatorio()
    validador.test_campo_noético_temporal()
    validador.test_señal_eov_completa()
    
    # Generar reporte
    exito = validador.generar_reporte()
    
    return 0 if exito else 1


if __name__ == "__main__":
    sys.exit(main())
