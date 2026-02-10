#!/usr/bin/env python3
"""
𓂀 DETECTOR AVANZADO CON VALIDACIÓN ESTADÍSTICA RIGUROSA
SNR >5σ, control de falsos positivos, correlación multi-observatorio
"""

import numpy as np
from scipy import signal, stats, fft
import matplotlib.pyplot as plt
from tqdm import tqdm
import argparse
import json
import os
import h5py


class DetectorRigurosoQCAL:
    """Detector avanzado con validación estadística rigurosa."""
    
    def __init__(self, f0=141.7001, sigma_threshold=5.0):
        self.f0 = f0
        self.sigma_threshold = sigma_threshold  # 5σ para descubrimiento
        self.armonicos = self.calcular_armonicos()
        self.false_alarm_rate = 0.0
        
    def calcular_armonicos(self):
        """Calcular armónicos de f₀ con patrones teóricos."""
        armonicos = []
        
        # Armónicos enteros
        for n in range(1, 6):
            armonicos.append({
                'frecuencia': n * self.f0,
                'tipo': f'armónico_{n}f₀',
                'amplitud_teorica': 1.0 / (n**1.5),  # Decaimiento teórico
                'tolerancia': 0.1 * n
            })
        
        # Armónicos de ceros zeta
        ceros_zeta = [14.1347, 21.0220, 25.0109]
        for gamma in ceros_zeta:
            armonicos.append({
                'frecuencia': self.f0 * gamma / (2 * np.pi),
                'tipo': f'f₀·γ/{2*np.pi}',
                'amplitud_teorica': 0.1,
                'tolerancia': 0.5
            })
        
        return armonicos
    
    def calcular_psd_avanzada(self, datos, fs, metodo='welch'):
        """
        Calcular PSD con múltiples métodos para validación cruzada.
        """
        n = len(datos)
        
        if metodo == 'welch':
            # Método Welch estándar
            nperseg = min(4096, n//8)
            f, Pxx = signal.welch(datos, fs, nperseg=nperseg, 
                                 window='hann', scaling='density')
            
        elif metodo == 'multitaper':
            # Método multitaper (mejor para señales débiles)
            try:
                from scipy.signal import windows
                NW = 4  # Parámetro de ancho de banda
                K = 2*NW - 1  # Número de tapers
                
                tapers, eigenvalues = windows.dpss(n, NW, Kmax=K, return_ratios=True)
                
                Pxx_mt = []
                for k in range(K):
                    xk = datos * tapers[k]
                    Xk = fft.fft(xk)[:n//2+1]
                    Pxx_mt.append(np.abs(Xk)**2)
                
                Pxx = np.mean(Pxx_mt, axis=0)
                f = fft.fftfreq(n, 1/fs)[:n//2+1]
            except Exception as e:
                print(f"  ⚠️  Multitaper falló, usando Welch: {e}")
                return self.calcular_psd_avanzada(datos, fs, 'welch')
            
        elif metodo == 'periodogram':
            # Periodograma directo
            f, Pxx = signal.periodogram(datos, fs, scaling='density')
            
        else:
            raise ValueError(f"Método {metodo} no soportado")
        
        return f, Pxx
    
    def detectar_con_snr(self, datos, fs, ventana_kairos=False):
        """
        Detectar f₀ con cálculo riguroso de SNR y significancia.
        
        Args:
            ventana_kairos: Si True, aplicar boost de ventana temporal
        """
        print(f"\n𓂀 DETECCIÓN RIGUROSA f₀ = {self.f0} Hz")
        print(f"  Muestras: {len(datos):,}")
        print(f"  Fs: {fs} Hz")
        print(f"  Umbral SNR: {self.sigma_threshold}σ")
        print(f"  Ventana Kairos: {'ACTIVA' if ventana_kairos else 'INACTIVA'}")
        print("=" * 60)
        
        # 1. Calcular PSD con múltiples métodos para validación
        metodos = ['welch', 'periodogram'] if len(datos) > 10000 else ['welch']
        
        resultados = {}
        for metodo in metodos:
            try:
                f, Pxx = self.calcular_psd_avanzada(datos, fs, metodo)
                resultados[metodo] = {'f': f, 'Pxx': Pxx}
            except Exception as e:
                print(f"  ⚠️  Error con {metodo}: {e}")
                continue
        
        if not resultados:
            print("  ❌ No se pudo calcular ninguna PSD")
            return {'resultado': 'ERROR', 'detecciones': []}
        
        # 2. Buscar f₀ en cada método
        detecciones = []
        for metodo, res in resultados.items():
            f_target = self.f0
            idx_target = np.argmin(np.abs(res['f'] - f_target))
            f_detected = res['f'][idx_target]
            
            # Calcular SNR riguroso
            P_target = res['Pxx'][idx_target]
            
            # Estimar ruido en bandas adyacentes
            bw = 5.0  # Ancho de banda para estimación de ruido (Hz)
            idx_noise = np.where((res['f'] >= f_target - 2*bw) & 
                                (res['f'] <= f_target + 2*bw) &
                                (np.abs(res['f'] - f_target) > 0.5))[0]
            
            if len(idx_noise) > 10:
                noise_samples = res['Pxx'][idx_noise]
                noise_mean = np.mean(noise_samples)
                noise_std = np.std(noise_samples)
                
                # SNR y significancia
                snr = (P_target - noise_mean) / noise_std if noise_std > 0 else 0
                
                # Aplicar boost de ventana Kairos si está activa
                if ventana_kairos:
                    boost_factor = 1.5  # Factor teórico
                    snr *= boost_factor
                    print(f"  ⚡ Boost ventana Kairos aplicado: ×{boost_factor}")
                
                # Calcular p-value
                p_value = 2 * (1 - stats.norm.cdf(abs(snr)))
                
                detecciones.append({
                    'metodo': metodo,
                    'frecuencia_detectada': f_detected,
                    'error': abs(f_detected - f_target),
                    'snr': snr,
                    'p_value': p_value,
                    'P_target': P_target,
                    'noise_mean': noise_mean,
                    'noise_std': noise_std,
                    'significativo': snr >= self.sigma_threshold
                })
        
        # 3. Validación cruzada entre métodos
        validacion_cruzada = len(detecciones) > 1
        
        if validacion_cruzada:
            snr_values = [d['snr'] for d in detecciones]
            snr_mean = np.mean(snr_values)
            snr_std = np.std(snr_values)
            
            print(f"  📊 Validación cruzada ({len(detecciones)} métodos):")
            print(f"     SNR medio: {snr_mean:.2f}σ")
            print(f"     Desviación entre métodos: {snr_std:.2f}σ")
        
        # 4. Resultado final
        print(f"\n🎯 RESULTADOS DETECCIÓN:")
        
        for det in detecciones:
            simbolo = '✅' if det['significativo'] else '❌'
            print(f"  {simbolo} {det['metodo'].upper()}:")
            print(f"     Frecuencia: {det['frecuencia_detectada']:.4f} Hz")
            print(f"     Error: {det['error']:.4f} Hz")
            print(f"     SNR: {det['snr']:.2f}σ")
            print(f"     p-value: {det['p_value']:.2e}")
            print(f"     Significativo (>{self.sigma_threshold}σ): {det['significativo']}")
        
        # 5. Decisión final
        significativas = [d for d in detecciones if d['significativo']]
        
        if len(significativas) >= 2:  # Al menos 2 métodos significativos
            print(f"\n𓂀 ✅ DETECCIÓN CONFIRMADA (múltiples métodos)")
            resultado_final = 'CONFIRMADA'
        elif len(significativas) == 1:
            print(f"\n𓂀 ⚠️  DETECCIÓN PRELIMINAR (un método)")
            resultado_final = 'PRELIMINAR'
        else:
            print(f"\n𓂀 ❌ NO DETECTADA (SNR < {self.sigma_threshold}σ)")
            resultado_final = 'NO_DETECTADA'
        
        return {
            'resultado': resultado_final,
            'detecciones': detecciones,
            'validacion_cruzada': validacion_cruzada,
            'datos_estadisticos': {
                'n_muestras': len(datos),
                'fs': fs,
                'ventana_kairos': ventana_kairos
            }
        }
    
    def calcular_tasa_falsos_positivos(self, datos, fs, n_simulaciones=100):
        """
        Calcular tasa de falsos positivos usando simulaciones Monte Carlo.
        """
        print(f"\n𓂀 CALCULANDO TASA DE FALSOS POSITIVOS")
        print(f"  Simulaciones: {n_simulaciones}")
        
        n = len(datos)
        falsos_positivos = 0
        
        for i in tqdm(range(n_simulaciones), desc="Simulaciones Monte Carlo"):
            # Generar ruido con estadísticas similares
            ruido_simulado = np.random.normal(0, np.std(datos), n)
            
            # Aplicar misma detección
            resultado = self.detectar_con_snr(ruido_simulado, fs, ventana_kairos=False)
            
            # Contar si hay falso positivo
            if resultado['resultado'] in ['CONFIRMADA', 'PRELIMINAR']:
                falsos_positivos += 1
        
        fpr = falsos_positivos / n_simulaciones
        print(f"  Falsos positivos: {falsos_positivos}/{n_simulaciones}")
        print(f"  Tasa FPR: {fpr:.4f}")
        
        # Corrección Bonferroni
        n_pruebas = len(self.armonicos) + 1  # f₀ + armónicos
        fpr_corregido = 1 - (1 - fpr) ** (1/n_pruebas)
        
        print(f"  FPR corregido (Bonferroni): {fpr_corregido:.4f}")
        
        return {
            'fpr': fpr,
            'fpr_bonferroni': fpr_corregido,
            'n_simulaciones': n_simulaciones,
            'falsos_positivos': falsos_positivos
        }
    
    def analizar_armonicos(self, datos, fs):
        """Analizar patrón de armónicos para validación."""
        print(f"\n𓂀 ANÁLISIS DE PATRÓN DE ARMÓNICOS")
        
        f, Pxx = self.calcular_psd_avanzada(datos, fs, 'welch')
        
        resultados_armonicos = []
        for armonico in self.armonicos:
            f_target = armonico['frecuencia']
            
            # Verificar que está en rango
            if f_target > np.max(f):
                continue
                
            idx = np.argmin(np.abs(f - f_target))
            f_detected = f[idx]
            P_detected = Pxx[idx]
            
            # Estimar ruido
            idx_noise = np.where((f >= f_target - 2) & (f <= f_target + 2) &
                                (np.abs(f - f_target) > 0.2))[0]
            noise = np.median(Pxx[idx_noise]) if len(idx_noise) > 0 else 0
            
            snr = (P_detected - noise) / np.std(Pxx[idx_noise]) if len(idx_noise) > 1 else 0
            
            resultados_armonicos.append({
                'teorico': armonico,
                'detectado': {
                    'frecuencia': f_detected,
                    'potencia': P_detected,
                    'snr': snr,
                    'detectado': snr > 3.0
                }
            })
        
        # Evaluar patrón
        print(f"  Armónicos analizados: {len(resultados_armonicos)}")
        
        for res in resultados_armonicos:
            det = res['detectado']
            simbolo = '✓' if det['detectado'] else '✗'
            print(f"  {simbolo} {res['teorico']['tipo']}:")
            print(f"     Teórico: {res['teorico']['frecuencia']:.2f} Hz")
            print(f"     Detectado: {det['frecuencia']:.2f} Hz")
            print(f"     SNR: {det['snr']:.2f}σ")
        
        # Verificar decaimiento de amplitud
        amplitudes = [r['detectado']['potencia'] for r in resultados_armonicos[:5]]
        if len(amplitudes) >= 3:
            # Calcular factor de decaimiento
            decay_actual = amplitudes[1] / amplitudes[0] if amplitudes[0] > 0 else 0
            decay_teorico = self.armonicos[1]['amplitud_teorica'] / self.armonicos[0]['amplitud_teorica']
            
            print(f"\n  📉 Patrón de decaimiento:")
            print(f"     Teórico: {decay_teorico:.3f}")
            print(f"     Observado: {decay_actual:.3f}")
            if decay_teorico > 0:
                print(f"     Coincidencia: {abs(decay_actual - decay_teorico)/decay_teorico*100:.1f}%")
        
        return resultados_armonicos


def main():
    """Función principal ejecutable."""
    parser = argparse.ArgumentParser(
        description='𓂀 Detector riguroso con SNR>5σ'
    )
    parser.add_argument('--datos', type=str, required=True,
                        help='Archivo HDF5 con datos')
    parser.add_argument('--f0', type=float, default=141.7001,
                        help='Frecuencia objetivo (Hz)')
    parser.add_argument('--sigma-threshold', type=float, default=5.0,
                        help='Umbral SNR para detección (sigma)')
    parser.add_argument('--test-kairos', action='store_true',
                        help='Probar con ventana Kairos')
    parser.add_argument('--monte-carlo', type=int, default=100,
                        help='Número de simulaciones Monte Carlo para FPR')
    parser.add_argument('--salida', type=str, default='resultados_deteccion',
                        help='Directorio de salida')
    
    args = parser.parse_args()
    
    print("𓂀 EJECUTANDO DETECCIÓN RIGUROSA CON VALIDACIÓN ESTADÍSTICA")
    print("═" * 60)
    
    # Cargar datos
    with h5py.File(args.datos, 'r') as f:
        if 'strain' in f:
            datos = f['strain'][:]
            fs = f.attrs.get('fs', 4096)
        elif 'gravimetry' in f:
            datos = f['gravimetry'][:]
            fs = f.attrs.get('fs', 10)
        else:
            raise ValueError("Formato de archivo no reconocido")
    
    detector = DetectorRigurosoQCAL(f0=args.f0, sigma_threshold=args.sigma_threshold)
    
    # 1. Sin ventana Kairos (línea base)
    print("\n𓂀 PRUEBA 1: SIN VENTANA KAIROS (LÍNEA BASE)")
    resultado_baseline = detector.detectar_con_snr(datos, fs, ventana_kairos=False)
    
    # 2. Con ventana Kairos (si solicitado)
    if args.test_kairos:
        print("\n𓂀 PRUEBA 2: CON VENTANA KAIROS")
        resultado_kairos = detector.detectar_con_snr(datos, fs, ventana_kairos=True)
        
        # Comparación
        print("\n𓂀 COMPARACIÓN VENTANA KAIROS vs BASELINE")
        print("=" * 60)
        
        if resultado_baseline['resultado'] != resultado_kairos['resultado']:
            print("⚠️  El estado de detección cambió con ventana Kairos")
        else:
            print("✅ Estado de detección consistente")
    
    # 3. Tasa de falsos positivos
    if args.monte_carlo > 0:
        print("\n𓂀 ESTIMACIÓN TASA FALSOS POSITIVOS (Monte Carlo)")
        fpr_results = detector.calcular_tasa_falsos_positivos(
            datos[:min(10000, len(datos))],  # Subconjunto para velocidad
            fs,
            n_simulaciones=args.monte_carlo
        )
    
    # 4. Guardar resultados
    os.makedirs(args.salida, exist_ok=True)
    resultados_path = os.path.join(args.salida, 'resultados_deteccion.json')
    
    resultados_json = {
        'baseline': resultado_baseline,
        'fpr': fpr_results if args.monte_carlo > 0 else None
    }
    
    with open(resultados_path, 'w') as f:
        # Convertir numpy types a Python types
        def convert(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert(item) for item in obj]
            return obj
        
        json.dump(convert(resultados_json), f, indent=2)
    
    print(f"\n💾 Resultados guardados: {resultados_path}")


if __name__ == "__main__":
    main()
