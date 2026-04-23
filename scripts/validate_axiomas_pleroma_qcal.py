#!/usr/bin/env python3
"""
Validate Axiomas del Pleroma QCAL — ∴APQ∞³
===============================================================================

Valida la implementación del módulo physics.axiomas_pleroma_qcal contra los
criterios teóricos de los 5 Axiomas del Pleroma QCAL ∞³:

  Fase 1 — Constantes fundamentales y Axioma 1 (Plenitud del Pleroma)
  Fase 2 — Axioma 2 (Materia como bucle de 4π, Brecha de Torsión)
  Fase 3 — Axioma 3 (Manta Adélica de Responsabilidad, Ψ = I × A_eff²)
  Fase 4 — Axioma 4 (Operador de Riemann–Hubble, E₀ = ℏω₀)
  Fase 5 — Axioma 5 (Inmortalidad Dinámica de la Luz)
  Fase 6 — Coherencia global y certificación ∴APQ∞³

Criterios de éxito:
  - f₀ = 141.7001 Hz                    [exacto]
  - γ₁ = 14.134725141734694             [cero Riemann]
  - Brecha de Torsión = 3.00052°        [Axioma 2]
  - E₀ = ℏω₀ ≈ 9.389e-32 J            [Axioma 4]
  - Vacío inexistente (S = 0)           [Axioma 1]
  - Bucle de 4π estable                 [Axioma 2]
  - Ψ_nodo = I × A_eff²                [Axioma 3]
  - Ĥ_RH hermítico, r_GUE ∈ [0.3,0.8] [Axioma 4]
  - Sándwich de coherencia abierto      [Axioma 5]
  - Ψ_global ≥ 0.888                   → sello ∴APQ∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
RAM: RAM-LX-2026-AXIOMAS-PLEROMA-QCAL
"""

import math
import sys
from pathlib import Path

# Añadir la raíz del repositorio al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.axiomas_pleroma_qcal import (
    ConstantesAxiomasPleroma,
    AtomoBlancoSaturado,
    MateriaBucle4Pi,
    MantaAdelicaRiemann,
    OperadorRiemannHubble,
    InmortalidadDinamicaLuz,
    CoherenciaAxiomasPleroma,
    SistemaAxiomasPleroma,
    axiomas_pleroma_qcal_activar,
    _F0,
    _GAMMA_1,
    _ZEROS_10,
    _BRECHA_TORSION_DEG,
    _BRECHA_TORSION_RAD,
    _N_LOOPS,
    _HBAR,
    _OMEGA_0,
    _PSI_UMBRAL,
    _SELLO,
    _RAM,
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


def section(title: str) -> None:
    """Imprime un encabezado de sección."""
    print(f"\n{'─'*62}")
    print(f"  {title}")
    print(f"{'─'*62}")


# =============================================================================
# FASE 1 — CONSTANTES FUNDAMENTALES Y AXIOMA 1
# =============================================================================

def fase_1_constantes_y_axioma1() -> None:
    """Valida las constantes del módulo y el Axioma 1: Plenitud del Pleroma."""
    section("FASE 1 — Constantes fundamentales + Axioma 1 (Plenitud del Pleroma)")

    # Constantes de módulo
    check(abs(_F0 - 141.7001) < 1e-4, "f₀ = 141.7001 Hz", f"f₀ = {_F0}")
    check(abs(_GAMMA_1 - 14.134725) < 1e-5, "γ₁ ≈ 14.134725", f"γ₁ = {_GAMMA_1:.6f}")
    check(len(_ZEROS_10) == 10, "10 ceros de Riemann cargados")
    check(abs(_BRECHA_TORSION_DEG - 3.00052) < 1e-5,
          "Brecha de Torsión = 3.00052°", f"θ_brecha = {_BRECHA_TORSION_DEG}°")
    check(abs(_N_LOOPS - 4.0 * math.pi) < 1e-10, "n_loops = 4π")
    check(abs(_PSI_UMBRAL - 0.888) < 1e-4, "Ψ_umbral = 0.888")
    check(_SELLO == "∴APQ∞³", f"Sello = {_SELLO!r}")
    check(_RAM == "RAM-LX-2026-AXIOMAS-PLEROMA-QCAL", f"RAM = {_RAM!r}")

    # ConstantesAxiomasPleroma
    c = ConstantesAxiomasPleroma()
    check(c.suma_primos() == 58, "Σ primos P = 58", f"Σ = {c.suma_primos()}")
    check(abs(c.razon_f0_gamma1() - _F0 / _GAMMA_1) < 1e-6,
          f"f₀/γ₁ ≈ {_F0/_GAMMA_1:.6f}",
          f"calculado = {c.razon_f0_gamma1():.6f}")
    check(c.energia_fundamental_j() > 0.0, "E₀ = ℏω₀ > 0",
          f"E₀ = {c.energia_fundamental_j():.3e} J")

    # Axioma 1 — AtomoBlancoSaturado
    atomo = AtomoBlancoSaturado()
    check(atomo.es_vacio_inexistente(),
          "Axioma 1: el vacío no existe (S = 0)")
    check(abs(atomo.psi_axioma1() - 1.0) < 1e-6,
          "Axioma 1: Ψ₁ = 1.0 (Pleroma Saturado perfecto)",
          f"Ψ₁ = {atomo.psi_axioma1():.6f}")
    check(abs(atomo.densidad_informacion_normalizada() - 1.0) < 1e-10,
          "Densidad de información normalizada = 1.0")
    check(atomo.superposicion_total() >= 0.9999,
          "Superposición total del Átomo Blanco ≈ 1.0",
          f"σ_WA = {atomo.superposicion_total():.6f}")


# =============================================================================
# FASE 2 — AXIOMA 2: MATERIA COMO BUCLE DE 4π
# =============================================================================

def fase_2_axioma2_bucle_4pi() -> None:
    """Valida el Axioma 2: Materia como bucle de 4π."""
    section("FASE 2 — Axioma 2 (Materia como bucle de 4π)")

    bucle = MateriaBucle4Pi()

    check(bucle.es_bucle_estable(),
          "Bucle de 4π topológicamente estable")
    check(abs(bucle.frecuencia_nodo_hz() - _F0) < 1e-6,
          f"Frecuencia del nodo = f₀ = {_F0} Hz",
          f"f_nodo = {bucle.frecuencia_nodo_hz():.4f} Hz")
    check(bucle.radio_nodo_m() > 0,
          f"Radio del nodo r₀ > 0",
          f"r₀ = {bucle.radio_nodo_m():.3e} m")
    check(abs(bucle.angulo_torsion_total_rad() - (_N_LOOPS + _BRECHA_TORSION_RAD)) < 1e-10,
          "Ángulo total = 4π + θ_brecha",
          f"θ_total = {bucle.angulo_torsion_total_rad():.6f} rad")

    # Verificar que f_n=1 = f₀
    f1 = bucle.frecuencia_modo_n_hz(1)
    check(abs(f1 - _F0) < 1e-6,
          "Modo n=1 del bucle = f₀",
          f"f₁ = {f1:.4f} Hz")

    # Verificar modos crecientes
    modos = [bucle.frecuencia_modo_n_hz(n) for n in range(1, 8)]
    es_creciente = all(modos[i] < modos[i + 1] for i in range(len(modos) - 1))
    check(es_creciente, "Modos del bucle son crecientes")

    # Coherencia Ψ₂
    psi2 = bucle.psi_axioma2()
    check(psi2 >= 0.999,
          f"Ψ₂ = cos²(θ_brecha/2) ≥ 0.999",
          f"Ψ₂ = {psi2:.6f}")
    check(psi2 >= _PSI_UMBRAL,
          "Ψ₂ supera umbral 0.888")

    # Verificar la Brecha de Torsión
    check(abs(math.degrees(bucle.brecha_torsion_rad) - 3.00052) < 1e-5,
          "Brecha de Torsión = 3.00052° (verificado en rad)",
          f"θ_deg = {math.degrees(bucle.brecha_torsion_rad):.5f}°")


# =============================================================================
# FASE 3 — AXIOMA 3: MANTA ADÉLICA DE RESPONSABILIDAD
# =============================================================================

def fase_3_axioma3_manta_adelica() -> None:
    """Valida el Axioma 3: Manta Adélica de Responsabilidad."""
    section("FASE 3 — Axioma 3 (Manta Adélica de Responsabilidad)")

    manta = MantaAdelicaRiemann()

    # Ψ = I × A_eff² con I=1, A_eff=1 → Ψ = 1
    check(abs(manta.psi_nodo() - 1.0) < 1e-10,
          "Ψ_nodo = I × A_eff² = 1.0 (con I=1, A_eff=1)",
          f"Ψ_nodo = {manta.psi_nodo():.6f}")

    # Ψ con I=0.5
    m05 = MantaAdelicaRiemann(intencion=0.5, a_eff=1.0)
    check(abs(m05.psi_nodo() - 0.5) < 1e-10,
          "Ψ_nodo = 0.5 con I=0.5, A_eff=1",
          f"Ψ_nodo = {m05.psi_nodo():.6f}")

    # Ψ con A_eff=0.9
    m09 = MantaAdelicaRiemann(intencion=1.0, a_eff=0.9)
    check(abs(m09.psi_nodo() - 0.81) < 1e-10,
          "Ψ_nodo = 0.81 con I=1, A_eff=0.9",
          f"Ψ_nodo = {m09.psi_nodo():.6f}")

    # 7 pliegues adélicos
    pliegues = manta.pliegues_adelicos()
    check(len(pliegues) == 7, "7 pliegues adélicos (uno por primo)")
    check(all(p > 0 for p in pliegues), "Todos los pliegues > 0")
    check(abs(pliegues[0] - _F0) < 1e-4,
          "Pliegue del primo 2 = f₀ (log₂(2) = 1)",
          f"pliegue₁ = {pliegues[0]:.4f} Hz")

    # 10 nodos de ceros de Riemann
    nodos = manta.nodos_ceros_riemann()
    check(len(nodos) == 10, "10 nodos espectrales de la Manta")
    check(abs(nodos[0] - _F0) < 1e-4,
          "Primer nodo espectral = f₀",
          f"nodo₁ = {nodos[0]:.4f} Hz")

    # Responsabilidad
    delta = manta.responsabilidad_acto(0.1)
    check(delta > 0.0, "Acto de coherencia aumenta curvatura (+ΔΨ)")
    delta_neg = manta.responsabilidad_acto(-0.1)
    check(delta_neg < 0.0, "Acto de descoherencia reduce curvatura (-ΔΨ)")

    # Ψ₃
    psi3 = manta.psi_axioma3()
    check(abs(psi3 - manta.psi_nodo()) < 1e-10,
          "Ψ₃ = Ψ_nodo (ley directa de la Manta)",
          f"Ψ₃ = {psi3:.6f}")
    check(psi3 >= _PSI_UMBRAL,
          "Ψ₃ supera umbral 0.888")


# =============================================================================
# FASE 4 — AXIOMA 4: OPERADOR DE RIEMANN–HUBBLE
# =============================================================================

def fase_4_axioma4_operador_rh() -> None:
    """Valida el Axioma 4: Operador de Riemann–Hubble."""
    section("FASE 4 — Axioma 4 (Operador de Riemann-Hubble)")

    op = OperadorRiemannHubble()

    # E₀ = ℏω₀
    e0_j = op.energia_fundamental_j()
    e0_esperado = _HBAR * _OMEGA_0
    check(abs(e0_j - e0_esperado) < 1e-38,
          "E₀ = ℏω₀ (estado fundamental del Ĥ_RH)",
          f"E₀ = {e0_j:.3e} J")

    # Hermiticidad
    check(op.es_hermitiano(),
          "Ĥ_RH es hermítico (todos los γₙ > 0)")

    # Espectro discreto
    espectro = op.espectro_discreto_j()
    check(len(espectro) == 10, "Espectro discreto: 10 niveles E_n = ℏγₙ")
    check(all(e > 0 for e in espectro), "Todos los niveles E_n > 0")
    check(all(espectro[i] < espectro[i + 1] for i in range(len(espectro) - 1)),
          "Espectro creciente (ceros ordenados)")

    # Nivel 1: E₁ = ℏγ₁
    e1_esperado = _HBAR * _GAMMA_1
    check(abs(espectro[0] - e1_esperado) < 1e-38,
          f"E₁ = ℏγ₁ ≈ {e1_esperado:.3e} J")

    # Índice GUE
    r_gue = op.espaciado_gue_ratio()
    check(0.3 < r_gue < 0.8,
          f"Índice r_GUE ∈ (0.3, 0.8) [compatible con GUE]",
          f"r_GUE = {r_gue:.4f}")

    # Razón H₀/ω₀
    razon = op.razon_hubble_qcal()
    check(razon > 0.0 and razon < 1e-18,
          "H₀/ω₀ << 1 (separación de escalas cósmica/QCAL)",
          f"H₀/ω₀ = {razon:.3e}")

    # Ψ₄
    psi4 = op.psi_axioma4()
    check(psi4 >= _PSI_UMBRAL,
          f"Ψ₄ ≥ 0.888",
          f"Ψ₄ = {psi4:.6f}")
    check(psi4 <= 1.0, "Ψ₄ ≤ 1.0")


# =============================================================================
# FASE 5 — AXIOMA 5: INMORTALIDAD DINÁMICA DE LA LUZ
# =============================================================================

def fase_5_axioma5_inmortalidad() -> None:
    """Valida el Axioma 5: Inmortalidad Dinámica de la Luz."""
    section("FASE 5 — Axioma 5 (Inmortalidad Dinámica de la Luz)")

    inm = InmortalidadDinamicaLuz()

    # α = ω₀
    check(abs(inm.alpha - _OMEGA_0) < 1e-6,
          "α = ω₀ (tasa de retorno de la luz)",
          f"α = {inm.alpha:.4f} rad/s")

    # Sándwich de coherencia
    check(inm.sandwitch_coherencia_abierto(),
          "Sándwich de coherencia ABIERTO (Ψ_bio = 1.0 ≥ 0.888)")

    # Retorno en t=0 es Ψ₀
    psi_t0 = inm.psi_retorno(0.0)
    check(abs(psi_t0 - inm.psi_inicial) < 1e-6,
          "Ψ(t=0) = Ψ_inicial = 0.888")

    # Retorno monótono
    psi_t1 = inm.psi_retorno(1.0e-4)
    psi_t2 = inm.psi_retorno(1.0e-3)
    check(psi_t1 < psi_t2,
          "Ψ(t) crece monotónicamente con t")

    # Convergencia a 1 en t grande
    psi_inf = inm.psi_retorno(1000.0)
    check(abs(psi_inf - 1.0) < 1e-3,
          "Ψ(t→∞) → 1.0 (inmortalidad dinámica)",
          f"Ψ(1000 s) = {psi_inf:.6f}")

    # Tiempo de retorno
    t_ret = inm.tiempo_retorno_s()
    check(t_ret > 0.0,
          f"Tiempo de retorno T_retorno > 0",
          f"T_retorno = {t_ret:.6f} s")
    check(t_ret * _F0 > 0.0,
          f"N_periodos = T_retorno × f₀ > 0",
          f"N = {inm.n_periodos_retorno():.4f} períodos")

    # Sándwich cerrado con Ψ_bio bajo
    inm_bajo = InmortalidadDinamicaLuz(psi_bio=0.5)
    check(not inm_bajo.sandwitch_coherencia_abierto(),
          "Sándwich CERRADO cuando Ψ_bio = 0.5 < 0.888")

    # Ψ₅
    psi5 = inm.psi_axioma5()
    check(psi5 >= _PSI_UMBRAL,
          f"Ψ₅ ≥ 0.888 (inmortalidad activa)",
          f"Ψ₅ = {psi5:.6f}")
    check(psi5 > 0.99,
          f"Ψ₅ > 0.99 (retorno casi completo en T₀)",
          f"Ψ₅ = {psi5:.6f}")


# =============================================================================
# FASE 6 — COHERENCIA GLOBAL Y CERTIFICACIÓN ∴APQ∞³
# =============================================================================

def fase_6_coherencia_y_certificacion() -> None:
    """Valida la coherencia global y activa el sello ∴APQ∞³."""
    section("FASE 6 — Coherencia global y certificación ∴APQ∞³")

    resultado = axiomas_pleroma_qcal_activar()

    # Identificación
    check(resultado["sello"] == "∴APQ∞³",
          f"Sello = {resultado['sello']!r}")
    check(resultado["ram"] == "RAM-LX-2026-AXIOMAS-PLEROMA-QCAL",
          f"RAM = {resultado['ram']!r}")

    # Coherencias individuales
    coh = resultado["coherencias"]
    psi1 = coh["psi_axioma1_pleroma_saturado"]
    psi2 = coh["psi_axioma2_bucle_4pi"]
    psi3 = coh["psi_axioma3_manta_adelica"]
    psi4 = coh["psi_axioma4_operador_rh"]
    psi5 = coh["psi_axioma5_inmortalidad"]

    check(abs(psi1 - 1.0) < 1e-6, f"Ψ₁ = {psi1:.6f} (Pleroma Saturado)")
    check(psi2 >= 0.999, f"Ψ₂ = {psi2:.6f} (bucle 4π)")
    check(psi3 >= 0.999, f"Ψ₃ = {psi3:.6f} (Manta Adélica)")
    check(psi4 >= 0.888, f"Ψ₄ = {psi4:.6f} (Operador RH)")
    check(psi5 >= 0.888, f"Ψ₅ = {psi5:.6f} (Inmortalidad)")

    # Coherencia global
    psi_g = resultado["psi_global"]
    check(psi_g >= _PSI_UMBRAL,
          f"Ψ_global ≥ 0.888 → SELLO ACTIVO",
          f"Ψ_global = {psi_g:.6f}")

    # Sello activo
    check(resultado["sello_activo"],
          "∴APQ∞³ ACTIVO ✓")

    # Idempotencia
    r2 = axiomas_pleroma_qcal_activar()
    check(abs(resultado["psi_global"] - r2["psi_global"]) < 1e-10,
          "Idempotencia: llamadas múltiples dan el mismo resultado")

    # Certificación AURON
    cert = resultado["certificacion"]
    check("∴APQ∞³" in cert, "Certificación AURON contiene el sello")
    check("ACTIVO" in cert, "Certificación AURON reporta estado ACTIVO")


# =============================================================================
# RESUMEN FINAL
# =============================================================================

def resumen_final() -> int:
    """Imprime el resumen final y devuelve el código de salida."""
    print(f"\n{'═'*62}")
    print(f"  RESUMEN DE VALIDACIÓN — ∴APQ∞³")
    print(f"{'═'*62}")
    total = _passed + _failed
    print(f"  Pruebas ejecutadas: {total}")
    print(f"  ✅ Aprobadas:       {_passed}")
    print(f"  ❌ Fallidas:        {_failed}")
    print(f"{'─'*62}")
    if _failed == 0:
        print("  ✅ SELLO ∴APQ∞³ VERIFICADO — Ψ_global ≥ 0.888")
        print(f"  RAM: RAM-LX-2026-AXIOMAS-PLEROMA-QCAL")
    else:
        print(f"  ❌ VALIDACIÓN FALLIDA — {_failed} prueba(s) no superadas")
    print(f"{'═'*62}\n")
    return 0 if _failed == 0 else 1


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(f"\n{'═'*62}")
    print(f"  VALIDACIÓN: AXIOMAS DEL PLEROMA QCAL — ∴APQ∞³")
    print(f"  RAM: RAM-LX-2026-AXIOMAS-PLEROMA-QCAL")
    print(f"{'═'*62}")

    fase_1_constantes_y_axioma1()
    fase_2_axioma2_bucle_4pi()
    fase_3_axioma3_manta_adelica()
    fase_4_axioma4_operador_rh()
    fase_5_axioma5_inmortalidad()
    fase_6_coherencia_y_certificacion()

    sys.exit(resumen_final())
