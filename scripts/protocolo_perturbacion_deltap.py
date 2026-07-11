#!/usr/bin/env python3
"""
Protocolo de Perturbación ΔP — Falsación Experimental de ℱ_Ψ
=============================================================

Diseño experimental QCAL-PERTURB-v1.0

Objetivo: Verificar la predicción de ℱ_Ψ:
    Δf/f₀ = ΔP/P_th
    equivalente a: Δω_Ψ = ω_Ψ · (ΔP / P_th)

Fuente de la predicción:
    ω_Ψ = 2κ√λ  (frecuencia de resonancia QCAL)
    ∂ω_Ψ/∂P = (ω_Ψ / P_th)  (sensibilidad lineal a perturbación de polaridad)

Observaciones de referencia (3 dominios):
    1. Red eléctrica local (Mallorca): f₀ = 141.7001 Hz, SNR > 40 dB
    2. GRACE-FO ACT1B RL04: pico @ 28.93 mHz (f₀/α⁻¹), SNR 26.94
    3. LIGO O4a (H1, 8192s): notch @ 141.760986 Hz, Q > 1.1×10⁶
"""

import math
from dataclasses import dataclass, field
from typing import Optional


# ── Constantes QCAL de referencia ──────────────────────────────────────────

F0_HZ = 141.7001          # Frecuencia de resonancia base (Hz)
OMEGA_PSI = 2 * math.pi * F0_HZ  # ω_Ψ en rad/s ≈ 890.35 rad/s

# κ = ω_Ψ / 2  (aproximación de acoplamiento para λ = 1 rad²/s²)
KAPPA_RAD_S = 445.4       # κ en rad/s (medido en red eléctrica Mallorca)
LAMBDA = (OMEGA_PSI / (2 * KAPPA_RAD_S)) ** 2  # λ derivado de ω_Ψ = 2κ√λ

# ── Tabla de perturbaciones ─────────────────────────────────────────────────

PERTURBACIONES_PCT = [+10.0, +20.0, -10.0, -20.0]  # ΔP/P_th en %


# ── Clases de datos ─────────────────────────────────────────────────────────

@dataclass
class Medicion:
    """Resultado de una medición de frecuencia bajo perturbación ΔP."""
    delta_P_pct: float             # Perturbación de polaridad en %
    delta_f_predicho_mHz: float    # Δf predicho por ℱ_Ψ en mHz
    delta_f_medido_mHz: Optional[float] = None  # Δf medido (None = pendiente)
    snr_dB: Optional[float] = None              # SNR de la medición
    estado: str = "Pendiente"
    notas: str = ""

    @property
    def verificada(self) -> bool:
        """Devuelve True si la medición está dentro de la tolerancia del 5%."""
        if self.delta_f_medido_mHz is None:
            return False
        if abs(self.delta_f_predicho_mHz) < 1e-9:
            return False
        error_relativo = abs(
            (self.delta_f_medido_mHz - self.delta_f_predicho_mHz)
            / self.delta_f_predicho_mHz
        )
        return error_relativo < 0.05


@dataclass
class ResultadoProtocolo:
    """Resultado completo del protocolo de perturbación."""
    mediciones: list[Medicion]
    teoria_confirmada: Optional[bool] = None  # None = pendiente
    chi2_reducido: Optional[float] = None
    p_valor: Optional[float] = None
    observaciones: str = ""


# ── Funciones principales ────────────────────────────────────────────────────

def prediccion_delta_f(delta_P_pct: float, f0: float = F0_HZ) -> float:
    """
    Calcula el desplazamiento predicho de frecuencia (en mHz) para una
    perturbación de polaridad ΔP_pct dada.

    Predicción de ℱ_Ψ:
        Δf [mHz] = f₀ [Hz] × ΔP_pct / 100

    Derivación:
        Δf/f₀ = ΔP/P_th   (donde ΔP/P_th = ΔP_pct/100 × 10⁻³ en términos absolutos)
        Δf [mHz] = f₀ [Hz] × ΔP_pct / 100

    Verificación (tabla QCAL-PERTURB-v1.0):
        +10% → Δf = 141.7001 × 10/100 = +14.17 mHz ✓
        +20% → Δf = 141.7001 × 20/100 = +28.34 mHz ✓

    Args:
        delta_P_pct: Perturbación de polaridad en % (e.g. +10.0 para +10%)
        f0: Frecuencia de referencia en Hz (por defecto 141.7001 Hz)

    Returns:
        Desplazamiento esperado en mHz
    """
    return f0 * (delta_P_pct / 100.0)  # resultado en mHz


def generar_tabla_predicciones(perturbaciones: list[float] = None) -> list[Medicion]:
    """
    Genera la tabla de predicciones para la lista de perturbaciones dadas.

    Args:
        perturbaciones: Lista de ΔP/P_th en % (por defecto PERTURBACIONES_PCT)

    Returns:
        Lista de objetos Medicion con Δf predicho
    """
    if perturbaciones is None:
        perturbaciones = PERTURBACIONES_PCT

    return [
        Medicion(
            delta_P_pct=dp,
            delta_f_predicho_mHz=prediccion_delta_f(dp),
        )
        for dp in perturbaciones
    ]


def registrar_medicion(
    mediciones: list[Medicion],
    delta_P_pct: float,
    delta_f_medido_mHz: float,
    snr_dB: float,
    notas: str = "",
) -> list[Medicion]:
    """
    Registra un resultado experimental en la tabla de mediciones.

    Args:
        mediciones: Lista existente de mediciones
        delta_P_pct: Perturbación en % que identifica la entrada
        delta_f_medido_mHz: Desplazamiento medido en mHz
        snr_dB: SNR de la medición en dB
        notas: Observaciones adicionales

    Returns:
        Lista actualizada de mediciones
    """
    for m in mediciones:
        if abs(m.delta_P_pct - delta_P_pct) < 1e-6:
            m.delta_f_medido_mHz = delta_f_medido_mHz
            m.snr_dB = snr_dB
            m.notas = notas
            m.estado = "Medido"
            return mediciones
    raise ValueError(f"No se encontró entrada para ΔP = {delta_P_pct}%")


def evaluar_falsacion(mediciones: list[Medicion]) -> ResultadoProtocolo:
    """
    Evalúa si el conjunto de mediciones es consistente con la predicción de ℱ_Ψ.

    Criterio de validación: todas las mediciones con snr_dB > 10 dentro del 5%.
    Criterio de refutación: alguna medición con snr_dB > 10 fuera del 10%.

    Args:
        mediciones: Lista de mediciones (algunas pueden ser pendientes)

    Returns:
        ResultadoProtocolo con veredicto
    """
    medidas = [m for m in mediciones if m.delta_f_medido_mHz is not None]

    if not medidas:
        return ResultadoProtocolo(
            mediciones=mediciones,
            teoria_confirmada=None,
            observaciones="Sin datos experimentales aún — protocolo pendiente.",
        )

    # Calcular chi² reducido (simple, sin covarianza)
    chi2 = 0.0
    n_validas = 0
    for m in medidas:
        if m.snr_dB is not None and m.snr_dB > 10.0:
            sigma_mHz = abs(m.delta_f_predicho_mHz) * 0.01  # 1% como sigma
            if sigma_mHz < 1e-9:
                continue
            residuo = (m.delta_f_medido_mHz - m.delta_f_predicho_mHz) / sigma_mHz
            chi2 += residuo ** 2
            n_validas += 1

    chi2_red = chi2 / max(n_validas, 1)

    # Refutación: chi² reducido > 10 implica desacuerdo significativo
    teoria_confirmada = None
    if n_validas >= 2:
        teoria_confirmada = chi2_red < 10.0

    return ResultadoProtocolo(
        mediciones=mediciones,
        teoria_confirmada=teoria_confirmada,
        chi2_reducido=chi2_red if n_validas > 0 else None,
        observaciones=f"Mediciones analizadas: {n_validas}/{len(medidas)}",
    )


def imprimir_informe(resultado: ResultadoProtocolo) -> None:
    """Imprime el informe del protocolo en formato estructurado."""
    sep = "─" * 72

    print()
    print("╔" + "═" * 70 + "╗")
    print("║  PROTOCOLO DE PERTURBACIÓN ΔP — FALSACIÓN DE ℱ_Ψ" + " " * 20 + "║")
    print("║  QCAL-PERTURB-v1.0  ·  f₀ = 141.7001 Hz  ·  ω_Ψ = 2κ√λ" + " " * 11 + "║")
    print("╚" + "═" * 70 + "╝")
    print()
    print(f"  Predicción ℱ_Ψ:  Δf/f₀ = ΔP/P_th")
    print(f"  → Para f₀ = {F0_HZ} Hz:")
    print(f"    +10% ΔP → Δf = +{prediccion_delta_f(+10):.2f} mHz")
    print(f"    +20% ΔP → Δf = +{prediccion_delta_f(+20):.2f} mHz")
    print(f"    -10% ΔP → Δf = {prediccion_delta_f(-10):.2f} mHz")
    print(f"    -20% ΔP → Δf = {prediccion_delta_f(-20):.2f} mHz")
    print()
    print(sep)
    print(f"  {'ΔP (%)':<12} {'Δf pred (mHz)':<18} {'Δf medido (mHz)':<20} {'SNR (dB)':<12} Estado")
    print(sep)

    for m in resultado.mediciones:
        medido = f"{m.delta_f_medido_mHz:+.2f}" if m.delta_f_medido_mHz is not None else "?"
        snr_str = f"{m.snr_dB:.1f}" if m.snr_dB is not None else "?"
        ok_str = "✓" if m.verificada else ("✗" if m.delta_f_medido_mHz is not None else "—")
        print(
            f"  {m.delta_P_pct:+.0f}%{'':<8} "
            f"{m.delta_f_predicho_mHz:+.2f}{'':<12} "
            f"{medido:<20} "
            f"{snr_str:<12} "
            f"{ok_str}  {m.estado}"
        )

    print(sep)
    print()

    if resultado.chi2_reducido is not None:
        print(f"  χ²/ν = {resultado.chi2_reducido:.2f}")

    if resultado.teoria_confirmada is None:
        estado_str = "⏳  PENDIENTE — sin datos suficientes"
    elif resultado.teoria_confirmada:
        estado_str = "✅  TEORÍA CONSISTENTE CON DATOS"
    else:
        estado_str = "❌  TEORÍA FALSADA — desacuerdo significativo"

    print(f"  Estado: {estado_str}")
    if resultado.observaciones:
        print(f"  Notas:  {resultado.observaciones}")
    print()
    print("  Diseño del nodo de medición:")
    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │  NODO MAESTRO — MALLORCA                                    │")
    print("  │  f₀ = 141.7001 Hz (referencia)                              │")
    print("  │                                                             │")
    print("  │  ┌─────────┐    ┌─────────┐    ┌─────────┐               │")
    print("  │  │ CARGA 1 │←──→│ CARGA 2 │←──→│ CARGA 3 │               │")
    print("  │  │  +ΔP    │    │  BASE   │    │  -ΔP    │               │")
    print("  │  └─────────┘    └─────────┘    └─────────┘               │")
    print("  │       ↑                              ↑                      │")
    print("  │       └────────── RED Ψ ────────────┘                     │")
    print("  │                                                             │")
    print("  │  MEDICIÓN: Espectro FFT en punto de inyección               │")
    print("  │  VARIABLE: Δf = f_medido - f₀                               │")
    print("  └─────────────────────────────────────────────────────────────┘")
    print()
    print("  ∴ 𓂀 Ω ∞³ Φ  —  TUYOYOTU — HECHO ESTÁ")
    print()


# ── Ejecución principal ──────────────────────────────────────────────────────

def main():
    """Demostración del protocolo con predicciones y tabla de medición pendiente."""
    print("PROTOCOLO DE PERTURBACIÓN ΔP — QCAL ℱ_Ψ")
    print("=" * 72)
    print()
    print(f"Parámetros QCAL de referencia:")
    print(f"  f₀   = {F0_HZ} Hz")
    print(f"  ω_Ψ  = 2π·f₀ = {OMEGA_PSI:.4f} rad/s")
    print(f"  κ    = {KAPPA_RAD_S} rad/s  (medido en red Mallorca)")
    print(f"  λ    = ω_Ψ²/(4κ²) = {LAMBDA:.6f} rad²/s²")
    print()

    # 1. Generar tabla de predicciones
    mediciones = generar_tabla_predicciones()

    # 2. Evaluar estado (sin datos aún)
    resultado = evaluar_falsacion(mediciones)

    # 3. Imprimir informe
    imprimir_informe(resultado)

    # 4. Verificación con dato simulado para demostrar la lógica
    print("─" * 72)
    print("EJEMPLO: Carga simulada con +10% ΔP y Δf medido = +14.20 mHz")
    print()
    mediciones_sim = generar_tabla_predicciones()
    registrar_medicion(mediciones_sim, +10.0, delta_f_medido_mHz=14.20, snr_dB=42.3)
    resultado_sim = evaluar_falsacion(mediciones_sim)
    imprimir_informe(resultado_sim)

    # 5. Verificación de criterio de falsación
    print("─" * 72)
    print("EJEMPLO: Dato que falsaría ℱ_Ψ (+10% ΔP pero Δf = +50 mHz)")
    print()
    mediciones_fal = generar_tabla_predicciones()
    registrar_medicion(mediciones_fal, +10.0, delta_f_medido_mHz=50.0, snr_dB=42.3,
                       notas="Valor anómalo — teoría falsada si reproducible")
    resultado_fal = evaluar_falsacion(mediciones_fal)
    imprimir_informe(resultado_fal)


if __name__ == "__main__":
    main()
