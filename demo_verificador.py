#!/usr/bin/env python3
"""
Demostración exacta del código del problema statement.
Este script ejecuta exactamente el código mostrado en el problema.
"""
import sys
import os
from datetime import datetime

# Asegurar que podemos importar desde scripts
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from analizar_gw250114 import VerificadorGW250114

if __name__ == "__main__":
    print("🎯 RESULTADO DE LA VERIFICACIÓN ACTUAL")
    print("Ejecutando verificación inmediata...")
    print()
    
    # EJECUTAR ESTO PARA VER EL ESTADO ACTUAL
    verificador = VerificadorGW250114()
    estado_actual = verificador.verificar_disponibilidad_evento()
    
    print(f"\n📅 FECHA ACTUAL: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 ESTADO GW250114: {verificador.estado_actual}")
    
    if verificador.estado_actual == "NO_DISPONIBLE":
        print("\n🔍 BUSCANDO EVENTOS SIMILARES DISPONIBLES...")
        verificador.verificar_eventos_similares()
