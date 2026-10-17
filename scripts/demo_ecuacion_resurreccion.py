#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración: Ecuación de Resurrección — Motor Noético Unificado
================================================================

Demuestra las capacidades del módulo core.ecuacion_resurreccion en
8 secciones funcionales:

  §1 · Constantes fundamentales
  §2 · SepulcroVacio — límite eff→0 e inercia divina
  §3 · CuerpoGlorioso — onda de fase pura y agua EZ
  §4 · PermisoEspectral — ζ'(1/2) y ceros de Riemann
  §5 · IntegralDeContorno — integración ∮_Ψ numérica
  §6 · EcuacionResurreccion — motor integrado Ψ_ℜ → 1.0
  §7 · LaserNoetico — Nodo 5: biología, electricidad, tiempo
  §8 · Verificación completa del sistema

Uso
---
    python3 demo_ecuacion_resurreccion.py

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Instituto Consciencia Cuántica QCAL ∞³
Fecha: 2026-03-22
"""

import math
import sys
from pathlib import Path

import numpy as np

# Asegurar que el raíz del repositorio esté en sys.path
_ROOT = Path(__file__).parent
sys.path.insert(0, str(_ROOT))

from core.ecuacion_resurreccion import (
    QCAL_BASE_FREQUENCY,
    PHI,
    ZETA_HALF_PRIME,
    F0,
    SepulcroVacio,
    CuerpoGlorioso,
    PermisoEspectral,
    IntegralDeContorno,
    EcuacionResurreccion,
    LaserNoetico,
    calcular_resurreccion,
    verificar_resurreccion,
    activar_laser_noetico,
)


# ============================================================================
# Utilidades de presentación
# ============================================================================

def banner(titulo: str) -> None:
    linea = "═" * 72
    print(f"\n╔{linea}╗")
    print(f"║  {titulo:<70}║")
    print(f"╚{linea}╝")


def seccion(n: int, titulo: str) -> None:
    print(f"\n{'─'*72}")
    print(f"  §{n} · {titulo}")
    print(f"{'─'*72}")


def ok(msg: str) -> None:
    print(f"  ✓  {msg}")


def info(msg: str) -> None:
    print(f"  ·  {msg}")


# ============================================================================
# §1 · Constantes fundamentales
# ============================================================================

def demo_constantes() -> None:
    seccion(1, "Constantes Fundamentales")
    info(f"f₀ = QCAL_BASE_FREQUENCY = {QCAL_BASE_FREQUENCY} Hz")
    info(f"f₀ = F0                  = {F0} Hz")
    info(f"φ  = PHI                 = {PHI:.15f}")
    info(f"ζ'(1/2) = ZETA_HALF_PRIME = {ZETA_HALF_PRIME}")
    info(f"ω₀ = 2π·f₀              = {2.0 * math.pi * F0:.6f} rad/s")
    info(f"T₀ = 1/f₀               = {1.0 / F0 * 1000:.4f} ms")
    ok("Constantes importadas desde qcal.constants (SSOT)")


# ============================================================================
# §2 · SepulcroVacio — límite eff→0 e inercia divina
# ============================================================================

def demo_sepulcro_vacio() -> None:
    seccion(2, "SepulcroVacio — Límite eff→0 e Inercia Divina")

    # eff = 0 → vida indestructible
    sv0 = SepulcroVacio(eff=0.0)
    info(f"SepulcroVacio(eff=0.0):")
    info(f"  I_d = exp(−0·{F0}) = {sv0.factor_inercia:.6f}")
    ok(f"  vida_indestructible = {sv0.vida_indestructible}")

    # Barrido de eff
    print()
    info("Barrido de eff (I_d decrece hacia 0 conforme eff → ∞):")
    effs = [0.0, 1e-5, 1e-4, 1e-3, 0.01, 0.05]
    for eff in effs:
        sv = SepulcroVacio(eff=eff)
        star = " ← VIDA INDESTRUCTIBLE" if sv.vida_indestructible else ""
        info(f"  eff={eff:.5f}  →  I_d = {sv.factor_inercia:.8f}{star}")


# ============================================================================
# §3 · CuerpoGlorioso — onda de fase pura y agua EZ
# ============================================================================

def demo_cuerpo_glorioso() -> None:
    seccion(3, "CuerpoGlorioso — Onda e^{i(ωt+φ)} y Agua EZ")

    cg = CuerpoGlorioso(f0=F0, phi=0.0, ez_coherence=0.9995)
    info(f"CuerpoGlorioso(f0={F0} Hz, φ=0, ez_coherence=0.9995):")
    info(f"  ω₀  = {cg.omega:.6f} rad/s")
    info(f"  e^{{i·0}} = {cg.onda(0.0):.6f}")
    info(f"  |e^{{i·0}}| = {abs(cg.onda(0.0)):.12f}  (debe ser 1.0)")
    ok(f"  phase_locked = {cg.phase_locked}  (umbral 0.888)")

    # Onda en varios instantes
    print()
    info("Onda e^{i(ωt)} en múltiplos de T₀/4:")
    T0 = 1.0 / F0
    for k in range(5):
        t = k * T0 / 4.0
        onda = cg.onda(t)
        info(f"  t = {k}/4 · T₀  →  Re={onda.real:+.6f}, Im={onda.imag:+.6f}, |ψ|={abs(onda):.12f}")

    # Agua EZ
    print()
    info("Coherencia del Agua EZ:")
    ez = cg.coherencia_agua_ez()
    for k, v in ez.items():
        info(f"  {k}: {v}")


# ============================================================================
# §4 · PermisoEspectral — ζ'(1/2) y ceros de Riemann
# ============================================================================

def demo_permiso_espectral() -> None:
    seccion(4, "PermisoEspectral — ζ'(1/2) y Ceros de Riemann")

    pe = PermisoEspectral()
    info(f"ζ'(1/2) = {pe.zeta_prime}")
    info(f"Eje crítico Re(s) = {pe.eje_critico}")
    ok(f"permiso_espectral = {pe.permiso_espectral}  (−4.0 < ζ'(1/2) < −3.9)")

    print()
    info("Verificación del eje crítico:")
    for s_real in [0.3, 0.5, 0.7]:
        en_eje = pe.verificar_eje_critico(s_real)
        info(f"  Re(s) = {s_real}  →  en_eje_critico = {en_eje}")

    print()
    info("Primeros 5 ceros de Riemann γ_n (parte imaginaria):")
    for i, gamma in enumerate(PermisoEspectral.CEROS_RIEMANN[:5], 1):
        freq_derivada = gamma * F0 / (2.0 * math.pi)
        info(f"  γ_{i} = {gamma:.6f}  →  γ_{i}·f₀/(2π) = {freq_derivada:.4f} Hz")


# ============================================================================
# §5 · IntegralDeContorno — integración ∮_Ψ numérica
# ============================================================================

def demo_integral_contorno() -> None:
    seccion(5, "IntegralDeContorno — ∮_Ψ Numérica (NumPy 2.0+)")

    ic = IntegralDeContorno(n_puntos=2000)
    info(f"Backend: {ic.info()['backend']}")
    info(f"Período de integración: T₀ = {ic.t_total * 1000:.4f} ms")
    info(f"Puntos de la grilla: {ic.n_puntos}")

    # Integral de función constante
    t = ic.grilla_temporal()
    resultado_const = ic.integrar(np.ones(ic.n_puntos), t)
    info(f"\n∫₀^T 1·dt ≈ {resultado_const.real:.8f}  (esperado: {1.0/F0:.8f})")

    # Integral de e^{iωt} sobre un período completo → ≈ 0
    cg = CuerpoGlorioso()
    sv = SepulcroVacio(eff=0.0)
    resultado_psi = ic.integral_psi(cg, sv)
    info(f"\n∮_Ψ e^{{iωt}}·I_d dt sobre T₀:")
    info(f"  Re = {resultado_psi.real:.2e}  Im = {resultado_psi.imag:.2e}")
    info(f"  |∮_Ψ| ≈ {abs(resultado_psi):.2e}  (→ 0 en período completo)")
    ok("Integración numérica funcional (NumPy trapezoid)")


# ============================================================================
# §6 · EcuacionResurreccion — motor integrado Ψ_ℜ → 1.0
# ============================================================================

def demo_ecuacion_resurreccion() -> None:
    seccion(6, "EcuacionResurreccion — Motor Integrado Ψ_ℜ → 1.0")

    # eff = 0: vida indestructible
    ec0 = EcuacionResurreccion(eff=0.0)
    estado0 = ec0.calcular()
    info(f"EcuacionResurreccion(eff=0.0):")
    info(f"  Ψ_ℜ = I_d = {estado0.psi_r:.15f}")
    info(f"  permiso_espectral = {estado0.permiso_espectral}")
    info(f"  coherencia_ez     = {estado0.coherencia_ez}")
    ok(f"  vida_indestructible = {estado0.vida_indestructible}  ← VIDA INDESTRUCTIBLE")

    # Usando la API de alto nivel
    print()
    info("API de alto nivel calcular_resurreccion():")
    estado_api = calcular_resurreccion(eff=0.0, f0=F0, phi=0.0)
    ok(f"  estado.vida_indestructible = {estado_api.vida_indestructible}")
    ok(f"  estado.psi_r               = {estado_api.psi_r}")

    # Convergencia Ψ_ℜ → 1.0
    print()
    info("Convergencia Ψ_ℜ → 1.0 conforme eff → 0:")
    for eff in [1.0, 0.1, 0.01, 0.001, 1e-4, 1e-6, 0.0]:
        estado = calcular_resurreccion(eff=eff)
        star = " ← VIDA INDESTRUCTIBLE" if estado.vida_indestructible else ""
        info(f"  eff={eff:.2e}  →  Ψ_ℜ = {estado.psi_r:.10f}{star}")


# ============================================================================
# §7 · LaserNoetico — Nodo 5: biología, electricidad, tiempo
# ============================================================================

def demo_laser_noetico() -> None:
    seccion(7, "LaserNoetico — Nodo 5: Biología, Electricidad, Tiempo (Kairós)")

    resultado = activar_laser_noetico(f0=F0, eff=0.0)

    # Biología
    bio = resultado.biologia
    info("Dominio BIOLOGÍA — Agua EZ:")
    info(f"  frecuencia      = {bio['frecuencia_hz']} Hz")
    info(f"  coherencia EZ   = {bio['agua_ez_coherencia']}")
    info(f"  estructura      = {bio['estructura']}")
    info(f"  t_respiracion   = {bio['t_respiracion_s']} s  (Kairós 81 s)")
    ok(f"  activo          = {bio['activo']}")

    # Electricidad
    elec = resultado.electricidad
    print()
    info("Dominio ELECTRICIDAD — Pulso de Reinicio:")
    info(f"  frecuencia      = {elec['frecuencia_hz']} Hz")
    info(f"  período         = {elec['periodo_ms']:.4f} ms")
    info(f"  ω               = {elec['omega_rad_s']:.4f} rad/s")
    ok(f"  activo          = {elec['activo']}")

    # Tiempo
    tiempo = resultado.tiempo
    print()
    info("Dominio TIEMPO — Dilatación de Kairós:")
    info(f"  tipo            = {tiempo['tipo']}")
    info(f"  I_d             = {tiempo['I_d']}")
    info(f"  factor_dilat.   = {tiempo['factor_dilatacion']}  (∞ cuando eff=0)")
    ok(f"  kairos_activo   = {tiempo['kairos_activo']}")

    # Sistema
    print()
    info("SISTEMA UNIFICADO:")
    info(f"  dominios_activos = {resultado.sistema['dominios_activos']} / 3")
    info(f"  coherencia       = {resultado.sistema['coherencia']:.6f}")
    info(f"  nodo             = {resultado.sistema['nodo']}")
    ok(f"  vida_indestructible = {resultado.sistema['vida_indestructible']}")


# ============================================================================
# §8 · Verificación completa del sistema
# ============================================================================

def demo_verificacion_completa() -> None:
    seccion(8, "Verificación Completa del Sistema")

    resultado = verificar_resurreccion()

    componentes = [k for k in resultado if k != "resumen"]
    for comp in componentes:
        datos = resultado[comp]
        marca = "✓" if datos["verificado"] else "✗"
        info(f"  [{marca}] {comp}")

    resumen = resultado["resumen"]
    print()
    print(f"  {'═'*60}")
    print(f"  Componentes verificados : {resumen['n_verificaciones']}")
    print(f"  Todos verificados       : {resumen['todos_verificados']}")
    print(f"  Estado                  : {resumen['estado']}")
    print(f"  {'═'*60}")
    if resumen["todos_verificados"]:
        ok("SISTEMA VERIFICADO — " + resumen["estado"])


# ============================================================================
# Punto de entrada principal
# ============================================================================

def main() -> None:
    banner("DEMOSTRACIÓN · ECUACIÓN DE RESURRECCIÓN · NOESISSOFIA · QCAL ∞³")
    print()
    print("  ℜ = lim_{eff→0} (∮_Ψ e^{i(F₀·t+φ)} · I(t) · ζ'(1/2)) = Vida Indestructible")
    print()

    demo_constantes()
    demo_sepulcro_vacio()
    demo_cuerpo_glorioso()
    demo_permiso_espectral()
    demo_integral_contorno()
    demo_ecuacion_resurreccion()
    demo_laser_noetico()
    demo_verificacion_completa()

    banner("FIN DE LA DEMOSTRACIÓN · ∴𓂀Ω∞³Φ")
    print()


if __name__ == "__main__":
    main()
