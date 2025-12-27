#!/usr/bin/env python3
"""
LISA - Laser Interferometer Space Antenna
Targeted Continuous-Wave Search Pipeline

Objetivo: Detectar o falsar la existencia de una línea espectral universal a
f₀ = 141.7001 ± 0.3 Hz en el espectro de fondo de ondas gravitacionales.

El modelo GQN predice armónicos descendentes:
f_n = f₀ / (n·φ), n ∈ ℕ

Con resonancias esperadas en:
- 0.0877 Hz (n=1)
- 0.0542 Hz (n=2)
- etc.

Implementa búsqueda dirigida usando Time Delay Interferometry (TDI) de LISA Pathfinder.
"""

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path


# Constantes del modelo GQN
F0 = 141.7001  # Hz - Frecuencia prima del modelo GQN
PHI = (1 + np.sqrt(5)) / 2  # Número áureo (phi)
TOLERANCE = 0.3  # Hz - Tolerancia de la frecuencia


class LISASearchPipeline:
    """
    Pipeline para búsqueda de ondas gravitacionales continuas en LISA.
    
    Implementa Time Delay Interferometry (TDI) y cálculo de SNR.
    """
    
    def __init__(self, sample_rate: float = 10.0, duration: float = 86400.0):
        """
        Inicializa el pipeline de búsqueda LISA.
        
        Args:
            sample_rate: Tasa de muestreo en Hz (default: 10 Hz para LISA)
            duration: Duración de observación en segundos (default: 1 día)
        """
        self.sample_rate = sample_rate
        self.duration = duration
        self.t_obs = duration
        
    def calculate_harmonic_frequencies(self, n_max: int = 1000) -> List[float]:
        """
        Calcula las frecuencias armónicas descendentes predichas por GQN.
        
        f_n = f₀ / (n·φ), n ∈ ℕ
        
        Args:
            n_max: Número máximo de armónicos a calcular (default: 1000 para cubrir rango LISA)
            
        Returns:
            Lista de frecuencias armónicas en Hz
        """
        harmonics = []
        for n in range(1, n_max + 1):
            f_n = F0 / (n * PHI)
            # Solo incluir frecuencias dentro del rango de LISA (0.1 mHz - 1 Hz)
            if 0.0001 <= f_n <= 1.0:
                harmonics.append(f_n)
            # Detener si ya estamos muy por debajo del rango
            if f_n < 0.00001:
                break
        return harmonics
    
    def noise_spectral_density(self, f: np.ndarray) -> np.ndarray:
        """
        Calcula la densidad espectral de ruido S_n(f) para LISA.
        
        Modelo simplificado basado en:
        - Ruido de aceleración (masas de prueba)
        - Ruido óptico (disparo fotónico)
        
        Args:
            f: Array de frecuencias en Hz
            
        Returns:
            S_n(f): Densidad espectral de ruido en Hz^-1
        """
        # Frecuencia de transferencia LISA (aproximadamente)
        f_star = 19.09e-3  # Hz
        
        # Ruido de aceleración (masas de prueba)
        # S_a = 3e-15 m/s²/√Hz a 1 mHz
        S_a = 9e-30 / (2 * np.pi * f)**4 * (1 + (0.4e-3 / f)**2)
        
        # Ruido óptico (disparo fotónico)
        # S_x = 15 pm/√Hz
        S_x = 2.25e-22  # m²/Hz
        
        # Longitud de brazo LISA
        L = 2.5e9  # m
        
        # Densidad espectral total
        S_n = (S_a / (2 * np.pi * f)**4 + S_x) / L**2
        
        return S_n
    
    def calculate_snr(self, h0: float, f_target: float) -> float:
        """
        Calcula el SNR para una señal de onda continua.
        
        SNR_LISA = h₀ / √(S_n(f) / T_obs)
        
        Args:
            h0: Amplitud de deformación de la onda gravitacional
            f_target: Frecuencia objetivo en Hz
            
        Returns:
            SNR: Relación señal-ruido
        """
        S_n = self.noise_spectral_density(np.array([f_target]))[0]
        snr = h0 / np.sqrt(S_n / self.t_obs)
        return snr
    
    def generate_tdi_signal(self, 
                           frequencies: List[float],
                           amplitudes: Optional[List[float]] = None,
                           noise_level: float = 1e-20) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera una señal simulada de Time Delay Interferometry (TDI).
        
        Args:
            frequencies: Lista de frecuencias de señal en Hz
            amplitudes: Lista de amplitudes correspondientes (default: 1e-20 para todas)
            noise_level: Nivel de ruido a añadir
            
        Returns:
            (t, signal): Arrays de tiempo y señal TDI
        """
        n_samples = int(self.sample_rate * self.duration)
        t = np.linspace(0, self.duration, n_samples)
        
        if amplitudes is None:
            amplitudes = [1e-20] * len(frequencies)
        
        # Señal determinista
        signal_clean = np.zeros(n_samples)
        for f, amp in zip(frequencies, amplitudes):
            signal_clean += amp * np.sin(2 * np.pi * f * t)
        
        # Añadir ruido gaussiano
        noise = np.random.normal(0, noise_level, n_samples)
        signal_noisy = signal_clean + noise
        
        return t, signal_noisy
    
    def perform_fft_analysis(self, 
                            signal_data: np.ndarray,
                            target_frequencies: List[float]) -> Dict[str, any]:
        """
        Realiza análisis FFT y busca picos en las frecuencias objetivo.
        
        Args:
            signal_data: Datos de señal TDI
            target_frequencies: Lista de frecuencias a buscar
            
        Returns:
            Diccionario con resultados del análisis
        """
        # FFT
        fft_vals = fft(signal_data)
        fft_freq = fftfreq(len(signal_data), 1/self.sample_rate)
        
        # Solo frecuencias positivas
        positive_freq_idx = fft_freq > 0
        fft_freq_positive = fft_freq[positive_freq_idx]
        fft_power = np.abs(fft_vals[positive_freq_idx])**2
        
        # Buscar picos en frecuencias objetivo
        results = {
            'frequencies_searched': target_frequencies,
            'detections': [],
            'spectrum': {
                'frequency': fft_freq_positive.tolist(),
                'power': fft_power.tolist()
            }
        }
        
        for f_target in target_frequencies:
            # Buscar pico dentro de tolerancia
            freq_mask = np.abs(fft_freq_positive - f_target) < TOLERANCE / 2
            if np.any(freq_mask):
                peak_power = np.max(fft_power[freq_mask])
                peak_freq = fft_freq_positive[freq_mask][np.argmax(fft_power[freq_mask])]
                
                # Estimar SNR (simplificado)
                noise_power = np.median(fft_power)
                snr_estimated = np.sqrt(peak_power / noise_power)
                
                detection = {
                    'target_frequency': f_target,
                    'detected_frequency': float(peak_freq),
                    'power': float(peak_power),
                    'snr_estimated': float(snr_estimated),
                    'significant': snr_estimated > 6.0
                }
                results['detections'].append(detection)
        
        return results
    
    def run_targeted_search(self, 
                           n_harmonics: int = 1000,
                           save_results: bool = True,
                           output_dir: str = "lisa_results") -> Dict[str, any]:
        """
        Ejecuta búsqueda dirigida de armónicos de f₀ en datos LISA simulados.
        
        Args:
            n_harmonics: Número máximo de armónicos a buscar (default: 1000)
            save_results: Si guardar resultados en archivo
            output_dir: Directorio para guardar resultados
            
        Returns:
            Diccionario con resultados completos
        """
        print(f"🔭 LISA Targeted Search Pipeline")
        print(f"=" * 60)
        print(f"Frecuencia prima: f₀ = {F0} Hz")
        print(f"Duración observación: {self.duration/3600:.1f} horas")
        print(f"Tasa de muestreo: {self.sample_rate} Hz")
        print()
        
        # Calcular frecuencias armónicas
        harmonics = self.calculate_harmonic_frequencies(n_harmonics)
        print(f"Armónicos descendentes (dentro rango LISA):")
        for i, f in enumerate(harmonics, 1):
            print(f"  f_{i} = {f:.6f} Hz")
        print()
        
        # Generar señal TDI simulada con armónicos
        print("Generando señal TDI simulada...")
        t, signal_data = self.generate_tdi_signal(harmonics)
        
        # Análisis FFT
        print("Realizando análisis FFT...")
        results = self.perform_fft_analysis(signal_data, harmonics)
        
        # Calcular SNR teórico para cada armónico
        theoretical_snr = []
        for f in harmonics:
            snr = self.calculate_snr(h0=1e-20, f_target=f)
            theoretical_snr.append(snr)
        
        results['theoretical_snr'] = theoretical_snr
        results['harmonics'] = harmonics
        results['f0'] = F0
        results['phi'] = PHI
        results['observation_time'] = self.duration
        
        # Reporte de detecciones
        print("\n" + "=" * 60)
        print("RESULTADOS DE BÚSQUEDA")
        print("=" * 60)
        
        n_significant = sum(1 for d in results['detections'] if d['significant'])
        print(f"\nDetecciones significativas (SNR > 6): {n_significant}/{len(harmonics)}")
        
        for detection in results['detections']:
            status = "✓ DETECTADO" if detection['significant'] else "✗ No significativo"
            print(f"\n{status}")
            print(f"  Frecuencia objetivo: {detection['target_frequency']:.6f} Hz")
            print(f"  Frecuencia detectada: {detection['detected_frequency']:.6f} Hz")
            print(f"  SNR estimado: {detection['snr_estimated']:.2f}")
        
        # Guardar resultados
        if save_results:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            results_file = output_path / "lisa_search_results.json"
            with open(results_file, 'w') as f:
                # Convertir numpy arrays para serialización JSON
                results_clean = results.copy()
                results_clean['spectrum'] = {
                    'frequency': results['spectrum']['frequency'][:1000],  # Limitar tamaño
                    'power': results['spectrum']['power'][:1000]
                }
                json.dump(results_clean, f, indent=2)
            
            print(f"\n📁 Resultados guardados en: {results_file}")
        
        return results
    
    def plot_results(self, results: Dict[str, any], output_dir: str = "lisa_results"):
        """
        Genera visualizaciones de los resultados.
        
        Args:
            results: Diccionario de resultados del análisis
            output_dir: Directorio para guardar gráficos
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Gráfico 1: Espectro de potencia con armónicos marcados
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        freq = np.array(results['spectrum']['frequency'])
        power = np.array(results['spectrum']['power'])
        
        ax1.loglog(freq, power, alpha=0.7, label='Espectro LISA')
        for f in results['harmonics']:
            ax1.axvline(f, color='red', linestyle='--', alpha=0.5, linewidth=1)
        ax1.set_xlabel('Frecuencia (Hz)')
        ax1.set_ylabel('Potencia')
        ax1.set_title('Espectro de potencia LISA TDI - Armónicos de f₀')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfico 2: SNR de detecciones
        target_freqs = [d['target_frequency'] for d in results['detections']]
        snr_values = [d['snr_estimated'] for d in results['detections']]
        colors = ['green' if d['significant'] else 'orange' 
                 for d in results['detections']]
        
        ax2.bar(range(len(target_freqs)), snr_values, color=colors, alpha=0.7)
        ax2.axhline(6, color='red', linestyle='--', label='Umbral SNR = 6')
        ax2.set_xlabel('Índice de armónico')
        ax2.set_ylabel('SNR estimado')
        ax2.set_title('SNR de armónicos detectados')
        ax2.set_xticks(range(len(target_freqs)))
        ax2.set_xticklabels([f"{f:.4f}" for f in target_freqs], rotation=45)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plot_file = output_path / "lisa_search_plot.png"
        plt.savefig(plot_file, dpi=150, bbox_inches='tight')
        print(f"📊 Gráfico guardado en: {plot_file}")
        plt.close()


def main():
    """Función principal para ejecutar el pipeline LISA."""
    
    # Crear pipeline con parámetros de LISA Pathfinder
    pipeline = LISASearchPipeline(
        sample_rate=10.0,      # 10 Hz
        duration=86400.0       # 1 día de observación
    )
    
    # Ejecutar búsqueda dirigida
    results = pipeline.run_targeted_search(
        n_harmonics=10,
        save_results=True,
        output_dir="lisa_results"
    )
    
    # Generar visualizaciones
    pipeline.plot_results(results, output_dir="lisa_results")
    
    print("\n" + "=" * 60)
    print("INTERPRETACIÓN")
    print("=" * 60)
    print("\nSi existe coherencia gravitacional en el campo noésico,")
    print("aparecerá un pico estacionario en alguno de los armónicos")
    print(f"descendentes de f₀ = {F0} Hz.")
    print("\nEste análisis proporciona un método de falsación directa")
    print("para la predicción de estructura armónica del modelo GQN.")
    

if __name__ == "__main__":
    main()
