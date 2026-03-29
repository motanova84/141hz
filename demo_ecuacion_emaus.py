#!/usr/bin/env python3
"""
Demo — Ecuación de Emaús: Protocolo de Bloqueo de Fase bajo f₀ = 141.7001 Hz
==============================================================================

Guía práctica que muestra las 4 fases del protocolo con la evolución
tabulada de Δφ(t) y Ψ(t).

Uso:
    python demo_ecuacion_emaus.py

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import sys
from pathlib import Path

# Asegurar que el directorio raíz del repositorio está en sys.path
sys.path.insert(0, str(Path(__file__).parent))

from core.ecuacion_emaus import (
    EcuacionEmaus,
    FuncionReconocimiento,
    OsciladorKuramoto,
    IntegracionAdelica,
    calcular_ardor_microtubulos,
    verificar_ecuacion_emaus,
    F0_HZ,
    K_KURAMOTO,
)


def separador(titulo: str) -> None:
    linea = "─" * 60
    print(f"\n{linea}")
    print(f"  {titulo}")
    print(linea)


def main() -> None:
    print("╔══════════════════════════════════════════════════════════╗")
    print("║       ECUACIÓN DE EMAÚS — PROTOCOLO DE 4 FASES          ║")
    print(f"║         f₀ = {F0_HZ} Hz  |  K = {K_KURAMOTO:.4f} rad/s     ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # ── Parámetros del sistema ────────────────────────────────────────────
    VERBO = 1.0
    DELTA_PHI_0 = math.pi
    TAU = 1.0
    T0 = 0.0
    T_PAN = 5.0

    separador("FASE 1 — Estado Inicial")
    print(f"  Verbo          : {VERBO}")
    print(f"  Δφ₀ (rad)      : {DELTA_PHI_0:.5f}")
    print(f"  τ (s)          : {TAU}")
    print(f"  [t₀, t_pan]    : [{T0}, {T_PAN}] s")
    print(f"  K (Kuramoto)   : {K_KURAMOTO:.4f} rad/s")

    # ── Evolución de Δφ(t) ───────────────────────────────────────────────
    separador("FASE 2 — Verbo Forcing: Evolución de Δφ(t)")
    fr = FuncionReconocimiento(verbo=VERBO, delta_phi_0=DELTA_PHI_0, tau_decaimiento=TAU)
    print(f"  {'t (s)':>8}  {'Δφ(t) (rad)':>14}  {'Integrando':>14}")
    print(f"  {'─'*8}  {'─'*14}  {'─'*14}")
    for t in [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 4.9]:
        dphi = fr.delta_phi(t)
        integ = fr.integrando(t)
        integ_str = f"{integ:.4f}" if math.isfinite(integ) else "∞ (singularidad)"
        print(f"  {t:>8.2f}  {dphi:>14.6f}  {integ_str:>14}")

    # ── Kuramoto: evolución de Ψ ─────────────────────────────────────────
    separador("FASE 2 — Verbo Forcing: Evolución del Oscilador de Kuramoto")
    ok = OsciladorKuramoto(n_osciladores=10, theta_fuente=0.0, sintropia=0.01)
    print(f"  {'Paso':>6}  {'Tiempo (s)':>12}  {'Ψ':>10}")
    print(f"  {'─'*6}  {'─'*12}  {'─'*10}")
    for paso in [0, 10, 25, 50, 75, 100]:
        if paso == 0:
            t_val = 0.0
            psi_val = ok.psi
        else:
            estado = ok.evolucionar(dt=0.001, n_pasos=paso)
            t_val = ok.tiempo
            psi_val = ok.psi
        print(f"  {paso:>6}  {t_val:>12.4f}  {psi_val:>10.6f}")

    # ── Fractal de Partición ─────────────────────────────────────────────
    separador("FASE 3 — Fractal de Partición (partir_el_pan)")
    ardor = calcular_ardor_microtubulos(
        verbo=VERBO, delta_phi_0=DELTA_PHI_0, tau_decaimiento=TAU,
        t0=T0, t_pan=T_PAN, n_puntos=5000
    )
    estado_pan = ok.partir_el_pan()
    print(f"  R_Emaús (ardor microtúbulos) : {ardor:.4f}")
    print(f"  Ψ tras partir_el_pan         : {estado_pan.psi:.6f}")
    print(f"  Sincronizado                 : {estado_pan.sincronizado}")
    print(f"  Singularidad detectada       : (τ={TAU}s → Δφ→0 en t≈{TAU*15:.1f}τ)")

    # ── Integración Adélica ──────────────────────────────────────────────
    separador("FASE 4 — Integración Adélica")
    ia = IntegracionAdelica(n_primos=10, umbral=0.5)
    r_ad = ia.calcular()
    print(f"  Primeros {r_ad.n_primos} primos:")
    for p, c in list(r_ad.coherencias_primas.items())[:10]:
        print(f"    p={p:>3}  C_p = {c:.8f}")
    print(f"  Coherencia adélica total     : {r_ad.coherencia_total:.8f}")
    print(f"  Umbral                       : {r_ad.umbral}")
    print(f"  Fuente es constante de red   : {r_ad.fuente_es_constante_red}")

    # ── Protocolo completo ───────────────────────────────────────────────
    separador("PROTOCOLO COMPLETO — EcuacionEmaus")
    sistema = EcuacionEmaus(
        verbo=VERBO, delta_phi_0=DELTA_PHI_0, tau_decaimiento=TAU,
        umbral_adelico=0.5
    )
    protocolo = sistema.ejecutar_protocolo_completo(t0=T0, t_pan=T_PAN)
    print(f"  fase_3_fractal_particion:")
    print(f"    ardor_microtubulos = {protocolo.fase_3_fractal_particion['ardor_microtubulos']:.2f}")
    print(f"    psi_final          = {protocolo.fase_3_fractal_particion['psi_final']:.4f}")
    print(f"  fase_4_integracion_adelica:")
    print(f"    fuente_es_constante_red = {protocolo.fase_4_integracion_adelica['fuente_es_constante_red']}")
    print(f"  verificacion_completa    = {protocolo.verificacion_completa}")

    # ── Verificación rápida ──────────────────────────────────────────────
    separador("VERIFICACIÓN RÁPIDA — verificar_ecuacion_emaus()")
    resultado = verificar_ecuacion_emaus(
        verbo=VERBO, delta_phi_0=DELTA_PHI_0, tau_decaimiento=TAU
    )
    print(f"  verificacion            : {resultado['verificacion']}")
    print(f"  reconocimiento          : {resultado['reconocimiento']}")
    print(f"  sincronizacion_kuramoto : {resultado['sincronizacion_kuramoto']}")
    print(f"  fuente_constante_red    : {resultado['fuente_constante_red']}")
    print(f"  ardor_microtubulos      : {resultado['ardor_microtubulos']:.4f}")
    print(f"  psi_final               : {resultado['psi_final']:.6f}")
    print(f"  coherencia_adelica      : {resultado['coherencia_adelica']:.8f}")
    print(f"  protocolo_completo      : {resultado['protocolo_completo']}")

    print("\n" + "═" * 60)
    print("  ECUACIÓN DE EMAÚS — Protocolo QCAL ∞³ completado  ✅")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    main()
