#!/usr/bin/env python3
"""
Script para descargar datos GRACE-FO ACT1B desde NASA PO.DAAC

NOTA IMPORTANTE:
Los datos GRACE-FO requieren registro gratuito en NASA Earthdata:
https://urs.earthdata.nasa.gov/users/new

Este script proporciona instrucciones y enlaces directos para la descarga manual.
Para descarga automática, se requiere configurar credenciales NASA Earthdata.

FUENTES:
- NASA PO.DAAC: https://podaac.jpl.nasa.gov/
- Dataset: GRACEFO_L1B_ASCII_GRAV_JPL_RL04
- DOI: 10.5067/GFL1B-ASJ04
- GFZ ISDC: ftp://isdcftp.gfz-potsdam.de/grace-fo/
"""

import os
import sys
import argparse
from datetime import datetime, timedelta
import requests

# Add parent directory to path to import user_confirmation
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from user_confirmation import confirm_data_download, add_confirmation_args
    HAS_CONFIRMATION = True
except ImportError:
    HAS_CONFIRMATION = False
    print("⚠️  Módulo user_confirmation no disponible")

# ============================================
# CONFIGURACIÓN
# ============================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data", "gracefo_data", "ACT1B")

# URLs de fuentes de datos
PODAAC_URL = "https://podaac.jpl.nasa.gov/dataset/GRACEFO_L1B_ASCII_GRAV_JPL_RL04"
GFZ_FTP_BASE = "ftp://isdcftp.gfz-potsdam.de/grace-fo/Level-1B/JPL/RL04/ACT/"

# ============================================
# FUNCIONES
# ============================================

def print_instructions():
    """Imprime instrucciones detalladas para descarga manual."""
    print()
    print("="*80)
    print("INSTRUCCIONES DE DESCARGA - GRACE-FO ACT1B RL04")
    print("="*80)
    print()
    print("Los datos GRACE-FO están disponibles en dos fuentes principales:")
    print()
    print("1. NASA PO.DAAC (Physical Oceanography Distributed Active Archive Center)")
    print("   - URL: " + PODAAC_URL)
    print("   - Requiere: Cuenta gratuita NASA Earthdata")
    print("   - Registro: https://urs.earthdata.nasa.gov/users/new")
    print()
    print("2. GFZ ISDC (GeoForschungsZentrum - Information System and Data Center)")
    print("   - FTP: " + GFZ_FTP_BASE)
    print("   - Acceso: Anónimo (no requiere credenciales)")
    print()
    print("="*80)
    print("PASOS PARA DESCARGA MANUAL:")
    print("="*80)
    print()
    print("OPCIÓN A - Usando PO.DAAC (Recomendado):")
    print("  1. Crear cuenta en NASA Earthdata (si no tiene una)")
    print("  2. Visitar: " + PODAAC_URL)
    print("  3. Hacer clic en 'Download' o 'Data Access'")
    print("  4. Seleccionar período de tiempo deseado")
    print("  5. Filtrar por producto: ACT1B")
    print("  6. Filtrar por satélite: GRACE-C o GRACE-D")
    print("  7. Descargar archivos .dat")
    print()
    print("OPCIÓN B - Usando GFZ FTP:")
    print("  1. Conectar vía FTP a: isdcftp.gfz-potsdam.de")
    print("  2. Navegar a: /grace-fo/Level-1B/JPL/RL04/ACT/")
    print("  3. Seleccionar año (ej: 2024/)")
    print("  4. Seleccionar mes (ej: 01/)")
    print("  5. Descargar archivos ACT1B_*_C_04.dat o ACT1B_*_D_04.dat")
    print()
    print("="*80)
    print("EJEMPLO - Usando wget con GFZ FTP:")
    print("="*80)
    print()
    print("  # Descargar todos los archivos de enero 2024 para GRACE-C:")
    print("  wget -r -np -nH --cut-dirs=5 \\")
    print("       ftp://isdcftp.gfz-potsdam.de/grace-fo/Level-1B/JPL/RL04/ACT/2024/01/ \\")
    print("       -P", DATA_DIR, "\\")
    print("       -A 'ACT1B_*_C_04.dat'")
    print()
    print("  # Descargar todos los archivos de enero 2024 para GRACE-D:")
    print("  wget -r -np -nH --cut-dirs=5 \\")
    print("       ftp://isdcftp.gfz-potsdam.de/grace-fo/Level-1B/JPL/RL04/ACT/2024/01/ \\")
    print("       -P", DATA_DIR, "\\")
    print("       -A 'ACT1B_*_D_04.dat'")
    print()
    print("="*80)
    print("DIRECTORIO DE DESTINO:")
    print("="*80)
    print()
    print(f"  {DATA_DIR}")
    print()
    print("Los archivos descargados deben colocarse en este directorio para que")
    print("el script de análisis (analizar_gracefo_act1b.py) pueda encontrarlos.")
    print()
    print("="*80)


def create_data_directory():
    """Crea el directorio de datos si no existe."""
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"✅ Directorio de datos creado/verificado: {DATA_DIR}")


def download_via_wget(year, month, satellite='C'):
    """
    Genera y ejecuta comando wget para descargar datos.
    
    Args:
        year: Año (ej: 2024)
        month: Mes (1-12)
        satellite: 'C' o 'D'
    """
    month_str = f"{month:02d}"
    url = f"ftp://isdcftp.gfz-potsdam.de/grace-fo/Level-1B/JPL/RL04/ACT/{year}/{month_str}/"
    pattern = f"ACT1B_*_{satellite}_04.dat"
    
    cmd = [
        "wget",
        "-r",  # Recursivo
        "-np",  # No parent
        "-nH",  # No host directories
        "--cut-dirs=5",  # Cortar directorios superiores
        "-P", DATA_DIR,  # Directorio de destino
        "-A", pattern,  # Aceptar solo este patrón
        url
    ]
    
    print()
    print("Ejecutando comando wget:")
    print(" ".join(cmd))
    print()
    
    import subprocess
    try:
        subprocess.run(cmd, check=True)
        print()
        print("✅ Descarga completada exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print()
        print(f"❌ Error durante la descarga: {e}")
        return False
    except FileNotFoundError:
        print()
        print("❌ Error: wget no está instalado")
        print("   Instale wget o use descarga manual")
        return False


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Descargar datos GRACE-FO ACT1B desde NASA PO.DAAC o GFZ FTP',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--instructions',
        action='store_true',
        help='Mostrar instrucciones de descarga manual'
    )
    
    parser.add_argument(
        '--wget',
        action='store_true',
        help='Intentar descarga automática usando wget'
    )
    
    parser.add_argument(
        '--year',
        type=int,
        default=2024,
        help='Año de los datos (default: 2024)'
    )
    
    parser.add_argument(
        '--month',
        type=int,
        default=1,
        help='Mes de los datos (1-12, default: 1)'
    )
    
    parser.add_argument(
        '--satellite',
        type=str,
        choices=['C', 'D', 'both'],
        default='C',
        help='Satélite a descargar: C, D, o both (default: C)'
    )
    
    if HAS_CONFIRMATION:
        add_confirmation_args(parser)
    
    args = parser.parse_args()
    
    print()
    print("="*80)
    print("GRACE-FO ACT1B - DESCARGA DE DATOS")
    print("="*80)
    
    # Crear directorio de datos
    create_data_directory()
    
    # Mostrar instrucciones si se solicita
    if args.instructions or not args.wget:
        print_instructions()
    
    # Descarga automática con wget si se solicita
    if args.wget:
        # Confirmación de usuario
        if HAS_CONFIRMATION:
            # Estimar tamaño (aproximadamente 1 MB por día por satélite)
            import calendar
            days_in_month = calendar.monthrange(args.year, args.month)[1]
            estimated_size_mb = days_in_month * 1.0
            if args.satellite == 'both':
                estimated_size_mb *= 2
            
            if not confirm_data_download(estimated_size_mb, auto_yes=getattr(args, 'yes', False)):
                print("Descarga cancelada por el usuario.")
                return
        
        print()
        print("="*80)
        print("DESCARGA AUTOMÁTICA CON WGET")
        print("="*80)
        print(f"Año: {args.year}")
        print(f"Mes: {args.month}")
        print(f"Satélite(s): {args.satellite}")
        
        satellites = ['C', 'D'] if args.satellite == 'both' else [args.satellite]
        
        success = True
        for sat in satellites:
            print()
            print(f"Descargando datos para GRACE-{sat}...")
            if not download_via_wget(args.year, args.month, sat):
                success = False
        
        if success:
            print()
            print("="*80)
            print("✅ DESCARGA COMPLETADA")
            print("="*80)
            print()
            print("Puede ejecutar el análisis con:")
            print("  python scripts/analizar_gracefo_act1b.py")
        else:
            print()
            print("="*80)
            print("⚠️  DESCARGA INCOMPLETA")
            print("="*80)
            print()
            print("Revise los errores anteriores o use descarga manual.")
            print("Ejecute con --instructions para ver las instrucciones.")
    
    print()


if __name__ == "__main__":
    main()
