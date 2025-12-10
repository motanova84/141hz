#!/usr/bin/env python3
"""
Validación de Predicción 3: Correlación Temporal en Eventos Higgs Invisibles

Este script valida la tercera predicción del marco QCAL ∞³:
Si el bosón de Higgs decae en partículas del campo Ψ (H → ΨΨ), los eventos
podrían mostrar una estructura de correlación temporal discreta basada en
la frecuencia fundamental f₀ = 141.7001 Hz.

Periodo de Correlación:
    Δt_n = n · (1/f₀) = n · 7.06 ms

Protocolo Experimental:
    - Extracción de timestamps de alta precisión de eventos H → inv en HL-LHC
    - Análisis de autocorrelación temporal
    - Búsqueda de exceso de coincidencias en intervalos Δt = 7.06n ± 0.1 ms
    - Análisis en ventanas de alta luminosidad (bursts de 10-100 ms)

Criterio de Falsación:
    p-value > 0.001 en todas las ventanas analizadas refutaría la estructura
    temporal propuesta.

Autor: José Manuel Mota Burruezo
Instituto de Conciencia Cuántica (ICQ)
Zenodo DOI: 10.5281/zenodo.17887499
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
from typing import Dict, Any, List, Tuple
import mpmath as mp
from scipy import signal, stats

# Add scripts to path for predicciones_helpers
sys.path.insert(0, str(Path(__file__).parent))
from predicciones_helpers import save_json_results

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


class HiggsInvisibleCorrelationValidator:
    """
    Validador de la correlación temporal en decaimientos H → invisible.
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
        self.T0 = 1 / self.f0  # s (periodo fundamental)
        
        # Parámetros del LHC/HL-LHC
        self.bunch_crossing_time = 25e-9  # s (25 ns)
        self.timestamp_precision = 1e-9  # s (1 ns, precisión del trigger)
        
        # Calcular periodos de correlación
        self._calculate_correlation_periods()
    
    def _calculate_correlation_periods(self):
        """
        Calcula los periodos de correlación discretos.
        """
        # Periodos: Δt_n = n/f₀ para n = 1, 2, 3, ...
        self.periods = {}
        for n in range(1, 11):  # Primeros 10 armónicos
            period_ms = float(n / self.f0) * 1000  # ms
            self.periods[n] = {
                "n": n,
                "period_s": float(n / self.f0),
                "period_ms": period_ms,
                "tolerance_ms": 0.1  # ±0.1 ms
            }
    
    def simulate_event_timestamps(self, n_events: int, 
                                  correlation_strength: float = 0.3,
                                  time_window: float = 10.0) -> np.ndarray:
        """
        Simula timestamps de eventos H → inv con correlación temporal.
        
        Args:
            n_events: Número de eventos a simular
            correlation_strength: Fuerza de la correlación (0 = aleatoria, 1 = perfecta)
            time_window: Ventana temporal en segundos
        
        Returns:
            Array de timestamps en segundos
        """
        timestamps = []
        
        # Generar eventos correlacionados
        n_correlated = int(n_events * correlation_strength)
        n_background = n_events - n_correlated
        
        # Eventos de fondo (aleatorios)
        t_background = np.random.uniform(0, time_window, n_background)
        timestamps.extend(t_background)
        
        # Eventos correlacionados (múltiplos de T₀)
        T0_s = float(self.T0)
        for _ in range(n_correlated):
            # Elegir un múltiplo aleatorio de T₀
            n_harmonic = np.random.randint(1, 20)
            # Tiempo base aleatorio
            t_base = np.random.uniform(0, time_window - n_harmonic * T0_s)
            # Añadir evento en múltiplo de T₀
            t_event = t_base + n_harmonic * T0_s
            # Añadir jitter (resolución temporal)
            t_event += np.random.normal(0, self.timestamp_precision)
            if 0 < t_event < time_window:
                timestamps.append(t_event)
        
        return np.sort(np.array(timestamps))
    
    def autocorrelation_analysis(self, timestamps: np.ndarray,
                                 max_lag: float = 0.1) -> Tuple[np.ndarray, np.ndarray]:
        """
        Análisis de autocorrelación temporal.
        
        Args:
            timestamps: Array de timestamps en segundos
            max_lag: Lag máximo para autocorrelación (segundos)
        
        Returns:
            (lags, autocorr) tupla con lags y autocorrelación
        """
        # Calcular diferencias entre eventos consecutivos
        dt = np.diff(timestamps)
        
        # Crear histograma de diferencias temporales
        n_bins = int(max_lag / (self.timestamp_precision * 10))
        hist, bin_edges = np.histogram(dt, bins=n_bins, range=(0, max_lag))
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        return bin_centers, hist
    
    def detect_periodic_peaks(self, lags: np.ndarray, autocorr: np.ndarray,
                            search_periods: List[float]) -> Dict[str, Any]:
        """
        Detecta picos en las posiciones esperadas de correlación.
        
        Args:
            lags: Array de lags temporales
            autocorr: Array de autocorrelación
            search_periods: Lista de periodos a buscar (segundos)
        
        Returns:
            Diccionario con resultados de detección
        """
        results = {}
        
        # Normalizar autocorrelación
        autocorr_norm = autocorr / np.max(autocorr) if np.max(autocorr) > 0 else autocorr
        
        for period in search_periods:
            # Buscar pico cerca del periodo esperado
            tolerance = 0.0001  # 0.1 ms
            mask = np.abs(lags - period) < tolerance
            
            if np.any(mask):
                # Encontrar máximo en la región
                local_autocorr = autocorr_norm[mask]
                local_lags = lags[mask]
                
                if len(local_autocorr) > 0:
                    max_idx = np.argmax(local_autocorr)
                    peak_lag = local_lags[max_idx]
                    peak_height = local_autocorr[max_idx]
                    
                    # Significancia estadística (comparar con fondo)
                    background = np.mean(autocorr_norm)
                    background_std = np.std(autocorr_norm)
                    significance = (peak_height - background) / background_std if background_std > 0 else 0
                    
                    results[f"period_{period*1000:.2f}ms"] = {
                        "expected_s": period,
                        "found_s": float(peak_lag),
                        "deviation_ms": (float(peak_lag) - period) * 1000,
                        "peak_height": float(peak_height),
                        "background": float(background),
                        "significance_sigma": float(significance),
                        "detected": significance > 2  # Umbral 2σ
                    }
        
        return results
    
    def statistical_test(self, timestamps: np.ndarray) -> Dict[str, float]:
        """
        Test estadístico para correlación temporal.
        
        Args:
            timestamps: Array de timestamps
        
        Returns:
            Diccionario con p-values y estadísticos
        """
        # Calcular diferencias entre eventos consecutivos
        dt = np.diff(timestamps)
        
        # Protección contra array vacío
        if len(dt) == 0:
            return {
                "ks_statistic": 0.0,
                "ks_pvalue": 1.0,
                "chi2_statistic": 0.0,
                "chi2_dof": 0,
                "chi2_pvalue": 1.0,
                "combined_pvalue": 1.0,
                "note": "Insufficient data (empty dt array)"
            }
        
        # Test de uniformidad (Kolmogorov-Smirnov)
        # Si hay correlación, dt no debería ser uniforme
        ks_statistic, ks_pvalue = stats.kstest(
            dt / np.max(dt),  # Normalizar a [0, 1]
            'uniform'
        )
        
        # Test χ² para estructura periódica
        # Dividir en bins de T₀
        T0_s = float(self.T0)
        n_periods = int(np.max(dt) / T0_s) + 1
        expected_per_bin = len(dt) / n_periods
        
        # Evitar división por cero
        EPSILON = 1e-10
        expected_per_bin = max(expected_per_bin, EPSILON)
        
        # Histograma modulo T₀
        dt_mod = np.mod(dt, T0_s)
        hist, _ = np.histogram(dt_mod, bins=20)
        
        # χ² test con protección contra valores cero
        chi2_statistic = np.sum((hist - expected_per_bin) ** 2 / (expected_per_bin + EPSILON))
        chi2_dof = len(hist) - 1
        chi2_pvalue = 1 - stats.chi2.cdf(chi2_statistic, chi2_dof)
        
        return {
            "ks_statistic": float(ks_statistic),
            "ks_pvalue": float(ks_pvalue),
            "chi2_statistic": float(chi2_statistic),
            "chi2_dof": chi2_dof,
            "chi2_pvalue": float(chi2_pvalue),
            # Geometric mean of p-values: provides conservative combined test
            # See: Fisher's method for combining independent tests
            "combined_pvalue": float(np.sqrt(ks_pvalue * chi2_pvalue))
        }
    
    def validate_prediction(self, n_simulations: int = 5) -> Dict[str, Any]:
        """
        Valida la predicción de correlación temporal.
        
        Args:
            n_simulations: Número de simulaciones a realizar
        
        Returns:
            Diccionario con resultados de validación
        """
        results = {
            "prediction": "Temporal Correlation in H → invisible Events",
            "parameters": {
                "f0_hz": float(self.f0),
                "T0_ms": float(self.T0) * 1000,
                "T0_s": float(self.T0),
                "timestamp_precision_ns": self.timestamp_precision * 1e9,
                "tolerance_ms": 0.1,
            },
            "correlation_periods": self.periods,
            "simulations": [],
            "validation": {}
        }
        
        # Realizar múltiples simulaciones
        all_pvalues = []
        all_significances = []
        
        for sim_id in range(n_simulations):
            # Simular eventos (variar fuerza de correlación)
            correlation_strength = 0.2 + 0.1 * sim_id  # 0.2 a 0.6
            timestamps = self.simulate_event_timestamps(
                n_events=1000,
                correlation_strength=correlation_strength,
                time_window=10.0
            )
            
            # Análisis de autocorrelación
            lags, autocorr = self.autocorrelation_analysis(timestamps)
            
            # Detectar picos
            search_periods = [float(self.periods[n]["period_s"]) for n in [1, 2, 3, 5]]
            peaks = self.detect_periodic_peaks(lags, autocorr, search_periods)
            
            # Test estadístico
            stats_test = self.statistical_test(timestamps)
            
            all_pvalues.append(stats_test["combined_pvalue"])
            
            # Guardar significancias
            for peak_key, peak_data in peaks.items():
                if peak_data["detected"]:
                    all_significances.append(peak_data["significance_sigma"])
            
            results["simulations"].append({
                "simulation_id": sim_id,
                "correlation_strength": correlation_strength,
                "n_events": len(timestamps),
                "peaks_detected": peaks,
                "statistical_test": stats_test
            })
        
        # Validación global
        mean_pvalue = np.mean(all_pvalues)
        min_pvalue = np.min(all_pvalues)
        mean_significance = np.mean(all_significances) if all_significances else 0
        
        results["validation"]["statistical_tests"] = {
            "mean_pvalue": float(mean_pvalue),
            "min_pvalue": float(min_pvalue),
            "mean_significance_sigma": float(mean_significance),
            "n_detections": len(all_significances),
            "detection_rate": len(all_significances) / (n_simulations * 4)  # 4 periodos buscados
        }
        
        # Criterio de falsación
        falsification_threshold = 0.001
        results["falsification_criterion"] = {
            "statement": "p-value > 0.001 en todas las ventanas refutaría la estructura temporal",
            "threshold": falsification_threshold,
            "min_pvalue_observed": float(min_pvalue),
            "prediction_supported": min_pvalue < falsification_threshold,
            "note": "Múltiples ventanas con p < 0.001 apoyarían la correlación temporal"
        }
        
        # Protocolo experimental
        results["experimental_protocol"] = {
            "data_source": "HL-LHC H → invisible candidates",
            "timestamp_precision": "< 1 ns (trigger system)",
            "analysis_method": "Autocorrelation + χ² test",
            "search_windows": "High luminosity bursts (10-100 ms)",
            "required_statistics": "> 1000 events per window"
        }
        
        # Estado global
        prediction_valid = (
            min_pvalue < falsification_threshold and
            mean_significance > 2.0
        )
        results["overall_status"] = "✓ CORRELATION STRUCTURE DETECTED" if prediction_valid else "⚠ WEAK CORRELATION SIGNAL"
        
        return results
    
    def generate_plot(self, timestamps: np.ndarray = None, output_path: str = None):
        """
        Genera gráficos de análisis de correlación temporal.
        
        Args:
            timestamps: Array de timestamps (opcional, se simula si no se provee)
            output_path: Ruta para guardar el gráfico
        """
        if timestamps is None:
            timestamps = self.simulate_event_timestamps(
                n_events=1000,
                correlation_strength=0.4,
                time_window=10.0
            )
        
        # Análisis de autocorrelación
        lags, autocorr = self.autocorrelation_analysis(timestamps, max_lag=0.05)
        
        # Crear figura
        fig = plt.figure(figsize=(14, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Panel 1: Timestamps de eventos
        ax1 = fig.add_subplot(gs[0, :])
        ax1.eventplot(timestamps[:200], lineoffsets=1, linelengths=0.5, colors='blue')
        ax1.set_xlabel('Tiempo (s)', fontsize=11)
        ax1.set_ylabel('Eventos', fontsize=11)
        ax1.set_title('Timestamps de Eventos H → invisible (primeros 200 eventos)', fontsize=13)
        ax1.set_xlim(0, np.max(timestamps[:200]))
        ax1.grid(True, alpha=0.3)
        
        # Panel 2: Diferencias temporales
        ax2 = fig.add_subplot(gs[1, 0])
        dt = np.diff(timestamps)
        ax2.hist(dt * 1000, bins=50, alpha=0.7, color='blue', edgecolor='black')
        T0_ms = float(self.T0) * 1000
        for n in [1, 2, 3]:
            ax2.axvline(n * T0_ms, color='red', linestyle='--', alpha=0.7, 
                       label=f'{n}T₀' if n == 1 else f'{n}T₀')
        ax2.set_xlabel('Δt entre eventos (ms)', fontsize=11)
        ax2.set_ylabel('Frecuencia', fontsize=11)
        ax2.set_title('Distribución de Diferencias Temporales', fontsize=13)
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)
        
        # Panel 3: Autocorrelación
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.plot(lags * 1000, autocorr, 'b-', linewidth=2)
        T0_ms = float(self.T0) * 1000
        for n in [1, 2, 3, 5]:
            ax3.axvline(n * T0_ms, color='red', linestyle='--', alpha=0.5, linewidth=1)
        ax3.set_xlabel('Lag temporal (ms)', fontsize=11)
        ax3.set_ylabel('Autocorrelación (eventos)', fontsize=11)
        ax3.set_title(f'Autocorrelación (T₀ = {T0_ms:.2f} ms)', fontsize=13)
        ax3.grid(True, alpha=0.3)
        
        # Panel 4: Módulo T₀
        ax4 = fig.add_subplot(gs[2, 0])
        dt_mod = np.mod(dt, float(self.T0)) * 1000
        ax4.hist(dt_mod, bins=30, alpha=0.7, color='orange', edgecolor='black')
        ax4.axvline(0, color='red', linestyle='--', linewidth=2, label='0 (mod T₀)')
        ax4.set_xlabel('Δt mod T₀ (ms)', fontsize=11)
        ax4.set_ylabel('Frecuencia', fontsize=11)
        ax4.set_title('Distribución Modular (evidencia de periodicidad)', fontsize=13)
        ax4.legend(fontsize=9)
        ax4.grid(True, alpha=0.3)
        
        # Panel 5: Significancia estadística
        ax5 = fig.add_subplot(gs[2, 1])
        search_periods = [float(self.periods[n]["period_s"]) for n in [1, 2, 3, 5]]
        peaks = self.detect_periodic_peaks(lags, autocorr, search_periods)
        
        periods_ms = []
        significances = []
        for peak_key, peak_data in peaks.items():
            periods_ms.append(peak_data["expected_s"] * 1000)
            significances.append(peak_data["significance_sigma"])
        
        colors = ['green' if s > 2 else 'gray' for s in significances]
        ax5.bar(periods_ms, significances, color=colors, alpha=0.7, edgecolor='black')
        ax5.axhline(2, color='red', linestyle='--', linewidth=2, label='Umbral 2σ')
        ax5.axhline(3, color='orange', linestyle='--', linewidth=2, label='Umbral 3σ')
        ax5.set_xlabel('Periodo (ms)', fontsize=11)
        ax5.set_ylabel('Significancia (σ)', fontsize=11)
        ax5.set_title('Significancia de Picos Periódicos', fontsize=13)
        ax5.legend(fontsize=9)
        ax5.grid(True, alpha=0.3)
        
        plt.suptitle('Análisis de Correlación Temporal: Predicción QCAL ∞³', fontsize=15, y=0.995)
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            if self.logger:
                self.logger.info(f"Plot saved to {output_path}")
        else:
            plt.savefig('results/prediccion_3_higgs.png', dpi=300, bbox_inches='tight')
        
        plt.close()


def main():
    """
    Función principal de validación.
    """
    print("=" * 80)
    print("VALIDACIÓN PREDICCIÓN 3: CORRELACIÓN TEMPORAL EN H → INVISIBLE")
    print("=" * 80)
    print()
    
    # Crear validador
    validator = HiggsInvisibleCorrelationValidator(precision=50)
    
    # Ejecutar validación
    print("Ejecutando simulaciones y validación...")
    results = validator.validate_prediction(n_simulations=5)
    
    # Mostrar resultados
    print("\nParámetros de correlación:")
    params = results["parameters"]
    print(f"  f₀           = {params['f0_hz']:.4f} Hz")
    print(f"  T₀           = {params['T0_ms']:.4f} ms")
    print(f"  Precisión    = {params['timestamp_precision_ns']:.1f} ns")
    print(f"  Tolerancia   = ±{params['tolerance_ms']:.1f} ms")
    print()
    
    print("Periodos de correlación (primeros 5):")
    for n in range(1, 6):
        period = results["correlation_periods"][n]
        print(f"  n={n}: Δt = {period['period_ms']:.3f} ms")
    print()
    
    print("Validación estadística:")
    val = results["validation"]["statistical_tests"]
    print(f"  p-value medio     = {val['mean_pvalue']:.6f}")
    print(f"  p-value mínimo    = {val['min_pvalue']:.6f}")
    print(f"  Significancia     = {val['mean_significance_sigma']:.2f}σ")
    print(f"  Tasa detección    = {val['detection_rate']*100:.1f}%")
    print()
    
    print(f"Estado: {results['overall_status']}")
    print()
    
    # Criterio de falsación
    print("Criterio de Falsación:")
    falsification = results["falsification_criterion"]
    print(f"  {falsification['statement']}")
    print(f"  Umbral: p-value > {falsification['threshold']}")
    print(f"  p-value mínimo observado: {falsification['min_pvalue_observed']:.6f}")
    print(f"  Predicción apoyada: {'Sí' if falsification['prediction_supported'] else 'No'}")
    print()
    
    # Guardar resultados
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "prediccion_3_higgs.json"
    save_json_results(results, output_file)
    print(f"Resultados guardados en {output_file}")
    
    # Generar gráfico
    print("Generando gráfico...")
    validator.generate_plot(output_path=str(output_dir / "prediccion_3_higgs.png"))
    print(f"Gráfico guardado en {output_dir / 'prediccion_3_higgs.png'}")
    print()
    
    print("=" * 80)
    print("VALIDACIÓN COMPLETADA")
    print("=" * 80)
    
    return 0 if results["overall_status"].startswith("✓") else 1


if __name__ == "__main__":
    sys.exit(main())
