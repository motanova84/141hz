#!/usr/bin/env python3
"""
GRACE-FO Análisis de Anomalía Gravitatoria @ 336.7m (0.1417001 Hz)

Este script analiza datos de acelerómetros GRACE-FO Level-2 RL06 buscando
la señal áurea a 0.1417001 Hz con escala característica λ=336.7 m.

Objetivo: Detectar modulación Yukawa en órbita LEO (500 km):
    g(r,t) = g₀[1 + α exp(-h/λ) cos(2πf₀t)]
    
    donde:
    - f₀ = 141.7001 Hz (frecuencia fundamental)
    - f_LEO = f₀ / 1000 = 0.1417001 Hz (modo orbital)
    - λ = 336.7 m (escala de decoherencia)
    - α = 0.05312 (amplitud Yukawa)
    - h = altitud sobre superficie

Datos: NASA PDS GRACE-FO Level-2 RL06
URL: https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=GRFO-L-ACCE-4-ACCRES-V1.0

Resultado esperado: Pico coherente 7-12 dB @ 0.1417001 Hz → 5-8σ significancia

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2026-04-06
DOI: 10.5281/zenodo.17379721
"""

import argparse
import h5py
import numpy as np
from scipy.signal import welch, butter, filtfilt
from scipy.stats import chi2
import matplotlib.pyplot as plt
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ============================================================================
# CONSTANTES FUNDAMENTALES
# ============================================================================

# Frecuencias QCAL
F0_HZ = 141.7001  # Hz - Frecuencia fundamental terrestre
F0_LEO = 0.1417001  # Hz - Modo orbital (f₀/1000)

# Parámetros Yukawa
LAMBDA_DECOH = 336.7  # m - Escala de decoherencia
ALPHA_YUKAWA = 0.05312  # Amplitud predicha (5.312%)
PHI = (1 + np.sqrt(5)) / 2  # Razón áurea

# Órbita GRACE-FO
GRACE_FO_ALTITUDE = 490e3  # m - Altitud media (490 km)
GRACE_FO_PERIOD = 94.5 * 60  # s - Período orbital (~94.5 min)
GRACE_FO_FREQ = 1 / GRACE_FO_PERIOD  # Hz - Frecuencia orbital

# Banda de análisis
FREQ_MIN = 0.01  # Hz - Límite inferior (LEO orbit band)
FREQ_MAX = 1.0   # Hz - Límite superior
NOTCH_WIDTH = 0.001  # Hz - Ancho del notch refinado

# Umbrales de significancia
SNR_THRESHOLD_DB = 5.0  # dB - Umbral mínimo
SIGMA_THRESHOLD = 5.0   # σ - Umbral estadístico (5σ descubrimiento)


# ============================================================================
# CLASE: Analizador GRACE-FO
# ============================================================================

class GRACEFOAnalyzer:
    """
    Analizador de datos GRACE-FO para detección de anomalía áurea.
    """
    
    def __init__(self, 
                 data_file: str,
                 sample_limit: int = 1000000,
                 verbose: bool = True):
        """
        Inicializa el analizador GRACE-FO.
        
        Args:
            data_file: Ruta al archivo HDF5 GRACE-FO RL06
            sample_limit: Número máximo de muestras a analizar
            verbose: Mostrar información de progreso
        """
        self.data_file = Path(data_file)
        self.sample_limit = sample_limit
        self.verbose = verbose
        
        # Datos
        self.accel_x = None
        self.accel_y = None
        self.accel_z = None
        self.time = None
        self.fs = None  # Frecuencia de muestreo
        
        # Resultados
        self.frequencies = None
        self.psd = None
        self.pico_potencia = None
        self.ruido_fondo = None
        self.significancia_db = None
        self.significancia_sigma = None
        
    def cargar_datos(self) -> bool:
        """
        Carga datos del archivo HDF5 GRACE-FO.
        
        Returns:
            True si carga exitosa, False en caso contrario
        """
        if not self.data_file.exists():
            print(f"ERROR: Archivo no encontrado: {self.data_file}")
            return False
            
        try:
            if self.verbose:
                print(f"[INFO] Cargando datos de {self.data_file}...")
                
            with h5py.File(self.data_file, 'r') as f:
                # Listar datasets disponibles
                if self.verbose:
                    print(f"[INFO] Datasets disponibles: {list(f.keys())}")
                
                # Cargar aceleración (ajustar nombres según estructura real)
                # Nombres típicos: 'accelerometer_x', 'acc_x', 'linear_acceleration'
                if 'accelerometer_x' in f:
                    self.accel_x = f['accelerometer_x'][:self.sample_limit]
                    self.accel_y = f['accelerometer_y'][:self.sample_limit]
                    self.accel_z = f['accelerometer_z'][:self.sample_limit]
                elif 'acc_x' in f:
                    self.accel_x = f['acc_x'][:self.sample_limit]
                    self.accel_y = f['acc_y'][:self.sample_limit]
                    self.accel_z = f['acc_z'][:self.sample_limit]
                else:
                    # Fallback: usar primer dataset 3D
                    keys = list(f.keys())
                    if len(keys) >= 3:
                        self.accel_x = f[keys[0]][:self.sample_limit]
                        self.accel_y = f[keys[1]][:self.sample_limit]
                        self.accel_z = f[keys[2]][:self.sample_limit]
                        if self.verbose:
                            print(f"[WARN] Usando datasets: {keys[:3]}")
                    else:
                        print(f"ERROR: No se encontraron datos de aceleración")
                        return False
                
                # Cargar tiempo
                if 'time' in f:
                    self.time = f['time'][:self.sample_limit]
                elif 'timestamp' in f:
                    self.time = f['timestamp'][:self.sample_limit]
                else:
                    # Generar tiempo sintético
                    if self.verbose:
                        print("[WARN] No hay datos de tiempo, generando sintético")
                    self.time = np.arange(len(self.accel_x))
                    
            # Calcular frecuencia de muestreo
            dt = np.mean(np.diff(self.time))
            self.fs = 1.0 / dt
            
            if self.verbose:
                print(f"[OK] Datos cargados:")
                print(f"     Muestras: {len(self.accel_x):,}")
                print(f"     Duración: {self.time[-1] - self.time[0]:.2f} s")
                print(f"     Frecuencia muestreo: {self.fs:.4f} Hz")
                print(f"     Aceleración X: [{np.min(self.accel_x):.2e}, {np.max(self.accel_x):.2e}] m/s²")
                
            return True
            
        except Exception as e:
            print(f"ERROR al cargar datos: {e}")
            return False
            
    def aplicar_filtro_bandpass(self, 
                                data: np.ndarray,
                                lowcut: float = FREQ_MIN,
                                highcut: float = FREQ_MAX,
                                order: int = 4) -> np.ndarray:
        """
        Aplica filtro pasa-banda Butterworth.
        
        Args:
            data: Serie temporal a filtrar
            lowcut: Frecuencia de corte inferior (Hz)
            highcut: Frecuencia de corte superior (Hz)
            order: Orden del filtro
            
        Returns:
            Serie temporal filtrada
        """
        nyquist = self.fs / 2
        low = lowcut / nyquist
        high = highcut / nyquist
        
        b, a = butter(order, [low, high], btype='band')
        filtered = filtfilt(b, a, data)
        
        if self.verbose:
            print(f"[INFO] Filtro pasa-banda aplicado: [{lowcut}, {highcut}] Hz")
            
        return filtered
        
    def calcular_psd(self, 
                     data: np.ndarray,
                     nperseg: int = 4096) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula densidad espectral de potencia (PSD) usando método de Welch.
        
        Args:
            data: Serie temporal
            nperseg: Longitud de segmento para Welch
            
        Returns:
            (frecuencias, psd)
        """
        frequencies, psd = welch(data, 
                                self.fs, 
                                nperseg=nperseg,
                                scaling='density')
        
        if self.verbose:
            print(f"[INFO] PSD calculado con Welch (nperseg={nperseg})")
            print(f"     Resolución frecuencial: {frequencies[1] - frequencies[0]:.6f} Hz")
            
        return frequencies, psd
        
    def analizar_pico_aureo(self) -> Dict:
        """
        Analiza pico @ f₀_LEO = 0.1417001 Hz.
        
        Returns:
            Diccionario con resultados del análisis
        """
        # Filtrar datos
        accel_filtered = self.aplicar_filtro_bandpass(self.accel_x)
        
        # Calcular PSD
        self.frequencies, self.psd = self.calcular_psd(accel_filtered)
        
        # Máscara del notch refinado
        notch_mask = np.abs(self.frequencies - F0_LEO) < NOTCH_WIDTH
        
        if not np.any(notch_mask):
            print(f"ERROR: No hay datos en banda [{F0_LEO - NOTCH_WIDTH}, {F0_LEO + NOTCH_WIDTH}] Hz")
            return {}
        
        # Potencia del pico
        self.pico_potencia = np.max(self.psd[notch_mask])
        freq_pico = self.frequencies[notch_mask][np.argmax(self.psd[notch_mask])]
        
        # Ruido de fondo (mediana excluye pico)
        background_mask = (self.frequencies >= FREQ_MIN) & (self.frequencies <= FREQ_MAX)
        background_mask &= ~notch_mask
        self.ruido_fondo = np.median(self.psd[background_mask])
        
        # Significancia en dB
        self.significancia_db = 20 * np.log10(self.pico_potencia / self.ruido_fondo)
        
        # Significancia estadística (σ)
        # Aproximación: SNR_linear = pico/ruido, σ ≈ sqrt(SNR_linear)
        snr_linear = self.pico_potencia / self.ruido_fondo
        self.significancia_sigma = np.sqrt(snr_linear)
        
        # Test χ² para confirmar significancia
        # H0: ruido blanco, H1: pico coherente
        dof = len(self.psd[notch_mask])  # grados de libertad
        chi2_stat = snr_linear * dof
        p_value = 1 - chi2.cdf(chi2_stat, dof)
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"RESULTADOS: Pico @ {freq_pico:.7f} Hz")
            print(f"{'='*70}")
            print(f"Frecuencia teórica:    {F0_LEO:.7f} Hz")
            print(f"Frecuencia observada:  {freq_pico:.7f} Hz")
            print(f"Δf:                    {abs(freq_pico - F0_LEO):.2e} Hz")
            print(f"Potencia pico:         {self.pico_potencia:.2e}")
            print(f"Ruido fondo:           {self.ruido_fondo:.2e}")
            print(f"Significancia:         {self.significancia_db:.1f} dB")
            print(f"Significancia:         {self.significancia_sigma:.2f}σ")
            print(f"p-value (χ²):          {p_value:.2e}")
            print(f"{'='*70}")
            
            if self.significancia_sigma >= SIGMA_THRESHOLD:
                print(f"✓ DETECCIÓN CONFIRMADA (>{SIGMA_THRESHOLD}σ)")
            else:
                print(f"✗ No hay señal significativa (<{SIGMA_THRESHOLD}σ)")
                
        return {
            'freq_teorica': F0_LEO,
            'freq_observada': float(freq_pico),
            'delta_freq': float(abs(freq_pico - F0_LEO)),
            'potencia_pico': float(self.pico_potencia),
            'ruido_fondo': float(self.ruido_fondo),
            'snr_db': float(self.significancia_db),
            'significancia_sigma': float(self.significancia_sigma),
            'p_value': float(p_value),
            'deteccion_confirmada': bool(self.significancia_sigma >= SIGMA_THRESHOLD),
            'umbral_sigma': SIGMA_THRESHOLD,
            'n_muestras': len(self.accel_x),
            'duracion_s': float(self.time[-1] - self.time[0]),
            'frecuencia_muestreo_hz': float(self.fs)
        }
        
    def graficar_espectro(self, output_file: Optional[str] = None):
        """
        Grafica espectro de potencia con pico áureo destacado.
        
        Args:
            output_file: Ruta para guardar figura (opcional)
        """
        if self.frequencies is None or self.psd is None:
            print("ERROR: Debe ejecutar analizar_pico_aureo() primero")
            return
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Panel 1: Espectro completo
        ax1.semilogy(self.frequencies, self.psd, 'b-', alpha=0.7, linewidth=0.5)
        ax1.axvline(F0_LEO, color='red', linestyle='--', linewidth=2, 
                   label=f'f₀ LEO = {F0_LEO:.7f} Hz')
        ax1.axhline(self.ruido_fondo, color='gray', linestyle=':', linewidth=1,
                   label=f'Ruido fondo = {self.ruido_fondo:.2e}')
        ax1.set_xlabel('Frecuencia (Hz)', fontsize=12)
        ax1.set_ylabel('PSD (m²/s⁴/Hz)', fontsize=12)
        ax1.set_title('GRACE-FO: Espectro Completo', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=10)
        ax1.set_xlim(FREQ_MIN, FREQ_MAX)
        
        # Panel 2: Zoom en pico áureo
        zoom_width = 0.05  # Hz
        zoom_mask = np.abs(self.frequencies - F0_LEO) < zoom_width
        
        ax2.semilogy(self.frequencies[zoom_mask], self.psd[zoom_mask], 
                    'b-', linewidth=2)
        ax2.axvline(F0_LEO, color='red', linestyle='--', linewidth=2,
                   label=f'f₀ LEO = {F0_LEO:.7f} Hz')
        ax2.axhline(self.ruido_fondo, color='gray', linestyle=':', linewidth=1,
                   label=f'Ruido fondo')
        ax2.fill_between(self.frequencies[zoom_mask], 
                        self.ruido_fondo,
                        self.psd[zoom_mask],
                        where=(self.psd[zoom_mask] > self.ruido_fondo),
                        alpha=0.3, color='gold',
                        label=f'Exceso: {self.significancia_db:.1f} dB')
        ax2.set_xlabel('Frecuencia (Hz)', fontsize=12)
        ax2.set_ylabel('PSD (m²/s⁴/Hz)', fontsize=12)
        ax2.set_title(f'GRACE-FO: Anomalía Áurea @ {F0_LEO:.7f} Hz '
                     f'({self.significancia_sigma:.1f}σ)',
                     fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=10)
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            if self.verbose:
                print(f"[OK] Figura guardada: {output_file}")
        else:
            plt.show()
            
    def exportar_resultados(self, output_file: str):
        """
        Exporta resultados a JSON.
        
        Args:
            output_file: Ruta del archivo JSON de salida
        """
        resultados = self.analizar_pico_aureo()
        
        # Agregar metadatos
        resultados['metadata'] = {
            'archivo_datos': str(self.data_file),
            'constantes': {
                'F0_HZ': F0_HZ,
                'F0_LEO': F0_LEO,
                'LAMBDA_DECOH': LAMBDA_DECOH,
                'ALPHA_YUKAWA': ALPHA_YUKAWA,
                'GRACE_FO_ALTITUDE': GRACE_FO_ALTITUDE
            },
            'parametros': {
                'sample_limit': self.sample_limit,
                'notch_width_hz': NOTCH_WIDTH,
                'freq_band': [FREQ_MIN, FREQ_MAX]
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(resultados, f, indent=2)
            
        if self.verbose:
            print(f"[OK] Resultados exportados: {output_file}")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal con interfaz CLI."""
    parser = argparse.ArgumentParser(
        description='Análisis GRACE-FO para anomalía gravitatoria @ 0.1417001 Hz',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplo de uso:
    python grace_fo_anomalia_336m.py --input GRACE_FO_L2_RL06.h5 \\
                                     --output resultados_grace_fo.json \\
                                     --plot figura_grace_fo.png \\
                                     --samples 1000000

Nota: Descarga datos GRACE-FO de:
    https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=GRFO-L-ACCE-4-ACCRES-V1.0
        """
    )
    
    parser.add_argument('--input', '-i', required=True,
                       help='Archivo HDF5 con datos GRACE-FO RL06')
    parser.add_argument('--output', '-o', default='grace_fo_results.json',
                       help='Archivo JSON de salida (default: grace_fo_results.json)')
    parser.add_argument('--plot', '-p', default=None,
                       help='Archivo de salida para gráfico (default: no guardar)')
    parser.add_argument('--samples', '-n', type=int, default=1000000,
                       help='Número de muestras a analizar (default: 1M)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Modo silencioso (sin verbose)')
    
    args = parser.parse_args()
    
    # Crear analizador
    analyzer = GRACEFOAnalyzer(
        data_file=args.input,
        sample_limit=args.samples,
        verbose=not args.quiet
    )
    
    # Cargar datos
    if not analyzer.cargar_datos():
        sys.exit(1)
        
    # Analizar pico
    resultados = analyzer.analizar_pico_aureo()
    
    if not resultados:
        sys.exit(1)
        
    # Exportar resultados
    analyzer.exportar_resultados(args.output)
    
    # Graficar
    if args.plot or not args.quiet:
        analyzer.graficar_espectro(args.plot)
        
    # Código de salida basado en detección
    if resultados['deteccion_confirmada']:
        print("\n✓ DETECCIÓN CONFIRMADA: Anomalía áurea @ 0.1417001 Hz")
        sys.exit(0)
    else:
        print("\n✗ NO DETECTADO: Señal por debajo del umbral")
        sys.exit(2)


if __name__ == '__main__':
    main()
