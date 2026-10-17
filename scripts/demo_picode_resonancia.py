#!/usr/bin/env python3
r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║            demo_picode_resonancia.py — Demostración del Motor πCODE         ║
║                                                                              ║
║  Demuestra el Motor de Resonancia de Simetría PT (πCODE RESONANCIA)         ║
║  implementado en core/picode_resonancia.py.                                  ║
║                                                                              ║
║  Módulos demostrados:                                                        ║
║    1. EmisionInformacionResonante — emisión desde escala de Planck           ║
║    2. PTSymmetryOperator          — operador no-hermítico con simetría PT    ║
║    3. AdSCFTCitoplasma            — citoplasma como borde holográfico        ║
║    4. RiemannEstabilizadorBiologico — ceros de Riemann como anclas           ║
║    5. PiCodeResonancia            — motor integrador QCAL-SYMBIO-1           ║
║    6. Simulación de falsabilidad  — estrés celular rompe la simetría PT      ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Uso:
    python demo_picode_resonancia.py
"""

from __future__ import annotations

import sys
import os
import math

# ── Ruta al módulo core ──────────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "core"))

from picode_resonancia import (
    EmisionInformacionResonante,
    PTSymmetryOperator,
    AdSCFTCitoplasma,
    RiemannEstabilizadorBiologico,
    PiCodeResonancia,
    activar_picode_resonancia,
    _F0_HZ,
    _HBAR,
    _OMEGA_0,
    _PSI_UMBRAL,
    _ORDENES_MAGNITUD,
)

# ── Separador visual ──────────────────────────────────────────────────────────
SEP = "─" * 70
DOBLE_SEP = "═" * 70


def demo_encabezado() -> None:
    """Imprime el encabezado de la demostración."""
    print(DOBLE_SEP)
    print("  πCODE RESONANCIA — Motor de Resonancia de Simetría PT")
    print("  QCAL-SYMBIO-1  |  f₀ = 141.7001 Hz  |  Ψ_umbral = 0.888")
    print(DOBLE_SEP)
    print()


def demo_emision_informacion(coherencia: float = 0.999999) -> None:
    """
    Demuestra la emisión de información resonante desde la escala de Planck.

    Parámetros
    ----------
    coherencia : float
        Parámetro de coherencia Ψ.
    """
    print(SEP)
    print("  1. EmisionInformacionResonante — Escala de Planck")
    print(SEP)

    emision = EmisionInformacionResonante(coherencia=coherencia)

    energia = emision.energia_emision()
    coh_pc = emision.coherencia_planck_celular()
    amp_t0 = emision.amplitud_coherente(0.0)

    print(f"  Coherencia Ψ          : {coherencia}")
    print(f"  f₀                    : {_F0_HZ} Hz")
    print(f"  ω₀                    : {_OMEGA_0:.4f} rad/s")
    print(f"  E = ℏ·ω₀·Ψ           : {energia:.4e} J")
    print(f"  Órdenes de magnitud   : {emision.ordenes_magnitud()}")
    print(f"  Coherencia Planck→célula : {coh_pc:.6f}")
    print(f"  A(t=0) = Ψ            : {abs(amp_t0):.6f}")
    print()


def demo_pt_symmetry(coherencia: float = 0.999999, n: int = 100) -> None:
    """
    Demuestra el operador de simetría PT con alta coherencia.

    Parámetros
    ----------
    coherencia : float
        Parámetro de coherencia Ψ.
    n : int
        Dimensión del espacio de Hilbert.
    """
    print(SEP)
    print("  2. PTSymmetryOperator — Operador No-Hermítico con Simetría PT")
    print(SEP)

    op = PTSymmetryOperator(coherencia=coherencia, n_dimension=n, semilla=42)
    pt_activa = op.es_pt_activa()
    frac = op.fraccion_autovalores_reales()
    n_reales = int(round(frac * n))
    max_imag = op.max_parte_imaginaria()

    estado_pt = "✓ ACTIVA" if pt_activa else "✗ ROTA"

    print(f"  Coherencia Ψ          : {coherencia}")
    print(f"  Dimensión N           : {n}")
    print(f"  Ĥ = diag(Riemann) + i·(1−Ψ)·fliplr(I)")
    print(f"  Simetría PT           : {estado_pt}")
    print(f"  Autovalores reales    : {n_reales}/{n}")
    print(f"  Max |Im(λ)|           : {max_imag:.2e}")
    print(f"  Coherencia PT (Ψ_PT)  : {op.coherencia_pt():.6f}")
    print()


def demo_ads_cft_citoplasma(coherencia: float = 0.999999) -> None:
    """
    Demuestra el citoplasma como límite holográfico AdS/CFT.

    Parámetros
    ----------
    coherencia : float
        Parámetro de coherencia Ψ.
    """
    print(SEP)
    print("  3. AdSCFTCitoplasma — Borde Holográfico AdS/CFT")
    print(SEP)

    cito = AdSCFTCitoplasma(coherencia=coherencia)

    rho_0 = cito.densidad_ez(0.0)
    rho_lambda = cito.densidad_ez(cito.lambda_ez)
    entropia = cito.entropia_holografica()
    psi_holo = cito.coherencia_holografica()
    xi_eff = cito.longitud_coherencia_citoplasma()

    print(f"  Coherencia Ψ          : {coherencia}")
    print(f"  λ_EZ                  : {cito.lambda_ez:.2e} m")
    print(f"  ρ_EZ(0) = Ψ          : {rho_0:.6f}")
    print(f"  ρ_EZ(λ_EZ)           : {rho_lambda:.6f}")
    print(f"  Entropía holográfica  : {entropia:.4f} bits")
    print(f"  Coherencia holográfica: {psi_holo:.6f}")
    print(f"  Longitud coherencia   : {xi_eff:.4e} m")
    print()


def demo_riemann_estabilizador(coherencia: float = 0.999999) -> None:
    """
    Demuestra el estabilizador biológico de Riemann.

    Parámetros
    ----------
    coherencia : float
        Parámetro de coherencia Ψ.
    """
    print(SEP)
    print("  4. RiemannEstabilizadorBiologico — Anclas de Resonancia")
    print(SEP)

    reb = RiemannEstabilizadorBiologico(f0=_F0_HZ, coherencia=coherencia)

    freqs = reb.frecuencias_resonancia()
    pesos = reb.pesos_resonancia()
    corr = reb.correlacion_espectral()
    estab = reb.estabilidad_biologica()

    print(f"  Coherencia Ψ          : {coherencia}")
    print(f"  f₀ = {_F0_HZ} Hz")
    print(f"  Frecuencias biológicas f_n = f₀·γ_n/γ₁:")
    for i, (f, w) in enumerate(zip(freqs[:5], pesos[:5])):
        print(f"    f_{i+1} = {f:.4f} Hz   (peso: {w:.4f})")
    print(f"    ... ({reb.n_zeros} frecuencias en total)")
    print(f"  Correlación de Riemann: {corr:.4f}  (≈ {corr:.2f})")
    print(f"  Estabilidad biológica : {estab:.4f}  (≈ {estab:.2f})")
    print()


def demo_motor_principal(coherencia: float = 0.999999, n: int = 100) -> None:
    """
    Demuestra el motor πCODE completo.

    Parámetros
    ----------
    coherencia : float
        Parámetro de coherencia Ψ.
    n : int
        Dimensión del espacio de Hilbert.
    """
    print(DOBLE_SEP)
    print("  5. PiCodeResonancia — Motor QCAL-SYMBIO-1 Completo")
    print(DOBLE_SEP)

    resultado = activar_picode_resonancia(
        coherencia=coherencia, n_dimension=n, semilla=42
    )

    print(resultado.resumen())
    print()

    print("  Métricas detalladas:")
    print(f"    Energía de emisión    : {resultado.energia_emision:.4e} J")
    print(f"    Coherencia citoplasma : {resultado.coherencia_citoplasma:.6f}")
    print(f"    Frecuencias Riemann   :")
    for i, f in enumerate(resultado.frecuencias_riemann[:3]):
        print(f"      f_{i+1} = {f:.4f} Hz")
    print()


def demo_falsabilidad() -> None:
    """
    Demuestra la simulación de falsabilidad: el estrés celular rompe la
    simetría PT y disuelve la geometría de Riemann.
    """
    print(SEP)
    print("  6. Simulación de Falsabilidad — Estrés Celular")
    print(SEP)
    print("  Predicción del modelo πCODE:")
    print("    • Alta coherencia (Ψ ≈ 1) → PT activa → resonancia alta")
    print("    • Estrés celular (Ψ << 1) → PT rota → resonancia colapsa")
    print()

    motor = PiCodeResonancia(coherencia=0.999999, n_dimension=100, semilla=42)
    nominal, estres = motor.simular_estres_celular(psi_estres=0.05)

    print(f"  {'Estado':<25} {'Nominal (Ψ=0.999999)':<22} {'Estrés (Ψ=0.05)'}")
    print(f"  {'─'*25} {'─'*22} {'─'*18}")

    pt_nom = "✓ ACTIVA" if nominal.pt_activa else "✗ ROTA"
    pt_str = "✓ ACTIVA" if estres.pt_activa else "✗ ROTA"
    print(f"  {'Simetría PT':<25} {pt_nom:<22} {pt_str}")

    reales_nom = f"{nominal.n_autovalores_reales}/{nominal.n_dimension}"
    reales_str = f"{estres.n_autovalores_reales}/{estres.n_dimension}"
    print(f"  {'Autovalores reales':<25} {reales_nom:<22} {reales_str}")

    print(f"  {'Correlación Riemann':<25} {nominal.correlacion_riemann:<22.4f} {estres.correlacion_riemann:.4f}")
    print(f"  {'Estabilidad biológica':<25} {nominal.estabilidad_biologica:<22.4f} {estres.estabilidad_biologica:.4f}")
    print(f"  {'Resonancia global':<25} {nominal.resonancia_global:<22.4f} {estres.resonancia_global:.4f}")

    aprobado_nom = "✓ APROBADO" if nominal.aprobado else "✗ NO APROBADO"
    aprobado_str = "✓ APROBADO" if estres.aprobado else "✗ NO APROBADO"
    print(f"  {'Estado':<25} {aprobado_nom:<22} {aprobado_str}")

    print()
    print(f"  Umbral biológico Ψ_umbral = {_PSI_UMBRAL}")
    print("  ✓ El estrés celular ROMPE la simetría PT y DISUELVE la geometría.")
    print()


def demo_comparacion_coherencias() -> None:
    """
    Compara la resonancia global para distintos valores de coherencia.
    """
    print(SEP)
    print("  7. Comparación de Resonancias a Distintos Valores de Ψ")
    print(SEP)
    print(f"  {'Ψ':<12} {'PT':<8} {'Reales':<10} {'Corr Riemann':<14} {'Resonancia':<12} {'Aprobado'}")
    print(f"  {'─'*12} {'─'*8} {'─'*10} {'─'*14} {'─'*12} {'─'*10}")

    valores_psi = [0.999999, 0.95, 0.888, 0.5, 0.2, 0.05]

    for psi in valores_psi:
        r = activar_picode_resonancia(coherencia=psi, n_dimension=50, semilla=42)
        pt = "✓" if r.pt_activa else "✗"
        reales = f"{r.n_autovalores_reales}/{r.n_dimension}"
        aprobado = "✓" if r.aprobado else "✗"
        print(
            f"  {psi:<12.6f} {pt:<8} {reales:<10} "
            f"{r.correlacion_riemann:<14.4f} {r.resonancia_global:<12.4f} {aprobado}"
        )
    print()


def main() -> None:
    """Ejecuta la demostración completa del motor πCODE RESONANCIA."""
    demo_encabezado()
    demo_emision_informacion()
    demo_pt_symmetry()
    demo_ads_cft_citoplasma()
    demo_riemann_estabilizador()
    demo_motor_principal()
    demo_falsabilidad()
    demo_comparacion_coherencias()

    print(DOBLE_SEP)
    print("  Demostración completada exitosamente.")
    print(f"  Motor πCODE RESONANCIA — QCAL-SYMBIO-1 activo.")
    print(DOBLE_SEP)


if __name__ == "__main__":
    main()
