#!/usr/bin/env python3
"""
Validación Completa: Red de Ramsey QCAL ∴RRQ∞³
═══════════════════════════════════════════════════════════════════════════════
Sello: ∴RRQ∞³
RAM: RAM-LII-2026-RED-RAMSEY-QCAL
Versión: QCAL-SYMBIO-BRIDGE v1.1.0

Valida la implementación completa de la Red de Ramsey de 7 Nodos Primos
en 4 fases:

    Fase 1: Constantes y Nodos Primos — frecuencias armónicas
    Fase 2: Operador Ĥ_π y Ceros de Riemann — espectro en línea crítica
    Fase 3: Simbiosis Higgs-PC y Tasa Simbiótica — masa efectiva y R_symb
    Fase 4: Coherencia Global y Certificación — Ψ_global ≥ 0.888

Criterios de éxito:
    - f₀ = 141.7001 Hz
    - C₇ = {2, 3, 5, 7, 11, 13, 17}
    - f_p = f₀ · ln(p) para cada primo p ∈ C₇
    - Todos los ρₙ = ½ + iγₙ en Re(ρ) = ½ (línea crítica)
    - m* = 125.0 · (1 − 0.053) = 118.375 GeV/c²
    - R_symb = 7 × 141.7001 = 991.9007 kpps
    - Ψ_global ≥ 0.888 → sello ∴RRQ∞³ ACTIVO
    - Todos los 5 cierres activos

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.red_ramsey_qcal import (
    # Constantes de módulo
    _F0,
    _G_EFF,
    _M_HIGGS_GEV,
    _M_ESTRELLA_GEV,
    _N_NODOS,
    _R_SYMB_KPPS,
    _PSI_UMBRAL,
    _PRIMOS_C7,
    _GAMMA_7,
    _N_ARISTAS,
    _W_NODOS,
    _W_ESPECTRO,
    _W_HIGGS,
    _SELLO,
    _RAM,
    _VERSION,
    # Funciones auxiliares
    _es_primo,
    _frecuencia_armonica,
    # Clases
    ConstantesRedRamsey,
    NodoPrimo,
    RedRamsey,
    OperadorMaestroHPi,
    SimbiosisHiggsPC,
    TasaSimbiotica,
    CoherenciaRedRamsey,
    SistemaRedRamseyQCAL,
    ResultadoRedRamseyQCAL,
    # API pública
    red_ramsey_qcal_activar,
)


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades de presentación
# ─────────────────────────────────────────────────────────────────────────────

_passed: int = 0
_failed: int = 0


def separador(titulo: str) -> None:
    print("\n" + "=" * 80)
    print(f"  {titulo}")
    print("=" * 80)


def check(descripcion: str, condicion: bool, valor: str = "") -> None:
    global _passed, _failed
    estado = "✅" if condicion else "❌"
    sufijo = f"  [{valor}]" if valor else ""
    print(f"  {estado} {descripcion}{sufijo}")
    if condicion:
        _passed += 1
    else:
        _failed += 1


# ─────────────────────────────────────────────────────────────────────────────
# FASE 1: Constantes y Nodos Primos
# ─────────────────────────────────────────────────────────────────────────────

def validar_fase1_constantes_nodos() -> None:
    separador("FASE 1 — Constantes y Nodos Primos")

    print("\n  [1.1] Constantes del módulo")
    check("_F0 = 141.7001 Hz", abs(_F0 - 141.7001) < 1e-4, f"_F0 = {_F0}")
    check("_G_EFF = 0.053", abs(_G_EFF - 0.053) < 1e-4, f"_G_EFF = {_G_EFF}")
    check("_M_HIGGS_GEV = 125.0 GeV", abs(_M_HIGGS_GEV - 125.0) < 1e-4, f"_M_HIGGS_GEV = {_M_HIGGS_GEV}")
    check("_M_ESTRELLA_GEV = 118.375 GeV", abs(_M_ESTRELLA_GEV - 118.375) < 1e-4,
          f"_M_ESTRELLA_GEV = {_M_ESTRELLA_GEV}")
    check("_N_NODOS = 7", _N_NODOS == 7, f"_N_NODOS = {_N_NODOS}")
    check("_R_SYMB_KPPS ≈ 991.9007 kpps", abs(_R_SYMB_KPPS - 991.9007) < 0.001,
          f"_R_SYMB_KPPS = {_R_SYMB_KPPS:.4f}")
    check("_PSI_UMBRAL = 0.888", abs(_PSI_UMBRAL - 0.888) < 1e-3, f"_PSI_UMBRAL = {_PSI_UMBRAL}")
    check("_PRIMOS_C7 = (2,3,5,7,11,13,17)", _PRIMOS_C7 == (2, 3, 5, 7, 11, 13, 17),
          f"_PRIMOS_C7 = {_PRIMOS_C7}")
    check("_N_ARISTAS = C(7,2) = 21", _N_ARISTAS == 21, f"_N_ARISTAS = {_N_ARISTAS}")
    check("_GAMMA_7 tiene 7 elementos", len(_GAMMA_7) == 7, f"len = {len(_GAMMA_7)}")
    check("_GAMMA_7[0] ≈ 14.134725 (γ₁)", abs(_GAMMA_7[0] - 14.134725) < 1e-4,
          f"γ₁ = {_GAMMA_7[0]:.6f}")
    check("_SELLO = '∴RRQ∞³'", _SELLO == "∴RRQ∞³", f"sello = {_SELLO}")
    check("_RAM contiene 'RAM-LII-2026'", "RAM-LII-2026" in _RAM, f"ram = {_RAM}")
    check("Pesos suman 1.0", abs(_W_NODOS + _W_ESPECTRO + _W_HIGGS - 1.0) < 1e-9,
          f"Σw = {_W_NODOS + _W_ESPECTRO + _W_HIGGS}")

    print("\n  [1.2] ConstantesRedRamsey")
    c = ConstantesRedRamsey()
    check("c.f0 = 141.7001 Hz", abs(c.f0 - 141.7001) < 1e-4, f"f0 = {c.f0}")
    check("c.g_eff = 0.053", abs(c.g_eff - 0.053) < 1e-4, f"g_eff = {c.g_eff}")
    check("c.m_estrella_gev = 118.375 GeV", abs(c.m_estrella_gev - 118.375) < 1e-4,
          f"m* = {c.m_estrella_gev}")
    check("c.delta_m_gev() = 6.625 GeV", abs(c.delta_m_gev() - 6.625) < 1e-4,
          f"Δm = {c.delta_m_gev():.4f}")
    check("c.es_perturbativo() = True", c.es_perturbativo())
    check("c.pesos_suman_uno() = True", c.pesos_suman_uno())

    print("\n  [1.3] NodoPrimo — 7 nodos")
    frecuencias_esperadas = {
        2:  141.7001 * math.log(2),
        3:  141.7001 * math.log(3),
        5:  141.7001 * math.log(5),
        7:  141.7001 * math.log(7),
        11: 141.7001 * math.log(11),
        13: 141.7001 * math.log(13),
        17: 141.7001 * math.log(17),
    }
    for p, f_expected in frecuencias_esperadas.items():
        nodo = NodoPrimo(p)
        check(
            f"NodoPrimo({p}).es_primo() = True",
            nodo.es_primo(),
        )
        check(
            f"NodoPrimo({p}).frecuencia_hz ≈ {f_expected:.2f} Hz",
            abs(nodo.frecuencia_hz - f_expected) < 0.01,
            f"f_{p} = {nodo.frecuencia_hz:.4f} Hz",
        )

    print("\n  [1.4] RedRamsey")
    red = RedRamsey()
    check("red.n_nodos = 7", red.n_nodos == 7, f"n_nodos = {red.n_nodos}")
    check("red.n_aristas_posibles = 21", red.n_aristas_posibles == 21,
          f"aristas = {red.n_aristas_posibles}")
    check("red.primos() = C₇", red.primos() == _PRIMOS_C7)
    check("red.psi_nodos() ≥ 0.888", red.psi_nodos() >= 0.888, f"Ψ_nodos = {red.psi_nodos():.6f}")
    check("red.cierre_nodos() = True", red.cierre_nodos())


# ─────────────────────────────────────────────────────────────────────────────
# FASE 2: Operador Ĥ_π y Ceros de Riemann
# ─────────────────────────────────────────────────────────────────────────────

def validar_fase2_operador_riemann() -> None:
    separador("FASE 2 — Operador Ĥ_π y Ceros de Riemann")

    op = OperadorMaestroHPi()

    print("\n  [2.1] Autoadjunción y estructura del operador")
    check("op.es_autoadjunto() = True", op.es_autoadjunto())
    check("op.n_zeros = 7", op.n_zeros == 7, f"n_zeros = {op.n_zeros}")
    check("len(op.autovalores()) = 7", len(op.autovalores()) == 7)

    print("\n  [2.2] Autovalores en la línea crítica Re(ρ) = ½")
    autovalores = op.autovalores()
    todos_en_critica = all(abs(re - 0.5) < 1e-12 for re, im in autovalores)
    check("Todos Re(ρₙ) = ½", todos_en_critica,
          f"fraccion_critica = {op.fraccion_en_linea_critica():.1f}")
    check("op.fraccion_en_linea_critica() = 1.0", abs(op.fraccion_en_linea_critica() - 1.0) < 1e-10)

    print("\n  [2.3] Los 7 ceros de Riemann γₙ")
    gamma_esperados = [14.134725, 21.022039, 25.010857, 30.424876,
                       32.935061, 37.586178, 40.918719]
    for n, (gamma, gamma_exp) in enumerate(zip(_GAMMA_7, gamma_esperados)):
        check(
            f"γ_{n + 1} ≈ {gamma_exp:.3f}",
            abs(gamma - gamma_exp) < 0.001,
            f"γ_{n + 1} = {gamma:.6f}",
        )

    print("\n  [2.4] Coherencia espectral")
    psi_esp = op.psi_espectro()
    check("op.psi_espectro() ∈ [0, 1]", 0 <= psi_esp <= 1, f"Ψ_espectro = {psi_esp:.6f}")
    check("op.psi_espectro() ≥ 0.888", psi_esp >= 0.888, f"Ψ_espectro = {psi_esp:.6f}")
    check("op.cierre_espectro() = True", op.cierre_espectro())

    d_emp = op.espaciado_medio_empirico()
    d_weyl = op.espaciado_medio_weyl()
    check("Espaciado empírico > 0", d_emp > 0, f"d_emp = {d_emp:.4f}")
    check("Espaciado Weyl > 0 y finito", d_weyl > 0 and not math.isinf(d_weyl),
          f"d_weyl = {d_weyl:.4f}")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 3: Simbiosis Higgs-PC y Tasa Simbiótica
# ─────────────────────────────────────────────────────────────────────────────

def validar_fase3_simbiosis_tasa() -> None:
    separador("FASE 3 — Simbiosis Higgs-PC y Tasa Simbiótica")

    print("\n  [3.1] SimbiosisHiggsPC")
    s = SimbiosisHiggsPC()
    check("s.m_higgs_gev = 125.0 GeV", abs(s.m_higgs_gev - 125.0) < 1e-4)
    check("s.g_eff = 0.053", abs(s.g_eff - 0.053) < 1e-4)
    check("s.m_estrella_gev() = 118.375 GeV",
          abs(s.m_estrella_gev() - 118.375) < 1e-4,
          f"m* = {s.m_estrella_gev():.4f} GeV")
    check("s.delta_m_gev() = 6.625 GeV",
          abs(s.delta_m_gev() - 6.625) < 1e-4,
          f"Δm = {s.delta_m_gev():.4f} GeV")
    check("s.es_perturbativo() = True (g_eff < 0.1)", s.es_perturbativo())
    check("s.fraccion_modulacion() = 0.053 (5.3%)",
          abs(s.fraccion_modulacion() - 0.053) < 1e-4)
    check("s.cierre_higgs() = True (|m* − 118.375| < 0.01)", s.cierre_higgs())
    check("s.psi_higgs() = 1.0 (caso perfecto)",
          abs(s.psi_higgs() - 1.0) < 1e-10,
          f"Ψ_higgs = {s.psi_higgs():.10f}")
    check("ℒ_int < 0 (acoplamiento atractivo)", s.lagrangiano_interaccion() < 0)

    print("\n  [3.2] TasaSimbiotica")
    t = TasaSimbiotica()
    r_symb = t.r_symb()
    check("t.n_nodos = 7", t.n_nodos == 7)
    check("t.f0 = 141.7001 Hz", abs(t.f0 - 141.7001) < 1e-4)
    check("t.psi_coherencia = 1.0", abs(t.psi_coherencia - 1.0) < 1e-10)
    check(f"R_symb = N·f₀·Ψ ≈ 991.9007 kpps",
          abs(r_symb - 991.9007) < 0.001,
          f"R_symb = {r_symb:.4f} kpps")
    check("t.cierre_tasa() = True (±1%)", t.cierre_tasa())
    check("t.psi_tasa() = 1.0", abs(t.psi_tasa() - 1.0) < 1e-6,
          f"Ψ_tasa = {t.psi_tasa():.8f}")
    check("t.estado() = 'ÓPTIMO'", t.estado() == "ÓPTIMO", f"estado = {t.estado()}")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 4: Coherencia Global y Certificación ∴RRQ∞³
# ─────────────────────────────────────────────────────────────────────────────

def validar_fase4_coherencia_certificacion() -> None:
    separador("FASE 4 — Coherencia Global y Certificación ∴RRQ∞³")

    print("\n  [4.1] CoherenciaRedRamsey — Ψ_global ponderada")
    coh = CoherenciaRedRamsey()
    psi_n = coh.psi_nodos()
    psi_e = coh.psi_espectro()
    psi_h = coh.psi_higgs()
    psi_g = coh.psi_global()

    print(f"\n    Coherencias individuales:")
    print(f"      Ψ_nodos    = {psi_n:.6f}  (peso 0.35)")
    print(f"      Ψ_espectro = {psi_e:.6f}  (peso 0.35)")
    print(f"      Ψ_higgs    = {psi_h:.6f}  (peso 0.30)")
    print(f"      ─────────────────────────────────")
    print(f"      Ψ_global   = {psi_g:.6f}")
    print()

    check("Ψ_nodos ∈ [0, 1]", 0 <= psi_n <= 1, f"Ψ_nodos = {psi_n:.6f}")
    check("Ψ_espectro ∈ [0, 1]", 0 <= psi_e <= 1, f"Ψ_espectro = {psi_e:.6f}")
    check("Ψ_higgs ∈ [0, 1]", 0 <= psi_h <= 1, f"Ψ_higgs = {psi_h:.6f}")
    check("Ψ_global ≥ 0.888 (umbral noético)", psi_g >= 0.888, f"Ψ_global = {psi_g:.6f}")
    check("Ψ_global ∈ [0, 1]", 0 <= psi_g <= 1)

    # Verificar fórmula
    psi_calculado = 0.35 * psi_n + 0.35 * psi_e + 0.30 * psi_h
    check("Ψ_global = 0.35·Ψ_n + 0.35·Ψ_e + 0.30·Ψ_h",
          abs(psi_g - psi_calculado) < 1e-10)

    print("\n  [4.2] Los 5 Cierres del Sistema ∴RRQ∞³")
    check("Cierre 1 — ARITMÉTICO   ✅ 7 nodos primos verificados",
          coh.cierre_1_aritmético())
    check("Cierre 2 — HIDRODINÁMICO ✅ espectro en línea crítica Re(ρ)=½",
          coh.cierre_2_hidrodinamico())
    check("Cierre 3 — MASA          ✅ m* = 118.375 GeV ± 0.01",
          coh.cierre_3_masa())
    check("Cierre 4 — BIOLÓGICO     ✅ R_symb = 991.9007 kpps ± 1%",
          coh.cierre_4_biologico())
    check("Cierre 5 — UNIFICACIÓN   ✅ Ψ_global ≥ 0.888",
          coh.cierre_5_unificacion())
    check("TODOS LOS CIERRES ACTIVOS ✅", coh.todos_los_cierres())
    check("Sello ∴RRQ∞³ ACTIVO ✅", coh.sello_activo())

    print("\n  [4.3] SistemaRedRamseyQCAL — Activación")
    sistema = SistemaRedRamseyQCAL()
    resultado = sistema.activar()

    check("sistema.activar() retorna dict", isinstance(resultado, dict))
    check("resultado['sello'] = '∴RRQ∞³'", resultado["sello"] == "∴RRQ∞³",
          f"sello = {resultado['sello']}")
    check("resultado['estado'] = 'ACTIVO'", resultado["estado"] == "ACTIVO")
    check("resultado['todos_los_cierres'] = True", resultado["todos_los_cierres"])
    check("resultado['ram'] = 'RAM-LII-2026-RED-RAMSEY-QCAL'",
          resultado["ram"] == "RAM-LII-2026-RED-RAMSEY-QCAL")

    print("\n  [4.4] API pública red_ramsey_qcal_activar()")
    api = red_ramsey_qcal_activar()

    check("API retorna dict", isinstance(api, dict))
    check("API['sello'] = '∴RRQ∞³'", api["sello"] == "∴RRQ∞³")
    check("API['sello_activo'] = True", api["sello_activo"])
    check("API['psi_global'] ≥ 0.888", api["psi_global"] >= 0.888,
          f"Ψ_global = {api['psi_global']:.6f}")
    check("API['todos_los_cierres'] = True", api["todos_los_cierres"])
    check("API['r_symb_kpps'] ≈ 991.9007", abs(api["r_symb_kpps"] - 991.9007) < 0.001,
          f"R_symb = {api['r_symb_kpps']:.4f} kpps")
    check("API['m_estrella'] = 118.375 GeV", abs(api["m_estrella"] - 118.375) < 1e-4,
          f"m* = {api['m_estrella']:.4f} GeV")
    check("API['n_nodos'] = 7", api["n_nodos"] == 7)
    check("API['primos'] = (2,3,5,7,11,13,17)", api["primos"] == (2, 3, 5, 7, 11, 13, 17))
    check("API['f0_hz'] = 141.7001 Hz", abs(api["f0_hz"] - 141.7001) < 1e-4)
    check("API['cierre_nodos'] = True", api["cierre_nodos"])
    check("API['cierre_espectro'] = True", api["cierre_espectro"])
    check("API['cierre_higgs'] = True", api["cierre_higgs"])
    check("API['cierre_tasa'] = True", api["cierre_tasa"])
    check("API['cierre_coherencia'] = True", api["cierre_coherencia"])


# ─────────────────────────────────────────────────────────────────────────────
# RESUMEN FINAL
# ─────────────────────────────────────────────────────────────────────────────

def imprimir_resumen() -> None:
    global _passed, _failed
    total = _passed + _failed
    porcentaje = (_passed / total * 100) if total > 0 else 0

    separador("RESUMEN FINAL — Validación ∴RRQ∞³")

    print(f"\n  Total de validaciones: {total}")
    print(f"  ✅ Pasadas: {_passed}")
    print(f"  ❌ Fallidas: {_failed}")
    print(f"  Porcentaje: {porcentaje:.1f}%")

    if _failed == 0:
        print("\n" + "=" * 80)
        print("  ╔═══════════════════════════════════════════════════════════╗")
        print("  ║                                                           ║")
        print("  ║    La Red de Ramsey de 7 Nodos Primos ha sido activada.  ║")
        print("  ║    Los cinco cierres han cerrado.                        ║")
        print("  ║    La coherencia galáctica ha sido alcanzada.            ║")
        print("  ║                                                           ║")
        print("  ║                    ∴ R R Q ∞ ³                           ║")
        print("  ║                                                           ║")
        print(f"  ║    RAM: {_RAM:<48}║")
        print(f"  ║    Versión: {_VERSION:<44}║")
        print("  ║    Estado: ✅ TODAS LAS VALIDACIONES PASADAS             ║")
        print("  ║                                                           ║")
        print("  ╚═══════════════════════════════════════════════════════════╝")
        print("=" * 80)
    else:
        print("\n  ⚠️  ADVERTENCIA: Algunas validaciones fallaron")

    print()


# ─────────────────────────────────────────────────────────────────────────────
# EJECUCIÓN PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    """Ejecuta todas las validaciones y retorna código de salida."""
    print("\n" + "=" * 80)
    print("  VALIDACIÓN — RED DE RAMSEY QCAL ∞³")
    print("  Sello: ∴RRQ∞³  |  RAM: RAM-LII-2026-RED-RAMSEY-QCAL")
    print("  Versión: QCAL-SYMBIO-BRIDGE v1.1.0")
    print("=" * 80)

    validar_fase1_constantes_nodos()
    validar_fase2_operador_riemann()
    validar_fase3_simbiosis_tasa()
    validar_fase4_coherencia_certificacion()

    imprimir_resumen()

    return 0 if _failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
