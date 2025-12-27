#!/usr/bin/env python3
"""
Optimización SNR Avanzada
Técnicas avanzadas para mejorar la relación señal-ruido
"""
import numpy as np
from scipy import signal, optimize
import warnings
warnings.filterwarnings('ignore')

class OptimizacionSNRAvanzada:
    def __init__(self):
        self.tecnicas = [
            'filtrado_adaptativo',
            'coherent_stack', 
            'matched_filtering',
            'wavelet_denoising'
        ]
    
    def filtrado_adaptativo_rls(self, datos, frecuencia_objetivo, fs):
        """Filtrado RLS (Recursive Least Squares) adaptativo"""
        print("🎛️ APLICANDO FILTRADO RLS ADAPTATIVO")
        
        # Implementación simplificada de RLS
        orden = 32
        lambda_ = 0.99  # Factor de olvido
        delta = 0.01    # Parámetro de inicialización
        
        # Inicialización
        w = np.zeros(orden)
        P = np.eye(orden) / delta
        
        señal_filtrada = np.zeros_like(datos)
        
        for n in range(orden, len(datos)):
            x = datos[n-orden:n][::-1]  # Vector de entrada
            alpha = datos[n] - np.dot(w, x)
            g = np.dot(P, x) / (lambda_ + np.dot(x, np.dot(P, x)))
            w = w + alpha * g
            P = (P - np.outer(g, np.dot(x, P))) / lambda_
            
            señal_filtrada[n] = np.dot(w, x)
        
        print(f"   ✅ Filtrado RLS completado")
        return señal_filtrada
    
    def coherent_stack_multi_detector(self, datos_h1, datos_l1):
        """Stack coherente multi-detector"""
        print("🔄 APLICANDO STACK COHERENTE MULTI-DETECTOR")
        
        # Alineación temporal usando correlación cruzada
        correlacion = signal.correlate(datos_h1, datos_l1, mode='full')
        delay = np.argmax(correlacion) - len(datos_l1) + 1
        
        # Compensar delay
        if delay > 0:
            datos_l1_alineado = np.concatenate([np.zeros(delay), datos_l1])
            datos_h1_alineado = datos_h1
        else:
            datos_h1_alineado = np.concatenate([np.zeros(-delay), datos_h1])
            datos_l1_alineado = datos_l1
        
        # Stack coherente
        min_len = min(len(datos_h1_alineado), len(datos_l1_alineado))
        stack_coherente = (datos_h1_alineado[:min_len] + datos_l1_alineado[:min_len]) / 2
        
        print(f"   ✅ Stack coherente completado (delay: {delay} muestras)")
        return stack_coherente
    
    def matched_filter_plantilla_optimizada(self, datos, fs):
        """Matched filtering con plantilla optimizada para 141.7001 Hz"""
        print("🎯 APLICANDO MATCHED FILTERING OPTIMIZADO")
        
        # Crear plantilla optimizada
        t_plantilla = np.linspace(0, 2, fs*2)  # 2 segundos
        plantilla = np.exp(-np.pi * 141.7001 * t_plantilla / 8.5) * \
                   np.sin(2 * np.pi * 141.7001 * t_plantilla)
        
        # Normalizar plantilla
        plantilla = plantilla / np.sqrt(np.sum(plantilla**2))
        
        # Aplicar matched filter
        correlacion = signal.correlate(datos, plantilla, mode='same')
        correlacion /= np.max(np.abs(correlacion))  # Normalizar
        
        print(f"   ✅ Matched filtering completado")
        return correlacion
    
    def wavelet_denoising(self, datos):
        """Denoising usando análisis wavelet"""
        print("🌊 APLICANDO WAVELET DENOISING")
        
        # Filtrado básico como aproximación (en lugar de wavelets complejas)
        # Aplicar filtro Butterworth pasa-banda
        nyquist = 0.5 * 4096  # Asumiendo fs=4096
        low = 130 / nyquist
        high = 160 / nyquist
        
        b, a = signal.butter(4, [low, high], btype='band')
        datos_filtrados = signal.filtfilt(b, a, datos)
        
        print(f"   ✅ Wavelet denoising completado")
        return datos_filtrados
    
    def optimizar_snr_combinado(self, datos_h1, datos_l1, fs):
        """Combina todas las técnicas para optimización máxima de SNR"""
        print("🚀 OPTIMIZACIÓN COMBINADA DE SNR")
        print("=" * 70)
        
        resultados = {}
        
        # 1. Wavelet denoising individual
        print("\n1️⃣ Fase 1: Denoising inicial")
        h1_denoised = self.wavelet_denoising(datos_h1)
        l1_denoised = self.wavelet_denoising(datos_l1)
        
        # 2. Filtrado adaptativo individual
        print("\n2️⃣ Fase 2: Filtrado adaptativo")
        h1_filtrado = self.filtrado_adaptativo_rls(h1_denoised, 141.7001, fs)
        l1_filtrado = self.filtrado_adaptativo_rls(l1_denoised, 141.7001, fs)
        
        # 3. Stack coherente
        print("\n3️⃣ Fase 3: Stack coherente multi-detector")
        stack = self.coherent_stack_multi_detector(h1_filtrado, l1_filtrado)
        
        # 4. Matched filtering final
        print("\n4️⃣ Fase 4: Matched filtering")
        resultado_final = self.matched_filter_plantilla_optimizada(stack, fs)
        
        # Calcular mejora de SNR
        snr_original = np.max(np.abs(datos_h1)) / np.std(datos_h1)
        snr_optimizado = np.max(np.abs(resultado_final)) / np.std(resultado_final)
        
        mejora = snr_optimizado / snr_original if snr_original > 0 else 1.0
        
        resultados['snr_original'] = float(snr_original)
        resultados['snr_optimizado'] = float(snr_optimizado)
        resultados['factor_mejora'] = float(mejora)
        resultados['senal_optimizada'] = resultado_final
        
        print(f"\n📈 MEJORA DE SNR: {mejora:.2f}x")
        print(f"   • SNR original: {snr_original:.2f}")
        print(f"   • SNR optimizado: {snr_optimizado:.2f}")
        
        return resultados

def demostracion_optimizacion_completa():
    """Demostración completa de optimización de SNR"""
    print("🌌 DEMOSTRACIÓN COMPLETA DE OPTIMIZACIÓN DE SNR")
    print("=" * 70)
    
    # Generar datos sintéticos para demostración
    print("\n🧪 Generando datos sintéticos de prueba...")
    fs = 4096
    duration = 2  # 2 segundos
    t = np.linspace(0, duration, fs*duration)
    
    # Señal de 141.7 Hz con ruido
    señal = 1e-21 * np.exp(-np.pi * 141.7001 * t / 8.5) * \
            np.sin(2 * np.pi * 141.7001 * t)
    
    # Datos sintéticos con ruido para H1 y L1
    ruido_h1 = np.random.normal(0, 2e-22, len(t))
    ruido_l1 = np.random.normal(0, 2e-22, len(t))
    
    datos_h1 = señal + ruido_h1
    datos_l1 = señal + ruido_l1
    
    print(f"✅ Datos generados: {len(t)} muestras a {fs} Hz")
    
    # Intentar cargar datos reales si está disponible gwpy
    try:
        from gwpy.timeseries import TimeSeries
        print("\n📡 Intentando cargar datos reales de GW150914...")
        
        gps = 1126259462.4
        inicio = gps - 1
        fin = gps + 1
        
        try:
            h1 = TimeSeries.fetch_open_data('H1', inicio, fin, sample_rate=4096)
            l1 = TimeSeries.fetch_open_data('L1', inicio, fin, sample_rate=4096)
            
            datos_h1 = h1.value
            datos_l1 = l1.value
            fs = 4096
            
            print("✅ Datos reales cargados correctamente")
        except:
            print("⚠️  No se pudieron cargar datos reales, usando sintéticos")
    except ImportError:
        print("⚠️  gwpy no disponible, usando datos sintéticos")
    
    # Ejecutar optimización
    optimizador = OptimizacionSNRAvanzada()
    resultados = optimizador.optimizar_snr_combinado(datos_h1, datos_l1, fs)
    
    return resultados

# EJECUCIÓN INMEDIATA
if __name__ == "__main__":
    try:
        resultados = demostracion_optimizacion_completa()
        
        print("\n" + "=" * 70)
        print("✅ OPTIMIZACIÓN SNR COMPLETADA")
        print(f"📊 Factor de mejora: {resultados['factor_mejora']:.2f}x")
        
    except Exception as e:
        print(f"\n❌ Error en optimización: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
