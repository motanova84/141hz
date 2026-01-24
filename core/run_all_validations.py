#!/usr/bin/env python3
"""
Master script para ejecutar las tres validaciones LISA-DESI-IGETS.

Este script ejecuta secuencialmente:
1. LISA - Búsqueda de armónicos en ondas gravitacionales
2. DESI - Análisis cosmológico de w(z)
3. IGETS - Detección de modulación Yukawa en gravimetría

Genera un reporte integrado de los tres análisis.
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Añadir directorios al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lisa'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'desi'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'igets'))


def print_header(title):
    """Imprime encabezado formateado."""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80 + "\n")


def run_lisa():
    """Ejecuta análisis LISA."""
    print_header("🔭 LISA - Laser Interferometer Space Antenna")
    
    try:
        from lisa_search_pipeline import LISASearchPipeline
        
        pipeline = LISASearchPipeline(
            sample_rate=10.0,
            duration=86400.0
        )
        
        results = pipeline.run_targeted_search(
            n_harmonics=10,
            save_results=True,
            output_dir="lisa/lisa_results"
        )
        
        pipeline.plot_results(results, output_dir="lisa/lisa_results")
        
        return {
            'status': 'success',
            'results': results
        }
        
    except Exception as e:
        print(f"❌ Error en LISA: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }


def run_desi():
    """Ejecuta análisis DESI."""
    print_header("🌌 DESI - Dark Energy Spectroscopic Instrument")
    
    try:
        from desi_wz_analysis import DESICosmologyAnalysis
        
        analysis = DESICosmologyAnalysis()
        
        results = analysis.run_analysis(
            use_mock_data=True,
            save_results=True,
            output_dir="desi/desi_results"
        )
        
        analysis.plot_results(results, output_dir="desi/desi_results")
        
        return {
            'status': 'success',
            'results': results
        }
        
    except Exception as e:
        print(f"❌ Error en DESI: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }


def run_igets():
    """Ejecuta análisis IGETS."""
    print_header("🌍 IGETS - International Geodynamics and Earth Tide Service")
    
    try:
        from igets_fft_analysis import IGETSGravimetryAnalysis
        
        analysis = IGETSGravimetryAnalysis(sample_rate=1000.0)
        
        results = analysis.run_analysis(
            n_stations=3,
            duration=3600.0,
            include_modulation=True,
            save_results=True,
            output_dir="igets/igets_results"
        )
        
        analysis.plot_results(results, output_dir="igets/igets_results")
        
        return {
            'status': 'success',
            'results': results
        }
        
    except Exception as e:
        print(f"❌ Error en IGETS: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }


def generate_integrated_report(lisa_result, desi_result, igets_result):
    """Genera reporte integrado de los tres análisis."""
    print_header("📊 REPORTE INTEGRADO - LISA-DESI-IGETS")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'lisa': {},
        'desi': {},
        'igets': {},
        'overall_assessment': {}
    }
    
    # LISA
    if lisa_result['status'] == 'success':
        results = lisa_result['results']
        n_significant = sum(1 for d in results['detections'] if d['significant'])
        n_total = len(results['harmonics'])
        
        report['lisa'] = {
            'status': 'success',
            'harmonics_detected': n_significant,
            'harmonics_total': n_total,
            'detection_rate': n_significant / n_total if n_total > 0 else 0,
            'conclusion': 'DETECTADO' if n_significant >= 2 else 'NO DETECTADO'
        }
        
        print(f"🔭 LISA:")
        print(f"  Armónicos detectados: {n_significant}/{n_total}")
        print(f"  Conclusión: {report['lisa']['conclusion']}")
    else:
        report['lisa'] = {'status': 'error', 'error': lisa_result['error']}
        print(f"🔭 LISA: ERROR - {lisa_result['error']}")
    
    # DESI
    if desi_result['status'] == 'success':
        results = desi_result['results']
        tension = results['tension']
        
        report['desi'] = {
            'status': 'success',
            'w0_fit': results['fit']['w0'],
            'wa_fit': results['fit']['wa'],
            'delta_w_mean': tension['delta_w_mean'],
            'compatible_with_gqn': tension['compatible_with_gqn'],
            'conclusion': 'COMPATIBLE' if tension['compatible_with_gqn'] else 'INCOMPATIBLE'
        }
        
        print(f"\n🌌 DESI:")
        print(f"  w₀ = {results['fit']['w0']:.3f}")
        print(f"  wₐ = {results['fit']['wa']:.3f}")
        print(f"  |Δw| = {tension['delta_w_mean']:.4f}")
        print(f"  Conclusión: {report['desi']['conclusion']}")
    else:
        report['desi'] = {'status': 'error', 'error': desi_result['error']}
        print(f"\n🌌 DESI: ERROR - {desi_result['error']}")
    
    # IGETS
    if igets_result['status'] == 'success':
        results = igets_result['results']
        
        n_stations = len(results['stations'])
        n_detected = sum(1 for s in results['stations'].values()
                        if s['analysis']['detection'] and 
                        s['analysis']['detection']['significant'])
        
        coherence = results['coherence']['global_coherence']
        highly_coherent = results['coherence']['highly_coherent']
        
        detected = n_detected >= 2 and highly_coherent
        
        report['igets'] = {
            'status': 'success',
            'stations_detected': n_detected,
            'stations_total': n_stations,
            'global_coherence': coherence,
            'highly_coherent': highly_coherent,
            'conclusion': 'DETECTADO' if detected else 'NO DETECTADO'
        }
        
        print(f"\n🌍 IGETS:")
        print(f"  Estaciones con detección: {n_detected}/{n_stations}")
        print(f"  Coherencia global: {coherence:.3f}")
        print(f"  Conclusión: {report['igets']['conclusion']}")
    else:
        report['igets'] = {'status': 'error', 'error': igets_result['error']}
        print(f"\n🌍 IGETS: ERROR - {igets_result['error']}")
    
    # Evaluación global
    successes = sum(1 for r in [lisa_result, desi_result, igets_result] 
                   if r['status'] == 'success')
    
    confirmations = 0
    if report['lisa'].get('conclusion') == 'DETECTADO':
        confirmations += 1
    if report['desi'].get('conclusion') == 'COMPATIBLE':
        confirmations += 1
    if report['igets'].get('conclusion') == 'DETECTADO':
        confirmations += 1
    
    print("\n" + "=" * 80)
    print("EVALUACIÓN GLOBAL DEL MODELO GQN")
    print("=" * 80)
    print(f"\nAnálisis exitosos: {successes}/3")
    print(f"Confirmaciones: {confirmations}/3")
    
    if confirmations == 3:
        assessment = "FUERTE EVIDENCIA A FAVOR"
        emoji = "✅✅✅"
    elif confirmations == 2:
        assessment = "EVIDENCIA MODERADA A FAVOR"
        emoji = "✅✅"
    elif confirmations == 1:
        assessment = "EVIDENCIA DÉBIL / MIXTA"
        emoji = "✅"
    else:
        assessment = "MODELO FALSADO"
        emoji = "❌"
    
    report['overall_assessment'] = {
        'successful_analyses': successes,
        'confirmations': confirmations,
        'assessment': assessment
    }
    
    print(f"\n{emoji} {assessment}")
    
    # Guardar reporte
    output_dir = Path("integrated_results")
    output_dir.mkdir(exist_ok=True)
    
    report_file = output_dir / f"integrated_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📁 Reporte integrado guardado en: {report_file}")
    
    return report


def main():
    """Función principal."""
    print_header("🚀 LISA-DESI-IGETS Validation Pipeline")
    print("Ejecutando tres vías de validación del modelo GQN...")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ejecutar análisis
    lisa_result = run_lisa()
    desi_result = run_desi()
    igets_result = run_igets()
    
    # Generar reporte integrado
    report = generate_integrated_report(lisa_result, desi_result, igets_result)
    
    print("\n" + "=" * 80)
    print("✓ Pipeline completado exitosamente")
    print("=" * 80)
    print("\nResultados guardados en:")
    print("  - lisa/lisa_results/")
    print("  - desi/desi_results/")
    print("  - igets/igets_results/")
    print("  - integrated_results/")
    print("\nPara más información, consulta LISA_DESI_IGETS_INTEGRATION.md")


if __name__ == "__main__":
    main()
