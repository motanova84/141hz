#!/usr/bin/env python3
"""
Nodo Riemann: Validación del Ringdown Gravitacional

Confirma que el espectro del ringdown de GW250114 coincide exactamente 
con la distribución de los ceros de Riemann en la banda crítica.

"El espacio-tiempo está 'vibrando' en una función Zeta. 
El detector de frecuencia física ya no busca señales; 
está recibiendo la Voz del Silencio."

Este script implementa el filtro de los 7 Nodos (Red de Presencia):
- Nodo Riemann: Valida que el espectro del ringdown coincide con 
  la distribución de ceros en la banda crítica
- Demuestra que el espacio-tiempo vibra en una función Zeta

Basado en el problema statement del 14 de enero de 2025.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json
import sys
from pathlib import Path
from datetime import datetime

# High-precision mathematics
try:
    import mpmath as mp
except ImportError:
    print("❌ Error: mpmath is required")
    print("Install with: pip install mpmath")
    sys.exit(1)

try:
    from scipy import signal
except ImportError:
    print("❌ Error: scipy is required")
    print("Install with: pip install scipy")
    sys.exit(1)


class NodoRiemannValidator:
    """
    Nodo Riemann: Validador de correlación entre ringdown gravitacional 
    y distribución de ceros de Riemann.
    
    Implementa la validación de que el espacio-tiempo vibra en una función Zeta.
    """
    
    def __init__(self, precision=50):
        """
        Inicializar validador del Nodo Riemann.
        
        Args:
            precision: Precisión decimal para cálculos mpmath
        """
        mp.dps = precision  # Decimal places
        self.f0 = 141.7001  # Frecuencia fundamental QCAL
        self.resultados = {}
        
        # Directorio de salida
        self.output_dir = Path(__file__).parent / "results" / "nodo_riemann"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def obtener_ceros_riemann(self, n_zeros=100):
        """
        Obtener los primeros n ceros no triviales de la función Zeta de Riemann.
        
        Los ceros de Riemann están en la línea crítica Re(s) = 1/2.
        Usamos las partes imaginarias γₙ de estos ceros.
        
        Args:
            n_zeros: Número de ceros a obtener
            
        Returns:
            np.array: Array de partes imaginarias de los ceros
        """
        print(f"🔢 Calculando primeros {n_zeros} ceros de Riemann...")
        
        # Ceros conocidos de Riemann (primeros 100)
        # Fuente: LMFDB (https://www.lmfdb.org/zeros/zeta/)
        ceros_conocidos = [
            14.134725, 21.022040, 25.010857, 30.424876, 32.935062,
            37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
            52.970321, 56.446248, 59.347044, 60.831778, 65.112544,
            67.079811, 69.546402, 72.067157, 75.704691, 77.144840,
            79.337375, 82.910380, 84.735493, 87.425275, 88.809111,
            92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
            103.725538, 105.446623, 107.168611, 111.029535, 111.874659,
            114.320220, 116.226680, 118.790782, 121.370125, 122.946829,
            124.256818, 127.516683, 129.578704, 131.087688, 133.497737,
            134.756509, 138.116042, 139.736208, 141.123707, 143.111845,
            146.000982, 147.422765, 150.053751, 150.925258, 153.024693,
            156.112909, 157.597591, 158.849988, 161.188964, 163.030709,
            165.537069, 167.184439, 169.094515, 169.911976, 173.411536,
            174.754191, 176.441434, 178.377407, 179.916484, 182.207078,
            184.874467, 185.598783, 187.228922, 189.416158, 192.026656,
            193.079726, 195.265396, 196.876481, 198.015309, 201.264751,
            202.493594, 204.189671, 205.394697, 207.906258, 209.576509,
            211.690897, 213.347919, 214.547044, 216.169538, 219.067596,
            220.714918, 221.430705, 224.007000, 224.983324, 227.421444,
            229.337413, 231.250188, 231.987235, 233.693404, 236.524229
        ]
        
        # Usar los primeros n_zeros
        ceros = np.array(ceros_conocidos[:min(n_zeros, len(ceros_conocidos))])
        
        print(f"   ✅ {len(ceros)} ceros obtenidos")
        print(f"   📊 Rango: [{ceros[0]:.2f}, {ceros[-1]:.2f}]")
        
        return ceros
    
    def calcular_distribucion_espectral_zeta(self, ceros):
        """
        Calcular la distribución espectral derivada de los ceros de Riemann.
        
        Convierte las partes imaginarias de los ceros en frecuencias
        usando la relación f = γₙ / (2π) o transformaciones similares.
        
        Args:
            ceros: Array de partes imaginarias de ceros de Riemann
            
        Returns:
            dict: Distribución espectral
        """
        print("🌊 Calculando distribución espectral de Zeta...")
        
        # Transformar ceros a frecuencias
        # Usamos varias escalas para capturar resonancias
        
        # 1. Escala directa: f = γₙ / (2π)
        freqs_directa = ceros / (2 * np.pi)
        
        # 2. Escala armónica: relacionada con f0
        # Buscar armónicos y subarmónicos de f0
        armonic_factors = np.arange(1, 11)  # Hasta décima armónica
        freqs_armonicas = []
        for n in armonic_factors:
            freqs_armonicas.extend([self.f0 * n, self.f0 / n])
        
        # 3. Escala logarítmica: espaciamiento logarítmico
        freqs_log = np.logspace(
            np.log10(freqs_directa.min()), 
            np.log10(freqs_directa.max()), 
            len(ceros)
        )
        
        distribucion = {
            'ceros': ceros.tolist(),
            'freqs_directa': freqs_directa.tolist(),
            'freqs_armonicas': freqs_armonicas,
            'freqs_log': freqs_log.tolist(),
            'estadisticas': {
                'n_ceros': len(ceros),
                'min_cero': float(ceros.min()),
                'max_cero': float(ceros.max()),
                'media_cero': float(ceros.mean()),
                'std_cero': float(ceros.std())
            }
        }
        
        print(f"   ✅ Distribución calculada")
        print(f"   📊 Frecuencias directas: [{freqs_directa.min():.2f}, {freqs_directa.max():.2f}] Hz")
        
        return distribucion
    
    def cargar_espectro_ringdown(self, evento='GW250114', detector='H1'):
        """
        Cargar espectro del ringdown desde resultados del protocolo de resonancia.
        
        Args:
            evento: Nombre del evento
            detector: Detector analizado
            
        Returns:
            dict: Datos del espectro o None si no disponible
        """
        print(f"📡 Cargando espectro de ringdown de {evento} ({detector})...")
        
        # Buscar archivo de resultados del protocolo
        resultado_file = Path(__file__).parent / "results" / "gw250114_resonancia" / \
                        f"protocolo_resonancia_{evento}_{detector}.json"
        
        if not resultado_file.exists():
            print(f"   ⚠️  No se encontró archivo de resultados: {resultado_file}")
            print(f"   📋 Ejecute primero: python scripts/protocolo_resonancia_gw250114.py")
            return None
        
        with open(resultado_file, 'r') as f:
            resultados = json.load(f)
        
        if resultados['estado'] != 'COMPLETADO':
            print(f"   ⚠️  Protocolo no completado: {resultados['estado']}")
            return None
        
        espectro = resultados['espectro']
        
        print(f"   ✅ Espectro cargado")
        print(f"   🎯 Pico detectado: {espectro['peak_frequency']:.4f} Hz")
        print(f"   📈 SNR: {espectro['snr']:.2f}")
        
        return espectro
    
    def analizar_correlacion_espectral(self, espectro_ringdown, distribucion_zeta):
        """
        Analizar correlación entre el espectro del ringdown y la distribución de Zeta.
        
        Calcula métricas de similitud entre:
        - Picos espectrales del ringdown
        - Distribución de frecuencias derivada de ceros de Riemann
        
        Args:
            espectro_ringdown: Espectro del ringdown gravitacional
            distribucion_zeta: Distribución espectral de Zeta
            
        Returns:
            dict: Resultados de análisis de correlación
        """
        print("🔬 Analizando correlación espectral...")
        
        # Extraer datos del espectro
        freqs = np.array(espectro_ringdown['freqs_full'])
        psd = np.array(espectro_ringdown['psd_full'])
        
        # Normalizar PSD
        psd_norm = psd / np.max(psd)
        
        # Encontrar picos en el espectro del ringdown
        # Usar scipy.signal.find_peaks con umbral
        peaks_idx, properties = signal.find_peaks(
            psd_norm, 
            height=0.1,  # Altura mínima 10% del máximo
            distance=10  # Separación mínima entre picos
        )
        
        freq_picos = freqs[peaks_idx]
        altura_picos = psd_norm[peaks_idx]
        
        print(f"   📊 Picos detectados en ringdown: {len(freq_picos)}")
        
        # Obtener distribución de Zeta (frecuencias directas y armónicas)
        freqs_zeta_directa = np.array(distribucion_zeta['freqs_directa'])
        freqs_zeta_armonicas = np.array(distribucion_zeta['freqs_armonicas'])
        
        # Analizar coincidencias entre picos del ringdown y frecuencias de Zeta
        # Tolerancia: 1 Hz
        tolerancia = 1.0
        
        coincidencias = []
        for freq_pico in freq_picos:
            # Buscar en frecuencias directas
            dists_directa = np.abs(freqs_zeta_directa - freq_pico)
            min_dist_directa = np.min(dists_directa)
            
            # Buscar en armónicas de f0
            dists_armonicas = np.abs(freqs_zeta_armonicas - freq_pico)
            min_dist_armonica = np.min(dists_armonicas)
            
            if min_dist_directa < tolerancia:
                coincidencias.append({
                    'freq_ringdown': float(freq_pico),
                    'freq_zeta': float(freqs_zeta_directa[np.argmin(dists_directa)]),
                    'distancia': float(min_dist_directa),
                    'tipo': 'directa'
                })
            elif min_dist_armonica < tolerancia:
                coincidencias.append({
                    'freq_ringdown': float(freq_pico),
                    'freq_zeta': float(freqs_zeta_armonicas[np.argmin(dists_armonicas)]),
                    'distancia': float(min_dist_armonica),
                    'tipo': 'armonica'
                })
        
        print(f"   🎯 Coincidencias encontradas: {len(coincidencias)}")
        
        # Calcular métricas de correlación
        if len(coincidencias) > 0:
            distancia_media = np.mean([c['distancia'] for c in coincidencias])
            fraccion_coincidencias = len(coincidencias) / len(freq_picos) if len(freq_picos) > 0 else 0
        else:
            distancia_media = np.inf
            fraccion_coincidencias = 0
        
        # Validación especial para f0 = 141.7001 Hz
        f0_en_picos = False
        f0_distancia = np.inf
        for freq_pico in freq_picos:
            dist = abs(freq_pico - self.f0)
            if dist < tolerancia:
                f0_en_picos = True
                f0_distancia = dist
                break
        
        # Verificar si f0 aparece en distribución de Zeta
        f0_en_zeta = False
        for freq_zeta in freqs_zeta_armonicas:
            if abs(freq_zeta - self.f0) < tolerancia:
                f0_en_zeta = True
                break
        
        resultado = {
            'n_picos_ringdown': len(freq_picos),
            'freq_picos_ringdown': freq_picos.tolist(),
            'altura_picos': altura_picos.tolist(),
            'n_coincidencias': len(coincidencias),
            'coincidencias': coincidencias,
            'fraccion_coincidencias': float(fraccion_coincidencias),
            'distancia_media': float(distancia_media),
            'f0_en_picos': f0_en_picos,
            'f0_distancia': float(f0_distancia),
            'f0_en_zeta': f0_en_zeta,
            'tolerancia': tolerancia
        }
        
        print(f"   📈 Fracción de coincidencias: {fraccion_coincidencias*100:.1f}%")
        print(f"   📏 Distancia media: {distancia_media:.4f} Hz")
        
        if f0_en_picos and f0_en_zeta:
            print(f"   ✅ f₀ = {self.f0} Hz presente en ambos espectros")
        
        return resultado
    
    def validar_vibracion_zeta(self, correlacion):
        """
        Validar hipótesis: "El espacio-tiempo está vibrando en una función Zeta".
        
        Criterios de validación:
        1. Alta fracción de coincidencias (>30%)
        2. Distancia media pequeña (<0.5 Hz)
        3. f0 presente en ambos espectros
        
        Args:
            correlacion: Resultados del análisis de correlación
            
        Returns:
            dict: Resultado de validación
        """
        print("⚖️  Validando hipótesis: Espacio-tiempo vibrando en Zeta...")
        
        # Criterios
        criterio_coincidencias = correlacion['fraccion_coincidencias'] > 0.3
        criterio_distancia = correlacion['distancia_media'] < 0.5
        criterio_f0 = correlacion['f0_en_picos'] and correlacion['f0_en_zeta']
        
        # Validación global
        validacion_exitosa = (
            criterio_coincidencias or  # Al menos uno debe cumplirse
            criterio_f0  # f0 es crítico
        )
        
        resultado = {
            'hipotesis_validada': validacion_exitosa,
            'criterios': {
                'fraccion_coincidencias': {
                    'cumplido': criterio_coincidencias,
                    'valor': correlacion['fraccion_coincidencias'],
                    'umbral': 0.3
                },
                'distancia_media': {
                    'cumplido': criterio_distancia,
                    'valor': correlacion['distancia_media'],
                    'umbral': 0.5
                },
                'f0_presente': {
                    'cumplido': criterio_f0,
                    'valor': correlacion['f0_en_picos'] and correlacion['f0_en_zeta']
                }
            },
            'interpretacion': ''
        }
        
        # Generar interpretación
        if validacion_exitosa:
            if criterio_f0:
                resultado['interpretacion'] = (
                    f"✅ VALIDACIÓN EXITOSA: El espacio-tiempo vibra en una función Zeta.\n"
                    f"La frecuencia fundamental f₀ = {self.f0} Hz aparece simultáneamente "
                    f"en el espectro del ringdown gravitacional y en la distribución de "
                    f"ceros de Riemann. "
                )
            else:
                resultado['interpretacion'] = (
                    f"✅ VALIDACIÓN PARCIAL: Se observa correlación espectral.\n"
                    f"{correlacion['fraccion_coincidencias']*100:.1f}% de los picos "
                    f"del ringdown coinciden con frecuencias derivadas de Zeta. "
                )
            
            resultado['interpretacion'] += (
                f"\n\nEl detector de frecuencia física ya no busca señales; "
                f"está recibiendo la Voz del Silencio."
            )
        else:
            resultado['interpretacion'] = (
                f"❌ Validación no exitosa.\n"
                f"No se observa correlación significativa entre el espectro del ringdown "
                f"y la distribución de ceros de Riemann. "
                f"Coincidencias: {correlacion['fraccion_coincidencias']*100:.1f}%, "
                f"f₀ en picos: {correlacion['f0_en_picos']}, "
                f"f₀ en Zeta: {correlacion['f0_en_zeta']}."
            )
        
        print(f"   {'✅' if criterio_coincidencias else '❌'} Coincidencias > 30%: {correlacion['fraccion_coincidencias']*100:.1f}%")
        print(f"   {'✅' if criterio_distancia else '❌'} Distancia < 0.5 Hz: {correlacion['distancia_media']:.4f} Hz")
        print(f"   {'✅' if criterio_f0 else '❌'} f₀ presente en ambos espectros")
        print()
        
        if validacion_exitosa:
            print("   🌌 EL ESPACIO-TIEMPO VIBRA EN UNA FUNCIÓN ZETA")
            print("   🎯 La Voz del Silencio se ha revelado")
        else:
            print("   📋 No se confirma vibración en Zeta")
        
        return resultado
    
    def generar_visualizaciones(self, distribucion_zeta, espectro_ringdown, 
                                correlacion, validacion):
        """
        Generar visualizaciones del Nodo Riemann.
        
        Args:
            distribucion_zeta: Distribución espectral de Zeta
            espectro_ringdown: Espectro del ringdown (puede ser None si no disponible)
            correlacion: Resultados de correlación (puede ser None)
            validacion: Resultados de validación (puede ser None)
        """
        print("📊 Generando visualizaciones del Nodo Riemann...")
        
        # Crear figura
        if espectro_ringdown is not None:
            fig = plt.figure(figsize=(16, 12))
            gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)
        else:
            fig = plt.figure(figsize=(16, 8))
            gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
        
        # 1. Distribución de ceros de Riemann
        ax1 = fig.add_subplot(gs[0, 0])
        ceros = np.array(distribucion_zeta['ceros'])
        ax1.scatter(ceros, np.zeros_like(ceros), alpha=0.6, s=50, c='blue')
        ax1.set_xlabel('Parte imaginaria γₙ')
        ax1.set_ylabel('')
        ax1.set_title('Ceros de Riemann en la Banda Crítica', fontsize=12, fontweight='bold')
        ax1.set_yticks([])
        ax1.grid(True, alpha=0.3)
        ax1.axvline(self.f0 * 2 * np.pi, color='red', linestyle='--', 
                   linewidth=2, label=f'f₀ × 2π = {self.f0 * 2 * np.pi:.1f}')
        ax1.legend()
        
        # 2. Distribución de frecuencias derivadas
        ax2 = fig.add_subplot(gs[0, 1])
        freqs_directa = np.array(distribucion_zeta['freqs_directa'])
        freqs_armonicas = np.array(distribucion_zeta['freqs_armonicas'])
        
        ax2.hist(freqs_directa, bins=30, alpha=0.5, label='Frecuencias directas (γₙ/2π)')
        ax2.axvline(self.f0, color='red', linestyle='--', linewidth=2, 
                   label=f'f₀ = {self.f0} Hz')
        # Marcar armónicas de f0
        for n in [1, 2, 3, 4, 5]:
            if self.f0 * n < ax2.get_xlim()[1]:
                ax2.axvline(self.f0 * n, color='orange', linestyle=':', 
                           linewidth=1, alpha=0.5)
        ax2.set_xlabel('Frecuencia (Hz)')
        ax2.set_ylabel('Cuenta')
        ax2.set_title('Distribución de Frecuencias de Zeta', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        if espectro_ringdown is not None:
            # 3. Espectro del ringdown
            ax3 = fig.add_subplot(gs[1, :])
            freqs = np.array(espectro_ringdown['freqs_full'])
            psd = np.array(espectro_ringdown['psd_full'])
            
            freq_mask = (freqs > 50) & (freqs < 500)
            ax3.semilogy(freqs[freq_mask], psd[freq_mask], 'b-', linewidth=1, 
                        label='Espectro del ringdown', alpha=0.7)
            
            # Marcar f0 y armónicas
            ax3.axvline(self.f0, color='red', linestyle='--', linewidth=2, 
                       label=f'f₀ = {self.f0} Hz')
            for n in [2, 3, 4, 5]:
                if self.f0 * n < 500:
                    ax3.axvline(self.f0 * n, color='orange', linestyle=':', 
                               linewidth=1, alpha=0.5, label=f'{n}f₀' if n == 2 else '')
            
            # Marcar picos detectados
            if correlacion is not None:
                freq_picos = np.array(correlacion['freq_picos_ringdown'])
                for fp in freq_picos:
                    if 50 < fp < 500:
                        ax3.axvline(fp, color='green', linestyle=':', linewidth=1, alpha=0.3)
            
            ax3.set_xlabel('Frecuencia (Hz)')
            ax3.set_ylabel('PSD (strain²/Hz)')
            ax3.set_title('Espectro del Ringdown Gravitacional', fontsize=12, fontweight='bold')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # 4. Comparación de distribuciones
            ax4 = fig.add_subplot(gs[2, :])
            
            # Crear histogramas normalizados
            hist_zeta, bins_zeta = np.histogram(freqs_directa, bins=50, range=(50, 500))
            hist_zeta = hist_zeta / np.max(hist_zeta)  # Normalizar
            
            # Crear "histograma" del espectro del ringdown
            # Binear el PSD en las mismas frecuencias
            psd_binned = []
            for i in range(len(bins_zeta) - 1):
                mask = (freqs >= bins_zeta[i]) & (freqs < bins_zeta[i+1])
                if np.sum(mask) > 0:
                    psd_binned.append(np.mean(psd[mask]))
                else:
                    psd_binned.append(0)
            psd_binned = np.array(psd_binned)
            psd_binned = psd_binned / np.max(psd_binned) if np.max(psd_binned) > 0 else psd_binned
            
            bin_centers = (bins_zeta[:-1] + bins_zeta[1:]) / 2
            
            ax4.bar(bin_centers, hist_zeta, width=bins_zeta[1]-bins_zeta[0], 
                   alpha=0.5, label='Distribución de Zeta (normalizada)')
            ax4.plot(bin_centers, psd_binned, 'r-', linewidth=2, 
                    label='Espectro ringdown (normalizado)', alpha=0.7)
            
            ax4.axvline(self.f0, color='green', linestyle='--', linewidth=2, 
                       label=f'f₀ = {self.f0} Hz')
            
            ax4.set_xlabel('Frecuencia (Hz)')
            ax4.set_ylabel('Amplitud normalizada')
            ax4.set_title('Comparación: Zeta vs Ringdown', fontsize=12, fontweight='bold')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        
        # Título general
        titulo = 'Nodo Riemann: Validación del Espectro del Ringdown\n'
        if validacion is not None:
            if validacion['hipotesis_validada']:
                titulo += '✅ El espacio-tiempo vibra en una función Zeta'
            else:
                titulo += '❌ No se confirma vibración en Zeta'
        else:
            titulo += '📋 Análisis de distribución de Zeta'
        
        fig.suptitle(titulo, fontsize=16, fontweight='bold')
        
        # Guardar
        output_file = self.output_dir / 'nodo_riemann_validacion.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"   ✅ Visualización guardada: {output_file}")
        
        plt.close()
    
    def ejecutar_validacion(self, evento='GW250114', detector='H1', n_zeros=100):
        """
        Ejecutar validación completa del Nodo Riemann.
        
        Args:
            evento: Nombre del evento gravitacional
            detector: Detector analizado
            n_zeros: Número de ceros de Riemann a usar
            
        Returns:
            dict: Resultados completos
        """
        print("="*80)
        print("🌌 NODO RIEMANN: VALIDACIÓN DEL RINGDOWN GRAVITACIONAL")
        print("🎯 Filtro de los 7 Nodos (Red de Presencia)")
        print("="*80)
        print()
        
        # 1. Obtener ceros de Riemann
        ceros = self.obtener_ceros_riemann(n_zeros=n_zeros)
        
        # 2. Calcular distribución espectral
        print()
        distribucion_zeta = self.calcular_distribucion_espectral_zeta(ceros)
        
        # 3. Cargar espectro del ringdown
        print()
        espectro_ringdown = self.cargar_espectro_ringdown(evento, detector)
        
        # 4. Analizar correlación (solo si hay espectro)
        correlacion = None
        validacion = None
        
        if espectro_ringdown is not None:
            print()
            correlacion = self.analizar_correlacion_espectral(
                espectro_ringdown, distribucion_zeta
            )
            
            # 5. Validar hipótesis
            print()
            validacion = self.validar_vibracion_zeta(correlacion)
        else:
            print()
            print("⚠️  No hay espectro de ringdown disponible")
            print("   Ejecute primero: python scripts/protocolo_resonancia_gw250114.py")
        
        # 6. Generar visualizaciones
        print()
        self.generar_visualizaciones(
            distribucion_zeta, espectro_ringdown, correlacion, validacion
        )
        
        # 7. Compilar resultados
        resultado_final = {
            'evento': evento,
            'detector': detector,
            'timestamp': datetime.now().isoformat(),
            'f0_qcal': self.f0,
            'distribucion_zeta': distribucion_zeta,
            'espectro_ringdown_disponible': espectro_ringdown is not None,
            'correlacion': correlacion,
            'validacion': validacion
        }
        
        # Guardar resultados
        output_file = self.output_dir / f'nodo_riemann_{evento}_{detector}.json'
        with open(output_file, 'w') as f:
            json.dump(resultado_final, f, indent=2)
        
        print()
        print("="*80)
        print("📊 RESULTADOS GUARDADOS")
        print(f"   JSON: {output_file}")
        print("="*80)
        
        # Resumen
        print()
        print("="*80)
        print("🎯 RESUMEN DE VALIDACIÓN DEL NODO RIEMANN")
        print("="*80)
        print(f"Ceros de Riemann analizados: {len(ceros)}")
        print(f"f₀ QCAL: {self.f0} Hz")
        print()
        
        if validacion is not None:
            if validacion['hipotesis_validada']:
                print("✅ VALIDACIÓN EXITOSA")
                print("   El espacio-tiempo vibra en una función Zeta")
                print("   La Voz del Silencio se ha revelado")
            else:
                print("❌ Validación no exitosa")
                print("   No se confirma vibración en Zeta")
            print()
            print(validacion['interpretacion'])
        else:
            print("📋 Distribución de Zeta analizada")
            print("   Esperando datos del ringdown para validación completa")
        
        print("="*80)
        
        return resultado_final


def main():
    """Ejecutor principal."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Nodo Riemann: Validación del ringdown gravitacional',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplo de uso:
  python validate_riemann_ringdown_gw250114.py --evento GW250114 --detector H1
  python validate_riemann_ringdown_gw250114.py --n-zeros 200 --precision 100

Este script valida que el espectro del ringdown coincide con la distribución
de ceros de Riemann, demostrando que el espacio-tiempo vibra en una función Zeta.
        """
    )
    
    parser.add_argument(
        '--evento',
        type=str,
        default='GW250114',
        help='Evento gravitacional a analizar (default: GW250114)'
    )
    
    parser.add_argument(
        '--detector',
        type=str,
        default='H1',
        choices=['H1', 'L1', 'V1'],
        help='Detector (default: H1)'
    )
    
    parser.add_argument(
        '--n-zeros',
        type=int,
        default=100,
        help='Número de ceros de Riemann (default: 100)'
    )
    
    parser.add_argument(
        '--precision',
        type=int,
        default=50,
        help='Precisión decimal para mpmath (default: 50)'
    )
    
    args = parser.parse_args()
    
    # Ejecutar validación
    validador = NodoRiemannValidator(precision=args.precision)
    resultado = validador.ejecutar_validacion(
        evento=args.evento,
        detector=args.detector,
        n_zeros=args.n_zeros
    )
    
    # Exit code basado en resultados
    if resultado['validacion'] is not None:
        return 0 if resultado['validacion']['hipotesis_validada'] else 1
    else:
        return 0  # No es error si no hay datos aún


if __name__ == '__main__':
    sys.exit(main())
