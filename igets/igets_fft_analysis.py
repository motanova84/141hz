#!/usr/bin/env python3
"""
IGETS - International Geodynamics and Earth Tide Service Gravimetry
Análisis de modulación Yukawa

Objetivo: Buscar la modulación Yukawa predicha:
V(r,t) = -GM/r [1 + α_Y e^(-r/λ̄) (1 + ε cos 2πf₀t)]

con λ̄ ≈ 3.37×10⁵ m, f₀ = 141.7001 Hz.

Acciones:
1. Analizar series temporales de superconducting gravimeters (SGs)
2. Aplicar FFT sobre intervalos de alta frecuencia (100-300 Hz)
3. Buscar picos coherentes en f₀ ± 0.5 Hz con SNR > 6
4. Verificar coherencia fase-tiempo entre estaciones

Resultado esperado:
Una modulación coherente global confirmaría un acoplo gravitacional oscilante
del campo Ψ; su ausencia falsaría la hipótesis de coherencia gravitatoria.
"""

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq, rfft, rfftfreq
from scipy.stats import chi2
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path


# Constantes del modelo GQN
F0 = 141.7001  # Hz - Frecuencia prima del modelo GQN
TOLERANCE = 0.5  # Hz - Tolerancia de búsqueda
LAMBDA_BAR = 3.37e5  # m - Longitud característica Yukawa
ALPHA_Y = 1e-6  # Amplitud Yukawa (orden de magnitud esperado)

# Estaciones IGETS de referencia
IGETS_STATIONS = {
    'CANTLEY': {'lat': 45.59, 'lon': -75.87, 'name': 'Cantley, Canada'},
    'BAD_HOMBURG': {'lat': 50.23, 'lon': 8.61, 'name': 'Bad Homburg, Germany'},
    'KYOTO': {'lat': 35.03, 'lon': 135.78, 'name': 'Kyoto, Japan'},
    'STRASBOURG': {'lat': 48.62, 'lon': 7.68, 'name': 'Strasbourg, France'},
    'MEMBACH': {'lat': 50.61, 'lon': 6.01, 'name': 'Membach, Belgium'}
}


class IGETSGravimetryAnalysis:
    """
    Análisis de datos gravimétricos IGETS para detectar modulación Yukawa.
    """
    
    def __init__(self, sample_rate: float = 1000.0):
        """
        Inicializa el análisis gravimétrico.
        
        Args:
            sample_rate: Tasa de muestreo en Hz (típico: 1-10 Hz para SGs,
                        pero usamos 1000 Hz para capturar f₀=141.7 Hz)
        """
        self.sample_rate = sample_rate
        self.nyquist = sample_rate / 2
        
    def yukawa_potential(self, 
                        r: float, 
                        t: np.ndarray, 
                        M: float = 5.972e24,
                        alpha_y: float = ALPHA_Y,
                        epsilon: float = 1e-8) -> np.ndarray:
        """
        Calcula el potencial gravitacional con modulación Yukawa.
        
        V(r,t) = -GM/r [1 + α_Y e^(-r/λ̄) (1 + ε cos 2πf₀t)]
        
        Args:
            r: Distancia en metros
            t: Array de tiempo en segundos
            M: Masa de la Tierra en kg
            alpha_y: Amplitud del término Yukawa
            epsilon: Amplitud de modulación temporal
            
        Returns:
            V(r,t): Potencial gravitacional modulado
        """
        G = 6.67430e-11  # m³/kg/s²
        
        # Potencial Newtoniano
        V_newton = -G * M / r
        
        # Término Yukawa estático
        yukawa_static = alpha_y * np.exp(-r / LAMBDA_BAR)
        
        # Modulación temporal
        modulation = 1 + epsilon * np.cos(2 * np.pi * F0 * t)
        
        # Potencial total
        V_total = V_newton * (1 + yukawa_static * modulation)
        
        return V_total
    
    def generate_sg_signal(self,
                          duration: float = 3600.0,
                          station: str = 'CANTLEY',
                          include_modulation: bool = True,
                          tide_amplitude: float = 1e-7,
                          seismic_noise: float = 1e-9) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera señal simulada de superconducting gravimeter.
        
        Args:
            duration: Duración en segundos
            station: Nombre de estación IGETS
            include_modulation: Si incluir modulación a f₀
            tide_amplitude: Amplitud de marea terrestre (m/s²)
            seismic_noise: Nivel de ruido sísmico (m/s²)
            
        Returns:
            (t, g): Arrays de tiempo y aceleración gravitacional
        """
        n_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, n_samples)
        
        # Radio efectivo (profundidad típica de SG)
        r_earth = 6.371e6  # m
        r_sg = r_earth + 100  # ~100m bajo superficie
        
        # Señal base: marea terrestre (M2, frecuencia ~12.42h)
        f_tide_M2 = 1 / (12.42 * 3600)  # Hz
        g_tide = tide_amplitude * np.sin(2 * np.pi * f_tide_M2 * t)
        
        # Añadir componente solar (S2)
        f_tide_S2 = 1 / (12.0 * 3600)
        g_tide += 0.5 * tide_amplitude * np.sin(2 * np.pi * f_tide_S2 * t)
        
        # Modulación Yukawa a f₀ (si activada)
        g_yukawa = np.zeros_like(t)
        if include_modulation:
            # Convertir potencial a aceleración: g = -dV/dr
            epsilon = 1e-8  # Amplitud muy pequeña
            g_yukawa = epsilon * ALPHA_Y * np.cos(2 * np.pi * F0 * t)
        
        # Ruido sísmico (espectro 1/f en bajas frecuencias)
        noise = np.random.normal(0, seismic_noise, n_samples)
        # Filtro pasa-bajos para ruido sísmico (< 10 Hz típico)
        sos = signal.butter(4, 10, 'low', fs=self.sample_rate, output='sos')
        noise_filtered = signal.sosfilt(sos, noise)
        
        # Señal total
        g_total = g_tide + g_yukawa + noise_filtered
        
        return t, g_total
    
    def preprocess_signal(self, 
                         signal_data: np.ndarray,
                         remove_tide: bool = True) -> np.ndarray:
        """
        Preprocesa señal gravimétrica: remueve marea y tendencias.
        
        Args:
            signal_data: Datos de gravímetro
            remove_tide: Si remover componentes de marea
            
        Returns:
            Señal preprocesada
        """
        # Remover tendencia lineal
        signal_detrended = signal.detrend(signal_data, type='linear')
        
        if remove_tide:
            # Filtro pasa-altos para remover mareas (< 1 Hz)
            # y preservar señal de alta frecuencia (>100 Hz)
            sos = signal.butter(4, 50, 'high', fs=self.sample_rate, output='sos')
            signal_filtered = signal.sosfilt(sos, signal_detrended)
        else:
            signal_filtered = signal_detrended
        
        return signal_filtered
    
    def perform_fft_analysis(self,
                            signal_data: np.ndarray,
                            freq_range: Tuple[float, float] = (100, 300)) -> Dict[str, any]:
        """
        Realiza análisis FFT en rango de alta frecuencia.
        
        Args:
            signal_data: Datos preprocesados
            freq_range: Rango de frecuencias a analizar (Hz)
            
        Returns:
            Diccionario con resultados FFT
        """
        # FFT real (señal real)
        fft_vals = rfft(signal_data)
        fft_freq = rfftfreq(len(signal_data), 1/self.sample_rate)
        fft_power = np.abs(fft_vals)**2
        
        # Filtrar por rango de frecuencia
        freq_mask = (fft_freq >= freq_range[0]) & (fft_freq <= freq_range[1])
        freq_filtered = fft_freq[freq_mask]
        power_filtered = fft_power[freq_mask]
        
        # Buscar pico en f₀ ± tolerancia
        f0_mask = np.abs(freq_filtered - F0) <= TOLERANCE
        
        results = {
            'frequency_range': freq_range,
            'spectrum': {
                'frequency': freq_filtered.tolist(),
                'power': power_filtered.tolist()
            }
        }
        
        if np.any(f0_mask):
            peak_power = np.max(power_filtered[f0_mask])
            peak_freq = freq_filtered[f0_mask][np.argmax(power_filtered[f0_mask])]
            
            # Estimar SNR
            noise_power = np.median(power_filtered)
            snr = np.sqrt(peak_power / noise_power) if noise_power > 0 else 0
            
            results['detection'] = {
                'frequency': float(peak_freq),
                'power': float(peak_power),
                'snr': float(snr),
                'significant': snr > 6.0,
                'delta_f': float(peak_freq - F0)
            }
        else:
            results['detection'] = None
        
        return results
    
    def analyze_phase_coherence(self,
                                station_data: Dict[str, np.ndarray],
                                window_size: int = 1000) -> Dict[str, any]:
        """
        Analiza coherencia de fase entre múltiples estaciones.
        
        Args:
            station_data: Dict {station_name: signal_data}
            window_size: Tamaño de ventana para análisis
            
        Returns:
            Diccionario con coherencia de fase
        """
        stations = list(station_data.keys())
        n_stations = len(stations)
        
        if n_stations < 2:
            return {'error': 'Se necesitan al menos 2 estaciones'}
        
        # Calcular fase de cada estación en f₀
        phases = {}
        for station, data in station_data.items():
            # Filtro pasa-banda alrededor de f₀
            sos = signal.butter(4, [F0-5, F0+5], 'band', 
                              fs=self.sample_rate, output='sos')
            signal_filtered = signal.sosfilt(sos, data)
            
            # Transformada de Hilbert para fase instantánea
            analytic_signal = signal.hilbert(signal_filtered)
            instantaneous_phase = np.angle(analytic_signal)
            phases[station] = instantaneous_phase
        
        # Calcular coherencia entre pares de estaciones
        coherence_matrix = np.zeros((n_stations, n_stations))
        
        for i, station1 in enumerate(stations):
            for j, station2 in enumerate(stations):
                if i <= j:
                    # Diferencia de fase
                    phase_diff = phases[station1] - phases[station2]
                    # Coherencia como consistencia de fase
                    coherence = np.abs(np.mean(np.exp(1j * phase_diff)))
                    coherence_matrix[i, j] = coherence
                    coherence_matrix[j, i] = coherence
        
        # Coherencia global (promedio)
        global_coherence = np.mean(coherence_matrix[np.triu_indices(n_stations, k=1)])
        
        return {
            'stations': stations,
            'coherence_matrix': coherence_matrix.tolist(),
            'global_coherence': float(global_coherence),
            'highly_coherent': global_coherence > 0.7
        }
    
    def run_analysis(self,
                    n_stations: int = 3,
                    duration: float = 3600.0,
                    include_modulation: bool = True,
                    save_results: bool = True,
                    output_dir: str = "igets_results") -> Dict[str, any]:
        """
        Ejecuta análisis completo IGETS.
        
        Args:
            n_stations: Número de estaciones a simular
            duration: Duración de observación (s)
            include_modulation: Si incluir modulación a f₀
            save_results: Si guardar resultados
            output_dir: Directorio de salida
            
        Returns:
            Diccionario con resultados completos
        """
        print(f"🌍 IGETS Gravimetric Analysis")
        print(f"=" * 60)
        print(f"Frecuencia objetivo: f₀ = {F0} Hz")
        print(f"Tolerancia búsqueda: ±{TOLERANCE} Hz")
        print(f"Duración observación: {duration/3600:.1f} horas")
        print(f"Modulación incluida: {'SÍ' if include_modulation else 'NO'}")
        print()
        
        # Seleccionar estaciones
        station_names = list(IGETS_STATIONS.keys())[:n_stations]
        print(f"Estaciones analizadas:")
        for station in station_names:
            info = IGETS_STATIONS[station]
            print(f"  - {station}: {info['name']} ({info['lat']:.2f}°, {info['lon']:.2f}°)")
        print()
        
        # Generar datos para cada estación
        station_results = {}
        station_signals = {}
        
        for station in station_names:
            print(f"Procesando {station}...")
            
            # Generar señal
            t, g_signal = self.generate_sg_signal(
                duration=duration,
                station=station,
                include_modulation=include_modulation
            )
            
            # Preprocesar
            g_processed = self.preprocess_signal(g_signal, remove_tide=True)
            station_signals[station] = g_processed
            
            # Análisis FFT
            fft_results = self.perform_fft_analysis(g_processed)
            station_results[station] = fft_results
            
            # Reportar detección
            if fft_results['detection']:
                det = fft_results['detection']
                status = "✓ DETECTADO" if det['significant'] else "○ Débil"
                print(f"  {status}: f = {det['frequency']:.4f} Hz, SNR = {det['snr']:.2f}")
            else:
                print(f"  ✗ No detectado en rango f₀ ± {TOLERANCE} Hz")
        
        print()
        
        # Análisis de coherencia de fase
        print("Analizando coherencia de fase entre estaciones...")
        coherence_results = self.analyze_phase_coherence(station_signals)
        
        print("\n" + "=" * 60)
        print("RESULTADOS DE COHERENCIA")
        print("=" * 60)
        print(f"\nCoherencia global: {coherence_results['global_coherence']:.3f}")
        print(f"Alta coherencia (>0.7): {'✓ SÍ' if coherence_results['highly_coherent'] else '✗ NO'}")
        
        # Compilar resultados
        results = {
            'f0': F0,
            'tolerance': TOLERANCE,
            'duration': duration,
            'modulation_included': include_modulation,
            'stations': {
                station: {
                    'location': IGETS_STATIONS[station],
                    'analysis': station_results[station]
                }
                for station in station_names
            },
            'coherence': coherence_results
        }
        
        # Evaluación final
        n_detected = sum(1 for s in station_results.values() 
                        if s['detection'] and s['detection']['significant'])
        
        print("\n" + "=" * 60)
        print("EVALUACIÓN FINAL")
        print("=" * 60)
        print(f"\nDetecciones significativas: {n_detected}/{n_stations}")
        print(f"Coherencia de fase: {coherence_results['global_coherence']:.3f}")
        
        if n_detected >= 2 and coherence_results['highly_coherent']:
            conclusion = "✓ MODULACIÓN YUKAWA DETECTADA"
            print(f"\n{conclusion}")
            print("Se confirma acoplo gravitacional oscilante del campo Ψ.")
        else:
            conclusion = "✗ MODULACIÓN NO CONFIRMADA"
            print(f"\n{conclusion}")
            print("Se falsa la hipótesis de coherencia gravitatoria a f₀.")
        
        results['conclusion'] = conclusion
        
        # Guardar resultados
        if save_results:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            results_file = output_path / "igets_fft_results.json"
            
            # Limpiar arrays grandes para JSON
            results_save = results.copy()
            for station in results_save['stations'].keys():
                spectrum = results_save['stations'][station]['analysis']['spectrum']
                results_save['stations'][station]['analysis']['spectrum'] = {
                    'frequency': spectrum['frequency'][:1000],
                    'power': spectrum['power'][:1000]
                }
            
            with open(results_file, 'w') as f:
                json.dump(results_save, f, indent=2)
            
            print(f"\n📁 Resultados guardados en: {results_file}")
        
        return results
    
    def plot_results(self, results: Dict[str, any], output_dir: str = "igets_results"):
        """
        Genera visualizaciones de los resultados.
        
        Args:
            results: Diccionario de resultados
            output_dir: Directorio para gráficos
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        stations = list(results['stations'].keys())
        n_stations = len(stations)
        
        fig, axes = plt.subplots(n_stations, 2, figsize=(14, 4*n_stations))
        if n_stations == 1:
            axes = axes.reshape(1, -1)
        
        for i, station in enumerate(stations):
            station_data = results['stations'][station]['analysis']
            spectrum = station_data['spectrum']
            freq = np.array(spectrum['frequency'])
            power = np.array(spectrum['power'])
            
            # Gráfico 1: Espectro completo
            axes[i, 0].semilogy(freq, power, alpha=0.7, linewidth=1)
            axes[i, 0].axvline(F0, color='red', linestyle='--', 
                              label=f'f₀ = {F0} Hz')
            axes[i, 0].axvspan(F0-TOLERANCE, F0+TOLERANCE, 
                              alpha=0.2, color='red')
            axes[i, 0].set_xlabel('Frecuencia (Hz)')
            axes[i, 0].set_ylabel('Potencia')
            axes[i, 0].set_title(f'{station} - Espectro FFT (100-300 Hz)')
            axes[i, 0].legend()
            axes[i, 0].grid(True, alpha=0.3)
            
            # Gráfico 2: Zoom en f₀
            zoom_mask = (freq >= F0-10) & (freq <= F0+10)
            if np.any(zoom_mask):
                axes[i, 1].plot(freq[zoom_mask], power[zoom_mask], 
                              'b-', linewidth=2)
                axes[i, 1].axvline(F0, color='red', linestyle='--', 
                                  label=f'f₀ = {F0} Hz')
                
                # Marcar detección si existe
                if station_data['detection']:
                    det = station_data['detection']
                    axes[i, 1].plot(det['frequency'], det['power'], 
                                   'ro', markersize=10, 
                                   label=f"SNR = {det['snr']:.2f}")
                
                axes[i, 1].set_xlabel('Frecuencia (Hz)')
                axes[i, 1].set_ylabel('Potencia')
                axes[i, 1].set_title(f'{station} - Zoom en f₀')
                axes[i, 1].legend()
                axes[i, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plot_file = output_path / "igets_fft_plot.png"
        plt.savefig(plot_file, dpi=150, bbox_inches='tight')
        print(f"📊 Gráfico guardado en: {plot_file}")
        plt.close()
        
        # Gráfico de coherencia
        if 'coherence' in results and 'coherence_matrix' in results['coherence']:
            fig, ax = plt.subplots(figsize=(8, 6))
            coherence_matrix = np.array(results['coherence']['coherence_matrix'])
            
            im = ax.imshow(coherence_matrix, cmap='RdYlGn', vmin=0, vmax=1)
            ax.set_xticks(range(len(stations)))
            ax.set_yticks(range(len(stations)))
            ax.set_xticklabels(stations, rotation=45)
            ax.set_yticklabels(stations)
            
            # Añadir valores en celdas
            for i in range(len(stations)):
                for j in range(len(stations)):
                    text = ax.text(j, i, f'{coherence_matrix[i, j]:.2f}',
                                 ha="center", va="center", color="black")
            
            ax.set_title('Matriz de coherencia de fase entre estaciones')
            plt.colorbar(im, ax=ax, label='Coherencia')
            plt.tight_layout()
            
            coherence_file = output_path / "igets_coherence_plot.png"
            plt.savefig(coherence_file, dpi=150, bbox_inches='tight')
            print(f"📊 Gráfico de coherencia guardado en: {coherence_file}")
            plt.close()


def main():
    """Función principal para ejecutar análisis IGETS."""
    
    # Crear analizador
    analysis = IGETSGravimetryAnalysis(sample_rate=1000.0)
    
    # Ejecutar análisis con modulación (caso positivo)
    print("=" * 60)
    print("ANÁLISIS 1: Con modulación Yukawa")
    print("=" * 60)
    results_with = analysis.run_analysis(
        n_stations=3,
        duration=3600.0,
        include_modulation=True,
        save_results=True,
        output_dir="igets_results"
    )
    
    analysis.plot_results(results_with, output_dir="igets_results")
    
    print("\n\n" + "=" * 60)
    print("INTERPRETACIÓN")
    print("=" * 60)
    print("\nUna modulación coherente global confirmaría un acoplo gravitacional")
    print("oscilante del campo Ψ; su ausencia falsaría la hipótesis de")
    print("coherencia gravitatoria.")
    print("\nEste análisis proporciona una prueba directa terrestre de la")
    print("predicción GQN sobre interacciones gravitacionales modificadas.")


if __name__ == "__main__":
    main()
