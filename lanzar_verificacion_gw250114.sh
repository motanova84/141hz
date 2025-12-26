#!/bin/bash
# lanzar_verificacion_gw250114.sh
# Script de lanzamiento y verificación inmediata de GW250114

echo "🌌 VERIFICACIÓN INMEDIATA GW250114"
echo "==================================="
echo ""

# Detectar directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR" || exit 1

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Crear directorios necesarios
echo "📁 Creando estructura de directorios..."
mkdir -p data/raw
mkdir -p resultados
mkdir -p scripts
mkdir -p dashboard

print_success "Directorios creados/verificados"
echo ""

# Verificar que existe el script de verificación
if [ ! -f "scripts/verificador_gw250114.py" ]; then
    print_error "Script verificador_gw250114.py no encontrado"
    echo "   Esperado en: scripts/verificador_gw250114.py"
    exit 1
fi

# Verificar Python
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    print_error "Python no encontrado"
    echo "   Por favor instalar Python 3.7+"
    exit 1
fi

# Determinar comando Python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

print_info "Usando: $PYTHON_CMD"
echo ""

# Ejecutar verificación inmediata
echo "🔍 Ejecutando verificación inmediata..."
echo ""

$PYTHON_CMD scripts/verificador_gw250114.py

# Capturar código de salida
EXIT_CODE=$?

echo ""
echo "==================================="

# Si no está disponible, iniciar monitoreo continuo
if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    print_warning "GW250114 no disponible aún"
    echo ""
    echo "🔄 ¿Desea iniciar monitoreo continuo en segundo plano?"
    echo "   El sistema verificará automáticamente cada hora"
    echo ""
    
    # En modo no interactivo o si se pasa argumento --auto, iniciar automáticamente
    if [ "$1" == "--auto" ] || [ ! -t 0 ]; then
        RESPUESTA="s"
    else
        read -p "Iniciar monitoreo continuo? (s/n): " RESPUESTA
    fi
    
    if [[ "$RESPUESTA" =~ ^[SsYy]$ ]]; then
        echo ""
        print_info "Iniciando monitoreo continuo en segundo plano..."
        
        # Ejecutar en segundo plano
        nohup $PYTHON_CMD scripts/verificador_gw250114.py --continuo > monitoreo_gw250114.log 2>&1 &
        
        MONITOR_PID=$!
        
        echo ""
        print_success "Monitoreo ejecutándose en segundo plano"
        echo "   📝 Logs: monitoreo_gw250114.log"
        echo "   🔢 PID: $MONITOR_PID"
        echo "   🛑 Para detener: pkill -f verificador_gw250114.py"
        echo ""
        echo "📊 Para ver el estado actual:"
        echo "   tail -f monitoreo_gw250114.log"
        echo ""
        echo "🎯 El sistema alertará automáticamente cuando GW250114 esté disponible"
        echo "   Crear archivo: GW250114_DISPONIBLE.txt"
        
        # Guardar PID en archivo
        echo $MONITOR_PID > monitoreo_gw250114.pid
        print_info "PID guardado en: monitoreo_gw250114.pid"
    else
        echo ""
        print_info "Monitoreo continuo NO iniciado"
        echo ""
        echo "💡 Para iniciar manualmente más tarde:"
        echo "   nohup $PYTHON_CMD scripts/verificador_gw250114.py --continuo > monitoreo_gw250114.log 2>&1 &"
    fi
else
    echo ""
    print_success "GW250114 DISPONIBLE - Listo para análisis"
    echo ""
    echo "🚀 Ejecutar análisis con:"
    echo "   $PYTHON_CMD scripts/analizar_gw250114.py"
fi

echo ""
echo "==================================="
echo "✅ Script completado"
echo ""

exit $EXIT_CODE
