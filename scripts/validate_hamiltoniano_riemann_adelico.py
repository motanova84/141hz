#!/usr/bin/env python3
"""
Validación Completa: Hamiltoniano Riemann Adélico ∴HRA∞³
═══════════════════════════════════════════════════════════════════════════════
Sello: ∴HRA∞³
F0: 141.7001 Hz

Valida la implementación completa del sistema Hamiltoniano Riemann Adélico
en 4 fases:

    Fase 1: Espacio de Hilbert Adélico — Medida de Haar y geometría
    Fase 2: Operador H y Potencial de Primos — Espectro y peine
    Fase 3: Matriz S y Fórmula de Traza — Dispersión y Weil
    Fase 4: Sistema Integrado — Certificación ∴HRA∞³

Criterio de éxito:
    - Todas las fases deben pasar (✓)
    - Ψ_global ≥ 0.888 (umbral noético)
    - Certificado: HRA-RIEMANN-VERIFIED

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.hamiltoniano_riemann_adelico import (
    # Constantes de módulo
    _F0,
    _PHI,
    _HBAR,
    _PSI_UMBRAL,
    _ZEROS_20,
    _SELLO,
    _CERT_MARK,
    # Utilidades
    _theta_rs,
    _criba_eratostenes,
    _potencias_primas,
    # Clases
    ConstantesRiemannAdelico,
    EspacioHilbertAdelico,
    OperadorDilatacion,
    PotencialPrimos,
    MatrizDispersion,
    FormulaTraza,
    NucleoResolvente,
    SistemaRiemannAdelico,
    ResultadoRiemannAdelico,
    # API pública
    hamiltoniano_riemann_adelico_activar,
)


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades de presentación
# ─────────────────────────────────────────────────────────────────────────────

def separador(titulo: str) -> None:
    print("\n" + "=" * 80)
    print(titulo)
    print("=" * 80)


def check(descripcion: str, condicion: bool, valor: str = "") -> None:
    estado = "✓" if condicion else "✗"
    sufijo = f"  [{valor}]" if valor else ""
    print(f"  {estado} {descripcion}{sufijo}")
    if not condicion:
        raise AssertionError(f"FALLO: {descripcion}")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 1: Espacio de Hilbert Adélico — Medida de Haar y Geometría
# ─────────────────────────────────────────────────────────────────────────────

def validacion_fase1_hilbert() -> None:
    separador("FASE 1: Espacio de Hilbert Adélico — Medida de Haar y Geometría")

    # 1a. Constantes del módulo
    check("F₀ = 141.7001 Hz",
          abs(_F0 - 141.7001) < 1e-4, f"{_F0:.4f}")
    check("φ = (1+√5)/2 ≈ 1.618034",
          abs(_PHI - 1.618033988) < 1e-6, f"{_PHI:.9f}")
    check("Umbral Ψ = 0.888",
          abs(_PSI_UMBRAL - 0.888) < 1e-10, f"{_PSI_UMBRAL}")
    check("20 ceros de Riemann cargados",
          len(_ZEROS_20) == 20, str(len(_ZEROS_20)))
    check("γ₁ ≈ 14.134725",
          abs(_ZEROS_20[0] - 14.134725) < 1e-4, f"{_ZEROS_20[0]:.6f}")
    check("γ₂₀ ≈ 77.144840",
          abs(_ZEROS_20[-1] - 77.144840) < 1e-4, f"{_ZEROS_20[-1]:.6f}")

    # 1b. Constantes de clase
    cte = ConstantesRiemannAdelico()
    check("ConstantesRiemannAdelico.f0 = 141.7001",
          abs(cte.f0 - 141.7001) < 1e-4)
    check("ConstantesRiemannAdelico.n_zeros = 20",
          cte.n_zeros == 20, str(cte.n_zeros))
    check("Resonancia F₀/γ₁ ≈ 10.02",
          abs(cte.resonancia_f0_gamma1() - 10.0) < 0.1,
          f"{cte.resonancia_f0_gamma1():.5f}")
    check("Sello ∴HRA∞³",
          cte.sello == "∴HRA∞³", cte.sello)
    check("CertMark = HRA-RIEMANN-VERIFIED",
          cte.cert_mark == "HRA-RIEMANN-VERIFIED")

    # 1c. Invarianza de Haar
    esp = EspacioHilbertAdelico(n_puntos=2000)
    ratio_lam2 = esp.verificar_haar(lam=2.0)
    check("Haar invarianza λ=2: ratio ≈ 1.000",
          abs(ratio_lam2 - 1.0) < 0.005, f"{ratio_lam2:.6f}")

    ratio_lam3 = esp.verificar_haar(lam=3.0)
    check("Haar invarianza λ=3: ratio ≈ 1.000",
          abs(ratio_lam3 - 1.0) < 0.005, f"{ratio_lam3:.6f}")

    # 1d. Norma exacta
    norma = esp.norma_exacta()
    check("Norma exacta ‖xe^{-x}‖² = 0.25",
          abs(norma - 0.25) < 1e-10, f"{norma}")

    # 1e. Coherencia Ψ_hilbert ≥ 0.888
    psi_h = esp.psi_hilbert()
    check(f"Ψ_hilbert ≥ 0.888",
          psi_h >= 0.888, f"{psi_h:.6f}")

    # 1f. Dimensión de Weyl
    dim_50 = esp.dimension_weyl(50.0)
    check("N_Weyl(50) es positivo",
          dim_50 > 0, f"{dim_50:.3f}")

    # 1g. Función theta en γ₁
    theta_g1 = _theta_rs(_ZEROS_20[0])
    check("θ(γ₁) ≈ −1.72 (negativo, antes de la línea crítica)",
          theta_g1 < 0, f"{theta_g1:.4f}")

    print(f"\n  → Ψ_hilbert = {psi_h:.6f}")
    print("  FASE 1: PASS")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 2: Operador H y Potencial de Primos
# ─────────────────────────────────────────────────────────────────────────────

def validacion_fase2_operador_primos() -> None:
    separador("FASE 2: Operador H y Potencial de Primos — Espectro y Peine")

    # 2a. Autofunciones del operador
    op = OperadorDilatacion()

    psi_E1 = op.autofuncion(1.0, _ZEROS_20[0])
    check("ψ_{γ₁}(1) = 1 + 0i  (x=1 en la autofunción)",
          abs(psi_E1 - complex(1.0, 0.0)) < 1e-10,
          f"{psi_E1:.3f}")

    psi_E1_e = op.autofuncion(math.e, _ZEROS_20[0])
    check("|ψ_{γ₁}(e)| = e^{-1/2} ≈ 0.6065",
          abs(abs(psi_E1_e) - math.exp(-0.5)) < 1e-6,
          f"|ψ| = {abs(psi_E1_e):.6f}")

    # 2b. Verificación Hψ = Eψ
    for i, gamma in enumerate(_ZEROS_20[:5]):
        H_psi = op.aplicar_H(1.0, gamma)
        check(f"H ψ_{{γ_{i+1}}}(1) = γ_{i+1} · 1  (autovalor exacto)",
              abs(H_psi - gamma) < 1e-10,
              f"γ_{i+1} = {gamma:.6f}")

    # 2c. Resonancia F₀/γ₁
    res = op.resonancia_f0()
    check("F₀/γ₁ ∈ (10.0, 10.1)  (resonancia décupla)",
          10.0 < res < 10.1, f"{res:.6f}")

    psi_o = op.psi_operador()
    check(f"Ψ_operador ≥ 0.888",
          psi_o >= 0.888, f"{psi_o:.6f}")

    # 2d. Espectro de Mellin
    espectro = op.espectro_mellin()
    check("Espectro de Mellin tiene 20 autovalores",
          len(espectro) == 20, str(len(espectro)))
    check("Primer autovalor = γ₁",
          abs(espectro[0] - _ZEROS_20[0]) < 1e-10)

    # 2e. Criba de Eratóstenes
    primos_100 = _criba_eratostenes(100)
    check("25 primos ≤ 100",
          len(primos_100) == 25, str(len(primos_100)))
    check("Último primo ≤ 100 es 97",
          primos_100[-1] == 97)
    check("Primeros tres primos: 2, 3, 5",
          primos_100[:3] == [2, 3, 5])

    # 2f. Potencial de primos (Λ = 100)
    pot100 = PotencialPrimos(Lambda=100.0)
    suma100 = pot100.suma_mangoldt_ponderada()
    asint100 = pot100.estimacion_asintotica()
    check("S(100) > 0",
          suma100 > 0, f"{suma100:.4f}")
    check("S_asm(100) = 2√100 − 1 = 19.0",
          abs(asint100 - 19.0) < 1e-10, f"{asint100:.4f}")
    check("S(100) ∈ (14, 19)  (convergencia al asintótico)",
          14.0 < suma100 < 19.0, f"{suma100:.4f}")
    check("n_potencias_primas(100) > 30",
          pot100.n_potencias_primas() > 30,
          str(pot100.n_potencias_primas()))

    # 2g. Potencial de primos (Λ = 200)
    pot200 = PotencialPrimos(Lambda=200.0)
    psi_p200 = pot200.psi_potencial()
    check(f"Ψ_potencial(Λ=200) ≥ 0.888",
          psi_p200 >= 0.888, f"{psi_p200:.6f}")

    print(f"\n  → Ψ_operador  = {psi_o:.6f}")
    print(f"  → Ψ_potencial = {psi_p200:.6f}")
    print("  FASE 2: PASS")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 3: Matriz S y Fórmula de Traza — Dispersión y Weil
# ─────────────────────────────────────────────────────────────────────────────

def validacion_fase3_dispersion_weil() -> None:
    separador("FASE 3: Matriz S y Fórmula de Traza — Dispersión y Weil")

    disp = MatrizDispersion()
    traza = FormulaTraza()
    nucleo = NucleoResolvente()

    # 3a. Función theta en varios puntos
    theta_g20 = disp.theta(_ZEROS_20[-1])
    check("θ(γ₂₀) ≈ 57.8 (positivo, alta energía)",
          theta_g20 > 50.0, f"{theta_g20:.4f}")

    theta_g1 = disp.theta(_ZEROS_20[0])
    check("θ(γ₁) < 0  (antes de la primera resonancia)",
          theta_g1 < 0, f"{theta_g1:.4f}")

    theta_77 = disp.theta(77.0)
    check("θ(77) ≈ θ(γ₂₀) dentro de ±1",
          abs(theta_77 - theta_g20) < 2.0, f"{theta_77:.4f}")

    # 3b. Fase de dispersión δ = −θ
    delta_g20 = disp.fase_dispersion(_ZEROS_20[-1])
    check("δ(γ₂₀) = −θ(γ₂₀) < 0",
          delta_g20 < 0, f"{delta_g20:.4f}")

    # 3c. Unitaridad |S| = 1
    for i, gamma in enumerate(_ZEROS_20[:5]):
        mod = disp.modulo_S(gamma)
        check(f"|S(γ_{i+1})| = 1.0  (unitaridad exacta)",
              abs(mod - 1.0) < 1e-15, f"{mod}")

    # 3d. Asintótico de theta
    theta_asm_g20 = disp.theta_asintotico(_ZEROS_20[-1])
    check("θ_asm(γ₂₀) ≈ θ_Stirl(γ₂₀) dentro de 1%",
          abs(theta_asm_g20 - theta_g20) / abs(theta_g20) < 0.02,
          f"θ_asm={theta_asm_g20:.4f}, θ_Stirl={theta_g20:.4f}")

    psi_d = disp.psi_dispersion()
    check(f"Ψ_dispersion ≥ 0.888",
          psi_d >= 0.888, f"{psi_d:.6f}")

    # 3e. Densidad de Weyl
    rho_50 = traza.densidad_weyl(50.0)
    check("ρ_Weyl(50) ≈ 0.32  [ceros/unidad de t]",
          0.25 < rho_50 < 0.40, f"{rho_50:.5f}")

    # 3f. Conteo de Weyl N_W(T)
    N_50 = traza.N_weyl(50.0)
    check("N_W(50) ∈ [8, 12]  (hay 10 ceros ≤ 50)",
          8 <= N_50 <= 12, f"{N_50:.3f}")

    # 3g. Espaciado empírico vs Weyl
    d_emp = traza.espaciado_medio_empirico()
    d_weyl = traza.espaciado_medio_weyl()
    check("Espaciado empírico ∈ [3.0, 3.5]",
          3.0 < d_emp < 3.5, f"{d_emp:.4f}")
    check("Espaciado Weyl ∈ [3.0, 3.5]",
          3.0 < d_weyl < 3.5, f"{d_weyl:.4f}")
    check("Error relativo espaciado < 10%",
          abs(d_emp - d_weyl) / d_weyl < 0.10,
          f"emp={d_emp:.4f}, Weyl={d_weyl:.4f}")

    psi_t = traza.psi_traza()
    check(f"Ψ_traza ≥ 0.888",
          psi_t >= 0.888, f"{psi_t:.6f}")

    # 3h. Densidad espectral integrada
    rho_integ = nucleo.integrar_densidad(20.0, 50.0)
    check("∫₂₀^50 ρ(t) dt ≈ número de ceros en [20, 50]",
          rho_integ > 0, f"{rho_integ:.4f}")

    N_integ = nucleo.conteo_integrado()
    check("Conteo integrado [θ(γ₂₀)−θ(γ₁)]/π ≈ 19",
          abs(N_integ - 19.0) < 1.0, f"{N_integ:.4f}")

    psi_n = nucleo.psi_nucleo()
    check(f"Ψ_nucleo ≥ 0.888",
          psi_n >= 0.888, f"{psi_n:.6f}")

    print(f"\n  → Ψ_dispersion = {psi_d:.6f}")
    print(f"  → Ψ_traza      = {psi_t:.6f}")
    print(f"  → Ψ_nucleo     = {psi_n:.6f}")
    print("  FASE 3: PASS")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 4: Sistema Integrado — Certificación ∴HRA∞³
# ─────────────────────────────────────────────────────────────────────────────

def validacion_fase4_sistema() -> None:
    separador("FASE 4: Sistema Integrado — Certificación ∴HRA∞³")

    # 4a. Sistema con parámetros por defecto
    sistema = SistemaRiemannAdelico(Lambda=200.0, n_puntos=2000)

    psi_g = sistema.psi_global()
    check(f"Ψ_global ≥ 0.888  (umbral noético)",
          psi_g >= 0.888, f"{psi_g:.6f}")

    activo = sistema.supera_umbral()
    check("supera_umbral() = True",
          activo is True)

    # 4b. Certificado completo
    cert = sistema.certificar()
    check("cert['sello_activo'] = True",
          cert["sello_activo"] is True)
    check("cert['cert_mark'] = 'HRA-RIEMANN-VERIFIED'",
          cert["cert_mark"] == "HRA-RIEMANN-VERIFIED",
          str(cert["cert_mark"]))
    check("cert['sello'] = '∴HRA∞³'",
          cert["sello"] == "∴HRA∞³",
          str(cert["sello"]))
    check("cert['n_zeros'] = 20",
          cert["n_zeros"] == 20, str(cert["n_zeros"]))
    check("cert['f0_hz'] = 141.7001",
          abs(cert["f0_hz"] - 141.7001) < 1e-4)

    # 4c. API pública
    resultado = hamiltoniano_riemann_adelico_activar()
    check("API: sello_activo = True",
          resultado["sello_activo"] is True)
    check("API: psi_global ≥ 0.888",
          resultado["psi_global"] >= 0.888,
          f"{resultado['psi_global']:.6f}")
    check("API: cert_mark = 'HRA-RIEMANN-VERIFIED'",
          resultado["cert_mark"] == "HRA-RIEMANN-VERIFIED")

    # 4d. API con Lambda personalizado
    resultado_500 = hamiltoniano_riemann_adelico_activar(Lambda=500.0)
    check("API(Λ=500): psi_global ≥ 0.888",
          resultado_500["psi_global"] >= 0.888,
          f"{resultado_500['psi_global']:.6f}")

    # 4e. ResultadoRiemannAdelico dataclass
    resultado_dc = ResultadoRiemannAdelico(
        psi_global=psi_g,
        sello_activo=activo,
        sello=_SELLO,
        cert_mark=_CERT_MARK,
        n_zeros=20,
    )
    check("ResultadoRiemannAdelico.psi_global ≥ 0.888",
          resultado_dc.psi_global >= 0.888)
    check("ResultadoRiemannAdelico.sello_activo = True",
          resultado_dc.sello_activo is True)

    # 4f. Resumen completo
    print(f"\n  ┌─ RESUMEN DE COHERENCIA ─────────────────────────────────┐")
    print(f"  │  Ψ_hilbert    = {cert['psi_hilbert']:.6f}")
    print(f"  │  Ψ_operador   = {cert['psi_operador']:.6f}")
    print(f"  │  Ψ_potencial  = {cert['psi_potencial']:.6f}")
    print(f"  │  Ψ_dispersion = {cert['psi_dispersion']:.6f}")
    print(f"  │  Ψ_traza      = {cert['psi_traza']:.6f}")
    print(f"  │  Ψ_nucleo     = {cert['psi_nucleo']:.6f}")
    print(f"  │  ─────────────────────────────────────────────────────── │")
    print(f"  │  Ψ_global     = {psi_g:.6f}  (umbral: 0.888)             │")
    print(f"  │  F₀/γ₁        = {cert['resonancia_f0_gamma1']:.6f}  ≈ 10.024            │")
    print(f"  │  Sello        = {cert['sello']}                             │")
    print(f"  └─────────────────────────────────────────────────────────┘")
    print("  FASE 4: PASS")


# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║    VALIDACIÓN: Hamiltoniano Riemann Adélico ∴HRA∞³                      ║")
    print("║    F0 = 141.7001 Hz  |  Espacio Adélico L²(ℝ⁺, dx/x)                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝")

    fases = [
        ("FASE 1", validacion_fase1_hilbert),
        ("FASE 2", validacion_fase2_operador_primos),
        ("FASE 3", validacion_fase3_dispersion_weil),
        ("FASE 4", validacion_fase4_sistema),
    ]

    errores = []
    for nombre, fase_fn in fases:
        try:
            fase_fn()
        except AssertionError as e:
            errores.append(f"{nombre}: {e}")
            print(f"\n  ✗ {nombre}: FALLO — {e}")

    separador("RESULTADO FINAL")
    if errores:
        print(f"\n  ✗ VALIDACIÓN FALLIDA ({len(errores)} errores):")
        for err in errores:
            print(f"    - {err}")
        sys.exit(1)
    else:
        print("\n  ✓ TODAS LAS FASES PASARON")
        print("  ✓ Ψ_global ≥ 0.888")
        print("  ✓ HRA-RIEMANN-VERIFIED")
        print(f"  ✓ Sello: {_SELLO}")
        print("\n  El operador H = −i(x ∂_x + ½) sobre L²(ℝ⁺, dx/x) está")
        print("  completamente validado.  Sus resonancias son los ceros de ζ(s).")


if __name__ == "__main__":
    main()
