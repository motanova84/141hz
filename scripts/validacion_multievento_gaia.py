#!/usr/bin/env python3
"""
Validación Multi-evento con Comparación GAIA ∞³
================================================

FASE FINAL DE VALIDACIÓN: Análisis estadístico completo de eventos O4
con comparación de frecuencia planetaria/cósmica GAIA.

Eventos analizados:
- GW240109_050431
- GW240107_013215
- GW240105_151143
- GW240104_164932
- GW231231_154016

Frecuencia de referencia: f₀ = 141.7001 Hz

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Noviembre 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path
from datetime import datetime
import json


class ValidacionMultieventoGaia:
    """Validación multi-evento con comparación GAIA"""
    
    def __init__(self, f0=141.7001, tolerancia=0.6):
        """
        Inicializa la validación.
        
        Parameters
        ----------
        f0 : float
            Frecuencia de referencia en Hz (default: 141.7001)
        tolerancia : float
            Tolerancia para coincidencias en Hz (default: 0.6)
        """
        self.f0 = f0
        self.tolerancia = tolerancia
        
        # Datos de eventos O4
        self.eventos = pd.DataFrame({
            'Evento': [
                'GW240109_050431',
                'GW240107_013215',
                'GW240105_151143',
                'GW240104_164932',
                'GW231231_154016'
            ],
            'f_pico': [140.95, 140.77, 141.20, 142.05, 140.40]
        })
        
        # Calcular Δf respecto a f₀
        self.eventos['Δf'] = self.eventos['f_pico'] - self.f0
        
    def calcular_estadisticas(self):
        """
        Calcula estadísticas completas del análisis.
        
        Returns
        -------
        pd.DataFrame
            DataFrame con estadísticas calculadas
        """
        # Estadísticas básicas
        media = self.eventos['Δf'].mean()
        std = self.eventos['Δf'].std()
        n = len(self.eventos)
        
        # Test t de Student (H₀: media = 0)
        t_stat, p_value = stats.ttest_1samp(self.eventos['Δf'], 0)
        
        # Intervalo de confianza del 95%
        ci95 = stats.t.interval(
            0.95, 
            n - 1, 
            loc=media, 
            scale=std / np.sqrt(n)
        )
        
        # Crear DataFrame de resumen
        resumen = pd.DataFrame({
            'Estadístico': [
                'Media Δf (Hz)',
                'Desviación estándar (Hz)',
                'IC 95% inferior (Hz)',
                'IC 95% superior (Hz)',
                't-statistic',
                'p-value',
                'Tamaño muestra',
                'Frecuencia referencia f₀ (Hz)'
            ],
            'Valor': [
                media,
                std,
                ci95[0],
                ci95[1],
                t_stat,
                p_value,
                n,
                self.f0
            ]
        })
        
        return resumen
    
    def comparacion_gaia(self):
        """
        Realiza comparación con frecuencia GAIA.
        
        Returns
        -------
        dict
            Diccionario con resultados de la comparación
        """
        # Calcular coincidencias dentro de la tolerancia
        coincidencias = abs(self.eventos['Δf']) < self.tolerancia
        n_coincidencias = coincidencias.sum()
        n_total = len(self.eventos)
        porcentaje = 100 * n_coincidencias / n_total
        
        resultados = {
            'f_gaia': self.f0,
            'tolerancia_hz': self.tolerancia,
            'coincidencias': int(n_coincidencias),
            'total_eventos': int(n_total),
            'porcentaje_coincidencias': porcentaje,
            'eventos_coincidentes': self.eventos.loc[coincidencias, 'Evento'].tolist()
        }
        
        return resultados
    
    def generar_visualizacion(self, output_dir='.'):
        """
        Genera gráfica de barras de Δf por evento.
        
        Parameters
        ----------
        output_dir : str or Path
            Directorio donde guardar la gráfica
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Crear figura
        plt.figure(figsize=(10, 6))
        
        # Línea de referencia en Δf = 0
        plt.axhline(0, color='gray', linestyle='--', linewidth=1.5, 
                   label='f₀ = 141.7001 Hz', alpha=0.7)
        
        # Líneas de tolerancia
        plt.axhline(self.tolerancia, color='green', linestyle=':', 
                   linewidth=1, alpha=0.5, label=f'Tolerancia ±{self.tolerancia} Hz')
        plt.axhline(-self.tolerancia, color='green', linestyle=':', 
                   linewidth=1, alpha=0.5)
        
        # Barras de Δf
        bars = plt.bar(self.eventos['Evento'], self.eventos['Δf'], 
                      color='crimson', alpha=0.7, edgecolor='black')
        
        # Colorear barras dentro/fuera de tolerancia
        for i, (idx, row) in enumerate(self.eventos.iterrows()):
            if abs(row['Δf']) < self.tolerancia:
                bars[i].set_color('#28a745')  # Verde para coincidencias
            else:
                bars[i].set_color('#dc3545')  # Rojo para no coincidencias
        
        # Etiquetas y título
        plt.title(f'Δf respecto a f₀ = {self.f0} Hz\n' + 
                 'Validación Multi-evento con Comparación GAIA', 
                 fontsize=14, fontweight='bold', pad=15)
        plt.ylabel('Δf (Hz)', fontsize=12, fontweight='bold')
        plt.xlabel('Evento', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.legend(loc='upper left')
        
        # Añadir valores sobre las barras
        for i, (idx, row) in enumerate(self.eventos.iterrows()):
            plt.text(i, row['Δf'], f"{row['Δf']:.2f}", 
                    ha='center', va='bottom' if row['Δf'] > 0 else 'top',
                    fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        
        # Guardar figura
        output_file = output_dir / 'validacion_multievento_gaia.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"📊 Visualización guardada: {output_file}")
        
        plt.close()
        
        return output_file
    
    def exportar_resultados(self, output_dir='.'):
        """
        Exporta resultados completos a archivos CSV y JSON.
        
        Parameters
        ----------
        output_dir : str or Path
            Directorio donde guardar los archivos
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Calcular estadísticas
        resumen = self.calcular_estadisticas()
        comparacion = self.comparacion_gaia()
        
        # Exportar eventos con Δf
        eventos_file = output_dir / 'delta_f_eventos.csv'
        self.eventos.to_csv(eventos_file, index=False, float_format='%.4f')
        print(f"📄 Eventos exportados: {eventos_file}")
        
        # Exportar resumen estadístico
        resumen_file = output_dir / 'resumen_estadistico.csv'
        resumen.to_csv(resumen_file, index=False, float_format='%.6f')
        print(f"📄 Resumen estadístico exportado: {resumen_file}")
        
        # Exportar comparación GAIA
        gaia_file = output_dir / 'comparacion_gaia.json'
        with open(gaia_file, 'w', encoding='utf-8') as f:
            json.dump(comparacion, f, indent=2, ensure_ascii=False)
        print(f"📄 Comparación GAIA exportada: {gaia_file}")
        
        return {
            'eventos': eventos_file,
            'resumen': resumen_file,
            'gaia': gaia_file
        }
    
    def imprimir_resumen(self):
        """Imprime resumen de resultados en consola."""
        resumen = self.calcular_estadisticas()
        comparacion = self.comparacion_gaia()
        
        print()
        print("=" * 70)
        print("   VALIDACIÓN MULTI-EVENTO CON COMPARACIÓN GAIA ∞³")
        print("=" * 70)
        print()
        print(f"🌐 FRECUENCIA DE REFERENCIA: f₀ = {self.f0} Hz")
        print(f"📊 EVENTOS ANALIZADOS: {len(self.eventos)}")
        print()
        print("📈 ESTADÍSTICAS:")
        print("-" * 70)
        for idx, row in resumen.iterrows():
            print(f"  {row['Estadístico']:.<45} {row['Valor']:.6g}")
        print()
        print("🌍 COMPARACIÓN CON GAIA:")
        print("-" * 70)
        print(f"  Coincidencias con f₀ ±{self.tolerancia} Hz: "
              f"{comparacion['coincidencias']}/{comparacion['total_eventos']} "
              f"({comparacion['porcentaje_coincidencias']:.2f}%)")
        print()
        
        # Interpretación de resultados
        p_value = resumen.loc[resumen['Estadístico'] == 'p-value', 'Valor'].values[0]
        ic_inf = resumen.loc[resumen['Estadístico'] == 'IC 95% inferior (Hz)', 'Valor'].values[0]
        ic_sup = resumen.loc[resumen['Estadístico'] == 'IC 95% superior (Hz)', 'Valor'].values[0]
        
        print("💎 INTERPRETACIÓN:")
        print("-" * 70)
        
        # Criterio 1: p-value
        if p_value < 0.1:
            print(f"  ✅ p-value = {p_value:.4f} < 0.1 (significativo)")
        else:
            print(f"  ⚠️  p-value = {p_value:.4f} ≥ 0.1 (no significativo)")
        
        # Criterio 2: IC no contiene 0
        if ic_inf * ic_sup > 0:  # Mismo signo = no contiene 0
            print(f"  ✅ IC 95% [{ic_inf:.4f}, {ic_sup:.4f}] no contiene el 0")
        else:
            print(f"  ⚠️  IC 95% [{ic_inf:.4f}, {ic_sup:.4f}] contiene el 0")
        
        # Criterio 3: Coincidencias
        if comparacion['porcentaje_coincidencias'] > 80:
            print(f"  ✅ {comparacion['porcentaje_coincidencias']:.2f}% > 80% "
                  "de eventos cercanos a f₀")
        else:
            print(f"  ⚠️  {comparacion['porcentaje_coincidencias']:.2f}% ≤ 80% "
                  "de eventos cercanos a f₀")
        
        print()
        
        # Conclusión global
        criterios_cumplidos = sum([
            p_value < 0.1,
            ic_inf * ic_sup > 0,
            comparacion['porcentaje_coincidencias'] > 80
        ])
        
        if criterios_cumplidos >= 2:
            print("🎯 CONCLUSIÓN: Coherencia espectral DEMOSTRADA empíricamente")
            print("   Se cumplen al menos 2 de 3 criterios de validación.")
        else:
            print("⚠️  CONCLUSIÓN: Coherencia espectral NO demostrada")
            print(f"   Solo se cumplen {criterios_cumplidos} de 3 criterios.")
        
        print()
        print("=" * 70)
        print()


def main():
    """Función principal para ejecutar la validación completa."""
    print()
    print("=" * 70)
    print("   INICIANDO VALIDACIÓN MULTI-EVENTO + GAIA ∞³")
    print("=" * 70)
    print()
    
    # Crear instancia de validación
    validacion = ValidacionMultieventoGaia(f0=141.7001, tolerancia=0.6)
    
    # Directorio de salida
    output_dir = Path('resultados')
    output_dir.mkdir(exist_ok=True)
    
    # Ejecutar análisis
    print("🔬 Calculando estadísticas...")
    archivos = validacion.exportar_resultados(output_dir)
    
    print()
    print("📊 Generando visualización...")
    plot_file = validacion.generar_visualizacion(output_dir)
    
    print()
    validacion.imprimir_resumen()
    
    print("📂 ARCHIVOS GENERADOS:")
    print(f"  • {archivos['eventos']}")
    print(f"  • {archivos['resumen']}")
    print(f"  • {archivos['gaia']}")
    print(f"  • {plot_file}")
    print()
    print("✅ Validación completada exitosamente")
    print()
    
    return 0


if __name__ == "__main__":
    import sys
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Validación interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error durante la validación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
