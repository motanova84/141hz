#!/usr/bin/env python3
"""
Ejemplo de Uso en Google Colab - Validación Multi-evento + GAIA
================================================================

Este script proporciona un ejemplo de cómo ejecutar el análisis
de validación multi-evento con comparación GAIA en Google Colab.

Para usar en Colab, copia y pega el contenido en una celda y ejecuta.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Noviembre 2025
"""

# ============================================================================
# PASO 1: INSTALACIÓN DE DEPENDENCIAS (ejecutar en Colab)
# ============================================================================

def install_dependencies():
    """Instala las dependencias necesarias en Colab"""
    print("📦 Instalando dependencias...")
    import subprocess
    import sys
    
    packages = ['numpy', 'pandas', 'matplotlib', 'scipy']
    for package in packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', package])
    
    print("✅ Dependencias instaladas correctamente")


# ============================================================================
# PASO 2: DEFINICIÓN DE DATOS Y ANÁLISIS
# ============================================================================

def colab_validation_example():
    """
    Ejemplo completo de validación multi-evento que puede ejecutarse en Colab.
    """
    # Importar librerías
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy import stats
    
    print()
    print("=" * 70)
    print("   VALIDACIÓN MULTI-EVENTO + COMPARACIÓN GAIA ∞³")
    print("=" * 70)
    print()
    
    # ========================================================================
    # PASO 3: DATOS MULTIEVENTO - GWTC-3 + O4
    # ========================================================================
    
    print("📂 Cargando datos de eventos...")
    
    # Datos de los 5 eventos O4
    eventos = pd.DataFrame({
        'Evento': [
            'GW240109_050431', 'GW240107_013215', 'GW240105_151143',
            'GW240104_164932', 'GW231231_154016'
        ],
        'f_pico': [140.95, 140.77, 141.20, 142.05, 140.40]
    })
    
    # Frecuencia de referencia
    f0 = 141.7001
    
    # Calcular desviaciones
    eventos['Δf'] = eventos['f_pico'] - f0
    
    print("✅ Datos cargados:")
    print(eventos)
    print()
    
    # ========================================================================
    # PASO 4: ANÁLISIS ESTADÍSTICO
    # ========================================================================
    
    print("📊 Realizando análisis estadístico...")
    
    # Estadísticas básicas
    media = eventos['Δf'].mean()
    std = eventos['Δf'].std()
    n = len(eventos)
    
    # Test t de Student
    t_stat, p_value = stats.ttest_1samp(eventos['Δf'], 0)
    
    # Intervalo de confianza 95%
    ci95 = stats.t.interval(0.95, n-1, loc=media, scale=std/np.sqrt(n))
    
    # Crear DataFrame de resumen
    resumen = pd.DataFrame({
        'Estadístico': [
            'Media Δf', 'Desviación estándar', 'IC 95% inferior', 
            'IC 95% superior', 't-stat', 'p-value'
        ],
        'Valor': [media, std, ci95[0], ci95[1], t_stat, p_value]
    })
    
    print("✅ Estadísticas calculadas:")
    print(resumen)
    print()
    
    # ========================================================================
    # PASO 5: GRÁFICAS COMPLETAS
    # ========================================================================
    
    print("📈 Generando visualización...")
    
    plt.figure(figsize=(10, 6))
    
    # Línea de referencia
    plt.axhline(0, color='gray', linestyle='--', linewidth=1.5, label='f₀ = 141.7001 Hz')
    
    # Barras de Δf
    colors = ['#28a745' if abs(df) < 0.6 else '#dc3545' for df in eventos['Δf']]
    bars = plt.bar(eventos['Evento'], eventos['Δf'], color=colors, alpha=0.7, edgecolor='black')
    
    # Configuración
    plt.title(f'Δf respecto a f₀ = {f0} Hz\nValidación Multi-evento con Comparación GAIA', 
             fontsize=14, fontweight='bold')
    plt.ylabel('Δf (Hz)', fontsize=12, fontweight='bold')
    plt.xlabel('Evento', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    plt.legend()
    
    # Añadir valores
    for i, (idx, row) in enumerate(eventos.iterrows()):
        plt.text(i, row['Δf'], f"{row['Δf']:.2f}", 
                ha='center', va='bottom' if row['Δf'] > 0 else 'top',
                fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Visualización generada")
    print()
    
    # ========================================================================
    # PASO 6: COMPARACIÓN CON GAIA / FRECUENCIA PLANETARIA
    # ========================================================================
    
    print("🌍 Comparando con frecuencia GAIA...")
    
    f_gaia = 141.7001
    tolerancia = 0.6
    coincidencias = abs(eventos['Δf']) < tolerancia
    porcentaje = 100 * coincidencias.sum() / len(eventos)
    
    print(f"✅ Coincidencias con f₀ ±{tolerancia} Hz: {porcentaje:.2f}%")
    print(f"   Eventos coincidentes: {coincidencias.sum()}/{len(eventos)}")
    print()
    
    # ========================================================================
    # PASO 7: EXPORTAR RESULTADOS (opcional en Colab)
    # ========================================================================
    
    print("💾 Exportando resultados...")
    
    # En Colab, los archivos se guardan en el sistema de archivos temporal
    eventos.to_csv("delta_f_eventos.csv", index=False)
    resumen.to_csv("resumen_estadistico.csv", index=False)
    
    print("✅ Archivos exportados:")
    print("   • delta_f_eventos.csv")
    print("   • resumen_estadistico.csv")
    print()
    
    # ========================================================================
    # CONCLUSIÓN
    # ========================================================================
    
    print("=" * 70)
    print("   💎 CONCLUSIÓN")
    print("=" * 70)
    print()
    
    # Evaluar criterios
    criterio1 = p_value < 0.1
    criterio2 = ci95[0] * ci95[1] > 0  # IC no contiene 0
    criterio3 = porcentaje > 80
    
    print("Criterios de validación:")
    print(f"  {'✅' if criterio1 else '⚠️ '} p-value < 0.1: {p_value:.4f}")
    print(f"  {'✅' if criterio2 else '⚠️ '} IC 95% no contiene 0: [{ci95[0]:.4f}, {ci95[1]:.4f}]")
    print(f"  {'✅' if criterio3 else '⚠️ '} >80% eventos cercanos a f₀: {porcentaje:.2f}%")
    print()
    
    criterios_cumplidos = sum([criterio1, criterio2, criterio3])
    
    if criterios_cumplidos >= 2:
        print("🎯 Coherencia espectral DEMOSTRADA empíricamente")
        print("   (2 o más criterios cumplidos)")
    else:
        print("⚠️  Coherencia espectral NO demostrada")
        print(f"   (Solo {criterios_cumplidos} de 3 criterios cumplidos)")
    
    print()
    print("=" * 70)
    print()
    
    return eventos, resumen


# ============================================================================
# EJECUCIÓN EN COLAB
# ============================================================================

def main():
    """Función principal para ejecutar en Colab"""
    print()
    print("🌐 VALIDACIÓN MULTI-EVENTO + GAIA en Google Colab")
    print()
    
    # Instalar dependencias (descomenta si es la primera vez)
    # install_dependencies()
    
    # Ejecutar validación
    eventos, resumen = colab_validation_example()
    
    print("✅ Análisis completado exitosamente")
    print()
    print("📝 NOTAS:")
    print("   - Los archivos CSV están disponibles en el entorno de Colab")
    print("   - Puedes descargarlos usando el menú lateral de archivos")
    print("   - Para más detalles, visita el repositorio: github.com/motanova84/141hz")
    print()
    
    return 0


if __name__ == "__main__":
    import sys
    
    # Descomenta la siguiente línea para instalar dependencias en Colab
    # install_dependencies()
    
    sys.exit(main())


# ============================================================================
# INSTRUCCIONES PARA GOOGLE COLAB
# ============================================================================
"""
Para ejecutar este análisis en Google Colab:

1. Abre un nuevo notebook en https://colab.research.google.com/

2. Copia este script completo en una celda

3. Ejecuta la celda (Shift+Enter)

4. Los resultados se mostrarán en la salida, incluyendo:
   - Tabla de eventos con Δf
   - Estadísticas completas
   - Gráfico de barras
   - Evaluación de criterios
   - Archivos CSV exportados

ALTERNATIVA - Ejecutar paso a paso:

Puedes copiar cada sección (PASO 1, PASO 2, etc.) en celdas separadas
para ejecutar el análisis paso a paso y ver resultados intermedios.

DESCARGAR RESULTADOS:

Los archivos CSV se guardan en el sistema de archivos temporal de Colab.
Para descargarlos:

    from google.colab import files
    files.download('delta_f_eventos.csv')
    files.download('resumen_estadistico.csv')

REPOSITORIO COMPLETO:

Para acceder al código completo con más análisis y validaciones:
https://github.com/motanova84/141hz

DOCUMENTACIÓN:

Ver VALIDACION_MULTIEVENTO_GAIA.md para documentación completa.
"""
