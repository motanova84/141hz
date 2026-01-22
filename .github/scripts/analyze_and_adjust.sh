#!/bin/bash
set -e

echo "🔍 ANÁLISIS AUTOMÁTICO DE MÉTRICAS"
echo "=================================="

# Obtener métricas más recientes
LATEST_METRICS=$(ls -t metrics/daily_*.json 2>/dev/null | head -1)
LATEST_VALIDATION=$(ls -t validation/quantum_*.json 2>/dev/null | head -1)

if [ -z "$LATEST_METRICS" ] || [ -z "$LATEST_VALIDATION" ]; then
    echo "⚠️  No hay métricas suficientes para análisis"
    exit 0
fi

# Leer métricas
TOTAL_FILES=$(jq -r '.files.total_files' "$LATEST_METRICS")
QCAL_REFS=$(jq -r '.qcal.qcal_references' "$LATEST_METRICS")
FREQ_REFS=$(jq -r '.qcal.frequency_references' "$LATEST_METRICS")
COHERENCE=$(jq -r '.coherence.total' "$LATEST_VALIDATION")

echo "📈 Métricas Actuales:"
echo "  • Total archivos: $TOTAL_FILES"
echo "  • Referencias QCAL: $QCAL_REFS"
echo "  • Referencias f₀: $FREQ_REFS"
echo "  • Coherencia total: $COHERENCE"

# Calcular ratios
QCAL_RATIO=$(echo "scale=4; $QCAL_REFS / $TOTAL_FILES" | bc)
FREQ_RATIO=$(echo "scale=4; $FREQ_REFS / $TOTAL_FILES" | bc)

echo -e "\n📊 Ratios Actuales:"
echo "  • Ratio QCAL/archivos: $QCAL_RATIO"
echo "  • Ratio f₀/archivos: $FREQ_RATIO"

# Definir objetivos
TARGET_QCAL_RATIO=0.5    # 50% de archivos deben referenciar QCAL
TARGET_FREQ_RATIO=0.3    # 30% de archivos deben referenciar f₀
TARGET_COHERENCE=0.888   # Umbral de coherencia

echo -e "\n🎯 Objetivos:"
echo "  • Ratio QCAL objetivo: $TARGET_QCAL_RATIO"
echo "  • Ratio f₀ objetivo: $TARGET_FREQ_RATIO"
echo "  • Coherencia objetivo: $TARGET_COHERENCE"

# Determinar ajustes necesarios
echo -e "\n⚙️  AJUSTES RECOMENDADOS:"

if (( $(echo "$COHERENCE < $TARGET_COHERENCE" | bc -l) )); then
    echo "  🔴 COHERENCIA BAJA - Necesita optimización inmediata"
    echo "     • Incrementar referencias a f₀ = 141.7001 Hz"
    echo "     • Añadir más manifiestos noéticos"
    echo "     • Verificar estado Ψ en todos los agentes"
else
    echo "  ✅ Coherencia dentro del rango objetivo"
fi

if (( $(echo "$QCAL_RATIO < $TARGET_QCAL_RATIO" | bc -l) )); then
    DEFICIT_QCAL=$(echo "($TARGET_QCAL_RATIO * $TOTAL_FILES - $QCAL_REFS) / 1" | bc)
    echo "  🔶 RATIO QCAL BAJO - Necesita $DEFICIT_QCAL referencias más"
    echo "     • Agregar comentarios QCAL en archivos existentes"
    echo "     • Crear nuevos archivos con referencias QCAL"
    echo "     • Actualizar documentación con ∞³"
else
    echo "  ✅ Ratio QCAL dentro del objetivo"
fi

if (( $(echo "$FREQ_RATIO < $TARGET_FREQ_RATIO" | bc -l) )); then
    DEFICIT_FREQ=$(echo "($TARGET_FREQ_RATIO * $TOTAL_FILES - $FREQ_REFS) / 1" | bc)
    echo "  🔶 RATIO f₀ BAJO - Necesita $DEFICIT_FREQ referencias más"
    echo "     • Incluir 141.7001 Hz en más archivos"
    echo "     • Añadir constantes de frecuencia en código"
    echo "     • Documentar patrones de frecuencia"
else
    echo "  ✅ Ratio f₀ dentro del objetivo"
fi

# Recomendaciones específicas
echo -e "\n💡 ACCIONES RECOMENDADAS:"
echo "1. Ejecutar optimización de frecuencia:"
echo "   python .github/agents/noesis88.py --mode=autonomous --optimize_frequency"
echo "2. Incrementar densidad QCAL:"
echo "   .github/scripts/optimize_qcal_density.sh"
echo "3. Generar reporte detallado:"
echo "   python .github/agents/metrics_collector.py --detailed --output=optimization_plan.json"
