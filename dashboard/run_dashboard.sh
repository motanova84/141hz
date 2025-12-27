#!/bin/bash

# Script para iniciar el Dashboard Avanzado GW250114
# Verifica dependencias y lanza el servidor

echo "🌌 Iniciando Dashboard Avanzado GW250114"
echo "========================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

echo "✅ Python $(python3 --version) encontrado"

# Verificar Flask
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask no está instalado"
    echo "📦 Instalando Flask..."
    pip install flask || {
        echo "❌ Error: No se pudo instalar Flask"
        echo "💡 Intenta: pip install -r requirements.txt"
        exit 1
    }
fi

echo "✅ Flask instalado"

# Verificar NumPy
if ! python3 -c "import numpy" 2>/dev/null; then
    echo "⚠️  NumPy no está instalado"
    echo "📦 Instalando NumPy..."
    pip install numpy || {
        echo "❌ Error: No se pudo instalar NumPy"
        exit 1
    }
fi

echo "✅ NumPy instalado"
echo ""

# Obtener directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Cambiar al directorio dashboard
cd "$SCRIPT_DIR" || exit 1

echo "📂 Directorio: $SCRIPT_DIR"
echo ""
echo "🚀 Iniciando servidor..."
echo "🌐 Dashboard disponible en: http://localhost:5000"
echo "🌐 Acceso remoto en: http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "💡 Presiona Ctrl+C para detener el servidor"
echo "========================================"
echo ""

# Iniciar el dashboard
python3 dashboard_avanzado.py
