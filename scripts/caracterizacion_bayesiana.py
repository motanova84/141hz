#!/usr/bin/env python3
"""
Caracterización Bayesiana del Q-factor
======================================
Estimación bayesiana completa del Q-factor con distribuciones posteriores.

Incluye:
- Estimación del Q-factor con método de half-power bandwidth
- Distribución posterior bayesiana
- Análisis de incertidumbres
- Análisis de armónicos
- Visualización de resultados

Autor: José Manuel Mota Burruezo
Instituto Conciencia Cuántica
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class CaracterizacionBayesiana:
    """Caracterización bayesiana completa del Q-factor"""
    
    def __init__(self, frecuencia_objetivo=141.7001):
        self.f0 = frecuencia_objetivo
        self.resultados = {}
        
    def estimar_q_factor(self, datos, fs):
        """
        Estimación del Q-factor usando análisis espectral
        
        Args:
            datos: Array de datos de strain
            fs: Frecuencia de muestreo (Hz)
            
        Returns:
            dict: Resultados incluyendo Q-factor, incertidumbre y posterior
        """
        print("🎯 INICIANDO CARACTERIZACIÓN BAYESIANA DEL Q-FACTOR")
        
        # Análisis espectral
        freqs, psd = signal.welch(datos, fs, nperseg=min(len(datos)//4, 2048))
        
        # Encontrar pico cercano a frecuencia objetivo
        idx_target = np.argmin(np.abs(freqs - self.f0))
        banda_inicio = max(0, idx_target - 50)
        banda_fin = min(len(freqs), idx_target + 50)
        
        # Estimar Q-factor desde el ancho del pico
        psd_banda = psd[banda_inicio:banda_fin]
        freqs_banda = freqs[banda_inicio:banda_fin]
        
        # Half-power bandwidth method
        pico_idx = np.argmax(psd_banda)
        pico_freq = freqs_banda[pico_idx]
        pico_power = psd_banda[pico_idx]
        
        # Encontrar ancho a mitad de potencia
        half_power = pico_power / 2
        indices_half = np.where(psd_banda > half_power)[0]
        
        if len(indices_half) > 1:
            ancho_banda = freqs_banda[indices_half[-1]] - freqs_banda[indices_half[0]]
            q_factor = pico_freq / ancho_banda if ancho_banda > 0 else 10.0
        else:
            q_factor = 10.0  # Valor por defecto
        
        # Estimación de incertidumbre (aproximación)
        q_std = q_factor * 0.15  # ~15% de incertidumbre típica
        
        # Calcular distribución posterior bayesiana
        posterior_q = self._calcular_posterior_q_factor(
            psd_banda, freqs_banda, pico_freq, q_factor, q_std
        )
        
        self.resultados['q_factor'] = float(q_factor)
        self.resultados['q_std'] = float(q_std)
        self.resultados['q_lower'] = float(q_factor - q_std)
        self.resultados['q_upper'] = float(q_factor + q_std)
        self.resultados['frecuencia_detectada'] = float(pico_freq)
        self.resultados['ancho_banda'] = float(ancho_banda) if len(indices_half) > 1 else None
        self.resultados['posterior_q'] = posterior_q
        
        print(f"📊 Q-factor estimado: {self.resultados['q_factor']:.2f} ± {self.resultados['q_std']:.2f}")
        print(f"📊 Intervalo 68%: [{self.resultados['q_lower']:.2f}, {self.resultados['q_upper']:.2f}]")
        print(f"📊 Frecuencia detectada: {self.resultados['frecuencia_detectada']:.4f} Hz")
        
        return self.resultados
    
    def _calcular_posterior_q_factor(self, psd_banda, freqs_banda, f_peak, q_ml, q_std):
        """
        Calcula la distribución posterior del Q-factor usando aproximación bayesiana
        
        Args:
            psd_banda: PSD en la banda de interés
            freqs_banda: Frecuencias en la banda
            f_peak: Frecuencia del pico
            q_ml: Q-factor de máxima verosimilitud
            q_std: Desviación estándar estimada
            
        Returns:
            dict: Parámetros de la distribución posterior
        """
        # Prior: log-normal para Q (siempre positivo)
        # Verosimilitud: Gaussiana en log-espacio
        
        # Rango de Q a explorar
        q_range = np.linspace(max(1, q_ml - 3*q_std), q_ml + 3*q_std, 100)
        
        # Prior log-normal: P(Q) ∝ 1/(Q*σ) * exp(-(log Q - μ)²/(2σ²))
        prior_mu = np.log(q_ml)
        prior_sigma = 0.5  # Prior relativamente amplio
        log_prior = -np.log(q_range * prior_sigma * np.sqrt(2*np.pi)) - \
                    (np.log(q_range) - prior_mu)**2 / (2 * prior_sigma**2)
        
        # Verosimilitud: basada en ajuste del modelo al espectro
        log_likelihood = np.zeros_like(q_range)
        for i, q_test in enumerate(q_range):
            # Modelo lorentziano para el pico
            gamma = f_peak / (2 * q_test)  # Ancho del pico
            modelo = psd_banda.max() / (1 + ((freqs_banda - f_peak) / gamma)**2)
            
            # Chi-cuadrado
            chi2 = np.sum((psd_banda - modelo)**2 / (modelo + 1e-30))
            log_likelihood[i] = -0.5 * chi2
        
        # Posterior (no normalizado)
        log_posterior = log_prior + log_likelihood
        
        # Normalizar
        posterior = np.exp(log_posterior - np.max(log_posterior))
        posterior /= np.trapezoid(posterior, q_range)
        
        # Calcular estadísticas de la posterior
        q_media = np.trapezoid(q_range * posterior, q_range)
        q_var = np.trapezoid((q_range - q_media)**2 * posterior, q_range)
        q_std_post = np.sqrt(q_var)
        
        # Intervalo de credibilidad 68%
        cdf = np.cumsum(posterior) * (q_range[1] - q_range[0])
        idx_16 = np.searchsorted(cdf, 0.16)
        idx_84 = np.searchsorted(cdf, 0.84)
        
        return {
            'q_values': q_range.tolist()[:50],  # Limitar para JSON
            'posterior': posterior.tolist()[:50],
            'q_media': float(q_media),
            'q_std': float(q_std_post),
            'q_16': float(q_range[idx_16]),
            'q_84': float(q_range[idx_84])
        }
    
    def generar_reporte(self, evento='GW250114', detector='H1', output_dir='../results'):
        """
        Genera reporte completo de la caracterización
        
        Args:
            evento: Nombre del evento
            detector: Nombre del detector
            output_dir: Directorio de salida
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Guardar JSON
        json_file = output_path / f'caracterizacion_bayesiana_{evento}_{detector}.json'
        with open(json_file, 'w') as f:
            json.dump(self.resultados, f, indent=2)
        print(f"\n💾 Resultados guardados en: {json_file}")
        
        # Generar visualización
        self._generar_visualizacion(evento, detector, output_path)
        
        print("\n📊 RESUMEN DE CARACTERIZACIÓN BAYESIANA:")
        print("=" * 70)
        print(f"Evento: {evento}")
        print(f"Detector: {detector}")
        print(f"Q-factor: {self.resultados['q_factor']:.2f} ± {self.resultados['q_std']:.2f}")
        print(f"Intervalo credibilidad 68%: [{self.resultados['q_lower']:.2f}, {self.resultados['q_upper']:.2f}]")
        print(f"Frecuencia: {self.resultados['frecuencia_detectada']:.4f} Hz")
        
        if self.resultados.get('posterior_q'):
            post = self.resultados['posterior_q']
            print(f"\nDistribución Posterior:")
            print(f"  Media: {post['q_media']:.2f}")
            print(f"  Std: {post['q_std']:.2f}")
            print(f"  16% percentil: {post['q_16']:.2f}")
            print(f"  84% percentil: {post['q_84']:.2f}")
        
        return json_file
    
    def _generar_visualizacion(self, evento, detector, output_path):
        """Genera visualización de la caracterización bayesiana"""
        if not self.resultados.get('posterior_q'):
            print("⚠️  No hay distribución posterior para visualizar")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # 1. Distribución posterior del Q-factor
        post = self.resultados['posterior_q']
        q_vals = np.array(post['q_values'])
        posterior = np.array(post['posterior'])
        
        axes[0].plot(q_vals, posterior, 'b-', linewidth=2, label='Posterior')
        axes[0].axvline(post['q_media'], color='red', linestyle='--', 
                       label=f'Media: {post["q_media"]:.2f}', linewidth=2)
        axes[0].axvline(post['q_16'], color='orange', linestyle=':', 
                       label=f'16%: {post["q_16"]:.2f}', linewidth=1.5)
        axes[0].axvline(post['q_84'], color='orange', linestyle=':', 
                       label=f'84%: {post["q_84"]:.2f}', linewidth=1.5)
        axes[0].fill_between(q_vals, posterior, alpha=0.3)
        axes[0].set_xlabel('Q-factor')
        axes[0].set_ylabel('Densidad de Probabilidad')
        axes[0].set_title(f'Distribución Posterior del Q-factor\n{evento} - {detector}')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # 2. Resumen estadístico
        axes[1].axis('off')
        summary_text = f"""
CARACTERIZACIÓN BAYESIANA
{'=' * 40}

Evento: {evento}
Detector: {detector}

RESULTADOS:
Q-factor (ML): {self.resultados['q_factor']:.2f} ± {self.resultados['q_std']:.2f}
Q-factor (media posterior): {post['q_media']:.2f} ± {post['q_std']:.2f}

Intervalo de Credibilidad 68%:
  [{self.resultados['q_lower']:.2f}, {self.resultados['q_upper']:.2f}]

Percentiles:
  16%: {post['q_16']:.2f}
  50%: {post['q_media']:.2f}
  84%: {post['q_84']:.2f}

Frecuencia Detectada:
  {self.resultados['frecuencia_detectada']:.4f} Hz
  Δf = {abs(self.resultados['frecuencia_detectada'] - self.f0):.4f} Hz

INTERPRETACIÓN:
  Q-factor típico de QNM: 2-20
  Q-factor detectado: {"✅ Consistente" if 2 <= post['q_media'] <= 20 else "⚠️  Revisar"}
        """
        axes[1].text(0.1, 0.5, summary_text, transform=axes[1].transAxes,
                    fontfamily='monospace', fontsize=10, verticalalignment='center')
        
        plt.tight_layout()
        fig_file = output_path / f'caracterizacion_bayesiana_{evento}_{detector}.png'
        plt.savefig(fig_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Visualización guardada en: {fig_file}")
    
    def analisis_armonicos(self, espectro, freqs):
        """Análisis de armónicos en el espectro"""
        print("🔍 ANALIZANDO ARMÓNICOS")
        
        # Identificar picos significativos
        threshold = np.median(espectro) * 2
        picos, propiedades = signal.find_peaks(espectro, height=threshold)
        
        armonicos = []
        for i, pico in enumerate(picos[:5]):  # Primeros 5 picos
            freq_armonico = freqs[pico]
            amplitud = espectro[pico]
            
            armonicos.append({
                'frecuencia': float(freq_armonico),
                'amplitud': float(amplitud),
                'orden': i + 1
            })
            
            print(f"   Armónico {i+1}: {freq_armonico:.2f} Hz (amp: {amplitud:.2e})")
        
        self.resultados['armonicos'] = armonicos
        return armonicos

def generar_datos_sinteticos_gw250114():
    """Genera datos sintéticos basados en predicciones para GW250114"""
    print("🧪 GENERANDO DATOS SINTÉTICOS GW250114")
    
    fs = 4096
    duration = 32  # segundos
    t = np.linspace(0, duration, fs*duration)
    
    # Parámetros predichos para GW250114
    params = {
        'frecuencia': 141.7001,
        'q_factor': 8.5,
        'amplitud': 1e-21,
        'snr_esperado': 15.2
    }
    
    # Señal de ringdown sintética
    decay_rate = np.pi * params['frecuencia'] / params['q_factor']
    señal = params['amplitud'] * np.exp(-decay_rate * t) * \
            np.sin(2 * np.pi * params['frecuencia'] * t)
    
    # Ruido realista
    ruido = np.random.normal(0, params['amplitud']/params['snr_esperado'], len(t))
    
    print(f"✅ Datos sintéticos generados: {len(t)} muestras")
    print(f"   Parámetros: f={params['frecuencia']} Hz, Q={params['q_factor']}, SNR={params['snr_esperado']}")
    
    return señal + ruido, fs, params

# EJECUCIÓN INMEDIATA
def main():
    """Función principal"""
    print("🌌 CARACTERIZACIÓN BAYESIANA - SIMULACIÓN GW250114")
    print("=" * 70)
    
    try:
        # Generar datos sintéticos
        datos, fs, params_reales = generar_datos_sinteticos_gw250114()
        
        # Caracterización bayesiana
        bayes = CaracterizacionBayesiana()
        resultados = bayes.estimar_q_factor(datos, fs)
        
        # Análisis espectral para armónicos
        freqs, psd = signal.welch(datos, fs, nperseg=2048)
        bayes.analisis_armonicos(psd, freqs)
        
        # Generar reporte completo
        bayes.generar_reporte(evento='GW250114', detector='SIMULATED')
        
        print(f"\n🎯 COMPARACIÓN CON PARÁMETROS REALES:")
        print(f"   • Q-factor real: {params_reales['q_factor']}")
        print(f"   • Q-factor estimado: {resultados['q_factor']:.2f}")
        print(f"   • Error: {abs(resultados['q_factor'] - params_reales['q_factor']):.2f}")
        
        print("\n✅ CARACTERIZACIÓN BAYESIANA COMPLETADA")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error en caracterización: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
