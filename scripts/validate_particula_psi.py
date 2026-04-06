#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              VALIDACIÓN PARTÍCULA Ψ — PSI PARTICLE                           ║
║                   Fenomenología Inmediata (Labs 2026)                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Script de validación para el módulo physics/particula_psi.py

Fases de validación:
    1. Constantes fundamentales y masa m_ψ
    2. LIGO/Virgo detección coherente
    3. Birrefringencia del vacío
    4. Estadística GUE de biofotones
    5. Coherencia global Ψ_global ≥ 0.888

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
FECHA: 6 de abril de 2026
"""

import sys
import math
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.particula_psi import (
    particula_psi_activar,
    ConstantesParticulaPsi,
    ModoLIGOVirgo,
    VacuoBirefringencia,
    BiofotonesGUE,
    AcoplamientoCoherente,
    FirmaEspectral,
    CoherenciaParticulaPsi,
    SistemaParticulaPsi,
)

# Global counters
PASADO = 0
FALLIDO = 0

def check(condicion: bool, descripcion: str, detalle: str = "") -> None:
    """
    Valida una condición y actualiza contadores.
    
    Parameters
    ----------
    condicion : bool
        Condición a validar
    descripcion : str
        Descripción del test
    detalle : str, optional
        Detalle adicional
    """
    global PASADO, FALLIDO
    
    if condicion:
        PASADO += 1
        print(f"  ✅ {descripcion}")
        if detalle:
            print(f"     → {detalle}")
    else:
        FALLIDO += 1
        print(f"  ❌ {descripcion}")
        if detalle:
            print(f"     → {detalle}")

def separador(titulo: str) -> None:
    """Imprime un separador visual."""
    print(f"\n{'=' * 70}")
    print(f"{titulo}")
    print('=' * 70)

def fase_1_constantes() -> None:
    """FASE 1: Validación de constantes fundamentales y masa."""
    separador("FASE 1: CONSTANTES FUNDAMENTALES Y MASA m_ψ")
    
    const = ConstantesParticulaPsi()
    
    # Frecuencia fundamental
    check(
        abs(const.f0 - 141.7001) < 1e-6,
        "Frecuencia fundamental f₀ = 141.7001 Hz",
        f"f₀ = {const.f0:.6f} Hz"
    )
    
    # Razón áurea
    phi_expected = (1.0 + math.sqrt(5.0)) / 2.0
    check(
        abs(const.phi - phi_expected) < 1e-9,
        "Razón áurea φ ≈ 1.618034",
        f"φ = {const.phi:.9f}"
    )
    
    # Compactificación φ¹²
    check(
        const.validar_phi_12(),
        "Compactificación φ¹² ≈ 1442.220",
        f"φ¹² = {const.phi_12:.6f}"
    )
    
    # Masa de la partícula Ψ
    check(
        abs(const.m_psi_ev - 5.861427e-13) < 1e-18,
        "Masa m_ψ = 5.861427×10⁻¹³ eV",
        f"m_ψ = {const.m_psi_ev:.6e} eV"
    )
    
    # Validación de la fórmula de masa
    check(
        const.validar_masa(),
        "Fórmula de masa: m_ψ = ħ×f₀/(c²×φ¹²)",
        "Error relativo < 10⁻⁹"
    )
    
    # Longitud de onda Compton
    lambda_c = const.compton_wavelength()
    check(
        lambda_c > 0 and lambda_c < 1e10,
        "Longitud de onda Compton física",
        f"λ_C = {lambda_c:.6e} m"
    )
    
    # Tiempo Compton
    tau_c = const.tiempo_compton()
    check(
        tau_c > 0 and tau_c < 1e3,
        "Tiempo Compton físico",
        f"τ_C = {tau_c:.6e} s"
    )
    
    # Energía en reposo
    E_rest = const.energia_reposo()
    check(
        E_rest > 0,
        "Energía en reposo E = m_ψ c²",
        f"E = {E_rest:.6e} J"
    )
    
    # Temperatura equivalente
    T_eq = const.temperatura_equivalente()
    check(
        T_eq > 0 and T_eq < 1e10,
        "Temperatura equivalente física",
        f"T_eq = {T_eq:.6e} K"
    )
    
    # Umbral de coherencia
    check(
        abs(const.psi_umbral - 0.888) < 1e-10,
        "Umbral de coherencia Ψ_umbral = 0.888",
        f"Ψ_umbral = {const.psi_umbral:.3f}"
    )

def fase_2_ligo_virgo() -> None:
    """FASE 2: Validación de detección LIGO/Virgo."""
    separador("FASE 2: LIGO/VIRGO — LATIDO COHERENTE")
    
    ligo = ModoLIGOVirgo()
    
    # Frecuencia de detección
    check(
        abs(ligo.f0 - 141.7001) < 1e-6,
        "Frecuencia de detección = 141.7001 Hz",
        f"f₀ = {ligo.f0:.6f} Hz"
    )
    
    # Potencia espectral de strain
    check(
        abs(ligo.strain_power - 1e-24) < 1e-25,
        "Potencia espectral S_h(f) ≈ 10⁻²⁴ strain²/Hz",
        f"S_h = {ligo.strain_power:.2e} strain²/Hz"
    )
    
    # SNR
    check(
        abs(ligo.snr - 7.47) < 0.1,
        "Signal-to-noise ratio SNR = 7.47",
        f"SNR = {ligo.snr:.2f}"
    )
    
    # Factor de calidad
    check(
        ligo.q_factor >= 1e6,
        "Factor de calidad Q > 10⁶",
        f"Q = {ligo.q_factor:.2e}"
    )
    
    # Ancho de línea
    check(
        ligo.delta_f < 1e-6,
        "Ancho de línea Δf < 10⁻⁶ Hz",
        f"Δf = {ligo.delta_f:.2e} Hz"
    )
    
    # Amplitud de strain
    h0 = ligo.strain_amplitude()
    check(
        h0 > 0 and h0 < 1e-15,
        "Amplitud de strain h₀ física",
        f"h₀ = {h0:.6e}"
    )
    
    # Señal de strain
    h_t = ligo.strain_signal(t=0.0)
    check(
        abs(h_t) <= h0,
        "Señal de strain h(t) acotada",
        f"h(0) = {h_t:.6e}"
    )
    
    # Energía gravitacional
    E_gw = ligo.energia_gravitacional()
    check(
        E_gw > 0,
        "Energía gravitacional positiva",
        f"E_gw = {E_gw:.6e}"
    )
    
    # Calidad de la línea espectral
    Q_bw = ligo.bandwidth_quality()
    check(
        Q_bw > 1e6,
        "Calidad de línea Q = f₀/Δf > 10⁶",
        f"Q_bw = {Q_bw:.2e}"
    )
    
    # Tiempo de coherencia
    tau_coh = ligo.coherence_time()
    check(
        tau_coh > 1.0,
        "Tiempo de coherencia > 1 s",
        f"τ_coh = {tau_coh:.6e} s"
    )
    
    # Parámetros del notch filter
    notch = ligo.notch_filter_params()
    check(
        abs(notch["f_center_hz"] - 141.7001) < 1e-6,
        "Notch filter centrado en f₀",
        f"f_center = {notch['f_center_hz']:.6f} Hz"
    )
    
    # Coherencia LIGO
    psi_ligo = ligo.psi_ligo()
    check(
        0.0 <= psi_ligo <= 1.0,
        "Coherencia ψ_LIGO ∈ [0, 1]",
        f"ψ_LIGO = {psi_ligo:.6f}"
    )

def fase_3_vacuum_birefringencia() -> None:
    """FASE 3: Validación de birrefringencia del vacío."""
    separador("FASE 3: BIRREFRINGENCIA DEL VACÍO")
    
    vacuum = VacuoBirefringencia()
    
    # Masa de la partícula
    check(
        abs(vacuum.m_psi_ev - 5.861427e-13) < 1e-18,
        "Masa m_ψ correcta",
        f"m_ψ = {vacuum.m_psi_ev:.6e} eV"
    )
    
    # Parámetro de birrefringencia
    alpha = vacuum.alpha_psi()
    check(
        alpha > 0,
        "Parámetro α_Ψ = (m_ψ c / ħ)² positivo",
        f"α_Ψ = {alpha:.6e}"
    )
    
    # Rotación de polarización por metro
    delta_theta_per_m = vacuum.delta_theta_per_meter()
    check(
        delta_theta_per_m > 0,
        "Birrefringencia Δθ/L > 0",
        f"Δθ/L = {delta_theta_per_m:.6e} rad/m"
    )
    
    # Comparación con predicción Marte-Tierra
    expected_mars = 1.4e-14  # rad/m
    ratio = delta_theta_per_m / expected_mars
    check(
        0.1 < ratio < 10.0,
        "Birrefringencia orden de magnitud correcto",
        f"Ratio predicción = {ratio:.2f}"
    )
    
    # Rotación total
    delta_theta_t = vacuum.delta_theta(t=0.0)
    check(
        abs(delta_theta_t) < 1e-5,
        "Rotación total física",
        f"Δθ(0) = {delta_theta_t:.6e} rad"
    )
    
    # Setup DSN
    dsn = vacuum.setup_dsn_interferometry()
    check(
        "frequency_hz" in dsn and abs(dsn["frequency_hz"] - 141.7001) < 1e-6,
        "Setup DSN con frecuencia correcta",
        f"f_DSN = {dsn['frequency_hz']:.6f} Hz"
    )
    
    check(
        "distance_km" in dsn and dsn["distance_km"] > 1e7,
        "Distancia DSN Marte-Tierra",
        f"L = {dsn['distance_km']:.2e} km"
    )
    
    check(
        "sensitivity_rad" in dsn and dsn["sensitivity_rad"] < 1e-10,
        "Sensibilidad angular adecuada",
        f"Resolución = {dsn['sensitivity_rad']:.2e} rad"
    )
    
    # Coherencia vacuum
    psi_vacuum = vacuum.psi_vacuum()
    check(
        0.0 <= psi_vacuum <= 1.0,
        "Coherencia ψ_vacuum ∈ [0, 1]",
        f"ψ_vacuum = {psi_vacuum:.6f}"
    )

def fase_4_biofotones_gue() -> None:
    """FASE 4: Validación de estadística GUE."""
    separador("FASE 4: BIOFOTONES — ESTADÍSTICA GUE")
    
    gue = BiofotonesGUE()
    
    # Frecuencia fundamental
    check(
        abs(gue.f0 - 141.7001) < 1e-6,
        "Frecuencia f₀ correcta",
        f"f₀ = {gue.f0:.6f} Hz"
    )
    
    # Número de eigenvalores
    check(
        gue.n_eigenvalues >= 10,
        "Número de eigenvalores suficiente",
        f"N = {gue.n_eigenvalues}"
    )
    
    # Distribución de Wigner en s=0 (repulsión de niveles)
    P_0 = gue.wigner_surmise(0.0)
    check(
        P_0 < 0.01,
        "Repulsión de niveles: P(0) ≈ 0",
        f"P(0) = {P_0:.6e}"
    )
    
    # Distribución de Wigner en s=1 (pico)
    P_1 = gue.wigner_surmise(1.0)
    check(
        P_1 > 0.1,
        "Pico de Wigner cerca de s=1",
        f"P(1) = {P_1:.6f}"
    )
    
    # Espaciados de eigenvalores
    spacings = gue.eigenvalue_spacing()
    check(
        len(spacings) > 0,
        "Espaciados calculados",
        f"N_spacings = {len(spacings)}"
    )
    
    # Todos los espaciados positivos
    all_positive = all(s > 0 for s in spacings)
    check(
        all_positive,
        "Todos los espaciados positivos",
        f"min(s) = {min(spacings):.6f}" if spacings else "N/A"
    )
    
    # Repulsión de niveles
    level_rep = gue.level_repulsion()
    check(
        level_rep < 0.01,
        "Repulsión de niveles confirmada",
        f"P(0) = {level_rep:.6e}"
    )
    
    # Correlación espectral
    corr = gue.spectral_correlation()
    check(
        corr > 0,
        "Correlación espectral no trivial",
        f"R₂ = {corr:.6f}"
    )
    
    # Ratio super-Poisson
    ratio = gue.super_poisson_ratio()
    check(
        ratio > 1.0,
        "Estadística super-Poisson: Var/<n> > 1",
        f"Var/<n> = {ratio:.6f}"
    )
    
    # Tasa de emisión de biofotones
    rate = gue.biophoton_emission_rate()
    check(
        10.0 < rate < 200.0,
        "Tasa de emisión biológica",
        f"Rate = {rate:.2f} fotones/s"
    )
    
    # Coherencia GUE
    psi_gue = gue.psi_gue()
    check(
        0.0 <= psi_gue <= 1.0,
        "Coherencia ψ_GUE ∈ [0, 1]",
        f"ψ_GUE = {psi_gue:.6f}"
    )

def fase_5_coherencia_global() -> None:
    """FASE 5: Validación de coherencia global."""
    separador("FASE 5: COHERENCIA GLOBAL Ψ_global ≥ 0.888")
    
    # Crear sistema completo
    sistema = SistemaParticulaPsi()
    resultado = sistema.activar()
    
    # Verificar sello
    check(
        resultado["sello"] == "∴PSI∞³",
        "Sello correcto",
        f"Sello = {resultado['sello']}"
    )
    
    # Verificar RAM
    check(
        "RAM-LII-2026-PARTICULA-PSI" in resultado["ram"],
        "RAM ID correcto",
        f"RAM = {resultado['ram']}"
    )
    
    # Coherencias individuales
    coherencias = resultado["coherencias"]
    
    check(
        "psi_ligo" in coherencias,
        "Coherencia LIGO presente",
        f"ψ_LIGO = {coherencias.get('psi_ligo', 0.0):.6f}"
    )
    
    check(
        "psi_vacuum" in coherencias,
        "Coherencia vacuum presente",
        f"ψ_vacuum = {coherencias.get('psi_vacuum', 0.0):.6f}"
    )
    
    check(
        "psi_gue" in coherencias,
        "Coherencia GUE presente",
        f"ψ_GUE = {coherencias.get('psi_gue', 0.0):.6f}"
    )
    
    check(
        "psi_coupling" in coherencias,
        "Coherencia coupling presente",
        f"ψ_coupling = {coherencias.get('psi_coupling', 0.0):.6f}"
    )
    
    check(
        "psi_signature" in coherencias,
        "Coherencia signature presente",
        f"ψ_signature = {coherencias.get('psi_signature', 0.0):.6f}"
    )
    
    # Todas las coherencias en [0, 1]
    all_in_range = all(0.0 <= v <= 1.0 for v in coherencias.values())
    check(
        all_in_range,
        "Todas las coherencias ∈ [0, 1]",
        f"Rango OK"
    )
    
    # Coherencia global
    psi_global = resultado["psi_global"]
    check(
        0.0 <= psi_global <= 1.0,
        "Coherencia global ∈ [0, 1]",
        f"Ψ_global = {psi_global:.6f}"
    )
    
    # Media geométrica correcta
    producto = 1.0
    for v in coherencias.values():
        producto *= v
    psi_geo = producto ** (1.0 / len(coherencias))
    check(
        abs(psi_global - psi_geo) < 1e-9,
        "Media geométrica correcta",
        f"Ψ_global = {psi_global:.6f}, Ψ_geo = {psi_geo:.6f}"
    )
    
    # Umbral
    check(
        abs(resultado["psi_umbral"] - 0.888) < 1e-10,
        "Umbral correcto Ψ_umbral = 0.888",
        f"Umbral = {resultado['psi_umbral']:.3f}"
    )
    
    # Sello activo
    sello_activo = resultado["sello_activo"]
    check(
        isinstance(sello_activo, bool),
        "Sello activo es booleano",
        f"Sello = {sello_activo}"
    )
    
    # Consistencia de sello
    sello_esperado = (psi_global >= 0.888)
    check(
        sello_activo == sello_esperado,
        "Sello consistente con Ψ_global",
        f"Ψ_global = {psi_global:.6f}, Sello = {sello_activo}"
    )
    
    # Validaciones adicionales
    check(
        resultado["masa_validada"] == True,
        "Masa validada",
        "Fórmula correcta"
    )
    
    check(
        resultado["phi_12_validada"] == True,
        "φ¹² validada",
        "Compactificación correcta"
    )

def main():
    """Ejecuta todas las fases de validación."""
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║         VALIDACIÓN PARTÍCULA Ψ — FENOMENOLOGÍA INMEDIATA            ║")
    print("╚══════════════════════════════════════════════════════════════════════╝\n")
    
    # Ejecutar fases
    fase_1_constantes()
    fase_2_ligo_virgo()
    fase_3_vacuum_birefringencia()
    fase_4_biofotones_gue()
    fase_5_coherencia_global()
    
    # Reporte final
    print(f"\n{'=' * 70}")
    print("REPORTE FINAL")
    print('=' * 70)
    print(f"✅ Pasado:  {PASADO}")
    print(f"❌ Fallido: {FALLIDO}")
    print(f"Total:     {PASADO + FALLIDO}")
    
    if FALLIDO == 0:
        print(f"\n🎉 VALIDACIÓN COMPLETA: Todos los tests pasaron.")
        print(f"   La partícula Ψ está correctamente implementada.\n")
        return 0
    else:
        print(f"\n⚠️  VALIDACIÓN INCOMPLETA: {FALLIDO} tests fallaron.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
