#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validación del Sistema TOPC Lagrangiano  ∴TOPC∞³
==================================================

Script de validación en cuatro fases para el módulo
physics/topc_lagrangiano.py:

  Fase 1 — Constantes físicas del sistema TOPC
  Fase 2 — Lagrangiano y campo escalar ψ
  Fase 3 — Birrefringencia y señal observable Δθ(t)
  Fase 4 — Coherencia global Ψ_global y API pública

Uso
---
    python scripts/validate_topc_lagrangiano.py

Códigos de salida
-----------------
    0 — todas las fases validadas
    1 — una o más fases fallidas

RAM: RAM-XLII-2026-TOPC-LAGRANGIANO
"""

import math
import sys
import os

# Resolución del directorio raíz del repositorio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

from physics.topc_lagrangiano import (
    # Constantes
    M_PLANCK_KG,
    M_PSI_KG,
    M_PSI_EV,
    H_PLANCK,
    ALFA_EM,
    LAMBDA_SELF,
    G_AGG,
    F_A_EV,
    OMEGA_0,
    RHO_DM_GEV_CM3,
    FRACCION_DOPPLER_SIDEREO,
    SELLO_TOPC,
    RAM_TOPC,
    # Clases
    ConstantesTopc,
    LagrangianoTopc,
    CampoEscalarPsi,
    EcuacionFoton,
    BirrefringenciaCircular,
    DesfasePolarizacion,
    CoherenciaTopc,
    SistemaTopc,
    # API
    topc_lagrangiano_activar,
)
from qcal.constants import F0_HZ, C


def separador(titulo: str) -> None:
    linea = "─" * 68
    print(f"\n{linea}")
    print(f"  {titulo}")
    print(linea)


def ok(mensaje: str) -> None:
    print(f"  ✓  {mensaje}")


def fallo(mensaje: str) -> None:
    print(f"  ✗  {mensaje}")


# ============================================================================
# FASE 1 — Constantes físicas
# ============================================================================

def fase1_constantes() -> bool:
    """Valida las constantes físicas del sistema TOPC."""
    separador("FASE 1 — Constantes físicas del sistema TOPC")
    aprobado = 0
    fallido = 0

    # V1.1 — f₀ coincide con QCAL
    try:
        c = ConstantesTopc()
        assert abs(c.f0 - F0_HZ) < 1.0e-4, f"f₀={c.f0} ≠ F0_HZ={F0_HZ}"
        ok(f"f₀ = {c.f0} Hz  (coincide con constante QCAL)")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V1.2 — m_ψ ≈ 5.86×10⁻¹³ eV
    try:
        ratio = M_PSI_EV / 5.86e-13
        assert 0.95 <= ratio <= 1.05, f"m_ψ ratio={ratio:.3f} fuera de ±5 %"
        ok(f"m_ψ = {M_PSI_EV:.3e} eV  (≈ 5.86×10⁻¹³ eV ✓)")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V1.3 — λ ≈ 4.8×10⁻⁴¹
    try:
        ratio = LAMBDA_SELF / 4.8e-41
        assert 0.9 <= ratio <= 1.1, f"λ ratio={ratio:.3f} fuera de ±10 %"
        ok(f"λ = {LAMBDA_SELF:.3e}  (≈ 4.8×10⁻⁴¹ ✓)")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V1.4 — Masa de Planck
    try:
        ratio = M_PLANCK_KG / 2.176e-8
        assert 0.99 <= ratio <= 1.01, f"M_P ratio={ratio:.4f} fuera de ±1 %"
        ok(f"M_P = {M_PLANCK_KG:.3e} kg  (≈ 2.176×10⁻⁸ kg ✓)")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V1.5 — α ≈ 1/137
    try:
        assert abs(ALFA_EM * 137.0 - 1.0) < 1.0e-3, f"α·137 = {ALFA_EM * 137.0:.6f}"
        ok(f"α = 1/{1/ALFA_EM:.3f}  ≈ 1/137 ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V1.6 — ω₀ = 2π f₀
    try:
        omega_calc = 2.0 * math.pi * F0_HZ
        assert abs(OMEGA_0 - omega_calc) < 1.0e-6, f"ω₀={OMEGA_0} ≠ 2πf₀={omega_calc}"
        ok(f"ω₀ = {OMEGA_0:.4f} rad s⁻¹  = 2π × {F0_HZ} Hz ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V1.7 — m_ψ ≪ M_P
    try:
        ratio_masas = M_PSI_KG / M_PLANCK_KG
        assert ratio_masas < 1.0e-30, f"m_ψ/M_P = {ratio_masas:.2e} (debe ser ≪ 1)"
        ok(f"m_ψ/M_P = {ratio_masas:.2e}  ≪ 1 (régimen sub-Planck ✓)")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V1.8 — Validación de parámetros inválidos
    try:
        errores_capturados = 0
        for kwargs in [
            {"f0": -1.0},
            {"f888": 0.0},
            {"rho_dm": 0.0},
            {"L_m": -100.0},
        ]:
            try:
                ConstantesTopc(**kwargs)
            except ValueError:
                errores_capturados += 1
        assert errores_capturados == 4, f"Solo {errores_capturados}/4 errores capturados"
        ok("Validación de entradas: 4/4 errores ValueError capturados ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    print(f"\n  Fase 1: {aprobado} ✓  {fallido} ✗")
    return fallido == 0


# ============================================================================
# FASE 2 — Lagrangiano y campo escalar ψ
# ============================================================================

def fase2_lagrangiano_campo() -> bool:
    """Valida las componentes del Lagrangiano y el campo escalar ψ."""
    separador("FASE 2 — Lagrangiano y campo escalar ψ")
    aprobado = 0
    fallido = 0

    lag = LagrangianoTopc()
    campo = CampoEscalarPsi()

    # V2.1 — ℒ_gravedad = 0 en espacio plano
    try:
        L_grav = lag.densidad_gravedad(0.0)
        assert L_grav == 0.0, f"ℒ_gravedad(R=0)={L_grav} ≠ 0"
        ok("ℒ_gravedad(R=0) = 0  (espacio plano ✓)")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V2.2 — ℒ_tejido con término cinético puro
    try:
        dpsi = 1.0
        L_tej = lag.densidad_tejido(0.0, 0.0, dpsi)
        assert abs(L_tej - 0.5) < 1.0e-10, f"ℒ_tejido={L_tej} ≠ 0.5"
        ok("ℒ_tejido(ψ=0, ∂_tψ=1) = 0.5  (término cinético ✓)")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V2.3 — ψ(0) = ψ₀
    try:
        psi0 = campo.constantes.psi0_ev
        psi_t0 = campo.psi(0.0)
        assert abs(psi_t0 - psi0) < psi0 * 1.0e-10, f"ψ(0)={psi_t0} ≠ ψ₀={psi0}"
        ok(f"ψ(0) = ψ₀ = {psi0:.3e} eV ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V2.4 — ψ(T/4) ≈ 0 (relativo a ψ₀; residuo es ruido numérico ∼ ε_float64 × ψ₀)
    try:
        T_cuarto = 1.0 / (4.0 * F0_HZ)
        psi_t4 = campo.psi(T_cuarto)
        psi0_val = campo.constantes.psi0_ev
        # ε_machine de float64 ≈ 2.22e-16; se usa tolerancia relajada 1e-15
        # para absorber acumulación de error en las operaciones trigonométricas
        assert abs(psi_t4) < psi0_val * 1.0e-15, \
            f"|ψ(T/4)|={abs(psi_t4):.2e} > tolerancia ({psi0_val * 1e-15:.2e})"
        ok(f"ψ(T/4) ≈ 0  (|ψ(T/4)|/ψ₀ = {abs(psi_t4)/psi0_val:.2e} ≪ 1 ✓)")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V2.5 — Conservación de energía ½ (∂_t ψ)² + ½ ω₀² ψ² = const
    try:
        omega0 = campo.constantes.omega0
        psi0 = campo.constantes.psi0_ev
        E_ref = 0.5 * psi0**2 * omega0**2
        errores_energia = []
        for t in [0.0, 0.1, 0.5, 1.0, 10.0]:
            E = campo.energia_total(t)
            err = abs(E / E_ref - 1.0)
            if err > 1.0e-8:
                errores_energia.append(f"t={t}: err={err:.2e}")
        assert not errores_energia, f"Energía no conservada: {errores_energia}"
        ok("Conservación de energía armónica: ½(∂_tψ)² + ½ω₀²ψ² = const ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V2.6 — ψ₀ ∝ √(ρ_DM)
    try:
        c1 = ConstantesTopc(rho_dm=0.3)
        c2 = ConstantesTopc(rho_dm=1.2)
        ratio = CampoEscalarPsi(c2).constantes.psi0_ev / CampoEscalarPsi(c1).constantes.psi0_ev
        esperado = math.sqrt(1.2 / 0.3)
        assert abs(ratio - esperado) < 1.0e-6, f"ψ₀ ratio={ratio:.6f} ≠ √4={esperado:.6f}"
        ok(f"ψ₀ ∝ √(ρ_DM): ratio = {ratio:.6f} = √(1.2/0.3) ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    print(f"\n  Fase 2: {aprobado} ✓  {fallido} ✗")
    return fallido == 0


# ============================================================================
# FASE 3 — Birrefringencia y señal observable Δθ(t)
# ============================================================================

def fase3_birrefringencia_señal() -> bool:
    """Valida la birrefringencia circular y la señal de polarización."""
    separador("FASE 3 — Birrefringencia y señal observable Δθ(t)")
    aprobado = 0
    fallido = 0

    c = ConstantesTopc()
    birr = BirrefringenciaCircular(c)
    dp = DesfasePolarizacion(c)
    omega_laser = 2.0 * math.pi * C / 532.0e-9   # láser verde 532 nm

    # V3.1 — n_L > n_R para ψ̇ > 0 (usando dpsi grande para superar ε_machine)
    try:
        # g_aγγ ≈ 1.84e-28 eV⁻¹; con dpsi=1e30 → delta_n ≈ 2.6e-14 (representable)
        n_L, n_R = birr.indices_refraccion(1.0e30, omega_laser)
        assert n_L > n_R, f"n_L={n_L} ≤ n_R={n_R} para ψ̇ > 0"
        ok(f"n_L={n_L:.6e} > n_R={n_R:.6e}  para ψ̇ > 0 ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V3.2 — Δn ∝ ψ̇ (proporcionalidad lineal; dpsi grande para superar ε_machine)
    try:
        dpsi = 1.0e30
        dn1 = birr.diferencia_indices(dpsi, omega_laser)
        dn2 = birr.diferencia_indices(2.0 * dpsi, omega_laser)
        ratio = dn2 / dn1
        assert abs(ratio - 2.0) < 0.01, f"Δn(2ψ̇)/Δn(ψ̇) = {ratio:.4f} ≠ 2"
        ok(f"Δn ∝ ψ̇: Δn(2ψ̇)/Δn(ψ̇) = {ratio:.4f} ≈ 2 ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V3.3 — Δθ(0) = 0
    try:
        theta0 = dp.desfase(0.0)
        assert abs(theta0) < 1.0e-40, f"Δθ(0)={theta0} ≠ 0"
        ok(f"Δθ(0) = {theta0:.2e} ≈ 0 ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V3.4 — Amplitud ∼ 10⁻¹⁹ rad (2 órdenes de magnitud)
    try:
        A = dp.amplitud()
        assert 1.0e-21 < A < 1.0e-17, f"Amplitud={A:.2e} fuera de [10⁻²¹, 10⁻¹⁷]"
        ok(f"Δθ_amp = {A:.3e} rad  (∼ 10⁻¹⁹ rad ✓)")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V3.5 — Δθ_amp ∝ L
    try:
        A1 = dp.amplitud(L=100.0e3)
        A2 = dp.amplitud(L=200.0e3)
        ratio = A2 / A1
        assert abs(ratio - 2.0) < 1.0e-9, f"A(2L)/A(L)={ratio:.10f} ≠ 2"
        ok(f"Δθ_amp ∝ L: A(200km)/A(100km) = {ratio:.10f} ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V3.6 — Fórmula de amplitud: ½ g_aγγ ψ₀ ω₀ L / c
    try:
        g_inv_eV = c.g_agg * 1.0e-9
        esperado = 0.5 * g_inv_eV * c.psi0_ev * c.omega0 * c.L_m / C
        A = dp.amplitud()
        ratio = A / esperado
        assert abs(ratio - 1.0) < 1.0e-9, f"A/esperado={ratio:.10f}"
        ok("Δθ_amp = ½ g_aγγ ψ₀ ω₀ L / c  verificado ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V3.7 — Frecuencia de señal: f₀ = 141.7001 Hz
    try:
        t_array = np.linspace(0, 10.0 / F0_HZ, 10000)
        señal = dp.serie_temporal(t_array)
        # El espectro debe tener máximo en f₀
        dt = t_array[1] - t_array[0]
        freqs = np.fft.rfftfreq(len(t_array), d=dt)
        poder = np.abs(np.fft.rfft(señal))
        f_pico = freqs[np.argmax(poder)]
        assert abs(f_pico - F0_HZ) < 1.0, f"Pico espectral en {f_pico:.2f} Hz ≠ {F0_HZ} Hz"
        ok(f"Frecuencia del pico espectral: {f_pico:.4f} Hz  ≈ f₀ = {F0_HZ} Hz ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V3.8 — Modulación Doppler sidéreo
    try:
        assert 1.0e-4 < FRACCION_DOPPLER_SIDEREO < 1.0e-2, \
            f"Fracción Doppler = {FRACCION_DOPPLER_SIDEREO}"
        t = 0.5 / F0_HZ
        theta_plain = dp.desfase(t)
        theta_dopp = dp.desfase_con_doppler(t)
        A = dp.amplitud()
        assert abs(theta_dopp) <= A * (1.0 + FRACCION_DOPPLER_SIDEREO + 1.0e-9)
        ok(f"Fracción Doppler sidéreo = {FRACCION_DOPPLER_SIDEREO:.1e}  ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    print(f"\n  Fase 3: {aprobado} ✓  {fallido} ✗")
    return fallido == 0


# ============================================================================
# FASE 4 — Coherencia global y API pública
# ============================================================================

def fase4_coherencia_api() -> bool:
    """Valida la coherencia global Ψ_global y la API pública."""
    separador("FASE 4 — Coherencia global Ψ_global y API pública")
    aprobado = 0
    fallido = 0

    # V4.1 — Ψ_global ∈ [0, 1]
    try:
        coh = CoherenciaTopc()
        psi = coh.psi_global
        assert 0.0 <= psi <= 1.0, f"Ψ_global={psi} fuera de [0, 1]"
        ok(f"Ψ_global = {psi:.6f}  ∈ [0, 1] ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V4.2 — Ψ_global = 1 cuando f₀ = f₈₈₈ / n exacto
    try:
        f0_test = 888.0 / 6.0
        c = ConstantesTopc(f0=f0_test, f888=888.0)
        coh_exacta = CoherenciaTopc(c)
        psi_exacto = coh_exacta.psi_global
        assert abs(psi_exacto - 1.0) < 1.0e-10, f"Ψ_global={psi_exacto} ≠ 1"
        ok(f"Ψ_global = {psi_exacto:.10f} = 1  cuando f₀ = f₈₈₈/n ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V4.3 — Sello ∴TOPC∞³ presente en evaluación
    try:
        r = CoherenciaTopc().evaluar_coherencia()
        assert r["sello"] == SELLO_TOPC, f"sello='{r['sello']}' ≠ '{SELLO_TOPC}'"
        ok(f"Sello: {r['sello']} ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V4.4 — SistemaTopc.activar()
    try:
        sistema = SistemaTopc()
        resultado = sistema.activar()
        assert resultado["estado"] == "ACTIVADO", f"estado='{resultado['estado']}'"
        assert resultado["sello"] == SELLO_TOPC
        assert resultado["ram"] == RAM_TOPC
        ok(f"SistemaTopc.activar() → estado='{resultado['estado']}' ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V4.5 — Amplitud en orden de magnitud correcto
    try:
        sistema = SistemaTopc()
        resultado = sistema.activar()
        assert resultado["amplitud_orden_correcto"], "Amplitud fuera del orden esperado"
        A = resultado["amplitud_delta_theta_rad"]
        ok(f"Amplitud Δθ_amp = {A:.3e} rad  (orden correcto ✓)")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V4.6 — API pública topc_lagrangiano_activar()
    try:
        resultado = topc_lagrangiano_activar()
        assert isinstance(resultado, dict), "No devuelve dict"
        assert resultado["estado"] == "ACTIVADO"
        assert resultado["sello"] == SELLO_TOPC
        ok("topc_lagrangiano_activar() → estado='ACTIVADO', sello='∴TOPC∞³' ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V4.7 — Parámetros personalizados en API
    try:
        r_custom = topc_lagrangiano_activar(f0=200.0, rho_dm=0.5, L_m=50.0e3)
        assert abs(r_custom["f0_Hz"] - 200.0) < 1.0e-6
        assert abs(r_custom["L_m"] - 50.0e3) < 1.0
        ok("API con parámetros personalizados (f₀=200 Hz, L=50 km) ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    # V4.8 — RAM correcto
    try:
        assert RAM_TOPC.startswith("RAM-XLII"), f"RAM='{RAM_TOPC}'"
        ok(f"RAM: {RAM_TOPC} ✓")
        aprobado += 1
    except AssertionError as e:
        fallo(str(e))
        fallido += 1

    print(f"\n  Fase 4: {aprobado} ✓  {fallido} ✗")
    return fallido == 0


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    print("=" * 68)
    print("  VALIDACIÓN — TOPC LAGRANGIANO  ∴TOPC∞³")
    print(f"  f₀ = {F0_HZ} Hz  |  f₈₈₈ = 888 Hz")
    print(f"  {RAM_TOPC}")
    print("=" * 68)

    fases = [
        ("Fase 1 — Constantes físicas", fase1_constantes),
        ("Fase 2 — Lagrangiano y campo ψ", fase2_lagrangiano_campo),
        ("Fase 3 — Birrefringencia y señal", fase3_birrefringencia_señal),
        ("Fase 4 — Coherencia y API", fase4_coherencia_api),
    ]

    resultados = []
    for nombre, funcion in fases:
        ok_fase = funcion()
        resultados.append(ok_fase)

    separador("RESUMEN FINAL")
    total = len(fases)
    aprobadas = sum(resultados)
    fallidas = total - aprobadas

    for i, (nombre, _) in enumerate(fases):
        estado = "✓  APROBADA" if resultados[i] else "✗  FALLIDA"
        print(f"  {estado} — {nombre}")

    print()
    if fallidas == 0:
        print(f"  🎯  TODAS LAS FASES APROBADAS ({aprobadas}/{total})")
        print(f"  {SELLO_TOPC}  Sistema TOPC Lagrangiano VALIDADO")
        return 0
    else:
        print(f"  ⚠   {fallidas}/{total} FASES FALLIDAS")
        return 1


if __name__ == "__main__":
    sys.exit(main())
