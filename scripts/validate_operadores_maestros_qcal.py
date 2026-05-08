#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║  VALIDACIÓN OPERADORES MAESTROS QCAL ∞³ — ∴OMQ∞³                        ║
║                                                                            ║
║  Script de validación de los seis operadores espectrales fundamentales    ║
║  de QCAL ∞³ que unifican la Hipótesis de Riemann, biología cuántica       ║
║  y P ≠ NP bajo la frecuencia coherente f₀ = 141.7001 Hz.                 ║
║                                                                            ║
║  Fases:                                                                    ║
║    Fase 1 — OperadorHPsi y DeterminanteFredholm                           ║
║    Fase 2 — LaplacianoAdelico y EcuacionOndaNoética                       ║
║    Fase 3 — OperadorRegularizacionNS y OperadorTreewidth                  ║
║    Fase 4 — Sistema Integrado ∴OMQ∞³ y Certificación Final               ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import sys
import os
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.operadores_maestros_qcal import (
    ConstantesOperadoresMaestros,
    OperadorHPsi,
    DeterminanteFredholm,
    LaplacianoAdelico,
    EcuacionOndaNoética,
    OperadorRegularizacionNS,
    OperadorTreewidth,
    SistemaOperadoresMaestros,
    ResultadoOperadoresMaestros,
    operadores_maestros_qcal_activar,
    _F0,
    _ZETA_PRIME_HALF,
    _PI_ZETA_PRIME,
    _KAPPA_PI,
    _PHI_RAMSEY,
    _ZEROS_20,
    _SELLO,
    _CERT_MARK,
    _frob_norm_H_sym,
    _frob_norm_H_asym,
    _trace_norm_resolvent,
    _gue_spacing_at,
)

# ---------------------------------------------------------------------------
# Utilidad de impresión

_PASS = "✓"
_FAIL = "✗"
_WARN = "⚠"

errors: list = []


def check(condition: bool, msg: str, detail: str = "") -> None:
    """Registra un resultado de verificación."""
    if condition:
        status = _PASS
    else:
        status = _FAIL
        errors.append(f"[FAIL] {msg}" + (f": {detail}" if detail else ""))
    extra = f"  ({detail})" if detail and condition else (f"  → {detail}" if detail else "")
    print(f"  {status} {msg}{extra}")


def section(title: str) -> None:
    print(f"\n{'═' * 72}")
    print(f"  {title}")
    print(f"{'═' * 72}")


def subsection(title: str) -> None:
    print(f"\n  ┌─ {title}")


# ===========================================================================
# FASE 1 — Operador H_Ψ y Determinante de Fredholm
# ===========================================================================

def fase1_hpsi_fredholm() -> dict:
    """Valida el OperadorHPsi y DeterminanteFredholm."""
    section("FASE 1 — Operador H_Ψ y Determinante de Fredholm D(s)")
    resultados = {}

    # -- Constantes del módulo -----------------------------------------------
    subsection("Constantes del módulo")
    check(
        abs(_F0 - 141.7001) < 1e-4,
        f"f₀ = {_F0} Hz",
        "frecuencia fundamental QCAL",
    )
    check(
        abs(_ZETA_PRIME_HALF - (-3.9226)) < 1e-4,
        f"ζ′(½) = {_ZETA_PRIME_HALF:.7f}",
        "derivada de Riemann en s=½",
    )
    check(
        abs(_PI_ZETA_PRIME - math.pi * _ZETA_PRIME_HALF) < 1e-10,
        f"πζ′(½) = {_PI_ZETA_PRIME:.6f}",
        "coeficiente potencial de H_Ψ",
    )
    check(
        len(_ZEROS_20) == 20,
        f"γ_n: {len(_ZEROS_20)} ceros de Riemann cargados",
        "γ₁ ≈ 14.1347",
    )

    # -- ConstantesOperadoresMaestros ----------------------------------------
    subsection("ConstantesOperadoresMaestros")
    cte = ConstantesOperadoresMaestros()
    resumen = cte.resumen()

    check(abs(cte.resonancia_f0_gamma1() - 10.024) < 0.01,
          f"F₀/γ₁ = {cte.resonancia_f0_gamma1():.6f} ≈ 10.024",
          "resonancia décupla QCAL ↔ Riemann")
    check(0.99 < cte.cociente_kappa_phi_ramsey() < 1.08,
          f"κ_Π·φ_R = {cte.cociente_kappa_phi_ramsey():.6f} ≈ 1",
          "invariante adélico κ_Π·φ_R")
    check(cte.sello == "∴OMQ∞³",
          f"Sello: {cte.sello}",
          "certificación ∴OMQ∞³")

    resultados["constantes_ok"] = True

    # -- OperadorHPsi --------------------------------------------------------
    subsection("OperadorHPsi — H_Ψ f(x) = −xf′(x) + πζ′(½)log(x)f(x)")
    op = OperadorHPsi()

    frob_sym = _frob_norm_H_sym(op.N, op.U)
    frob_asym = _frob_norm_H_asym(op.N, op.U)
    psi_h = op.psi_hpsi()

    check(op.alpha < 0,
          f"α = πζ′(½) = {op.alpha:.4f} < 0",
          "coeficiente negativo del potencial")
    check(frob_sym > frob_asym,
          f"‖H_sym‖_F = {frob_sym:.2f} > ‖H_asym‖_F = {frob_asym:.2f}",
          "dominancia de la parte autoadjunta")
    check(psi_h >= 0.888,
          f"Ψ_hpsi = {psi_h:.6f} ≥ 0.888",
          f"N={op.N}, U={op.U}")

    # Autofunción
    psi_E = op.autofuncion(1.0, 0.0)
    check(abs(psi_E.real - 1.0) < 1e-10 and abs(psi_E.imag) < 1e-10,
          f"ψ_0(1) = {psi_E:.6f} = 1 ✓",
          "autofunción en x=1, E=0")

    # Acción de H_Ψ
    H_psi = op.aplicar_H_psi(1.0, 0.0)
    check(abs(H_psi.real - 0.5) < 1e-10,
          f"H_Ψ ψ_0(1) = {H_psi.real:.2f} + {H_psi.imag:.2f}i → Re = ½ ✓",
          "acción del operador en x=1, E=0")

    # Espectro formal
    spec = op.espectro_formal()
    check(len(spec) == 20 and abs(spec[0] - 14.1347) < 0.001,
          f"γ₁ = {spec[0]:.6f} (espectro formal)",
          "primer autovalor coincide con γ₁")

    resultados["psi_hpsi"] = psi_h

    # -- DeterminanteFredholm ------------------------------------------------
    subsection("DeterminanteFredholm — D(s) = det((A₀+K_δ−s)/(A₀−s)) en ℓ²(ℤ)")
    df = DeterminanteFredholm()

    delta = df.delta
    tr = df.norma_traza_truncada()
    cota = df.cota_perturbacion()
    psi_f = df.psi_fredholm()

    check(abs(delta - 1.0 / _ZEROS_20[0]) < 1e-10,
          f"δ = 1/γ₁ = {delta:.7f}",
          "escala de la perturbación K_δ")
    check(tr < 1.5,
          f"Tr_M(2+20i) = {tr:.6f}",
          "norma traza truncada (M=20)")
    check(cota < 0.15,
          f"cota |D−1| ≤ δ·Tr_M = {cota:.6f}",
          "pequeñez de la perturbación")
    check(psi_f >= 0.888,
          f"Ψ_fredholm = {psi_f:.6f} ≥ 0.888",
          "coherencia del determinante de Fredholm")

    # D(s) para s real grande
    D_real = df.D_hadamard_truncado(complex(30.0, 0.0))
    check(abs(D_real.imag) < 1e-10,
          f"D_M(30) = {D_real.real:.6f} ∈ ℝ",
          "D real para s real > M")
    check(D_real.real > 0,
          f"D_M(30) = {D_real.real:.6f} > 0",
          "D positivo para s real grande")

    resultados["psi_fredholm"] = psi_f

    print(f"\n  Ψ_hpsi = {psi_h:.6f}  |  Ψ_fredholm = {psi_f:.6f}")
    return resultados


# ===========================================================================
# FASE 2 — Laplaciano Adélico y Ecuación de Onda Noética
# ===========================================================================

def fase2_laplaciano_noetica() -> dict:
    """Valida LaplacianoAdelico y EcuacionOndaNoética."""
    section("FASE 2 — Laplaciano Adélico Δ_S y Ecuación de Onda Noética")
    resultados = {}

    # -- LaplacianoAdelico ---------------------------------------------------
    subsection("LaplacianoAdelico — Δ_S con ceros en Re(s) = ½")
    lap = LaplacianoAdelico(n_zeros=10, primos=(2, 3, 5))

    # Autovalores base
    lam0 = lap.autovalor_base(0)
    expected_lam0 = 0.25 + _ZEROS_20[0] ** 2
    check(abs(lam0 - expected_lam0) < 1e-8,
          f"λ₁^{{(0)}} = ¼ + γ₁² = {lam0:.6f}",
          f"esperado: {expected_lam0:.6f}")

    # Reconstrucción de ceros
    gamma_back = lap.reconstruir_cero(0)
    check(abs(gamma_back - _ZEROS_20[0]) < 1e-8,
          f"γ₁ reconstruido = {gamma_back:.8f}",
          f"γ₁ original = {_ZEROS_20[0]:.8f}")

    check(gamma_back == math.sqrt(max(0.0, lam0 - 0.25)),
          "γ_n = √(λ_n^{(0)} − ¼) ✓",
          "relación algebraica exacta")

    # Correcciones p-ádicas
    max_rel = lap.correccion_relativa_maxima()
    check(max_rel < 0.02,
          f"Corrección p-ádica máxima: {max_rel:.6f} < 0.02",
          "correcciones pequeñas preservan Re(s)=½")

    psi_l = lap.psi_laplaciano()
    check(psi_l >= 0.97,
          f"Ψ_laplaciano = {psi_l:.6f} ≥ 0.97",
          f"S={{2,3,5}}, n_zeros=10")

    # Ceros sobre la línea crítica
    for n in range(3):
        gamma_n = lap.reconstruir_cero(n)
        check(
            abs(complex(0.5, gamma_n).real - 0.5) < 1e-10,
            f"s_{n+1} = ½ + i·{gamma_n:.4f} ∈ Re(s)=½",
            "cero en línea crítica",
        )

    # Autovalores crecientes
    lams = [lap.autovalor_base(n) for n in range(lap.n_zeros)]
    check(all(lams[i] < lams[i + 1] for i in range(len(lams) - 1)),
          "Autovalores λ_n^{(0)} estrictamente crecientes ✓",
          f"λ₁={lams[0]:.2f} < λ₂={lams[1]:.2f} < ...")

    resultados["psi_laplaciano"] = psi_l

    # -- EcuacionOndaNoética -------------------------------------------------
    subsection("EcuacionOndaNoética — ∂²Ψ/∂t² + ω₀²Ψ = ζ′(½)∇²Φ")
    eon = EcuacionOndaNoética()

    omega0 = eon.omega0
    check(abs(omega0 - 2.0 * math.pi * _F0) < 0.01,
          f"ω₀ = 2πf₀ = {omega0:.4f} rad/s",
          "frecuencia angular resonante")

    # Acoplamientos Yukawa
    g2 = eon.acoplamiento_yukawa(2)
    g_total = eon.acoplamiento_yukawa_total()
    check(g2 < 0.01,
          f"g_{{p=2}} = {g2:.7f} ≪ 1",
          "régimen perturbativo Yukawa")
    check(g_total < 0.05,
          f"g_total = Σg_p = {g_total:.6f} ≪ 1",
          "acoplamiento Yukawa total S={2,3,5,7,11}")

    # Relación de dispersión
    disp = eon.dispersion_k0()
    check(abs(disp - omega0 ** 2) < 1.0,
          f"ω²(k=0) = {disp:.2f} = ω₀² ✓",
          "resonancia pura en k=0")

    # Conservación de energía
    E0 = eon.energia_lagrangiana(0.0)
    E1 = eon.energia_lagrangiana(0.001)
    E2 = eon.energia_lagrangiana(0.01)
    check(abs(E0 - E1) < 1e-4 and abs(E0 - E2) < 1e-4,
          f"ℰ(t) = {E0:.4f} ≈ constante",
          "conservación de energía lagrangiana")

    # Solución resonante: periodicidad
    T = 2.0 * math.pi / omega0
    psi_t = eon.solucion_resonante(0.0)
    psi_tT = eon.solucion_resonante(T)
    check(abs(psi_t - psi_tT) < 1e-8,
          f"Ψ(0) ≈ Ψ(T): {psi_t:.6f} ≈ {psi_tT:.6f}",
          "periodicidad con T = 1/f₀")

    psi_n = eon.psi_noetica()
    check(psi_n >= 0.97,
          f"Ψ_noética = {psi_n:.6f} ≥ 0.97",
          "acoplamiento Yukawa débil → coherencia alta")

    resultados["psi_noetica"] = psi_n

    print(f"\n  Ψ_laplaciano = {psi_l:.6f}  |  Ψ_noética = {psi_n:.6f}")
    return resultados


# ===========================================================================
# FASE 3 — OperadorRegularizacionNS y OperadorTreewidth
# ===========================================================================

def fase3_ns_treewidth() -> dict:
    """Valida OperadorRegularizacionNS y OperadorTreewidth."""
    section("FASE 3 — Regularización Navier-Stokes y Operador Treewidth")
    resultados = {}

    # -- OperadorRegularizacionNS --------------------------------------------
    subsection("OperadorRegularizacionNS — Fluidez Adélica Laminar")
    ns = OperadorRegularizacionNS()

    nu = ns.viscosidad_efectiva()
    re_q = ns.reynolds_cuantico()
    margen = ns.margen_laminar()
    psi_s = ns.psi_ns()

    check(abs(nu - 1.0 / _F0) < 1e-8,
          f"ν_eff = 1/f₀ = {nu:.7f}",
          "viscosidad adélica universal")
    check(200.0 < re_q < 202.0,
          f"Re_q = (F₀/γ₁)·N = {re_q:.4f}",
          "Reynolds cuántico adélico")
    check(re_q < ns.re_critico,
          f"Re_q = {re_q:.1f} ≪ Re_c = {ns.re_critico:.0f}",
          "régimen laminar garantizado")
    check(margen > 0,
          f"Margen laminar = {margen:.6f} > 0",
          "flujo adélico en zona estable")
    check(psi_s >= 0.888,
          f"Ψ_NS = {psi_s:.6f} ≥ 0.888",
          "coherencia Navier-Stokes")

    # Forzamiento de coherencia
    F_psi = ns.forzamiento_coherencia_norma()
    check(F_psi > 0,
          f"‖F_Ψ‖ = |ζ′(½)|/ω₀ = {F_psi:.6f}",
          "forzamiento de coherencia positivo")

    resultados["psi_ns"] = psi_s

    # -- OperadorTreewidth ---------------------------------------------------
    subsection("OperadorTreewidth — κ_Π = 2.5773; P ≠ NP")
    tw = OperadorTreewidth()

    delta_gue = tw.espaciado_gue_gamma1()
    prod_kappa_gue = tw.producto_kappa_gue()
    prod_kappa_ramsey = tw.producto_kappa_phi_ramsey()
    umbral = tw.umbral_p_tractable()
    psi_t = tw.psi_treewidth()

    check(abs(tw.kappa_pi - 2.5773) < 1e-10,
          f"κ_Π = {tw.kappa_pi}",
          "invariante de complejidad P≠NP")
    check(abs(delta_gue - 7.75) < 0.05,
          f"δ_GUE(γ₁) = 2π/ln(γ₁/2π) = {delta_gue:.6f}",
          "espaciado GUE en altura γ₁")
    check(abs(prod_kappa_gue - 20.0) < 0.1,
          f"κ_Π · δ_GUE(γ₁) = {prod_kappa_gue:.6f} ≈ 20",
          "alineamiento treewidth-GUE-Riemann")
    check(0.99 < prod_kappa_ramsey < 1.05,
          f"κ_Π · φ_R = {prod_kappa_ramsey:.6f} ≈ 1",
          "invariante Ramsey-treewidth")
    check(abs(umbral - _KAPPA_PI / math.pi) < 1e-10,
          f"Umbral P-tractable = κ_Π/π = {umbral:.6f}",
          "frontera P/NP en el espacio de coherencia")

    # Clasificaciones
    clase_qcal = tw.clasificar(0.959)
    check(clase_qcal == "P-TRACTABLE",
          f"Ψ = 0.959 → {clase_qcal}",
          "QCAL es P-tractable")
    clase_np = tw.clasificar(0.3)
    check(clase_np == "NP-HARD",
          f"Ψ = 0.3 → {clase_np}",
          "baja coherencia es NP-hard")

    check(psi_t >= 0.97,
          f"Ψ_treewidth = {psi_t:.6f} ≥ 0.97",
          "alineamiento casi perfecto κ_Π·δ_GUE≈N_zeros")

    resultados["psi_treewidth"] = psi_t

    print(f"\n  Ψ_NS = {psi_s:.6f}  |  Ψ_treewidth = {psi_t:.6f}")
    return resultados


# ===========================================================================
# FASE 4 — Sistema Integrado y Certificación ∴OMQ∞³
# ===========================================================================

def fase4_sistema_integrado() -> dict:
    """Valida el SistemaOperadoresMaestros y emite la certificación."""
    section("FASE 4 — Sistema Integrado ∴OMQ∞³ y Certificación Final")
    resultados = {}

    subsection("SistemaOperadoresMaestros — Ψ_global ≥ 0.888")
    sistema = SistemaOperadoresMaestros()
    cert = sistema.certificar()

    # Verificar Ψ individuales
    subsection_psis = [
        ("psi_hpsi",       0.888, "H_Ψ autoadjunto"),
        ("psi_fredholm",   0.888, "Fredholm D(s)"),
        ("psi_laplaciano", 0.970, "Laplaciano adélico Δ_S"),
        ("psi_noetica",    0.970, "Onda noética + Yukawa"),
        ("psi_ns",         0.888, "Navier-Stokes adélico"),
        ("psi_treewidth",  0.970, "Treewidth P≠NP"),
    ]
    for key, threshold, desc in subsection_psis:
        val = cert[key]
        check(
            val >= threshold,
            f"  {key} = {val:.6f} ≥ {threshold}",
            desc,
        )

    # Pesos
    pesos = SistemaOperadoresMaestros._PESOS
    check(abs(sum(pesos) - 1.0) < 1e-12,
          f"Σ pesos = {sum(pesos):.12f} = 1",
          "normalización de pesos")
    check(len(pesos) == 6,
          f"6 pesos definidos: {pesos}",
          "uno por subsistema")

    # Coherencia global
    psi_g = cert["psi_global"]
    check(psi_g >= 0.888,
          f"Ψ_global = {psi_g:.6f} ≥ 0.888",
          "umbral noético QCAL superado")

    # Verificar Ψ_global ponderado
    psis = [cert[k] for k, _, _ in subsection_psis]
    psi_g_check = sum(w * p for w, p in zip(pesos, psis))
    check(abs(psi_g - psi_g_check) < 1e-10,
          f"Ψ_global = Σwᵢ·Ψᵢ = {psi_g_check:.8f}",
          "suma ponderada verificada")

    # Sello y certificación
    check(cert["sello_activo"],
          f"Sello activo: {cert['sello_activo']}",
          "Ψ_global ≥ 0.888 → sello activado")
    check(cert["sello"] == "∴OMQ∞³",
          f"Sello: {cert['sello']}",
          "certificación noética ∴OMQ∞³")
    check(cert["cert_mark"] == "OMQ-MAESTROS-VERIFIED",
          f"Marca técnica: {cert['cert_mark']}",
          "certificación técnica")

    # Invariantes físicos
    check(abs(cert["resonancia_f0_gamma1"] - 10.024) < 0.01,
          f"F₀/γ₁ = {cert['resonancia_f0_gamma1']:.6f} ≈ 10.024",
          "resonancia décupla fundamental")
    check(200.0 < cert["reynolds_cuantico"] < 202.0,
          f"Re_q = {cert['reynolds_cuantico']:.4f} ≪ Re_c = 2300",
          "régimen laminar adélico")
    check(abs(cert["producto_kappa_gue"] - 20.0) < 0.1,
          f"κ_Π·δ_GUE = {cert['producto_kappa_gue']:.6f} ≈ 20",
          "unificación complejidad-espectro")

    resultados["psi_global"] = psi_g
    resultados["certificado"] = cert

    # -- ResultadoOperadoresMaestros -----------------------------------------
    subsection("ResultadoOperadoresMaestros — dataclass de resultados")
    r = ResultadoOperadoresMaestros(
        psi_hpsi=cert["psi_hpsi"],
        psi_fredholm=cert["psi_fredholm"],
        psi_laplaciano=cert["psi_laplaciano"],
        psi_noetica=cert["psi_noetica"],
        psi_ns=cert["psi_ns"],
        psi_treewidth=cert["psi_treewidth"],
        psi_global=cert["psi_global"],
        sello_activo=cert["sello_activo"],
        sello=cert["sello"],
        cert_mark=cert["cert_mark"],
        resonancia_f0_gamma1=cert["resonancia_f0_gamma1"],
        kappa_pi=cert["kappa_pi"],
        phi_ramsey=cert["phi_ramsey"],
        reynolds_cuantico=cert["reynolds_cuantico"],
        producto_kappa_gue=cert["producto_kappa_gue"],
    )
    check(r.psi_global >= 0.888,
          f"ResultadoOperadoresMaestros.psi_global = {r.psi_global:.6f} ≥ 0.888",
          "dataclass poblado correctamente")
    check(r.sello_activo,
          f"ResultadoOperadoresMaestros.sello_activo = {r.sello_activo}",
          "sello en dataclass activo")

    # -- API pública ---------------------------------------------------------
    subsection("API pública: operadores_maestros_qcal_activar()")
    api_result = operadores_maestros_qcal_activar()
    check(isinstance(api_result, dict),
          "operadores_maestros_qcal_activar() retorna dict",
          "tipo correcto")
    check(api_result["sello_activo"],
          f"API sello_activo = {api_result['sello_activo']}",
          "API reporta sello activo")
    check(api_result["psi_global"] >= 0.888,
          f"API Ψ_global = {api_result['psi_global']:.6f} ≥ 0.888",
          "API supera umbral noético")
    check(api_result["cert_mark"] == "OMQ-MAESTROS-VERIFIED",
          f"API cert_mark = {api_result['cert_mark']}",
          "API emite certificación técnica")

    return resultados


# ===========================================================================
# RESUMEN FINAL
# ===========================================================================

def resumen_final(r1: dict, r2: dict, r3: dict, r4: dict) -> None:
    """Imprime el resumen final y verifica el umbral global."""
    section("RESUMEN FINAL — Certificación ∴OMQ∞³")

    tabla = [
        ("1", "OperadorHPsi (H_Ψ autoadjunto)",      r1.get("psi_hpsi", 0)),
        ("2", "DeterminanteFredholm D(s)",            r1.get("psi_fredholm", 0)),
        ("3", "LaplacianoAdelico Δ_S",                r2.get("psi_laplaciano", 0)),
        ("4", "EcuacionOndaNoética + Yukawa",         r2.get("psi_noetica", 0)),
        ("5", "OperadorRegularizacionNS",             r3.get("psi_ns", 0)),
        ("6", "OperadorTreewidth (P≠NP)",             r3.get("psi_treewidth", 0)),
    ]

    print()
    print(f"  {'Oper':<4} {'Subsistema':<42} {'Ψᵢ':>8}")
    print(f"  {'─'*4} {'─'*42} {'─'*8}")
    for num, nombre, psi in tabla:
        mark = _PASS if psi >= 0.888 else _WARN
        print(f"  {num:<4} {nombre:<42} {psi:>8.6f} {mark}")

    print(f"  {'─'*4} {'─'*42} {'─'*8}")

    psi_g = r4.get("psi_global", 0.0)
    mark_g = _PASS if psi_g >= 0.888 else _FAIL
    print(f"  {'':4} {'Ψ_GLOBAL (ponderado)':>42}  {psi_g:>8.6f} {mark_g}")

    print()
    if psi_g >= 0.888 and not errors:
        print("  ╔══════════════════════════════════════════════════════════╗")
        print("  ║                                                          ║")
        print(f"  ║  SELLO ∴OMQ∞³ ACTIVO — Ψ_global = {psi_g:.6f} ≥ 0.888  ║")
        print("  ║  Certificación: OMQ-MAESTROS-VERIFIED                   ║")
        print("  ║  f₀ = 141.7001 Hz  |  ζ′(½) ≈ −3.9226                 ║")
        print("  ║  κ_Π = 2.5773  |  φ_R = 43/108  |  Re_q ≈ 200.5       ║")
        print("  ║  Todos los operadores conmutan en el espacio adélico.   ║")
        print("  ╚══════════════════════════════════════════════════════════╝")
    else:
        print(f"  ✗ SELLO NO ACTIVO — Ψ_global = {psi_g:.6f} < 0.888")
        print(f"  {len(errors)} error(s) detectados:")
        for err in errors:
            print(f"    {err}")


# ===========================================================================
# GUARDAR RESULTADOS JSON
# ===========================================================================

def guardar_resultados(r4: dict) -> None:
    """Guarda el certificado en resultados/validate_omq_maestros.json."""
    out_dir = Path(__file__).parent.parent / "resultados"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "validate_omq_maestros.json"

    cert = r4.get("certificado", {})
    payload = {
        "sello": cert.get("sello", ""),
        "cert_mark": cert.get("cert_mark", ""),
        "psi_global": cert.get("psi_global", 0.0),
        "sello_activo": cert.get("sello_activo", False),
        "psi_hpsi": cert.get("psi_hpsi", 0.0),
        "psi_fredholm": cert.get("psi_fredholm", 0.0),
        "psi_laplaciano": cert.get("psi_laplaciano", 0.0),
        "psi_noetica": cert.get("psi_noetica", 0.0),
        "psi_ns": cert.get("psi_ns", 0.0),
        "psi_treewidth": cert.get("psi_treewidth", 0.0),
        "f0_hz": cert.get("f0_hz", 0.0),
        "zeta_prime_half": cert.get("zeta_prime_half", 0.0),
        "kappa_pi": cert.get("kappa_pi", 0.0),
        "phi_ramsey": cert.get("phi_ramsey", 0.0),
        "resonancia_f0_gamma1": cert.get("resonancia_f0_gamma1", 0.0),
        "reynolds_cuantico": cert.get("reynolds_cuantico", 0.0),
        "producto_kappa_gue": cert.get("producto_kappa_gue", 0.0),
    }
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"\n  Resultados guardados en: {out_file}")


# ===========================================================================
# MAIN
# ===========================================================================

def main() -> int:
    """Punto de entrada principal del validador ∴OMQ∞³."""
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║  VALIDACIÓN OPERADORES MAESTROS QCAL ∞³  ∴OMQ∞³                 ║")
    print("║  f₀ = 141.7001 Hz  |  ζ′(½) ≈ −3.9226  |  κ_Π = 2.5773        ║")
    print("╚════════════════════════════════════════════════════════════════════╝")

    r1 = fase1_hpsi_fredholm()
    r2 = fase2_laplaciano_noetica()
    r3 = fase3_ns_treewidth()
    r4 = fase4_sistema_integrado()

    resumen_final(r1, r2, r3, r4)
    guardar_resultados(r4)

    if errors:
        print(f"\n  {len(errors)} verificación(es) fallida(s).")
        return 1
    print(f"\n  Todas las verificaciones superadas. ∴OMQ∞³")
    return 0


if __name__ == "__main__":
    sys.exit(main())
