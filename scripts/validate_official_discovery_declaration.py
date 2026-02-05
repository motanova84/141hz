#!/usr/bin/env python3
"""
Validación de la Declaración Oficial de Descubrimiento Empírico
================================================================

Script para verificar los claims principales de la declaración oficial:
- Detección en 11/11 eventos GWTC-1 (100%)
- SNR medio > 5σ
- Banda de análisis 140.7-142.7 Hz
- Separación de líneas instrumentales > 20 Hz

Este script valida que los datos y análisis respaldan la declaración oficial.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 5 de febrero de 2026
Referencia: DECLARACION_OFICIAL_DESCUBRIMIENTO_EMPIRICO_141HZ.md
"""

import sys
import json
from pathlib import Path

# Constantes del descubrimiento
F0_TARGET = 141.7001  # Hz - Frecuencia fundamental predicha teóricamente
BANDWIDTH = 1.0       # Hz - Ancho de banda de análisis (±1 Hz)
SNR_THRESHOLD = 5.0   # σ - Umbral estándar de descubrimiento en física
GWTC1_EVENTS = 11     # Número de eventos en catálogo GWTC-1
INSTRUMENTAL_LINES = [60, 120, 180, 393]  # Hz - Líneas instrumentales conocidas
MIN_INSTRUMENTAL_SEPARATION = 20.0  # Hz - Separación mínima requerida


def validate_discovery_claims():
    """
    Valida los claims principales de la declaración oficial de descubrimiento.
    
    Returns
    -------
    bool
        True si todos los claims son válidos, False en caso contrario
    """
    print("=" * 80)
    print("VALIDACIÓN DE DECLARACIÓN OFICIAL DE DESCUBRIMIENTO EMPÍRICO")
    print("Rasgo Espectral Universal a 141.7 Hz en Ondas Gravitacionales GWTC-1")
    print("=" * 80)
    print()
    
    # Verificar que existe el archivo de resultados multi-evento
    results_file = Path('multi_event_final.json')
    
    if not results_file.exists():
        print("❌ ERROR: Archivo de resultados no encontrado: multi_event_final.json")
        print()
        print("Para generar los resultados, ejecute:")
        print("  python core/multi_event_analysis.py")
        print()
        return False
    
    # Cargar resultados
    print("📂 Cargando resultados de análisis multi-evento...")
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    stats = results['statistics']
    
    print("✅ Resultados cargados exitosamente")
    print()
    
    # Claim 1: Tasa de detección 100% (11/11 eventos GWTC-1)
    print("🔍 CLAIM 1: Tasa de detección 100% (11/11 eventos GWTC-1)")
    print("-" * 80)
    
    total_events = stats.get('total_events', 0)
    detection_rate = stats.get('detection_rate', '0%')
    
    print(f"  Total de eventos analizados: {total_events}")
    print(f"  Tasa de detección: {detection_rate}")
    
    if total_events == GWTC1_EVENTS and detection_rate == '100%':
        print(f"  ✅ VALIDADO: Detección en {GWTC1_EVENTS}/{GWTC1_EVENTS} eventos (100%)")
        claim1_valid = True
    else:
        print(f"  ❌ FALLO: Se esperaban {GWTC1_EVENTS} eventos con 100% detección")
        print(f"          Encontrado: {total_events} eventos, {detection_rate} detección")
        claim1_valid = False
    
    print()
    
    # Claim 2: SNR medio > 5σ (umbral estándar de descubrimiento)
    print("🔍 CLAIM 2: SNR medio > 5σ (umbral estándar de descubrimiento)")
    print("-" * 80)
    
    snr_mean = stats.get('snr_mean', 0)
    snr_std = stats.get('snr_std', 0)
    
    print(f"  SNR medio: {snr_mean:.2f} ± {snr_std:.2f}")
    
    if snr_mean > SNR_THRESHOLD:
        print(f"  ✅ VALIDADO: SNR medio ({snr_mean:.2f}) supera umbral de {SNR_THRESHOLD}σ")
        claim2_valid = True
    else:
        print(f"  ❌ FALLO: SNR medio ({snr_mean:.2f}) no alcanza umbral de 5σ")
        claim2_valid = False
    
    print()
    
    # Claim 3: Banda de análisis 140.7-142.7 Hz (±1 Hz de f₀)
    print(f"🔍 CLAIM 3: Banda de análisis [{F0_TARGET - BANDWIDTH:.1f}-{F0_TARGET + BANDWIDTH:.1f}] Hz (±{BANDWIDTH} Hz de f₀ = {F0_TARGET} Hz)")
    print("-" * 80)
    
    band_low = F0_TARGET - BANDWIDTH
    band_high = F0_TARGET + BANDWIDTH
    
    print(f"  Frecuencia objetivo f₀: {F0_TARGET} Hz")
    print(f"  Banda de análisis: [{band_low:.1f} - {band_high:.1f}] Hz")
    print(f"  Ancho de banda: ±{BANDWIDTH} Hz")
    
    # Verificar que todos los eventos tienen frecuencias en la banda
    events = results.get('events', [])
    all_in_band = True
    
    for event in events:
        freq = event.get('frequency_detected', 0)
        if not (band_low <= freq <= band_high):
            print(f"  ⚠️  {event['name']}: frecuencia {freq:.2f} Hz fuera de banda")
            all_in_band = False
    
    if all_in_band and len(events) == GWTC1_EVENTS:
        print(f"  ✅ VALIDADO: Todos los eventos detectados en banda [{band_low:.1f}-{band_high:.1f}] Hz")
        claim3_valid = True
    else:
        print("  ❌ FALLO: Algunos eventos fuera de la banda especificada")
        claim3_valid = False
    
    print()
    
    # Claim 4: Separación de líneas instrumentales > 20 Hz
    print(f"🔍 CLAIM 4: Separación de líneas instrumentales > {MIN_INSTRUMENTAL_SEPARATION} Hz")
    print("-" * 80)
    
    min_separation = min(abs(F0_TARGET - line) for line in INSTRUMENTAL_LINES)
    
    print(f"  Líneas instrumentales conocidas: {INSTRUMENTAL_LINES} Hz")
    print(f"  Separación mínima de f₀ = {F0_TARGET} Hz: {min_separation:.1f} Hz")
    
    if min_separation > MIN_INSTRUMENTAL_SEPARATION:
        print(f"  ✅ VALIDADO: Separación ({min_separation:.1f} Hz) > {MIN_INSTRUMENTAL_SEPARATION} Hz")
        print("               Descarta origen instrumental")
        claim4_valid = True
    else:
        print(f"  ❌ FALLO: Separación ({min_separation:.1f} Hz) ≤ 20 Hz")
        claim4_valid = False
    
    print()
    
    # Claim 5: Multi-detector (H1 y L1 separados 3,002 km)
    print("🔍 CLAIM 5: Validación multi-detector (H1, L1 separados 3,002 km)")
    print("-" * 80)
    
    # Verificar que hay datos de ambos detectores
    detectors_found = set()
    for event in events:
        if 'detectors' in event:
            detectors_found.update(event['detectors'].keys())
    
    expected_detectors = {'H1', 'L1'}
    
    print(f"  Detectores esperados: {expected_detectors}")
    print(f"  Detectores encontrados: {detectors_found}")
    
    if expected_detectors.issubset(detectors_found):
        print("  ✅ VALIDADO: Datos de detectores H1 y L1 presentes")
        print("               Separación geográfica: 3,002 km")
        claim5_valid = True
    else:
        print(f"  ⚠️  ADVERTENCIA: No todos los detectores esperados están presentes")
        claim5_valid = False
    
    print()
    
    # Resumen final
    print("=" * 80)
    print("RESUMEN DE VALIDACIÓN")
    print("=" * 80)
    
    all_claims = [claim1_valid, claim2_valid, claim3_valid, claim4_valid, claim5_valid]
    claims_passed = sum(all_claims)
    claims_total = len(all_claims)
    
    print()
    print(f"Claims validados: {claims_passed}/{claims_total}")
    print()
    
    if claim1_valid:
        print("✅ CLAIM 1: Detección 100% (11/11 GWTC-1)")
    else:
        print("❌ CLAIM 1: Detección 100% (11/11 GWTC-1)")
    
    if claim2_valid:
        print("✅ CLAIM 2: SNR medio > 5σ")
    else:
        print("❌ CLAIM 2: SNR medio > 5σ")
    
    if claim3_valid:
        print("✅ CLAIM 3: Banda de análisis [140.7-142.7] Hz")
    else:
        print("❌ CLAIM 3: Banda de análisis [140.7-142.7] Hz")
    
    if claim4_valid:
        print("✅ CLAIM 4: Separación instrumental > 20 Hz")
    else:
        print("❌ CLAIM 4: Separación instrumental > 20 Hz")
    
    if claim5_valid:
        print("✅ CLAIM 5: Multi-detector H1 y L1")
    else:
        print("❌ CLAIM 5: Multi-detector H1 y L1")
    
    print()
    print("=" * 80)
    
    if all(all_claims):
        print("🎉 VALIDACIÓN EXITOSA")
        print()
        print("Todos los claims de la declaración oficial han sido validados.")
        print()
        print("Referencia: DECLARACION_OFICIAL_DESCUBRIMIENTO_EMPIRICO_141HZ.md")
        print("=" * 80)
        return True
    else:
        print("⚠️  VALIDACIÓN INCOMPLETA")
        print()
        print(f"Algunos claims no pudieron ser validados ({claims_total - claims_passed}/{claims_total} fallos).")
        print()
        print("Por favor, revise los resultados del análisis multi-evento.")
        print("=" * 80)
        return False


def main():
    """Función principal."""
    try:
        success = validate_discovery_claims()
        sys.exit(0 if success else 1)
    
    except FileNotFoundError as e:
        print(f"❌ ERROR: Archivo no encontrado: {e}")
        sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Error al decodificar JSON: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
