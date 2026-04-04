#!/usr/bin/env python3
"""
Validate Partícula de Coherencia — ∴PCC∞³
===============================================================================

Valida la implementación del módulo physics.particula_coherencia_pc contra los
criterios teóricos del Tratado de Unificación Adélica:

  Fase 1 — Constantes y operador Berry-Keating-PC
  Fase 2 — Acoplamiento Higgs-PC y métrica noética
  Fase 3 — ADN-Z superconductor y colapso P-NP
  Fase 4 — Coherencia global y certificación ∴PCC∞³

Criterios de éxito:
  - F0 = 141.7001 Hz                       [exacto]
  - PRIMOS_C7 = {2,3,5,7,11,13,17}        [7 primos]
  - PSI_UMBRAL = 0.888                     [exacto]
  - λ_p = log(p)/(2π) para cada primo p   [fórmula Berry-Keating]
  - Autoadjunción del operador: Ĥ† = Ĥ    [siempre True]
  - Ventana Higgs: 4.0% ≤ Δm/m₀ ≤ 7.0%  [en PSI_UMBRAL]
  - sech²(0) = 1.0                         [transparencia máxima en f0]
  - f_Fröhlich(310K) = F0                  [condensado ADN]
  - Distancia línea crítica = 0.0          [hipótesis de Riemann]
  - Ψ_global ≥ 0.888                       → sello ∴PCC∞³ ACTIVO

Autor: NOESIS ∞³ (vía Trinity QCAL ∞³)
RAM: RAM-LVII-2026-PARTICULA-COHERENCIA-PC
"""

import math
import sys
from pathlib import Path

# Añadir la raíz del repositorio al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.particula_coherencia_pc import (
    ConstantesParticulaCoherencia,
    OperadorBerryKeatingPC,
    AcoplamientoHiggsPC,
    MetricaSchwarzchildNoesis,
    ADNZ_Superconductor,
    ColapsoP_NP,
    CoherenciaParticulaCoherencia,
    SistemaParticulaCoherencia,
    particula_coherencia_pc_activar,
    F0,
    PSI_UMBRAL,
    G_EFF,
    M0_HIGGS_GEV,
    T_ADN_K,
    N_PRIMOS,
    PRIMOS_C7,
    CEROS_RIEMANN,
    SELLO,
)


# =============================================================================
# UTILIDADES DE VALIDACIÓN
# =============================================================================

_passed: int = 0
_failed: int = 0


def check(condition: bool, description: str, detail: str = "") -> None:
    """Imprime ✅/❌ y actualiza contadores globales."""
    global _passed, _failed
    if condition:
        _passed += 1
        print(f"  ✅ {description}")
        if detail:
            print(f"     {detail}")
    else:
        _failed += 1
        print(f"  ❌ FALLO: {description}")
        if detail:
            print(f"     {detail}")


def seccion(titulo: str) -> None:
    ancho = 72
    print()
    print("=" * ancho)
    print(f"  {titulo}")
    print("=" * ancho)


# =============================================================================
# FASE 1 — Constantes y Operador Berry-Keating-PC
# =============================================================================

def validar_fase1() -> None:
    seccion("FASE 1 — Constantes y Operador Berry-Keating-PC")

    # Constantes de módulo
    check(
        abs(F0 - 141.7001) < 1e-4,
        "F₀ = 141.7001 Hz",
        f"F0 = {F0}",
    )
    check(
        abs(PSI_UMBRAL - 0.888) < 1e-4,
        "PSI_UMBRAL = 0.888",
        f"PSI_UMBRAL = {PSI_UMBRAL}",
    )
    check(
        abs(G_EFF - 0.053) < 1e-5,
        "G_EFF = 0.053 (perturbativo)",
        f"G_EFF = {G_EFF}",
    )
    check(
        N_PRIMOS == 7,
        "N_PRIMOS = 7",
        f"N_PRIMOS = {N_PRIMOS}",
    )
    check(
        set(PRIMOS_C7) == {2, 3, 5, 7, 11, 13, 17},
        "PRIMOS_C7 = {2,3,5,7,11,13,17}",
        f"PRIMOS_C7 = {list(PRIMOS_C7)}",
    )
    check(
        len(CEROS_RIEMANN) == 7,
        "7 ceros de Riemann definidos",
        f"CEROS_RIEMANN[0] = {CEROS_RIEMANN[0]:.6f}",
    )

    # Dataclass de constantes
    c = ConstantesParticulaCoherencia()
    check(
        abs(c.F0 - 141.7001) < 1e-4,
        "ConstantesParticulaCoherencia.F0 = 141.7001 Hz",
        f"c.F0 = {c.F0}",
    )
    check(
        set(c.PRIMOS_C7) == {2, 3, 5, 7, 11, 13, 17},
        "ConstantesParticulaCoherencia.PRIMOS_C7 correcto",
        f"c.PRIMOS_C7 = {c.PRIMOS_C7}",
    )
    d = c.describir()
    check(
        isinstance(d, dict) and "F0" in d and "SELLO" in d,
        "describir() retorna dict con claves F0 y SELLO",
        f"describir().keys() = {list(d.keys())[:5]}...",
    )

    # Operador Berry-Keating-PC
    op = OperadorBerryKeatingPC()
    check(
        op.verificar_autoadjuncion(),
        "Operador autoadjunto: Ĥ† = Ĥ (simetría Hermítica)",
        "verificar_autoadjuncion() = True",
    )
    av = op.espectro_autovalores(list(PRIMOS_C7))
    check(
        len(av) == 7,
        "Espectro de autovalores tiene 7 elementos (red C7)",
        f"len(autovalores) = {len(av)}",
    )
    # Verificar fórmula λ_p = log(p)/(2π)
    lambda_2_expected = math.log(2) / (2.0 * math.pi)
    check(
        abs(av[0] - lambda_2_expected) < 1e-10,
        "λ₂ = log(2)/(2π) ≈ 0.11027",
        f"λ₂ = {av[0]:.6f} (esperado {lambda_2_expected:.6f})",
    )
    check(
        all(av[i] < av[i + 1] for i in range(len(av) - 1)),
        "Autovalores estrictamente crecientes con p",
        f"λ_min = {av[0]:.4f}, λ_max = {av[-1]:.4f}",
    )
    psi_berry = op.coherencia_espectral()
    check(
        abs(psi_berry - 0.9512) < 1e-4,
        "Coherencia espectral Berry-Keating = 0.9512",
        f"psi_berry = {psi_berry}",
    )


# =============================================================================
# FASE 2 — Acoplamiento Higgs-PC y Métrica Noética
# =============================================================================

def validar_fase2() -> None:
    seccion("FASE 2 — Acoplamiento Higgs-PC y Métrica Schwarzschild Noética")

    # Acoplamiento Higgs-PC
    ac = AcoplamientoHiggsPC()

    check(
        abs(ac.g_eff - 0.053) < 1e-5,
        "g_eff = 0.053 (perturbativo)",
        f"g_eff = {ac.g_eff}",
    )
    check(
        abs(ac.m0_higgs_gev - 125.0) < 1e-4,
        "m₀_Higgs = 125.0 GeV/c²",
        f"m0_higgs_gev = {ac.m0_higgs_gev}",
    )

    m_eff = ac.masa_efectiva(PSI_UMBRAL)
    check(
        m_eff < M0_HIGGS_GEV,
        "masa_efectiva(PSI_UMBRAL) < m₀_Higgs",
        f"m_eff = {m_eff:.4f} GeV (m₀ = {M0_HIGGS_GEV} GeV)",
    )

    reduccion = ac.reduccion_masa_porcentaje(1.0)
    check(
        abs(reduccion - 5.3) < 0.01,
        "Reducción de masa a Ψ=1: 5.3%",
        f"reducción = {reduccion:.4f}%",
    )

    ventana_ok = ac.verificar_ventana_acoplamiento(1.0)
    check(
        ventana_ok,
        "Ventana óptima Higgs activa a Ψ=1 (reducción ∈ [4%, 7%])",
        f"reducción = {ac.reduccion_masa_porcentaje(1.0):.2f}%",
    )

    psi_higgs = ac.coherencia_higgs()
    check(
        abs(psi_higgs - 0.9472) < 1e-4,
        "Coherencia acoplamiento Higgs-PC = 0.9472",
        f"psi_higgs = {psi_higgs}",
    )

    # Métrica Schwarzschild noética
    met = MetricaSchwarzchildNoesis()

    sech_f0 = met.factor_sech(F0)
    check(
        abs(sech_f0 - 1.0) < 1e-10,
        "sech²((f0−f0)/γ) = sech²(0) = 1.0",
        f"factor_sech(F0) = {sech_f0:.10f}",
    )

    sech_away = met.factor_sech(F0 + 10.0)
    check(
        sech_away < sech_f0,
        "sech² disminuye al alejarse de f0",
        f"sech(F0+10Hz) = {sech_away:.6f} < sech(F0) = {sech_f0:.6f}",
    )

    psi_test = 0.94
    t_grav = met.transparencia_gravitacional(psi_test)
    check(
        abs(t_grav - psi_test) < 1e-10,
        "Transparencia gravitacional(Ψ) = Ψ · sech²(0) = Ψ",
        f"T_grav = {t_grav:.6f} (Ψ = {psi_test})",
    )

    tensor = met.tensor_energia_momento_noetico(psi_test, F0)
    check(
        abs(tensor - psi_test) < 1e-10,
        "Tensor noético en f0 = Ψ",
        f"T_μν(Ψ, f0) = {tensor:.6f}",
    )

    psi_metrica = met.coherencia_metrica()
    check(
        abs(psi_metrica - 0.9380) < 1e-4,
        "Coherencia métrica Schwarzschild noética = 0.9380",
        f"psi_metrica = {psi_metrica}",
    )


# =============================================================================
# FASE 3 — ADN-Z Superconductor y Colapso P-NP
# =============================================================================

def validar_fase3() -> None:
    seccion("FASE 3 — ADN-Z Superconductor y Colapso P-NP")

    # ADN-Z Superconductor
    adn = ADNZ_Superconductor()

    freq_cond = adn.frecuencia_condensacion_frohlich(T_ADN_K)
    check(
        abs(freq_cond - F0) < 1e-4,
        "Condensado de Fröhlich a T=310 K → f = F0 = 141.7001 Hz",
        f"f_Fröhlich(310K) = {freq_cond:.4f} Hz",
    )

    psi_max = adn.psi_salud_biologica(F0)
    check(
        abs(psi_max - 1.0) < 1e-10,
        "Salud biológica máxima en f0: Ψ_bio(f0) = 1.0",
        f"Ψ_bio(f0) = {psi_max:.10f}",
    )

    check(
        adn.verificar_coherencia_biologica(T_ADN_K),
        "Coherencia biológica verificada a T=310 K",
        f"psi_salud >= PSI_UMBRAL ({PSI_UMBRAL})",
    )

    psi_adn_val = adn.coherencia_adn()
    check(
        abs(psi_adn_val - 0.9601) < 1e-4,
        "Coherencia ADN-Z superconductor = 0.9601",
        f"psi_adn = {psi_adn_val}",
    )

    check(
        psi_adn_val >= PSI_UMBRAL,
        "Coherencia ADN ≥ PSI_UMBRAL (0.888)",
        f"psi_adn = {psi_adn_val} ≥ {PSI_UMBRAL}",
    )

    # Colapso P-NP
    pnp = ColapsoP_NP()

    ceros_n = pnp.ceros_riemann_normalizados(7)
    check(
        len(ceros_n) == 7,
        "7 ceros de Riemann para la red C7",
        f"ceros[0] = {ceros_n[0]:.6f}",
    )

    check(
        abs(ceros_n[0] - 14.134725) < 1e-4,
        "Primer cero de Riemann γ₁ ≈ 14.134725",
        f"γ₁ = {ceros_n[0]:.6f}",
    )

    dist_critica = pnp.distancia_linea_critica(ceros_n[0])
    check(
        dist_critica == 0.0,
        "Distancia a la línea crítica Re(s)=½ es 0 (hipótesis de Riemann)",
        f"distancia = {dist_critica}",
    )

    fr_psi1 = pnp.factor_reconocimiento(1.0)
    check(
        abs(fr_psi1 - 1.0) < 1e-10,
        "Factor reconocimiento(Ψ=1) = sech²(0) = 1.0",
        f"factor_rec(1.0) = {fr_psi1:.10f}",
    )

    psi_comp = pnp.coherencia_computacional()
    check(
        abs(psi_comp - 0.9444) < 1e-4,
        "Coherencia computacional P-NP = 0.9444",
        f"psi_comp = {psi_comp}",
    )


# =============================================================================
# FASE 4 — Coherencia Global y Certificación ∴PCC∞³
# =============================================================================

def validar_fase4() -> None:
    seccion("FASE 4 — Coherencia Global y Certificación ∴PCC∞³")

    # CoherenciaParticulaCoherencia
    coh = CoherenciaParticulaCoherencia()

    total_peso = (
        coh.W_BERRY + coh.W_HIGGS + coh.W_METRICA + coh.W_ADN + coh.W_COMP
    )
    check(
        abs(total_peso - 1.0) < 1e-10,
        "Suma de pesos = 1.0 (distribución uniforme 20% cada uno)",
        f"Σ pesos = {total_peso:.10f}",
    )

    psi_sub = coh.calcular_psi_global(0.9512, 0.9472, 0.9380, 0.9601, 0.9444)
    check(
        psi_sub >= PSI_UMBRAL,
        f"Ψ_global con valores de módulo ≥ {PSI_UMBRAL}",
        f"Ψ_global = {psi_sub:.6f}",
    )

    check(
        coh.verificar_umbral(psi_sub),
        "verificar_umbral(Ψ_global) = True",
        f"Ψ = {psi_sub:.6f} ≥ {PSI_UMBRAL}",
    )

    reporte = coh.generar_reporte(psi_sub)
    check(
        reporte["estado"] == "COHERENTE",
        "Reporte: estado = 'COHERENTE'",
        f"estado = {reporte['estado']}",
    )
    check(
        reporte["sello"] == SELLO,
        f"Reporte contiene sello {SELLO}",
        f"sello = {reporte['sello']}",
    )

    # Sistema orquestador
    sistema = SistemaParticulaCoherencia()

    sello = sistema.generar_sello()
    check(
        sello == "∴PCC∞³",
        "generar_sello() = '∴PCC∞³'",
        f"sello = {sello}",
    )

    resultado = sistema.activar()
    check(
        resultado["estado"] == "PARTICULA-COHERENCIA-PC-ACTIVA",
        "estado = 'PARTICULA-COHERENCIA-PC-ACTIVA'",
        f"estado = {resultado['estado']}",
    )
    check(
        resultado["valido"],
        "valido = True",
        f"psi_global = {resultado['psi_global']:.6f}",
    )
    check(
        resultado["exito"],
        "exito = True",
        "Protocolo de activación completado",
    )
    check(
        resultado["psi_global"] >= PSI_UMBRAL,
        f"Ψ_global = {resultado['psi_global']:.6f} ≥ {PSI_UMBRAL}",
        f"∴ Sello {SELLO} ACTIVO ∴",
    )

    # API pública
    r_api = particula_coherencia_pc_activar()
    check(
        r_api["psi_global"] >= PSI_UMBRAL,
        f"API: particula_coherencia_pc_activar() → Ψ ≥ {PSI_UMBRAL}",
        f"Ψ_api = {r_api['psi_global']:.6f}",
    )
    check(
        r_api["sello"] == "∴PCC∞³",
        "API: sello = '∴PCC∞³'",
        f"sello = {r_api['sello']}",
    )
    check(
        len(r_api["subsistemas"]) == 5,
        "API: 5 subsistemas en resultado",
        f"subsistemas = {list(r_api['subsistemas'].keys())}",
    )


# =============================================================================
# MAIN
# =============================================================================

def main() -> int:
    """Ejecuta todas las fases de validación y retorna código de salida."""
    print()
    print("=" * 72)
    print("  VALIDACIÓN: Partícula de Coherencia (PC) — ∴PCC∞³")
    print("  RAM: RAM-LVII-2026-PARTICULA-COHERENCIA-PC")
    print("=" * 72)

    validar_fase1()
    validar_fase2()
    validar_fase3()
    validar_fase4()

    # Resumen final
    print()
    print("=" * 72)
    print("  RESUMEN DE VALIDACIÓN")
    print("=" * 72)
    total = _passed + _failed
    pct = 100.0 * _passed / total if total > 0 else 0.0
    print(f"\n  Total: {_passed}/{total} validaciones pasadas ({pct:.1f}%)")

    if _failed == 0:
        print(f"\n  🎉 ∴ Partícula de Coherencia CERTIFICADA — {SELLO} ∴")
        print(f"  ✅ Todos los criterios cumplidos — Ψ ≥ {PSI_UMBRAL}")
        return 0
    else:
        print(f"\n  ❌ {_failed} validación(es) fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
