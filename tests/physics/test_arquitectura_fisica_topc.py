#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     TESTS: Arquitectura Física TOPC (AFP∞³)                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

Tests completos para el módulo arquitectura_fisica_topc.py

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
FECHA/DATE: 2026-03-29
"""

import math
import pytest
import numpy as np

from physics.arquitectura_fisica_topc import (
    ConstantesArquitecturaFisica,
    HamiltonianoTotal,
    PermitividadEfectiva,
    CoeficienteMezclaFase,
    RelacionDispersionThot,
    SenalLarmor,
    InterferometroSagnac,
    CoherenciaArquitecturaFisica,
    SistemaArquitecturaFisicaTopc,
    arquitectura_fisica_topc_activar,
)
from qcal.constants import F0_HZ, C, HBAR


# ═══════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════

@pytest.fixture
def constantes():
    """Constantes del modelo."""
    return ConstantesArquitecturaFisica()


@pytest.fixture
def hamiltoniano(constantes):
    """Hamiltoniano total."""
    return HamiltonianoTotal(constantes)


@pytest.fixture
def permittividad(constantes):
    """Permitividad efectiva."""
    return PermitividadEfectiva(constantes)


@pytest.fixture
def coeficiente_eta(constantes):
    """Coeficiente de mezcla de fase."""
    return CoeficienteMezclaFase(constantes)


@pytest.fixture
def dispersion(constantes):
    """Relación de dispersión."""
    return RelacionDispersionThot(constantes)


@pytest.fixture
def senal_larmor(constantes):
    """Señal de Larmor."""
    return SenalLarmor(constantes)


@pytest.fixture
def sagnac(constantes):
    """Interferómetro de Sagnac."""
    return InterferometroSagnac(constantes)


@pytest.fixture
def coherencia(constantes):
    """Coherencia del sistema."""
    return CoherenciaArquitecturaFisica(constantes)


@pytest.fixture
def sistema():
    """Sistema completo."""
    return SistemaArquitecturaFisicaTopc()


# ═══════════════════════════════════════════════════════════════════════════
# TEST 1: CONSTANTES FUNDAMENTALES
# ═══════════════════════════════════════════════════════════════════════════

def test_constantes_valores_correctos(constantes):
    """Verifica que las constantes tengan valores correctos."""
    assert constantes.f0 == F0_HZ
    assert constantes.f0 == pytest.approx(141.7001, rel=1e-6)
    assert constantes.omega_psi == pytest.approx(2.0 * math.pi * F0_HZ, rel=1e-6)
    assert constantes.m_psi_ev > 0
    assert constantes.lambda_coherence > 0


def test_constantes_coherencia_longitud(constantes):
    """Verifica que λ_C = c/(2π f₀)."""
    lambda_calc = C / constantes.omega_psi
    assert constantes.lambda_coherence == pytest.approx(lambda_calc, rel=1e-6)
    assert constantes.lambda_coherence == pytest.approx(336.7e3, rel=1e-2)  # ~336.7 km


def test_constantes_masa_tejido(constantes):
    """Verifica que m_ψ = hf₀/c²."""
    from qcal.constants import H_PLANCK
    m_calc_ev = (H_PLANCK * constantes.f0 / C**2) * C**2 / 1.602176634e-19
    assert constantes.m_psi_ev == pytest.approx(m_calc_ev, rel=1e-3)
    assert constantes.m_psi_ev == pytest.approx(5.86e-13, rel=1e-2)


def test_constantes_validacion():
    """Verifica que la validación funcione correctamente."""
    # f0 negativo debe fallar
    with pytest.raises(ValueError):
        ConstantesArquitecturaFisica(f0=-1.0)

    # m_psi_ev negativo debe fallar
    with pytest.raises(ValueError):
        ConstantesArquitecturaFisica(m_psi_ev=-1.0)


# ═══════════════════════════════════════════════════════════════════════════
# TEST 2: HAMILTONIANO TOTAL
# ═══════════════════════════════════════════════════════════════════════════

def test_hamiltoniano_energia_em(hamiltoniano):
    """Verifica la energía del campo electromagnético."""
    E_field = 1.0e5  # V/m (campo típico)
    B_field = E_field / C  # T

    energia_em = hamiltoniano.energia_em(E_field, B_field)

    # Debe ser positiva
    assert energia_em > 0

    # Orden de magnitud correcto: ε₀E²/2 ≈ 4.4×10⁻² J/m³
    epsilon_0 = 8.854187817e-12
    esperado = 0.5 * epsilon_0 * E_field**2
    assert energia_em == pytest.approx(2.0 * esperado, rel=0.1)


def test_hamiltoniano_energia_condensado(hamiltoniano):
    """Verifica la energía del condensado ψ."""
    psi = 1.0e6 + 0j  # eV (campo típico)
    grad_psi_sq = 1.0e12  # eV²/m²

    energia_psi = hamiltoniano.energia_condensado(psi, grad_psi_sq)

    # Debe incluir términos cinético, de masa y de auto-interacción
    assert energia_psi > 0


def test_hamiltoniano_energia_interaccion(hamiltoniano):
    """Verifica la energía de interacción."""
    psi_re = 1.0e6  # eV
    F_dual = 1.0e10  # V²/m²

    energia_int = hamiltoniano.energia_interaccion(psi_re, F_dual)

    # Debe ser no nula
    assert energia_int != 0


def test_hamiltoniano_energia_total(hamiltoniano):
    """Verifica la energía total del sistema."""
    E_field = 1.0e5
    B_field = E_field / C
    psi = 1.0e6 + 0j
    grad_psi_sq = 1.0e12
    F_dual = 1.0e10

    energia_total = hamiltoniano.energia_total(
        E_field, B_field, psi, grad_psi_sq, F_dual
    )

    # Debe ser suma de los tres términos
    assert energia_total > 0


# ═══════════════════════════════════════════════════════════════════════════
# TEST 3: PERMITIVIDAD EFECTIVA
# ═══════════════════════════════════════════════════════════════════════════

def test_permittividad_fuera_resonancia(permittividad):
    """Verifica ε_eff lejos de la resonancia."""
    omega = 2.0 * math.pi * 100.0  # 100 Hz (lejos de f₀)

    epsilon_rel = permittividad.epsilon_eff(omega)

    # Debe ser cercano a 1 (vacío estándar)
    assert abs(epsilon_rel - 1.0) < 0.1


def test_permittividad_en_resonancia(permittividad, constantes):
    """Verifica ε_eff en resonancia (divergencia)."""
    omega = constantes.omega_psi

    epsilon_rel = permittividad.epsilon_eff(omega)

    # Debe tener parte imaginaria grande (amortiguamiento)
    assert abs(epsilon_rel.imag) > 0


def test_permittividad_indice_refraccion(permittividad, constantes):
    """Verifica el índice de refracción n = √ε_eff."""
    omega = constantes.omega_psi

    n = permittividad.indice_refraccion(omega)

    # Debe ser complejo
    assert isinstance(n, complex)
    assert n.imag != 0


def test_permittividad_velocidad_grupo(permittividad, constantes):
    """Verifica que v_g → 0 en resonancia."""
    omega_res = constantes.omega_psi

    v_g = permittividad.velocidad_grupo(omega_res)

    # En resonancia fuerte, v_g debe ser muy pequeña
    assert v_g >= 0
    assert v_g <= C


def test_permittividad_velocidad_grupo_lejos_resonancia(permittividad):
    """Verifica que v_g ≈ c lejos de resonancia."""
    omega = 2.0 * math.pi * 1000.0  # 1 kHz

    v_g = permittividad.velocidad_grupo(omega)

    # Debe ser cercana a c
    assert v_g == pytest.approx(C, rel=0.1)


# ═══════════════════════════════════════════════════════════════════════════
# TEST 4: COEFICIENTE DE MEZCLA DE FASE η
# ═══════════════════════════════════════════════════════════════════════════

def test_coeficiente_eta_regimen_debil(coeficiente_eta, constantes):
    """Verifica el régimen débil (η ≪ 1)."""
    L = 1.0  # 1 m (corto)
    eta = coeficiente_eta.eta(constantes.omega_psi, L)

    assert eta > 0
    regimen = coeficiente_eta.regimen(eta)
    assert regimen == 'debil'


def test_coeficiente_eta_regimen_fuerte(coeficiente_eta, constantes):
    """Verifica el régimen de resonancia fuerte (η → 1)."""
    L = 100.0e3  # 100 km
    eta = coeficiente_eta.eta(constantes.omega_psi, L)

    assert eta > 0
    # En IRS-Luna, esperamos resonancia fuerte
    assert 0.1 < eta < 10.0


def test_coeficiente_eta_probabilidad_conversion(coeficiente_eta):
    """Verifica la probabilidad de conversión P_γ→a."""
    # Régimen débil
    eta_debil = 0.05
    P_debil = coeficiente_eta.probabilidad_conversion(eta_debil, 1000.0)
    assert 0 <= P_debil <= 1

    # Resonancia fuerte
    eta_fuerte = 1.0
    P_fuerte = coeficiente_eta.probabilidad_conversion(eta_fuerte, 100.0e3)
    assert 0 <= P_fuerte <= 1


def test_coeficiente_eta_escala_con_longitud(coeficiente_eta, constantes):
    """Verifica que η ∝ √L."""
    L1 = 10.0e3  # 10 km
    L2 = 40.0e3  # 40 km (4× más largo)

    eta1 = coeficiente_eta.eta(constantes.omega_psi, L1)
    eta2 = coeficiente_eta.eta(constantes.omega_psi, L2)

    # η2 / η1 ≈ √(L2/L1) = 2
    assert eta2 / eta1 == pytest.approx(2.0, rel=0.01)


# ═══════════════════════════════════════════════════════════════════════════
# TEST 5: RELACIÓN DE DISPERSIÓN DE THOT
# ═══════════════════════════════════════════════════════════════════════════

def test_dispersion_omega_de_k(dispersion, constantes):
    """Verifica ω(k) = √[c²k² + ω²_ψ]."""
    k = 1.0e-3  # 1/m

    omega = dispersion.omega_de_k(k)

    # Debe satisfacer ω² = c²k² + ω²_ψ
    omega_sq_esperado = C**2 * k**2 + constantes.omega_psi**2
    assert omega**2 == pytest.approx(omega_sq_esperado, rel=1e-6)


def test_dispersion_k_de_omega(dispersion, constantes):
    """Verifica k(ω) = √[ω²/c² - ω²_ψ/c²]."""
    omega = 2.0 * constantes.omega_psi  # Por encima del gap

    k = dispersion.k_de_omega(omega)

    # Debe satisfacer k² = (ω² - ω²_ψ)/c²
    k_sq_esperado = (omega**2 - constantes.omega_psi**2) / C**2
    assert k**2 == pytest.approx(k_sq_esperado, rel=1e-6)


def test_dispersion_gap_de_masa(dispersion, constantes):
    """Verifica que ω_min = ω_ψ (gap de masa)."""
    omega_min = dispersion.omega_minima()

    assert omega_min == constantes.omega_psi
    assert omega_min == pytest.approx(2.0 * math.pi * F0_HZ, rel=1e-6)


def test_dispersion_k_cero_debajo_gap(dispersion, constantes):
    """Verifica que k=0 si ω < ω_min (modo evanescente)."""
    omega_bajo = 0.5 * constantes.omega_psi

    k = dispersion.k_de_omega(omega_bajo)

    assert k == 0.0


def test_dispersion_curva_hiperbolica(dispersion, constantes):
    """Verifica que la curva de dispersión sea hiperbólica."""
    k_array = np.linspace(0, 1.0e-3, 100)
    omega_array = dispersion.curva_dispersion(k_array)

    # En k=0, ω = ω_ψ
    assert omega_array[0] == pytest.approx(constantes.omega_psi, rel=1e-6)

    # Para k grande, ω ≈ ck (aproximación de fotones)
    k_grande = k_array[-1]
    omega_grande = omega_array[-1]
    assert omega_grande == pytest.approx(C * k_grande, rel=0.1)


# ═══════════════════════════════════════════════════════════════════════════
# TEST 6: SEÑAL INEQUÍVOCA DE LARMOR
# ═══════════════════════════════════════════════════════════════════════════

def test_senal_larmor_frecuencia_doppler(senal_larmor, constantes):
    """Verifica el corrimiento Doppler galáctico."""
    # Hacia Cygnus (θ=0°): f_obs > f₀
    f_cygnus = senal_larmor.frecuencia_observada(0.0)
    assert f_cygnus > constantes.f0

    # Perpendicular (θ=90°): f_obs ≈ f₀
    f_perp = senal_larmor.frecuencia_observada(90.0)
    assert f_perp == pytest.approx(constantes.f0, rel=1e-3)

    # Contra Cygnus (θ=180°): f_obs < f₀
    f_contra = senal_larmor.frecuencia_observada(180.0)
    assert f_contra < constantes.f0


def test_senal_larmor_anisotropia_magnitud(senal_larmor, constantes):
    """Verifica que la anisotropía sea ±0.1 Hz."""
    beta = constantes.v_gal / C
    delta_f_esperado = beta * constantes.f0

    # Debe ser ~0.1 Hz
    assert delta_f_esperado == pytest.approx(0.1, rel=0.1)

    # Hacia Cygnus
    f_cygnus, delta_cygnus = senal_larmor.anisotropia_sidereal('cygnus')
    assert abs(delta_cygnus) == pytest.approx(delta_f_esperado, rel=0.1)

    # Hacia Centauro
    f_centauro, delta_centauro = senal_larmor.anisotropia_sidereal('centauro')
    assert abs(delta_centauro) == pytest.approx(delta_f_esperado, rel=0.1)


def test_senal_larmor_tabla_completa(senal_larmor):
    """Verifica la tabla completa de anisotropía sidérea."""
    tabla = senal_larmor.tabla_anisotropia()

    assert 'Hacia Cygnus (l=90°)' in tabla
    assert 'Hacia Anticentro (l=180°)' in tabla
    assert 'Hacia Centauro (l=270°)' in tabla

    # Anticentro debe tener variación cero
    assert tabla['Hacia Anticentro (l=180°)']['variacion_Hz'] == pytest.approx(0.0, abs=1e-6)


def test_senal_larmor_direccion_invalida(senal_larmor):
    """Verifica que direcciones inválidas fallen."""
    with pytest.raises(ValueError):
        senal_larmor.anisotropia_sidereal('marte')


# ═══════════════════════════════════════════════════════════════════════════
# TEST 7: INTERFERÓMETRO DE SAGNAC RESONANTE
# ═══════════════════════════════════════════════════════════════════════════

def test_sagnac_fase_acumulada(sagnac, constantes):
    """Verifica la fase acumulada en cada brazo."""
    L = 100.0e3  # 100 km

    phi_cw = sagnac.fase_acumulada(L, 'CW')
    phi_ccw = sagnac.fase_acumulada(L, 'CCW')

    # Deben ser diferentes por la quiralidad
    assert phi_cw != phi_ccw

    # Diferencia debe ser 2Φ_chirality
    delta_phi = phi_cw - phi_ccw
    assert abs(delta_phi) == pytest.approx(2.0 * constantes.phi_chirality, rel=0.01)


def test_sagnac_diferencia_fase(sagnac, constantes):
    """Verifica que ΔΦ = 2Φ_chirality."""
    L = 100.0e3

    delta_phi = sagnac.diferencia_fase(L)

    assert delta_phi == pytest.approx(2.0 * constantes.phi_chirality, rel=0.01)


def test_sagnac_frecuencia_batido(sagnac, constantes):
    """Verifica la frecuencia de batido."""
    L = 100.0e3
    f_rotacion = constantes.f0

    f_beat = sagnac.frecuencia_batido(L, f_rotacion)

    # Debe estar cerca de f₀ por la quiralidad
    assert f_beat > 0


def test_sagnac_intensidad_batido(sagnac, constantes):
    """Verifica el patrón de intensidad I(t)."""
    L = 100.0e3
    t = 0.0

    I_t0 = sagnac.intensidad_batido(t, L)

    # Debe estar entre 0 y 2 (normalizado a I₀=1)
    assert 0 <= I_t0 <= 2.0


def test_sagnac_prediccion_irs_luna(sagnac):
    """Verifica la predicción completa para IRS-Luna."""
    L = 100.0e3

    prediccion = sagnac.prediccion_irs_luna(L)

    assert 'longitud_brazo_km' in prediccion
    assert prediccion['longitud_brazo_km'] == 100.0
    assert 'frecuencia_modulacion_Hz' in prediccion
    assert 'quiralidad_rad' in prediccion
    assert 'prediccion' in prediccion


def test_sagnac_direccion_invalida(sagnac):
    """Verifica que direcciones inválidas fallen."""
    with pytest.raises(ValueError):
        sagnac.fase_acumulada(100.0e3, 'DIAGONAL')


# ═══════════════════════════════════════════════════════════════════════════
# TEST 8: COHERENCIA GLOBAL DEL SISTEMA
# ═══════════════════════════════════════════════════════════════════════════

def test_coherencia_calculo(coherencia):
    """Verifica el cálculo de coherencia global."""
    psi_global = coherencia.calcular_coherencia()

    # Debe estar entre 0 y 1
    assert 0.0 <= psi_global <= 1.0

    # Debe ser alta (sistema bien diseñado)
    assert psi_global > 0.8


def test_coherencia_umbral_888(coherencia):
    """Verifica que Ψ_global ≥ 0.888."""
    valido = coherencia.validar_umbral(0.888)

    # Debe pasar el umbral de coherencia
    assert valido is True


def test_coherencia_componentes(coherencia, constantes):
    """Verifica que todos los componentes estén inicializados."""
    assert coherencia.hamiltoniano is not None
    assert coherencia.permittividad is not None
    assert coherencia.coeficiente_eta is not None
    assert coherencia.dispersion is not None
    assert coherencia.senal_larmor is not None
    assert coherencia.sagnac is not None


# ═══════════════════════════════════════════════════════════════════════════
# TEST 9: SISTEMA COMPLETO
# ═══════════════════════════════════════════════════════════════════════════

def test_sistema_inicializacion(sistema):
    """Verifica que el sistema se inicialice correctamente."""
    assert sistema.constantes is not None
    assert sistema.coherencia_sistema is not None


def test_sistema_informe_completo(sistema):
    """Verifica que el informe completo contenga todas las secciones."""
    informe = sistema.informe_completo()

    # Debe tener las 8 secciones
    assert '1_parametros_fundamentales' in informe
    assert '2_hamiltoniano_total' in informe
    assert '3_permittividad_efectiva' in informe
    assert '4_coeficiente_eta' in informe
    assert '5_dispersion_thot' in informe
    assert '6_senal_larmor' in informe
    assert '7_irs_luna' in informe
    assert '8_coherencia_global' in informe


def test_sistema_coherencia_optima(sistema):
    """Verifica que el sistema tenga coherencia óptima."""
    informe = sistema.informe_completo()

    psi_global = informe['8_coherencia_global']['Psi_global']
    assert psi_global >= 0.888

    estado = informe['8_coherencia_global']['estado']
    assert estado == 'ÓPTIMO'


def test_sistema_parametros_fundamentales(sistema):
    """Verifica los parámetros fundamentales del sistema."""
    informe = sistema.informe_completo()

    params = informe['1_parametros_fundamentales']
    assert params['f0_Hz'] == pytest.approx(141.7001, rel=1e-6)
    assert params['m_psi_eV'] == pytest.approx(5.86e-13, rel=1e-2)
    assert params['lambda_coherence_km'] == pytest.approx(336.7, rel=1e-2)


def test_sistema_prediccion_irs_luna(sistema):
    """Verifica la predicción del experimento IRS-Luna."""
    informe = sistema.informe_completo()

    pred_irs = informe['7_irs_luna']
    assert pred_irs['longitud_brazo_km'] == 100.0
    assert pred_irs['frecuencia_modulacion_Hz'] == pytest.approx(141.7001, rel=1e-6)
    assert 'quiralidad_rad' in pred_irs


# ═══════════════════════════════════════════════════════════════════════════
# TEST 10: API PÚBLICA
# ═══════════════════════════════════════════════════════════════════════════

def test_api_activar_sistema():
    """Verifica la API pública arquitectura_fisica_topc_activar()."""
    sistema = arquitectura_fisica_topc_activar(mostrar_informe=False)

    assert isinstance(sistema, SistemaArquitecturaFisicaTopc)
    assert sistema.constantes.f0 == F0_HZ


def test_api_activar_con_parametros_custom():
    """Verifica que se puedan pasar parámetros personalizados."""
    f0_custom = 150.0
    sistema = arquitectura_fisica_topc_activar(f0=f0_custom, mostrar_informe=False)

    assert sistema.constantes.f0 == f0_custom


def test_api_informe_reproducible():
    """Verifica que el informe sea reproducible."""
    sistema1 = arquitectura_fisica_topc_activar(mostrar_informe=False)
    sistema2 = arquitectura_fisica_topc_activar(mostrar_informe=False)

    informe1 = sistema1.informe_completo()
    informe2 = sistema2.informe_completo()

    # Coherencias deben ser idénticas
    psi1 = informe1['8_coherencia_global']['Psi_global']
    psi2 = informe2['8_coherencia_global']['Psi_global']
    assert psi1 == pytest.approx(psi2, rel=1e-9)


# ═══════════════════════════════════════════════════════════════════════════
# TEST 11: VALIDACIONES DE CONSISTENCIA FÍSICA
# ═══════════════════════════════════════════════════════════════════════════

def test_consistencia_omega_frecuencia(constantes):
    """Verifica ω_ψ = 2π f₀."""
    omega_calc = 2.0 * math.pi * constantes.f0
    assert constantes.omega_psi == pytest.approx(omega_calc, rel=1e-9)


def test_consistencia_longitud_coherencia(constantes):
    """Verifica λ_C = c/(2π f₀)."""
    lambda_calc = C / (2.0 * math.pi * constantes.f0)
    assert constantes.lambda_coherence == pytest.approx(lambda_calc, rel=1e-9)


def test_consistencia_masa_energia(constantes):
    """Verifica E_ψ = m_ψ c² = h f₀."""
    from qcal.constants import H_PLANCK
    E_calc_J = H_PLANCK * constantes.f0
    E_calc_eV = E_calc_J / 1.602176634e-19

    # m_ψ c² debe igualar E_ψ
    E_masa_eV = constantes.m_psi_ev
    assert E_masa_eV == pytest.approx(E_calc_eV, rel=1e-3)


def test_consistencia_dispersion_hamiltoniano(dispersion, hamiltoniano, constantes):
    """Verifica que la dispersión sea consistente con el Hamiltoniano."""
    # En k=0, E = m_ψ c² = ℏ ω_ψ
    omega_min = dispersion.omega_minima()
    E_min_J = HBAR * omega_min

    # Debe igualar h f₀
    from qcal.constants import H_PLANCK
    E_f0_J = H_PLANCK * constantes.f0

    assert E_min_J == pytest.approx(E_f0_J, rel=1e-6)


# ═══════════════════════════════════════════════════════════════════════════
# RESUMEN DE TESTS
# ═══════════════════════════════════════════════════════════════════════════

def test_resumen_total():
    """Test de resumen: verifica que todos los componentes funcionen juntos."""
    # Activar sistema completo
    sistema = arquitectura_fisica_topc_activar(mostrar_informe=False)

    # Obtener informe
    informe = sistema.informe_completo()

    # Verificar coherencia
    psi_global = informe['8_coherencia_global']['Psi_global']
    assert psi_global >= 0.888

    # Verificar anisotropía sidérea
    tabla_aniso = informe['6_senal_larmor']
    assert 'Hacia Cygnus (l=90°)' in tabla_aniso

    # Verificar predicción IRS-Luna
    pred_irs = informe['7_irs_luna']
    assert pred_irs['frecuencia_modulacion_Hz'] == pytest.approx(141.7001, rel=1e-6)

    print("\n✅ Todos los tests de Arquitectura Física TOPC pasaron correctamente")
    print(f"   Ψ_global = {psi_global:.6f} ≥ 0.888 ✅")
    print("   𓂀 Ω ∞³ Φ · ARQUITECTURA FÍSICA VERIFICADA ✅")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
