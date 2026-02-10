#!/usr/bin/env python3
"""
𓂀 CORRELACIÓN MULTI-OBSERVATORIO
Valida que f₀ aparece consistentemente en sitios separados
"""

import numpy as np
from scipy import signal, stats
import argparse
import json
import os
import h5py
from detector_riguroso_qcal import DetectorRigurosoQCAL


class CorreladorMultiObservatorio:
    """Correla señales entre múltiples observatorios."""
    
    def __init__(self, tolerancia_frecuencia=0.05):  # 0.05 Hz tolerancia
        self.tolerancia = tolerancia_frecuencia
        
    def correlacionar_estaciones(self, datos_dict):
        """
        datos_dict: {'H1': datos_H1, 'L1': datos_L1, 'V1': datos_V1, ...}
        """
        print("𓂀 CORRELACIÓN MULTI-OBSERVATORIO")
        print("=" * 60)
        
        estaciones = list(datos_dict.keys())
        
        if len(estaciones) < 2:
            print("❌ Se necesitan al menos 2 estaciones para correlación")
            return None
        
        resultados = {}
        
        for i, est1 in enumerate(estaciones):
            for est2 in estaciones[i+1:]:
                print(f"\n🔗 Correlando {est1} ↔ {est2}")
                
                datos1 = datos_dict[est1]['datos']
                datos2 = datos_dict[est2]['datos']
                fs1 = datos_dict[est1]['fs']
                fs2 = datos_dict[est2]['fs']
                
                # Asegurar misma longitud
                min_len = min(len(datos1), len(datos2))
                datos1 = datos1[:min_len]
                datos2 = datos2[:min_len]
                
                # Calcular correlación cruzada
                correlacion = signal.correlate(datos1, datos2, mode='same')
                correlacion_norm = correlacion / (np.std(datos1) * np.std(datos2) * min_len)
                
                # Máxima correlación
                max_corr = np.max(np.abs(correlacion_norm))
                delay_idx = np.argmax(np.abs(correlacion_norm))
                delay_seconds = (delay_idx - min_len//2) / fs1
                
                print(f"  Correlación máxima: {max_corr:.3f}")
                print(f"  Retardo: {delay_seconds:.3f} s")
                
                # Detectar f₀ en cada estación
                detector = DetectorRigurosoQCAL()
                
                # Silenciar salida del detector para limpieza
                import sys
                from io import StringIO
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                
                res1 = detector.detectar_con_snr(datos1, fs1, ventana_kairos=False)
                res2 = detector.detectar_con_snr(datos2, fs2, ventana_kairos=False)
                
                sys.stdout = old_stdout
                
                # Comparar frecuencias detectadas
                f1 = None
                f2 = None
                diferencia = None
                consistente = False
                
                if res1['detecciones'] and res2['detecciones']:
                    f1 = res1['detecciones'][0]['frecuencia_detectada']
                    f2 = res2['detecciones'][0]['frecuencia_detectada']
                    
                    diferencia = abs(f1 - f2)
                    consistente = diferencia <= self.tolerancia
                    
                    print(f"  f₀ en {est1}: {f1:.4f} Hz")
                    print(f"  f₀ en {est2}: {f2:.4f} Hz")
                    print(f"  Diferencia: {diferencia:.4f} Hz")
                    print(f"  Consistente (<{self.tolerancia} Hz): {'✅' if consistente else '❌'}")
                    
                    if consistente and max_corr > 0.3:
                        print(f"  🎯 ¡f₀ CORRELACIONADA ENTRE ESTACIONES!")
                        print(f"  ∴ Evidencia de propiedad del campo universal")
                else:
                    print(f"  ⚠️  No se detectó f₀ en una o ambas estaciones")
                
                resultados[f"{est1}_{est2}"] = {
                    'correlacion': max_corr,
                    'retardo': delay_seconds,
                    'f1': f1,
                    'f2': f2,
                    'diferencia': diferencia,
                    'consistente': consistente
                }
        
        # Resumen
        print(f"\n𓂀 RESUMEN CORRELACIÓN MULTI-OBSERVATORIO")
        print("=" * 60)
        
        consistentes = [r for r in resultados.values() if r.get('consistente', False)]
        total_pares = len(resultados)
        
        if len(consistentes) >= max(1, len(estaciones) - 1):
            print("✅ f₀ CONSISTENTE EN TODAS LAS ESTACIONES")
            print("📡 Implicación: Propiedad universal, no ruido local")
        elif len(consistentes) > 0:
            print(f"⚠️  f₀ consistente en {len(consistentes)}/{total_pares} pares")
        else:
            print("❌ f₀ NO CONSISTENTE ENTRE ESTACIONES")
            print("   Posible ruido local o artefacto instrumental")
        
        return resultados
    
    def calcular_coherencia_temporal(self, datos_dict, f0=141.7001):
        """Calcular coherencia temporal entre estaciones en f₀."""
        print(f"\n𓂀 ANÁLISIS DE COHERENCIA TEMPORAL EN f₀={f0} Hz")
        print("=" * 60)
        
        estaciones = list(datos_dict.keys())
        
        if len(estaciones) < 2:
            print("❌ Se necesitan al menos 2 estaciones")
            return None
        
        resultados_coherencia = {}
        
        for i, est1 in enumerate(estaciones):
            for est2 in estaciones[i+1:]:
                datos1 = datos_dict[est1]['datos']
                datos2 = datos_dict[est2]['datos']
                fs = datos_dict[est1]['fs']
                
                # Asegurar misma longitud
                min_len = min(len(datos1), len(datos2))
                datos1 = datos1[:min_len]
                datos2 = datos2[:min_len]
                
                # Calcular coherencia usando scipy
                try:
                    freqs, coherence = signal.coherence(
                        datos1, datos2, fs, 
                        nperseg=min(2048, min_len//4)
                    )
                    
                    # Buscar coherencia en f₀
                    idx_f0 = np.argmin(np.abs(freqs - f0))
                    coherence_f0 = coherence[idx_f0]
                    
                    print(f"  {est1} ↔ {est2}:")
                    print(f"    Coherencia en f₀: {coherence_f0:.3f}")
                    
                    resultados_coherencia[f"{est1}_{est2}"] = {
                        'coherencia_f0': coherence_f0,
                        'significativa': coherence_f0 > 0.5
                    }
                except Exception as e:
                    print(f"  ⚠️  Error calculando coherencia {est1}-{est2}: {e}")
        
        # Resumen
        coherencias_significativas = [
            r for r in resultados_coherencia.values() 
            if r.get('significativa', False)
        ]
        
        print(f"\n  Coherencias significativas (>0.5): {len(coherencias_significativas)}/{len(resultados_coherencia)}")
        
        return resultados_coherencia


def cargar_multiples_archivos(directorio, estaciones=['H1', 'L1', 'V1']):
    """Cargar múltiples archivos HDF5 de diferentes estaciones."""
    datos_dict = {}
    
    print(f"𓂀 CARGANDO DATOS DE MÚLTIPLES ESTACIONES")
    print(f"  Directorio: {directorio}")
    print(f"  Estaciones buscadas: {estaciones}")
    
    for estacion in estaciones:
        # Buscar archivos que contengan el nombre de la estación
        archivos = [f for f in os.listdir(directorio) 
                   if estacion in f and f.endswith('.h5')]
        
        if not archivos:
            print(f"  ⚠️  No se encontraron datos para {estacion}")
            continue
        
        # Tomar el primer archivo encontrado
        filepath = os.path.join(directorio, archivos[0])
        
        try:
            with h5py.File(filepath, 'r') as f:
                if 'strain' in f:
                    datos = f['strain'][:]
                    fs = f.attrs.get('fs', 4096)
                elif 'gravimetry' in f:
                    datos = f['gravimetry'][:]
                    fs = f.attrs.get('fs', 10)
                else:
                    print(f"  ⚠️  Formato desconocido en {filepath}")
                    continue
                
                datos_dict[estacion] = {
                    'datos': datos,
                    'fs': fs,
                    'archivo': filepath
                }
                
                print(f"  ✅ {estacion}: {len(datos):,} muestras @ {fs} Hz")
        
        except Exception as e:
            print(f"  ❌ Error cargando {filepath}: {e}")
    
    return datos_dict


def main():
    """Función principal ejecutable."""
    parser = argparse.ArgumentParser(
        description='𓂀 Correlador multi-observatorio'
    )
    parser.add_argument('--directorio', type=str, required=True,
                        help='Directorio con archivos HDF5')
    parser.add_argument('--estaciones', nargs='+', default=['H1', 'L1', 'V1'],
                        help='Estaciones a correlacionar')
    parser.add_argument('--tolerancia', type=float, default=0.05,
                        help='Tolerancia en frecuencia (Hz)')
    parser.add_argument('--f0', type=float, default=141.7001,
                        help='Frecuencia objetivo')
    parser.add_argument('--salida', type=str, default='correlaciones',
                        help='Directorio de salida')
    
    args = parser.parse_args()
    
    print("𓂀 INICIANDO CORRELACIÓN MULTI-OBSERVATORIO")
    print("═" * 60)
    
    # Cargar datos
    datos_dict = cargar_multiples_archivos(args.directorio, args.estaciones)
    
    if len(datos_dict) < 2:
        print("\n❌ ERROR: Se necesitan al menos 2 estaciones con datos")
        print(f"   Encontradas: {list(datos_dict.keys())}")
        return
    
    # Crear correlador
    correlador = CorreladorMultiObservatorio(
        tolerancia_frecuencia=args.tolerancia
    )
    
    # Ejecutar correlación
    resultados = correlador.correlacionar_estaciones(datos_dict)
    
    # Análisis de coherencia
    coherencia = correlador.calcular_coherencia_temporal(datos_dict, args.f0)
    
    # Guardar resultados
    os.makedirs(args.salida, exist_ok=True)
    resultados_path = os.path.join(args.salida, 'correlacion_multi_observatorio.json')
    
    resultados_json = {
        'correlacion': resultados,
        'coherencia': coherencia,
        'estaciones': list(datos_dict.keys()),
        'parametros': {
            'tolerancia': args.tolerancia,
            'f0': args.f0
        }
    }
    
    # Convertir numpy types
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
    
    with open(resultados_path, 'w') as f:
        json.dump(convert(resultados_json), f, indent=2)
    
    print(f"\n💾 Resultados guardados: {resultados_path}")


if __name__ == "__main__":
    main()
