#!/usr/bin/env python3
"""
Análisis de AT2020afhd - Tidal Disruption Event con Precesión Lense-Thirring

Este script procesa y analiza datos de AT2020afhd para:
1. Visualizar curvas de luz X-ray y radio
2. Calcular periodogramas (Lomb-Scargle)
3. Ajustar modelo de precesión Lense-Thirring
4. Comparar con predicciones teóricas del marco QCAL ∞³

Referencias:
- Periodo observado: ~19.6-20 días
- Mecanismo: Precesión Lense-Thirring (relatividad general)
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit
from astropy.timeseries import LombScargle
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def lense_thirring_precession_model(t, A, omega, phi, offset):
    """
    Modelo simple de precesión Lense-Thirring
    
    Parameters:
    -----------
    t : array
        Tiempo (días)
    A : float
        Amplitud de la oscilación
    omega : float
        Frecuencia angular (rad/día)
    phi : float
        Fase inicial (rad)
    offset : float
        Nivel base de flujo
    
    Returns:
    --------
    flux : array
        Flujo modelado como función sinusoidal
    """
    return A * np.sin(omega * t + phi) + offset


def analyze_lightcurve(time, flux, flux_err, label="X-ray", color='blue'):
    """
    Analiza una curva de luz: periodograma y ajuste de modelo
    
    Returns:
    --------
    results : dict
        Diccionario con resultados del análisis
    """
    print(f"\n{'='*60}")
    print(f"Análisis de curva de luz: {label}")
    print(f"{'='*60}")
    
    # Basic statistics
    print(f"Número de observaciones: {len(time)}")
    print(f"Rango temporal: {time.min():.2f} - {time.max():.2f} MJD")
    print(f"Duración: {time.max() - time.min():.1f} días")
    print(f"Flujo medio: {flux.mean():.4e} ± {flux.std():.4e}")
    
    # Lomb-Scargle periodogram
    print(f"\nCalculando periodograma Lomb-Scargle...")
    
    # Convert time to relative days from start
    t_rel = time - time.min()
    
    # Calculate periodogram
    frequency, power = LombScargle(t_rel, flux, flux_err).autopower(
        minimum_frequency=1/100,  # Up to 100 days
        maximum_frequency=1/5,     # Down to 5 days
        samples_per_peak=10
    )
    period = 1 / frequency
    
    # Find peak period
    peak_idx = np.argmax(power)
    peak_period = period[peak_idx]
    peak_power = power[peak_idx]
    
    print(f"Periodo dominante: {peak_period:.2f} días (potencia: {peak_power:.3f})")
    
    # Fit Lense-Thirring precession model
    print(f"\nAjustando modelo de precesión Lense-Thirring...")
    
    # Initial guess
    A_guess = (flux.max() - flux.min()) / 2
    period_guess = peak_period
    omega_guess = 2 * np.pi / period_guess
    phi_guess = 0.0
    offset_guess = flux.mean()
    
    p0 = [A_guess, omega_guess, phi_guess, offset_guess]
    
    try:
        # Fit the model
        params, covariance = curve_fit(
            lense_thirring_precession_model, 
            t_rel, 
            flux, 
            p0=p0,
            sigma=flux_err,
            absolute_sigma=True,
            maxfev=10000
        )
        
        A_fit, omega_fit, phi_fit, offset_fit = params
        period_fit = 2 * np.pi / omega_fit
        
        # Calculate errors
        perr = np.sqrt(np.diag(covariance))
        A_err, omega_err, phi_err, offset_err = perr
        period_err = period_fit * omega_err / omega_fit
        
        print(f"\nParámetros ajustados:")
        print(f"  Amplitud: {A_fit:.4e} ± {A_err:.4e}")
        print(f"  Periodo: {period_fit:.2f} ± {period_err:.2f} días")
        print(f"  Fase: {phi_fit:.3f} ± {phi_err:.3f} rad")
        print(f"  Offset: {offset_fit:.4e} ± {offset_err:.4e}")
        
        # Calculate chi-squared
        model_flux = lense_thirring_precession_model(t_rel, *params)
        chi2 = np.sum(((flux - model_flux) / flux_err)**2)
        dof = len(flux) - len(params)
        reduced_chi2 = chi2 / dof
        
        print(f"  χ² reducido: {reduced_chi2:.3f}")
        
        fit_success = True
        
    except Exception as e:
        print(f"Error en ajuste: {e}")
        params = None
        covariance = None
        fit_success = False
        period_fit = peak_period
        reduced_chi2 = np.nan
    
    # Compile results
    results = {
        'label': label,
        'color': color,
        'n_obs': len(time),
        'time': time,
        'time_rel': t_rel,
        'flux': flux,
        'flux_err': flux_err,
        'flux_mean': float(flux.mean()),
        'flux_std': float(flux.std()),
        'periodogram': {
            'frequency': frequency,
            'period': period,
            'power': power,
            'peak_period': float(peak_period),
            'peak_power': float(peak_power)
        },
        'fit': {
            'success': fit_success,
            'params': params.tolist() if params is not None else None,
            'period': float(period_fit),
            'reduced_chi2': float(reduced_chi2) if not np.isnan(reduced_chi2) else None
        }
    }
    
    return results


def plot_lightcurves(xray_results, radio_results, output_dir):
    """Plot light curves for both X-ray and radio"""
    print(f"\nGenerando gráfico de curvas de luz...")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # X-ray light curve
    ax1.errorbar(xray_results['time'], xray_results['flux'], 
                yerr=xray_results['flux_err'],
                fmt='o', color=xray_results['color'], alpha=0.6,
                label='Swift X-ray', markersize=6)
    
    # Add fit if available
    if xray_results['fit']['success']:
        t_model = np.linspace(xray_results['time_rel'].min(), 
                             xray_results['time_rel'].max(), 300)
        flux_model = lense_thirring_precession_model(t_model, 
                                                     *xray_results['fit']['params'])
        ax1.plot(xray_results['time'].min() + t_model, flux_model, 
                'r-', linewidth=2, alpha=0.8,
                label=f'Modelo L-T (P={xray_results["fit"]["period"]:.1f}d)')
    
    ax1.set_ylabel('Flujo X-ray (cts/s)', fontsize=11)
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_title('AT2020afhd - Curvas de Luz Multi-longitud de Onda', 
                 fontsize=13, fontweight='bold')
    
    # Radio light curve
    ax2.errorbar(radio_results['time'], radio_results['flux'], 
                yerr=radio_results['flux_err'],
                fmt='s', color=radio_results['color'], alpha=0.6,
                label='VLA Radio', markersize=6)
    
    # Add fit if available
    if radio_results['fit']['success']:
        t_model = np.linspace(radio_results['time_rel'].min(), 
                             radio_results['time_rel'].max(), 300)
        flux_model = lense_thirring_precession_model(t_model, 
                                                     *radio_results['fit']['params'])
        ax2.plot(radio_results['time'].min() + t_model, flux_model, 
                'orange', linewidth=2, alpha=0.8,
                label=f'Modelo L-T (P={radio_results["fit"]["period"]:.1f}d)')
    
    ax2.set_xlabel('Tiempo (MJD)', fontsize=11)
    ax2.set_ylabel('Flujo Radio (mJy)', fontsize=11)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_file = output_dir / 'at2020afhd_lightcurves.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico guardado: {output_file}")
    
    return output_file


def plot_periodograms(xray_results, radio_results, output_dir):
    """Plot periodograms for both X-ray and radio"""
    print(f"\nGenerando gráfico de periodogramas...")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # X-ray periodogram
    period_xray = xray_results['periodogram']['period']
    power_xray = xray_results['periodogram']['power']
    peak_period_xray = xray_results['periodogram']['peak_period']
    
    ax1.plot(period_xray, power_xray, color=xray_results['color'], 
            linewidth=2, label='X-ray')
    ax1.axvline(peak_period_xray, color='red', linestyle='--', 
               label=f'Pico: {peak_period_xray:.1f}d', linewidth=2)
    ax1.axvline(20, color='black', linestyle=':', alpha=0.5,
               label='Esperado: ~20d')
    ax1.set_ylabel('Potencia (X-ray)', fontsize=11)
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_title('AT2020afhd - Periodogramas Lomb-Scargle', 
                 fontsize=13, fontweight='bold')
    
    # Radio periodogram
    period_radio = radio_results['periodogram']['period']
    power_radio = radio_results['periodogram']['power']
    peak_period_radio = radio_results['periodogram']['peak_period']
    
    ax2.plot(period_radio, power_radio, color=radio_results['color'], 
            linewidth=2, label='Radio')
    ax2.axvline(peak_period_radio, color='orange', linestyle='--', 
               label=f'Pico: {peak_period_radio:.1f}d', linewidth=2)
    ax2.axvline(20, color='black', linestyle=':', alpha=0.5,
               label='Esperado: ~20d')
    ax2.set_xlabel('Periodo (días)', fontsize=11)
    ax2.set_ylabel('Potencia (Radio)', fontsize=11)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_file = output_dir / 'at2020afhd_periodograms.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico guardado: {output_file}")
    
    return output_file


def plot_combined_analysis(xray_results, radio_results, output_dir):
    """Create combined analysis figure"""
    print(f"\nGenerando análisis combinado...")
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # Top: Light curves
    ax1 = fig.add_subplot(gs[0, :])
    ax1.errorbar(xray_results['time'], xray_results['flux'], 
                yerr=xray_results['flux_err'],
                fmt='o', color='blue', alpha=0.6, label='X-ray (Swift)', markersize=5)
    
    # Scale radio to match for visual comparison
    radio_scaled = radio_results['flux'] / radio_results['flux'].max() * xray_results['flux'].max()
    ax1_twin = ax1.twinx()
    ax1_twin.errorbar(radio_results['time'], radio_results['flux'],
                     yerr=radio_results['flux_err'],
                     fmt='s', color='orange', alpha=0.6, label='Radio (VLA)', markersize=5)
    
    ax1.set_ylabel('Flujo X-ray (cts/s)', color='blue', fontsize=11)
    ax1_twin.set_ylabel('Flujo Radio (mJy)', color='orange', fontsize=11)
    ax1.set_xlabel('Tiempo (MJD)', fontsize=11)
    ax1.set_title('AT2020afhd - Análisis Multi-longitud de Onda', 
                 fontsize=14, fontweight='bold')
    ax1.legend(loc='upper left')
    ax1_twin.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Middle left: X-ray periodogram
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(xray_results['periodogram']['period'], 
            xray_results['periodogram']['power'],
            color='blue', linewidth=2)
    ax2.axvline(xray_results['periodogram']['peak_period'], 
               color='red', linestyle='--', linewidth=2)
    ax2.axvline(20, color='black', linestyle=':', alpha=0.5)
    ax2.set_xlabel('Periodo (días)', fontsize=10)
    ax2.set_ylabel('Potencia', fontsize=10)
    ax2.set_title(f'Periodograma X-ray (pico: {xray_results["periodogram"]["peak_period"]:.1f}d)', 
                 fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # Middle right: Radio periodogram
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(radio_results['periodogram']['period'], 
            radio_results['periodogram']['power'],
            color='orange', linewidth=2)
    ax3.axvline(radio_results['periodogram']['peak_period'], 
               color='red', linestyle='--', linewidth=2)
    ax3.axvline(20, color='black', linestyle=':', alpha=0.5)
    ax3.set_xlabel('Periodo (días)', fontsize=10)
    ax3.set_ylabel('Potencia', fontsize=10)
    ax3.set_title(f'Periodograma Radio (pico: {radio_results["periodogram"]["peak_period"]:.1f}d)', 
                 fontsize=11)
    ax3.grid(True, alpha=0.3)
    
    # Bottom left: X-ray fit
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.errorbar(xray_results['time_rel'], xray_results['flux'], 
                yerr=xray_results['flux_err'],
                fmt='o', color='blue', alpha=0.5, markersize=4, label='Datos')
    if xray_results['fit']['success']:
        t_model = np.linspace(0, xray_results['time_rel'].max(), 300)
        flux_model = lense_thirring_precession_model(t_model, 
                                                     *xray_results['fit']['params'])
        ax4.plot(t_model, flux_model, 'r-', linewidth=2, 
                label=f'Modelo L-T (χ²ᵣ={xray_results["fit"]["reduced_chi2"]:.2f})')
    ax4.set_xlabel('Días desde inicio', fontsize=10)
    ax4.set_ylabel('Flujo X-ray', fontsize=10)
    ax4.set_title(f'Ajuste X-ray: P={xray_results["fit"]["period"]:.1f}d', fontsize=11)
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)
    
    # Bottom right: Radio fit
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.errorbar(radio_results['time_rel'], radio_results['flux'], 
                yerr=radio_results['flux_err'],
                fmt='s', color='orange', alpha=0.5, markersize=4, label='Datos')
    if radio_results['fit']['success']:
        t_model = np.linspace(0, radio_results['time_rel'].max(), 300)
        flux_model = lense_thirring_precession_model(t_model, 
                                                     *radio_results['fit']['params'])
        ax5.plot(t_model, flux_model, 'r-', linewidth=2, 
                label=f'Modelo L-T (χ²ᵣ={radio_results["fit"]["reduced_chi2"]:.2f})')
    ax5.set_xlabel('Días desde inicio', fontsize=10)
    ax5.set_ylabel('Flujo Radio', fontsize=10)
    ax5.set_title(f'Ajuste Radio: P={radio_results["fit"]["period"]:.1f}d', fontsize=11)
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3)
    
    # Save figure
    output_file = output_dir / 'at2020afhd_combined_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico guardado: {output_file}")
    plt.close()
    
    return output_file


def save_results(xray_results, radio_results, output_dir):
    """Save analysis results to JSON"""
    print(f"\nGuardando resultados del análisis...")
    
    # Prepare summary
    summary = {
        'object': 'AT2020afhd',
        'analysis_type': 'Lense-Thirring Precession',
        'xray': {
            'n_observations': xray_results['n_obs'],
            'flux_mean': xray_results['flux_mean'],
            'flux_std': xray_results['flux_std'],
            'peak_period_days': xray_results['periodogram']['peak_period'],
            'peak_power': xray_results['periodogram']['peak_power'],
            'fit_period_days': xray_results['fit']['period'],
            'fit_chi2_reduced': xray_results['fit']['reduced_chi2']
        },
        'radio': {
            'n_observations': radio_results['n_obs'],
            'flux_mean': radio_results['flux_mean'],
            'flux_std': radio_results['flux_std'],
            'peak_period_days': radio_results['periodogram']['peak_period'],
            'peak_power': radio_results['periodogram']['peak_power'],
            'fit_period_days': radio_results['fit']['period'],
            'fit_chi2_reduced': radio_results['fit']['reduced_chi2']
        },
        'interpretation': {
            'precession_mechanism': 'Lense-Thirring (General Relativity)',
            'expected_period_days': 20.0,
            'xray_deviation_percent': abs(xray_results['fit']['period'] - 20.0) / 20.0 * 100,
            'radio_deviation_percent': abs(radio_results['fit']['period'] - 20.0) / 20.0 * 100,
            'multi_wavelength_consistent': abs(xray_results['fit']['period'] - 
                                                radio_results['fit']['period']) < 2.0
        }
    }
    
    # Save JSON
    output_file = output_dir / 'at2020afhd_results.json'
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✓ Resultados guardados: {output_file}")
    
    # Print summary
    print(f"\n{'='*60}")
    print("RESUMEN DE RESULTADOS")
    print(f"{'='*60}")
    print(f"\nPeriodos detectados:")
    print(f"  X-ray:  {summary['xray']['fit_period_days']:.2f} días")
    print(f"  Radio:  {summary['radio']['fit_period_days']:.2f} días")
    print(f"  Esperado: ~20 días (Lense-Thirring)")
    print(f"\nDesviaciones del valor esperado:")
    print(f"  X-ray:  {summary['interpretation']['xray_deviation_percent']:.1f}%")
    print(f"  Radio:  {summary['interpretation']['radio_deviation_percent']:.1f}%")
    print(f"\nConsistencia multi-longitud de onda: " + 
          ("✓ SÍ" if summary['interpretation']['multi_wavelength_consistent'] else "✗ NO"))
    
    return summary


def main():
    """Main analysis function"""
    parser = argparse.ArgumentParser(
        description="Analizar AT2020afhd - Tidal Disruption Event",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--data-dir', type=str, 
                       default='data/tde/at2020afhd',
                       help='Directorio con datos de AT2020afhd')
    parser.add_argument('--output-dir', type=str,
                       default='results/at2020afhd',
                       help='Directorio para resultados')
    parser.add_argument('--no-plots', action='store_true',
                       help='No generar gráficos (solo análisis)')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("AT2020afhd - Análisis de Precesión Lense-Thirring")
    print("="*60)
    
    # Setup paths
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    
    data_dir = project_dir / args.data_dir
    output_dir = project_dir / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nDirectorio de datos: {data_dir}")
    print(f"Directorio de salida: {output_dir}")
    
    # Load X-ray data
    xray_file = data_dir / 'xray' / 'swift_xray_at2020afhd.csv'
    if not xray_file.exists():
        print(f"\n⚠ Error: No se encuentra {xray_file}")
        print("Ejecutar primero: python scripts/descargar_at2020afhd.py")
        return 1
    
    print(f"\nCargando datos X-ray: {xray_file}")
    df_xray = pd.read_csv(xray_file)
    
    # Load radio data
    radio_file = data_dir / 'radio' / 'vla_radio_at2020afhd.csv'
    if not radio_file.exists():
        print(f"\n⚠ Error: No se encuentra {radio_file}")
        print("Ejecutar primero: python scripts/descargar_at2020afhd.py")
        return 1
    
    print(f"Cargando datos radio: {radio_file}")
    df_radio = pd.read_csv(radio_file)
    
    # Analyze X-ray light curve
    xray_results = analyze_lightcurve(
        df_xray['time_mjd'].values,
        df_xray['flux'].values,
        df_xray['flux_error'].values,
        label="X-ray",
        color='blue'
    )
    
    # Analyze radio light curve
    radio_results = analyze_lightcurve(
        df_radio['time_mjd'].values,
        df_radio['flux_mjy'].values,
        df_radio['flux_error_mjy'].values,
        label="Radio",
        color='orange'
    )
    
    # Generate plots
    if not args.no_plots:
        plot_lightcurves(xray_results, radio_results, output_dir)
        plot_periodograms(xray_results, radio_results, output_dir)
        plot_combined_analysis(xray_results, radio_results, output_dir)
    
    # Save results
    summary = save_results(xray_results, radio_results, output_dir)
    
    print(f"\n{'='*60}")
    print("✓ Análisis completado exitosamente")
    print(f"{'='*60}")
    print(f"\nResultados guardados en: {output_dir}")
    print(f"\nArchivos generados:")
    print(f"  - at2020afhd_results.json")
    if not args.no_plots:
        print(f"  - at2020afhd_lightcurves.png")
        print(f"  - at2020afhd_periodograms.png")
        print(f"  - at2020afhd_combined_analysis.png")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
