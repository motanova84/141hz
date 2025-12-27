#!/usr/bin/env python3
"""
Análisis de 141.7 Hz en KAGRA (K1) - O4 Open Data
Analiza un segmento de datos públicos de KAGRA para detectar la señal de 141.7 Hz

GPS: 1370294440 – 1370294472 (32 s)
Fecha: 2023-06-16
Detector: K1 (KAGRA)

Incluye funciones para buscar datos disponibles y manejar casos donde no hay datos
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries
from gwosc import datasets
import argparse
import traceback
from datetime import datetime

def analyze_kagra_141hz():
    """
    Analiza datos de KAGRA para detectar señal en 141.7 Hz
    
    Returns:
        dict: Resultados del análisis incluyendo SNR, frecuencia detectada, etc.
    """
    # Configuración
    start = 1370294440
    end = 1370294472
    target_band = [141.4, 142.0]
    target_freq = 141.7
    
    print("🔍 Test de 141.7 Hz en KAGRA (K1)")
    print("=" * 60)
    print(f"GPS Time: {start} - {end} (32 segundos)")
    print(f"Fecha: 2023-06-16")
    print(f"Banda objetivo: {target_band[0]} - {target_band[1]} Hz")
    print(f"Frecuencia objetivo: {target_freq} Hz")
    print()
    
    # Descargar datos de KAGRA
    print("⏳ Descargando datos de KAGRA...")
    try:
        k1 = TimeSeries.fetch_open_data('K1', start, end, cache=True)
        print("✅ Datos recibidos.")
        print(f"   Duración: {k1.duration.value:.2f} s")
        print(f"   Tasa de muestreo: {k1.sample_rate.value:.0f} Hz")
    except Exception as e:
        print(f"❌ Error descargando datos: {e}")
        return None
    
    # Procesamiento - aplicar filtro de banda
    print(f"\n🔧 Aplicando filtro de banda {target_band[0]}-{target_band[1]} Hz...")
    k1_band = k1.bandpass(*target_band)
    
    # Calcular SNR
    max_amplitude = np.max(np.abs(k1_band.value))
    std_deviation = np.std(k1_band.value)
    snr_k1 = max_amplitude / std_deviation
    
    print(f"\n📊 SNR KAGRA @141.7 Hz = {snr_k1:.2f}")
    
    # Interpretación del resultado
    print("\n📈 INTERPRETACIÓN:")
    if snr_k1 > 5.0:
        print("   ✅ SNR > 5.0: Posible señal coherente también en KAGRA")
        interpretation = "coherent_signal"
    elif snr_k1 >= 2.0:
        print("   ⚠️  SNR 2-4.9: Marginal – investigar más")
        interpretation = "marginal"
    else:
        print("   ❌ SNR < 2.0: No aparece – no universal")
        interpretation = "no_signal"
    
    # Crear directorio de resultados
    output_dir = '../results/figures'
    os.makedirs(output_dir, exist_ok=True)
    
    # Visualización
    print("\n📊 Generando visualización...")
    plt.figure(figsize=(10, 4))
    k1_band.plot()
    plt.axhline(std_deviation, color='red', linestyle='--', 
                label=f'1σ = {std_deviation:.2e}', linewidth=2)
    plt.axhline(-std_deviation, color='red', linestyle='--', linewidth=2)
    plt.title(f"KAGRA – Señal filtrada en 141.7 Hz (SNR = {snr_k1:.2f})", 
              fontsize=14, fontweight='bold')
    plt.xlabel('Tiempo (GPS)', fontsize=12)
    plt.ylabel('Amplitud (strain)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_file = f'{output_dir}/kagra_k1_141hz_analysis.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"💾 Visualización guardada en: {output_file}")
    
    # Guardar resultados numéricos
    results_file = f'{output_dir}/kagra_k1_141hz_results.txt'
    with open(results_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("RESULTADOS: Análisis de 141.7 Hz en KAGRA (K1)\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Detector: K1 (KAGRA)\n")
        f.write(f"GPS Time: {start} - {end}\n")
        f.write(f"Fecha: 2023-06-16\n")
        f.write(f"Duración: {k1.duration.value:.2f} s\n")
        f.write(f"Tasa de muestreo: {k1.sample_rate.value:.0f} Hz\n\n")
        f.write(f"Banda analizada: {target_band[0]} - {target_band[1]} Hz\n")
        f.write(f"Frecuencia objetivo: {target_freq} Hz\n\n")
        f.write(f"SNR calculado: {snr_k1:.2f}\n")
        f.write(f"Amplitud máxima: {max_amplitude:.2e}\n")
        f.write(f"Desviación estándar (1σ): {std_deviation:.2e}\n\n")
        f.write("Interpretación:\n")
        if interpretation == "coherent_signal":
            f.write("  ✅ SNR > 5.0: Posible señal coherente también en KAGRA\n")
        elif interpretation == "marginal":
            f.write("  ⚠️  SNR 2-4.9: Marginal – investigar más\n")
        else:
            f.write("  ❌ SNR < 2.0: No aparece – no universal\n")
    
    print(f"💾 Resultados guardados en: {results_file}")
    
    # Retornar resultados
    results = {
        'detector': 'K1',
        'gps_start': start,
        'gps_end': end,
        'date': '2023-06-16',
        'duration': k1.duration.value,
        'sample_rate': k1.sample_rate.value,
        'target_freq': target_freq,
        'target_band': target_band,
        'snr': snr_k1,
        'max_amplitude': max_amplitude,
        'std_deviation': std_deviation,
        'interpretation': interpretation,
        'output_file': output_file,
        'results_file': results_file
    }
    
    print("\n" + "=" * 60)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 60)
    
    return results


def buscar_datos_kagra_disponibles(run='O4'):
    """
    Escanear GWOSC por segmentos O4 publicados de KAGRA
    
    Args:
        run: Run de observación ('O3', 'O4', etc.)
    
    Returns:
        list: Lista de eventos disponibles con KAGRA, o None si no hay
    """
    print(f"\n🔍 Buscando datos de KAGRA en run {run}...")
    print("="*60)
    
    try:
        # Buscar eventos con KAGRA
        eventos = datasets.find_datasets(type='event', detector='K1')
        
        if not eventos or len(eventos) == 0:
            print("⚠️  KAGRA: Sin datos públicos aún en GWOSC")
            print(f"   Run {run} comenzó pero datos aún no liberados")
            print("   Típicamente los datos se liberan 18 meses después")
            print()
            print("📋 Creando documentación de espera...")
            crear_kagra_placeholder(run)
            return None
        
        print(f"✅ Encontrados {len(eventos)} eventos con KAGRA")
        for evento in eventos[:5]:  # Mostrar primeros 5
            print(f"   - {evento}")
        
        if len(eventos) > 5:
            print(f"   ... y {len(eventos) - 5} más")
        
        return eventos
        
    except Exception as e:
        print(f"❌ Error buscando datos: {e}")
        print("   Probablemente los datos de KAGRA O4 no están disponibles aún")
        crear_kagra_placeholder(run)
        return None


def crear_kagra_placeholder(run='O4'):
    """
    Documentar por qué KAGRA es importante y qué esperamos
    
    Args:
        run: Run de observación
    """
    # Usar path absoluto desde el script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    output_dir = os.path.join(repo_root, 'docs')
    os.makedirs(output_dir, exist_ok=True)
    
    placeholder_file = os.path.join(output_dir, f'KAGRA_{run}_WAITLIST.md')
    
    doc = f"""# KAGRA K1: Validación Pendiente - Run {run}

## 🎯 Por qué KAGRA es importante

KAGRA (K1) es crucial para validar si 141.7 Hz es una frecuencia física universal o un artefacto instrumental:

### 1. Detector Independiente
- **Ubicación:** Japón (Kamioka)
- **Operador:** Instituto Nacional de Ciencias Naturales de Japón
- **Diseño completamente independiente de LIGO**

### 2. Diseño Único
- **Subterráneo:** 200 metros bajo tierra (reducción de ruido sísmico)
- **Criogénico:** Espejos enfriados a 20K (reducción de ruido térmico)
- **Geometría diferente:** Brazos de 3 km (vs. 4 km de LIGO)

### 3. Orientación Única
- **Geometría del detector:** Diferente a H1/L1
- **Respuesta angular:** Complementaria a LIGO
- **Ubicación geográfica:** Red global de detección

## 🔬 Predicción Científica

Si 141.7 Hz es una frecuencia física universal (como predice Ψ = I × A²_eff):
- ✅ **DEBE aparecer en KAGRA K1** en eventos de fusión BBH
- ✅ **DEBE tener coherencia con H1/L1** cuando detecta simultáneamente
- ✅ **DEBE mostrar el mismo patrón de ringdown**

Si 141.7 Hz es un artefacto instrumental de LIGO:
- ❌ **NO aparecerá en KAGRA K1**
- ❌ **NO habrá coherencia con H1/L1**
- ❌ **Diferentes patrones de ruido instrumental**

## 📊 Estado Actual: Run {run}

### Información del Run
- **Run {run} comenzó:** Abril 2023 (aprox.)
- **Estado:** En curso / Recientemente finalizado
- **Datos públicos:** TBD (típicamente 18 meses después del run)

### Política de Datos LIGO/Virgo/KAGRA
GWOSC (Gravitational Wave Open Science Center) libera datos en fases:
1. **Eventos significativos:** ~6 meses después de detección
2. **Catálogo completo:** ~18 meses después del run
3. **Datos de strain continuos:** Progresivamente

### Próximos Pasos
Cuando los datos estén disponibles:

```bash
# Analizar segmento específico
python scripts/analizar_kagra_k1.py --run {run} --segment START-END

# Buscar automáticamente datos disponibles
python scripts/analizar_kagra_k1.py --search-available --run {run}
```

## 🌐 Análisis Comparativo Mientras Tanto

Mientras esperamos datos de KAGRA {run}, podemos:

### 1. Análisis de Sensibilidad
Comparar sensibilidad teórica LIGO vs. KAGRA en 141.7 Hz:
```bash
python scripts/comparar_ligo_vs_kagra_sensibilidad.py
```

### 2. Análisis de Runs Previos
Si hay datos de runs anteriores (O3), analizarlos:
```bash
python scripts/analizar_kagra_k1.py --run O3
```

### 3. Simulaciones
Simular respuesta esperada de KAGRA a señales con 141.7 Hz:
```bash
python scripts/simular_respuesta_kagra_141hz.py
```

## 📚 Referencias

### Diseño de KAGRA
- KAGRA Collaboration, "KAGRA: 2.5 generation interferometric gravitational wave detector"
- Nature Astronomy 3, 35-40 (2019)

### Sensibilidad y Ruido
- KAGRA Collaboration, "Overview of KAGRA: Detector design and construction history"
- arXiv:2005.05574

### Datos Abiertos
- GWOSC: https://gwosc.org
- KAGRA Data Release: https://gwcenter.icrr.u-tokyo.ac.jp/en/

## 🔔 Notificaciones

Para recibir notificaciones cuando los datos estén disponibles:
1. Suscribirse a GWOSC announcements: https://gwosc.org/news/
2. Seguir @KAGRA_PR en Twitter/X
3. Revisar periódicamente: https://gwosc.org/eventapi/

---

**Última actualización:** {get_timestamp()}
**Estado:** ESPERANDO DATOS {run}
**Importancia:** CRÍTICA para validación independiente
"""
    
    with open(placeholder_file, 'w', encoding='utf-8') as f:
        f.write(doc)
    
    print(f"📄 Documentación creada: {placeholder_file}")
    print()
    print("💡 RESUMEN:")
    print(f"   - KAGRA {run}: Datos no disponibles aún")
    print("   - Importancia: Validación independiente crucial")
    print("   - Predicción: 141.7 Hz DEBE aparecer si es universal")
    print(f"   - Acción: Esperar liberación de datos (~18 meses post-run)")
    print()


def get_timestamp():
    """Obtener timestamp actual formateado"""
    return datetime.now().strftime('%Y-%m-%d %H:%M UTC')


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Análisis de 141.7 Hz en KAGRA K1"
    )
    parser.add_argument(
        '--search-available',
        action='store_true',
        help='Buscar automáticamente datos disponibles de KAGRA'
    )
    parser.add_argument(
        '--run',
        type=str,
        default='O4',
        help='Run de observación (O3, O4, etc.)'
    )
    parser.add_argument(
        '--segment',
        type=str,
        help='Segmento GPS específico (formato: START-END)'
    )
    
    args = parser.parse_args()
    
    print("\n🌌 ANÁLISIS KAGRA - Búsqueda de 141.7 Hz en O4 Data")
    print()
    
    # Si se solicita búsqueda automática
    if args.search_available:
        eventos = buscar_datos_kagra_disponibles(args.run)
        if eventos is None:
            print("\n⏳ Esperando liberación de datos...")
            return 1
        else:
            print(f"\n✅ Datos disponibles. Use uno de los eventos encontrados.")
            return 0
    
    # Análisis normal
    try:
        results = analyze_kagra_141hz()
        
        if results is None:
            print("\n❌ Error: No se pudo completar el análisis")
            return 1
        
        print(f"\n📋 RESUMEN:")
        print(f"   Detector: {results['detector']}")
        print(f"   SNR: {results['snr']:.2f}")
        print(f"   Interpretación: {results['interpretation']}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error en el análisis: {e}")
        traceback.print_exc()
        
        # Si falla, probablemente datos no disponibles
        print("\n💡 Intentando verificar disponibilidad de datos...")
        buscar_datos_kagra_disponibles(args.run)
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
