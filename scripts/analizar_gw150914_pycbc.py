#!/usr/bin/env python3
"""
Análisis de GW150914 usando PyCBC
Script simplificado que carga, filtra y grafica la señal de tensión 
suavizada y blanqueada (whitened) de GW150914.

Basado en el código del problem statement, filtra la banda de frecuencias 
relevantes (aproximadamente 35 a 300 Hz) y el tiempo alrededor del evento.

Requiere:
    - pycbc >= 2.0.0
    - matplotlib >= 3.5.0

Uso:
    python scripts/analizar_gw150914_pycbc.py
    
Salida:
    - Genera una gráfica de la señal filtrada y blanqueada
    - Guarda la figura en results/figures/gw150914_pycbc_analysis.png
"""

import os
import sys

# Verificar que matplotlib está disponible
try:
    import matplotlib
    matplotlib.use('Agg')  # Backend sin GUI para entornos sin display
    import matplotlib.pyplot as plt
except ImportError:
    print("❌ Error: matplotlib no está instalado")
    print("   Instalar con: pip install matplotlib")
    sys.exit(1)

# Verificar que PyCBC está disponible
try:
    from pycbc.catalog import Merger
    from pycbc.filter import highpass_fir, lowpass_fir
    from pycbc.psd import welch, interpolate
except ImportError as e:
    print("❌ Error: PyCBC no está instalado o no se pudo importar")
    print(f"   Detalles: {e}")
    print("   Instalar con: pip install pycbc")
    print("\n⚠️  Nota: PyCBC requiere conectividad a internet para descargar datos")
    sys.exit(1)


def main():
    """Función principal que ejecuta el análisis de GW150914"""
    
    print("🌌 Análisis de GW150914 con PyCBC")
    print("=" * 50)
    
    # Crear directorio de salida si no existe
    output_dir = 'results/figures'
    os.makedirs(output_dir, exist_ok=True)
    
    # Cargar los datos del evento GW150914 para ambos detectores (H1 y L1)
    for ifo in ['H1', 'L1']:
        print(f"\n📡 Procesando detector {ifo}...")
        
        try:
            # Cargar datos del evento
            print(f"   Cargando datos de {ifo}...")
            strain = Merger("GW150914").strain(ifo)
            
            # Filtrar para eliminar frecuencias bajas y altas fuera del rango de interés
            print(f"   Aplicando filtros pasa-alto (15 Hz) y pasa-bajo (300 Hz)...")
            strain = highpass_fir(strain, 15, 8)
            strain = lowpass_fir(strain, 300, 8)
        
            # Calcular PSD (espectro de potencia del ruido)
            print(f"   Calculando PSD...")
            psd = interpolate(welch(strain), 1.0 / strain.duration)
        
            # Blanquear la señal para mejorar visibilidad del chirp
            print(f"   Blanqueando señal...")
            white_strain = (strain.to_frequencyseries() / psd**0.5).to_timeseries()
        
            # Filtrar frecuencias para centrar la señal visible de la fusión
            print(f"   Aplicando suavizado (35-300 Hz)...")
            smooth = highpass_fir(white_strain, 35, 8)
            smooth = lowpass_fir(smooth, 300, 8)
        
            # Corregir fase para L1
            if ifo == 'L1':
                print(f"   Aplicando corrección de fase para L1...")
                smooth *= -1
                smooth.roll(int(.007 / smooth.delta_t))
        
            # Graficar
            plt.plot(smooth.sample_times, smooth, label=ifo)
            print(f"   ✅ {ifo} procesado correctamente")
            
        except Exception as e:
            print(f"   ❌ Error procesando {ifo}: {e}")
            if "Connection" in str(e) or "Network" in str(e):
                print("   ⚠️  Posible problema de conectividad a GWOSC")
            raise
    
    # Configurar y guardar gráfica
    print("\n📊 Generando gráfica...")
    plt.legend()
    plt.xlim(1126259462.21, 1126259462.45)  # tiempo GPS del evento ± pequeño margen
    plt.ylim(-150, 150)
    plt.xlabel("GPS Time (s)")
    plt.ylabel("Smoothed-Whitened Strain")
    plt.title("GW150914 Gravitational Wave Signal")
    plt.grid()
    
    output_file = os.path.join(output_dir, 'gw150914_pycbc_analysis.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    
    print(f"\n✅ Análisis completado exitosamente")
    print(f"📁 Figura guardada en: {output_file}")
    print("\n🔍 La gráfica muestra:")
    print("   - Señal de tensión suavizada y blanqueada")
    print("   - Detectores H1 (Hanford) y L1 (Livingston)")
    print("   - Banda de frecuencia: 35-300 Hz")
    print("   - Tiempo alrededor del evento: GPS 1126259462.21-1126259462.45")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Análisis interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
