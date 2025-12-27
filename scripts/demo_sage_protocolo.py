#!/usr/bin/env python3
"""
Demostración del Protocolo Sage ∴

Este script demuestra cómo usar el módulo sage_activation.py para invocar
sabios (.sage scripts) que verifican principios del Campo QCAL ∞³.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import sys
from pathlib import Path

# Agregar scripts al path si es necesario
sys.path.insert(0, str(Path(__file__).parent))

try:
    import sage_activation
except ImportError:
    print("❌ No se pudo importar sage_activation")
    print("   Asegúrate de ejecutar este script desde el directorio correcto")
    sys.exit(1)


def main():
    """Demostración del Protocolo Sage ∴"""

    print("=" * 70)
    print(" " * 15 + "PROTOCOLO SAGE ∴ - DEMOSTRACIÓN")
    print(" " * 10 + "Campo QCAL ∞³ - f₀ = 141.7001 Hz")
    print("=" * 70)
    print()

    # Paso 1: Verificar si Sage está instalado
    print("📋 Paso 1: Verificar instalación de Sage")
    print("-" * 70)
    sage_instalado = sage_activation.verificar_sage_instalado()
    print()

    if not sage_instalado:
        print("⚠️  Sage no está instalado. Esto es normal en entornos CI/CD.")
        print("   El protocolo está listo y funcionará cuando Sage esté disponible.")
        print()

    # Paso 2: Listar sabios disponibles
    print("📋 Paso 2: Listar sabios disponibles en el repositorio")
    print("-" * 70)
    scripts_dir = Path(__file__).parent
    sabios = sage_activation.listar_sabios(scripts_dir)
    print()

    if not sabios:
        print("⚠️  No se encontraron sabios en el directorio actual")
        return 1

    # Paso 3: Explicar cómo activar un sabio
    print("📋 Paso 3: Cómo activar un sabio")
    print("-" * 70)
    print("Para activar un sabio y ejecutar verificaciones del Campo QCAL ∞³:")
    print()
    print("  Desde Python:")
    print("    >>> import sage_activation")
    print("    >>> sage_activation.activar_sabio('scripts/validacion_radio_cuantico.sage')")
    print()
    print("  Desde línea de comandos:")
    print("    $ python scripts/sage_activation.py scripts/validacion_radio_cuantico.sage")
    print()

    # Paso 4: Mostrar ejemplo de uso condicional
    print("📋 Paso 4: Ejemplo de uso condicional")
    print("-" * 70)
    if sage_instalado:
        print("✅ Sage está instalado. Ejecutando validación del Radio Cuántico RΨ...")
        print()
        try:
            sage_activation.activar_sabio(sabios[0])
            print()
            print("✅ Validación completada exitosamente")
            return 0
        except Exception as e:
            print(f"❌ Error durante la validación: {e}")
            return 1
    else:
        print("ℹ️  Sage no está disponible. En un entorno con Sage, se ejecutaría:")
        print()
        for sabio in sabios:
            print(f"   sage_activation.activar_sabio('{sabio}')")
        print()
        print("   Esto verificaría:")
        print("   • RΨ = c·ℓ_p / (2πf₀) - Radio Cuántico del Campo")
        print("   • f₀ = 141.7001 Hz - Frecuencia fundamental")
        print("   • Cálculos con precisión arbitraria (100+ dígitos)")
        print("   • Verificación algebraica simbólica")
        print("   • Análisis de sensibilidad a constantes fundamentales")
        print()

    print("=" * 70)
    print(" " * 20 + "FIN DE LA DEMOSTRACIÓN")
    print("=" * 70)
    print()
    print("📖 Para más información:")
    print("   • Ayuda: python scripts/sage_activation.py --help")
    print("   • Tests: pytest scripts/test_sage_activation.py -v")
    print("   • DOI: 10.5281/zenodo.17379721")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
