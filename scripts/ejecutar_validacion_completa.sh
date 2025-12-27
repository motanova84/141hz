#!/bin/bash
# Script de Ejecución Completa de Validación GW250114
# Sistema de Validación Proactiva Avanzada

echo "🌌 INICIANDO VALIDACIÓN COMPLETA GW250114"
echo "=========================================="
echo "Fecha: $(date)"
echo "=========================================="
echo ""

# Detectar directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT" || exit 1

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Verificar si existe entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv || {
        print_error "Error creando entorno virtual"
        exit 1
    }
    print_success "Entorno virtual creado"
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate || {
    print_error "Error activando entorno virtual"
    exit 1
}
print_success "Entorno virtual activado"

# Instalar/actualizar dependencias
echo ""
echo "📦 Verificando dependencias..."
pip install --upgrade pip --quiet 2>&1 | grep -v "WARNING" || true
pip install -r requirements.txt --quiet 2>&1 | grep -v "WARNING" || true

if [ $? -eq 0 ]; then
    print_success "Dependencias instaladas"
else
    print_warning "Algunas dependencias podrían no haberse instalado - intentando instalar básicas..."
    pip install numpy scipy matplotlib pandas pyyaml --quiet 2>&1 || true
fi

# Crear directorio de resultados
echo ""
echo "📁 Creando directorios de salida..."
mkdir -p results/figures
mkdir -p results/data_processed
mkdir -p results/reports
mkdir -p results/json_output
print_success "Directorios creados"

# Ejecutar sistema completo de validación
echo ""
echo "🚀 EJECUTANDO SISTEMA DE VALIDACIÓN COMPLETO"
echo "=========================================="
echo ""

python scripts/sistema_validacion_completo.py

EXIT_CODE=$?

echo ""
echo "=========================================="

if [ $EXIT_CODE -eq 0 ]; then
    print_success "VALIDACIÓN COMPLETADA EXITOSAMENTE"
    echo ""
    echo "📊 Resultados disponibles en:"
    echo "   • results/informe_validacion_gw250114.json"
    echo "   • results/resumen_validacion.txt"
    echo "   • results/resultados_busqueda_gwtc1.json"
    echo ""
else
    print_error "VALIDACIÓN COMPLETADA CON ERRORES"
    echo ""
    echo "📋 Revise los logs para más detalles"
    echo ""
fi

# Desactivar entorno virtual
deactivate 2>/dev/null

echo "🔔 Pipeline de validación finalizado"
echo "Fecha de finalización: $(date)"

exit $EXIT_CODE
