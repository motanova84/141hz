#!/usr/bin/env python3
"""
Protocolo Sage ∴ - Activación del Sabio Vibracional

Una estructura simbiótica donde los scripts .sage verifican principios del Campo QCAL ∞³
con precisión ilimitada.

Un puente matemático místico entre:
- RΨ (Radio Cuántico del Campo)
- f₀ = 141.7001 Hz (Frecuencia del Origen)
- ζ(s) (Zeta como vibración aritmética)
- αΨ (Derivada consciente de la creación)

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
DOI: 10.5281/zenodo.17379721
Fecha: Octubre 2025
"""

from pathlib import Path
import subprocess
import sys


def activar_sabio(script_sage):
    """
    Ejecuta un script .sage como un acto sabio dentro del sistema QCAL ∞³

    Esta función invoca al sistema algebraico computacional Sage para ejecutar
    scripts que verifican principios del Campo QCAL ∞³ con precisión arbitraria.

    Parameters
    ----------
    script_sage : str or Path
        Ruta al script .sage que se desea ejecutar

    Returns
    -------
    subprocess.CompletedProcess
        Resultado de la ejecución del script

    Raises
    ------
    FileNotFoundError
        Si el script .sage no existe en la ruta especificada
    RuntimeError
        Si Sage no está instalado o la ejecución falla

    Examples
    --------
    >>> activar_sabio("scripts/validacion_radio_cuantico.sage")
    ⚛️ Invocando al Sabio: scripts/validacion_radio_cuantico.sage
    ✅ Sabio activado con éxito ∴

    Notes
    -----
    El protocolo Sage ∴ permite:
    - Cálculos con precisión arbitraria (mpmath, RealField)
    - Verificación algebraica simbólica
    - Análisis de sensibilidad de constantes fundamentales
    - Exploración matemática del espacio QCAL ∞³
    """
    # Convertir a Path para manejo robusto
    script_path = Path(script_sage)

    # Verificar existencia del script
    if not script_path.exists():
        raise FileNotFoundError(f"No se encuentra el sabio en: {script_sage}")

    # Verificar que sea un archivo .sage
    if script_path.suffix != '.sage':
        print(f"⚠️ Advertencia: El archivo {script_sage} no tiene extensión .sage")

    print(f"⚛️ Invocando al Sabio: {script_sage}")
    print("━" * 60)

    try:
        # Ejecutar el script con Sage
        result = subprocess.run(
            ["sage", str(script_path)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos de timeout
        )

        # Mostrar salida estándar
        if result.stdout:
            print(result.stdout)

        # Verificar resultado
        if result.returncode != 0:
            print(f"❌ El sabio falló:\n{result.stderr}")
            raise RuntimeError(
                f"Error al ejecutar {script_sage}. "
                f"Código de salida: {result.returncode}"
            )
        else:
            print("━" * 60)
            print("✅ Sabio activado con éxito ∴")
            print(f"   Campo QCAL ∞³ verificado en: {script_sage}")

        return result

    except FileNotFoundError as e:
        error_msg = (
            f"❌ Sage no está instalado o no está en el PATH\n"
            f"   Para instalar Sage, visite: https://www.sagemath.org/\n"
            f"   Error: {e}"
        )
        print(error_msg)
        raise RuntimeError(error_msg) from e

    except subprocess.TimeoutExpired:
        error_msg = f"❌ El script {script_sage} excedió el tiempo límite de ejecución"
        print(error_msg)
        raise RuntimeError(error_msg)


def listar_sabios(directorio="."):
    """
    Lista todos los scripts .sage disponibles en un directorio

    Parameters
    ----------
    directorio : str or Path, optional
        Directorio donde buscar scripts .sage (default: directorio actual)

    Returns
    -------
    list of Path
        Lista de rutas a scripts .sage encontrados
    """
    directorio_path = Path(directorio)

    if not directorio_path.exists():
        print(f"⚠️ El directorio {directorio} no existe")
        return []

    # Buscar recursivamente todos los .sage
    sage_scripts = list(directorio_path.rglob("*.sage"))

    if sage_scripts:
        print(f"📚 Sabios encontrados en {directorio}:")
        for script in sorted(sage_scripts):
            print(f"   • {script}")
    else:
        print(f"🔍 No se encontraron sabios (.sage) en {directorio}")

    return sage_scripts


def verificar_sage_instalado():
    """
    Verifica si Sage está instalado y accesible

    Returns
    -------
    bool
        True si Sage está instalado, False en caso contrario
    """
    try:
        result = subprocess.run(
            ["sage", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Sage instalado: {version}")
            return True
        else:
            return False

    except FileNotFoundError:
        print("❌ Sage no está instalado o no está en el PATH")
        print("   Para instalar Sage, visite: https://www.sagemath.org/")
        return False
    except Exception as e:
        print(f"⚠️ Error al verificar Sage: {e}")
        return False


def main():
    """
    Función principal para uso desde línea de comandos
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Protocolo Sage ∴ - Activación del Sabio Vibracional del Campo QCAL ∞³",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Activar un sabio específico
  python sage_activation.py scripts/validacion_radio_cuantico.sage

  # Listar todos los sabios disponibles
  python sage_activation.py --listar scripts/

  # Verificar instalación de Sage
  python sage_activation.py --verificar

El protocolo Sage ∴ permite verificar principios del Campo QCAL ∞³ con:
  - Precisión arbitraria en cálculos numéricos
  - Verificación algebraica simbólica
  - Análisis matemático riguroso de f₀ = 141.7001 Hz
        """
    )

    parser.add_argument(
        'script',
        nargs='?',
        help='Ruta al script .sage que se desea ejecutar'
    )

    parser.add_argument(
        '--listar', '-l',
        metavar='DIR',
        help='Listar todos los scripts .sage en un directorio'
    )

    parser.add_argument(
        '--verificar', '-v',
        action='store_true',
        help='Verificar si Sage está instalado'
    )

    args = parser.parse_args()

    # Modo: verificar instalación
    if args.verificar:
        return 0 if verificar_sage_instalado() else 1

    # Modo: listar sabios
    if args.listar:
        sabios = listar_sabios(args.listar)
        return 0 if sabios else 1

    # Modo: ejecutar script
    if args.script:
        try:
            activar_sabio(args.script)
            return 0
        except Exception as e:
            print(f"\n💥 Error fatal: {e}", file=sys.stderr)
            return 1

    # Sin argumentos: mostrar ayuda
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
