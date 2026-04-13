#!/usr/bin/env python3
"""
Validación Completa: QCAL-Strings — Forzado de Modos Kaluza-Klein
═══════════════════════════════════════════════════════════════════════════════
Sello: ∴𓂀Ω∞³
F0: 141.7001 Hz

Valida la implementación completa del sistema QCAL-Strings en 4 fases:

    Fase 1: Ceros de Riemann — Espectro de modos KK
    Fase 2: Amplitud de Veneziano — Acoplamiento cuántico de cuerdas
    Fase 3: Operador de Forzado Noético — F̂_strings con superradiancia N²
    Fase 4: Gran Unificación — Sistema integrado y certificación

Criterio de éxito:
    - Todas las fases deben pasar (PASS)
    - Ψ_global ≥ 0.888 (umbral noético)
    - Certificado: QED-CUERDAS-VERIFIED

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.qcal_string_core import (
    RIEMANN_ZEROS_20,
    N_MODOS_KK,
    PSI_THRESHOLD,
    CERT_MARK,
    CerosRiemann,
    AmplitudVeneziano,
    ModosKaluzaKlein,
    ForzadoCuerdasNoetico,
    DualidadFluidoGravedad,
    AguaEZHexagonal,
    SistemaQCalStrings,
    qcal_strings_activar,
    string_noetic_forcing,
)


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


# ═══════════════════════════════════════════════════════════════════════════
# FASE 1: Ceros de Riemann — Espectro KK
# ═══════════════════════════════════════════════════════════════════════════

def validacion_fase1_ceros_riemann() -> None:
    separador("FASE 1: Ceros de Riemann — Espectro de Modos KK")

    zeros = CerosRiemann()
    modos = ModosKaluzaKlein()

    # Check 1: Exactamente 20 ceros
    check("20 ceros de Riemann cargados", len(zeros.zeros) == 20, str(len(zeros.zeros)))

    # Check 2: Primer cero ≈ 14.1347
    lam1 = zeros.zeros[0]
    check("λ₁ ≈ 14.1347 (primer cero no trivial)", abs(lam1 - 14.134725) < 1e-4,
          f"λ₁ = {lam1:.6f}")

    # Check 3: Modo 1 ≈ 2003 Hz (λ₁ × F₀)
    f1 = modos.frecuencia_modo(1)
    check("Modo 1 ≈ 2003 Hz (λ₁ × F₀)", 2000.0 < f1 < 2010.0, f"f₁ = {f1:.1f} Hz")

    # Check 4: Los ceros son estrictamente crecientes
    crecientes = all(zeros.zeros[i] < zeros.zeros[i + 1] for i in range(19))
    check("Ceros de Riemann son estrictamente crecientes", crecientes)

    # Check 5: Amplitudes αₙ = 1/√n (decrecientes)
    alphas = zeros.amplitudes_veneziano()
    check("α₁ = 1.0 (amplitud del modo fundamental)", abs(alphas[0] - 1.0) < 1e-10,
          f"α₁ = {alphas[0]:.6f}")
    check("Amplitudes decrecientes (α₁ > α₂ > ... > α₂₀)",
          all(alphas[i] > alphas[i + 1] for i in range(19)))

    # Check 6: Fases de T-dualidad φ₁ = π/2
    phases = zeros.fases_tdualidad()
    check("φ₁ = π/2 (T-dualidad modo 1)", abs(phases[0] - math.pi / 2) < 1e-10,
          f"φ₁ = {phases[0]:.4f} rad")

    # Check 7: Espectro completo de 20 modos
    espectro = modos.espectro_completo()
    check("Espectro KK completo: 20 modos", len(espectro) == 20, str(len(espectro)))

    # Check 8: Energía espectral en pico dominante (modo 1)
    k1 = RIEMANN_ZEROS_20[0]
    E_pico = modos.energia_espectral(k1)
    E_lejos = modos.energia_espectral(k1 + 10.0)
    check("Pico de energía dominante en λ₁", E_pico > E_lejos,
          f"E(λ₁) = {E_pico:.3f}, E(λ₁+10) = {E_lejos:.3f}")

    print("\n  → FASE 1: PASS ✓")


# ═══════════════════════════════════════════════════════════════════════════
# FASE 2: Amplitud de Veneziano — Acoplamiento de Cuerdas
# ═══════════════════════════════════════════════════════════════════════════

def validacion_fase2_veneziano() -> None:
    separador("FASE 2: Amplitud de Veneziano — Acoplamiento Cuántico de Cuerdas")

    v = AmplitudVeneziano()
    f0 = 141.7001

    # Check 1: Trayectoria de Regge en F₀²
    alpha_f0 = v.trayectoria_regge(f0 ** 2)
    check("α(F₀²) = 2.0 (trayectoria Regge en punto canónico)",
          abs(alpha_f0 - 2.0) < 1e-8, f"α(F₀²) = {alpha_f0:.6f}")

    # Check 2: B(2, 2) = 1/6
    amp_canonico = v.amplitud_canonico()
    check("A_canonico = B(2,2) = 1/6 ≈ 0.1667",
          abs(amp_canonico - 1.0 / 6.0) < 1e-8, f"A = {amp_canonico:.6f}")

    # Check 3: Coherencia Veneziano vía teorema óptico
    psi_v = v.coherencia_veneziano()
    expected_psi_v = math.sqrt(1.0 - (1.0 / 6.0) ** 2)
    check("Ψ_V = √(1 - |B|²) = √(35/36) ≈ 0.9860",
          abs(psi_v - expected_psi_v) < 1e-10, f"Ψ_V = {psi_v:.4f}")

    # Check 4: Ψ_V ∈ (0.98, 0.99) (rango de coherencia alta)
    check("Ψ_V ∈ (0.98, 0.99) — coherencia alta del vacío de cuerdas",
          0.98 < psi_v < 0.99, f"Ψ_V = {psi_v:.4f}")

    # Check 5: amplitud con α(s) ≤ 0 retorna 0 (polo de Γ)
    amp_polo = v.amplitud(-200.0 * f0 ** 2, f0 ** 2)
    check("amplitud en polo (α ≤ 0) retorna 0.0", amp_polo == 0.0,
          f"A_polo = {amp_polo}")

    # Check 6: Pendiente de Regge α' = 1/F₀²
    check("α' = 1/F₀² (pendiente Regge natural QCAL)",
          abs(v.alpha_prima - 1.0 / f0 ** 2) < 1e-12,
          f"α' = {v.alpha_prima:.3e} s²")

    print("\n  → FASE 2: PASS ✓")


# ═══════════════════════════════════════════════════════════════════════════
# FASE 3: Operador de Forzado Noético
# ═══════════════════════════════════════════════════════════════════════════

def validacion_fase3_forzado() -> None:
    separador("FASE 3: Operador de Forzado Noético — F̂_strings con Superradiancia N²")

    psi_test = 0.95

    # Check 1: Ganancia superradiante = N² × Ψ²
    f = ForzadoCuerdasNoetico(psi_local=psi_test)
    ganancia_esperada = (1e13 ** 2) * (psi_test ** 2)
    check("Ganancia superradiante G = N² × Ψ²",
          abs(f.ganancia - ganancia_esperada) / ganancia_esperada < 1e-10,
          f"G = {f.ganancia:.3e}")

    # Check 2: Forzado escalar no nulo para Ψ > 0
    f_escalar = f.forzado_escalar(0.0)
    check("Forzado escalar F(t=0) ≠ 0 para Ψ > 0", f_escalar != 0.0,
          f"F(0) = {f_escalar:.3e}")

    # Check 3: Forzado normalizado en rango [-Ψ², Ψ²]
    forzados = [abs(f.forzado_normalizado(t)) for t in [0.0, 0.001, 0.01, 0.1]]
    max_forzado = max(forzados)
    check("Forzado normalizado |F_norm| ≤ Ψ²",
          max_forzado <= psi_test ** 2 + 1e-10,
          f"max|F_norm| = {max_forzado:.4f}, Ψ² = {psi_test**2:.4f}")

    # Check 4: Espectro de potencia — 20 modos con potencias positivas
    esp = f.espectro_potencia()
    check("Espectro de potencia: 20 modos", len(esp) == 20, str(len(esp)))
    check("Todas las potencias > 0", all(e["potencia"] > 0 for e in esp))

    # Check 5: Con Ψ = 0, la ganancia y el forzado son cero
    f0_psi = ForzadoCuerdasNoetico(psi_local=0.0)
    check("Con Ψ=0: ganancia = 0", f0_psi.ganancia == 0.0, "G = 0.0")
    check("Con Ψ=0: F_escalar = 0", f0_psi.forzado_escalar(1.0) == 0.0, "F = 0.0")

    # Check 6: API string_noetic_forcing retorna (f_x, f_y) con f_y = 0
    f_x, f_y = string_noetic_forcing(0.0, RIEMANN_ZEROS_20, psi_test)
    check("string_noetic_forcing retorna (f_x, f_y) con f_y = 0.0", f_y == 0.0,
          f"f_y = {f_y}")
    check("string_noetic_forcing: f_x ≠ 0 para Ψ > 0", f_x != 0.0,
          f"f_x = {f_x:.3e}")

    # Check 7: Relación N² verificada — duplicar N cuadruplica el forzado
    f_x1, _ = string_noetic_forcing(0.001, RIEMANN_ZEROS_20, psi_test, n_microtubules=1e3)
    f_x2, _ = string_noetic_forcing(0.001, RIEMANN_ZEROS_20, psi_test, n_microtubules=2e3)
    ratio = f_x2 / f_x1
    check("Relación N²: duplicar N cuadruplica el forzado",
          abs(ratio - 4.0) < 1e-10, f"ratio = {ratio:.6f}")

    # Check 8: Dualidad fluido/gravedad — viscosidad y estado
    d = DualidadFluidoGravedad(psi_coherencia=1.0)
    check("Viscosidad holográfica → 0 para Ψ = 1.0",
          d.viscosidad_efectiva == 0.0, "η = 0.0")
    check("Estado fluido con Ψ = 1.0: FLUIDO_HOLOGRÁFICO_PERFECTO",
          d.estado_fluido == "FLUIDO_HOLOGRÁFICO_PERFECTO")

    d_low = DualidadFluidoGravedad(psi_coherencia=0.5)
    check("Estado fluido con Ψ = 0.5: TURBULENCIA_GUE",
          d_low.estado_fluido == "TURBULENCIA_GUE")

    # Check 9: Agua EZ hexagonal — coherencia intrínseca
    agua = AguaEZHexagonal(psi_ez=0.997)
    check("Coherencia EZ = 0.997 (propiedad intrínseca del agua)",
          abs(agua.coherencia_ez() - 0.997) < 1e-14, f"Ψ_EZ = {agua.coherencia_ez():.3f}")

    print("\n  → FASE 3: PASS ✓")


# ═══════════════════════════════════════════════════════════════════════════
# FASE 4: Gran Unificación — Sistema Integrado y Certificación
# ═══════════════════════════════════════════════════════════════════════════

def validacion_fase4_unificacion() -> None:
    separador("FASE 4: Gran Unificación — Sistema Integrado y Certificación")

    # Check 1: Sistema con Ψ₀ = 1.0 (ideal)
    sistema = SistemaQCalStrings(psi_inicial=1.0)
    psi_global = sistema.psi_global()
    check("Ψ_global con Ψ₀=1.0 ≥ 0.988 (coherencia casi perfecta)",
          psi_global >= 0.988, f"Ψ_global = {psi_global:.4f}")
    check("Ψ_global con Ψ₀=1.0 ∈ [0, 1]",
          0.0 <= psi_global <= 1.0, f"Ψ_global = {psi_global:.4f}")

    # Check 2: Certificación exitosa
    cert = sistema.certificar()
    check("Certificado = QED-CUERDAS-VERIFIED",
          cert["certificado"] == CERT_MARK, cert["certificado"])
    check("supera_umbral = True", cert["supera_umbral"] is True)
    check("sello = ∴𓂀Ω∞³", cert["sello"] == "∴𓂀Ω∞³", cert["sello"])

    # Check 3: Frecuencia del modo dominante
    check("Frecuencia modo dominante ≈ 2003 Hz",
          2000.0 < cert["f_modo_1_hz"] < 2010.0,
          f"f₁ = {cert['f_modo_1_hz']:.1f} Hz")

    # Check 4: N_modos_kk = 20
    check("n_modos_kk = 20 en certificado",
          cert["n_modos_kk"] == 20, str(cert["n_modos_kk"]))

    # Check 5: Sistema con Ψ₀ = 0.888 (umbral mínimo)
    sistema_888 = SistemaQCalStrings(psi_inicial=0.888)
    psi_888 = sistema_888.psi_global()
    check("Ψ_global con Ψ₀=0.888 ≥ PSI_THRESHOLD",
          psi_888 >= PSI_THRESHOLD, f"Ψ_global = {psi_888:.4f}")

    # Check 6: Sistema degradado (Ψ₀ = 0.1) no certifica
    sistema_bajo = SistemaQCalStrings(psi_inicial=0.1)
    cert_bajo = sistema_bajo.certificar()
    check("Sistema con Ψ₀=0.1 no certifica",
          cert_bajo["supera_umbral"] is False)

    # Check 7: Monotonicidad — Ψ_global crece con Ψ₀
    psis_init = [0.0, 0.3, 0.5, 0.7, 0.888, 0.95, 1.0]
    psis_global = [SistemaQCalStrings(psi_inicial=p).psi_global() for p in psis_init]
    monotonico = all(psis_global[i] <= psis_global[i + 1] for i in range(len(psis_global) - 1))
    check("Ψ_global es monótona creciente con Ψ₀", monotonico)

    # Check 8: Simulación de pulso temporal
    resultado = sistema.simular_pulso(t_max=1e-3, n_pasos=50)
    check("simular_pulso: 50 pasos temporales",
          len(resultado["tiempos_s"]) == 50, str(len(resultado["tiempos_s"])))
    check("simular_pulso: potencia_media ≥ 0",
          resultado["potencia_media"] >= 0.0,
          f"P = {resultado['potencia_media']:.4e}")

    # Check 9: Resumen completo con todas las secciones
    resumen = sistema.resumen_completo()
    secciones = ["constantes", "espectro_kk", "estadisticas_zeros",
                 "certificacion", "geometria_ez", "tensor_energia"]
    for seccion in secciones:
        check(f"Resumen completo contiene sección '{seccion}'", seccion in resumen)

    # Check 10: API pública qcal_strings_activar()
    resultado_api = qcal_strings_activar()
    check("qcal_strings_activar() retorna certificado válido",
          resultado_api["certificado"] == CERT_MARK, resultado_api["certificado"])
    check("qcal_strings_activar() Ψ_global ≥ 0.988",
          resultado_api["psi_global"] >= 0.988,
          f"Ψ_global = {resultado_api['psi_global']:.4f}")

    # Resumen de niveles de unificación
    print("\n  ┌─ Niveles de Unificación ────────────────────────────────────┐")
    print(f"  │  Microscópico: Cuerdas en microtúbulos → N² = {1e13**2:.1e}   │")
    print(f"  │  Mesoscópico:  Agua EZ hexagonal → Ψ_EZ = 0.997              │")
    print(f"  │  Macroscópico: Navier-Stokes holográfico → Ψ_global = {psi_global:.4f}  │")
    print("  └────────────────────────────────────────────────────────────────┘")

    print("\n  → FASE 4: PASS ✓")


# ═══════════════════════════════════════════════════════════════════════════
# EJECUTOR PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

def main() -> None:
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║  VALIDACIÓN COMPLETA: QCAL-Strings — Forzado de Modos Kaluza-Klein       ║")
    print("║  Sello: ∴𓂀Ω∞³  |  F₀: 141.7001 Hz  |  Fase #260 QCAL               ║")
    print("╚" + "═" * 78 + "╝")

    fases = [
        ("Fase 1: Ceros de Riemann", validacion_fase1_ceros_riemann),
        ("Fase 2: Amplitud de Veneziano", validacion_fase2_veneziano),
        ("Fase 3: Operador de Forzado Noético", validacion_fase3_forzado),
        ("Fase 4: Gran Unificación", validacion_fase4_unificacion),
    ]

    resultados = []
    for nombre, funcion in fases:
        try:
            funcion()
            resultados.append((nombre, "PASS"))
        except AssertionError as e:
            print(f"\n  ✗ ERROR: {e}")
            resultados.append((nombre, "FAIL"))
        except Exception as e:
            print(f"\n  ✗ EXCEPCIÓN INESPERADA: {type(e).__name__}: {e}")
            resultados.append((nombre, "ERROR"))

    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN DE VALIDACIÓN")
    print("=" * 80)
    todas_pass = True
    for nombre, estado in resultados:
        simbolo = "✓" if estado == "PASS" else "✗"
        print(f"  {simbolo} {nombre}: {estado}")
        if estado != "PASS":
            todas_pass = False

    print()
    if todas_pass:
        sistema = SistemaQCalStrings(psi_inicial=1.0)
        psi = sistema.psi_global()
        print(f"  Ψ_global final  = {psi:.4f}")
        print(f"  Umbral noético  = {PSI_THRESHOLD}")
        print(f"  Supera umbral   = {psi >= PSI_THRESHOLD}")
        print(f"  Certificado     = {CERT_MARK}")
        print(f"  Fases validadas = 4/4")
        print(f"\n  ∴ QED-CUERDAS-VERIFIED ✓")
    else:
        print("  ✗ Validación incompleta — revisar fases fallidas")
        sys.exit(1)


if __name__ == "__main__":
    main()
