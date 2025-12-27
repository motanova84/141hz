#!/usr/bin/env python3
"""
Script para validar resultados del análisis de ringdown.
Verifica que la frecuencia detectada esté dentro del rango esperado
y que el SNR sea suficiente.
"""
import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser(description='Validar resultados del análisis de ringdown')
    parser.add_argument('--freq', type=float, default=141.7, help='Frecuencia objetivo (Hz)')
    parser.add_argument('--tol', type=float, default=0.5, help='Tolerancia de frecuencia (Hz)')
    parser.add_argument('--snr-min', type=float, default=5.0, help='SNR mínimo requerido')
    parser.add_argument('--results-file', type=str, default=None, help='Archivo de resultados JSON (opcional)')
    args = parser.parse_args()
    
    # Obtener las rutas del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    results_dir = os.path.join(project_dir, 'results')
    
    # Si no se especificó archivo de resultados, buscar el más reciente
    if args.results_file is None:
        # Buscar archivos de resultados en el directorio results
        result_files = []
        if os.path.exists(results_dir):
            for filename in os.listdir(results_dir):
                if filename.startswith('ringdown_results_') and filename.endswith('.json'):
                    result_files.append(os.path.join(results_dir, filename))
        
        if not result_files:
            print("❌ ERROR: No se encontraron archivos de resultados")
            print(f"Buscado en: {results_dir}")
            sys.exit(1)
        
        # Usar el archivo más reciente
        args.results_file = max(result_files, key=os.path.getmtime)
        print(f"Usando archivo de resultados: {args.results_file}")
    
    # Cargar resultados
    try:
        with open(args.results_file, 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: Archivo de resultados no encontrado: {args.results_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ ERROR: El archivo de resultados no es JSON válido: {args.results_file}")
        sys.exit(1)
    
    # Extraer valores
    detected_freq = results.get('frequency', 0.0)
    detected_snr = results.get('snr', 0.0)
    detector = results.get('detector', 'Unknown')
    event = results.get('event', 'Unknown')
    
    print(f"\n{'='*60}")
    print(f"VALIDACIÓN DE RESULTADOS - {detector} {event}")
    print(f"{'='*60}\n")
    
    print(f"Parámetros de validación:")
    print(f"  - Frecuencia objetivo: {args.freq} Hz")
    print(f"  - Tolerancia: ±{args.tol} Hz")
    print(f"  - Rango aceptable: [{args.freq - args.tol}, {args.freq + args.tol}] Hz")
    print(f"  - SNR mínimo: {args.snr_min}")
    print()
    
    print(f"Resultados detectados:")
    print(f"  - Frecuencia detectada: {detected_freq:.2f} Hz")
    print(f"  - SNR detectado: {detected_snr:.2f}")
    print()
    
    # Validar frecuencia
    freq_diff = abs(detected_freq - args.freq)
    freq_valid = freq_diff <= args.tol
    
    # Validar SNR
    snr_valid = detected_snr >= args.snr_min
    
    # Mostrar resultados
    print("Resultados de validación:")
    print(f"  {'✅' if freq_valid else '❌'} Frecuencia: {detected_freq:.2f} Hz (diferencia: {freq_diff:.2f} Hz)")
    print(f"  {'✅' if snr_valid else '❌'} SNR: {detected_snr:.2f} (mínimo: {args.snr_min})")
    print()
    
    # Veredicto final
    all_valid = freq_valid and snr_valid
    
    if all_valid:
        print(f"{'='*60}")
        print("✅ VALIDACIÓN EXITOSA: Todos los criterios fueron cumplidos")
        print(f"{'='*60}\n")
        sys.exit(0)
    else:
        print(f"{'='*60}")
        print("❌ VALIDACIÓN FALLIDA: Algunos criterios no fueron cumplidos")
        print(f"{'='*60}\n")
        
        if not freq_valid:
            print(f"⚠️  La frecuencia detectada ({detected_freq:.2f} Hz) está fuera del rango")
            print(f"   aceptable [{args.freq - args.tol}, {args.freq + args.tol}] Hz")
        
        if not snr_valid:
            print(f"⚠️  El SNR detectado ({detected_snr:.2f}) es menor al mínimo ({args.snr_min})")
        
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
