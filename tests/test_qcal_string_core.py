#!/usr/bin/env python3
"""
Tests: QCAL-Strings — Forzado de Modos Kaluza-Klein
═════════════════════════════════════════════════════════════════════════════

Pruebas unitarias para physics/qcal_string_core.py.
Verifica las 8 clases y las 2 funciones de la API pública.

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
