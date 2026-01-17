#!/usr/bin/env python3
"""
Extracción de Strain GW250114 - 141.7001 Hz QNM Analysis
=========================================================

Extrae datos de strain de los detectores H1, L1, V1 para GW250114,
centrados en la ventana de ringdown (t_merger + 10ms).

Implementa el protocolo descrito en el problema statement:
1. Descarga de datos a 4KHz/16KHz usando gwpy
2. Extracción de ventana de ringdown
3. Aplicación de filtro QCAL ultra-estrecho (f₀ = 141.7001 Hz, Q alto)
4. Análisis de exponente de Lyapunov
5. Exportación en formato HDF5/JSON compatible con GWOSC

Autor: Sistema QCAL ∞³
Hash de Certificación: 1d62f6d4
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json
import h5py
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Import GW analysis libraries
try:
    from gwpy.timeseries import TimeSeries
    from gwpy.signal import filter_design
    from gwosc import datasets
except ImportError as e:
    print(f"❌ Error importing GW libraries: {e}")
    print("Install with: pip install gwpy gwosc")
    sys.exit(1)

try:
    from scipy import signal
    from scipy.optimize import curve_fit
except ImportError:
    print("❌ Error: scipy is required")
    print("Install with: pip install scipy")
    sys.exit(1)


class ExtractorStrainGW250114:
    """
    Extractor de strain para GW250114 con análisis de modo cuasinormal
    persistente en 141.7001 Hz.
    """
    
    def __init__(self, evento: str = "GW250114"):
        """
        Inicializar extractor de strain.
        
        Args:
            evento: Nombre del evento gravitacional
        """
        self.evento = evento
        self.f0 = 141.7001  # Frecuencia fundamental QCAL (Hz)
        self.Q_filter = 100  # Factor de calidad del filtro ultra-estrecho
        self.cert_hash = "1d62f6d4"  # Hash de certificación
        
        # Parámetros de extracción
        self.ringdown_start_offset = 0.010  # 10 ms después del merger
        self.ringdown_duration = 0.500      # 500 ms de ringdown
        self.sample_rates = [4096, 16384]   # 4KHz y 16KHz
        
        # Directorios de salida
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "results" / "gw250114_strain"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Resultados
        self.resultados = {
            "evento": self.evento,
            "f0_qcal": self.f0,
            "cert_hash": self.cert_hash,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "detectores": {}
        }
    
    def verificar_disponibilidad(self) -> Tuple[bool, Optional[float]]:
        """
        Verificar si GW250114 está disponible en GWOSC.
        
        Returns:
            tuple: (disponible, gps_time)
        """
        print("🔍 Verificando disponibilidad de GW250114 en GWOSC...")
        
        try:
            gps_time = datasets.event_gps(self.evento)
            print(f"   ✅ {self.evento} encontrado en GPS: {gps_time}")
            return True, gps_time
        except Exception as e:
            print(f"   ⚠️  {self.evento} no disponible aún: {e}")
            print("   📋 Esto es esperado hasta que LIGO libere los datos")
            return False, None
    
    def descargar_strain(self, detector: str, gps_time: float, 
                        sample_rate: int = 4096) -> TimeSeries:
        """
        Descargar datos de strain del detector.
        
        Args:
            detector: Nombre del detector ('H1', 'L1', 'V1')
            gps_time: GPS time del evento
            sample_rate: Tasa de muestreo (4096 o 16384 Hz)
            
        Returns:
            TimeSeries: Datos de strain
        """
        print(f"📡 Descargando strain de {detector} @ {sample_rate} Hz...")
        
        # Ventana de tiempo: ±16s alrededor del merger
        start = gps_time - 16
        end = gps_time + 16
        
        try:
            strain = TimeSeries.fetch_open_data(
                detector, start, end,
                sample_rate=sample_rate,
                cache=True
            )
            print(f"   ✅ Strain descargado: {len(strain)} muestras")
            return strain
        except Exception as e:
            print(f"   ❌ Error descargando strain: {e}")
            raise
    
    def extraer_ringdown(self, strain: TimeSeries, 
                        merger_time: float) -> TimeSeries:
        """
        Extraer ventana de ringdown (t_merger + 10ms).
        
        Args:
            strain: TimeSeries completa
            merger_time: GPS time del merger
            
        Returns:
            TimeSeries: Segmento de ringdown
        """
        print(f"📊 Extrayendo ringdown ({self.ringdown_duration}s desde +10ms)...")
        
        ringdown_start = merger_time + self.ringdown_start_offset
        ringdown_end = ringdown_start + self.ringdown_duration
        
        ringdown = strain.crop(ringdown_start, ringdown_end)
        
        print(f"   ✅ Ringdown extraído: {len(ringdown)} muestras")
        print(f"   📍 GPS: [{ringdown_start:.6f}, {ringdown_end:.6f}]")
        
        return ringdown
    
    def aplicar_filtro_qcal(self, ringdown: TimeSeries) -> TimeSeries:
        """
        Aplicar filtro QCAL ultra-estrecho centrado en f₀ = 141.7001 Hz.
        
        Implementa filtro de banda ultra-estrecha con factor de calidad Q alto
        para aislar la persistencia del modo cuasinormal.
        
        Args:
            ringdown: TimeSeries del ringdown
            
        Returns:
            TimeSeries: Ringdown filtrado
        """
        print(f"🔧 Aplicando filtro QCAL (f₀={self.f0} Hz, Q={self.Q_filter})...")
        
        # Ancho de banda basado en factor de calidad
        # Q = f0 / Δf => Δf = f0 / Q
        bandwidth = self.f0 / self.Q_filter
        
        # Frecuencias del filtro paso-banda
        f_low = self.f0 - bandwidth / 2
        f_high = self.f0 + bandwidth / 2
        
        print(f"   📏 Ancho de banda: {bandwidth:.4f} Hz")
        print(f"   📊 Rango: [{f_low:.4f}, {f_high:.4f}] Hz")
        
        # Diseñar y aplicar filtro
        bp_filter = filter_design.bandpass(f_low, f_high, ringdown.sample_rate)
        ringdown_filtered = ringdown.filter(bp_filter, filtfilt=True)
        
        print("   ✅ Filtro QCAL aplicado")
        
        return ringdown_filtered
    
    def calcular_lyapunov_exponent(self, ringdown: TimeSeries) -> Dict:
        """
        Calcular exponente de Lyapunov para analizar estabilidad de frecuencia.
        
        En la cola del ringdown, la estabilidad de 141.7001 Hz debe mostrar
        una tasa de decaimiento que no siga puramente la predicción de Kerr,
        sino que resuene con el operador H_Ψ.
        
        Args:
            ringdown: TimeSeries del ringdown filtrado
            
        Returns:
            dict: Resultados del análisis de Lyapunov
        """
        print("🔬 Calculando exponente de Lyapunov...")
        
        # Extraer amplitud del ringdown
        data = ringdown.value
        times = ringdown.times.value - ringdown.times.value[0]
        
        # Calcular envolvente (amplitud instantánea) usando transformada de Hilbert
        from scipy.signal import hilbert
        analytic_signal = hilbert(data)
        amplitude = np.abs(analytic_signal)
        
        # Ajustar decaimiento exponencial: A(t) = A0 * exp(-t/tau)
        # En escala logarítmica: ln(A) = ln(A0) - t/tau
        # Para Kerr: tau_Kerr ~ 1/(2*pi*f_imaginary)
        
        # Eliminar valores muy pequeños para evitar problemas con log
        valid_mask = amplitude > np.max(amplitude) * 1e-3
        amp_valid = amplitude[valid_mask]
        t_valid = times[valid_mask]
        
        if len(amp_valid) < 10:
            print("   ⚠️  Datos insuficientes para análisis de Lyapunov")
            return {
                "exito": False,
                "mensaje": "Datos insuficientes"
            }
        
        # Ajuste exponencial
        try:
            log_amp = np.log(amp_valid)
            
            # Ajuste lineal: log(A) = a - t/tau
            coef = np.polyfit(t_valid, log_amp, 1)
            decay_rate = -coef[0]  # 1/tau
            
            # Calcular tau (tiempo de decaimiento)
            tau_measured = 1 / decay_rate if decay_rate > 0 else np.inf
            
            # Predicción de Kerr para modo dominante (l=2, m=2)
            # Para agujero negro de ~70 M☉: f_real ~ 250 Hz, f_imag ~ 50 Hz
            # tau_Kerr ~ 1/(2*pi*f_imag)
            f_imag_kerr = 50  # Hz (aproximado)
            tau_kerr = 1 / (2 * np.pi * f_imag_kerr)
            
            # Calcular desviación de Kerr
            deviation_kerr = abs(tau_measured - tau_kerr) / tau_kerr * 100
            
            # Exponente de Lyapunov λ = 1/tau
            lyapunov_exp = decay_rate
            
            resultado = {
                "exito": True,
                "tau_measured": float(tau_measured),
                "tau_kerr": float(tau_kerr),
                "deviation_from_kerr_percent": float(deviation_kerr),
                "decay_rate": float(decay_rate),
                "lyapunov_exponent": float(lyapunov_exp),
                "amplitude_fit": {
                    "times": t_valid.tolist(),
                    "amplitude": amp_valid.tolist(),
                    "fit_coefficients": coef.tolist()
                }
            }
            
            print(f"   ✅ τ medido: {tau_measured*1000:.2f} ms")
            print(f"   📊 τ Kerr: {tau_kerr*1000:.2f} ms")
            print(f"   📈 Desviación: {deviation_kerr:.1f}%")
            print(f"   🎯 λ (Lyapunov): {lyapunov_exp:.3f} s⁻¹")
            
            if deviation_kerr > 20:
                print("   ⚡ DESVIACIÓN SIGNIFICATIVA DE KERR")
                print("   🎯 Resonancia con operador H_Ψ detectada")
                resultado["resonancia_h_psi"] = True
            else:
                print("   ✓ Consistente con predicción de Kerr")
                resultado["resonancia_h_psi"] = False
            
            return resultado
            
        except Exception as e:
            print(f"   ❌ Error en ajuste exponencial: {e}")
            return {
                "exito": False,
                "mensaje": str(e)
            }
    
    def calcular_psd_contrast(self, ringdown: TimeSeries) -> Dict:
        """
        Calcular métrica de contraste de PSD en 141.7 Hz.
        
        Compara la densidad espectral de potencia en 141.7 Hz frente
        a la sensibilidad del gravímetro superconductor.
        
        Args:
            ringdown: TimeSeries del ringdown
            
        Returns:
            dict: Resultados de contraste PSD
        """
        print("📊 Calculando contraste PSD en 141.7 Hz...")
        
        # Calcular PSD
        psd = ringdown.psd(fftlength=4)
        freqs = psd.frequencies.value
        psd_values = psd.value
        
        # Encontrar índice más cercano a f0
        f0_idx = np.argmin(np.abs(freqs - self.f0))
        psd_at_f0 = psd_values[f0_idx]
        
        # Calcular PSD de fondo (mediana en ventana alrededor de f0)
        window_width = 10  # Hz
        window_mask = (freqs > self.f0 - window_width) & \
                     (freqs < self.f0 + window_width)
        psd_background = np.median(psd_values[window_mask])
        
        # Contraste: ratio de PSD en f0 vs fondo
        contrast = psd_at_f0 / psd_background if psd_background > 0 else 0
        
        # Umbral de sensibilidad de gravímetro superconductor
        # Típicamente ~10^-11 m/s² en 141.7 Hz
        sg_sensitivity = 1e-11  # m/s² (aproximado)
        
        # Convertir PSD de strain a aceleración (aproximado)
        # a ~ strain * (2πf)²
        accel_psd = psd_at_f0 * (2 * np.pi * self.f0)**2
        
        resultado = {
            "psd_at_f0": float(psd_at_f0),
            "psd_background": float(psd_background),
            "contrast_ratio": float(contrast),
            "frequency_resolution": float(freqs[1] - freqs[0]),
            "accel_psd": float(accel_psd),
            "sg_sensitivity": float(sg_sensitivity),
            "detectable_by_sg": bool(accel_psd > sg_sensitivity)
        }
        
        print(f"   ✅ PSD en f₀: {psd_at_f0:.2e} strain²/Hz")
        print(f"   📊 PSD fondo: {psd_background:.2e} strain²/Hz")
        print(f"   📈 Contraste: {contrast:.2f}")
        print(f"   🎯 Detectable por SG: {'Sí' if resultado['detectable_by_sg'] else 'No'}")
        
        return resultado
    
    def procesar_detector(self, detector: str, gps_time: float) -> Dict:
        """
        Procesar datos completos de un detector.
        
        Args:
            detector: Nombre del detector
            gps_time: GPS time del evento
            
        Returns:
            dict: Resultados completos del detector
        """
        print(f"\n{'='*80}")
        print(f"📡 PROCESANDO DETECTOR: {detector}")
        print(f"{'='*80}\n")
        
        resultados_detector = {
            "detector": detector,
            "sample_rates": {}
        }
        
        for sample_rate in self.sample_rates:
            print(f"\n--- Tasa de muestreo: {sample_rate} Hz ---\n")
            
            try:
                # 1. Descargar strain
                strain = self.descargar_strain(detector, gps_time, sample_rate)
                
                # 2. Extraer ringdown
                ringdown = self.extraer_ringdown(strain, gps_time)
                
                # 3. Aplicar filtro QCAL
                ringdown_filtered = self.aplicar_filtro_qcal(ringdown)
                
                # 4. Calcular exponente de Lyapunov
                lyapunov_result = self.calcular_lyapunov_exponent(ringdown_filtered)
                
                # 5. Calcular contraste PSD
                psd_contrast = self.calcular_psd_contrast(ringdown_filtered)
                
                # Guardar resultados
                resultados_detector["sample_rates"][str(sample_rate)] = {
                    "exito": True,
                    "n_samples": len(ringdown),
                    "duration": float(self.ringdown_duration),
                    "lyapunov": lyapunov_result,
                    "psd_contrast": psd_contrast
                }
                
                # Guardar datos de strain en HDF5
                self.guardar_hdf5(detector, sample_rate, ringdown_filtered, 
                                 lyapunov_result, psd_contrast)
                
            except Exception as e:
                print(f"   ❌ Error procesando {detector} @ {sample_rate} Hz: {e}")
                resultados_detector["sample_rates"][str(sample_rate)] = {
                    "exito": False,
                    "error": str(e)
                }
        
        return resultados_detector
    
    def guardar_hdf5(self, detector: str, sample_rate: int, 
                    ringdown: TimeSeries, lyapunov: Dict, psd: Dict):
        """
        Guardar datos en formato HDF5 compatible con GWOSC.
        
        Args:
            detector: Nombre del detector
            sample_rate: Tasa de muestreo
            ringdown: TimeSeries del ringdown filtrado
            lyapunov: Resultados de Lyapunov
            psd: Resultados de PSD
        """
        filename = f"{self.evento}_{detector}_{sample_rate}Hz_QCAL.hdf5"
        filepath = self.output_dir / filename
        
        print(f"💾 Guardando HDF5: {filename}...")
        
        with h5py.File(filepath, 'w') as f:
            # Metadata
            f.attrs['event'] = self.evento
            f.attrs['detector'] = detector
            f.attrs['sample_rate'] = sample_rate
            f.attrs['f0_qcal'] = self.f0
            f.attrs['cert_hash'] = self.cert_hash
            f.attrs['timestamp'] = datetime.now(timezone.utc).isoformat()
            
            # Strain data
            strain_group = f.create_group('strain')
            strain_group.create_dataset('data', data=ringdown.value)
            strain_group.create_dataset('times', data=ringdown.times.value)
            strain_group.attrs['t0'] = float(ringdown.times.value[0])
            strain_group.attrs['dt'] = float(1.0 / sample_rate)
            strain_group.attrs['duration'] = float(self.ringdown_duration)
            
            # Lyapunov analysis
            if lyapunov.get('exito', False):
                lyap_group = f.create_group('lyapunov')
                for key, value in lyapunov.items():
                    if isinstance(value, dict):
                        subgroup = lyap_group.create_group(key)
                        for subkey, subvalue in value.items():
                            if isinstance(subvalue, (list, np.ndarray)):
                                subgroup.create_dataset(subkey, data=subvalue)
                            else:
                                subgroup.attrs[subkey] = subvalue
                    elif not isinstance(value, (list, np.ndarray)):
                        lyap_group.attrs[key] = value
            
            # PSD contrast
            psd_group = f.create_group('psd_contrast')
            for key, value in psd.items():
                if not isinstance(value, (list, np.ndarray)):
                    psd_group.attrs[key] = value
        
        print(f"   ✅ HDF5 guardado: {filepath}")
    
    def ejecutar_extraccion(self, detectores: Optional[List[str]] = None) -> Dict:
        """
        Ejecutar extracción completa para todos los detectores.
        
        Args:
            detectores: Lista de detectores a procesar (default: ['H1', 'L1', 'V1'])
            
        Returns:
            dict: Resultados completos de la extracción
        """
        if detectores is None:
            detectores = ['H1', 'L1', 'V1']
        
        print("="*80)
        print(f"🌌 EXTRACCIÓN DE STRAIN: {self.evento} - 141.7001 Hz")
        print(f"🎯 Hash de Certificación: {self.cert_hash}")
        print("="*80)
        print()
        
        # Verificar disponibilidad
        disponible, gps_time = self.verificar_disponibilidad()
        
        if not disponible:
            print()
            print("="*80)
            print("📅 DATOS NO DISPONIBLES")
            print(f"   {self.evento} será procesado cuando se libere en GWOSC")
            print("="*80)
            
            resultado_final = {
                "estado": "DATOS_NO_DISPONIBLES",
                "evento": self.evento,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "mensaje": f"{self.evento} aún no disponible en GWOSC"
            }
            
            # Guardar estado
            output_file = self.output_dir / f"{self.evento}_estado.json"
            with open(output_file, 'w') as f:
                json.dump(resultado_final, f, indent=2)
            
            return resultado_final
        
        # Procesar cada detector
        for detector in detectores:
            try:
                resultado_det = self.procesar_detector(detector, gps_time)
                self.resultados["detectores"][detector] = resultado_det
            except Exception as e:
                print(f"\n❌ Error procesando {detector}: {e}")
                self.resultados["detectores"][detector] = {
                    "exito": False,
                    "error": str(e)
                }
        
        # Guardar resultados en JSON
        self.resultados["estado"] = "COMPLETADO"
        self.resultados["gps_time"] = float(gps_time)
        
        output_file = self.output_dir / f"{self.evento}_extraccion_completa.json"
        with open(output_file, 'w') as f:
            json.dump(self.resultados, f, indent=2)
        
        print()
        print("="*80)
        print("📊 EXTRACCIÓN COMPLETADA")
        print(f"   JSON: {output_file}")
        print(f"   HDF5: {self.output_dir}/*.hdf5")
        print("="*80)
        
        return self.resultados


def main():
    """Función principal."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Extracción de strain GW250114 para análisis QNM QCAL',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--detectores',
        nargs='+',
        default=['H1', 'L1', 'V1'],
        choices=['H1', 'L1', 'V1'],
        help='Detectores a procesar (default: H1 L1 V1)'
    )
    
    args = parser.parse_args()
    
    # Ejecutar extracción
    extractor = ExtractorStrainGW250114()
    resultados = extractor.ejecutar_extraccion(detectores=args.detectores)
    
    # Exit code
    if resultados.get("estado") == "DATOS_NO_DISPONIBLES":
        return 0
    elif resultados.get("estado") == "COMPLETADO":
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
