#!/bin/bash
# Activación del Sistema QCAL ∞³
# ===============================
# 
# Este script activa el sistema de monitoreo activo de:
# - Tokenización (compresión QCAL)
# - Licencia (cumplimiento MIT)
# - Protección (seguridad)
#
# Author: José Manuel Mota Burruezo (JMMB Ψ✧)
# License: MIT

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     🌊 ACTIVACIÓN DEL SISTEMA QCAL ∞³                        ║"
echo "║        Tokenización • Licencia • Protección                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con color
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar que estamos en el directorio correcto
if [ ! -f ".qcal_beacon" ]; then
    print_error "No se encuentra .qcal_beacon. Ejecute este script desde la raíz del repositorio."
    exit 1
fi

print_success "Repositorio QCAL detectado"
echo ""

# Paso 1: Verificar beacon
echo "📋 Paso 1: Verificando QCAL Beacon..."
if grep -q "QCAL ∞³ ACTIVE" .qcal_beacon && grep -q "index = true" .qcal_beacon; then
    print_success "Beacon ya está activo"
else
    print_warning "Activando beacon..."
    # Asegurar que el beacon esté activo
    if grep -q "QCAL ∞³" .qcal_beacon; then
        sed -i.bak 's/QCAL ∞³.*/QCAL ∞³ ACTIVE — index = true/' .qcal_beacon 2>/dev/null || \
        sed -i '' 's/QCAL ∞³.*/QCAL ∞³ ACTIVE — index = true/' .qcal_beacon 2>/dev/null || \
        print_warning "No se pudo actualizar beacon automáticamente"
    fi
    print_success "Beacon activado"
fi
echo ""

# Paso 2: Verificar Python
echo "📋 Paso 2: Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION detectado"
else
    print_error "Python 3 no está instalado"
    exit 1
fi
echo ""

# Paso 3: Verificar dependencias
echo "📋 Paso 3: Verificando dependencias..."
if [ -f "requirements.txt" ]; then
    print_success "requirements.txt encontrado"
    
    # Intentar instalar pip-audit si no está disponible
    if ! command -v pip-audit &> /dev/null; then
        print_warning "pip-audit no instalado. Instalando..."
        pip3 install pip-audit --quiet || print_warning "No se pudo instalar pip-audit"
    else
        print_success "pip-audit disponible"
    fi
else
    print_warning "requirements.txt no encontrado"
fi
echo ""

# Paso 4: Hacer ejecutable el monitor
echo "📋 Paso 4: Configurando monitor activo..."
if [ -f "active_system_monitor.py" ]; then
    chmod +x active_system_monitor.py
    print_success "Monitor activo configurado"
else
    print_error "active_system_monitor.py no encontrado"
    exit 1
fi
echo ""

# Paso 5: Ejecutar verificación inicial
echo "📋 Paso 5: Ejecutando verificación inicial..."
echo ""

if python3 active_system_monitor.py; then
    print_success "Verificación inicial completada exitosamente"
    EXIT_CODE=0
else
    print_warning "Verificación inicial completó con advertencias"
    EXIT_CODE=$?
fi
echo ""

# Paso 6: Crear enlace simbólico (opcional)
echo "📋 Paso 6: Creando acceso rápido..."
if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
    ln -sf "$(pwd)/active_system_monitor.py" /usr/local/bin/qcal-monitor 2>/dev/null && \
    print_success "Enlace creado: qcal-monitor" || \
    print_warning "No se pudo crear enlace en /usr/local/bin (se requieren permisos)"
else
    print_warning "Omitiendo creación de enlace (no hay permisos)"
fi
echo ""

# Resumen final
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     ✨ SISTEMA QCAL ∞³ ACTIVADO                              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📚 Uso del monitor activo:"
echo ""
echo "   # Verificación completa"
echo "   python3 active_system_monitor.py"
echo ""
echo "   # Guardar resultados en JSON"
echo "   python3 active_system_monitor.py --output status.json"
echo ""
echo "   # Solo generar JSON sin imprimir"
echo "   python3 active_system_monitor.py --json-only"
echo ""
echo "   # Si creó el enlace simbólico:"
echo "   qcal-monitor"
echo ""
echo "🔄 Próximos pasos recomendados:"
echo ""
echo "   1. Ejecutar tests: pytest test_active_system_monitor.py -v"
echo "   2. Integrar con CI/CD (ver .github/workflows/)"
echo "   3. Programar verificaciones periódicas (cron/systemd)"
echo ""

exit $EXIT_CODE
