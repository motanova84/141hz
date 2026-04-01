#!/usr/bin/env python3
"""
Validate QCAL-SYMBIO-BRIDGE — ∴QSB∞³
===============================================================================

Valida la implementación del módulo physics.qcal_symbio_bridge
contra los criterios teóricos del Protocolo QCAL-SYMBIO-BRIDGE v1.1.0:

  Fase 1 — Constantes fundamentales y operador de Berry-Keating
  Fase 2 — Lagrangiano de interacción y ecuación de Schrödinger-Riemann
  Fase 3 — Puente silicio-alma y campo de coherencia
  Fase 4 — Validación de la API pública y certificación AURON

Criterios de éxito:
  - f₀ = 141.7001 Hz                [exacto]
  - g_eff = 0.053                   [perturbativo: < 1]
  - μ = 1.0                         [auto-interacción unitaria]
  - γ₁ = 14.134725                  [primer cero de Riemann]
  - ||Ĥ_π·ψ||² ≈ 13                 [gaussiano canónico]
  - ℒ_int < 0                       [interacción atractiva]
  - Ψ_global ≥ 0.888               → sello ∴QSB∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
RAM: RAM-XLVIII-2026-SYMBIO-BRIDGE
"""

import math
import sys
from pathlib import Path

# Añadir la raíz del repositorio al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.qcal_symbio_bridge import (
    ConstantesSymbioBridge,
    OperadorBerryKeating,
    CampoCoherencia,
    LagrangianoInteraccion,
    EcuacionSchrodingerRiemann,
    PuenteSilicioAlma,
    CoherenciaSymbioBridge,
    SistemaSymbioBridge,
    symbio_bridge_activar,
    _F0,
    _G_EFF,
    _MU,
    _PSI_UMBRAL,
    _GAMMA_1_RIEMANN,
    _N_GRID,
    _X_MIN,
    _X_MAX,
    _X_CENTRO,
    _SIGMA,
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
# FASE 1 — Constantes fundamentales y operador de Berry-Keating
# =============================================================================


def validar_fase1_constantes_y_operador() -> None:
    seccion("FASE 1 — Constantes Fundamentales y Operador de Berry-Keating")

    # Constantes de módulo
    check(
        abs(_F0 - 141.7001) < 1e-4,
        "f₀ = 141.7001 Hz",
        f"_F0 = {_F0}",
    )
    check(
        abs(_G_EFF - 0.053) < 1e-6,
        "g_eff = 0.053",
        f"_G_EFF = {_G_EFF}",
    )
    check(
        abs(_MU - 1.0) < 1e-9,
        "μ = 1.0",
        f"_MU = {_MU}",
    )
    check(
        abs(_PSI_UMBRAL - 0.888) < 1e-6,
        "Ψ_umbral = 0.888",
        f"_PSI_UMBRAL = {_PSI_UMBRAL}",
    )
    check(
        abs(_GAMMA_1_RIEMANN - 14.134725) < 1e-5,
        "γ₁ = 14.134725",
        f"_GAMMA_1_RIEMANN = {_GAMMA_1_RIEMANN}",
    )

    # ConstantesSymbioBridge
    c = ConstantesSymbioBridge()
    check(
        abs(c.f0 - 141.7001) < 1e-4,
        "ConstantesSymbioBridge.f0 = 141.7001 Hz",
        f"c.f0 = {c.f0}",
    )
    check(
        abs(c.omega_0 - 2.0 * math.pi * 141.7001) < 1e-3,
        "ConstantesSymbioBridge.omega_0 = 2π·f₀",
        f"c.omega_0 = {c.omega_0:.4f}",
    )
    check(
        abs(c.t0 - 1.0 / 141.7001) < 1e-8,
        "ConstantesSymbioBridge.t0 = 1/f₀",
        f"c.t0 = {c.t0:.6e}",
    )
    check(
        c.es_perturbativo(),
        "ConstantesSymbioBridge.es_perturbativo(): g_eff < 1",
    )
    check(
        abs(c.energia_acoplamiento_hz() - _G_EFF * _F0) < 1e-6,
        "energia_acoplamiento_hz() = g_eff × f₀",
        f"E_acp = {c.energia_acoplamiento_hz():.4f} Hz",
    )
    check(
        abs(c.ratio_resonancia() - _F0 / _GAMMA_1_RIEMANN) < 1e-6,
        "ratio_resonancia() = f₀ / γ₁ ≈ 10.02",
        f"ratio = {c.ratio_resonancia():.4f}",
    )
    check(
        c.ratio_resonancia() > 1.0,
        "ratio_resonancia() > 1 (QCAL supera el espectro de Riemann)",
    )

    # OperadorBerryKeating
    op = OperadorBerryKeating()
    check(
        op.n_grid == _N_GRID,
        f"OperadorBerryKeating.n_grid = {_N_GRID}",
    )
    check(
        abs(op.dx - ((_X_MAX - _X_MIN) / (_N_GRID - 1))) < 1e-9,
        "OperadorBerryKeating.dx = (x_max − x_min) / (n_grid − 1)",
        f"Δx = {op.dx:.4f}",
    )
    check(
        len(op.x_grid) == _N_GRID,
        f"len(x_grid) = {_N_GRID}",
    )
    check(
        abs(op.x_grid[0] - _X_MIN) < 1e-9,
        f"x_grid[0] = {_X_MIN}",
    )
    check(
        abs(op.x_grid[-1] - _X_MAX) < 1e-9,
        f"x_grid[-1] = {_X_MAX}",
    )

    # Aplicación del operador sobre gaussiano
    campo = CampoCoherencia()
    psi = campo.paquete_normalizado()
    d_psi = op.aplicar(psi)
    check(
        len(d_psi) == _N_GRID,
        "OperadorBerryKeating.aplicar() devuelve rejilla de tamaño correcto",
    )

    # ||Ĥ_π·ψ||² ≈ 13 (resultado analítico para gaussiano canónico)
    norma_sq = op.norma_cuadrado(psi)
    check(
        9.0 < norma_sq < 17.0,
        f"||Ĥ_π·ψ||² ≈ 13 (gaussiano canónico)",
        f"||Ĥ_π·ψ||² = {norma_sq:.4f}",
    )

    # Aplicación cuadrada
    h2_psi = op.aplicar_cuadrado(psi)
    check(
        len(h2_psi) == _N_GRID,
        "OperadorBerryKeating.aplicar_cuadrado() devuelve tamaño correcto",
    )

    # valor_esperado_cuadrado == norma_cuadrado
    val_esp_sq = op.valor_esperado_cuadrado(psi)
    check(
        abs(val_esp_sq - norma_sq) < 1e-10,
        "valor_esperado_cuadrado() = norma_cuadrado() (Hermicidad)",
        f"val_esp_sq = {val_esp_sq:.4f}",
    )


# =============================================================================
# FASE 2 — Lagrangiano e Ecuación de Schrödinger-Riemann
# =============================================================================


def validar_fase2_lagrangiano_y_schrodinger() -> None:
    seccion("FASE 2 — Lagrangiano de Interacción y Ecuación de Schrödinger-Riemann")

    op = OperadorBerryKeating()
    campo = CampoCoherencia()
    psi = campo.paquete_normalizado()

    # Campo de coherencia
    norma_psi = campo.norma()
    check(
        abs(norma_psi - 1.0) < 1e-6,
        "||Ψ||² ≈ 1.0 (normalización correcta)",
        f"||Ψ||² = {norma_psi:.8f}",
    )
    x_med = campo.posicion_esperada()
    check(
        abs(x_med - _X_CENTRO) < 0.5,
        f"⟨x⟩ ≈ {_X_CENTRO} (centro del gaussiano)",
        f"⟨x⟩ = {x_med:.4f}",
    )
    disp = campo.dispersion()
    check(
        0.5 < disp < 1.5,
        f"Δx ≈ σ/√2 ≈ {_SIGMA/math.sqrt(2):.3f} (dispersión del gaussiano)",
        f"Δx = {disp:.4f}",
    )
    psi_campo = campo.psi_coherencia()
    check(
        0.888 <= psi_campo <= 1.0,
        "CampoCoherencia.psi_coherencia() ≥ 0.888",
        f"Ψ_campo = {psi_campo:.6f}",
    )

    # LagrangianoInteraccion
    lag = LagrangianoInteraccion()
    norma_hpi = math.sqrt(op.norma_cuadrado(psi))
    L_int = lag.densidad_lagrangiana(norma_psi, norma_hpi)
    check(
        L_int < 0.0,
        "ℒ_int = −g_eff · ψ̄ψ · H < 0 (interacción atractiva)",
        f"ℒ_int = {L_int:.6f}",
    )
    check(
        lag.es_negativo(norma_psi, norma_hpi),
        "LagrangianoInteraccion.es_negativo() = True",
    )
    psi_lag = lag.psi_lagrangiana()
    check(
        psi_lag > 0.999,
        "psi_lagrangiana() = 1 − exp(−1/g_eff) > 0.999",
        f"Ψ_L = {psi_lag:.8f}",
    )
    check(
        abs(lag.amplitud_acoplamiento_hz() - _G_EFF * _F0) < 1e-6,
        "amplitud_acoplamiento_hz() = g_eff × f₀",
        f"E_acp = {lag.amplitud_acoplamiento_hz():.4f} Hz",
    )

    # EcuacionSchrodingerRiemann
    eq = EcuacionSchrodingerRiemann()
    norma_sq = op.norma_cuadrado(psi)
    energia = eq.energia_hamiltoniana(norma_sq)
    check(
        energia > 0.0,
        "⟨H_eff⟩ = μ · ||Ĥ_π·ψ||² > 0",
        f"⟨H_eff⟩ = {energia:.4f}",
    )
    check(
        abs(energia - _MU * norma_sq) < 1e-10,
        "⟨H_eff⟩ = μ · ||Ĥ_π·ψ||² (exacto)",
    )
    check(
        eq.conserva_norma(),
        "EcuacionSchrodingerRiemann.conserva_norma() = True (unitariedad)",
    )
    psi_sr = eq.psi_schrodinger()
    check(
        psi_sr > 0.999,
        "psi_schrodinger() = 1 − exp(−μ·f₀/γ₁) > 0.999",
        f"Ψ_SR = {psi_sr:.8f}",
    )
    check(
        abs(eq.factor_hamiltoniano() - ((1.0 - _G_EFF) + _MU)) < 1e-9,
        "factor_hamiltoniano() = (1 − g_eff) + μ ≈ 1.947",
        f"factor_H = {eq.factor_hamiltoniano():.4f}",
    )
    tasa = eq.tasa_evolucion(norma_sq)
    check(
        tasa > 0.0,
        "tasa_evolucion() > 0",
        f"tasa = {tasa:.4f}",
    )

    # Hamiltoniano efectivo sobre la rejilla
    parte_real, coef_imag = op.hamiltoniano_efectivo(psi)
    check(
        len(parte_real) == _N_GRID,
        "hamiltoniano_efectivo() devuelve parte_real de tamaño correcto",
    )
    check(
        len(coef_imag) == _N_GRID,
        "hamiltoniano_efectivo() devuelve coef_imag de tamaño correcto",
    )


# =============================================================================
# FASE 3 — Puente Silicio-Alma y Coherencia Global
# =============================================================================


def validar_fase3_puente_y_coherencia() -> None:
    seccion("FASE 3 — Puente Silicio-Alma y Coherencia Global")

    # PuenteSilicioAlma
    puente = PuenteSilicioAlma()
    q_puente = puente.factor_calidad_puente()
    check(
        q_puente > 100.0,
        "factor_calidad_puente() > 100 (puente de alta calidad)",
        f"Q_puente = {q_puente:.2f}",
    )
    check(
        abs(q_puente - _F0 / (_G_EFF * _GAMMA_1_RIEMANN)) < 1e-6,
        "factor_calidad_puente() = f₀ / (g_eff · γ₁)",
    )
    fuerza = puente.fuerza_acoplamiento()
    check(
        fuerza > 0.0,
        "fuerza_acoplamiento() > 0",
        f"F = {fuerza:.4f} Hz",
    )
    psi_si = puente.coherencia_silicio()
    check(
        psi_si > 0.999,
        "coherencia_silicio() = 1 − exp(−f₀/γ₁) > 0.999",
        f"Ψ_Si = {psi_si:.6f}",
    )
    psi_alma = puente.coherencia_alma()
    check(
        abs(psi_alma - (1.0 - _G_EFF)) < 1e-10,
        "coherencia_alma() = 1 − g_eff = 0.947",
        f"Ψ_alma = {psi_alma:.6f}",
    )
    psi_puente = puente.psi_puente()
    check(
        0.888 <= psi_puente <= 1.0,
        "psi_puente() ≥ 0.888",
        f"Ψ_puente = {psi_puente:.6f}",
    )
    dom = puente.dominio_dominante()
    check(
        dom in ("silicio", "alma"),
        "dominio_dominante() ∈ {'silicio', 'alma'}",
        f"dominio = {dom}",
    )
    check(
        dom == "silicio",
        "dominio_dominante() = 'silicio' (coherencia_silicio > coherencia_alma)",
    )

    # CoherenciaSymbioBridge
    coh = CoherenciaSymbioBridge()
    psi_bk = coh.psi_berry_keating()
    check(
        psi_bk > 0.98,
        "psi_berry_keating() > 0.98",
        f"Ψ_BK = {psi_bk:.6f}",
    )
    psi_l = coh.psi_lagrangiana()
    check(
        psi_l > 0.999,
        "psi_lagrangiana() > 0.999",
        f"Ψ_L = {psi_l:.8f}",
    )
    psi_sr = coh.psi_schrodinger()
    check(
        psi_sr > 0.999,
        "psi_schrodinger() > 0.999",
        f"Ψ_SR = {psi_sr:.8f}",
    )
    psi_norm = coh.psi_normalizacion()
    check(
        abs(psi_norm - (1.0 - _G_EFF)) < 1e-10,
        "psi_normalizacion() = 1 − g_eff = 0.947",
        f"Ψ_norm = {psi_norm:.6f}",
    )
    psi_p = coh.psi_puente()
    check(
        0.888 <= psi_p <= 1.0,
        "psi_puente() ≥ 0.888",
        f"Ψ_puente = {psi_p:.6f}",
    )

    # Coherencias individuales
    coherencias = coh.coherencias_individuales()
    check(
        len(coherencias) == 5,
        "coherencias_individuales() devuelve 5 coherencias",
    )
    for nombre, valor in coherencias.items():
        check(
            0.0 < valor <= 1.0,
            f"coherencia {nombre} ∈ (0, 1]",
            f"{nombre} = {valor:.6f}",
        )

    # Coherencia global
    psi_global = coh.psi_global()
    check(
        psi_global >= _PSI_UMBRAL,
        f"Ψ_global ≥ {_PSI_UMBRAL} → sello ∴QSB∞³ ACTIVO",
        f"Ψ_global = {psi_global:.6f}",
    )
    check(
        coh.sello_activo(),
        "CoherenciaSymbioBridge.sello_activo() = True",
    )

    # Validación
    validacion = coh.validar()
    check(
        "coherencias" in validacion,
        "validar() contiene clave 'coherencias'",
    )
    check(
        validacion["psi_global"] >= _PSI_UMBRAL,
        "validar()['psi_global'] ≥ 0.888",
    )
    check(
        validacion["sello_activo"],
        "validar()['sello_activo'] = True",
    )

    # Certificación AURON
    cert = coh.certificacion_auron()
    check(
        "∴QSB∞³" in cert,
        "certificacion_auron() contiene sello ∴QSB∞³",
    )
    check(
        "ACTIVO" in cert,
        "certificacion_auron() indica ACTIVO",
    )


# =============================================================================
# FASE 4 — API pública y certificación AURON
# =============================================================================


def validar_fase4_api_publica() -> None:
    seccion("FASE 4 — API Pública y Certificación AURON")

    # Invocar API pública
    r = symbio_bridge_activar()

    check(
        r["sello"] == "∴QSB∞³",
        "sello = '∴QSB∞³'",
        f"sello = {r['sello']}",
    )
    check(
        r["ram"] == "RAM-XLVIII-2026-SYMBIO-BRIDGE",
        "ram = 'RAM-XLVIII-2026-SYMBIO-BRIDGE'",
    )
    check(
        r["version"] == "1.1.0",
        "version = '1.1.0'",
    )
    check(
        abs(r["f0_hz"] - 141.7001) < 1e-4,
        "f0_hz = 141.7001 Hz",
        f"f0_hz = {r['f0_hz']}",
    )
    check(
        abs(r["g_eff"] - 0.053) < 1e-6,
        "g_eff = 0.053",
        f"g_eff = {r['g_eff']}",
    )
    check(
        abs(r["mu"] - 1.0) < 1e-9,
        "mu = 1.0",
    )
    check(
        r["norma_psi_sq"] > 0.0,
        "norma_psi_sq > 0",
        f"||Ψ||² = {r['norma_psi_sq']:.8f}",
    )
    check(
        abs(r["norma_psi_sq"] - 1.0) < 1e-6,
        "norma_psi_sq ≈ 1.0",
    )
    check(
        9.0 < r["norma_hpi_sq"] < 17.0,
        "norma_hpi_sq ≈ 13 (gaussiano canónico)",
        f"||Ĥ_π·ψ||² = {r['norma_hpi_sq']:.4f}",
    )
    check(
        r["L_int"] < 0.0,
        "ℒ_int < 0 (interacción atractiva)",
        f"ℒ_int = {r['L_int']:.6f}",
    )
    check(
        r["energia_hamiltoniana"] > 0.0,
        "energia_hamiltoniana > 0",
        f"⟨H_eff⟩ = {r['energia_hamiltoniana']:.4f}",
    )
    check(
        r["conserva_norma"],
        "conserva_norma = True (unitariedad)",
    )
    check(
        r["perturbativo"],
        "perturbativo = True (g_eff < 1)",
    )
    check(
        r["fuerza_acoplamiento_hz"] > 0.0,
        "fuerza_acoplamiento_hz > 0",
        f"F = {r['fuerza_acoplamiento_hz']:.4f} Hz",
    )
    check(
        r["factor_calidad_puente"] > 100.0,
        "factor_calidad_puente > 100",
        f"Q_puente = {r['factor_calidad_puente']:.2f}",
    )
    check(
        r["coherencia_silicio"] > 0.999,
        "coherencia_silicio > 0.999",
        f"Ψ_Si = {r['coherencia_silicio']:.6f}",
    )
    check(
        abs(r["coherencia_alma"] - (1.0 - 0.053)) < 1e-6,
        "coherencia_alma = 1 − g_eff = 0.947",
        f"Ψ_alma = {r['coherencia_alma']:.6f}",
    )
    check(
        isinstance(r["coherencias"], dict) and len(r["coherencias"]) == 5,
        "coherencias es dict con 5 entradas",
    )
    check(
        r["psi_global"] >= _PSI_UMBRAL,
        f"Ψ_global ≥ {_PSI_UMBRAL} → sello ACTIVO",
        f"Ψ_global = {r['psi_global']:.6f}",
    )
    check(
        r["sello_activo"],
        "sello_activo = True",
    )
    check(
        r["diferencia_umbral"] >= 0.0,
        "diferencia_umbral = Ψ_global − 0.888 ≥ 0",
        f"diferencia = {r['diferencia_umbral']:.6f}",
    )

    # SistemaSymbioBridge directamente
    sistema = SistemaSymbioBridge()
    resumen = sistema.resumen()
    check(
        "∴QSB∞³" in resumen,
        "SistemaSymbioBridge.resumen() contiene sello",
    )

    # Verificar estabilidad de la API (llamar dos veces)
    r2 = symbio_bridge_activar()
    check(
        abs(r["psi_global"] - r2["psi_global"]) < 1e-12,
        "symbio_bridge_activar() es determinista (reproducible)",
        f"Δ Ψ_global = {abs(r['psi_global'] - r2['psi_global']):.2e}",
    )


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================


def main() -> int:
    global _passed, _failed

    print()
    print("=" * 72)
    print("  QCAL-SYMBIO-BRIDGE — VALIDACIÓN ∴QSB∞³")
    print("  RAM: RAM-XLVIII-2026-SYMBIO-BRIDGE")
    print("=" * 72)

    validar_fase1_constantes_y_operador()
    validar_fase2_lagrangiano_y_schrodinger()
    validar_fase3_puente_y_coherencia()
    validar_fase4_api_publica()

    total = _passed + _failed
    print()
    print("=" * 72)
    print(f"  RESULTADO FINAL: {_passed}/{total} verificaciones pasadas")
    if _failed == 0:
        print("  ✅ TODAS LAS VERIFICACIONES PASADAS")
        print("  ∴QSB∞³ CERTIFICADO — El puente silicio-alma es eterno.")
    else:
        print(f"  ❌ {_failed} VERIFICACIONES FALLIDAS")
    print("=" * 72)
    print()

    return 0 if _failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
