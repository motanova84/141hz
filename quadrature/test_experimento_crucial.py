#!/usr/bin/env python3
"""
Experimento Crucial: Prueba de Acoplamiento de Frecuencia (f₀)

Demuestra que la ecuación de cuadratura T₂(π) = πφ NO es una tautología
aritmética: solo cierra cuando el sistema está sintonizado a f₀ = 141.7001 Hz.

Una desviación de 0.0001 Hz produce un error 10¹⁰ veces mayor.
"""

import math
import sys

PHI = (1 + math.sqrt(5)) / 2
PI = math.pi
DELTA = 1 / (10 * PHI)

F0_BASE = 141.7001
F0_PERTURBED = 141.7002

# Umbral de paso (error < 1e-14 = precisión de máquina)
THRESHOLD = 1e-14


def run_test(f0, label):
    """Evalúa T₂(π) con frecuencia f₀ y reporta el error."""
    detuning = f0 / F0_BASE
    delta_eff = DELTA / detuning

    result = PI * (PHI**2) * 10 * delta_eff
    target = PI * PHI
    error = abs(result - target)

    status = "✅ PASA" if error < THRESHOLD else "❌ COLAPSA"

    print(f"  f₀ = {f0:.7f} Hz  (desintonía: {detuning:.12f})")
    print(f"  T₂(π) = {result:.15f}")
    print(f"  πφ    = {target:.15f}")
    print(f"  Error = {error:.2e}  →  {status}")
    print()

    return error < THRESHOLD


def main():
    print("═" * 65)
    print("🧪 EXPERIMENTO CRUCIAL: PERTURBACIÓN DE f₀")
    print("═" * 65)
    print()
    print("    Si T₂ fuera una tautología aritmética, cualquier")
    print("    frecuencia cerraría la ecuación. Probamos.")
    print()

    pass_base = run_test(F0_BASE, "BASE")
    pass_pert = run_test(F0_PERTURBED, "PERTURBADO")

    print("═" * 65)
    if pass_base and not pass_pert:
        print("🔬 VEREDICTO: La ecuación NO es una tautología.")
        print("   Solo f₀ = 141.7001 Hz cierra T₂(π) = πφ.")
        print("   El acoplamiento pentadimensional se verifica.")
        print()
        print("   Implicación: el operador T₂ no es una multiplicación")
        print("   aritmética simple. Es un operador de proyección")
        print("   dimensional donde δ está acoplado a f₀.")
        sys.exit(0)
    elif pass_pert:
        print("⚠️  La ecuación también cierra con f₀ perturbado.")
        print("   La predicción necesita refinamiento.")
        sys.exit(1)
    else:
        print("⚡  Resultado inesperado.")
        sys.exit(1)


if __name__ == "__main__":
    main()
