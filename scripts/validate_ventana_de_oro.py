#!/usr/bin/env python3
"""
Validación del módulo physics.ventana_de_oro — ∴VDO∞³
===============================================================================

Valida la implementación del módulo physics.ventana_de_oro contra los
criterios teóricos del sistema Ventana de Oro (Golden Window):

  Fase 1 — Constantes fundamentales y canal de información
  Fase 2 — Umbral térmico y firma espectral (Eco de Noesis88)
  Fase 3 — Red de Ramsey (7 nodos) y ventana de transparencia
  Fase 4 — Antena de fase, coherencia global y certificación ∴VDO∞³

Criterios de éxito:
  - f₀ = 141.7001 Hz                            [exacto]
  - Cd ≈ 141.7001 Mbits/s                        [< 0.01 Mbits/s]
  - T_crit ≈ 300 K                               [< 0.1 K]
  - m_PC ≈ 5.86×10⁻¹³ eV                        [< 1×10⁻¹⁴ eV]
  - det(V) = 1.0                                  [< 10⁻¹⁰]
  - V·Vᵀ = I₇  (error < 10⁻¹⁰)                  [< 10⁻¹⁰]
  - f_det = 141.7001 Hz                           [< 10⁻⁴ Hz]
  - σ_ext ≈ 6.4×10⁻¹³ m²                        [< 10⁻¹⁴ m²]
  - Ψ_global ≥ 0.888                              [≥ 0.888]
  - sello_activo = True

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0
FECHA/DATE: 2026-04-01
"""

import math
import sys
import os
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from physics.ventana_de_oro import (
    ConstantesVentanaOro,
    CapacidadCanal,
    UmbralTermico,
    FirmaEspectral,
    RedRamsey7Nodos,
    VentanaTransparencia,
    AntenaFase,
    CoherenciaVentanaOro,
    SistemaVentanaDeOro,
    ventana_de_oro_activar,
)

# ─────────────────────────────────────────────────────────────────────────────
# Utilidades de reporte
# ─────────────────────────────────────────────────────────────────────────────

_PASS = "  ✓"
_FAIL = "  ✗"
_resultados: dict = {"pasados": 0, "fallados": 0, "errores": []}


def verificar(descripcion: str, condicion: bool, detalle: str = "") -> bool:
    if condicion:
        print(f"{_PASS} {descripcion}")
        _resultados["pasados"] += 1
    else:
        msg = f"{_FAIL} FALLA: {descripcion}"
        if detalle:
            msg += f"  ({detalle})"
        print(msg)
        _resultados["fallados"] += 1
        _resultados["errores"].append(descripcion)
    return condicion


def verificar_aprox(descripcion: str, valor: float, esperado: float,
                    delta: float, unidades: str = "") -> bool:
    ok = abs(valor - esperado) <= delta
    det = f"obtenido={valor:.6g}{unidades}, esperado={esperado:.6g}{unidades}, Δ={abs(valor-esperado):.3g}"
    return verificar(descripcion, ok, detalle=det if not ok else "")


def seccion(titulo: str) -> None:
    print(f"\n{'─'*70}")
    print(f"  {titulo}")
    print(f"{'─'*70}")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 1: Constantes fundamentales y canal de información
# ─────────────────────────────────────────────────────────────────────────────

def fase_1_constantes_y_canal() -> bool:
    seccion("FASE 1 — Constantes fundamentales y canal de información")

    try:
        c = ConstantesVentanaOro()
        canal = CapacidadCanal(c)

        # Frecuencias
        verificar_aprox("f₀ = 141.7001 Hz", c.F0_HZ, 141.7001, 1.0e-4, " Hz")
        verificar_aprox("f₀_kHz = 141700.1 Hz", c.F0_KHZ, 141700.1, 0.01, " Hz")
        ratio = c.F0_KHZ / c.F0_HZ
        verificar_aprox("f₀_kHz / f₀ = 1000 (escalado)", ratio, 1000.0, 0.1)

        # Período
        t_esperado = 1.0 / c.F0_KHZ
        verificar_aprox("T_periodo_kHz = 1/f₀_kHz ≈ 7.057 μs",
                        c.T_PERIODO_KHZ_S, t_esperado, 1.0e-12, " s")

        # Parámetros del canal
        verificar_aprox("τ_pulse = 1 ns", c.TAU_PULSE_S, 1.0e-9, 1.0e-12, " s")
        verificar_aprox("log₂(1+SNR) = 1000 bits/muestra",
                        c.LOG2_SNR_QUANTUM, 1000.0, 1.0e-6)
        verificar_aprox("Ψ_coherencia = 0.999999",
                        c.PSI_COHERENCIA, 0.999999, 1.0e-8)

        # Parámetros de acoplamiento
        verificar_aprox("g_eff = 0.053", c.G_EFF, 0.053, 1.0e-4)
        verificar_aprox("m_H = 125 GeV", c.M_HIGGS_GEV, 125.0, 0.1, " GeV")

        # Capacidad del canal
        bps = canal.bits_por_muestra()
        verificar_aprox("bits_por_muestra() = 1000", bps, 1000.0, 1.0e-6)

        cd = canal.cd_mbits_por_segundo()
        verificar_aprox("Cd ≈ 141.7001 Mbits/s", cd, 141.7001, 0.01, " Mbits/s")

        fc = canal.factor_ciclo()
        fc_esperado = c.TAU_PULSE_S * c.F0_KHZ
        verificar_aprox("factor_ciclo = τ × f₀_kHz ≈ 1.417×10⁻⁴",
                        fc, fc_esperado, 1.0e-8)
        verificar("factor_ciclo ∈ (0, 1)", 0.0 < fc < 1.0)

        # Relación Cd = log₂(SNR) × f₀_kHz / 1e6
        cd_formula = c.LOG2_SNR_QUANTUM * c.F0_KHZ / 1.0e6
        verificar_aprox("Cd = log₂(SNR) × f₀_kHz / 1e6 (consistencia)",
                        cd, cd_formula, 0.001, " Mbits/s")

        print(f"\n  → Cd = {cd:.6f} Mbits/s  [criterio: 141.7001 ± 0.01 Mbits/s]")
        return True

    except Exception as exc:
        print(f"\n  ✗ ERROR en Fase 1: {exc}")
        traceback.print_exc()
        _resultados["fallados"] += 1
        return False


# ─────────────────────────────────────────────────────────────────────────────
# FASE 2: Umbral térmico y firma espectral
# ─────────────────────────────────────────────────────────────────────────────

def fase_2_termico_y_espectral() -> bool:
    seccion("FASE 2 — Umbral térmico y firma espectral (Eco de Noesis88)")

    try:
        c = ConstantesVentanaOro()
        termico = UmbralTermico(c)
        espectral = FirmaEspectral(c)

        # Umbral térmico
        e_ev = termico.energia_acoplamiento_ev()
        verificar_aprox("E_cond ≈ 0.488 eV", e_ev, 0.488, 0.01, " eV")

        t_crit = termico.calcular_t_crit()
        verificar_aprox("T_crit ≈ 300 K", t_crit, 300.0, 0.1, " K")

        verificar("Condensado estable a 300 K (ambiente)",
                  termico.es_estable_ambiente(300.0))
        verificar("Condensado inestable a 301 K",
                  not termico.es_estable_ambiente(301.0))
        verificar("Condensado estable a 77 K (N₂ líquido)",
                  termico.es_estable_ambiente(77.0))

        # Consistencia: g_eff × E_cond / k_B = T_crit
        k_b = 1.380649e-23
        t_calc = (c.G_EFF * c.E_COND_J) / k_b
        verificar_aprox("T_crit reconstruido = g_eff × E_cond / k_B",
                        t_calc, t_crit, 0.01, " K")

        # Firma espectral
        m_pc = espectral.masa_pc_ev()
        verificar_aprox("m_PC = ℏω₀ ≈ 5.86×10⁻¹³ eV",
                        m_pc, 5.86e-13, 5.0e-15, " eV")
        verificar("m_PC > 0", m_pc > 0.0)

        sep = espectral.separacion_ev()
        verificar_aprox("ΔE_sideband ≈ 5.86×10⁻¹³ eV",
                        sep, 5.86e-13, 5.0e-15, " eV")
        verificar("ΔE_sideband = m_PC (coherencia ℏω₀)",
                  abs(sep - m_pc) < 1.0e-16)

        m_minus, m_plus = espectral.sidebands_gev()
        verificar("m_minus construido como m_H − delta (algebraico)",
                  m_minus == c.M_HIGGS_GEV - espectral.energia_sideband_gev())
        verificar("m_plus construido como m_H + delta (algebraico)",
                  m_plus == c.M_HIGGS_GEV + espectral.energia_sideband_gev())
        simetria = abs((m_plus - c.M_HIGGS_GEV) - (c.M_HIGGS_GEV - m_minus))
        verificar_aprox("Sidebands simétricos respecto a m_H",
                        simetria, 0.0, 1.0e-30, " GeV")

        eco = espectral.detectar_eco_noesis88()
        verificar("Eco de Noesis88 devuelve dict completo",
                  all(k in eco for k in ("m_higgs_gev", "m_pc_ev",
                                         "delta_e_ev", "m_minus_gev",
                                         "m_plus_gev", "omega_0_rad_s")))

        omega_esperado = 2.0 * math.pi * c.F0_HZ
        verificar_aprox("ω₀ = 2π × f₀ ≈ 890.33 rad/s",
                        eco["omega_0_rad_s"], omega_esperado, 0.01, " rad/s")

        print(f"\n  → m_PC = {m_pc:.3e} eV  [criterio: (5.86 ± 0.05)×10⁻¹³ eV]")
        print(f"  → T_crit = {t_crit:.1f} K  [criterio: 300 ± 0.1 K]")
        return True

    except Exception as exc:
        print(f"\n  ✗ ERROR en Fase 2: {exc}")
        traceback.print_exc()
        _resultados["fallados"] += 1
        return False


# ─────────────────────────────────────────────────────────────────────────────
# FASE 3: Red de Ramsey y ventana de transparencia
# ─────────────────────────────────────────────────────────────────────────────

def fase_3_red_y_ventana() -> bool:
    seccion("FASE 3 — Red de Ramsey (7 nodos) y ventana de transparencia")

    try:
        c = ConstantesVentanaOro()
        red = RedRamsey7Nodos(c)
        ventana = VentanaTransparencia(c)

        # Matriz de traslación
        V = red.matriz_traslacion()
        verificar("V tiene forma 7×7", len(V) == 7 and all(len(r) == 7 for r in V))

        # Estructura cíclica
        n = 7
        estructura_ok = all(
            V[i][(i + 1) % n] == 1.0 and
            all(V[i][j] == 0.0 for j in range(n) if j != (i + 1) % n)
            for i in range(n)
        )
        verificar("V es desplazamiento cíclico V[i][(i+1)%7]=1", estructura_ok)

        # Determinante
        det = red.verificar_determinante()
        verificar_aprox("det(V) = +1", det, 1.0, 1.0e-10)

        # Ortogonalidad
        err_ort = red.verificar_ortogonalidad()
        verificar(f"V·Vᵀ = I₇ (error < 10⁻¹⁰, obtenido: {err_ort:.2e})",
                  err_ort < 1.0e-10)

        res_red = red.resumen()
        verificar("red.resumen()['es_unitaria'] = True", res_red["es_unitaria"])

        # Masa efectiva mínima
        m_min = red.masa_efectiva_minima_gev()
        m_min_esperado = c.M_HIGGS_GEV * (1.0 - c.G_EFF)
        verificar_aprox("m*_min = m_H(1−g_eff) ≈ 118.375 GeV",
                        m_min, m_min_esperado, 0.001, " GeV")

        # Energía por nodo
        e_nodo = red.energia_por_nodo_j()
        verificar("E_nodo = E_PC / 7 > 0", e_nodo > 0.0)
        verificar_aprox("7 × E_nodo = E_PC (conservación energía)",
                        7.0 * e_nodo, c.E_PC_J, 1.0e-35, " J")

        # Ventana de transparencia
        f_det = ventana.calcular_f_det()
        verificar_aprox("f_det = 141.7001 Hz (batido heterodino)",
                        f_det, 141.7001, 1.0e-4, " Hz")
        verificar("ventana.verificar_coincidencia_f0() = True",
                  ventana.verificar_coincidencia_f0())

        # Formula del batido: |f_vac − N × f_mat|
        f_det_manual = abs(c.F_VAC_HZ - c.N_BATIDO * c.F_MAT_HZ)
        verificar_aprox("f_det manual = |1.05 GHz − 7×f_mat|",
                        f_det_manual, c.F0_HZ, 1.0e-4, " Hz")

        # f_mat ≈ 150 MHz
        verificar_aprox("f_mat ≈ 150 MHz (red de carbono)",
                        c.F_MAT_HZ / 1.0e6, 150.0, 0.01, " MHz")

        # Factor de sincronización
        fs = ventana.factor_sincronizacion()
        verificar("Ψ_ventana = 1 − τ·f₀ ∈ (0.9999, 1]",
                  0.9999 < fs <= 1.0)

        # Ancho de ventana
        ancho = ventana.ancho_ventana_hz()
        verificar_aprox("Ancho ventana = f₀ × g_eff ≈ 7.5 Hz",
                        ancho, c.F0_HZ * c.G_EFF, 0.01, " Hz")

        print(f"\n  → f_det = {f_det:.4f} Hz  [criterio: 141.7001 ± 10⁻⁴ Hz]")
        print(f"  → det(V) = {det:.1f}, error_ort = {err_ort:.2e}")
        return True

    except Exception as exc:
        print(f"\n  ✗ ERROR en Fase 3: {exc}")
        traceback.print_exc()
        _resultados["fallados"] += 1
        return False


# ─────────────────────────────────────────────────────────────────────────────
# FASE 4: Antena de fase, coherencia global y certificación
# ─────────────────────────────────────────────────────────────────────────────

def fase_4_antena_coherencia_certificacion() -> bool:
    seccion("FASE 4 — Antena de fase, coherencia global y certificación ∴VDO∞³")

    try:
        c = ConstantesVentanaOro()
        antena = AntenaFase(c)
        coh = CoherenciaVentanaOro(c)

        # Antena de fase
        sigma = antena.calcular_sigma_ext()
        verificar_aprox("σ_ext ≈ 6.4×10⁻¹³ m²",
                        sigma, 6.4e-13, 1.0e-14, " m²")
        verificar_aprox("σ_ext = ξ × A_antena (consistencia)",
                        sigma, c.SIGMA_EXT_M2, 1.0e-15, " m²")

        a_ant = antena.apertura_antena_m2()
        verificar_aprox("A_antena = σ_ext / ξ ≈ 1.208×10⁻¹¹ m²",
                        a_ant, c.SIGMA_EXT_M2 / c.XI_COOPERATIVIDAD, 1.0e-13, " m²")

        dim = antena.dimension_lineal_m() * 1.0e6
        verificar_aprox("Dimensión lineal ≈ 3.476 μm (micrométrica)",
                        dim, 3.476, 0.01, " μm")

        sg = antena.seccion_geometrica_m2()
        verificar_aprox("σ_geo = σ_ext / 10⁶ ≈ 6.4×10⁻¹⁹ m²",
                        sg, 6.4e-19, 1.0e-20, " m²")

        k = antena.factor_amplificacion()
        verificar_aprox("Factor K = 10⁶ (6 órdenes de magnitud)",
                        k, 1.0e6, 1.0)
        verificar_aprox("log₁₀(K) = 6", antena.ordenes_de_magnitud(), 6.0, 1.0e-6)

        v_opt = antena.potencial_electrostrictivo(1.0e6)
        verificar("Potencial electrostriccivo > 0 para E>0", v_opt > 0.0)

        # Coherencia global – componentes individuales
        comps = coh.componentes()
        for nombre, valor in comps.items():
            verificar(f"{nombre} ∈ (0.888, 1] (={valor:.4f})",
                      0.888 < valor <= 1.0)

        # Valores específicos
        verificar_aprox("Ψ_canal = PSI_COHERENCIA = 0.999999",
                        coh.psi_canal(), 0.999999, 1.0e-7)
        verificar_aprox("Ψ_termico = 300/301 ≈ 0.9967",
                        coh.psi_termico(), 300.0 / 301.0, 1.0e-6)
        verificar_aprox("Ψ_espectral = 1 − g_eff² ≈ 0.9972",
                        coh.psi_espectral(), 1.0 - 0.053 ** 2, 1.0e-6)
        verificar_aprox("Ψ_red = 48/49 ≈ 0.9796",
                        coh.psi_red(), 48.0 / 49.0, 1.0e-6)
        verificar("Ψ_ventana ≈ 1 (> 0.9999)", coh.psi_ventana() > 0.9999)
        verificar_aprox("Ψ_antena = 1 − ξ² ≈ 0.9972",
                        coh.psi_antena(), 1.0 - 0.053 ** 2, 1.0e-6)

        # Coherencia global
        psi_g = coh.psi_global()
        verificar_aprox("Ψ_global ≈ 0.995", psi_g, 0.995, 0.005)
        verificar(f"Ψ_global = {psi_g:.6f} ≥ 0.888 (umbral)", psi_g >= 0.888)

        # Media geométrica
        product = 1.0
        for v in comps.values():
            product *= v
        psi_geom = product ** (1.0 / len(comps))
        verificar_aprox("Ψ_global = media geométrica (6 componentes)",
                        psi_g, psi_geom, 1.0e-8)

        # Sello
        verificar("sello_activo() = True", coh.sello_activo())

        # API pública
        r = ventana_de_oro_activar()
        verificar("ventana_de_oro_activar() devuelve dict", isinstance(r, dict))
        verificar("sello = '∴VDO∞³'", r["sello"] == "∴VDO∞³")
        verificar("sello_activo = True", r["sello_activo"])
        verificar_aprox("API: Cd ≈ 141.7001 Mbits/s",
                        r["cd_mbits_per_sec"], 141.7001, 0.01, " Mbits/s")
        verificar_aprox("API: T_crit ≈ 300 K",
                        r["t_crit_k"], 300.0, 0.1, " K")
        verificar("API: red_unitaria = True", r["red_unitaria"])
        verificar("API: coincide_f0 = True", r["coincide_f0"])
        verificar_aprox("API: σ_ext ≈ 6.4×10⁻¹³ m²",
                        r["sigma_ext_m2"], 6.4e-13, 1.0e-14, " m²")
        verificar_aprox("API: Ψ_global ≥ 0.888",
                        r["psi_global"], 0.995, 0.005)
        verificar("API: certificacion contiene '∴VDO∞³'",
                  "∴VDO∞³" in r["certificacion"])

        print(f"\n  → Ψ_global = {psi_g:.6f}  [criterio: ≥ 0.888]")
        print(f"  → σ_ext = {sigma:.2e} m²  [criterio: 6.4×10⁻¹³ ± 10⁻¹⁴ m²]")
        return True

    except Exception as exc:
        print(f"\n  ✗ ERROR en Fase 4: {exc}")
        traceback.print_exc()
        _resultados["fallados"] += 1
        return False


# ─────────────────────────────────────────────────────────────────────────────
# RESUMEN FINAL
# ─────────────────────────────────────────────────────────────────────────────

def imprimir_resumen(fases_ok: list) -> None:
    total_v = _resultados["pasados"] + _resultados["fallados"]
    print("\n" + "=" * 70)
    print("  RESUMEN DE VALIDACIÓN — ∴VDO∞³")
    print("=" * 70)

    estados = ["✓" if ok else "✗" for ok in fases_ok]
    for i, (ok, estado) in enumerate(zip(fases_ok, estados), 1):
        etiquetas = [
            "Constantes y canal de información",
            "Umbral térmico y firma espectral",
            "Red de Ramsey y ventana de transparencia",
            "Antena de fase, coherencia y certificación",
        ]
        print(f"  Fase {i}: {estado} {etiquetas[i-1]}")

    print()
    print(f"  Verificaciones: {_resultados['pasados']}/{total_v} pasadas")

    if _resultados["errores"]:
        print(f"\n  Fallos ({len(_resultados['errores'])}):")
        for e in _resultados["errores"]:
            print(f"    ✗ {e}")

    todas_ok = all(fases_ok) and _resultados["fallados"] == 0
    print()
    if todas_ok:
        print("  ╔═══════════════════════════════════════════════════╗")
        print("  ║  ∴VDO∞³ VALIDACIÓN COMPLETA — 4/4 FASES         ║")
        print("  ║  VENTANA DE ORO: CERTIFICADA ∴𓂀Ω∞³Φ              ║")
        print("  ╚═══════════════════════════════════════════════════╝")
    else:
        n_ok = sum(1 for ok in fases_ok if ok)
        print(f"  ✗ Validación incompleta: {n_ok}/4 fases,",
              f"{_resultados['fallados']} verificaciones falladas")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    print()
    print("=" * 70)
    print("  VALIDACIÓN: physics.ventana_de_oro — ∴VDO∞³")
    print("  RAM: RAM-XLIX-2026-VENTANA-DE-ORO")
    print("  Ventana de Oro: Canal Higgs-PC a 141.7001 Hz / 141.7001 kHz")
    print("=" * 70)

    fases = [
        fase_1_constantes_y_canal,
        fase_2_termico_y_espectral,
        fase_3_red_y_ventana,
        fase_4_antena_coherencia_certificacion,
    ]

    fases_ok = []
    for fase_fn in fases:
        ok = fase_fn()
        fases_ok.append(ok)

    imprimir_resumen(fases_ok)

    return 0 if all(fases_ok) and _resultados["fallados"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
