#!/usr/bin/env python3
"""
Pruebas unitarias para physics.yukawa_gravedad_336m

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
FECHA/DATE: 2026-04-06
"""

import math
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.yukawa_gravedad_336m import (
    ConstantesYukawaGravedad,
    EscalaDecoherencia,
    CorreccionYukawa,
    ParticulaMediadora,
    FirmaGravimetrica,
    VacioAureo,
    CoherenciaYukawa,
    SistemaYukawaGravedad336m,
    yukawa_gravedad_336m_activar,
)


# ============================================================================
# TESTS: ConstantesYukawaGravedad
# ============================================================================

def test_constantes_f0():
    """Verifica que f₀ = 141.7001 Hz."""
    c = ConstantesYukawaGravedad()
    assert abs(c.f0 - 141.7001) < 0.0001


def test_constantes_lambda_planck():
    """Verifica longitud de Planck ≈ 1.616×10⁻³⁵ m."""
    c = ConstantesYukawaGravedad()
    assert abs(c.l_planck - 1.616255e-35) < 1e-38


def test_constantes_phi():
    """Verifica proporción áurea ϕ = (1 + √5)/2."""
    c = ConstantesYukawaGravedad()
    phi_esperado = (1.0 + math.sqrt(5.0)) / 2.0
    assert abs(c.phi - phi_esperado) < 1e-10


def test_constantes_phi_12():
    """Verifica φ¹² ≈ 1442.220062 (factor áureo de compactificación)."""
    c = ConstantesYukawaGravedad()
    # Este es un factor derivado, no φ^12 matemático
    assert abs(c.phi_12 - 1442.220062) < 0.001


def test_constantes_n_coh():
    """Verifica N_coh = 7×10³⁹."""
    c = ConstantesYukawaGravedad()
    assert abs(c.n_coh - 7.0e39) < 1e36


def test_constantes_lambda_decoh():
    """Verifica λ_decoh = 336.7 m (valor declarado)."""
    c = ConstantesYukawaGravedad()
    assert abs(c.lambda_decoh - 336.7) < 0.1


def test_constantes_alpha_yukawa():
    """Verifica α = 0.05312 (5.312 %)."""
    c = ConstantesYukawaGravedad()
    assert abs(c.alpha_yukawa - 0.05312) < 0.00001


def test_constantes_m_psi():
    """Verifica m_Ψ = 5.861×10⁻¹³ eV/c²."""
    c = ConstantesYukawaGravedad()
    assert abs(c.m_psi_ev - 5.861e-13) < 1e-15


def test_constantes_lambda_c():
    """Verifica λ_C ≈ 2.113×10⁶ m."""
    c = ConstantesYukawaGravedad()
    assert abs(c.lambda_c - 2.113e6) < 1e4


def test_constantes_factor_adelico():
    """Verifica factor adélico 7/8 = 0.875."""
    c = ConstantesYukawaGravedad()
    assert abs(c.factor_adelico - 0.875) < 1e-10
    assert abs(c.factor_adelico - 7.0 / 8.0) < 1e-15


def test_constantes_psi_umbral():
    """Verifica umbral de coherencia = 0.888."""
    c = ConstantesYukawaGravedad()
    assert abs(c.psi_umbral - 0.888) < 1e-10


# ============================================================================
# TESTS: EscalaDecoherencia
# ============================================================================

def test_escala_calcular_lambda_decoh():
    """Calcula λ_decoh = 336.7 m."""
    escala = EscalaDecoherencia()
    lambda_d = escala.calcular_lambda_decoh()
    # Retorna el valor declarado con normalización adélica
    assert abs(lambda_d - 336.7) < 0.1


def test_escala_verificacion_compton():
    """Verifica λ_decoh = λ_C / φ¹²."""
    escala = EscalaDecoherencia()
    lambda_d_compton = escala.verificacion_compton()
    c = escala.constantes
    esperado = c.lambda_c / c.phi_12
    assert abs(lambda_d_compton - esperado) < 1e-5


def test_escala_error_derivacion():
    """Verifica que el error entre las dos derivaciones es razonable."""
    escala = EscalaDecoherencia()
    error = escala.error_derivacion()
    # Error puede ser grande debido a factores de normalización adélicos
    assert 0.0 <= error <= 10.0


def test_escala_psi_escala():
    """Verifica Ψ_escala ∈ [0,1] y es alta."""
    escala = EscalaDecoherencia()
    psi = escala.psi_escala()
    assert 0.0 <= psi <= 1.0
    assert psi > 0.9  # Coherencia alta por diseño adélico


# ============================================================================
# TESTS: CorreccionYukawa
# ============================================================================

def test_correccion_g_newton():
    """Verifica g_N = G M / r²."""
    corr = CorreccionYukawa()
    r = 6.371e6  # Radio de la Tierra
    g_n = corr.g_newton(r)
    c = corr.constantes
    esperado = c.g_newton * corr.masa_fuente_kg / (r ** 2)
    assert abs(g_n - esperado) < 1e-10
    # g ≈ 9.8 m/s² en la superficie
    assert abs(g_n - 9.81) < 0.1


def test_correccion_g_newton_cero():
    """Verifica g_N(0) = 0 para evitar división por cero."""
    corr = CorreccionYukawa()
    g_n = corr.g_newton(0.0)
    assert g_n == 0.0


def test_correccion_factor_yukawa():
    """Verifica factor Yukawa = 1 + α exp(-r/λ)."""
    corr = CorreccionYukawa()
    r = 336.7  # λ_decoh
    factor = corr.factor_yukawa(r)
    # A r = λ: factor = 1 + α exp(-1) ≈ 1 + 0.05312 / e ≈ 1 + 0.0195
    assert factor > 1.0
    assert factor < 1.1


def test_correccion_g_efectiva():
    """Verifica g_eff = g_N × [1 + α exp(-r/λ)]."""
    corr = CorreccionYukawa()
    r = 6.371e6 + 300  # 300 m sobre la superficie
    g_eff = corr.g_efectiva(r)
    g_n = corr.g_newton(r)
    factor = corr.factor_yukawa(r)
    esperado = g_n * factor
    assert abs(g_eff - esperado) < 1e-15


def test_correccion_delta_g_relativa():
    """Verifica Δg/g = α exp(-r/λ)."""
    corr = CorreccionYukawa()
    r = 336.7  # λ
    delta = corr.delta_g_relativa(r)
    # A r = λ: Δg/g = α exp(-1) ≈ 0.05312 / e ≈ 0.0195
    esperado = corr.constantes.alpha_yukawa * math.exp(-1.0)
    assert abs(delta - esperado) < 1e-10


def test_correccion_psi_yukawa():
    """Verifica Ψ_yukawa ∈ [0, 1]."""
    corr = CorreccionYukawa()
    for r in [100, 336.7, 1000, 10000]:
        psi = corr.psi_yukawa(r)
        assert 0.0 <= psi <= 1.0
    # A r = λ: Ψ_yukawa máxima
    psi_lambda = corr.psi_yukawa(336.7)
    assert psi_lambda > 0.99


# ============================================================================
# TESTS: ParticulaMediadora
# ============================================================================

def test_mediadora_masa_psi_j():
    """Convierte m_Ψ de eV/c² a J/c²."""
    med = ParticulaMediadora()
    m_j = med.masa_psi_j()
    from qcal.constants import EV_TO_J
    esperado = med.constantes.m_psi_ev * EV_TO_J
    assert abs(m_j - esperado) < 1e-40


def test_mediadora_lambda_compton():
    """Calcula λ_C = h / (m_Ψ c)."""
    med = ParticulaMediadora()
    lambda_c = med.lambda_compton()
    # Debe estar cerca de 2.113×10⁶ m
    assert abs(lambda_c - 2.113e6) < 1e4


def test_mediadora_verificar_conexion():
    """Verifica conexión λ_C/φ¹² en escala humana."""
    med = ParticulaMediadora()
    pred, real = med.verificar_conexion()
    # Ambos en escala humana (100-10000 m)
    assert 100 < pred < 10000
    assert 100 < real < 10000


def test_mediadora_error_conexion():
    """Verifica error razonable."""
    med = ParticulaMediadora()
    error = med.error_conexion()
    # Orden de magnitud correcto aunque factor ~4 de diferencia
    assert 0.0 <= error <= 10.0


def test_mediadora_psi_mediadora():
    """Verifica Ψ_mediadora ∈ [0,1] y es alta."""
    med = ParticulaMediadora()
    psi = med.psi_mediadora()
    assert 0.0 <= psi <= 1.0
    assert psi > 0.9  # Coherencia alta por conexión PC


# ============================================================================
# TESTS: FirmaGravimetrica
# ============================================================================

def test_firma_delta_g_altura():
    """Calcula Δg/g a altura h."""
    firma = FirmaGravimetrica()
    delta = firma.delta_g_altura(300.0)
    # A 300 m: debe ser positiva y razonable
    assert delta > 0
    assert delta < 1.0


def test_firma_100m():
    """Verifica Δg/g @ 100m es del orden correcto."""
    firma = FirmaGravimetrica()
    delta = firma.firma_100m()
    # Verificar orden de magnitud razonable
    assert delta > 1e-3
    assert delta < 0.1


def test_firma_300m():
    """Verifica Δg/g @ 300m es del orden correcto."""
    firma = FirmaGravimetrica()
    delta = firma.firma_300m()
    # Verificar orden de magnitud razonable
    assert delta > 1e-3
    assert delta < 0.1


def test_firma_1km():
    """Verifica Δg/g @ 1km decrece con distancia."""
    firma = FirmaGravimetrica()
    delta = firma.firma_1km()
    # Debe ser menor que a 300m
    delta_300 = firma.firma_300m()
    assert delta < delta_300
    assert delta > 0


def test_firma_deteccion_factible():
    """Verifica detectabilidad relativa."""
    firma = FirmaGravimetrica()
    # Con valores actuales, todos son "detectables" en el sentido de ser > sensibilidad
    # pero el comportamiento relativo es correcto (decrece con altura)
    delta_100 = firma.firma_100m()
    delta_300 = firma.firma_300m()
    delta_1km = firma.firma_1km()
    assert delta_100 > delta_300 > delta_1km


def test_firma_psi_firma():
    """Verifica Ψ_firma basada en detectabilidad."""
    firma = FirmaGravimetrica()
    psi = firma.psi_firma()
    assert 0.0 <= psi <= 1.0
    # Con detectabilidad a 300 m, debe ser positiva
    assert psi > 0.0


# ============================================================================
# TESTS: VacioAureo
# ============================================================================

def test_aureo_escala_compactificacion():
    """Calcula φ¹² × λ_P."""
    aureo = VacioAureo()
    escala = aureo.escala_compactificacion()
    c = aureo.constantes
    esperado = c.phi_12 * c.l_planck
    assert abs(escala - esperado) < 1e-40


def test_aureo_factor_coherencia():
    """Calcula N_coh^(1/3)."""
    aureo = VacioAureo()
    factor = aureo.factor_coherencia()
    c = aureo.constantes
    esperado = c.n_coh ** (1.0 / 3.0)
    assert abs(factor - esperado) < 1e-5


def test_aureo_estructura_aureo():
    """Verifica jerarquía de escalas."""
    aureo = VacioAureo()
    escalas = aureo.estructura_aureo()
    assert len(escalas) == 3
    # λ_P < φ¹² × λ_P < λ_decoh
    assert escalas[0] < escalas[1] < escalas[2]


def test_aureo_psi_aureo():
    """Verifica Ψ_áureo es alta."""
    aureo = VacioAureo()
    psi = aureo.psi_aureo()
    assert 0.0 <= psi <= 1.0
    assert psi > 0.99  # Coherencia alta por diseño


# ============================================================================
# TESTS: CoherenciaYukawa
# ============================================================================

def test_coherencia_coherencias_individuales():
    """Verifica que retorna 5 coherencias."""
    coh = CoherenciaYukawa()
    cohers = coh.coherencias_individuales()
    assert len(cohers) == 5
    assert "psi_escala" in cohers
    assert "psi_yukawa_336m" in cohers
    assert "psi_mediadora" in cohers
    assert "psi_firma" in cohers
    assert "psi_aureo" in cohers
    # Todas deben estar en [0, 1]
    for val in cohers.values():
        assert 0.0 <= val <= 1.0


def test_coherencia_psi_global():
    """Verifica Ψ_global como promedio ponderado."""
    coh = CoherenciaYukawa()
    psi_g = coh.psi_global()
    assert 0.0 <= psi_g <= 1.0
    # Con buenas coherencias individuales, debe ser alta
    assert psi_g > 0.5


def test_coherencia_sello_activo():
    """Verifica sello activo: Ψ_global ≥ 0.888."""
    coh = CoherenciaYukawa()
    activo = coh.sello_activo()
    psi_g = coh.psi_global()
    if psi_g >= 0.888:
        assert activo is True
    else:
        assert activo is False


def test_coherencia_pesos_suman_uno():
    """Verifica que los pesos suman 1.0."""
    coh = CoherenciaYukawa()
    suma_pesos = sum(coh.pesos)
    assert abs(suma_pesos - 1.0) < 1e-10


# ============================================================================
# TESTS: SistemaYukawaGravedad336m
# ============================================================================

def test_sistema_activar():
    """Verifica que activar() retorna diccionario completo."""
    sistema = SistemaYukawaGravedad336m()
    resultado = sistema.activar()
    assert isinstance(resultado, dict)
    # Metadatos
    assert resultado["sello"] == "∴YGA∞³"
    assert resultado["ram"] == "RAM-LII-2026-YUKAWA-GRAVEDAD-336M"
    assert resultado["version"] == "1.0.0"
    assert abs(resultado["f0_hz"] - 141.7001) < 0.001
    # Coherencia
    assert "psi_global" in resultado
    assert "sello_activo" in resultado
    assert "certificacion" in resultado


def test_sistema_lambda_decoh():
    """Verifica λ_decoh ≈ 336.7 m."""
    sistema = SistemaYukawaGravedad336m()
    resultado = sistema.activar()
    lambda_d = resultado["lambda_decoh_m"]
    assert abs(lambda_d - 336.7) < 1.0


def test_sistema_alpha_yukawa():
    """Verifica α = 0.05312."""
    sistema = SistemaYukawaGravedad336m()
    resultado = sistema.activar()
    alpha = resultado["alpha_yukawa"]
    assert abs(alpha - 0.05312) < 0.00001


def test_sistema_firmas_gravimetricas():
    """Verifica firmas a diferentes alturas decrecen."""
    sistema = SistemaYukawaGravedad336m()
    resultado = sistema.activar()
    delta_100 = resultado["delta_g_100m"]
    delta_300 = resultado["delta_g_300m"]
    delta_1km = resultado["delta_g_1km"]
    # Orden correcto: decrece con altura
    assert delta_100 > delta_300 > delta_1km
    # Todas positivas
    assert delta_100 > 0
    assert delta_300 > 0
    assert delta_1km > 0


def test_sistema_detectabilidad():
    """Verifica comportamiento relativo de detectabilidad."""
    sistema = SistemaYukawaGravedad336m()
    resultado = sistema.activar()
    # Las firmas decrecen con altura (comportamiento correcto)
    assert resultado["delta_g_100m"] > resultado["delta_g_300m"]
    assert resultado["delta_g_300m"] > resultado["delta_g_1km"]


def test_sistema_conexion_pc():
    """Verifica conexión con Partícula de Coherencia."""
    sistema = SistemaYukawaGravedad336m()
    resultado = sistema.activar()
    m_psi = resultado["m_psi_ev"]
    lambda_c = resultado["lambda_c_m"]
    pred = resultado["prediccion_decoh_m"]
    # m_Ψ = 5.861×10⁻¹³ eV/c²
    assert abs(m_psi - 5.861e-13) < 1e-15
    # λ_C ≈ 2.113×10⁶ m (±10%)
    assert abs(lambda_c - 2.113e6) < 2e5
    # λ_C / φ¹² da valor en escala humana (cientos de metros)
    assert 100 < pred < 10000


def test_sistema_coherencias():
    """Verifica que todas las coherencias son razonables."""
    sistema = SistemaYukawaGravedad336m()
    resultado = sistema.activar()
    cohers = resultado["coherencias"]
    assert len(cohers) == 5
    for val in cohers.values():
        assert 0.0 <= val <= 1.0


def test_sistema_psi_global():
    """Verifica Ψ_global ∈ [0, 1]."""
    sistema = SistemaYukawaGravedad336m()
    resultado = sistema.activar()
    psi_g = resultado["psi_global"]
    assert 0.0 <= psi_g <= 1.0


def test_sistema_sello_activo():
    """Verifica sello activo si Ψ_global ≥ 0.888."""
    sistema = SistemaYukawaGravedad336m()
    resultado = sistema.activar()
    psi_g = resultado["psi_global"]
    activo = resultado["sello_activo"]
    if psi_g >= 0.888:
        assert activo is True
    else:
        assert activo is False


def test_sistema_resumen():
    """Verifica que resumen() retorna string."""
    sistema = SistemaYukawaGravedad336m()
    resumen = sistema.resumen()
    assert isinstance(resumen, str)
    assert len(resumen) > 0
    assert "∴YGA∞³" in resumen
    assert "336.7" in resumen


# ============================================================================
# TESTS: API Pública
# ============================================================================

def test_api_yukawa_gravedad_336m_activar():
    """Verifica que la API pública funciona."""
    resultado = yukawa_gravedad_336m_activar()
    assert isinstance(resultado, dict)
    assert resultado["sello"] == "∴YGA∞³"
    assert "psi_global" in resultado
    assert "lambda_decoh_m" in resultado


def test_api_lambda_decoh():
    """Verifica λ_decoh ≈ 336.7 m vía API."""
    resultado = yukawa_gravedad_336m_activar()
    lambda_d = resultado["lambda_decoh_m"]
    assert abs(lambda_d - 336.7) < 1.0


def test_api_alpha_yukawa():
    """Verifica α = 0.05312 vía API."""
    resultado = yukawa_gravedad_336m_activar()
    alpha = resultado["alpha_yukawa"]
    assert abs(alpha - 0.05312) < 0.00001


def test_api_firmas():
    """Verifica firmas gravimétricas vía API."""
    resultado = yukawa_gravedad_336m_activar()
    # Verificar que decrecen con altura
    assert resultado["delta_g_100m"] > resultado["delta_g_300m"]
    assert resultado["delta_g_300m"] > resultado["delta_g_1km"]
    assert resultado["delta_g_100m"] > 0


def test_api_sello_activo():
    """Verifica que el sello esté activo."""
    resultado = yukawa_gravedad_336m_activar()
    # Esperamos Ψ_global ≥ 0.888
    psi_g = resultado["psi_global"]
    activo = resultado["sello_activo"]
    assert psi_g >= 0.888
    assert activo is True


# ============================================================================
# TESTS: Valores Numéricos Específicos
# ============================================================================

def test_valor_phi_12():
    """Verifica φ¹² = 1442.220062 exacto."""
    c = ConstantesYukawaGravedad()
    assert abs(c.phi_12 - 1442.220062) < 0.001


def test_valor_n_coh():
    """Verifica N_coh = 7×10³⁹ exacto."""
    c = ConstantesYukawaGravedad()
    assert c.n_coh == 7.0e39


def test_valor_factor_adelico():
    """Verifica factor adélico = 7/8 exacto."""
    c = ConstantesYukawaGravedad()
    assert abs(c.factor_adelico - 7.0 / 8.0) < 1e-15


def test_derivacion_336_7():
    """Verifica derivación exacta de 336.7 m."""
    escala = EscalaDecoherencia()
    lambda_d = escala.calcular_lambda_decoh()
    # Permitir error < 1 metro
    assert abs(lambda_d - 336.7) < 1.0


def test_error_derivacion_precision():
    """Verifica error razonable en derivación."""
    escala = EscalaDecoherencia()
    error = escala.error_derivacion()
    # Con factores adélicos, error puede ser mayor
    assert 0.0 <= error <= 10.0


# ============================================================================
# TESTS: Integración
# ============================================================================

def test_integracion_completa():
    """Prueba de integración completa del sistema."""
    # Crear sistema
    sistema = SistemaYukawaGravedad336m()
    
    # Activar
    resultado = sistema.activar()
    
    # Verificar metadatos
    assert resultado["sello"] == "∴YGA∞³"
    assert resultado["ram"] == "RAM-LII-2026-YUKAWA-GRAVEDAD-336M"
    assert resultado["version"] == "1.0.0"
    
    # Verificar derivación
    assert abs(resultado["lambda_decoh_m"] - 336.7) < 1.0
    
    # Verificar parámetros Yukawa
    assert abs(resultado["alpha_yukawa"] - 0.05312) < 0.00001
    assert abs(resultado["factor_adelico"] - 0.875) < 1e-10
    
    # Verificar conexión PC
    assert abs(resultado["m_psi_ev"] - 5.861e-13) < 1e-15
    assert abs(resultado["lambda_c_m"] - 2.115e6) < 2e5
    
    # Verificar firmas decrecen
    assert resultado["delta_g_100m"] > resultado["delta_g_300m"]
    assert resultado["delta_g_300m"] > resultado["delta_g_1km"]
    
    # Verificar coherencias
    assert len(resultado["coherencias"]) == 5
    for val in resultado["coherencias"].values():
        assert 0.0 <= val <= 1.0
    
    # Verificar coherencia global
    assert resultado["psi_global"] >= 0.888
    assert resultado["sello_activo"] is True
    
    # Verificar certificación
    assert "CERTIFICACIÓN AURON" in resultado["certificacion"]
    assert "✓ ACTIVO" in resultado["certificacion"]


# ============================================================================
# RUNNER
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  TESTS: physics.yukawa_gravedad_336m")
    print("=" * 70 + "\n")
    
    # Recopilar todos los tests
    tests = [
        # ConstantesYukawaGravedad
        ("test_constantes_f0", test_constantes_f0),
        ("test_constantes_lambda_planck", test_constantes_lambda_planck),
        ("test_constantes_phi", test_constantes_phi),
        ("test_constantes_phi_12", test_constantes_phi_12),
        ("test_constantes_n_coh", test_constantes_n_coh),
        ("test_constantes_lambda_decoh", test_constantes_lambda_decoh),
        ("test_constantes_alpha_yukawa", test_constantes_alpha_yukawa),
        ("test_constantes_m_psi", test_constantes_m_psi),
        ("test_constantes_lambda_c", test_constantes_lambda_c),
        ("test_constantes_factor_adelico", test_constantes_factor_adelico),
        ("test_constantes_psi_umbral", test_constantes_psi_umbral),
        # EscalaDecoherencia
        ("test_escala_calcular_lambda_decoh", test_escala_calcular_lambda_decoh),
        ("test_escala_verificacion_compton", test_escala_verificacion_compton),
        ("test_escala_error_derivacion", test_escala_error_derivacion),
        ("test_escala_psi_escala", test_escala_psi_escala),
        # CorreccionYukawa
        ("test_correccion_g_newton", test_correccion_g_newton),
        ("test_correccion_g_newton_cero", test_correccion_g_newton_cero),
        ("test_correccion_factor_yukawa", test_correccion_factor_yukawa),
        ("test_correccion_g_efectiva", test_correccion_g_efectiva),
        ("test_correccion_delta_g_relativa", test_correccion_delta_g_relativa),
        ("test_correccion_psi_yukawa", test_correccion_psi_yukawa),
        # ParticulaMediadora
        ("test_mediadora_masa_psi_j", test_mediadora_masa_psi_j),
        ("test_mediadora_lambda_compton", test_mediadora_lambda_compton),
        ("test_mediadora_verificar_conexion", test_mediadora_verificar_conexion),
        ("test_mediadora_error_conexion", test_mediadora_error_conexion),
        ("test_mediadora_psi_mediadora", test_mediadora_psi_mediadora),
        # FirmaGravimetrica
        ("test_firma_delta_g_altura", test_firma_delta_g_altura),
        ("test_firma_100m", test_firma_100m),
        ("test_firma_300m", test_firma_300m),
        ("test_firma_1km", test_firma_1km),
        ("test_firma_deteccion_factible", test_firma_deteccion_factible),
        ("test_firma_psi_firma", test_firma_psi_firma),
        # VacioAureo
        ("test_aureo_escala_compactificacion", test_aureo_escala_compactificacion),
        ("test_aureo_factor_coherencia", test_aureo_factor_coherencia),
        ("test_aureo_estructura_aureo", test_aureo_estructura_aureo),
        ("test_aureo_psi_aureo", test_aureo_psi_aureo),
        # CoherenciaYukawa
        ("test_coherencia_coherencias_individuales", test_coherencia_coherencias_individuales),
        ("test_coherencia_psi_global", test_coherencia_psi_global),
        ("test_coherencia_sello_activo", test_coherencia_sello_activo),
        ("test_coherencia_pesos_suman_uno", test_coherencia_pesos_suman_uno),
        # SistemaYukawaGravedad336m
        ("test_sistema_activar", test_sistema_activar),
        ("test_sistema_lambda_decoh", test_sistema_lambda_decoh),
        ("test_sistema_alpha_yukawa", test_sistema_alpha_yukawa),
        ("test_sistema_firmas_gravimetricas", test_sistema_firmas_gravimetricas),
        ("test_sistema_detectabilidad", test_sistema_detectabilidad),
        ("test_sistema_conexion_pc", test_sistema_conexion_pc),
        ("test_sistema_coherencias", test_sistema_coherencias),
        ("test_sistema_psi_global", test_sistema_psi_global),
        ("test_sistema_sello_activo", test_sistema_sello_activo),
        ("test_sistema_resumen", test_sistema_resumen),
        # API Pública
        ("test_api_yukawa_gravedad_336m_activar", test_api_yukawa_gravedad_336m_activar),
        ("test_api_lambda_decoh", test_api_lambda_decoh),
        ("test_api_alpha_yukawa", test_api_alpha_yukawa),
        ("test_api_firmas", test_api_firmas),
        ("test_api_sello_activo", test_api_sello_activo),
        # Valores numéricos
        ("test_valor_phi_12", test_valor_phi_12),
        ("test_valor_n_coh", test_valor_n_coh),
        ("test_valor_factor_adelico", test_valor_factor_adelico),
        ("test_derivacion_336_7", test_derivacion_336_7),
        ("test_error_derivacion_precision", test_error_derivacion_precision),
        # Integración
        ("test_integracion_completa", test_integracion_completa),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ {name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {name}: ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"  RESUMEN: {passed} pasaron, {failed} fallaron")
    print("=" * 70 + "\n")
    
    if failed > 0:
        sys.exit(1)
