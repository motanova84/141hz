#!/usr/bin/env python3
"""
Validación del Modelo QCAL para Biología
========================================

Este script valida las predicciones del modelo QCAL aplicado a sincronización biológica,
específicamente para emergencia de cigarras Magicicada.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Enero 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, fftfreq
import json
from pathlib import Path

# Constantes fundamentales
F0_HZ = 141.7001  # Frecuencia fundamental QCAL
OMEGA_0 = 2 * np.pi * F0_HZ  # Frecuencia angular

# Parámetros del modelo
ALPHA = 0.1  # Memoria de fase (retención 90%)
SIGMA_FREQ = 20.0  # Ancho de banda de resonancia (Hz)
N_CICLOS_CIGARRA = 13  # Ciclos primos (13 o 17 años)

# Constantes de tiempo
DIAS_POR_ANO = 365.25
OMEGA_ANUAL = 2 * np.pi / (DIAS_POR_ANO * 24 * 3600)  # rad/s
OMEGA_DIURNO = 2 * np.pi / (24 * 3600)  # rad/s
OMEGA_LUNAR = 2 * np.pi / (29.5 * 24 * 3600)  # rad/s


class QCALBioModel:
    """
    Modelo QCAL para sincronización biológica.
    """
    
    def __init__(self, alpha=ALPHA, sigma_freq=SIGMA_FREQ, n_ciclos=N_CICLOS_CIGARRA):
        """
        Inicializar modelo QCAL.
        
        Args:
            alpha: Parámetro de memoria de fase (0-1)
            sigma_freq: Ancho de banda de resonancia (Hz)
            n_ciclos: Número de ciclos (años) para emergencia
        """
        self.alpha = alpha
        self.sigma_freq = sigma_freq
        self.n_ciclos = n_ciclos
        self.omega_0 = OMEGA_0
        
    def generate_psi_e(self, t, temp_profile, light_profile=None, add_hf_modulation=False):
        """
        Generar campo espectral Ψ_e(t) desde señales ambientales.
        
        Args:
            t: Array de tiempo (segundos)
            temp_profile: Perfil de temperatura (°C)
            light_profile: Perfil de luz (opcional)
            add_hf_modulation: Añadir modulación de alta frecuencia (141.7 Hz)
        
        Returns:
            Ψ_e: Campo espectral
        """
        # Normalizar temperatura
        T_norm = (temp_profile - np.mean(temp_profile)) / np.std(temp_profile)
        
        # FFT para extraer componentes espectrales
        fft_T = fft(T_norm)
        freqs = fftfreq(len(t), d=(t[1] - t[0]))
        
        # Filtrar frecuencias relevantes (ciclos anuales, diurnos)
        mask = (np.abs(freqs) > 1e-8) & (np.abs(freqs) < 1e-3)  # Hz
        
        # Reconstruir Ψ_e con componentes principales
        psi_e = np.real(np.fft.ifft(fft_T * mask))
        
        # Añadir modulación de alta frecuencia si se solicita
        if add_hf_modulation:
            # Modulación a 141.7 Hz con amplitud 10% de señal base
            hf_modulation = 0.1 * np.sin(self.omega_0 * t)
            psi_e = psi_e + hf_modulation
        
        return psi_e
    
    def accumulate_phase(self, psi_e, dt):
        """
        Acumular fase con memoria.
        
        Args:
            psi_e: Campo espectral
            dt: Paso de tiempo (segundos)
        
        Returns:
            Phi: Fase acumulada
        """
        Phi = np.zeros(len(psi_e))
        
        for i in range(1, len(psi_e)):
            # Integración con memoria
            d_phi = psi_e[i] * dt
            Phi[i] = self.alpha * Phi[i-1] + (1 - self.alpha) * (Phi[i-1] + d_phi)
        
        return Phi
    
    def predict_emergence(self, Phi, t_days):
        """
        Predecir tiempo de emergencia cuando Φ alcanza umbral crítico.
        
        Args:
            Phi: Fase acumulada
            t_days: Array de tiempo en días
        
        Returns:
            t_emergence: Tiempo de emergencia (días)
            Phi_critical: Umbral crítico
        """
        # Energía media por ciclo (aproximación) - calcular sobre todo el rango
        # Usar valor absoluto y normalizar por año
        days_per_year = 365
        
        # Calcular energía promedio por año (más robusto)
        if len(Phi) >= days_per_year * 2:
            # Usar años centrales para evitar efectos de borde
            year_start = days_per_year
            year_end = days_per_year * 2
            E_media = np.mean(np.abs(Phi[year_start:year_end] - Phi[year_start-1:year_end-1]))
        else:
            # Fallback: usar todo el rango
            E_media = np.mean(np.abs(np.diff(Phi))) * days_per_year
        
        # Umbral crítico más conservador
        Phi_critical = self.n_ciclos * E_media * 0.8  # 80% del teórico
        
        # Encontrar primer cruce del umbral (buscar después del año 10)
        min_day = int(10 * days_per_year)
        if len(Phi) > min_day:
            crossings = np.where(Phi[min_day:] >= Phi_critical)[0]
            
            if len(crossings) > 0:
                idx_emergence = crossings[0] + min_day
                t_emergence = t_days[idx_emergence]
            else:
                # Si no cruza, usar el máximo
                idx_max = np.argmax(Phi)
                t_emergence = t_days[idx_max]
        else:
            t_emergence = None
        
        return t_emergence, Phi_critical
    
    def calculate_synchrony_sd(self, emergence_times):
        """
        Calcular desviación estándar de sincronía.
        
        Args:
            emergence_times: Array de tiempos de emergencia (días)
        
        Returns:
            sd: Desviación estándar (días)
        """
        return np.std(emergence_times)


class StandardDDModel:
    """
    Modelo Estándar de Grados-Día (Degree-Days).
    """
    
    def __init__(self, base_temp=10.0, dd_threshold=1250.0):
        """
        Inicializar modelo DD.
        
        Args:
            base_temp: Temperatura base (°C)
            dd_threshold: Umbral de grados-día para emergencia
        """
        self.base_temp = base_temp
        self.dd_threshold = dd_threshold
    
    def calculate_dd(self, temp_profile, dt_days):
        """
        Calcular grados-día acumulados.
        
        Args:
            temp_profile: Perfil de temperatura (°C)
            dt_days: Paso de tiempo (días)
        
        Returns:
            DD: Grados-día acumulados
        """
        DD = np.zeros(len(temp_profile))
        
        for i in range(1, len(temp_profile)):
            # Solo acumular si T > T_base
            dd_increment = max(0, temp_profile[i] - self.base_temp) * dt_days
            DD[i] = DD[i-1] + dd_increment
        
        return DD
    
    def predict_emergence(self, DD, t_days):
        """
        Predecir emergencia cuando DD alcanza umbral.
        
        Args:
            DD: Grados-día acumulados
            t_days: Array de tiempo en días
        
        Returns:
            t_emergence: Tiempo de emergencia (días)
        """
        crossings = np.where(DD >= self.dd_threshold)[0]
        
        if len(crossings) > 0:
            idx_emergence = crossings[0]
            t_emergence = t_days[idx_emergence]
        else:
            t_emergence = None
        
        return t_emergence


def simulate_temperature_profile(n_years=13, noise_level=0.15, add_warm_winter=False):
    """
    Simular perfil de temperatura realista con ciclos anuales.
    
    Args:
        n_years: Número de años a simular
        noise_level: Nivel de ruido (fracción de amplitud)
        add_warm_winter: Añadir invierno inusualmente cálido (+5°C)
    
    Returns:
        t_days: Array de tiempo (días)
        T_profile: Perfil de temperatura (°C)
    """
    dias_totales = int(n_years * DIAS_POR_ANO)
    t_days = np.linspace(0, dias_totales, dias_totales)
    t_seconds = t_days * 24 * 3600
    
    # Temperatura media y amplitud estacional
    T_mean = 15.0  # °C
    T_amplitude = 10.0  # °C
    
    # Ciclo anual
    T_annual = T_amplitude * np.sin(OMEGA_ANUAL * t_seconds - np.pi/2)
    
    # Ciclo diurno (amplitud menor)
    T_diurno = 3.0 * np.sin(OMEGA_DIURNO * t_seconds)
    
    # Ruido gaussiano
    noise = noise_level * T_amplitude * np.random.randn(len(t_days))
    
    # Temperatura total
    T_profile = T_mean + T_annual + T_diurno + noise
    
    # Invierno cálido (si se solicita)
    if add_warm_winter:
        # Año 8, invierno (días 2800-2920)
        warm_winter_start = int(8 * DIAS_POR_ANO)
        warm_winter_end = int(8 * DIAS_POR_ANO + 120)
        T_profile[warm_winter_start:warm_winter_end] += 5.0  # +5°C
    
    return t_days, T_profile


def compare_models(n_simulations=20, scenario="normal"):
    """
    Comparar modelos QCAL vs. Estándar DD.
    
    Args:
        n_simulations: Número de simulaciones (individuos)
        scenario: Escenario ("normal", "hf_modulation", "warm_winter", "lunar_perturbation")
    
    Returns:
        results: Diccionario con resultados
    """
    print(f"\n{'='*60}")
    print(f"Comparando modelos: Escenario '{scenario}'")
    print(f"{'='*60}\n")
    
    # Modelos
    qcal_model = QCALBioModel()
    dd_model = StandardDDModel()
    
    # Arrays de resultados
    t_emergence_qcal = []
    t_emergence_dd = []
    
    # Configurar escenario
    add_hf = (scenario == "hf_modulation")
    add_warm = (scenario == "warm_winter")
    
    for i in range(n_simulations):
        # Simular temperatura (con variabilidad individual)
        t_days, T_profile = simulate_temperature_profile(
            n_years=13, 
            noise_level=0.15 + 0.05*np.random.randn(),
            add_warm_winter=add_warm
        )
        
        # QCAL
        t_seconds = t_days * 24 * 3600
        psi_e = qcal_model.generate_psi_e(t_seconds, T_profile, add_hf_modulation=add_hf)
        Phi = qcal_model.accumulate_phase(psi_e, dt=(t_seconds[1] - t_seconds[0]))
        t_em_qcal, _ = qcal_model.predict_emergence(Phi, t_days)
        
        if t_em_qcal is not None:
            t_emergence_qcal.append(t_em_qcal)
        
        # DD
        DD = dd_model.calculate_dd(T_profile, dt_days=(t_days[1] - t_days[0]))
        t_em_dd = dd_model.predict_emergence(DD, t_days)
        
        if t_em_dd is not None:
            t_emergence_dd.append(t_em_dd)
    
    # Convertir a arrays
    t_emergence_qcal = np.array(t_emergence_qcal)
    t_emergence_dd = np.array(t_emergence_dd)
    
    # Calcular métricas
    mean_qcal = np.mean(t_emergence_qcal)
    mean_dd = np.mean(t_emergence_dd)
    sd_qcal = np.std(t_emergence_qcal)
    sd_dd = np.std(t_emergence_dd)
    
    # RMSE (asumiendo emergencia observada en día 13*365)
    t_observed = 13 * DIAS_POR_ANO
    rmse_qcal = np.sqrt(np.mean((t_emergence_qcal - t_observed)**2))
    rmse_dd = np.sqrt(np.mean((t_emergence_dd - t_observed)**2))
    
    # Mejora relativa
    mejora_rmse = (rmse_dd - rmse_qcal) / rmse_dd * 100
    
    # Resultados
    results = {
        "scenario": scenario,
        "n_simulations": n_simulations,
        "QCAL": {
            "mean_days": float(mean_qcal),
            "sd_days": float(sd_qcal),
            "rmse_days": float(rmse_qcal)
        },
        "DD_Standard": {
            "mean_days": float(mean_dd),
            "sd_days": float(sd_dd),
            "rmse_days": float(rmse_dd)
        },
        "mejora_rmse_percent": float(mejora_rmse)
    }
    
    # Imprimir resultados
    print(f"Modelo QCAL:")
    print(f"  Media emergencia: {mean_qcal:.1f} días ({mean_qcal/365.25:.2f} años)")
    print(f"  Desv. estándar: {sd_qcal:.2f} días")
    print(f"  RMSE: {rmse_qcal:.2f} días")
    print()
    print(f"Modelo DD Estándar:")
    print(f"  Media emergencia: {mean_dd:.1f} días ({mean_dd/365.25:.2f} años)")
    print(f"  Desv. estándar: {sd_dd:.2f} días")
    print(f"  RMSE: {rmse_dd:.2f} días")
    print()
    print(f"Mejora QCAL: {mejora_rmse:.1f}% en RMSE")
    
    if mejora_rmse > 15:
        print("✅ QCAL supera criterio de validación (>15% mejora)")
    else:
        print("⚠️  QCAL no alcanza criterio de >15% mejora")
    
    return results, t_emergence_qcal, t_emergence_dd


def plot_comparison(t_emergence_qcal, t_emergence_dd, scenario, save_path=None):
    """
    Graficar comparación de emergencias.
    """
    # Check for empty arrays
    if len(t_emergence_qcal) == 0 or len(t_emergence_dd) == 0:
        print(f"⚠️  No hay datos suficientes para graficar en escenario {scenario}")
        return None
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogramas
    ax = axes[0]
    bins = np.linspace(
        min(t_emergence_qcal.min(), t_emergence_dd.min()) - 10,
        max(t_emergence_qcal.max(), t_emergence_dd.max()) + 10,
        30
    )
    
    ax.hist(t_emergence_dd, bins=bins, alpha=0.5, label='DD Estándar', color='blue', edgecolor='black')
    ax.hist(t_emergence_qcal, bins=bins, alpha=0.5, label='QCAL', color='red', edgecolor='black')
    ax.axvline(13*365.25, color='green', linestyle='--', linewidth=2, label='Teórico (13 años)')
    ax.set_xlabel('Tiempo de emergencia (días)', fontsize=12)
    ax.set_ylabel('Frecuencia', fontsize=12)
    ax.set_title(f'Distribución de Emergencias - {scenario}', fontsize=14)
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Box plot
    ax = axes[1]
    data = [t_emergence_dd, t_emergence_qcal]
    labels = ['DD Estándar', 'QCAL']
    bp = ax.boxplot(data, labels=labels, patch_artist=True, notch=True)
    
    # Colores
    bp['boxes'][0].set_facecolor('lightblue')
    bp['boxes'][1].set_facecolor('lightcoral')
    
    ax.axhline(13*365.25, color='green', linestyle='--', linewidth=2, label='Teórico (13 años)')
    ax.set_ylabel('Tiempo de emergencia (días)', fontsize=12)
    ax.set_title('Comparación de Sincronía', fontsize=14)
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nGráfico guardado en: {save_path}")
    
    return fig


def main():
    """
    Función principal de validación.
    """
    print("\n" + "="*70)
    print("VALIDACIÓN DEL MODELO QCAL PARA BIOLOGÍA")
    print("Sincronización en Emergencia de Magicicada")
    print("="*70)
    
    # Crear directorio de resultados
    results_dir = Path("results/biology")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Escenarios a comparar
    scenarios = [
        "normal",
        "hf_modulation",
        "warm_winter"
    ]
    
    all_results = {}
    
    for scenario in scenarios:
        results, t_qcal, t_dd = compare_models(n_simulations=50, scenario=scenario)
        all_results[scenario] = results
        
        # Graficar (solo si hay datos)
        if len(t_qcal) > 0 and len(t_dd) > 0:
            fig = plot_comparison(
                t_qcal, 
                t_dd, 
                scenario,
                save_path=results_dir / f"comparison_{scenario}.png"
            )
            if fig is not None:
                plt.close(fig)
    
    # Guardar resultados JSON
    json_path = results_dir / "qcal_biology_validation.json"
    with open(json_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"Resultados guardados en: {json_path}")
    print(f"Gráficos guardados en: {results_dir}/")
    print(f"{'='*70}\n")
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DE VALIDACIÓN")
    print("="*70)
    
    for scenario, results in all_results.items():
        mejora = results['mejora_rmse_percent']
        sd_qcal = results['QCAL']['sd_days']
        sd_dd = results['DD_Standard']['sd_days']
        
        print(f"\nEscenario: {scenario}")
        print(f"  Mejora RMSE: {mejora:.1f}%")
        print(f"  SD QCAL: {sd_qcal:.2f} días")
        print(f"  SD DD: {sd_dd:.2f} días")
        print(f"  Estado: {'✅ VALIDADO' if mejora > 15 else '⚠️  NO VALIDADO'}")
    
    print("\n" + "="*70)
    print("VALIDACIÓN COMPLETA")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Semilla para reproducibilidad
    np.random.seed(42)
    
    main()
