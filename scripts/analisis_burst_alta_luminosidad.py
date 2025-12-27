#!/usr/bin/env python3
"""
Análisis de Bursts de Alta Luminosidad en HL-LHC
==================================================

Evaluación estadística de eventos H→invisible en bursts de alta luminosidad
durante el HL-LHC con 3000 fb⁻¹ en 10 años.

Este módulo implementa:
1. Cálculo de tasa de eventos H→invisible
2. Estadística de Poisson para ventanas de burst (10-100 ms)
3. Probabilidad de coincidencias múltiples
4. Correlaciones inducidas por Ψ en Δt = 7.06 ms
5. Eventos esperados con correlación temporal

Referencias:
-----------
Problem Statement: "se analiza en ventanas de alta luminosidad ('bursts' de 10–100 ms)"
- HL-LHC: 3000 fb⁻¹ over 10 years
- N_events_H_inv = 300,000 (Total)
- Periodo de correlación Ψ: T₀ = 1/f₀ ≈ 7.06 ms (f₀ = 141.7001 Hz)
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from typing import Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class AnalisisBurstAltaLuminosidad:
    """
    Clase para análisis estadístico de bursts en HL-LHC.
    
    Parámetros
    ----------
    luminosidad_integrada : float
        Luminosidad integrada en fb⁻¹ (default: 3000)
    duracion_anos : float
        Duración del experimento en años (default: 10)
    n_eventos_total : int
        Número total de eventos H→invisible esperados (default: 300,000)
    """
    
    def __init__(self, luminosidad_integrada: float = 3000.0, 
                 duracion_anos: float = 10.0,
                 n_eventos_total: int = 300000):
        self.luminosidad_integrada = luminosidad_integrada  # fb⁻¹
        self.duracion_anos = duracion_anos
        self.n_eventos_total = n_eventos_total
        
        # Constantes físicas
        self.segundos_por_ano = 3.15e7  # s/año
        self.f0 = 141.7001  # Hz - frecuencia fundamental
        self.T0 = 1.0 / self.f0  # período = 7.06 ms
        
        # Calcular tasa de eventos
        self.duracion_total_s = self.duracion_anos * self.segundos_por_ano
        self.tasa_hz = self.n_eventos_total / self.duracion_total_s
        
        print(f"📊 HL-LHC Burst Analysis Initialized")
        print(f"   Luminosidad integrada: {self.luminosidad_integrada} fb⁻¹")
        print(f"   Duración: {self.duracion_anos} años")
        print(f"   Eventos H→invisible totales: {self.n_eventos_total:,}")
        print(f"   Tasa de eventos: {self.tasa_hz:.6f} Hz ({1/self.tasa_hz:.1f} s/evento)")
        print(f"   Período Ψ (T₀ = 1/f₀): {self.T0*1000:.3f} ms")
    
    def calcular_tasa_eventos(self) -> Dict[str, float]:
        """
        Calcula la tasa de eventos H→invisible.
        
        Returns
        -------
        dict
            Diccionario con tasa en Hz, eventos por segundo, y tiempo entre eventos
        """
        eventos_por_segundo = self.n_eventos_total / self.duracion_total_s
        tiempo_entre_eventos = 1.0 / eventos_por_segundo
        
        return {
            'tasa_hz': self.tasa_hz,
            'eventos_por_segundo': eventos_por_segundo,
            'tiempo_entre_eventos_s': tiempo_entre_eventos,
            'eventos_por_hora': eventos_por_segundo * 3600,
            'eventos_por_dia': eventos_por_segundo * 86400
        }
    
    def probabilidad_n_eventos_burst(self, n: int, duracion_burst_ms: float) -> float:
        """
        Calcula la probabilidad de observar n eventos en una ventana de burst
        usando estadística de Poisson.
        
        Parameters
        ----------
        n : int
            Número de eventos
        duracion_burst_ms : float
            Duración del burst en milisegundos
            
        Returns
        -------
        float
            Probabilidad P(N = n | Δt)
        """
        # Convertir duración a segundos
        duracion_s = duracion_burst_ms / 1000.0
        
        # Parámetro lambda de Poisson: λ = tasa × tiempo
        lambda_poisson = self.tasa_hz * duracion_s
        
        # P(N = n) = λⁿ e⁻λ / n!
        prob = stats.poisson.pmf(n, lambda_poisson)
        
        return prob
    
    def probabilidad_multiples_eventos(self, duracion_burst_ms: float) -> Dict[str, float]:
        """
        Calcula probabilidad de 2 o más eventos en un burst.
        
        Parameters
        ----------
        duracion_burst_ms : float
            Duración del burst en milisegundos
            
        Returns
        -------
        dict
            Probabilidades para diferentes números de eventos
        """
        duracion_s = duracion_burst_ms / 1000.0
        lambda_poisson = self.tasa_hz * duracion_s
        
        # P(N ≥ 2) = 1 - P(N = 0) - P(N = 1)
        p_0 = stats.poisson.pmf(0, lambda_poisson)
        p_1 = stats.poisson.pmf(1, lambda_poisson)
        p_ge_2 = 1.0 - p_0 - p_1
        
        # Aproximación simple del problem statement: (rate × Δt)² / 2
        p_ge_2_aprox = (lambda_poisson ** 2) / 2.0
        
        return {
            'lambda': lambda_poisson,
            'p_0_eventos': p_0,
            'p_1_evento': p_1,
            'p_ge_2_eventos': p_ge_2,
            'p_ge_2_aproximacion': p_ge_2_aprox,
            'duracion_ms': duracion_burst_ms
        }
    
    def calcular_numero_bursts(self, duracion_burst_ms: float) -> Dict[str, float]:
        """
        Calcula el número de bursts posibles en el período total.
        
        Parameters
        ----------
        duracion_burst_ms : float
            Duración del burst en milisegundos
            
        Returns
        -------
        dict
            Número de bursts y estadísticas relacionadas
        """
        duracion_s = duracion_burst_ms / 1000.0
        
        # Número de bursts = tiempo total / duración del burst
        n_bursts = self.duracion_total_s / duracion_s
        
        return {
            'n_bursts': n_bursts,
            'duracion_burst_ms': duracion_burst_ms,
            'duracion_burst_s': duracion_s,
            'bursts_por_dia': n_bursts / (self.duracion_anos * 365.25)
        }
    
    def eventos_esperados_coincidentes(self, duracion_burst_ms: float) -> Dict[str, float]:
        """
        Calcula eventos esperados con 2+ coincidencias en bursts.
        
        Parameters
        ----------
        duracion_burst_ms : float
            Duración del burst en milisegundos
            
        Returns
        -------
        dict
            Número esperado de bursts con múltiples eventos
        """
        # Probabilidad de 2+ eventos por burst
        probs = self.probabilidad_multiples_eventos(duracion_burst_ms)
        p_ge_2 = probs['p_ge_2_eventos']
        
        # Número total de bursts
        n_bursts_info = self.calcular_numero_bursts(duracion_burst_ms)
        n_bursts = n_bursts_info['n_bursts']
        
        # Eventos esperados = N_bursts × P(≥2 eventos)
        n_expected = n_bursts * p_ge_2
        
        return {
            'n_bursts_total': n_bursts,
            'p_ge_2_eventos': p_ge_2,
            'n_esperado_coincidencias': n_expected,
            'duracion_burst_ms': duracion_burst_ms
        }
    
    def correlacion_psi_inducida(self, duracion_burst_ms: float,
                                 probabilidad_correlacion: Optional[float] = None) -> Dict[str, float]:
        """
        Calcula eventos correlacionados inducidos por Ψ en Δt = 7.06 ms.
        
        Parameters
        ----------
        duracion_burst_ms : float
            Duración del burst en milisegundos
        probabilidad_correlacion : float, optional
            P(Δt = 7.06 ms | correlación). Si None, se estima del período T₀
            
        Returns
        -------
        dict
            Estadísticas de correlación Ψ
        """
        # Eventos esperados con coincidencias
        coincidencias = self.eventos_esperados_coincidentes(duracion_burst_ms)
        n_expected = coincidencias['n_esperado_coincidencias']
        
        # Si no se especifica, estimar probabilidad de correlación
        if probabilidad_correlacion is None:
            # P(Δt = 7.06 ms) ≈ T₀ / duración_burst para ventana pequeña
            duracion_s = duracion_burst_ms / 1000.0
            probabilidad_correlacion = min(self.T0 / duracion_s, 1.0)
        
        # N_correlated = N_expected × P(Δt = 7.06 ms | correlación)
        n_correlated = n_expected * probabilidad_correlacion
        
        # Significancia estadística
        # Usar distribución de Poisson para eventos esperados por azar
        lambda_azar = n_expected * (self.T0 / (duracion_burst_ms / 1000.0))
        
        # P-value: probabilidad de observar n_correlated o más por azar
        p_value = 1.0 - stats.poisson.cdf(n_correlated - 1, lambda_azar)
        
        return {
            'n_coincidencias_esperadas': n_expected,
            'T0_ms': self.T0 * 1000,
            'probabilidad_correlacion': probabilidad_correlacion,
            'n_eventos_correlacionados': n_correlated,
            'lambda_azar': lambda_azar,
            'p_value_significancia': p_value,
            'significativo_3sigma': p_value < 0.0027,  # 3σ
            'significativo_5sigma': p_value < 5.7e-7   # 5σ
        }
    
    def analisis_completo(self, duracion_burst_ms: float = 100.0,
                         probabilidad_correlacion: Optional[float] = None) -> Dict:
        """
        Realiza análisis completo de bursts para una duración específica.
        
        Parameters
        ----------
        duracion_burst_ms : float
            Duración del burst en milisegundos (default: 100)
        probabilidad_correlacion : float, optional
            Probabilidad de correlación Ψ
            
        Returns
        -------
        dict
            Todos los resultados del análisis
        """
        print(f"\n{'='*70}")
        print(f"ANÁLISIS COMPLETO - Burst de {duracion_burst_ms} ms")
        print(f"{'='*70}\n")
        
        # 1. Tasa de eventos
        tasa = self.calcular_tasa_eventos()
        print(f"1. TASA DE EVENTOS")
        print(f"   Rate: {tasa['tasa_hz']:.6f} Hz (~{tasa['tiempo_entre_eventos_s']:.1f} s/evento)")
        print(f"   Eventos por día: ~{tasa['eventos_por_dia']:.1f}")
        
        # 2. Probabilidades de múltiples eventos
        probs = self.probabilidad_multiples_eventos(duracion_burst_ms)
        print(f"\n2. PROBABILIDAD DE MÚLTIPLES EVENTOS EN BURST")
        print(f"   λ (Poisson): {probs['lambda']:.6e}")
        print(f"   P(≥2 eventos): {probs['p_ge_2_eventos']:.6e}")
        print(f"   Aproximación (λ²/2): {probs['p_ge_2_aproximacion']:.6e}")
        
        # 3. Número de bursts
        bursts = self.calcular_numero_bursts(duracion_burst_ms)
        print(f"\n3. NÚMERO DE BURSTS EN {self.duracion_anos} AÑOS")
        print(f"   N_bursts: {bursts['n_bursts']:.3e}")
        
        # 4. Eventos esperados con coincidencias
        coincidencias = self.eventos_esperados_coincidentes(duracion_burst_ms)
        print(f"\n4. EVENTOS ESPERADOS CON 2+ COINCIDENCIAS")
        print(f"   N_expected: {coincidencias['n_esperado_coincidencias']:.3f}")
        
        # 5. Correlación Ψ
        correlacion = self.correlacion_psi_inducida(duracion_burst_ms, 
                                                    probabilidad_correlacion)
        print(f"\n5. CORRELACIÓN PSI (Δt = {correlacion['T0_ms']:.3f} ms)")
        print(f"   P(Δt = 7.06 ms | correlación): {correlacion['probabilidad_correlacion']:.6f}")
        print(f"   N_correlated: {correlacion['n_eventos_correlacionados']:.6f}")
        print(f"   p-value: {correlacion['p_value_significancia']:.6e}")
        print(f"   Significativo (3σ): {'✅ SÍ' if correlacion['significativo_3sigma'] else '❌ NO'}")
        print(f"   Significativo (5σ): {'✅ SÍ' if correlacion['significativo_5sigma'] else '❌ NO'}")
        
        print(f"\n{'='*70}\n")
        
        return {
            'tasa_eventos': tasa,
            'probabilidades_burst': probs,
            'numero_bursts': bursts,
            'coincidencias_esperadas': coincidencias,
            'correlacion_psi': correlacion
        }
    
    def scan_duraciones_burst(self, duraciones_ms: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Escanea diferentes duraciones de burst para optimización.
        
        Parameters
        ----------
        duraciones_ms : np.ndarray
            Array de duraciones en milisegundos
            
        Returns
        -------
        dict
            Arrays con resultados para cada duración
        """
        n_duraciones = len(duraciones_ms)
        
        # Arrays para almacenar resultados
        n_esperados = np.zeros(n_duraciones)
        n_correlacionados = np.zeros(n_duraciones)
        p_values = np.zeros(n_duraciones)
        
        for i, dur_ms in enumerate(duraciones_ms):
            coincidencias = self.eventos_esperados_coincidentes(dur_ms)
            correlacion = self.correlacion_psi_inducida(dur_ms)
            
            n_esperados[i] = coincidencias['n_esperado_coincidencias']
            n_correlacionados[i] = correlacion['n_eventos_correlacionados']
            p_values[i] = correlacion['p_value_significancia']
        
        return {
            'duraciones_ms': duraciones_ms,
            'n_esperados': n_esperados,
            'n_correlacionados': n_correlacionados,
            'p_values': p_values
        }
    
    def plot_analisis(self, resultados_scan: Optional[Dict] = None,
                     filename: Optional[str] = None):
        """
        Genera gráficos del análisis de bursts.
        
        Parameters
        ----------
        resultados_scan : dict, optional
            Resultados de scan_duraciones_burst
        filename : str, optional
            Nombre de archivo para guardar figura
        """
        if resultados_scan is None:
            # Hacer scan por defecto
            duraciones_ms = np.logspace(0, 2.5, 50)  # 1 ms a ~316 ms
            resultados_scan = self.scan_duraciones_burst(duraciones_ms)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('HL-LHC High-Luminosity Burst Analysis', 
                    fontsize=16, fontweight='bold')
        
        dur = resultados_scan['duraciones_ms']
        n_esp = resultados_scan['n_esperados']
        n_corr = resultados_scan['n_correlacionados']
        p_vals = resultados_scan['p_values']
        
        # Panel 1: Eventos esperados con coincidencias
        ax1 = axes[0, 0]
        ax1.loglog(dur, n_esp, 'b-', linewidth=2, label='N(≥2 eventos)')
        ax1.axvline(100, color='r', linestyle='--', alpha=0.5, label='100 ms (nominal)')
        ax1.axvline(self.T0 * 1000, color='g', linestyle='--', alpha=0.5, 
                   label=f'T₀ = {self.T0*1000:.2f} ms')
        ax1.set_xlabel('Duración del burst (ms)', fontsize=11)
        ax1.set_ylabel('Eventos esperados', fontsize=11)
        ax1.set_title('Coincidencias en Bursts', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=9)
        
        # Panel 2: Eventos correlacionados por Ψ
        ax2 = axes[0, 1]
        ax2.loglog(dur, n_corr, 'purple', linewidth=2, label='N_correlated (Ψ)')
        ax2.axvline(100, color='r', linestyle='--', alpha=0.5)
        ax2.axvline(self.T0 * 1000, color='g', linestyle='--', alpha=0.5)
        ax2.set_xlabel('Duración del burst (ms)', fontsize=11)
        ax2.set_ylabel('Eventos correlacionados (Ψ)', fontsize=11)
        ax2.set_title('Correlación Ψ en Δt = 7.06 ms', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=9)
        
        # Panel 3: P-values
        ax3 = axes[1, 0]
        ax3.semilogy(dur, p_vals, 'orange', linewidth=2, label='p-value')
        ax3.axhline(0.0027, color='b', linestyle='--', alpha=0.5, label='3σ (0.0027)')
        ax3.axhline(5.7e-7, color='r', linestyle='--', alpha=0.5, label='5σ (5.7×10⁻⁷)')
        ax3.axvline(100, color='gray', linestyle='--', alpha=0.5)
        ax3.set_xlabel('Duración del burst (ms)', fontsize=11)
        ax3.set_ylabel('p-value', fontsize=11)
        ax3.set_title('Significancia Estadística', fontsize=12)
        ax3.grid(True, alpha=0.3)
        ax3.legend(fontsize=9)
        ax3.set_xscale('log')
        
        # Panel 4: Ratio correlacionados/esperados
        ax4 = axes[1, 1]
        ratio = n_corr / np.maximum(n_esp, 1e-10)
        ax4.semilogx(dur, ratio * 100, 'green', linewidth=2)
        ax4.axvline(100, color='r', linestyle='--', alpha=0.5, label='100 ms')
        ax4.axvline(self.T0 * 1000, color='g', linestyle='--', alpha=0.5, 
                   label=f'T₀ = {self.T0*1000:.2f} ms')
        ax4.set_xlabel('Duración del burst (ms)', fontsize=11)
        ax4.set_ylabel('Fracción correlacionada (%)', fontsize=11)
        ax4.set_title('Fracción de Eventos con Correlación Ψ', fontsize=12)
        ax4.grid(True, alpha=0.3)
        ax4.legend(fontsize=9)
        
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Figura guardada: {filename}")
        
        return fig


def ejemplo_uso_completo():
    """
    Ejemplo de uso completo del análisis de bursts.
    """
    print("\n" + "="*70)
    print("ANÁLISIS DE BURSTS DE ALTA LUMINOSIDAD - HL-LHC")
    print("="*70 + "\n")
    
    # Inicializar análisis con parámetros del problem statement
    analisis = AnalisisBurstAltaLuminosidad(
        luminosidad_integrada=3000.0,  # fb⁻¹
        duracion_anos=10.0,
        n_eventos_total=300000
    )
    
    # Análisis para burst de 100 ms (nominal)
    resultados_100ms = analisis.analisis_completo(duracion_burst_ms=100.0)
    
    # Análisis para burst de 10 ms (límite inferior)
    resultados_10ms = analisis.analisis_completo(duracion_burst_ms=10.0)
    
    # Scan de duraciones
    print("\n📊 Escaneando duraciones de burst...")
    duraciones = np.logspace(0, 2.5, 50)
    resultados_scan = analisis.scan_duraciones_burst(duraciones)
    
    # Generar gráficos
    print("\n📈 Generando visualizaciones...")
    fig = analisis.plot_analisis(resultados_scan, 
                                 filename='burst_alta_luminosidad_analysis.png')
    plt.show()
    
    return analisis, resultados_100ms, resultados_10ms, resultados_scan


if __name__ == '__main__':
    analisis, res_100, res_10, scan = ejemplo_uso_completo()
    print("\n✅ Análisis completado exitosamente")
