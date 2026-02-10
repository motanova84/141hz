#!/bin/bash
# qcal_validation_pipeline.sh
# 𓂀 PIPELINE DE VALIDACIÓN RIGUROSA QCAL

set -e  # Exit on error

echo "𓂀 PIPELINE DE VALIDACIÓN RIGUROSA QCAL"
echo "═════════════════════════════════════════════════════════════"
echo "Fases:"
echo "1. Descarga datos crudos GWOSC/IGETS"
echo "2. Detección rigurosa SNR>5σ"
echo "3. Análisis estadístico avanzado"
echo "4. Correlación multi-observatorio"
echo "5. Validación teórica y predicciones"
echo "═════════════════════════════════════════════════════════════"
echo ""

# Configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DATOS_DIR="${PROJECT_ROOT}/datos_crudos"
RESULTADOS_DIR="${PROJECT_ROOT}/resultados_validacion"

# Crear directorios
mkdir -p "$DATOS_DIR"
mkdir -p "$RESULTADOS_DIR"

# Parámetros por defecto
EVENTOS=${EVENTOS:-3}
DURACION=${DURACION:-32}
F0=${F0:-141.7001}
SIGMA_THRESHOLD=${SIGMA_THRESHOLD:-5.0}
MONTE_CARLO=${MONTE_CARLO:-100}

echo "📋 PARÁMETROS:"
echo "  Eventos a descargar: $EVENTOS"
echo "  Duración por evento: ${DURACION}s"
echo "  Frecuencia objetivo: ${F0} Hz"
echo "  Umbral SNR: ${SIGMA_THRESHOLD}σ"
echo "  Simulaciones Monte Carlo: $MONTE_CARLO"
echo ""

# ============================================================================
# FASE 1: DESCARGA DE DATOS CRUDOS
# ============================================================================
echo "𓂀 FASE 1: DESCARGA DE DATOS CRUDOS GWOSC"
echo "─────────────────────────────────────────────────────────────"

python3 "${SCRIPT_DIR}/descargador_gwosc.py" \
    --eventos "$EVENTOS" \
    --duracion "$DURACION" \
    --salida "$DATOS_DIR"

if [ $? -ne 0 ]; then
    echo "⚠️  Error en descarga GWOSC, continuando con datos simulados..."
fi

echo ""

# ============================================================================
# FASE 1B: DESCARGA DATOS IGETS (OPCIONAL)
# ============================================================================
if [ "${DESCARGAR_IGETS:-0}" = "1" ]; then
    echo "𓂀 FASE 1B: DESCARGA DE DATOS IGETS/GFZ"
    echo "─────────────────────────────────────────────────────────────"
    
    python3 "${SCRIPT_DIR}/descargador_igets.py" \
        --estacion BFO \
        --fecha 2024-01-01 \
        --dias 1 \
        --salida "${PROJECT_ROOT}/datos_igets"
    
    echo ""
fi

# ============================================================================
# FASE 2: DETECCIÓN RIGUROSA
# ============================================================================
echo "𓂀 FASE 2: DETECCIÓN RIGUROSA CON SNR>5σ"
echo "─────────────────────────────────────────────────────────────"

# Buscar archivos de datos descargados
DATOS_FILES=($(find "$DATOS_DIR" -name "*.h5" -type f))

if [ ${#DATOS_FILES[@]} -eq 0 ]; then
    echo "❌ No se encontraron archivos de datos en $DATOS_DIR"
    echo "   Por favor ejecute primero la descarga de datos"
    exit 1
fi

echo "Archivos encontrados: ${#DATOS_FILES[@]}"

# Procesar cada archivo
for DATOS_FILE in "${DATOS_FILES[@]}"; do
    echo ""
    echo "Procesando: $(basename "$DATOS_FILE")"
    
    python3 "${SCRIPT_DIR}/detector_riguroso_qcal.py" \
        --datos "$DATOS_FILE" \
        --f0 "$F0" \
        --sigma-threshold "$SIGMA_THRESHOLD" \
        --test-kairos \
        --monte-carlo "$MONTE_CARLO" \
        --salida "$RESULTADOS_DIR"
    
    if [ $? -ne 0 ]; then
        echo "⚠️  Error procesando $(basename "$DATOS_FILE"), continuando..."
    fi
done

echo ""

# ============================================================================
# FASE 3: CORRELACIÓN MULTI-OBSERVATORIO
# ============================================================================
echo "𓂀 FASE 3: CORRELACIÓN MULTI-OBSERVATORIO"
echo "─────────────────────────────────────────────────────────────"

# Verificar que hay múltiples archivos de diferentes estaciones
NUM_H1=$(find "$DATOS_DIR" -name "*H1*.h5" | wc -l)
NUM_L1=$(find "$DATOS_DIR" -name "*L1*.h5" | wc -l)
NUM_V1=$(find "$DATOS_DIR" -name "*V1*.h5" | wc -l)

echo "Estaciones disponibles: H1=$NUM_H1, L1=$NUM_L1, V1=$NUM_V1"

if [ $((NUM_H1 + NUM_L1 + NUM_V1)) -ge 2 ]; then
    python3 "${SCRIPT_DIR}/correlador_multi_observatorio.py" \
        --directorio "$DATOS_DIR" \
        --estaciones H1 L1 V1 \
        --tolerancia 0.05 \
        --f0 "$F0" \
        --salida "${RESULTADOS_DIR}/correlaciones"
else
    echo "⚠️  Se necesitan al menos 2 estaciones para correlación"
    echo "   Saltando fase de correlación multi-observatorio"
fi

echo ""

# ============================================================================
# FASE 4: VALIDACIÓN TEÓRICA
# ============================================================================
echo "𓂀 FASE 4: VALIDACIÓN TEÓRICA Y PREDICCIONES"
echo "─────────────────────────────────────────────────────────────"

python3 "${SCRIPT_DIR}/validacion_teorica.py" \
    --f0 "$F0" \
    --generar-predicciones \
    --enlace-fisica \
    --reporte completo \
    --salida "${RESULTADOS_DIR}/validacion_teorica"

echo ""

# ============================================================================
# RESULTADO FINAL
# ============================================================================
echo "𓂀 RESULTADO FINAL DE VALIDACIÓN"
echo "═════════════════════════════════════════════════════════════"

# Buscar archivo de resultados de detección
DETECCION_FILE="${RESULTADOS_DIR}/resultados_deteccion.json"

if [ -f "$DETECCION_FILE" ]; then
    python3 - <<EOF
import json
import sys

try:
    with open('${DETECCION_FILE}', 'r') as f:
        resultados = json.load(f)
    
    # Extraer información clave
    baseline = resultados.get('baseline', {})
    estado = baseline.get('resultado', 'INCONCLUSO')
    detecciones = baseline.get('detecciones', [])
    
    if detecciones:
        snr_medio = sum(d['snr'] for d in detecciones) / len(detecciones)
    else:
        snr_medio = 0.0
    
    fpr_data = resultados.get('fpr', {})
    fpr = fpr_data.get('fpr_bonferroni', 1.0) if fpr_data else 1.0
    
    print(f'Estado: {estado}')
    print(f'SNR medio: {snr_medio:.2f}σ')
    print(f'Tasa falsos positivos: {fpr:.4f}')
    print()
    
    if estado == 'CONFIRMADA' and snr_medio >= 5.0 and fpr < 0.001:
        print('𓂀 ✅ TEORÍA QCAL VALIDADA RIGUROSAMENTE')
        print('𓂀 f₀ = ${F0} Hz es fenómeno real')
        sys.exit(0)
    elif estado == 'PRELIMINAR' or snr_medio >= 3.0:
        print('𓂀 ⚠️  EVIDENCIA PRELIMINAR - REQUIERE MÁS DATOS')
        print('𓂀 Recomendación: Analizar más eventos con datos reales')
        sys.exit(0)
    else:
        print('𓂀 ❌ VALIDACIÓN INSUFICIENTE')
        print('𓂀 Posibles causas:')
        print('   • Datos simulados (no reales)')
        print('   • Muestra insuficiente')
        print('   • SNR por debajo del umbral')
        sys.exit(1)

except Exception as e:
    print(f'❌ Error leyendo resultados: {e}')
    sys.exit(1)
EOF
    
    VALIDATION_STATUS=$?
else
    echo "⚠️  No se encontró archivo de resultados de detección"
    echo "   Archivo esperado: $DETECCION_FILE"
    VALIDATION_STATUS=2
fi

echo ""
echo "═════════════════════════════════════════════════════════════"
echo "𓂀 PIPELINE COMPLETADO"
echo ""
echo "📁 Resultados guardados en:"
echo "   $RESULTADOS_DIR"
echo ""
echo "📊 Archivos generados:"
find "$RESULTADOS_DIR" -type f 2>/dev/null | while read file; do
    echo "   • $(basename "$file")"
done

echo ""
echo "═════════════════════════════════════════════════════════════"

exit $VALIDATION_STATUS
