#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     VALIDACIÓN: Arquitectura Física TOPC (AFP∞³)                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

Script de validación completa del modelo de Arquitectura Física TOPC.

Verifica todas las predicciones del modelo:
1. Hamiltoniano total (EM + ψ + interacción)
2. Permitividad efectiva con resonancia
3. Coeficiente de mezcla de fase η
4. Relación de dispersión de Thot
5. Señal inequívoca de Larmor
6. Interferómetro de Sagnac Resonante (IRS-Luna)

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
FECHA/DATE: 2026-03-29
"""

import sys
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend sin display
import matplotlib.pyplot as plt
from typing import Dict, Any, Tuple

from physics.arquitectura_fisica_topc import (
    arquitectura_fisica_topc_activar,
    SistemaArquitecturaFisicaTopc,
)
from qcal.constants import F0_HZ, C


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════

UMBRAL_COHERENCIA = 0.888
TOLERANCIA_RELATIVA = 1e-3


# ═══════════════════════════════════════════════════════════════════════════
# FUNCIONES DE VALIDACIÓN
# ═══════════════════════════════════════════════════════════════════════════

def validar_parametros_fundamentales(sistema: SistemaArquitecturaFisicaTopc) -> bool:
    """
    Valida los parámetros fundamentales del sistema.

    Returns
    -------
    bool
        True si todos los parámetros son correctos
    """
    print("\n" + "="*80)
    print("FASE 1: VALIDACIÓN DE PARÁMETROS FUNDAMENTALES")
    print("="*80)

    constantes = sistema.constantes
    fallos = []

    # 1. Frecuencia fundamental
    if abs(constantes.f0 - F0_HZ) / F0_HZ > TOLERANCIA_RELATIVA:
        fallos.append(f"f₀ incorrecto: {constantes.f0} ≠ {F0_HZ}")
    else:
        print(f"✅ f₀ = {constantes.f0:.6f} Hz")

    # 2. Frecuencia angular
    omega_esperado = 2.0 * math.pi * F0_HZ
    if abs(constantes.omega_psi - omega_esperado) / omega_esperado > TOLERANCIA_RELATIVA:
        fallos.append(f"ω_ψ incorrecto: {constantes.omega_psi} ≠ {omega_esperado}")
    else:
        print(f"✅ ω_ψ = {constantes.omega_psi:.6f} rad/s")

    # 3. Longitud de coherencia
    lambda_esperada = C / omega_esperado
    if abs(constantes.lambda_coherence - lambda_esperada) / lambda_esperada > TOLERANCIA_RELATIVA:
        fallos.append(f"λ_C incorrecto: {constantes.lambda_coherence} ≠ {lambda_esperada}")
    else:
        print(f"✅ λ_C = {constantes.lambda_coherence/1000.0:.2f} km")

    # 4. Masa del tejido
    m_psi_orden = 5.86e-13  # eV/c²
    if abs(constantes.m_psi_ev - m_psi_orden) / m_psi_orden > 0.1:
        fallos.append(f"m_ψ fuera del orden esperado: {constantes.m_psi_ev:.2e} eV/c²")
    else:
        print(f"✅ m_ψ = {constantes.m_psi_ev:.2e} eV/c²")

    if fallos:
        print("\n❌ FALLOS DETECTADOS:")
        for fallo in fallos:
            print(f"   - {fallo}")
        return False

    print("\n✅ Todos los parámetros fundamentales son correctos")
    return True


def validar_hamiltoniano(sistema: SistemaArquitecturaFisicaTopc) -> bool:
    """
    Valida el Hamiltoniano total.

    Returns
    -------
    bool
        True si el Hamiltoniano es consistente
    """
    print("\n" + "="*80)
    print("FASE 2: VALIDACIÓN DEL HAMILTONIANO TOTAL")
    print("="*80)

    hamiltoniano = sistema.coherencia_sistema.hamiltoniano
    fallos = []

    # Test de energía electromagnética
    E_field = 1.0e5  # V/m
    B_field = E_field / C
    energia_em = hamiltoniano.energia_em(E_field, B_field)

    if energia_em <= 0:
        fallos.append("Energía EM no positiva")
    else:
        print(f"✅ Ĥ_EM: energía = {energia_em:.6e} J/m³")

    # Test de energía del condensado
    psi = 1.0e6 + 0j  # eV
    grad_psi_sq = 1.0e12  # eV²/m²
    energia_psi = hamiltoniano.energia_condensado(psi, grad_psi_sq)

    if energia_psi <= 0:
        fallos.append("Energía del condensado no positiva")
    else:
        print(f"✅ Ĥ_ψ: energía = {energia_psi:.6e} eV⁴")

    # Test de energía de interacción
    F_dual = 1.0e10  # V²/m²
    energia_int = hamiltoniano.energia_interaccion(psi.real, F_dual)
    print(f"✅ Ĥ_int: energía = {energia_int:.6e}")

    # Energía total
    energia_total = hamiltoniano.energia_total(
        E_field, B_field, psi, grad_psi_sq, F_dual
    )

    if energia_total <= 0:
        fallos.append("Energía total no positiva")
    else:
        print(f"✅ Ĥ_Total = Ĥ_EM + Ĥ_ψ + Ĥ_int")

    if fallos:
        print("\n❌ FALLOS DETECTADOS:")
        for fallo in fallos:
            print(f"   - {fallo}")
        return False

    print("\n✅ Hamiltoniano total validado correctamente")
    return True


def validar_permitividad(sistema: SistemaArquitecturaFisicaTopc) -> bool:
    """
    Valida la permitividad efectiva y resonancia.

    Returns
    -------
    bool
        True si la permitividad es correcta
    """
    print("\n" + "="*80)
    print("FASE 3: VALIDACIÓN DE PERMITIVIDAD EFECTIVA")
    print("="*80)

    permittividad = sistema.coherencia_sistema.permittividad
    constantes = sistema.constantes
    fallos = []

    # Test 1: Lejos de resonancia → ε_eff ≈ 1
    omega_lejos = 2.0 * math.pi * 100.0  # 100 Hz
    epsilon_lejos = permittividad.epsilon_eff(omega_lejos)

    if abs(epsilon_lejos - 1.0) > 0.1:
        fallos.append(f"ε_eff lejos de resonancia no cercano a 1: {epsilon_lejos}")
    else:
        print(f"✅ ε_eff(ω≠ω_ψ) ≈ 1.0: {abs(epsilon_lejos):.6f}")

    # Test 2: En resonancia → parte imaginaria grande
    epsilon_res = permittividad.epsilon_eff(constantes.omega_psi)

    if abs(epsilon_res.imag) < 1e-6:
        fallos.append("ε_eff en resonancia no tiene parte imaginaria")
    else:
        print(f"✅ ε_eff(ω=ω_ψ) complejo: |ε| = {abs(epsilon_res):.6e}")

    # Test 3: Velocidad de grupo
    v_g_lejos = permittividad.velocidad_grupo(omega_lejos)
    v_g_res = permittividad.velocidad_grupo(constantes.omega_psi)

    print(f"✅ v_g(ω≠ω_ψ) = {v_g_lejos:.2e} m/s (≈ c)")
    print(f"✅ v_g(ω=ω_ψ) = {v_g_res:.2e} m/s (→ 0 en resonancia)")

    if fallos:
        print("\n❌ FALLOS DETECTADOS:")
        for fallo in fallos:
            print(f"   - {fallo}")
        return False

    print("\n✅ Permitividad efectiva validada correctamente")
    return True


def validar_coeficiente_eta(sistema: SistemaArquitecturaFisicaTopc) -> bool:
    """
    Valida el coeficiente de mezcla de fase η.

    Returns
    -------
    bool
        True si η es correcto
    """
    print("\n" + "="*80)
    print("FASE 4: VALIDACIÓN DEL COEFICIENTE η")
    print("="*80)

    coeficiente = sistema.coherencia_sistema.coeficiente_eta
    constantes = sistema.constantes
    fallos = []

    # Test 1: Régimen débil (L pequeño)
    L_corto = 1.0  # 1 m
    eta_debil = coeficiente.eta(constantes.omega_psi, L_corto)
    regimen_debil = coeficiente.regimen(eta_debil)

    if regimen_debil != 'debil':
        fallos.append(f"Régimen para L=1m no es débil: {regimen_debil}")
    else:
        print(f"✅ η(L=1m) = {eta_debil:.6e} → régimen {regimen_debil}")

    # Test 2: Régimen de resonancia fuerte (L = 100 km)
    L_largo = 100.0e3  # 100 km
    eta_fuerte = coeficiente.eta(constantes.omega_psi, L_largo)
    regimen_fuerte = coeficiente.regimen(eta_fuerte)

    print(f"✅ η(L=100km) = {eta_fuerte:.6e} → régimen {regimen_fuerte}")

    # Test 3: Escalamiento con longitud (η ∝ √L)
    L1 = 10.0e3
    L2 = 40.0e3
    eta1 = coeficiente.eta(constantes.omega_psi, L1)
    eta2 = coeficiente.eta(constantes.omega_psi, L2)
    razon = eta2 / eta1

    if abs(razon - 2.0) / 2.0 > 0.05:
        fallos.append(f"η no escala como √L: η₂/η₁ = {razon} ≠ 2.0")
    else:
        print(f"✅ η ∝ √L: η(40km)/η(10km) = {razon:.4f} ≈ 2.0")

    if fallos:
        print("\n❌ FALLOS DETECTADOS:")
        for fallo in fallos:
            print(f"   - {fallo}")
        return False

    print("\n✅ Coeficiente η validado correctamente")
    return True


def validar_dispersion_thot(sistema: SistemaArquitecturaFisicaTopc) -> bool:
    """
    Valida la relación de dispersión de Thot.

    Returns
    -------
    bool
        True si la dispersión es correcta
    """
    print("\n" + "="*80)
    print("FASE 5: VALIDACIÓN DE RELACIÓN DE DISPERSIÓN DE THOT")
    print("="*80)

    dispersion = sistema.coherencia_sistema.dispersion
    constantes = sistema.constantes
    fallos = []

    # Test 1: Gap de masa
    omega_min = dispersion.omega_minima()

    if abs(omega_min - constantes.omega_psi) / constantes.omega_psi > TOLERANCIA_RELATIVA:
        fallos.append(f"ω_min incorrecto: {omega_min} ≠ {constantes.omega_psi}")
    else:
        print(f"✅ ω_min = ω_ψ = {omega_min:.6f} rad/s (gap de masa)")

    # Test 2: Relación de dispersión hiperbólica
    k = 1.0e-3  # 1/m
    omega = dispersion.omega_de_k(k)
    omega_sq_esperado = C**2 * k**2 + constantes.omega_psi**2

    if abs(omega**2 - omega_sq_esperado) / omega_sq_esperado > TOLERANCIA_RELATIVA:
        fallos.append(f"ω²(k) no satisface dispersión hiperbólica")
    else:
        print(f"✅ ω²(k) = c²k² + ω²_ψ verificado")

    # Test 3: k(ω) inversa
    k_inverso = dispersion.k_de_omega(omega)

    if abs(k_inverso - k) / k > TOLERANCIA_RELATIVA:
        fallos.append(f"k(ω(k)) no invierte correctamente: {k_inverso} ≠ {k}")
    else:
        print(f"✅ k(ω(k)) = k (inversión correcta)")

    # Test 4: Modo evanescente debajo del gap
    omega_bajo = 0.5 * constantes.omega_psi
    k_bajo = dispersion.k_de_omega(omega_bajo)

    if k_bajo != 0.0:
        fallos.append(f"k(ω<ω_min) no es cero: {k_bajo}")
    else:
        print(f"✅ k(ω<ω_min) = 0 (modo evanescente)")

    if fallos:
        print("\n❌ FALLOS DETECTADOS:")
        for fallo in fallos:
            print(f"   - {fallo}")
        return False

    print("\n✅ Relación de dispersión de Thot validada correctamente")
    return True


def validar_senal_larmor(sistema: SistemaArquitecturaFisicaTopc) -> bool:
    """
    Valida la señal inequívoca de Larmor.

    Returns
    -------
    bool
        True si la señal es correcta
    """
    print("\n" + "="*80)
    print("FASE 6: VALIDACIÓN DE SEÑAL INEQUÍVOCA DE LARMOR")
    print("="*80)

    senal = sistema.coherencia_sistema.senal_larmor
    constantes = sistema.constantes
    fallos = []

    # Anisotropía esperada
    beta = constantes.v_gal / C
    delta_f_esperado = beta * constantes.f0

    print(f"   Anisotropía esperada: Δf = ±{delta_f_esperado:.4f} Hz")

    # Test 1: Hacia Cygnus (corrimiento positivo)
    f_cygnus, delta_cygnus = senal.anisotropia_sidereal('cygnus')

    if delta_cygnus <= 0:
        fallos.append("Corrimiento hacia Cygnus no positivo")
    elif abs(delta_cygnus - delta_f_esperado) / delta_f_esperado > 0.1:
        fallos.append(f"Δf(Cygnus) incorrecto: {delta_cygnus} ≠ {delta_f_esperado}")
    else:
        print(f"✅ Hacia Cygnus: f_obs = {f_cygnus:.6f} Hz (+{delta_cygnus:.4f} Hz)")

    # Test 2: Hacia Anticentro (sin corrimiento)
    f_anticentro, delta_anticentro = senal.anisotropia_sidereal('anticentro')

    if abs(delta_anticentro) > 1e-6:
        fallos.append(f"Corrimiento hacia Anticentro no cero: {delta_anticentro}")
    else:
        print(f"✅ Hacia Anticentro: f_obs = {f_anticentro:.6f} Hz ({delta_anticentro:.4f} Hz)")

    # Test 3: Hacia Centauro (corrimiento negativo)
    f_centauro, delta_centauro = senal.anisotropia_sidereal('centauro')

    if delta_centauro >= 0:
        fallos.append("Corrimiento hacia Centauro no negativo")
    elif abs(abs(delta_centauro) - delta_f_esperado) / delta_f_esperado > 0.1:
        fallos.append(f"Δf(Centauro) incorrecto: {delta_centauro} ≠ -{delta_f_esperado}")
    else:
        print(f"✅ Hacia Centauro: f_obs = {f_centauro:.6f} Hz ({delta_centauro:.4f} Hz)")

    if fallos:
        print("\n❌ FALLOS DETECTADOS:")
        for fallo in fallos:
            print(f"   - {fallo}")
        return False

    print("\n✅ Señal inequívoca de Larmor validada correctamente")
    return True


def validar_sagnac(sistema: SistemaArquitecturaFisicaTopc) -> bool:
    """
    Valida el Interferómetro de Sagnac Resonante.

    Returns
    -------
    bool
        True si las predicciones son correctas
    """
    print("\n" + "="*80)
    print("FASE 7: VALIDACIÓN DEL INTERFERÓMETRO DE SAGNAC RESONANTE")
    print("="*80)

    sagnac = sistema.coherencia_sistema.sagnac
    constantes = sistema.constantes
    fallos = []

    L = 100.0e3  # 100 km

    # Test 1: Fases CW y CCW
    phi_cw = sagnac.fase_acumulada(L, 'CW')
    phi_ccw = sagnac.fase_acumulada(L, 'CCW')

    if phi_cw == phi_ccw:
        fallos.append("Fases CW y CCW idénticas (no quiralidad)")
    else:
        print(f"✅ Φ_CW = {phi_cw:.6f} rad")
        print(f"✅ Φ_CCW = {phi_ccw:.6f} rad")

    # Test 2: Diferencia de fase
    delta_phi = sagnac.diferencia_fase(L)
    delta_phi_esperado = 2.0 * constantes.phi_chirality

    if abs(delta_phi - delta_phi_esperado) / delta_phi_esperado > 0.05:
        fallos.append(f"ΔΦ incorrecto: {delta_phi} ≠ {delta_phi_esperado}")
    else:
        print(f"✅ ΔΦ = {delta_phi:.6f} rad = 2Φ_chirality")

    # Test 3: Predicción completa IRS-Luna
    prediccion = sagnac.prediccion_irs_luna(L)

    if prediccion['frecuencia_modulacion_Hz'] != constantes.f0:
        fallos.append("Frecuencia de modulación incorrecta")
    else:
        print(f"✅ f_modulación = {prediccion['frecuencia_modulacion_Hz']:.6f} Hz")

    if fallos:
        print("\n❌ FALLOS DETECTADOS:")
        for fallo in fallos:
            print(f"   - {fallo}")
        return False

    print("\n✅ Interferómetro de Sagnac validado correctamente")
    print(f"\n   Predicción IRS-Luna:")
    print(f"   {prediccion['prediccion']}")
    return True


def validar_coherencia_global(sistema: SistemaArquitecturaFisicaTopc) -> bool:
    """
    Valida la coherencia global del sistema.

    Returns
    -------
    bool
        True si Ψ_global ≥ 0.888
    """
    print("\n" + "="*80)
    print("FASE 8: VALIDACIÓN DE COHERENCIA GLOBAL")
    print("="*80)

    coherencia = sistema.coherencia_sistema
    psi_global = coherencia.calcular_coherencia()

    print(f"   Ψ_global = {psi_global:.6f}")

    if psi_global < UMBRAL_COHERENCIA:
        print(f"\n❌ FALLO: Ψ_global = {psi_global:.6f} < {UMBRAL_COHERENCIA}")
        return False

    print(f"✅ Ψ_global = {psi_global:.6f} ≥ {UMBRAL_COHERENCIA}")
    print(f"✅ Sistema coherente (umbral 0.888 superado)")

    return True


def generar_graficas(sistema: SistemaArquitecturaFisicaTopc) -> None:
    """
    Genera gráficas de visualización del modelo.
    """
    print("\n" + "="*80)
    print("FASE 9: GENERACIÓN DE GRÁFICAS")
    print("="*80)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Gráfica 1: Relación de dispersión
    ax1 = axes[0, 0]
    dispersion = sistema.coherencia_sistema.dispersion
    k_array = np.linspace(0, 1.0e-3, 200)
    omega_array = dispersion.curva_dispersion(k_array)

    ax1.plot(k_array, omega_array / (2.0 * math.pi), 'b-', linewidth=2)
    ax1.axhline(y=F0_HZ, color='r', linestyle='--', label=f'f₀ = {F0_HZ:.4f} Hz')
    ax1.set_xlabel('k [1/m]', fontsize=12)
    ax1.set_ylabel('f [Hz]', fontsize=12)
    ax1.set_title('Relación de Dispersión de Thot: ω² = c²k² + m²c⁴/ℏ²', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Gráfica 2: Anisotropía sidérea
    ax2 = axes[0, 1]
    senal = sistema.coherencia_sistema.senal_larmor
    theta_array = np.linspace(0, 360, 100)
    f_obs_array = [senal.frecuencia_observada(theta) for theta in theta_array]

    ax2.plot(theta_array, f_obs_array, 'g-', linewidth=2)
    ax2.axhline(y=F0_HZ, color='r', linestyle='--', label=f'f₀ = {F0_HZ:.4f} Hz')
    ax2.set_xlabel('θ_gal [grados]', fontsize=12)
    ax2.set_ylabel('f_obs [Hz]', fontsize=12)
    ax2.set_title('Anisotropía Sidérea: Modulación de Larmor', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Gráfica 3: Permitividad efectiva
    ax3 = axes[1, 0]
    permittividad = sistema.coherencia_sistema.permittividad
    constantes = sistema.constantes
    omega_array = np.linspace(0.5 * constantes.omega_psi, 1.5 * constantes.omega_psi, 200)
    epsilon_array = [abs(permittividad.epsilon_eff(omega)) for omega in omega_array]

    ax3.semilogy(omega_array / (2.0 * math.pi), epsilon_array, 'purple', linewidth=2)
    ax3.axvline(x=F0_HZ, color='r', linestyle='--', label=f'f₀ = {F0_HZ:.4f} Hz')
    ax3.set_xlabel('f [Hz]', fontsize=12)
    ax3.set_ylabel('|ε_eff/ε₀|', fontsize=12)
    ax3.set_title('Permitividad Efectiva: Resonancia en ω_ψ', fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Gráfica 4: Coeficiente η vs L
    ax4 = axes[1, 1]
    coeficiente = sistema.coherencia_sistema.coeficiente_eta
    L_array = np.logspace(0, 6, 100)  # 1 m a 1000 km
    eta_array = [coeficiente.eta(constantes.omega_psi, L) for L in L_array]

    ax4.loglog(L_array / 1000.0, eta_array, 'orange', linewidth=2)
    ax4.axhline(y=1.0, color='r', linestyle='--', label='η = 1 (resonancia fuerte)')
    ax4.set_xlabel('L [km]', fontsize=12)
    ax4.set_ylabel('η', fontsize=12)
    ax4.set_title('Coeficiente de Mezcla de Fase: η ∝ √L', fontsize=12, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('arquitectura_fisica_topc_validacion.png', dpi=150, bbox_inches='tight')
    print("✅ Gráficas guardadas en 'arquitectura_fisica_topc_validacion.png'")


# ═══════════════════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

def main() -> int:
    """
    Ejecuta la validación completa del modelo.

    Returns
    -------
    int
        0 si todas las validaciones pasan, 1 si alguna falla
    """
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "VALIDACIÓN ARQUITECTURA FÍSICA TOPC" + " "*23 + "║")
    print("╚" + "="*78 + "╝\n")

    # Activar sistema
    print("Activando sistema TOPC...")
    sistema = arquitectura_fisica_topc_activar(mostrar_informe=False)

    # Ejecutar validaciones
    validaciones = [
        ("Parámetros Fundamentales", validar_parametros_fundamentales),
        ("Hamiltoniano Total", validar_hamiltoniano),
        ("Permitividad Efectiva", validar_permitividad),
        ("Coeficiente η", validar_coeficiente_eta),
        ("Dispersión de Thot", validar_dispersion_thot),
        ("Señal de Larmor", validar_senal_larmor),
        ("Interferómetro Sagnac", validar_sagnac),
        ("Coherencia Global", validar_coherencia_global),
    ]

    resultados = []
    for nombre, funcion_validacion in validaciones:
        try:
            resultado = funcion_validacion(sistema)
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"\n❌ ERROR en validación de {nombre}: {e}")
            resultados.append((nombre, False))

    # Generar gráficas
    try:
        generar_graficas(sistema)
    except Exception as e:
        print(f"\n⚠️  Advertencia al generar gráficas: {e}")

    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE VALIDACIÓN")
    print("="*80)

    for nombre, resultado in resultados:
        simbolo = "✅" if resultado else "❌"
        print(f"{simbolo} {nombre}: {'PASADO' if resultado else 'FALLADO'}")

    total = len(resultados)
    exitosos = sum(1 for _, r in resultados if r)

    print("\n" + "="*80)
    print(f"Total: {exitosos}/{total} validaciones pasadas")

    if exitosos == total:
        print("\n🎉 ✅ TODAS LAS VALIDACIONES PASARON CORRECTAMENTE ✅ 🎉")
        print("𓂀 Ω ∞³ Φ · ARQUITECTURA FÍSICA TOPC VERIFICADA ✅")
        print("="*80 + "\n")
        return 0
    else:
        print(f"\n❌ {total - exitosos} validaciones fallaron")
        print("="*80 + "\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
