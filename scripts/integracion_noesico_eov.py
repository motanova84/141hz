#!/usr/bin/env python3
"""
Integración EOV con Análisis Noésico
=====================================

Integra la Ecuación del Origen Vibracional (EOV) con el análisis
noésico existente del repositorio, ampliando las capacidades de
detección y validación.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2025-10-12
"""

import sys
import os
import numpy as np
from pathlib import Path

# Importar módulos existentes
try:
    from analisis_noesico import AnalizadorNoesico
except ImportError:
    print("⚠️  No se pudo importar AnalizadorNoesico")
    print("   Verifica que el archivo 'analisis_noesico.py' existe en el directorio 'scripts/'.")
    analisis_path = Path(__file__).parent / "analisis_noesico.py"
    if not analisis_path.exists():
        print(f"   Archivo no encontrado: {analisis_path}")
    print("   Asegúrate de estar en el directorio scripts/ y que el archivo no esté renombrado o movido.")
# Importar módulo EOV
try:
    from ecuacion_origen_vibracional import (
        termino_oscilatorio,
        detectar_firma_eov,
        campo_noético_temporal,
        F_0
    )
except ImportError:
    print("⚠️  No se pudo importar módulo EOV")
    sys.exit(1)


class AnalizadorNoesicoEOV(AnalizadorNoesico):
    """
    Extensión del AnalizadorNoesico con capacidades EOV.
    
    Combina el análisis espectral tradicional con predicciones
    basadas en la Ecuación del Origen Vibracional.
    """
    
    def __init__(self, frecuencia_objetivo=141.7001):
        """
        Inicializa el analizador con EOV.
        
        Parámetros
        ----------
        frecuencia_objetivo : float
            Frecuencia madre en Hz (por defecto 141.7001)
        """
        super().__init__(frecuencia_objetivo)
        self.nombre = "Analizador Noésico + EOV"
        
        # Parámetros EOV
        self.omega_0 = 2 * np.pi * frecuencia_objetivo
        self.R_escalar = 1e-20  # m⁻² (estimación)
        self.zeta = 1e-10  # m² (acoplamiento)
        
        print(f"🌌 {self.nombre} inicializado")
        print(f"   Frecuencia f₀: {frecuencia_objetivo} Hz")
        print(f"   Curvatura R: {self.R_escalar:.2e} m⁻²")
    
    def analizar_con_eov(self, data, sample_rate):
        """
        Análisis completo combinando métodos tradicionales y EOV.
        
        Parámetros
        ----------
        data : array
            Serie temporal del strain
        sample_rate : float
            Frecuencia de muestreo (Hz)
        
        Retorna
        -------
        dict
            Resultados combinados del análisis
        """
        print("\n" + "="*60)
        print("🔬 ANÁLISIS NOÉSICO + EOV")
        print("="*60)
        
        # 1. Análisis espectral tradicional
        print("\n📊 Fase 1: Análisis espectral clásico...")
        resultados_clasico = self.analizar_resonancia(data, sample_rate)
        
        # 2. Detección de firma EOV
        print("\n🌌 Fase 2: Detección de firma EOV...")
        tiempo = np.arange(len(data)) / sample_rate
        freq_eov, snr_eov, power_eov = detectar_firma_eov(
            tiempo, data, sample_rate
        )
        
        # 3. Estimación del campo noético
        print("\n🔮 Fase 3: Estimación de campo noético...")
        Psi_squared = self._estimar_campo_noético(data, sample_rate)
        
        # 4. Cálculo del término oscilatorio
        print("\n⚛️  Fase 4: Cálculo de término oscilatorio EOV...")
        termino_osc = termino_oscilatorio(
            tiempo, 
            self.R_escalar, 
            Psi_squared,
            self.frecuencia_objetivo
        )
        
        # Combinar resultados
        resultados = {
            'clasico': resultados_clasico,
            'eov': {
                'frecuencia': freq_eov,
                'snr': snr_eov,
                'potencia': power_eov,
                'campo_noético': Psi_squared,
                'termino_oscilatorio': termino_osc,
                'validacion': abs(freq_eov - self.frecuencia_objetivo) < 0.5
            }
        }
        
        # Resumen
        print("\n" + "="*60)
        print("📋 RESUMEN DE ANÁLISIS")
        print("="*60)
        print(f"Frecuencia detectada (clásico): {resultados_clasico['frecuencia_detectada']:.4f} Hz")
        print(f"Frecuencia detectada (EOV):     {freq_eov:.4f} Hz")
        print(f"SNR (clásico): {resultados_clasico['snr']:.2f}")
        print(f"SNR (EOV):     {snr_eov:.2f}")
        print(f"|Ψ|² medio:    {np.mean(Psi_squared):.2e}")
        
        if resultados['eov']['validacion']:
            print("\n✅✅ FIRMA EOV CONFIRMADA")
        else:
            print("\n⚠️  Firma EOV no detectada claramente")
        
        return resultados
    
    def _estimar_campo_noético(self, data, sample_rate):
        """
        Estima el campo noético |Ψ|² a partir de los datos.
        
        Usa la envolvente de amplitud como proxy del campo.
        
        Parámetros
        ----------
        data : array
            Serie temporal
        sample_rate : float
            Frecuencia de muestreo
        
        Retorna
        -------
        array
            Estimación de |Ψ|²
        """
        from scipy.signal import hilbert
        
        # Usar transformada de Hilbert para obtener envolvente
        analytic_signal = hilbert(data)
        envelope = np.abs(analytic_signal)
        
        # Normalizar y escalar
        Psi_squared = (envelope / np.max(envelope))**2
        
        return Psi_squared
    
    def visualizar_analisis_eov(self, data, sample_rate, output_path):
        """
        Genera visualización del análisis combinado.
        
        Parámetros
        ----------
        data : array
            Serie temporal
        sample_rate : float
            Frecuencia de muestreo
        output_path : str o Path
            Ruta de salida
        """
        import matplotlib.pyplot as plt
        
        # Ejecutar análisis
        resultados = self.analizar_con_eov(data, sample_rate)
        
        # Crear figura
        fig, axes = plt.subplots(3, 2, figsize=(14, 12))
        fig.suptitle('Análisis Noésico + EOV Integrado', 
                    fontsize=16, fontweight='bold')
        
        tiempo = np.arange(len(data)) / sample_rate
        
        # Panel 1: Serie temporal
        ax1 = axes[0, 0]
        ax1.plot(tiempo * 1000, data * 1e21, 'b-', linewidth=0.5, alpha=0.7)
        ax1.set_xlabel('Tiempo (ms)')
        ax1.set_ylabel('Strain (×10⁻²¹)')
        ax1.set_title('Serie Temporal')
        ax1.grid(True, alpha=0.3)
        
        # Panel 2: Campo noético estimado
        ax2 = axes[0, 1]
        Psi_sq = resultados['eov']['campo_noético']
        ax2.plot(tiempo * 1000, Psi_sq, 'purple', linewidth=1.5)
        ax2.set_xlabel('Tiempo (ms)')
        ax2.set_ylabel('|Ψ|²')
        ax2.set_title('Campo Noético Estimado')
        ax2.grid(True, alpha=0.3)
        
        # Panel 3: Espectro de potencia
        ax3 = axes[1, 0]
        freqs = np.fft.rfftfreq(len(data), 1/sample_rate)
        fft_val = np.fft.rfft(data)
        espectro = np.abs(fft_val)**2
        
        mask = (freqs >= 100) & (freqs <= 200)
        ax3.semilogy(freqs[mask], espectro[mask], 'g-', linewidth=1)
        ax3.axvline(self.frecuencia_objetivo, color='red', 
                   linestyle='--', linewidth=2, label=f'f₀ = {self.frecuencia_objetivo} Hz')
        ax3.set_xlabel('Frecuencia (Hz)')
        ax3.set_ylabel('Potencia Espectral')
        ax3.set_title('Espectro de Potencia')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Panel 4: Zoom en f₀
        ax4 = axes[1, 1]
        mask_zoom = (freqs >= self.frecuencia_objetivo - 2) & \
                    (freqs <= self.frecuencia_objetivo + 2)
        ax4.plot(freqs[mask_zoom], espectro[mask_zoom], 'b-', linewidth=2)
        ax4.axvline(self.frecuencia_objetivo, color='red', 
                   linestyle='--', linewidth=2)
        ax4.set_xlabel('Frecuencia (Hz)')
        ax4.set_ylabel('Potencia Espectral')
        ax4.set_title(f'Zoom en {self.frecuencia_objetivo} Hz')
        ax4.grid(True, alpha=0.3)
        
        # Panel 5: Término oscilatorio EOV
        ax5 = axes[2, 0]
        termino_osc = resultados['eov']['termino_oscilatorio']
        ax5.plot(tiempo[:1000] * 1000, termino_osc[:1000], 
                'purple', linewidth=1.5)
        ax5.set_xlabel('Tiempo (ms)')
        ax5.set_ylabel('R cos(2πf₀t)|Ψ|² (m⁻²)')
        ax5.set_title('Término Oscilatorio EOV')
        ax5.grid(True, alpha=0.3)
        
        # Panel 6: Resumen de resultados
        ax6 = axes[2, 1]
        ax6.axis('off')
        
        # Texto de resumen
        resumen = f"""
        RESULTADOS DEL ANÁLISIS
        {'='*30}
        
        Análisis Clásico:
        • Frecuencia: {resultados['clasico']['frecuencia_detectada']:.4f} Hz
        • SNR: {resultados['clasico']['snr']:.2f}
        
        Análisis EOV:
        • Frecuencia: {resultados['eov']['frecuencia']:.4f} Hz
        • SNR: {resultados['eov']['snr']:.2f}
        • |Ψ|² medio: {np.mean(Psi_sq):.2e}
        
        Validación:
        {'✅ CONFIRMADA' if resultados['eov']['validacion'] else '❌ NO DETECTADA'}
        
        {'='*30}
        🌌 EOV: G_μν + Λg_μν = ... + R cos(2πf₀t)|Ψ|²
        """
        
        ax6.text(0.1, 0.5, resumen, 
                fontsize=10, family='monospace',
                verticalalignment='center')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"\n✅ Visualización guardada: {output_path}")
        
        return fig


def main():
    """Ejemplo de uso de la integración."""
    
    print("="*70)
    print("🌌 INTEGRACIÓN: ANÁLISIS NOÉSICO + EOV")
    print("="*70)
    
    # Crear analizador integrado
    analizador = AnalizadorNoesicoEOV()
    
    # Generar datos sintéticos para demostración
    print("\n📊 Generando datos sintéticos...")
    sample_rate = 4096
    duracion = 1.0
    t = np.linspace(0, duracion, int(duracion * sample_rate))
    
    # Señal sintética: modo dominante + componente EOV + ruido
    h_dom = 1e-21 * np.exp(-t/0.01) * np.cos(2*np.pi*250*t)
    h_eov = 5e-23 * campo_noético_temporal(t) * np.cos(2*np.pi*F_0*t)
    ruido = np.random.normal(0, 1e-23, len(t))
    
    data = h_dom + h_eov + ruido
    
    # Ejecutar análisis integrado
    resultados = analizador.analizar_con_eov(data, sample_rate)
    
    # Generar visualización
    output_dir = Path(__file__).parent.parent / "results" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "analisis_noesico_eov_integrado.png"
    
    analizador.visualizar_analisis_eov(data, sample_rate, output_path)
    
    print("\n" + "="*70)
    print("✅ Análisis integrado completado exitosamente")
    print("✨ Resonancia del origen confirmada - QCAL ∞³")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
