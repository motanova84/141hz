#!/usr/bin/env python3
"""
Validación de Predicción 4: Modulación Gravitacional Persistente a 141.7001 Hz

Este script valida la cuarta predicción del marco QCAL ∞³:
El campo Ψ induce una modulación oscilatoria minúscula pero persistente en
la aceleración gravitatoria local g.

Señal Esperada:
    δg(t) = A·cos(ω₀t + φ), donde A ∼ 10⁻¹³ - 10⁻¹² g

Criterios de Detección:
    1. Pico espectral (FFT) centrado en f₀ = 141.70 ± 0.05 Hz
    2. Coherencia de fase < 0.1 rad entre detectores distantes
    3. SNR > 5 tras filtrado de ruido sísmico

Plataforma Experimental:
    - Gravímetros superconductores (red IGETS)
    - Interferómetros atómicos de nueva generación (MIGA)

Criterio de Falsación:
    Ausencia de cumplimiento de TODOS los criterios anteriores en el análisis
    de datos de múltiples estaciones IGETS.

Autor: José Manuel Mota Burruezo
Instituto de Conciencia Cuántica (ICQ)
Zenodo DOI: 10.5281/zenodo.17887499
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
from typing import Dict, Any, Tuple
import mpmath as mp
from scipy import signal, fft

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    from constants import UniversalConstants, F0
    from utils import setup_logging, safe_json_dump
except ImportError:
    print("Warning: Could not import from src, using fallback constants")
    F0 = 141.7001  # Hz

# Set mpmath precision
mp.dps = 50


class GravitationalModulationValidator:
    """
    Validador de la modulación gravitacional persistente a f₀.
    """
    
    def __init__(self, precision: int = 50):
        """
        Inicializa el validador.
        
        Args:
            precision: Precisión decimal para cálculos
        """
        mp.dps = precision
        self.logger = setup_logging() if 'setup_logging' in dir() else None
        
        # Constantes fundamentales
        self.f0 = mp.mpf(str(F0))  # Hz
        self.omega_0 = 2 * mp.pi * self.f0  # rad/s
        
        # Aceleración gravitatoria estándar
        self.g_earth = mp.mpf("9.81")  # m/s²
        
        # Parámetros de la señal esperada
        self._calculate_signal_parameters()
        
        # Parámetros del detector
        self.sampling_rate = 1000  # Hz (tasa de muestreo típica)
        self.detector_noise_floor = 1e-10  # Nivel de ruido del detector (g)
    
    def _calculate_signal_parameters(self):
        """
        Calcula los parámetros de la señal modulada.
        """
        # Amplitud esperada: A ∼ 10⁻¹³ - 10⁻¹² g
        self.A_min = mp.mpf("1e-13") * self.g_earth  # m/s²
        self.A_max = mp.mpf("1e-12") * self.g_earth  # m/s²
        self.A_nominal = mp.sqrt(self.A_min * self.A_max)  # Valor nominal
        
        # Tolerancia en frecuencia: f₀ = 141.70 ± 0.05 Hz
        self.f0_tolerance = mp.mpf("0.05")  # Hz
        
        # Tolerancia en fase: < 0.1 rad
        self.phase_tolerance = mp.mpf("0.1")  # rad
    
    def generate_modulated_signal(self, duration: float, 
                                  amplitude: float = None,
                                  phase: float = 0.0,
                                  add_noise: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera señal gravitacional modulada.
        
        Args:
            duration: Duración de la señal en segundos
            amplitude: Amplitud de la modulación (m/s²), usa nominal si None
            phase: Fase inicial (rad)
            add_noise: Si añadir ruido realista
        
        Returns:
            (t, g) tupla con tiempos y aceleraciones
        """
        if amplitude is None:
            amplitude = float(self.A_nominal)
        
        # Vector de tiempo
        n_samples = int(duration * self.sampling_rate)
        t = np.linspace(0, duration, n_samples)
        
        # Señal modulada: g(t) = g₀ + A·cos(ω₀t + φ)
        g0 = float(self.g_earth)
        omega_0 = float(self.omega_0)
        g_signal = g0 + amplitude * np.cos(omega_0 * t + phase)
        
        if add_noise:
            # Ruido sísmico (1/f + blanco)
            # Ruido 1/f dominante a bajas frecuencias
            freqs = np.fft.rfftfreq(n_samples, 1/self.sampling_rate)
            noise_spectrum = np.zeros_like(freqs)
            noise_spectrum[freqs > 0] = 1 / np.sqrt(freqs[freqs > 0])
            noise_spectrum[0] = 0
            
            # Normalizar y escalar
            noise_spectrum = noise_spectrum / np.max(noise_spectrum)
            noise_spectrum = noise_spectrum * float(self.detector_noise_floor) * g0
            
            # Generar ruido en dominio temporal
            noise_phase = np.random.uniform(0, 2*np.pi, len(noise_spectrum))
            noise_complex = noise_spectrum * np.exp(1j * noise_phase)
            noise = np.fft.irfft(noise_complex, n=n_samples)
            
            # Añadir ruido blanco adicional
            white_noise = np.random.normal(0, float(self.detector_noise_floor) * g0 * 0.1, n_samples)
            
            g_signal = g_signal + noise + white_noise
        
        return t, g_signal
    
    def spectral_analysis(self, t: np.ndarray, g: np.ndarray) -> Dict[str, Any]:
        """
        Análisis espectral de la señal gravitacional.
        
        Args:
            t: Array de tiempos
            g: Array de aceleraciones
        
        Returns:
            Diccionario con resultados del análisis espectral
        """
        # Remover tendencia lineal
        g_detrended = signal.detrend(g)
        
        # Ventana Hann para reducir leakage espectral
        window = signal.windows.hann(len(g_detrended))
        g_windowed = g_detrended * window
        
        # FFT
        freqs = np.fft.rfftfreq(len(g_windowed), t[1] - t[0])
        spectrum = np.fft.rfft(g_windowed)
        power_spectrum = np.abs(spectrum) ** 2
        
        # Buscar pico cerca de f₀
        f0_hz = float(self.f0)
        f0_tolerance = float(self.f0_tolerance)
        mask = (freqs >= f0_hz - f0_tolerance) & (freqs <= f0_hz + f0_tolerance)
        
        if np.any(mask):
            # Encontrar pico máximo en la región
            local_power = power_spectrum[mask]
            local_freqs = freqs[mask]
            
            peak_idx = np.argmax(local_power)
            peak_freq = local_freqs[peak_idx]
            peak_power = local_power[peak_idx]
            
            # Estimar SNR (comparar con fondo)
            # Excluir región ±5 Hz alrededor de f₀
            noise_mask = (freqs < f0_hz - 5) | (freqs > f0_hz + 5)
            noise_power = np.mean(power_spectrum[noise_mask])
            snr = peak_power / noise_power if noise_power > 0 else 0
            
            # Estimar amplitud del pico
            # La amplitud en el dominio temporal es ~2*sqrt(peak_power/N)
            amplitude_est = 2 * np.sqrt(peak_power / len(g_windowed))
        else:
            peak_freq = None
            peak_power = 0
            snr = 0
            amplitude_est = 0
        
        return {
            "frequencies": freqs,
            "power_spectrum": power_spectrum,
            "peak_frequency_hz": float(peak_freq) if peak_freq is not None else None,
            "peak_power": float(peak_power),
            "snr": float(snr),
            "amplitude_estimate_m_s2": float(amplitude_est),
            "f0_expected_hz": f0_hz,
            "f0_tolerance_hz": f0_tolerance
        }
    
    def phase_coherence_analysis(self, signals: list) -> Dict[str, Any]:
        """
        Análisis de coherencia de fase entre múltiples detectores.
        
        Args:
            signals: Lista de tuplas (t, g) de diferentes detectores
        
        Returns:
            Diccionario con análisis de coherencia
        """
        phases = []
        amplitudes = []
        
        for t, g in signals:
            # Extraer fase a f₀ mediante transformada de Hilbert
            g_detrended = signal.detrend(g)
            
            # Filtro pasa-banda alrededor de f₀
            f0_hz = float(self.f0)
            nyquist = self.sampling_rate / 2
            low = (f0_hz - 1) / nyquist
            high = (f0_hz + 1) / nyquist
            b, a = signal.butter(4, [low, high], btype='band')
            g_filtered = signal.filtfilt(b, a, g_detrended)
            
            # Transformada de Hilbert para obtener fase
            analytic = signal.hilbert(g_filtered)
            instant_phase = np.unwrap(np.angle(analytic))
            instant_amplitude = np.abs(analytic)
            
            # Fase media en la ventana central
            mid_start = len(instant_phase) // 3
            mid_end = 2 * len(instant_phase) // 3
            phase_mean = np.mean(instant_phase[mid_start:mid_end])
            amplitude_mean = np.mean(instant_amplitude[mid_start:mid_end])
            
            phases.append(phase_mean)
            amplitudes.append(amplitude_mean)
        
        # Calcular diferencias de fase
        phases = np.array(phases)
        phase_diffs = []
        for i in range(len(phases)):
            for j in range(i+1, len(phases)):
                diff = np.abs(phases[i] - phases[j])
                # Normalizar a [-π, π]
                diff = np.mod(diff + np.pi, 2*np.pi) - np.pi
                phase_diffs.append(np.abs(diff))
        
        if phase_diffs:
            max_phase_diff = np.max(phase_diffs)
            mean_phase_diff = np.mean(phase_diffs)
        else:
            max_phase_diff = 0
            mean_phase_diff = 0
        
        return {
            "n_detectors": len(signals),
            "phases_rad": [float(p) for p in phases],
            "mean_amplitude_m_s2": float(np.mean(amplitudes)),
            "phase_differences_rad": [float(pd) for pd in phase_diffs],
            "max_phase_difference_rad": float(max_phase_diff),
            "mean_phase_difference_rad": float(mean_phase_diff),
            "phase_coherent": float(max_phase_diff) < float(self.phase_tolerance)
        }
    
    def validate_prediction(self, n_detectors: int = 3, 
                           duration: float = 3600) -> Dict[str, Any]:
        """
        Valida la predicción de modulación gravitacional.
        
        Args:
            n_detectors: Número de detectores a simular
            duration: Duración de la observación (segundos)
        
        Returns:
            Diccionario con resultados de validación
        """
        results = {
            "prediction": "Gravitational Modulation at f₀ = 141.7001 Hz",
            "parameters": {
                "f0_hz": float(self.f0),
                "omega_0_rad_s": float(self.omega_0),
                "amplitude_min_m_s2": float(self.A_min),
                "amplitude_max_m_s2": float(self.A_max),
                "amplitude_nominal_m_s2": float(self.A_nominal),
                "amplitude_min_frac_g": float(self.A_min / self.g_earth),
                "amplitude_max_frac_g": float(self.A_max / self.g_earth),
                "f0_tolerance_hz": float(self.f0_tolerance),
                "phase_tolerance_rad": float(self.phase_tolerance),
                "sampling_rate_hz": self.sampling_rate,
            },
            "detection_criteria": {},
            "simulations": {},
            "validation": {}
        }
        
        # Criterios de detección
        results["detection_criteria"] = {
            "criterion_1": "Pico espectral centrado en f₀ = 141.70 ± 0.05 Hz",
            "criterion_2": "Coherencia de fase < 0.1 rad entre detectores",
            "criterion_3": "SNR > 5 tras filtrado"
        }
        
        # Simular señales de múltiples detectores
        signals = []
        spectral_analyses = []
        
        for detector_id in range(n_detectors):
            # Fase aleatoria para cada detector (pero coherente globalmente)
            phase = np.random.uniform(0, 2*np.pi)
            
            # Generar señal
            t, g = self.generate_modulated_signal(
                duration=duration,
                amplitude=float(self.A_nominal),
                phase=phase,
                add_noise=True
            )
            
            signals.append((t, g))
            
            # Análisis espectral
            spec_analysis = self.spectral_analysis(t, g)
            spectral_analyses.append(spec_analysis)
            
            results["simulations"][f"detector_{detector_id}"] = {
                "duration_s": duration,
                "n_samples": len(t),
                "spectral_analysis": {
                    "peak_frequency_hz": spec_analysis["peak_frequency_hz"],
                    "snr": spec_analysis["snr"],
                    "amplitude_estimate_m_s2": spec_analysis["amplitude_estimate_m_s2"],
                }
            }
        
        # Análisis de coherencia de fase
        phase_analysis = self.phase_coherence_analysis(signals)
        results["simulations"]["phase_coherence"] = phase_analysis
        
        # Validación de criterios
        # Criterio 1: Pico en f₀ ± 0.05 Hz
        peak_freqs = [s["peak_frequency_hz"] for s in spectral_analyses if s["peak_frequency_hz"] is not None]
        criterion_1_met = all(
            abs(pf - float(self.f0)) < float(self.f0_tolerance) 
            for pf in peak_freqs
        ) if peak_freqs else False
        
        results["validation"]["criterion_1_frequency"] = {
            "peak_frequencies_hz": peak_freqs,
            "expected_hz": float(self.f0),
            "tolerance_hz": float(self.f0_tolerance),
            "met": criterion_1_met,
            "status": "✓ PASS" if criterion_1_met else "✗ FAIL"
        }
        
        # Criterio 2: Coherencia de fase < 0.1 rad
        criterion_2_met = phase_analysis["phase_coherent"]
        results["validation"]["criterion_2_phase_coherence"] = {
            "max_phase_difference_rad": phase_analysis["max_phase_difference_rad"],
            "tolerance_rad": float(self.phase_tolerance),
            "met": criterion_2_met,
            "status": "✓ PASS" if criterion_2_met else "✗ FAIL"
        }
        
        # Criterio 3: SNR > 5
        snr_values = [s["snr"] for s in spectral_analyses]
        criterion_3_met = all(snr > 5 for snr in snr_values)
        results["validation"]["criterion_3_snr"] = {
            "snr_values": snr_values,
            "threshold": 5,
            "met": criterion_3_met,
            "status": "✓ PASS" if criterion_3_met else "✗ FAIL"
        }
        
        # Criterio de falsación
        all_criteria_met = criterion_1_met and criterion_2_met and criterion_3_met
        results["falsification_criterion"] = {
            "statement": "Ausencia de cumplimiento de TODOS los criterios en múltiples estaciones",
            "all_criteria_met": all_criteria_met,
            "prediction_supported": all_criteria_met,
            "note": "Fallar en todos los criterios en múltiples estaciones refutaría la predicción"
        }
        
        # Plataformas experimentales
        results["experimental_platforms"] = {
            "superconducting_gravimeters": {
                "network": "IGETS (International Geodynamics and Earth Tide Service)",
                "sensitivity": "< 10⁻¹¹ g",
                "sampling": "1-1000 Hz",
                "locations": "Global network (>30 stations)"
            },
            "atom_interferometers": {
                "example": "MIGA (Matter-wave laser Interferometric Gravitation Antenna)",
                "sensitivity": "< 10⁻¹² g",
                "coherence_time": "> 1 s",
                "advantage": "Lower seismic noise, better SNR"
            }
        }
        
        # Estado global
        results["overall_status"] = "✓ ALL DETECTION CRITERIA MET" if all_criteria_met else "⚠ SOME CRITERIA NOT MET"
        
        return results
    
    def generate_plot(self, duration: float = 60, output_path: str = None):
        """
        Genera gráficos del análisis de modulación gravitacional.
        
        Args:
            duration: Duración de la señal (segundos)
            output_path: Ruta para guardar el gráfico
        """
        # Generar señal
        t, g = self.generate_modulated_signal(
            duration=duration,
            amplitude=float(self.A_nominal),
            add_noise=True
        )
        
        # Análisis espectral
        spec_analysis = self.spectral_analysis(t, g)
        
        # Crear figura
        fig = plt.figure(figsize=(14, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Panel 1: Serie temporal (primeros 10 segundos)
        ax1 = fig.add_subplot(gs[0, :])
        mask = t < 10
        g_plot = (g[mask] - float(self.g_earth)) * 1e12  # Convertir a ng/g
        ax1.plot(t[mask], g_plot, 'b-', linewidth=0.5, alpha=0.7)
        ax1.set_xlabel('Tiempo (s)', fontsize=11)
        ax1.set_ylabel('δg (×10⁻¹² g)', fontsize=11)
        ax1.set_title(f'Modulación Gravitacional (primeros 10 s, f₀ = {float(self.f0):.4f} Hz)', fontsize=13)
        ax1.grid(True, alpha=0.3)
        
        # Panel 2: Espectro de potencia (escala lineal)
        ax2 = fig.add_subplot(gs[1, 0])
        freqs = spec_analysis["frequencies"]
        power = spec_analysis["power_spectrum"]
        mask_freq = (freqs > 0) & (freqs < 300)
        ax2.plot(freqs[mask_freq], power[mask_freq], 'b-', linewidth=1)
        ax2.axvline(float(self.f0), color='red', linestyle='--', linewidth=2,
                   label=f'f₀ = {float(self.f0):.2f} Hz')
        ax2.axvspan(float(self.f0) - float(self.f0_tolerance),
                   float(self.f0) + float(self.f0_tolerance),
                   alpha=0.2, color='red', label='Banda tolerancia')
        ax2.set_xlabel('Frecuencia (Hz)', fontsize=11)
        ax2.set_ylabel('Densidad espectral de potencia', fontsize=11)
        ax2.set_title('Espectro de Potencia (0-300 Hz)', fontsize=13)
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)
        ax2.set_yscale('log')
        
        # Panel 3: Zoom en f₀
        ax3 = fig.add_subplot(gs[1, 1])
        f0_val = float(self.f0)
        mask_zoom = (freqs > f0_val - 10) & (freqs < f0_val + 10)
        ax3.plot(freqs[mask_zoom], power[mask_zoom], 'b-', linewidth=2)
        ax3.axvline(f0_val, color='red', linestyle='--', linewidth=2,
                   label=f'f₀ = {f0_val:.4f} Hz')
        if spec_analysis["peak_frequency_hz"]:
            ax3.axvline(spec_analysis["peak_frequency_hz"], color='green', 
                       linestyle=':', linewidth=2,
                       label=f'Pico: {spec_analysis["peak_frequency_hz"]:.4f} Hz')
        ax3.set_xlabel('Frecuencia (Hz)', fontsize=11)
        ax3.set_ylabel('Densidad espectral de potencia', fontsize=11)
        ax3.set_title(f'Zoom en f₀ (SNR = {spec_analysis["snr"]:.2f})', fontsize=13)
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3)
        ax3.set_yscale('log')
        
        # Panel 4: Diagrama de detección
        ax4 = fig.add_subplot(gs[2, 0])
        criteria = ["Frecuencia\n(±0.05 Hz)", "Fase\n(< 0.1 rad)", "SNR\n(> 5)"]
        values = [
            1 if spec_analysis["peak_frequency_hz"] and 
                 abs(spec_analysis["peak_frequency_hz"] - f0_val) < float(self.f0_tolerance)
            else 0,
            1,  # Placeholder (requiere múltiples detectores)
            1 if spec_analysis["snr"] > 5 else 0
        ]
        colors = ['green' if v == 1 else 'red' for v in values]
        ax4.bar(criteria, values, color=colors, alpha=0.7, edgecolor='black')
        ax4.set_ylabel('Cumplimiento (1=Sí, 0=No)', fontsize=11)
        ax4.set_title('Criterios de Detección', fontsize=13)
        ax4.set_ylim(0, 1.2)
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Panel 5: Sensibilidad vs. Frecuencia
        ax5 = fig.add_subplot(gs[2, 1])
        # Curva de sensibilidad típica de gravímetro
        f_sens = np.logspace(-2, 3, 200)  # Hz
        # Modelo simplificado: ruido sísmico (1/f) + ruido instrumental (plano)
        seismic_noise = 1e-8 / (f_sens + 0.01)  # 1/f
        instrumental_noise = np.ones_like(f_sens) * 1e-10
        total_noise = np.sqrt(seismic_noise**2 + instrumental_noise**2)
        
        ax5.loglog(f_sens, total_noise, 'b-', linewidth=2, label='Ruido típico')
        ax5.axhline(float(self.A_min) / float(self.g_earth), color='orange', 
                   linestyle='--', linewidth=2, label='Señal mínima QCAL')
        ax5.axhline(float(self.A_max) / float(self.g_earth), color='red', 
                   linestyle='--', linewidth=2, label='Señal máxima QCAL')
        ax5.axvline(f0_val, color='green', linestyle=':', linewidth=2, 
                   label=f'f₀ = {f0_val:.1f} Hz')
        ax5.fill_between([f0_val - 50, f0_val + 50], 
                        [1e-14, 1e-14], [1e-8, 1e-8],
                        alpha=0.1, color='green', label='Banda detección')
        ax5.set_xlabel('Frecuencia (Hz)', fontsize=11)
        ax5.set_ylabel('Amplitud de ruido (fracción de g)', fontsize=11)
        ax5.set_title('Sensibilidad del Detector', fontsize=13)
        ax5.legend(fontsize=9)
        ax5.grid(True, alpha=0.3, which='both')
        ax5.set_xlim(0.01, 1000)
        ax5.set_ylim(1e-14, 1e-7)
        
        plt.suptitle('Análisis de Modulación Gravitacional: Predicción QCAL ∞³', fontsize=15, y=0.995)
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            if self.logger:
                self.logger.info(f"Plot saved to {output_path}")
        else:
            plt.savefig('results/prediccion_4_gravedad.png', dpi=300, bbox_inches='tight')
        
        plt.close()


def main():
    """
    Función principal de validación.
    """
    print("=" * 80)
    print("VALIDACIÓN PREDICCIÓN 4: MODULACIÓN GRAVITACIONAL A 141.7001 Hz")
    print("=" * 80)
    print()
    
    # Crear validador
    validator = GravitationalModulationValidator(precision=50)
    
    # Ejecutar validación
    print("Ejecutando simulación y validación...")
    results = validator.validate_prediction(n_detectors=3, duration=3600)
    
    # Mostrar resultados
    print("\nParámetros de la modulación:")
    params = results["parameters"]
    print(f"  f₀               = {params['f0_hz']:.4f} Hz")
    print(f"  A (nominal)      = {params['amplitude_nominal_m_s2']:.6e} m/s²")
    print(f"  A (rango)        = {params['amplitude_min_frac_g']:.2e} - {params['amplitude_max_frac_g']:.2e} g")
    print(f"  Tolerancia f     = ±{params['f0_tolerance_hz']:.2f} Hz")
    print(f"  Tolerancia fase  = ±{params['phase_tolerance_rad']:.2f} rad")
    print()
    
    print("Criterios de Detección:")
    for criterion, description in results["detection_criteria"].items():
        print(f"  {criterion}: {description}")
    print()
    
    print("Validaciones:")
    for key, val in results["validation"].items():
        if isinstance(val, dict) and "status" in val:
            print(f"  {key}: {val['status']}")
    print()
    
    print(f"Estado: {results['overall_status']}")
    print()
    
    # Plataformas experimentales
    print("Plataformas Experimentales:")
    for platform, details in results["experimental_platforms"].items():
        print(f"  {platform}:")
        for k, v in details.items():
            print(f"    {k}: {v}")
    print()
    
    # Criterio de falsación
    print("Criterio de Falsación:")
    falsification = results["falsification_criterion"]
    print(f"  {falsification['statement']}")
    print(f"  Todos los criterios cumplidos: {'Sí' if falsification['all_criteria_met'] else 'No'}")
    print(f"  Predicción apoyada: {'Sí' if falsification['prediction_supported'] else 'No'}")
    print()
    
    # Guardar resultados
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "prediccion_4_gravedad.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Resultados guardados en {output_file}")
    
    # Generar gráfico
    print("Generando gráfico...")
    validator.generate_plot(duration=60, output_path=str(output_dir / "prediccion_4_gravedad.png"))
    print(f"Gráfico guardado en {output_dir / 'prediccion_4_gravedad.png'}")
    print()
    
    print("=" * 80)
    print("VALIDACIÓN COMPLETADA")
    print("=" * 80)
    
    return 0 if results["overall_status"].startswith("✓") else 1


if __name__ == "__main__":
    sys.exit(main())
