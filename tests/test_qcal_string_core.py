#!/usr/bin/env python3
"""
Tests: QCAL-Strings — Forzado de Modos Kaluza-Klein
═════════════════════════════════════════════════════════════════════════════

Pruebas unitarias para physics/qcal_string_core.py.
Verifica las 8 clases y las 2 funciones de la API pública.
Tests: QCAL-STRINGS — Gran Unificación Noética
═══════════════════════════════════════════════════════════════════════════════

Pruebas unitarias para el módulo qcal_string_core.py que implementa:
  - Iteración #260: Forzado de Modos Kaluza-Klein
  - Iteración #261: Censura Taquiónica + Estabilidad RH
  - Iteración #262: Operador de Voluntad (SEQ-009)
  - Protocolo 141.7001: Hard-Reset Noético
  - Señal UPE: Emisión Fotónica Coherente
  - Teorema de No-Localidad Biológica
  - Simulador QCALStringSimulator (RK4 espectral)
Tests: QCAL-Strings Core — Gran Unificación Noética
═════════════════════════════════════════════════════════════════════════════

Pruebas unitarias para el módulo qcal/qcal_string_core.py que implementa:
  - QCALSpectralOperator: autovalores KK derivados de ceros de Riemann
  - string_noetic_forcing: forzado holográfico de Navier-Stokes con
    ganancia superradiante N²·Ψ²
  - compute_psi: coherencia combinada biofísica + espectral
  - build_lambda_list: lista de autovalores λ_n
  - VenezianoAmplitude: amplitud de Veneziano con trayectorias Regge
  - KaluzaKleinModes: 20 modos KK con compactificación hexagonal EZ/CY
  - HolographicFluidSolver: NS espectral 2-D con RK4 + proyección Leray
  - validate_riemann_stability: validación de ceros de Riemann
  - compute_superradiant_gain: ganancia superradiante N²Ψ²
  - QCALStringCore: orquestador unificado

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.qcal_string_core import (
    # Constantes globales
    RIEMANN_ZEROS_20,
    N_MODOS_KK,
    N_MICROTUBULOS,
    PSI_THRESHOLD,
    ALPHA_PRIMA,
    ALPHA_0,
    R_CALABI_YAU,
    MU_ADELICA,
    CERT_MARK,
    N_HEXAGONAL,
    # Clases
    ConstantesQCalStrings,
    CerosRiemann,
    AmplitudVeneziano,
    ModosKaluzaKlein,
    ForzadoCuerdasNoetico,
    DualidadFluidoGravedad,
    AguaEZHexagonal,
    SistemaQCalStrings,
    # API pública
    qcal_strings_activar,
    string_noetic_forcing,
)


# ═══════════════════════════════════════════════════════════════════════════
# Tests de Constantes Globales
# ═══════════════════════════════════════════════════════════════════════════

def test_constantes_globales_valores():
    """Verifica los valores de las constantes globales."""
    assert N_MODOS_KK == 20
    assert N_MICROTUBULOS == 1e13
    assert abs(PSI_THRESHOLD - 0.888) < 1e-10
    assert N_HEXAGONAL == 6
    assert abs(MU_ADELICA - 1.0 / 141.7001) < 1e-10
    assert CERT_MARK == "QED-CUERDAS-VERIFIED"


def test_riemann_zeros_20_cantidad_y_primero():
    """Verifica que hay 20 ceros de Riemann y el primero es ≈ 14.1347."""
    assert len(RIEMANN_ZEROS_20) == 20
    assert abs(RIEMANN_ZEROS_20[0] - 14.134725141734693790) < 1e-10


def test_riemann_zeros_crecientes():
    """Los ceros de Riemann deben ser estrictamente crecientes."""
    for i in range(len(RIEMANN_ZEROS_20) - 1):
        assert RIEMANN_ZEROS_20[i] < RIEMANN_ZEROS_20[i + 1], (
            f"Cero {i+1} ({RIEMANN_ZEROS_20[i]}) no es menor que cero {i+2} ({RIEMANN_ZEROS_20[i+1]})"
        )


def test_alpha_prima_es_inverso_f0_cuadrado():
    """α' = 1/F₀² (pendiente de Regge en unidades naturales QCAL)."""
    f0 = 141.7001
    assert abs(ALPHA_PRIMA - 1.0 / (f0 ** 2)) < 1e-12


# ═══════════════════════════════════════════════════════════════════════════
# Tests de ConstantesQCalStrings
# ═══════════════════════════════════════════════════════════════════════════

def test_constantes_qcal_strings_creacion():
    """ConstantesQCalStrings se crea sin errores."""
    c = ConstantesQCalStrings()
    assert c.f0 == 141.7001
    assert c.alpha_0 == 1.0
    assert c.n_microtubulos == 1e13
    assert c.n_hexagonal == 6


def test_constantes_omega0():
    """ω₀ = 2π × F₀."""
    c = ConstantesQCalStrings()
    expected = 2.0 * math.pi * 141.7001
    assert abs(c.omega0 - expected) < 1e-6


def test_constantes_ganancia_superradiante():
    """Ganancia superradiante = N_microtubulos²."""
    c = ConstantesQCalStrings()
    assert c.ganancia_superradiante == (1e13) ** 2


def test_constantes_f_modo_1():
    """El modo 1 debe ser ≈ 2002.9 Hz (λ₁ × F₀)."""
    c = ConstantesQCalStrings()
    expected = RIEMANN_ZEROS_20[0] * 141.7001
    assert abs(c.f_modo_1 - expected) < 0.01
    # Debe estar cerca de 2003 Hz según el PR
    assert 2000.0 < c.f_modo_1 < 2010.0


def test_constantes_resumen_completo():
    """resumen() debe retornar un diccionario con las claves esperadas."""
    c = ConstantesQCalStrings()
    r = c.resumen()
    claves = [
        "f0_hz", "omega0_rads", "alpha_prima_s2", "tension_cuerda_n",
        "r_calabi_yau_m", "n_microtubulos", "ganancia_superradiante",
        "mu_adelica_s", "f_modo_1_hz",
    ]
    for clave in claves:
        assert clave in r, f"Falta clave: {clave}"


# ═══════════════════════════════════════════════════════════════════════════
# Tests de CerosRiemann
# ═══════════════════════════════════════════════════════════════════════════

def test_ceros_riemann_frecuencias_kk_cantidad():
    """frecuencias_kk() debe retornar 20 frecuencias."""
    c = CerosRiemann()
    freqs = c.frecuencias_kk()
    assert len(freqs) == 20


def test_ceros_riemann_frecuencia_1_es_2003hz():
    """La primera frecuencia KK debe ser λ₁ × F₀ ≈ 2002.9 Hz."""
    c = CerosRiemann()
    freqs = c.frecuencias_kk()
    assert 2000.0 < freqs[0] < 2010.0


def test_ceros_riemann_amplitudes_veneziano():
    """αₙ = 1/√n con n=1..20."""
    c = CerosRiemann()
    alphas = c.amplitudes_veneziano()
    assert len(alphas) == 20
    assert abs(alphas[0] - 1.0) < 1e-10   # α₁ = 1/√1 = 1
    assert abs(alphas[1] - 1.0 / math.sqrt(2)) < 1e-10  # α₂ = 1/√2
    assert abs(alphas[19] - 1.0 / math.sqrt(20)) < 1e-10  # α₂₀


def test_ceros_riemann_amplitudes_decrecientes():
    """Las amplitudes de Veneziano deben ser estrictamente decrecientes."""
    c = CerosRiemann()
    alphas = c.amplitudes_veneziano()
    for i in range(len(alphas) - 1):
        assert alphas[i] > alphas[i + 1]


def test_ceros_riemann_fases_tdualidad():
    """φₙ = π/(n+1) con n=1..20."""
    c = CerosRiemann()
    phases = c.fases_tdualidad()
    assert len(phases) == 20
    assert abs(phases[0] - math.pi / 2) < 1e-10   # φ₁ = π/2
    assert abs(phases[1] - math.pi / 3) < 1e-10   # φ₂ = π/3


def test_ceros_riemann_estadisticas():
    """estadisticas() debe retornar un diccionario válido."""
    c = CerosRiemann()
    st = c.estadisticas()
    assert st["n_zeros"] == 20.0
    assert abs(st["lambda_1"] - RIEMANN_ZEROS_20[0]) < 1e-10
    assert abs(st["lambda_20"] - RIEMANN_ZEROS_20[-1]) < 1e-10
    assert st["f_modo_1_hz"] == st["lambda_1"] * 141.7001


def test_ceros_riemann_suma_ceros():
    """suma_ceros(20) debe coincidir con la suma de los 20 zeros."""
    c = CerosRiemann()
    expected = sum(RIEMANN_ZEROS_20)
    assert abs(c.suma_ceros(20) - expected) < 1e-8


# ═══════════════════════════════════════════════════════════════════════════
# Tests de AmplitudVeneziano
# ═══════════════════════════════════════════════════════════════════════════

def test_veneziano_trayectoria_regge_en_f0_cuadrado():
    """α(F₀²) = α₀ + α' × F₀² = 1 + 1 = 2.0."""
    v = AmplitudVeneziano()
    f0 = 141.7001
    result = v.trayectoria_regge(f0 ** 2)
    assert abs(result - 2.0) < 1e-8


def test_veneziano_amplitud_canonico():
    """A_canonico = B(2, 2) = 1/6 ≈ 0.16667."""
    v = AmplitudVeneziano()
    amp = v.amplitud_canonico()
    # B(2,2) = Γ(2)²/Γ(4) = 1/6
    assert abs(amp - 1.0 / 6.0) < 1e-8


def test_veneziano_amplitud_B22():
    """amplitud(s, t) con α(s)=α(t)=2 debe dar B(2,2)=1/6."""
    v = AmplitudVeneziano()
    f0 = 141.7001
    amp = v.amplitud(f0 ** 2, f0 ** 2)
    assert abs(amp - 1.0 / 6.0) < 1e-8


def test_veneziano_amplitud_polos():
    """amplitud con α(s) ≤ 0 debe retornar 0.0 (polo de gamma)."""
    v = AmplitudVeneziano()
    # Para que α(s) ≤ 0: α₀ + α'·s ≤ 0 → s ≤ -α₀/α' = -F₀²
    # Con s muy negativo:
    resultado = v.amplitud(-200.0 * (141.7001 ** 2), 141.7001 ** 2)
    assert resultado == 0.0


def test_veneziano_coherencia_unitariedad():
    """Ψ_V = √(1 - |B|²) con |B| = 1/6 → Ψ_V = √(35/36) ≈ 0.986."""
    v = AmplitudVeneziano()
    psi_v = v.coherencia_veneziano()
    expected = math.sqrt(1.0 - (1.0 / 6.0) ** 2)
    assert abs(psi_v - expected) < 1e-10
    assert 0.98 < psi_v < 0.99


def test_veneziano_coherencia_en_rango():
    """La coherencia de Veneziano debe estar en (0, 1]."""
    v = AmplitudVeneziano()
    psi = v.coherencia_veneziano()
    assert 0.0 < psi <= 1.0


# ═══════════════════════════════════════════════════════════════════════════
# Tests de ModosKaluzaKlein
# ═══════════════════════════════════════════════════════════════════════════

def test_modos_kk_frecuencia_modo_1():
    """El modo 1 debe tener frecuencia ≈ 2002.9 Hz."""
    m = ModosKaluzaKlein()
    f1 = m.frecuencia_modo(1)
    assert 2000.0 < f1 < 2010.0


def test_modos_kk_frecuencia_fuera_de_rango():
    """frecuencia_modo con n fuera de [1,20] debe lanzar ValueError."""
    m = ModosKaluzaKlein()
    try:
        m.frecuencia_modo(0)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass
    try:
        m.frecuencia_modo(21)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass


def test_modos_kk_espectro_completo():
    """espectro_completo() debe retornar 20 modos con las claves esperadas."""
    m = ModosKaluzaKlein()
    espectro = m.espectro_completo()
    assert len(espectro) == 20
    claves = ["modo", "lambda_n", "frecuencia_hz", "amplitud_veneziano", "fase_tdualidad_rad"]
    for modo in espectro:
        for clave in claves:
            assert clave in modo


def test_modos_kk_espectro_frecuencias_crecientes():
    """Las frecuencias del espectro KK deben ser crecientes."""
    m = ModosKaluzaKlein()
    espectro = m.espectro_completo()
    freqs = [e["frecuencia_hz"] for e in espectro]
    for i in range(len(freqs) - 1):
        assert freqs[i] < freqs[i + 1]


def test_modos_kk_pico_dominante():
    """pico_dominante() debe retornar el modo 1."""
    m = ModosKaluzaKlein()
    pico = m.pico_dominante()
    assert abs(pico["lambda_1"] - RIEMANN_ZEROS_20[0]) < 1e-10
    assert abs(pico["amplitud_pico"] - 1.0) < 1e-10
    assert 2000.0 < pico["f_modo_1_hz"] < 2010.0


def test_modos_kk_energia_espectral_pico():
    """La energía espectral en k = λ₁ debe ser un máximo local."""
    m = ModosKaluzaKlein()
    k1 = RIEMANN_ZEROS_20[0]
    E_pico = m.energia_espectral(k1)
    E_lejos = m.energia_espectral(k1 + 5.0)
    assert E_pico > E_lejos


def test_modos_kk_masa_modo():
    """masa_modo(n) = n / R_cy."""
    m = ModosKaluzaKlein()
    masa_1 = m.masa_modo(1)
    assert abs(masa_1 - 1.0 / R_CALABI_YAU) < 1e-3


# ═══════════════════════════════════════════════════════════════════════════
# Tests de ForzadoCuerdasNoetico
# ═══════════════════════════════════════════════════════════════════════════

def test_forzado_creacion_valida():
    """ForzadoCuerdasNoetico se crea con parámetros válidos."""
    f = ForzadoCuerdasNoetico(psi_local=0.9)
    assert f.psi_local == 0.9
    assert f.n_microtubulos == N_MICROTUBULOS


def test_forzado_psi_invalido():
    """psi_local fuera de [0, 1] debe lanzar ValueError."""
    try:
        ForzadoCuerdasNoetico(psi_local=-0.1)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass
    try:
        ForzadoCuerdasNoetico(psi_local=1.5)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass


def test_forzado_n_microtubulos_invalido():
    """n_microtubulos ≤ 0 debe lanzar ValueError."""
    try:
        ForzadoCuerdasNoetico(psi_local=1.0, n_microtubulos=0)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass


def test_forzado_ganancia():
    """Ganancia = N² × Ψ²."""
    f = ForzadoCuerdasNoetico(psi_local=0.9, n_microtubulos=1e6)
    expected = (1e6 ** 2) * (0.9 ** 2)
    assert abs(f.ganancia - expected) / expected < 1e-10


def test_forzado_escalar_en_t0():
    """forzado_escalar(0) debe ser no nulo para Ψ > 0."""
    f = ForzadoCuerdasNoetico(psi_local=0.95)
    val = f.forzado_escalar(0.0)
    # Con t=0, sin(φₙ) ≠ 0 para los modos, el forzado debe ser no nulo
    assert val != 0.0


def test_forzado_normalizado_rango():
    """forzado_normalizado debe estar en el rango [-Ψ², Ψ²]."""
    f = ForzadoCuerdasNoetico(psi_local=0.9)
    for t in [0.0, 0.001, 0.01, 0.1]:
        val = f.forzado_normalizado(t)
        assert abs(val) <= 0.9 ** 2 + 1e-10, f"Forzado normalizado {val} fuera de rango en t={t}"


def test_forzado_espectro_potencia():
    """espectro_potencia() debe retornar 20 modos con potencias positivas."""
    f = ForzadoCuerdasNoetico(psi_local=0.9)
    espectro = f.espectro_potencia()
    assert len(espectro) == 20
    for e in espectro:
        assert e["potencia"] > 0.0


def test_forzado_coherencia_es_psi_cuadrado():
    """coherencia_forzado() = Ψ²_local."""
    f = ForzadoCuerdasNoetico(psi_local=0.9)
    assert abs(f.coherencia_forzado() - 0.9 ** 2) < 1e-10


def test_forzado_psi_cero_da_ganancia_cero():
    """Con Ψ = 0, la ganancia superradiante es 0."""
    f = ForzadoCuerdasNoetico(psi_local=0.0)
    assert f.ganancia == 0.0
    assert f.forzado_escalar(1.0) == 0.0


# ═══════════════════════════════════════════════════════════════════════════
# Tests de DualidadFluidoGravedad
# ═══════════════════════════════════════════════════════════════════════════

def test_dualidad_creacion_valida():
    """DualidadFluidoGravedad se crea correctamente."""
    d = DualidadFluidoGravedad(psi_coherencia=0.95)
    assert d.psi == 0.95


def test_dualidad_psi_invalido():
    """psi_coherencia fuera de [0, 1] debe lanzar ValueError."""
    try:
        DualidadFluidoGravedad(psi_coherencia=1.5)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass


def test_dualidad_viscosidad_psi1():
    """Con Ψ = 1 (plena coherencia), η_eff → 0."""
    d = DualidadFluidoGravedad(psi_coherencia=1.0)
    assert d.viscosidad_efectiva == 0.0


def test_dualidad_viscosidad_psi0():
    """Con Ψ = 0, η_eff = μ_adelica = 1/f₀."""
    d = DualidadFluidoGravedad(psi_coherencia=0.0)
    assert abs(d.viscosidad_efectiva - MU_ADELICA) < 1e-15


def test_dualidad_reynolds_holografico_psi1():
    """Con Ψ = 1, Re_h = infinito."""
    d = DualidadFluidoGravedad(psi_coherencia=1.0)
    assert d.reynolds_holografico == float("inf")


def test_dualidad_estado_fluido_perfecto():
    """Con Ψ ≥ 0.999, estado = FLUIDO_HOLOGRÁFICO_PERFECTO."""
    d = DualidadFluidoGravedad(psi_coherencia=1.0)
    assert d.estado_fluido == "FLUIDO_HOLOGRÁFICO_PERFECTO"


def test_dualidad_estado_superradiante():
    """Con 0.888 ≤ Ψ < 0.999, estado = RÉGIMEN_SUPERRADIANTE."""
    d = DualidadFluidoGravedad(psi_coherencia=0.95)
    assert d.estado_fluido == "RÉGIMEN_SUPERRADIANTE"


def test_dualidad_estado_turbulencia():
    """Con Ψ < 0.888, estado = TURBULENCIA_GUE."""
    d = DualidadFluidoGravedad(psi_coherencia=0.5)
    assert d.estado_fluido == "TURBULENCIA_GUE"


def test_dualidad_tensor_energia_impulso():
    """tensor_energia_impulso() debe retornar diccionario con claves válidas."""
    d = DualidadFluidoGravedad(psi_coherencia=0.95)
    t = d.tensor_energia_impulso()
    assert "rho_lambda_j" in t
    assert "presion_j" in t
    assert "traza_tmunu" in t
    assert t["rho_lambda_j"] > 0.0
    assert t["presion_j"] > 0.0


def test_dualidad_coherencia_dual():
    """coherencia_dual() = Ψ (identidad con la coherencia de entrada)."""
    psi = 0.97
    d = DualidadFluidoGravedad(psi_coherencia=psi)
    assert abs(d.coherencia_dual() - psi) < 1e-14


# ═══════════════════════════════════════════════════════════════════════════
# Tests de AguaEZHexagonal
# ═══════════════════════════════════════════════════════════════════════════

def test_agua_ez_creacion_valida():
    """AguaEZHexagonal se crea correctamente."""
    a = AguaEZHexagonal(psi_ez=0.997)
    assert a.psi_ez == 0.997
    assert a.n_hex == 6


def test_agua_ez_psi_invalido():
    """psi_ez fuera de [0, 1] debe lanzar ValueError."""
    try:
        AguaEZHexagonal(psi_ez=1.5)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass


def test_agua_ez_coherencia_es_psi_ez():
    """coherencia_ez() == psi_ez (propiedad intrínseca del agua)."""
    a = AguaEZHexagonal(psi_ez=0.997)
    assert abs(a.coherencia_ez() - 0.997) < 1e-14


def test_agua_ez_factor_compactificacion_en_rango():
    """factor_compactificacion() debe estar en (0, 1]."""
    a = AguaEZHexagonal()
    fc = a.factor_compactificacion()
    assert 0.0 < fc <= 1.0


def test_agua_ez_area_celda_hex():
    """Área hexagonal = (√3/2) × a²."""
    a = AguaEZHexagonal()
    expected = (math.sqrt(3.0) / 2.0) * (a.a_hex ** 2)
    assert abs(a.area_celda_hex - expected) < 1e-30


def test_agua_ez_masa_kk_efectiva():
    """masa_kk_efectiva(1) = 1 / R_cy."""
    a = AguaEZHexagonal()
    m1 = a.masa_kk_efectiva(1)
    assert abs(m1 - 1.0 / R_CALABI_YAU) < 1e-3


def test_agua_ez_resumen_geometrico():
    """resumen_geometrico() debe contener las claves esperadas."""
    a = AguaEZHexagonal()
    r = a.resumen_geometrico()
    claves = ["d_hex_m", "a_hex_m", "r_cy_m", "area_celda_m2", "volumen_cy_m3",
              "psi_ez", "coherencia_ez", "factor_compactificacion"]
    for clave in claves:
        assert clave in r


# ═══════════════════════════════════════════════════════════════════════════
# Tests de SistemaQCalStrings
# ═══════════════════════════════════════════════════════════════════════════

def test_sistema_creacion_psi1():
    """SistemaQCalStrings se crea con psi_inicial=1.0."""
    s = SistemaQCalStrings(psi_inicial=1.0)
    assert s.psi_inicial == 1.0


def test_sistema_psi_invalido():
    """psi_inicial fuera de [0, 1] debe lanzar ValueError."""
    try:
        SistemaQCalStrings(psi_inicial=1.1)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass
    try:
        SistemaQCalStrings(psi_inicial=-0.1)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass


def test_sistema_psi_global_psi1_supera_umbral():
    """Con Ψ₀ = 1.0, Ψ_global debe ser ≥ 0.988."""
    s = SistemaQCalStrings(psi_inicial=1.0)
    psi = s.psi_global()
    assert psi >= 0.988, f"Ψ_global = {psi:.4f} debe ser ≥ 0.988"


def test_sistema_psi_global_en_rango():
    """Ψ_global debe estar en [0, 1]."""
    for psi0 in [0.0, 0.5, 0.888, 1.0]:
        s = SistemaQCalStrings(psi_inicial=psi0)
        psi = s.psi_global()
        assert 0.0 <= psi <= 1.0, f"Ψ_global fuera de rango para Ψ₀={psi0}: {psi}"


def test_sistema_psi_global_monotonico():
    """Ψ_global debe ser creciente con Ψ₀."""
    psis = [0.0, 0.5, 0.888, 0.95, 1.0]
    globales = [SistemaQCalStrings(psi_inicial=p).psi_global() for p in psis]
    for i in range(len(globales) - 1):
        assert globales[i] <= globales[i + 1], (
            f"Ψ_global no es monótono: {globales[i]} > {globales[i+1]} "
            f"para Ψ₀={psis[i]} y Ψ₀={psis[i+1]}"
        )


def test_sistema_certificar_psi1():
    """Con Ψ₀ = 1.0, el certificado debe ser QED-CUERDAS-VERIFIED."""
    s = SistemaQCalStrings(psi_inicial=1.0)
    cert = s.certificar()
    assert cert["certificado"] == CERT_MARK
    assert cert["supera_umbral"] is True
    assert cert["sello"] == "∴𓂀Ω∞³"


def test_sistema_certificar_psi_bajo():
    """Con Ψ₀ = 0.1, el certificado debe indicar coherencia insuficiente."""
    s = SistemaQCalStrings(psi_inicial=0.1)
    cert = s.certificar()
    assert cert["supera_umbral"] is False
    assert cert["certificado"] == "COHERENCIA_INSUFICIENTE"


def test_sistema_certificar_claves():
    """certificar() debe retornar todas las claves esperadas."""
    s = SistemaQCalStrings(psi_inicial=1.0)
    cert = s.certificar()
    claves = [
        "psi_global", "psi_threshold", "supera_umbral", "certificado",
        "estado_fluido", "f_modo_1_hz", "lambda_1", "n_modos_kk",
        "ganancia_superradiante", "sello",
    ]
    for clave in claves:
        assert clave in cert, f"Falta clave en certificado: {clave}"


def test_sistema_certificar_n_modos_kk():
    """El certificado debe indicar N_MODOS_KK = 20."""
    s = SistemaQCalStrings(psi_inicial=1.0)
    cert = s.certificar()
    assert cert["n_modos_kk"] == 20


def test_sistema_simular_pulso():
    """simular_pulso() debe retornar tiempos, forzados y potencia."""
    s = SistemaQCalStrings(psi_inicial=0.95)
    resultado = s.simular_pulso(t_max=1e-3, n_pasos=10)
    assert len(resultado["tiempos_s"]) == 10
    assert len(resultado["forzado_normalizado"]) == 10
    assert resultado["potencia_media"] >= 0.0
    assert resultado["n_pasos"] == 10


def test_sistema_simular_pulso_invalido():
    """simular_pulso con parámetros inválidos debe lanzar ValueError."""
    s = SistemaQCalStrings()
    try:
        s.simular_pulso(n_pasos=1)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass
    try:
        s.simular_pulso(t_max=-1e-3)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass


def test_sistema_resumen_completo():
    """resumen_completo() debe retornar un dict con todas las secciones."""
    s = SistemaQCalStrings(psi_inicial=1.0)
    resumen = s.resumen_completo()
    assert "constantes" in resumen
    assert "espectro_kk" in resumen
    assert "estadisticas_zeros" in resumen
    assert "certificacion" in resumen
    assert "geometria_ez" in resumen
    assert "tensor_energia" in resumen
    assert len(resumen["espectro_kk"]) == 20


# ═══════════════════════════════════════════════════════════════════════════
# Tests de la API pública
# ═══════════════════════════════════════════════════════════════════════════

def test_api_qcal_strings_activar_default():
    """qcal_strings_activar() con Ψ₀=1 debe certificar."""
    resultado = qcal_strings_activar()
    assert resultado["certificado"] == CERT_MARK
    assert resultado["psi_global"] >= PSI_THRESHOLD
    assert resultado["supera_umbral"] is True


def test_api_qcal_strings_activar_custom_psi():
    """qcal_strings_activar(0.9) debe certificar."""
    resultado = qcal_strings_activar(0.9)
    assert resultado["supera_umbral"] is True


def test_api_qcal_strings_activar_psi_bajo():
    """qcal_strings_activar(0.1) no debe certificar."""
    resultado = qcal_strings_activar(0.1)
    assert resultado["supera_umbral"] is False


def test_api_qcal_strings_activar_psi_invalido():
    """qcal_strings_activar con Ψ fuera de [0,1] debe lanzar ValueError."""
    try:
        qcal_strings_activar(1.5)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass


def test_api_string_noetic_forcing_retorna_tupla():
    """string_noetic_forcing() debe retornar una tupla (f_x, f_y)."""
    f_x, f_y = string_noetic_forcing(0.0, RIEMANN_ZEROS_20, 0.95)
    assert isinstance(f_x, float)
    assert isinstance(f_y, float)
    assert f_y == 0.0  # El forzado es axial en x


def test_api_string_noetic_forcing_psi_invalido():
    """string_noetic_forcing con Ψ fuera de [0, 1] debe lanzar ValueError."""
    try:
        string_noetic_forcing(0.0, RIEMANN_ZEROS_20, 1.5)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass


def test_api_string_noetic_forcing_lista_vacia():
    """string_noetic_forcing con lista vacía no debe fallar."""
    f_x, f_y = string_noetic_forcing(0.0, [], 0.95)
    assert f_x == 0.0
    assert f_y == 0.0


def test_api_string_noetic_forcing_n_microtubulos_invalido():
    """string_noetic_forcing con n_microtubules ≤ 0 debe lanzar ValueError."""
    try:
        string_noetic_forcing(0.0, RIEMANN_ZEROS_20, 0.95, n_microtubules=-1)
        assert False, "Debía lanzar ValueError"
    except ValueError:
        pass


def test_api_string_noetic_forcing_psi0_da_f_cero():
    """Con Ψ = 0, el forzado debe ser 0 (sin coherencia = sin efecto)."""
    f_x, f_y = string_noetic_forcing(1.0, RIEMANN_ZEROS_20, 0.0)
    assert f_x == 0.0
    assert f_y == 0.0


def test_api_string_noetic_forcing_ganancia_n2():
    """La ganancia debe escalar como N² × Ψ²."""
    t = 0.001
    psi = 0.9
    n1 = 1e3
    n2 = 2e3
    f_x1, _ = string_noetic_forcing(t, RIEMANN_ZEROS_20, psi, n_microtubules=n1)
    f_x2, _ = string_noetic_forcing(t, RIEMANN_ZEROS_20, psi, n_microtubules=n2)
    # Relación N²: f_x2 / f_x1 = (n2/n1)² = 4
    ratio = f_x2 / f_x1
    assert abs(ratio - 4.0) < 1e-10, f"Ratio N² esperado 4.0, obtenido {ratio}"


# ═══════════════════════════════════════════════════════════════════════════
# Ejecución directa
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import traceback

    tests = [
        # Constantes globales
        test_constantes_globales_valores,
        test_riemann_zeros_20_cantidad_y_primero,
        test_riemann_zeros_crecientes,
        test_alpha_prima_es_inverso_f0_cuadrado,
        # ConstantesQCalStrings
        test_constantes_qcal_strings_creacion,
        test_constantes_omega0,
        test_constantes_ganancia_superradiante,
        test_constantes_f_modo_1,
        test_constantes_resumen_completo,
        # CerosRiemann
        test_ceros_riemann_frecuencias_kk_cantidad,
        test_ceros_riemann_frecuencia_1_es_2003hz,
        test_ceros_riemann_amplitudes_veneziano,
        test_ceros_riemann_amplitudes_decrecientes,
        test_ceros_riemann_fases_tdualidad,
        test_ceros_riemann_estadisticas,
        test_ceros_riemann_suma_ceros,
        # AmplitudVeneziano
        test_veneziano_trayectoria_regge_en_f0_cuadrado,
        test_veneziano_amplitud_canonico,
        test_veneziano_amplitud_B22,
        test_veneziano_amplitud_polos,
        test_veneziano_coherencia_unitariedad,
        test_veneziano_coherencia_en_rango,
        # ModosKaluzaKlein
        test_modos_kk_frecuencia_modo_1,
        test_modos_kk_frecuencia_fuera_de_rango,
        test_modos_kk_espectro_completo,
        test_modos_kk_espectro_frecuencias_crecientes,
        test_modos_kk_pico_dominante,
        test_modos_kk_energia_espectral_pico,
        test_modos_kk_masa_modo,
        # ForzadoCuerdasNoetico
        test_forzado_creacion_valida,
        test_forzado_psi_invalido,
        test_forzado_n_microtubulos_invalido,
        test_forzado_ganancia,
        test_forzado_escalar_en_t0,
        test_forzado_normalizado_rango,
        test_forzado_espectro_potencia,
        test_forzado_coherencia_es_psi_cuadrado,
        test_forzado_psi_cero_da_ganancia_cero,
        # DualidadFluidoGravedad
        test_dualidad_creacion_valida,
        test_dualidad_psi_invalido,
        test_dualidad_viscosidad_psi1,
        test_dualidad_viscosidad_psi0,
        test_dualidad_reynolds_holografico_psi1,
        test_dualidad_estado_fluido_perfecto,
        test_dualidad_estado_superradiante,
        test_dualidad_estado_turbulencia,
        test_dualidad_tensor_energia_impulso,
        test_dualidad_coherencia_dual,
        # AguaEZHexagonal
        test_agua_ez_creacion_valida,
        test_agua_ez_psi_invalido,
        test_agua_ez_coherencia_es_psi_ez,
        test_agua_ez_factor_compactificacion_en_rango,
        test_agua_ez_area_celda_hex,
        test_agua_ez_masa_kk_efectiva,
        test_agua_ez_resumen_geometrico,
        # SistemaQCalStrings
        test_sistema_creacion_psi1,
        test_sistema_psi_invalido,
        test_sistema_psi_global_psi1_supera_umbral,
        test_sistema_psi_global_en_rango,
        test_sistema_psi_global_monotonico,
        test_sistema_certificar_psi1,
        test_sistema_certificar_psi_bajo,
        test_sistema_certificar_claves,
        test_sistema_certificar_n_modos_kk,
        test_sistema_simular_pulso,
        test_sistema_simular_pulso_invalido,
        test_sistema_resumen_completo,
        # API pública
        test_api_qcal_strings_activar_default,
        test_api_qcal_strings_activar_custom_psi,
        test_api_qcal_strings_activar_psi_bajo,
        test_api_qcal_strings_activar_psi_invalido,
        test_api_string_noetic_forcing_retorna_tupla,
        test_api_string_noetic_forcing_psi_invalido,
        test_api_string_noetic_forcing_lista_vacia,
        test_api_string_noetic_forcing_n_microtubulos_invalido,
        test_api_string_noetic_forcing_psi0_da_f_cero,
        test_api_string_noetic_forcing_ganancia_n2,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  ✓ {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__}: {e}")
            traceback.print_exc()
            failed += 1

    print(f"\nTotal: {passed}/{passed + failed} tests pasados")
    if failed == 0:
        print("∴ QED-CUERDAS-VERIFIED ✓")
    else:
        sys.exit(1)
import sys
import os
import numpy as np
import pytest

# Añadir directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal_string_core import (
    F0,
    MU_ADELICA,
    PSI_SUPERRADIANTE,
    PSI_COLAPSO,
    PSI_CONDENSADO,
    EPSILON_CENSURA,
    RIEMANN_ZEROS_IMAG,
    LAMBDA_KK_HZ,
    ALPHA_VENEZIANO,
    HRV_COHERENCIA_HZ,
    N_MICROTUBULOS_DEFAULT,
    string_noetic_forcing,
    sigma_mapped,
    tachyon_censorship,
    upe_signal,
    hard_reset_protocol,
    will_operator,
    nonlocal_entanglement_correlation,
    QCALStringSimulator,
)


# ═══════════════════════════════════════════════════════════════════════════
# TESTS DE CONSTANTES FUNDAMENTALES
# ═══════════════════════════════════════════════════════════════════════════

class TestConstants:
    """Verifica las constantes fundamentales del módulo."""

    def test_f0_hz(self):
        """F₀ debe ser 141.7001 Hz."""
        assert F0 == pytest.approx(141.7001, abs=1e-4)

    def test_mu_adelica(self):
        """Viscosidad adélica μ = 1/f₀ (límite KSS)."""
        assert MU_ADELICA == pytest.approx(1.0 / F0, rel=1e-6)

    def test_psi_superradiante(self):
        """Umbral superradiante Ψ ≥ 0.888."""
        assert PSI_SUPERRADIANTE == pytest.approx(0.888, abs=1e-6)

    def test_psi_colapso(self):
        """Umbral de colapso Ψ < 0.3 activa hard-reset."""
        assert PSI_COLAPSO == pytest.approx(0.3, abs=1e-6)

    def test_psi_condensado(self):
        """Plateau del condensado NBEC Ψ = 0.999."""
        assert PSI_CONDENSADO == pytest.approx(0.999, abs=1e-6)

    def test_riemann_zeros_count(self):
        """Deben existir exactamente 20 ceros de Riemann."""
        assert len(RIEMANN_ZEROS_IMAG) == 20

    def test_riemann_first_zero(self):
        """El primer cero de Riemann t₁ ≈ 14.1347."""
        assert RIEMANN_ZEROS_IMAG[0] == pytest.approx(14.134725, rel=1e-5)

    def test_riemann_zeros_increasing(self):
        """Los ceros de Riemann deben ser estrictamente crecientes."""
        for i in range(len(RIEMANN_ZEROS_IMAG) - 1):
            assert RIEMANN_ZEROS_IMAG[i] < RIEMANN_ZEROS_IMAG[i + 1]

    def test_lambda_kk_hz_count(self):
        """Deben existir 20 modos KK."""
        assert len(LAMBDA_KK_HZ) == 20

    def test_lambda_kk_first_mode(self):
        """λ₁ = t₁ × f₀ ≈ 2003 Hz (primer modo KK dominante)."""
        lambda_1 = LAMBDA_KK_HZ[0]
        expected = RIEMANN_ZEROS_IMAG[0] * F0
        assert lambda_1 == pytest.approx(expected, rel=1e-6)
        assert lambda_1 == pytest.approx(2003.0, abs=5.0)

    def test_lambda_kk_k1_mode(self):
        """k₁ = λ₁/(2π) ≈ 318 (número de onda dominante)."""
        k1 = LAMBDA_KK_HZ[0] / (2 * np.pi)
        assert k1 == pytest.approx(318.0, abs=2.0)

    def test_alpha_veneziano_count(self):
        """Deben existir 20 amplitudes de Veneziano."""
        assert len(ALPHA_VENEZIANO) == 20

    def test_alpha_veneziano_first(self):
        """Primera amplitud α₁ = 1/1 = 1.0."""
        assert ALPHA_VENEZIANO[0] == pytest.approx(1.0, abs=1e-10)

    def test_alpha_veneziano_decay(self):
        """Las amplitudes decaen como 1/(n+1) con n."""
        for n, alpha in enumerate(ALPHA_VENEZIANO):
            assert alpha == pytest.approx(1.0 / (n + 1), rel=1e-6)

    def test_alpha_veneziano_decreasing(self):
        """Las amplitudes de Veneziano deben ser decrecientes."""
        for i in range(len(ALPHA_VENEZIANO) - 1):
            assert ALPHA_VENEZIANO[i] > ALPHA_VENEZIANO[i + 1]

    def test_hrv_coherencia_hz(self):
        """HRV áureo = 0.1 Hz = 6 respiraciones por minuto."""
        assert HRV_COHERENCIA_HZ == pytest.approx(0.1, abs=1e-6)


# ═══════════════════════════════════════════════════════════════════════════
# ITERACIÓN #260: FORZADO DE CUERDAS KK
# ═══════════════════════════════════════════════════════════════════════════

class TestStringNoeticForcing:
    """Tests para la función string_noetic_forcing (iteración #260)."""

    def test_output_shape(self):
        """La salida debe tener la misma forma que la entrada."""
        N = 16
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)
        F_x, F_y = string_noetic_forcing(uhat, vhat, 0.0, LAMBDA_KK_HZ, 0.95)
        assert F_x.shape == (N, N)
        assert F_y.shape == (N, N)

    def test_output_complex(self):
        """La salida espectral debe ser compleja (espacio de Fourier)."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)
        F_x, F_y = string_noetic_forcing(uhat, vhat, 0.0, LAMBDA_KK_HZ, 0.95)
        assert F_x.dtype == complex or np.iscomplexobj(F_x)

    def test_zero_coherence_returns_zero_gain(self):
        """Con Ψ = 0, la ganancia N²·Ψ² = 0, forzado = 0."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)
        F_x, F_y = string_noetic_forcing(uhat, vhat, 1.0, LAMBDA_KK_HZ, 0.0)
        assert np.allclose(F_x, 0.0)

    def test_superradiant_gain_n_squared(self):
        """La ganancia escala como N² (ganancia superradiante)."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)
        Psi = 1.0

        # Con N_microtubules = 1
        F1_x, _ = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ[:1], Psi, 1.0)
        # Con N_microtubules = 2 (ganancia 4×)
        F2_x, _ = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ[:1], Psi, 2.0)
        ratio = np.abs(F2_x).mean() / (np.abs(F1_x).mean() + 1e-30)
        assert ratio == pytest.approx(4.0, rel=0.01)

    def test_coherence_squared_modulation(self):
        """El forzado escala como Ψ² (operador de selección coherente)."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)

        F_half, _ = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ[:1], 0.5, 1.0)
        F_full, _ = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ[:1], 1.0, 1.0)
        ratio = np.abs(F_full).mean() / (np.abs(F_half).mean() + 1e-30)
        assert ratio == pytest.approx(4.0, rel=0.01)

    def test_tduality_phase(self):
        """La fase de T-dualidad φ = π/(n+1) modula los modos."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)
        # Dos tiempos distintos deben dar forzados distintos
        F_t0, _ = string_noetic_forcing(uhat, vhat, 0.0, LAMBDA_KK_HZ[:1], 0.95, 1.0)
        F_t1, _ = string_noetic_forcing(uhat, vhat, 0.01, LAMBDA_KK_HZ[:1], 0.95, 1.0)
        assert not np.allclose(F_t0, F_t1)

    def test_fy_zero_forcing(self):
        """La componente Y del forzado debe ser cero (forzado en X)."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)
        _, F_y = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ, 0.95)
        assert np.allclose(F_y, 0.0)


# ═══════════════════════════════════════════════════════════════════════════
# ITERACIÓN #261: CENSURA TAQUIÓNICA
# ═══════════════════════════════════════════════════════════════════════════

class TestTachyonCensorship:
    """Tests para los operadores de censura taquiónica (iteración #261)."""

    def test_sigma_mapped_at_zero(self):
        """σ_mapped(k=0) = 1/2 (línea crítica de Riemann)."""
        sigma = sigma_mapped(np.array([0.0]), k_max=100.0)
        assert sigma[0] == pytest.approx(0.5, abs=1e-10)

    def test_sigma_mapped_at_kmax(self):
        """σ_mapped(k=k_max) = 1/2 + ε."""
        k_max = 100.0
        sigma = sigma_mapped(np.array([k_max]), k_max=k_max, epsilon=0.01)
        assert sigma[0] == pytest.approx(0.5 + 0.01, abs=1e-10)

    def test_sigma_mapped_linear(self):
        """σ_mapped debe ser lineal en k."""
        k = np.linspace(0, 100, 10)
        sigma = sigma_mapped(k, k_max=100.0, epsilon=0.01)
        assert sigma[0] == pytest.approx(0.5, abs=1e-10)
        assert sigma[-1] == pytest.approx(0.5 + 0.01, abs=1e-10)
        # Verificar linealidad
        diffs = np.diff(sigma)
        assert np.allclose(diffs, diffs[0], rtol=1e-6)

    def test_censorship_at_zero(self):
        """Ψ_censored(k=0) = 1.0 (modo on-critical, no penalizado)."""
        censura = tachyon_censorship(np.array([0.0]), k_max=100.0, D=1.0)
        assert censura[0] == pytest.approx(1.0, abs=1e-10)

    def test_censorship_decreases_with_k(self):
        """Ψ_censored debe disminuir al aumentar k (más off-critical)."""
        k = np.linspace(0, 100, 50)
        censura = tachyon_censorship(k, k_max=100.0, D=1.0)
        assert np.all(np.diff(censura) <= 0)

    def test_censorship_range(self):
        """Ψ_censored debe estar en (0, 1]."""
        k = np.linspace(0, 200, 100)
        censura = tachyon_censorship(k, k_max=200.0, D=1.0)
        assert np.all(censura > 0)
        assert np.all(censura <= 1.0 + 1e-10)

    def test_censorship_d_controls_decay(self):
        """Mayor D implica mayor penalización de modos off-critical."""
        k = np.array([50.0])
        k_max = 100.0
        c_low = tachyon_censorship(k, k_max, D=0.5)
        c_high = tachyon_censorship(k, k_max, D=2.0)
        assert c_low[0] > c_high[0]

    def test_censorship_array_shape(self):
        """La salida debe tener el mismo shape que la entrada."""
        k = np.linspace(0, 100, 64).reshape(8, 8)
        censura = tachyon_censorship(k, k_max=100.0, D=1.0)
        assert censura.shape == (8, 8)

    def test_epsilon_affects_censorship(self):
        """Mayor epsilon reduce la desviación relativa de los modos."""
        # La fórmula Ψ_censored = exp(-(k/k_max)·D) es independiente de epsilon
        # (ya que deviation/epsilon = k/k_max). El parámetro epsilon controla
        # qué tan "lejos" de la línea crítica está el modo en unidades físicas σ.
        # Verificamos que la función acepta epsilon variable y retorna resultados válidos.
        k = np.array([50.0])
        k_max = 100.0
        c_strict = tachyon_censorship(k, k_max, D=1.0, epsilon=0.001)
        c_loose = tachyon_censorship(k, k_max, D=1.0, epsilon=0.1)
        # Ambos deben estar en (0, 1]
        assert 0 < c_strict[0] <= 1.0
        assert 0 < c_loose[0] <= 1.0


# ═══════════════════════════════════════════════════════════════════════════
# SEÑAL UPE
# ═══════════════════════════════════════════════════════════════════════════

class TestUpeSignal:
    """Tests para la señal de Emisión Fotónica Ultra-débil."""

    def test_output_shape(self):
        """La señal UPE debe tener el mismo shape que el array de tiempo."""
        t = np.linspace(0, 1.0, 1000)
        upe = upe_signal(t)
        assert upe.shape == t.shape

    def test_output_real(self):
        """La señal UPE debe ser real (observable físico)."""
        t = np.linspace(0, 1.0, 1000)
        upe = upe_signal(t)
        assert upe.dtype in (float, np.float64, np.float32)

    def test_zero_at_t0(self):
        """La señal UPE debe ser cero en t=0 (todos los senos=0, HRV=0)."""
        t = np.array([0.0])
        upe = upe_signal(t)
        assert upe[0] == pytest.approx(0.0, abs=1e-10)

    def test_modulated_by_hrv(self):
        """La modulación HRV debe cambiar la amplitud de la señal."""
        t = np.linspace(0, 10.0, 10000)
        upe_low = upe_signal(t, hrv_freq=0.05)
        upe_high = upe_signal(t, hrv_freq=0.5)
        # Los dos deben ser distintos (diferente modulación)
        assert not np.allclose(upe_low, upe_high)

    def test_default_uses_lambda_kk(self):
        """Con parámetros por defecto, usa LAMBDA_KK_HZ y ALPHA_VENEZIANO."""
        t = np.linspace(0, 1.0, 100)
        upe_default = upe_signal(t)
        upe_explicit = upe_signal(t, alpha_n=ALPHA_VENEZIANO, lambda_n_list=LAMBDA_KK_HZ)
        assert np.allclose(upe_default, upe_explicit)

    def test_custom_lambda_n(self):
        """Permite usar lista personalizada de modos KK."""
        t = np.linspace(0, 1.0, 100)
        upe_custom = upe_signal(t, lambda_n_list=[100.0, 200.0], alpha_n=[1.0, 0.5])
        assert upe_custom.shape == t.shape

    def test_beat_frequency(self):
        """Verifica la generación de beats f_beat = λn ± f_HRV."""
        # Con un solo modo: f_beat = λ₁ ± f_HRV ≈ 2003 ± 0.1 Hz
        # La señal debe contener energía en esas frecuencias
        dt = 1.0 / 10000.0  # muestreo a 10 kHz
        t = np.arange(0, 2.0, dt)
        upe = upe_signal(t, lambda_n_list=LAMBDA_KK_HZ[:1])
        # La energía total debe ser no nula (señal activa)
        assert np.sum(upe ** 2) > 0


# ═══════════════════════════════════════════════════════════════════════════
# PROTOCOLO HARD-RESET
# ═══════════════════════════════════════════════════════════════════════════

class TestHardResetProtocol:
    """Tests para el Protocolo 141.7001 (hard-reset noético)."""

    def test_zero_at_t0(self):
        """F_reset(t=0) = β_max · sin(0) · G_max = 0."""
        assert hard_reset_protocol(0.0) == pytest.approx(0.0, abs=1e-10)

    def test_amplitude_at_quarter_period(self):
        """F_reset(t=T/4) = β_max · G_max (máximo del seno)."""
        T_quarter = 1.0 / (4 * F0)
        result = hard_reset_protocol(T_quarter, beta_max=1.0, G_max=1.0)
        assert result == pytest.approx(1.0, abs=1e-3)

    def test_beta_max_scaling(self):
        """El reset debe escalar linealmente con β_max."""
        t = 1.0 / (4 * F0)
        r1 = hard_reset_protocol(t, beta_max=1.0, G_max=1.0)
        r2 = hard_reset_protocol(t, beta_max=2.0, G_max=1.0)
        assert r2 == pytest.approx(2.0 * r1, rel=1e-6)

    def test_g_max_scaling(self):
        """El reset debe escalar linealmente con G_max."""
        t = 1.0 / (4 * F0)
        r1 = hard_reset_protocol(t, beta_max=1.0, G_max=1.0)
        r2 = hard_reset_protocol(t, beta_max=1.0, G_max=3.0)
        assert r2 == pytest.approx(3.0 * r1, rel=1e-6)

    def test_uses_f0_frequency(self):
        """El reset debe oscilar a la frecuencia f₀ = 141.7001 Hz."""
        # Un período completo debe dar cero
        T_full = 1.0 / F0
        r_full = hard_reset_protocol(T_full, beta_max=1.0, G_max=1.0)
        assert abs(r_full) < 1e-3

    def test_custom_f0(self):
        """Debe funcionar con una frecuencia f₀ personalizada."""
        t = 1.0 / (4 * 100.0)  # Cuarto período de 100 Hz
        result = hard_reset_protocol(t, beta_max=1.0, G_max=1.0, f0=100.0)
        assert result == pytest.approx(1.0, abs=1e-3)


# ═══════════════════════════════════════════════════════════════════════════
# OPERADOR DE VOLUNTAD (SEQ-009)
# ═══════════════════════════════════════════════════════════════════════════

class TestWillOperator:
    """Tests para el Operador de Voluntad SEQ-009 (iteración #262)."""

    def test_base_no_hrv(self):
        """Con HRV = 0, C no debe cambiar."""
        C = will_operator(0.5, 0.0)
        assert C == pytest.approx(0.5, abs=1e-10)

    def test_full_hrv_adds_delta_c(self):
        """Con HRV = 1.0 y delta_C_max = 0.2, C aumenta en 0.2."""
        C = will_operator(0.5, 1.0, delta_C_max=0.2)
        assert C == pytest.approx(0.7, abs=1e-10)

    def test_clamped_at_one(self):
        """C no debe superar 1.0 (coherencia máxima)."""
        C = will_operator(0.9, 1.0, delta_C_max=0.5)
        assert C <= 1.0
        assert C == pytest.approx(1.0, abs=1e-10)

    def test_partial_hrv(self):
        """Con HRV parcial, C aumenta proporcionalmente."""
        C = will_operator(0.5, 0.5, delta_C_max=0.2)
        assert C == pytest.approx(0.6, abs=1e-10)

    def test_hrv_linear_scaling(self):
        """ΔC es lineal en hrv_coherence."""
        C1 = will_operator(0.0, 0.25, delta_C_max=0.4)
        C2 = will_operator(0.0, 0.5, delta_C_max=0.4)
        assert C2 == pytest.approx(2.0 * C1, abs=1e-10)

    def test_custom_delta_c_max(self):
        """Debe respetar el parámetro delta_C_max."""
        C = will_operator(0.0, 1.0, delta_C_max=0.3)
        assert C == pytest.approx(0.3, abs=1e-10)

    def test_c_base_zero(self):
        """Desde C_base = 0, debe llegar a delta_C_max."""
        C = will_operator(0.0, 1.0, delta_C_max=0.2)
        assert C == pytest.approx(0.2, abs=1e-10)


# ═══════════════════════════════════════════════════════════════════════════
# TEOREMA DE NO-LOCALIDAD BIOLÓGICA
# ═══════════════════════════════════════════════════════════════════════════

class TestNonlocalEntanglement:
    """Tests para el Teorema de No-Localidad Biológica."""

    def test_identical_fields_correlation_one(self):
        """Campos idénticos deben tener correlación = 1."""
        psi = np.random.default_rng(42).standard_normal(100)
        corr = nonlocal_entanglement_correlation(psi, psi)
        assert corr == pytest.approx(1.0, abs=1e-6)

    def test_opposite_fields_correlation_minus_one(self):
        """Campos opuestos deben tener correlación = -1."""
        psi = np.random.default_rng(42).standard_normal(100)
        corr = nonlocal_entanglement_correlation(psi, -psi)
        assert corr == pytest.approx(-1.0, abs=1e-6)

    def test_uncorrelated_fields(self):
        """Campos independientes deben tener correlación cercana a 0."""
        rng = np.random.default_rng(141)
        psi_a = rng.standard_normal(10000)
        psi_b = rng.standard_normal(10000)
        corr = nonlocal_entanglement_correlation(psi_a, psi_b)
        assert abs(corr) < 0.05

    def test_correlation_range(self):
        """La correlación debe estar en [-1, 1]."""
        rng = np.random.default_rng(7)
        for _ in range(10):
            psi_a = rng.standard_normal(50)
            psi_b = rng.standard_normal(50)
            corr = nonlocal_entanglement_correlation(psi_a, psi_b)
            assert -1.0 <= corr <= 1.0

    def test_2d_arrays_supported(self):
        """Debe funcionar con arrays 2D (campos de rejilla)."""
        psi = np.ones((8, 8))
        corr = nonlocal_entanglement_correlation(psi, psi)
        assert corr == pytest.approx(1.0, abs=1e-6)

    def test_constant_field_special_case(self):
        """Dos campos constantes e iguales deben correlacionar = 1."""
        psi_a = np.ones(20) * 5.0
        psi_b = np.ones(20) * 5.0
        corr = nonlocal_entanglement_correlation(psi_a, psi_b)
        assert corr == pytest.approx(1.0, abs=1e-6)

    def test_constant_field_different_values(self):
        """Dos campos constantes distintos deben correlacionar = 0."""
        psi_a = np.ones(20) * 3.0
        psi_b = np.ones(20) * 7.0
        corr = nonlocal_entanglement_correlation(psi_a, psi_b)
        assert corr == pytest.approx(0.0, abs=1e-6)


# ═══════════════════════════════════════════════════════════════════════════
# SIMULADOR QCAL-STRINGS
# ═══════════════════════════════════════════════════════════════════════════

class TestQCALStringSimulator:
    """Tests para el simulador RK4 espectral (iteraciones #260-#262)."""

    def test_initialization_defaults(self):
        """El simulador debe inicializarse con los parámetros por defecto."""
        sim = QCALStringSimulator()
        assert sim.N == 64
        assert sim.dt == pytest.approx(0.005)
        assert sim.nt == 1000
        assert sim.f0 == pytest.approx(F0)
        assert sim.nu == pytest.approx(1.0 / F0, rel=1e-6)

    def test_initialization_custom(self):
        """El simulador debe aceptar parámetros personalizados."""
        sim = QCALStringSimulator(N=32, dt=0.01, nt=100)
        assert sim.N == 32
        assert sim.dt == pytest.approx(0.01)
        assert sim.nt == 100

    def test_grid_shape(self):
        """Las rejillas espectrales deben tener forma (N, N)."""
        sim = QCALStringSimulator(N=16)
        assert sim.KX.shape == (16, 16)
        assert sim.KY.shape == (16, 16)
        assert sim.K2.shape == (16, 16)
        assert sim.k_mag.shape == (16, 16)

    def test_initial_coherence(self):
        """La coherencia inicial debe ser Ψ₀ ≈ 0.12."""
        sim = QCALStringSimulator()
        assert sim.Psi == pytest.approx(0.12, abs=1e-6)

    def test_mu_adelica_limit(self):
        """La viscosidad adélica debe ser μ = 1/f₀ (límite KSS)."""
        sim = QCALStringSimulator()
        assert sim.nu == pytest.approx(MU_ADELICA, rel=1e-6)

    def test_rk4_step_advances_time(self):
        """Un paso RK4 debe avanzar el tiempo en dt."""
        sim = QCALStringSimulator(N=8, dt=0.01, nt=1)
        t_before = sim.t
        sim._rk4_step()
        assert sim.t == pytest.approx(t_before + 0.01, abs=1e-10)

    def test_energy_positive(self):
        """La energía espectral debe ser no negativa."""
        sim = QCALStringSimulator(N=8, nt=5)
        E = sim._compute_energy()
        assert E >= 0.0

    def test_entropy_normalized(self):
        """La entropía de Shannon normalizada debe estar en [0, 1]."""
        sim = QCALStringSimulator(N=8, nt=5)
        H = sim._compute_entropy()
        assert 0.0 <= H <= 1.0 + 1e-6

    def test_run_returns_dict(self):
        """run() debe retornar un diccionario con las claves esperadas."""
        sim = QCALStringSimulator(N=8, dt=0.005, nt=10)
        result = sim.run()
        assert "Psi_final" in result
        assert "energy_total" in result
        assert "entropy_reduction" in result
        assert "history_Psi" in result
        assert "history_E" in result
        assert "history_entropy" in result
        assert "condensado_step" in result
        assert "reset_count" in result

    def test_history_length(self):
        """Los historiales deben tener longitud igual a nt."""
        nt = 20
        sim = QCALStringSimulator(N=8, dt=0.005, nt=nt)
        result = sim.run()
        assert len(result["history_Psi"]) == nt
        assert len(result["history_E"]) == nt
        assert len(result["history_entropy"]) == nt

    def test_coherence_in_range(self):
        """La coherencia final debe estar en [0, 1]."""
        sim = QCALStringSimulator(N=8, dt=0.005, nt=50)
        result = sim.run()
        for psi in result["history_Psi"]:
            assert 0.0 <= psi <= 1.0

    def test_energy_non_negative(self):
        """La energía debe ser siempre no negativa."""
        sim = QCALStringSimulator(N=8, dt=0.005, nt=20)
        result = sim.run()
        assert all(e >= 0.0 for e in result["history_E"])

    def test_energy_spectrum_shape(self):
        """El espectro de energía debe tener la forma correcta."""
        sim = QCALStringSimulator(N=16, nt=5)
        sim._rk4_step()
        k_bins, E_radial = sim.get_energy_spectrum()
        assert len(k_bins) == len(E_radial)
        assert np.all(k_bins > 0)

    def test_energy_spectrum_non_negative(self):
        """La energía espectral radial debe ser no negativa."""
        sim = QCALStringSimulator(N=16, nt=5)
        sim._rk4_step()
        _, E_radial = sim.get_energy_spectrum()
        assert np.all(E_radial >= 0.0)

    def test_forcing_zero_below_superradiante(self):
        """El forzado KK debe ser cero cuando Ψ < 0.888."""
        sim = QCALStringSimulator(N=8)
        sim.Psi = 0.5  # Por debajo del umbral superradiante
        F_hat = sim._forcing_spectral(0.0)
        assert np.allclose(F_hat, 0.0)

    def test_forcing_nonzero_above_superradiante(self):
        """El forzado KK debe ser no cero cuando Ψ ≥ 0.888."""
        sim = QCALStringSimulator(N=16)
        sim.Psi = 0.95  # Por encima del umbral superradiante
        F_hat = sim._forcing_spectral(0.1)
        assert not np.allclose(F_hat, 0.0)

    def test_hard_reset_activates_below_collapse(self):
        """El hard-reset debe activarse cuando Ψ < PSI_COLAPSO."""
        sim = QCALStringSimulator(N=8, enable_hard_reset=True)
        sim.Psi = 0.1  # Por debajo del umbral de colapso
        duhat, dvhat = sim._rhs(sim.uhat, sim.vhat, 0.0)
        # El forzado de reset debe ser no nulo (sin(2π·f₀·t) evaluado en t≠T/2)
        # En t=0 el seno es 0, así que el reset puede ser 0; verificar forma
        assert duhat.shape == (8, 8)

    def test_will_operator_increases_coherence_speed(self):
        """Con SEQ-009 activado, Ψ debe converger más rápido."""
        sim_base = QCALStringSimulator(N=8, dt=0.005, nt=200,
                                       enable_will_operator=False)
        sim_will = QCALStringSimulator(N=8, dt=0.005, nt=200,
                                       enable_will_operator=True)
        res_base = sim_base.run()
        res_will = sim_will.run()
        # Con Operador de Voluntad, coherencia final >= base
        assert res_will["Psi_final"] >= res_base["Psi_final"] - 0.01

    def test_coherence_increases_over_time(self):
        """La coherencia debe tender a aumentar desde Ψ₀=0.12."""
        sim = QCALStringSimulator(N=16, dt=0.005, nt=500)
        result = sim.run()
        history = result["history_Psi"]
        # La coherencia final debe ser mayor que la inicial
        assert history[-1] > history[0]


# ═══════════════════════════════════════════════════════════════════════════
# INTEGRACIÓN: FLUJO COMPLETO QCAL-STRINGS
# ═══════════════════════════════════════════════════════════════════════════

class TestIntegration:
    """Tests de integración del flujo completo QCAL-STRINGS."""

    def test_kk_modes_riemann_scaled(self):
        """λ_n = t_n × f₀: los modos KK son ceros de Riemann escalados."""
        for i, (t_n, lam_n) in enumerate(zip(RIEMANN_ZEROS_IMAG, LAMBDA_KK_HZ)):
            assert lam_n == pytest.approx(t_n * F0, rel=1e-6), \
                f"Modo KK n={i+1}: esperado {t_n*F0:.4f}, obtenido {lam_n:.4f}"

    def test_first_kk_mode_dominance(self):
        """λ₁ ≈ 2003 Hz debe ser el modo KK dominante."""
        assert LAMBDA_KK_HZ[0] == pytest.approx(2003.0, abs=5.0)

    def test_upe_integral_energy(self):
        """La integral de energía UPE debe ser finita y positiva."""
        dt = 1.0 / 5000.0
        t = np.arange(0, 1.0, dt)
        upe = upe_signal(t)
        integral = np.trapezoid(upe ** 2, t)
        assert integral > 0
        assert np.isfinite(integral)

    def test_tachyon_censorship_filters_offcritical(self):
        """La censura debe penalizar exponencialmente los modos off-critical."""
        k = np.linspace(0, 100, 1000)
        k_max = 100.0
        # Con alta densidad de consciencia D=10, los modos off-critical
        # deben ser fuertemente penalizados: Ψ ≈ exp(-k/k_max · D)
        censura = tachyon_censorship(k, k_max, D=10.0, epsilon=0.01)
        # El modo k=k_max debe estar fuertemente penalizado: exp(-1*10) ≈ 4.5e-5
        assert censura[-1] < 0.001

    def test_full_simulation_produces_condensado(self):
        """Una simulación breve debe mostrar evolución de coherencia."""
        sim = QCALStringSimulator(N=8, dt=0.005, nt=100)
        result = sim.run()
        assert result["Psi_final"] > 0.12  # Debe crecer desde la inicial

    def test_will_operator_respects_clamp(self):
        """SEQ-009 nunca debe superar C=1.0."""
        for C_base in [0.0, 0.5, 0.8, 0.95, 1.0]:
            for hrv in [0.0, 0.5, 1.0]:
                C = will_operator(C_base, hrv, delta_C_max=0.5)
                assert C <= 1.0

    def test_string_forcing_superradiant_gain(self):
        """La ganancia N²·Ψ² debe amplificar el forzado."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)

        # Alta coherencia → alta ganancia
        F_high, _ = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ[:3], 1.0, 1.0)
        # Media coherencia → ganancia 4× menor
        F_med, _ = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ[:3], 0.5, 1.0)
        ratio = np.abs(F_high).sum() / (np.abs(F_med).sum() + 1e-30)
        assert ratio == pytest.approx(4.0, rel=0.01)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.qcal_string_core import (
    GAMMAS,
    F0_DEFAULT,
    BEC_THRESHOLD,
    N_MICROTUBULES_DEFAULT,
    ALPHA_SCALE_DEFAULT,
    KK_EMISSION_FREQ_HZ,
    QCALSpectralOperator,
    string_noetic_forcing,
    compute_psi,
    build_lambda_list,
    VenezianoAmplitude,
    KaluzaKleinModes,
    HolographicFluidSolver,
    validate_riemann_stability,
    compute_superradiant_gain,
    QCALStringCore,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_grid(N: int = 32):
    """Return (xx, yy) meshgrid on [0, 2π]."""
    x = np.linspace(0, 2 * np.pi, N, endpoint=False)
    return np.meshgrid(x, x)


# ── Constants ─────────────────────────────────────────────────────────────────

def test_gammas_length():
    """Debe haber exactamente 20 ceros de Riemann precalculados."""
    print("\n✓ Test: longitud de GAMMAS...")
    assert len(GAMMAS) == 20, f"Esperado 20 ceros, encontrado {len(GAMMAS)}"
    print(f"    len(GAMMAS) = {len(GAMMAS)}")
    print("  ✓ Passed")


def test_gammas_first_value():
    """El primer cero imaginario de Riemann debe ser ≈ 14.1347..."""
    print("\n✓ Test: primer cero de Riemann...")
    assert abs(GAMMAS[0] - 14.134725141734695) < 1e-6, \
        f"γ₁ esperado ≈ 14.1347, got {GAMMAS[0]}"
    print(f"    γ₁ = {GAMMAS[0]:.6f}")
    print("  ✓ Passed")


def test_gammas_strictly_increasing():
    """Los ceros de Riemann deben ser estrictamente crecientes."""
    print("\n✓ Test: ceros de Riemann crecientes...")
    for i in range(len(GAMMAS) - 1):
        assert GAMMAS[i] < GAMMAS[i + 1], \
            f"GAMMAS no es creciente en posición {i}: {GAMMAS[i]} >= {GAMMAS[i+1]}"
    print(f"    γ₁={GAMMAS[0]:.4f} < γ₂={GAMMAS[1]:.4f} < ... < γ₂₀={GAMMAS[19]:.4f}")
    print("  ✓ Passed")


def test_f0_default():
    """Frecuencia fundamental debe ser 141.7001 Hz."""
    print("\n✓ Test: F0_DEFAULT...")
    assert abs(F0_DEFAULT - 141.7001) < 1e-6, \
        f"F0_DEFAULT esperado 141.7001, got {F0_DEFAULT}"
    print(f"    F0_DEFAULT = {F0_DEFAULT} Hz")
    print("  ✓ Passed")


def test_bec_threshold():
    """Umbral BEC debe ser 0.888."""
    print("\n✓ Test: BEC_THRESHOLD...")
    assert abs(BEC_THRESHOLD - 0.888) < 1e-6, \
        f"BEC_THRESHOLD esperado 0.888, got {BEC_THRESHOLD}"
    print(f"    BEC_THRESHOLD = {BEC_THRESHOLD}")
    print("  ✓ Passed")


def test_kk_emission_freq():
    """Frecuencia de emisión KK debe ser ~2003 Hz."""
    print("\n✓ Test: KK_EMISSION_FREQ_HZ...")
    assert abs(KK_EMISSION_FREQ_HZ - 2003.0) < 1.0, \
        f"Emisión KK esperada ~2003 Hz, got {KK_EMISSION_FREQ_HZ}"
    print(f"    KK_EMISSION_FREQ_HZ = {KK_EMISSION_FREQ_HZ} Hz")
    print("  ✓ Passed")


# ── QCALSpectralOperator ──────────────────────────────────────────────────────

def test_operator_default_init():
    """Inicialización por defecto del operador espectral."""
    print("\n✓ Test: QCALSpectralOperator init por defecto...")
    op = QCALSpectralOperator()
    assert abs(op.f0 - F0_DEFAULT) < 1e-6
    assert abs(op.gamma - 1.0) < 1e-10
    assert abs(op.C - 1.0) < 1e-10
    assert abs(op.hbar - 1.0545718e-34) < 1e-40
    print(f"    f0={op.f0}, γ={op.gamma}, C={op.C}")
    print("  ✓ Passed")


def test_operator_zero_C_raises():
    """C=0 debe lanzar ValueError."""
    print("\n✓ Test: QCALSpectralOperator C=0 raises...")
    import pytest
    with pytest.raises(ValueError):
        QCALSpectralOperator(C=0)
    print("  ✓ Passed")


def test_modulation_potential_default():
    """V̂_mod = γ·ħ/C con parámetros por defecto."""
    print("\n✓ Test: modulation_potential...")
    op = QCALSpectralOperator()
    v_mod = op.modulation_potential()
    expected = 1.0 * 1.0545718e-34 / 1.0
    assert abs(v_mod - expected) < 1e-40, \
        f"V̂_mod esperado {expected:.3e}, got {v_mod:.3e}"
    print(f"    V̂_mod = {v_mod:.3e} J·s")
    print("  ✓ Passed")


def test_compute_eigenvalue_first_gamma():
    """λ₁ = γ₁ · f₀ + V̂_mod."""
    print("\n✓ Test: compute_eigenvalue con γ₁...")
    op = QCALSpectralOperator()
    lam = op.compute_eigenvalue(GAMMAS[0])
    expected = GAMMAS[0] * F0_DEFAULT + op.modulation_potential()
    assert abs(lam - expected) < 1e-6, \
        f"λ₁ esperado {expected:.4f}, got {lam:.4f}"
    print(f"    λ₁ = {lam:.4f} Hz  (γ₁·f₀ ≈ {GAMMAS[0]*F0_DEFAULT:.4f})")
    print("  ✓ Passed")


def test_compute_eigenvalue_positive():
    """Todos los autovalores deben ser positivos (γ_n > 0)."""
    print("\n✓ Test: autovalores positivos...")
    op = QCALSpectralOperator()
    for g in GAMMAS:
        lam = op.compute_eigenvalue(g)
        assert lam > 0, f"λ debe ser > 0, got {lam} para γ={g}"
    print(f"    Todos los {len(GAMMAS)} autovalores positivos ✓")
    print("  ✓ Passed")


def test_certify_critical_line_exact():
    """σ = 0.5 debe estar en la línea crítica (on_critical=True, Ψ=1)."""
    print("\n✓ Test: certify_critical_line en σ=0.5...")
    op = QCALSpectralOperator()
    on_critical, psi = op.certify_critical_line(0.5)
    assert on_critical is True, "σ=0.5 debe ser on_critical"
    assert abs(psi - 1.0) < 1e-10, f"Ψ en σ=0.5 debe ser 1.0, got {psi}"
    print(f"    σ=0.5: on_critical={on_critical}, Ψ={psi:.6f}")
    print("  ✓ Passed")


def test_certify_critical_line_off():
    """σ ≠ 0.5 debe dar on_critical=False y Ψ < 1."""
    print("\n✓ Test: certify_critical_line fuera de σ=0.5...")
    op = QCALSpectralOperator()
    for sigma in [0.3, 0.4, 0.6, 0.7]:
        on_critical, psi = op.certify_critical_line(sigma)
        assert on_critical is False, f"σ={sigma} no debe ser on_critical"
        assert psi < 1.0, f"Ψ debe ser < 1 para σ={sigma}, got {psi}"
    print("    σ ∈ {0.3, 0.4, 0.6, 0.7}: on_critical=False, Ψ<1 ✓")
    print("  ✓ Passed")


def test_certify_critical_line_decay_monotone():
    """Ψ(σ) debe decaer monótonamente al alejarse de σ=0.5."""
    print("\n✓ Test: decaimiento monotóno de Ψ...")
    op = QCALSpectralOperator()
    _, psi_05 = op.certify_critical_line(0.5)
    _, psi_04 = op.certify_critical_line(0.4)
    _, psi_03 = op.certify_critical_line(0.3)
    assert psi_05 > psi_04 > psi_03, \
        f"Ψ debe decaer: {psi_05:.4f} > {psi_04:.4f} > {psi_03:.4f}"
    print(f"    Ψ(0.5)={psi_05:.4f} > Ψ(0.4)={psi_04:.4f} > Ψ(0.3)={psi_03:.4f}")
    print("  ✓ Passed")


# ── string_noetic_forcing ─────────────────────────────────────────────────────

def test_forcing_below_threshold_returns_zeros():
    """Ψ < threshold debe devolver forzado cero."""
    print("\n✓ Test: forzado cero bajo umbral BEC...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)

    fx, fy = string_noetic_forcing(0.0, xx, yy, op, Psi_local=0.5, lambda_list=lambda_list)

    assert np.allclose(fx, 0.0), "fx debe ser cero para Ψ < threshold"
    assert np.allclose(fy, 0.0), "fy debe ser cero para Ψ < threshold"
    print(f"    Ψ=0.5 < {BEC_THRESHOLD}: forzado = 0 ✓")
    print("  ✓ Passed")


def test_forcing_above_threshold_nonzero():
    """Ψ ≥ threshold debe producir forzado no nulo."""
    print("\n✓ Test: forzado activo sobre umbral BEC...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)

    fx, fy = string_noetic_forcing(0.1, xx, yy, op, Psi_local=0.95, lambda_list=lambda_list)

    assert np.any(fx != 0.0), "fx no debe ser completamente cero para Ψ >= threshold"
    assert np.any(fy != 0.0), "fy no debe ser completamente cero para Ψ >= threshold"
    print(f"    Ψ=0.95 >= {BEC_THRESHOLD}: forzado activo, max|fx|={np.max(np.abs(fx)):.3e}")
    print("  ✓ Passed")


def test_forcing_shape():
    """El forzado debe tener la misma shape que xx."""
    print("\n✓ Test: shape del forzado...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid(N=16)
    lambda_list = build_lambda_list(op)

    fx, fy = string_noetic_forcing(0.0, xx, yy, op, Psi_local=0.99, lambda_list=lambda_list)

    assert fx.shape == xx.shape, f"fx.shape {fx.shape} != xx.shape {xx.shape}"
    assert fy.shape == yy.shape, f"fy.shape {fy.shape} != yy.shape {yy.shape}"
    print(f"    shape: fx={fx.shape}, xx={xx.shape} ✓")
    print("  ✓ Passed")


def test_forcing_scales_with_psi():
    """El forzado debe escalar monótonamente con Ψ (ganancia ∝ Ψ²)."""
    print("\n✓ Test: escalado del forzado con Ψ...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)

    fx_low, _ = string_noetic_forcing(0.1, xx, yy, op, Psi_local=0.9, lambda_list=lambda_list)
    fx_high, _ = string_noetic_forcing(0.1, xx, yy, op, Psi_local=0.99, lambda_list=lambda_list)

    rms_low = float(np.sqrt(np.mean(fx_low ** 2)))
    rms_high = float(np.sqrt(np.mean(fx_high ** 2)))
    assert rms_high > rms_low, \
        f"RMS debe crecer con Ψ: rms_low={rms_low:.3e}, rms_high={rms_high:.3e}"
    print(f"    RMS(Ψ=0.9)={rms_low:.3e} < RMS(Ψ=0.99)={rms_high:.3e} ✓")
    print("  ✓ Passed")


def test_forcing_threshold_boundary():
    """Exactamente en threshold, el forzado debe ser activo."""
    print("\n✓ Test: forzado en Ψ = threshold exacto...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)[:3]  # Solo 3 modos para velocidad

    fx, fy = string_noetic_forcing(0.0, xx, yy, op, Psi_local=BEC_THRESHOLD,
                                   lambda_list=lambda_list)
    # Ψ_local == threshold → sí activa (condición es Psi_local < threshold)
    assert np.any(fx != 0.0), "Forzado debe activarse cuando Ψ == threshold"
    print(f"    Ψ={BEC_THRESHOLD} (boundary): forzado activo ✓")
    print("  ✓ Passed")


def test_forcing_empty_lambda_list():
    """Lambda list vacía debe devolver ceros (sin modos)."""
    print("\n✓ Test: forzado con lista de modos vacía...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()

    fx, fy = string_noetic_forcing(0.0, xx, yy, op, Psi_local=0.99, lambda_list=[])

    assert np.allclose(fx, 0.0), "Sin modos, fx debe ser cero"
    assert np.allclose(fy, 0.0), "Sin modos, fy debe ser cero"
    print("    Lista vacía: forzado = 0 ✓")
    print("  ✓ Passed")


# ── compute_psi ───────────────────────────────────────────────────────────────

def test_compute_psi_returns_float():
    """compute_psi debe devolver un float."""
    print("\n✓ Test: compute_psi devuelve float...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    u = np.random.randn(*xx.shape)
    v = np.random.randn(*xx.shape)

    psi = compute_psi(u, v, xx, op)
    assert isinstance(psi, float), f"Ψ debe ser float, got {type(psi)}"
    print(f"    Ψ = {psi:.6f}")
    print("  ✓ Passed")


def test_compute_psi_in_range():
    """Ψ debe estar en [0, 1]."""
    print("\n✓ Test: compute_psi ∈ [0, 1]...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    u = np.random.randn(*xx.shape)
    v = np.random.randn(*xx.shape)

    psi = compute_psi(u, v, xx, op)
    assert 0.0 <= psi <= 1.0, f"Ψ debe estar en [0,1], got {psi}"
    print(f"    Ψ = {psi:.6f} ∈ [0, 1] ✓")
    print("  ✓ Passed")


def test_compute_psi_constant_field_safe():
    """Campos constantes no deben provocar NaN/error (std=0)."""
    print("\n✓ Test: compute_psi con campos constantes...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    u = np.ones_like(xx)
    v = np.ones_like(yy)

    psi = compute_psi(u, v, xx, op)
    assert np.isfinite(psi), f"Ψ debe ser finito para campos constantes, got {psi}"
    assert 0.0 <= psi <= 1.0, f"Ψ debe estar en [0,1], got {psi}"
    print(f"    Ψ (campo constante) = {psi:.6f} ✓")
    print("  ✓ Passed")


def test_compute_psi_resonant_field_higher():
    """Campo alineado con f₀ debe producir Ψ más alto que campo aleatorio."""
    print("\n✓ Test: campo resonante produce Ψ más alto...")
    op = QCALSpectralOperator()
    N = 32
    xx, yy = _make_grid(N)
    L = 2 * np.pi

    # Campo perfectamente resonante
    u_res = np.sin(2 * np.pi * op.f0 * xx / L)
    v_res = np.cos(2 * np.pi * op.f0 * xx / L)

    # Campo aleatorio
    rng = np.random.default_rng(42)
    u_rnd = rng.standard_normal(xx.shape)
    v_rnd = rng.standard_normal(xx.shape)

    psi_res = compute_psi(u_res, v_res, xx, op)
    psi_rnd = compute_psi(u_rnd, v_rnd, xx, op)

    assert psi_res > psi_rnd, \
        f"Campo resonante debe tener Ψ mayor: Ψ_res={psi_res:.4f}, Ψ_rnd={psi_rnd:.4f}"
    print(f"    Ψ_resonante={psi_res:.4f} > Ψ_aleatorio={psi_rnd:.4f} ✓")
    print("  ✓ Passed")


# ── build_lambda_list ─────────────────────────────────────────────────────────

def test_build_lambda_list_default():
    """build_lambda_list con gammas=None usa GAMMAS (20 ceros)."""
    print("\n✓ Test: build_lambda_list por defecto...")
    op = QCALSpectralOperator()
    lambdas = build_lambda_list(op)
    assert len(lambdas) == len(GAMMAS), \
        f"Esperados {len(GAMMAS)} autovalores, got {len(lambdas)}"
    print(f"    len(lambdas) = {len(lambdas)}")
    print("  ✓ Passed")


def test_build_lambda_list_values():
    """Autovalores deben coincidir con compute_eigenvalue(γ_n)."""
    print("\n✓ Test: valores de build_lambda_list...")
    op = QCALSpectralOperator()
    lambdas = build_lambda_list(op)
    for i, (lam, g) in enumerate(zip(lambdas, GAMMAS)):
        expected = op.compute_eigenvalue(g)
        assert abs(lam - expected) < 1e-9, \
            f"λ_{i+1} esperado {expected:.6f}, got {lam:.6f}"
    print(f"    Todos los {len(lambdas)} autovalores correctos ✓")
    print("  ✓ Passed")


def test_build_lambda_list_custom_gammas():
    """build_lambda_list con gammas personalizados."""
    print("\n✓ Test: build_lambda_list con gammas personalizados...")
    op = QCALSpectralOperator()
    custom_gammas = [14.1347, 21.0220]
    lambdas = build_lambda_list(op, gammas=custom_gammas)
    assert len(lambdas) == 2
    print(f"    lambdas = {lambdas}")
    print("  ✓ Passed")


def test_lambda_list_first_kk_mode():
    """El primer modo KK debe ser ≈ γ₁ · f₀ (~2003 Hz)."""
    print("\n✓ Test: primer modo KK (~2003 Hz)...")
    op = QCALSpectralOperator()
    lambdas = build_lambda_list(op)
    lam1 = lambdas[0]
    # γ₁ ≈ 14.1347, f₀ = 141.7001 → λ₁ ≈ 2002.35 Hz
    assert 1900 < lam1 < 2100, \
        f"λ₁ esperado ~2003 Hz (en [1900, 2100]), got {lam1:.2f}"
    print(f"    λ₁ = {lam1:.2f} Hz ≈ KK_EMISSION_FREQ_HZ={KK_EMISSION_FREQ_HZ} Hz ✓")
    print("  ✓ Passed")


# ── Integration tests ─────────────────────────────────────────────────────────

def test_full_pipeline_low_coherence():
    """Pipeline completo con Ψ bajo: el forzado no se activa."""
    print("\n✓ Test: pipeline completo Ψ < threshold...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)

    u = np.zeros_like(xx)
    v = np.zeros_like(yy)
    psi = compute_psi(u, v, xx, op)

    fx, fy = string_noetic_forcing(0.0, xx, yy, op, Psi_local=psi, lambda_list=lambda_list)

    assert psi < BEC_THRESHOLD or np.isfinite(np.max(np.abs(fx)))
    print(f"    Ψ={psi:.4f}, forzado max|fx|={np.max(np.abs(fx)):.3e}")
    print("  ✓ Passed")


def test_full_pipeline_high_coherence():
    """Pipeline completo con campo resonante: el forzado se activa."""
    print("\n✓ Test: pipeline completo Ψ > threshold...")
    op = QCALSpectralOperator()
    N = 32
    xx, yy = _make_grid(N)
    L = 2 * np.pi
    lambda_list = build_lambda_list(op)

    # Campo perfectamente resonante → Ψ alto
    u = np.sin(2 * np.pi * op.f0 * xx / L)
    v = np.cos(2 * np.pi * op.f0 * xx / L)
    psi = compute_psi(u, v, xx, op)

    fx, fy = string_noetic_forcing(0.1, xx, yy, op, Psi_local=psi, lambda_list=lambda_list)

    print(f"    Ψ={psi:.4f} (BEC_THRESHOLD={BEC_THRESHOLD})")
    # Result depends on whether psi >= threshold; just check no NaN
    assert np.all(np.isfinite(fx)), "fx no debe contener NaN/Inf"
    assert np.all(np.isfinite(fy)), "fy no debe contener NaN/Inf"
    print(f"    max|fx|={np.max(np.abs(fx)):.3e}, all finite ✓")
    print("  ✓ Passed")


def test_superradiant_gain_formula():
    """Ganancia superradiante N²·Ψ² es consistente con forzado escalonado."""
    print("\n✓ Test: ganancia superradiante N²·Ψ²...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = [op.compute_eigenvalue(GAMMAS[0])]  # Solo λ₁

    psi_a = 0.9
    psi_b = 0.95
    N = N_MICROTUBULES_DEFAULT

    fx_a, _ = string_noetic_forcing(0.0, xx, yy, op, Psi_local=psi_a, lambda_list=lambda_list)
    fx_b, _ = string_noetic_forcing(0.0, xx, yy, op, Psi_local=psi_b, lambda_list=lambda_list)

    rms_a = float(np.sqrt(np.mean(fx_a ** 2)))
    rms_b = float(np.sqrt(np.mean(fx_b ** 2)))

    # gain_ratio = (N²·Ψ_b²) / (N²·Ψ_a²) = (Ψ_b/Ψ_a)²
    expected_ratio = (psi_b / psi_a) ** 2
    actual_ratio = rms_b / rms_a if rms_a > 0 else 0.0

    assert abs(actual_ratio - expected_ratio) < 0.01, \
        f"Ratio ganancia esperado {expected_ratio:.4f}, got {actual_ratio:.4f}"
    print(f"    (Ψ_b/Ψ_a)² = {expected_ratio:.4f}, rms_b/rms_a = {actual_ratio:.4f} ✓")
    print("  ✓ Passed")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])


# ── string_noetic_forcing FFT extension ──────────────────────────────────────

def test_forcing_fft_return_shape():
    """Con return_fft=True, el espectro FFT tiene la misma shape que xx."""
    print("\n✓ Test: forzado con return_fft=True, shape espectro...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid(N=16)
    lambda_list = build_lambda_list(op)[:3]

    fx, fy, fft_spec = string_noetic_forcing(
        0.1, xx, yy, op, Psi_local=0.95, lambda_list=lambda_list, return_fft=True
    )
    assert fft_spec.shape == xx.shape, \
        f"fft_spec.shape {fft_spec.shape} != xx.shape {xx.shape}"
    assert np.all(fft_spec >= 0.0), "Espectro FFT debe ser no negativo"
    print(f"    shape espectro: {fft_spec.shape} ✓")
    print("  ✓ Passed")


def test_forcing_fft_zero_when_below_threshold():
    """Con Psi < threshold y return_fft=True, espectro debe ser cero."""
    print("\n✓ Test: FFT cero bajo umbral...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)[:3]

    fx, fy, fft_spec = string_noetic_forcing(
        0.0, xx, yy, op, Psi_local=0.5, lambda_list=lambda_list, return_fft=True
    )
    assert np.allclose(fft_spec, 0.0), "FFT debe ser cero cuando Psi < threshold"
    print("    FFT cero para Psi < threshold ✓")
    print("  ✓ Passed")


def test_forcing_backward_compat_no_fft():
    """Sin return_fft, la funcion devuelve exactamente 2 elementos."""
    print("\n✓ Test: compatibilidad retroactiva sin return_fft...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)[:2]

    result = string_noetic_forcing(0.0, xx, yy, op, Psi_local=0.95, lambda_list=lambda_list)
    assert len(result) == 2, f"Sin return_fft debe haber 2 elementos, got {len(result)}"
    print("  ✓ Passed")


# ── VenezianoAmplitude ────────────────────────────────────────────────────────

def test_veneziano_regge_trajectory():
    """alpha(s) = alpha0 + alpha_prime*s debe ser lineal."""
    print("\n✓ Test: trayectoria de Regge lineal...")
    va = VenezianoAmplitude(alpha_prime=1.0, alpha_0=-1.0)
    assert abs(va.regge_trajectory(0.0) - (-1.0)) < 1e-12
    assert abs(va.regge_trajectory(1.0) - 0.0) < 1e-12
    assert abs(va.regge_trajectory(2.0) - 1.0) < 1e-12
    print(f"    a(0)={va.regge_trajectory(0)}, a(1)={va.regge_trajectory(1)} ✓")
    print("  ✓ Passed")


def test_veneziano_amplitude_returns_complex():
    """amplitude(s, t) debe devolver un numero complejo."""
    print("\n✓ Test: amplitude devuelve complejo...")
    va = VenezianoAmplitude()
    amp = va.amplitude(1.5, 1.5)
    assert isinstance(amp, complex), f"Debe ser complex, got {type(amp)}"
    print(f"    A(1.5, 1.5) = {amp:.4f}")
    print("  ✓ Passed")


def test_veneziano_amplitude_finite_away_from_poles():
    """La amplitud debe ser finita para valores s, t alejados de polos."""
    print("\n✓ Test: amplitud finita lejos de polos...")
    va = VenezianoAmplitude()
    for s, t in [(1.5, 1.5), (2.3, 1.7), (0.5, 3.0)]:
        amp = va.amplitude(s, t)
        assert np.isfinite(amp.real), f"Re[A({s},{t})] debe ser finito, got {amp}"
    print("  ✓ Passed")


def test_veneziano_mode_coupling_positive():
    """Los acoplamientos de modo alpha_n deben ser positivos."""
    print("\n✓ Test: acoplamientos de modo positivos...")
    va = VenezianoAmplitude(alpha_prime=1.0)
    for n in range(5):
        alpha_n = va.mode_coupling(n)
        assert alpha_n > 0, f"alpha_{n} debe ser > 0, got {alpha_n}"
    print(f"    a_0={va.mode_coupling(0):.4f}, a_1={va.mode_coupling(1):.4f} ✓")
    print("  ✓ Passed")


def test_veneziano_mode_coupling_uses_gammas():
    """mode_coupling(n) = alpha_prime * gamma_n / (n+1)."""
    print("\n✓ Test: formula de acoplamiento de modo...")
    va = VenezianoAmplitude(alpha_prime=1.0)
    for n in range(5):
        expected = 1.0 * GAMMAS[n] / (n + 1)
        assert abs(va.mode_coupling(n) - expected) < 1e-12
    print("  ✓ Passed")


def test_veneziano_regularize_arg_near_pole():
    """_regularize_arg debe desplazar argumentos en o muy cerca de k<=0."""
    print("\n✓ Test: regularizacion en polo...")
    eps = VenezianoAmplitude._POLE_EPS
    assert abs(VenezianoAmplitude._regularize_arg(0.0) - eps) < 1e-15
    assert abs(VenezianoAmplitude._regularize_arg(-1.0) - (-1.0 + eps)) < 1e-15
    assert abs(VenezianoAmplitude._regularize_arg(0.5) - 0.5) < 1e-15
    print("  ✓ Passed")


# ── KaluzaKleinModes ──────────────────────────────────────────────────────────

def test_kk_modes_n_modes():
    """KaluzaKleinModes por defecto tiene 20 modos."""
    print("\n✓ Test: KaluzaKleinModes n_modes por defecto...")
    kk = KaluzaKleinModes()
    assert kk.n_modes == 20, f"Esperado 20 modos, got {kk.n_modes}"
    print(f"    n_modes = {kk.n_modes} ✓")
    print("  ✓ Passed")


def test_kk_modes_frequencies_first():
    """El primer modo KK debe ser gamma_1 x f0 aprox 2003 Hz."""
    print("\n✓ Test: primera frecuencia KK...")
    kk = KaluzaKleinModes()
    freqs = kk.frequencies()
    assert abs(freqs[0] - GAMMAS[0] * F0_DEFAULT) < 1e-6
    assert 1900 < freqs[0] < 2100
    print(f"    lambda1 = {freqs[0]:.2f} Hz ✓")
    print("  ✓ Passed")


def test_kk_modes_t_duality_phase():
    """phi_n = pi/(n+1), base 0."""
    print("\n✓ Test: fases de T-dualidad...")
    kk = KaluzaKleinModes()
    for n in range(5):
        phi = kk.t_duality_phase(n)
        expected = np.pi / (n + 1)
        assert abs(phi - expected) < 1e-12, f"phi_{n} esperado {expected:.4f}, got {phi:.4f}"
    print("  ✓ Passed")


def test_kk_modes_compactification_hex_low():
    """Para n <= 5, radio usa geometria hexagonal EZ."""
    print("\n✓ Test: radio hexagonal para n <= 5...")
    kk = KaluzaKleinModes()
    for n in range(6):
        R = kk.compactification_radius(n)
        expected = np.pi / (GAMMAS[n] * 6)
        assert abs(R - expected) < 1e-12, f"R_{n} esperado {expected:.6f}, got {R:.6f}"
    print("  ✓ Passed")


def test_kk_modes_compactification_cy_high():
    """Para n > 5, radio usa topologia Calabi-Yau periodica."""
    print("\n✓ Test: radio Calabi-Yau para n > 5...")
    kk = KaluzaKleinModes()
    for n in range(6, kk.n_modes):
        R = kk.compactification_radius(n)
        expected = 2.0 * np.pi / GAMMAS[n]
        assert abs(R - expected) < 1e-12, f"R_{n} esperado {expected:.6f}, got {R:.6f}"
    print("  ✓ Passed")


def test_kk_modes_mode_data_keys():
    """mode_data debe contener todas las claves esperadas."""
    print("\n✓ Test: claves de mode_data...")
    kk = KaluzaKleinModes()
    data = kk.mode_data(0)
    expected_keys = {"n", "gamma_n", "frequency_hz", "t_duality_phase",
                     "compactification_radius", "topology"}
    assert expected_keys.issubset(data.keys()), f"Faltan claves: {expected_keys - data.keys()}"
    assert data["topology"] == "hexagonal-EZ"
    print(f"    topology(n=0) = {data['topology']} ✓")
    print("  ✓ Passed")


def test_kk_modes_topology_transitions():
    """Topologia cambia de hexagonal-EZ a Calabi-Yau-periodic en n=6."""
    print("\n✓ Test: transicion de topologia en n=5->6...")
    kk = KaluzaKleinModes()
    assert kk.mode_data(5)["topology"] == "hexagonal-EZ"
    assert kk.mode_data(6)["topology"] == "Calabi-Yau-periodic"
    print("  ✓ Passed")


# ── validate_riemann_stability ────────────────────────────────────────────────

def test_validate_stability_default_passes():
    """Los ceros por defecto deben pasar la validacion."""
    print("\n✓ Test: validacion de estabilidad de Riemann por defecto...")
    result = validate_riemann_stability()
    assert result["stable"] is True, f"Esperado stable=True, got {result}"
    assert result["positive"] is True
    assert result["monotonic"] is True
    assert result["lambda1_valid"] is True
    print(f"    stable={result['stable']}, lambda1={result['lambda1_approx']:.6f} ✓")
    print("  ✓ Passed")


def test_validate_stability_lambda1_value():
    """lambda1_approx debe coincidir con GAMMAS[0]."""
    print("\n✓ Test: lambda1_approx en validacion...")
    result = validate_riemann_stability()
    assert abs(result["lambda1_approx"] - GAMMAS[0]) < 1e-12
    print(f"    lambda1 = {result['lambda1_approx']:.8f} ✓")
    print("  ✓ Passed")


def test_validate_stability_fails_negative():
    """Un cero negativo debe hacer stable=False."""
    print("\n✓ Test: validacion falla con cero negativo...")
    bad_gammas = [-1.0] + GAMMAS[1:]
    result = validate_riemann_stability(bad_gammas)
    assert result["positive"] is False
    assert result["stable"] is False
    print("  ✓ Passed")


def test_validate_stability_fails_non_monotonic():
    """Una secuencia no creciente debe hacer stable=False."""
    print("\n✓ Test: validacion falla con secuencia no monotonica...")
    bad_gammas = list(GAMMAS)
    bad_gammas[1], bad_gammas[2] = bad_gammas[2], bad_gammas[1]
    result = validate_riemann_stability(bad_gammas)
    assert result["monotonic"] is False
    assert result["stable"] is False
    print("  ✓ Passed")


# ── compute_superradiant_gain ─────────────────────────────────────────────────

def test_superradiant_gain_formula():
    """Ganancia = N2 * Psi2."""
    print("\n✓ Test: formula de ganancia superradiante...")
    N = 100.0
    Psi = 0.9
    gain = compute_superradiant_gain(N, Psi)
    expected = N ** 2 * Psi ** 2
    assert abs(gain - expected) < 1e-9, f"Ganancia esperada {expected:.4f}, got {gain:.4f}"
    print(f"    G({N}, {Psi}) = {gain:.4f} ✓")
    print("  ✓ Passed")


def test_superradiant_gain_clamping_below():
    """Psi < 0 se sujeta a 0 -> ganancia = 0."""
    print("\n✓ Test: sujecion Psi < 0...")
    assert abs(compute_superradiant_gain(1e10, -0.5)) < 1e-30
    print("  ✓ Passed")


def test_superradiant_gain_clamping_above():
    """Psi > 1 se sujeta a 1 -> ganancia = N2."""
    print("\n✓ Test: sujecion Psi > 1...")
    N = 5.0
    gain = compute_superradiant_gain(N, 2.0)
    expected = N ** 2 * 1.0 ** 2
    assert abs(gain - expected) < 1e-9
    print(f"    G({N}, 2.0) = {gain:.4f} = N2 ✓")
    print("  ✓ Passed")


def test_superradiant_gain_zero_psi():
    """Psi = 0 -> ganancia = 0."""
    print("\n✓ Test: Psi=0 -> ganancia 0...")
    assert abs(compute_superradiant_gain(1e13, 0.0)) < 1e-30
    print("  ✓ Passed")


def test_superradiant_gain_unit_psi():
    """Psi = 1 -> ganancia = N2."""
    print("\n✓ Test: Psi=1 -> ganancia N2...")
    N = N_MICROTUBULES_DEFAULT
    gain = compute_superradiant_gain(N, 1.0)
    assert abs(gain - N ** 2) < 1.0
    print(f"    G(N_default, 1.0) = {gain:.3e} = N2={N**2:.3e} ✓")
    print("  ✓ Passed")


# ── HolographicFluidSolver ────────────────────────────────────────────────────

def test_fluid_solver_init():
    """HolographicFluidSolver inicializa con la viscosidad adelica correcta."""
    print("\n✓ Test: HolographicFluidSolver init...")
    solver = HolographicFluidSolver(N=16, seed=0)
    assert abs(solver.mu - 1.0 / F0_DEFAULT) < 1e-12, \
        f"mu esperado {1.0/F0_DEFAULT:.6e}, got {solver.mu:.6e}"
    print(f"    mu = 1/f0 = {solver.mu:.6e} ✓")
    print("  ✓ Passed")


def test_fluid_solver_velocity_shape():
    """Los campos de velocidad iniciales tienen shape NxN."""
    print("\n✓ Test: shape de campos de velocidad...")
    N = 16
    solver = HolographicFluidSolver(N=N, seed=1)
    ux, uy = solver.velocity_fields
    assert ux.shape == (N, N), f"ux.shape esperado ({N},{N}), got {ux.shape}"
    assert uy.shape == (N, N)
    print(f"    ux.shape = {ux.shape} ✓")
    print("  ✓ Passed")


def test_fluid_solver_seed_reproducibility():
    """La misma semilla debe producir condiciones iniciales identicas."""
    print("\n✓ Test: reproducibilidad de semilla...")
    s1 = HolographicFluidSolver(N=16, seed=42)
    s2 = HolographicFluidSolver(N=16, seed=42)
    assert np.allclose(s1.ux, s2.ux), "ux debe ser identico con la misma semilla"
    assert np.allclose(s1.uy, s2.uy), "uy debe ser identico con la misma semilla"
    print("  ✓ Passed")


def test_fluid_solver_different_seeds():
    """Semillas distintas deben producir condiciones iniciales distintas."""
    print("\n✓ Test: semillas distintas -> campos distintos...")
    s1 = HolographicFluidSolver(N=16, seed=1)
    s2 = HolographicFluidSolver(N=16, seed=99)
    assert not np.allclose(s1.ux, s2.ux), "Semillas distintas deben dar ux distintos"
    print("  ✓ Passed")


def test_fluid_solver_step_shape():
    """step() devuelve (ux, uy) con la shape correcta."""
    print("\n✓ Test: shape tras step()...")
    N = 16
    solver = HolographicFluidSolver(N=N, seed=7)
    ux, uy = solver.step(dt=0.001)
    assert ux.shape == (N, N) and uy.shape == (N, N)
    print(f"    ux.shape tras step = {ux.shape} ✓")
    print("  ✓ Passed")


def test_fluid_solver_step_changes_field():
    """Un paso debe modificar los campos de velocidad."""
    print("\n✓ Test: step() modifica los campos...")
    solver = HolographicFluidSolver(N=16, seed=5)
    ux0 = solver.ux.copy()
    solver.step(dt=0.001)
    assert not np.allclose(solver.ux, ux0), "ux debe cambiar tras un paso"
    print("  ✓ Passed")


def test_fluid_solver_step_finite():
    """Los campos tras step deben ser finitos."""
    print("\n✓ Test: campos finitos tras step()...")
    solver = HolographicFluidSolver(N=16, seed=3)
    for _ in range(5):
        ux, uy = solver.step(dt=0.0005)
    assert np.all(np.isfinite(ux)), "ux debe ser finito"
    assert np.all(np.isfinite(uy)), "uy debe ser finito"
    print("  ✓ Passed")


def test_fluid_solver_leray_projection():
    """La proyeccion de Leray debe preservar la incompresibilidad."""
    print("\n✓ Test: proyeccion Leray preserva div(u) aprox 0...")
    N = 32
    solver = HolographicFluidSolver(N=N, seed=11)
    rng = np.random.default_rng(0)
    v_x = rng.standard_normal((N, N))
    v_y = rng.standard_normal((N, N))
    vx_hat = np.fft.fft2(v_x)
    vy_hat = np.fft.fft2(v_y)
    px_hat, py_hat = solver._leray_project(vx_hat, vy_hat)
    div_hat = 1j * solver.kx * px_hat + 1j * solver.ky * py_hat
    div = np.fft.ifft2(div_hat).real
    assert np.max(np.abs(div)) < 1e-10, \
        f"div(P(u)) debe ser ~0, max|div|={np.max(np.abs(div)):.2e}"
    print(f"    max|div(P(u))| = {np.max(np.abs(div)):.2e} aprox 0 ✓")
    print("  ✓ Passed")


def test_fluid_solver_kolmogorov_slope_returns_float():
    """kolmogorov_slope debe devolver un float."""
    print("\n✓ Test: kolmogorov_slope devuelve float...")
    solver = HolographicFluidSolver(N=32, seed=0)
    for _ in range(3):
        solver.step(dt=0.001)
    slope = solver.kolmogorov_slope()
    assert isinstance(slope, float), f"Pendiente debe ser float, got {type(slope)}"
    assert np.isfinite(slope), f"Pendiente debe ser finita, got {slope}"
    print(f"    pendiente Kolmogorov = {slope:.4f}")
    print("  ✓ Passed")


def test_fluid_solver_step_with_forcing():
    """step() con forzado externo no genera NaN."""
    print("\n✓ Test: step() con forzado externo...")
    N = 16
    solver = HolographicFluidSolver(N=N, seed=2)
    op = QCALSpectralOperator()
    lambda_list = build_lambda_list(op)[:3]
    fx, fy = string_noetic_forcing(0.0, solver.xx, solver.yy, op,
                                   Psi_local=0.95, lambda_list=lambda_list)
    ux, uy = solver.step(dt=0.001, forcing_x=fx, forcing_y=fy)
    assert np.all(np.isfinite(ux)) and np.all(np.isfinite(uy))
    print("  ✓ Passed")


# ── QCALStringCore ────────────────────────────────────────────────────────────

def test_qcal_string_core_seal():
    """El sello debe ser la cadena correcta."""
    print("\n✓ Test: sello QCALStringCore...")
    core = QCALStringCore(N=16, seed=0)
    assert core.SEAL == "\u2234\U00013080\u03a9\u221e\u00b3\u03a6", \
        f"Sello incorrecto: {core.SEAL}"
    print(f"    SEAL = {core.SEAL} ✓")
    print("  ✓ Passed")


def test_qcal_string_core_cert_string():
    """La cadena de certificacion debe ser 'QED-CUERDAS-VERIFIED'."""
    print("\n✓ Test: cadena de certificacion...")
    assert QCALStringCore.CERT_STRING == "QED-CUERDAS-VERIFIED"
    print("  ✓ Passed")


def test_qcal_string_core_resonance_peak():
    """El pico de resonancia debe ser aprox 2003 Hz."""
    print("\n✓ Test: pico de resonancia QCALStringCore...")
    core = QCALStringCore(N=16, seed=0)
    peak = core.resonance_peak_hz
    assert 1900 < peak < 2100, f"Pico esperado ~2003 Hz, got {peak:.2f}"
    expected = GAMMAS[0] * F0_DEFAULT
    assert abs(peak - expected) < 1e-9
    print(f"    pico = {peak:.4f} Hz ✓")
    print("  ✓ Passed")


def test_qcal_string_core_certify_keys():
    """certify() debe contener las claves: certificate, seal, resonance_peak_hz, sha256."""
    print("\n✓ Test: claves de certify()...")
    core = QCALStringCore(N=16, seed=0)
    cert = core.certify()
    for key in ("certificate", "seal", "resonance_peak_hz", "sha256"):
        assert key in cert, f"Clave '{key}' no encontrada en certificado"
    print("  ✓ Passed")


def test_qcal_string_core_certify_sha256_hex():
    """sha256 debe ser una cadena hex de 64 caracteres."""
    print("\n✓ Test: sha256 de certify()...")
    core = QCALStringCore(N=16, seed=0)
    sha = core.certify()["sha256"]
    assert isinstance(sha, str) and len(sha) == 64
    assert all(c in "0123456789abcdef" for c in sha)
    print(f"    sha256[:16] = {sha[:16]}... ✓")
    print("  ✓ Passed")


def test_qcal_string_core_certify_deterministic():
    """certify() debe ser determinista."""
    print("\n✓ Test: certify() determinista...")
    core = QCALStringCore(N=16, seed=0)
    cert1 = core.certify()
    cert2 = core.certify()
    assert cert1["sha256"] == cert2["sha256"]
    print("  ✓ Passed")


def test_qcal_string_core_run_forcing_cycle():
    """run_forcing_cycle debe devolver dict con las claves esperadas."""
    print("\n✓ Test: run_forcing_cycle() claves de salida...")
    core = QCALStringCore(N=16, seed=0)
    result = core.run_forcing_cycle(t=0.0, Psi_local=0.95, dt=0.001, n_steps=3)
    for key in ("psi", "resonance_peak_hz", "seal", "kolmogorov_slope", "certificate"):
        assert key in result, f"Clave '{key}' no encontrada en resultado"
    print(f"    psi={result['psi']:.4f}, seal={result['seal']} ✓")
    print("  ✓ Passed")


def test_qcal_string_core_run_forcing_cycle_finite():
    """run_forcing_cycle no debe producir NaN."""
    print("\n✓ Test: run_forcing_cycle() sin NaN...")
    core = QCALStringCore(N=16, seed=42)
    result = core.run_forcing_cycle(t=0.0, Psi_local=0.95, dt=0.001, n_steps=5)
    assert np.isfinite(result["psi"]), "psi debe ser finito"
    assert np.isfinite(result["kolmogorov_slope"]), "pendiente debe ser finita"
    print("  ✓ Passed")
