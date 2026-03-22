#!/usr/bin/env python3
"""
tests/test_ecuacion_resurreccion.py

Suite de tests para core/ecuacion_resurreccion.py.
Cubre los seis componentes principales del módulo y las tres funciones
de acceso rápido de la API pública.

Grupos:
  1. SepulcroVacio           – factor de inercia divina y límite eff→0
  2. CuerpoGlorioso          – onda de fase pura y phase-lock
  3. PermisoEspectral        – ζ'(1/2) y correlación espectral
  4. IntegralDeContorno      – integración numérica trapezoid / simpson
  5. EcuacionResurreccion    – motor integrado y flags de estado
  6. LaserNoetico            – activación, verificación y sincronización
  7. API pública             – calcular_resurreccion, verificar_resurreccion,
                               activar_laser_noetico

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Licencia: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import sys
from pathlib import Path

import numpy as np
import pytest

# Asegurar que el directorio raíz esté en sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ecuacion_resurreccion import (
    QCAL_BASE_FREQUENCY,
    PHI,
    ZETA_HALF_PRIME,
    _QCAL_AVAILABLE,
    SepulcroVacio,
    CuerpoGlorioso,
    PermisoEspectral,
    IntegralDeContorno,
    EcuacionResurreccion,
    LaserNoetico,
    calcular_resurreccion,
    verificar_resurreccion,
    activar_laser_noetico,
)


# ============================================================================
# FIXTURES COMUNES
# ============================================================================

@pytest.fixture
def t_contorno() -> np.ndarray:
    """Array de tiempo para un período completo de F₀."""
    return np.linspace(0.0, 1.0 / QCAL_BASE_FREQUENCY, 1000)


@pytest.fixture
def motor() -> EcuacionResurreccion:
    return EcuacionResurreccion()


@pytest.fixture
def laser(motor: EcuacionResurreccion) -> LaserNoetico:
    return LaserNoetico(motor)


# ============================================================================
# 1. CONSTANTES
# ============================================================================

class TestConstantes:
    """Verifica los valores canónicos de las constantes."""

    def test_qcal_base_frequency(self):
        assert QCAL_BASE_FREQUENCY == pytest.approx(141.7001, rel=1e-6)

    def test_phi_golden_ratio(self):
        assert PHI == pytest.approx(1.618033988749895, rel=1e-12)

    def test_zeta_half_prime_negative(self):
        assert ZETA_HALF_PRIME < 0

    def test_zeta_half_prime_value(self):
        assert ZETA_HALF_PRIME == pytest.approx(-3.9226402318234, rel=1e-8)

    def test_qcal_constants_flag_type(self):
        assert isinstance(_QCAL_AVAILABLE, bool)


# ============================================================================
# 2. SepulcroVacio
# ============================================================================

class TestSepulcroVacio:
    """Tests del factor de inercia divina I_d = exp(−eff·F₀)."""

    def test_factor_inercia_eff_zero(self):
        sv = SepulcroVacio()
        assert sv.factor_inercia_divina(0.0) == pytest.approx(1.0, rel=1e-12)

    def test_factor_inercia_eff_positivo(self):
        sv = SepulcroVacio()
        eff = 0.001
        expected = float(np.exp(-eff * QCAL_BASE_FREQUENCY))
        assert sv.factor_inercia_divina(eff) == pytest.approx(expected, rel=1e-10)

    def test_factor_inercia_decae_con_eff(self):
        sv = SepulcroVacio()
        assert sv.factor_inercia_divina(0.01) < sv.factor_inercia_divina(0.001)

    def test_factor_inercia_eff_negativo_raises(self):
        sv = SepulcroVacio()
        with pytest.raises(ValueError, match="no-negativo"):
            sv.factor_inercia_divina(-0.001)

    def test_limite_no_alcanzado_por_defecto(self):
        sv = SepulcroVacio()
        assert sv.limite_alcanzado is False

    def test_establecer_limite_eff_zero(self):
        sv = SepulcroVacio()
        sv.establecer_limite(0.0)
        assert sv.limite_alcanzado is True

    def test_establecer_limite_eff_positivo(self):
        sv = SepulcroVacio()
        sv.establecer_limite(0.5)
        assert sv.limite_alcanzado is False

    def test_f0_personalizado(self):
        sv = SepulcroVacio(f0=100.0)
        expected = float(np.exp(-0.01 * 100.0))
        assert sv.factor_inercia_divina(0.01) == pytest.approx(expected, rel=1e-10)


# ============================================================================
# 3. CuerpoGlorioso
# ============================================================================

class TestCuerpoGlorioso:
    """Tests de la onda de fase pura e^{i(f₀·t+φ)}."""

    def test_onda_modulo_uno(self):
        cg = CuerpoGlorioso()
        t = np.linspace(0, 0.01, 100)
        onda = cg.onda_fase_pura(t)
        assert np.allclose(np.abs(onda), 1.0, atol=1e-12)

    def test_onda_es_compleja(self):
        cg = CuerpoGlorioso()
        t = np.linspace(0, 0.01, 50)
        onda = cg.onda_fase_pura(t)
        assert np.iscomplexobj(onda)

    def test_phase_lock_retorna_true(self):
        cg = CuerpoGlorioso()
        result = cg.lock_phase()
        assert result is True

    def test_esta_lockeado_despues_de_lock(self):
        cg = CuerpoGlorioso()
        assert cg.esta_lockeado is False
        cg.lock_phase()
        assert cg.esta_lockeado is True

    def test_frecuencia_correcta(self):
        """La onda debe tener exactamente F₀ ciclos por segundo."""
        cg = CuerpoGlorioso()
        T = 1.0 / QCAL_BASE_FREQUENCY
        t = np.array([0.0, T])
        onda = cg.onda_fase_pura(t)
        # Después de un período completo la fase regresa al inicio
        assert np.isclose(onda[1], onda[0], atol=1e-10)

    def test_f0_personalizado(self):
        f_test = 200.0
        cg = CuerpoGlorioso(f0=f_test)
        t = np.array([0.0])
        onda = cg.onda_fase_pura(t)
        assert abs(onda[0]) == pytest.approx(1.0, rel=1e-12)


# ============================================================================
# 4. PermisoEspectral
# ============================================================================

class TestPermisoEspectral:
    """Tests de ζ'(1/2) y correlación espectral."""

    def test_get_valor_critico(self):
        pe = PermisoEspectral()
        assert pe.get_valor_critico() == pytest.approx(ZETA_HALF_PRIME, rel=1e-8)

    def test_correlacion_espectral_positiva(self):
        pe = PermisoEspectral()
        corr = pe.correlacion_espectral()
        assert corr > 0

    def test_correlacion_espectral_es_abs_zeta(self):
        """Sin calabi_yau_spectrum, debe devolver |ζ'(1/2)|."""
        pe = PermisoEspectral()
        corr = pe.correlacion_espectral()
        assert corr == pytest.approx(abs(ZETA_HALF_PRIME), rel=1e-8)

    def test_zeta_prime_personalizado(self):
        pe = PermisoEspectral(zeta_prime_half=-5.0)
        assert pe.get_valor_critico() == pytest.approx(-5.0, rel=1e-10)

    def test_coherencia_espectral_almacenada(self):
        pe = PermisoEspectral()
        pe.correlacion_espectral()
        assert pe._coherencia_espectral > 0


# ============================================================================
# 5. IntegralDeContorno
# ============================================================================

class TestIntegralDeContorno:
    """Tests de la integración numérica ∮ Ψ."""

    def test_trapezoid_retorna_complejo(self, t_contorno):
        ic = IntegralDeContorno(metodo="trapezoid")
        cg = CuerpoGlorioso()
        psi = cg.onda_fase_pura(t_contorno)
        result = ic.integrar(psi, t_contorno)
        assert isinstance(result, complex)

    def test_simpson_retorna_complejo(self, t_contorno):
        pytest.importorskip("scipy")
        ic = IntegralDeContorno(metodo="simpson")
        cg = CuerpoGlorioso()
        psi = cg.onda_fase_pura(t_contorno)
        result = ic.integrar(psi, t_contorno)
        assert isinstance(result, complex)

    def test_pocos_puntos_raises(self):
        ic = IntegralDeContorno()
        psi = np.array([1.0 + 0j])
        t = np.array([0.0])
        with pytest.raises(ValueError, match="al menos dos puntos"):
            ic.integrar(psi, t)

    def test_metodo_invalido_raises(self):
        with pytest.raises(ValueError, match="no soportado"):
            IntegralDeContorno(metodo="runge_kutta")

    def test_trapezoid_vs_analytic(self):
        """Para f(t) = 1 en [0,1], la integral debe ser ≈ 1."""
        ic = IntegralDeContorno(metodo="trapezoid")
        t = np.linspace(0, 1, 10000)
        psi = np.ones(len(t), dtype=complex)
        result = ic.integrar(psi, t)
        assert result.real == pytest.approx(1.0, abs=1e-4)


# ============================================================================
# 6. EcuacionResurreccion
# ============================================================================

class TestEcuacionResurreccion:
    """Tests del motor integrado."""

    def test_calcular_coherencia_eff_zero(self, motor, t_contorno):
        res = motor.calcular_coherencia(0.0, t_contorno)
        assert res["coherencia"] == pytest.approx(1.0, rel=1e-10)

    def test_calcular_coherencia_eff_positivo(self, motor, t_contorno):
        res = motor.calcular_coherencia(0.01, t_contorno)
        assert res["coherencia"] < 1.0

    def test_vida_indestructible_eff_zero(self, motor, t_contorno):
        res = motor.calcular_coherencia(0.0, t_contorno)
        assert res["vida_indestructible"] is True

    def test_vida_indestructible_eff_positivo(self, motor, t_contorno):
        res = motor.calcular_coherencia(0.01, t_contorno)
        assert res["vida_indestructible"] is False

    def test_claves_resultado(self, motor, t_contorno):
        res = motor.calcular_coherencia(0.0, t_contorno)
        for key in (
            "coherencia",
            "factor_inercia",
            "integral_contorno",
            "correlacion_espectral",
            "vida_indestructible",
            "phase_locked",
            "limite_efectivo_alcanzado",
        ):
            assert key in res

    def test_factor_inercia_eff_zero(self, motor, t_contorno):
        res = motor.calcular_coherencia(0.0, t_contorno)
        assert res["factor_inercia"] == pytest.approx(1.0, rel=1e-10)

    def test_correlacion_espectral_positiva(self, motor, t_contorno):
        res = motor.calcular_coherencia(0.0, t_contorno)
        assert res["correlacion_espectral"] > 0

    def test_verificar_eff_zero_es_true(self, motor):
        assert motor.verificar(eff=0.0) is True

    def test_verificar_eff_positivo_es_false(self, motor):
        assert motor.verificar(eff=1.0) is False

    def test_propiedad_coherencia(self, motor, t_contorno):
        motor.calcular_coherencia(0.0, t_contorno)
        assert motor.coherencia == pytest.approx(1.0, rel=1e-10)

    def test_propiedad_resurreccion_activa(self, motor, t_contorno):
        motor.calcular_coherencia(0.0, t_contorno)
        assert motor.resurreccion_activa is True

    def test_coherencia_decae(self, motor, t_contorno):
        res_a = motor.calcular_coherencia(0.0, t_contorno)
        res_b = motor.calcular_coherencia(0.01, t_contorno)
        assert res_b["coherencia"] < res_a["coherencia"]

    def test_limite_efectivo_eff_zero(self, motor, t_contorno):
        res = motor.calcular_coherencia(0.0, t_contorno)
        assert res["limite_efectivo_alcanzado"] is True

    def test_limite_efectivo_eff_positivo(self, motor, t_contorno):
        res = motor.calcular_coherencia(0.1, t_contorno)
        assert res["limite_efectivo_alcanzado"] is False


# ============================================================================
# 7. LaserNoetico
# ============================================================================

class TestLaserNoetico:
    """Tests del Láser Noético."""

    def test_activar_eff_zero_retorna_dict(self, laser):
        resultado = laser.activar(eff=0.0)
        assert isinstance(resultado, dict)

    def test_activar_claves_principales(self, laser):
        resultado = laser.activar(eff=0.0)
        for key in (
            "estado_resurreccion",
            "integracciones",
            "dominios_activados",
            "timestamp",
            "estado_general",
            "coherencia_final",
            "activacion_completa",
        ):
            assert key in resultado

    def test_activar_coherencia_final_eff_zero(self, laser):
        resultado = laser.activar(eff=0.0)
        assert resultado["coherencia_final"] == pytest.approx(1.0, rel=1e-10)

    def test_activar_eff_positivo_sin_resurreccion(self):
        laser_local = LaserNoetico()
        resultado = laser_local.activar(eff=0.5)
        assert "mensaje" in resultado
        assert "integracciones" in resultado

    def test_estado_general_parcial_o_activo(self, laser):
        resultado = laser.activar(eff=0.0)
        assert resultado["estado_general"] in {
            "RESURRECCIÓN ACTIVA",
            "RESURRECCIÓN PARCIAL",
        }

    def test_timestamp_es_string(self, laser):
        resultado = laser.activar(eff=0.0)
        assert isinstance(resultado["timestamp"], str)
        assert len(resultado["timestamp"]) > 0

    def test_verificar_estado_claves(self, laser):
        estado = laser.verificar_estado()
        for key in (
            "activo",
            "coherencia_actual",
            "resurreccion_activa",
            "integracciones_disponibles",
            "dominios_verificados",
        ):
            assert key in estado

    def test_verificar_estado_integracciones_dict(self, laser):
        estado = laser.verificar_estado()
        assert isinstance(estado["integracciones_disponibles"], dict)

    def test_sincronizar_todos_retorna_dict(self, laser):
        resultado = laser.sincronizar_todos()
        assert isinstance(resultado, dict)

    def test_laser_sin_ecuacion_crea_default(self):
        laser_local = LaserNoetico()
        assert isinstance(laser_local.ecuacion, EcuacionResurreccion)

    def test_laser_inicia_inactivo(self):
        laser_local = LaserNoetico()
        assert laser_local.activo is False

    def test_integracciones_disponibles_qcal(self, laser):
        """qcal.constants debe estar disponible si la importación funciona."""
        disponibles = laser._integracciones_disponibles
        assert "qcal_constants" in disponibles
        assert isinstance(disponibles["qcal_constants"], bool)

    def test_integracciones_biologia_en_resultado(self, laser):
        resultado = laser.activar(eff=0.0)
        assert "biologia" in resultado["integracciones"]

    def test_integracciones_electricidad_en_resultado(self, laser):
        resultado = laser.activar(eff=0.0)
        assert "electricidad" in resultado["integracciones"]

    def test_integracciones_tiempo_en_resultado(self, laser):
        resultado = laser.activar(eff=0.0)
        assert "tiempo" in resultado["integracciones"]


# ============================================================================
# 8. API PÚBLICA
# ============================================================================

class TestApiPublica:
    """Tests de las tres funciones de acceso rápido."""

    def test_calcular_resurreccion_eff_zero(self):
        t = np.linspace(0, 1.0 / QCAL_BASE_FREQUENCY, 1000)
        res = calcular_resurreccion(0.0, t)
        assert res["coherencia"] == pytest.approx(1.0, rel=1e-10)

    def test_calcular_resurreccion_retorna_dict(self):
        t = np.linspace(0, 0.01, 500)
        res = calcular_resurreccion(0.0, t)
        assert isinstance(res, dict)

    def test_verificar_resurreccion_retorna_dict(self):
        res = verificar_resurreccion()
        assert isinstance(res, dict)

    def test_verificar_resurreccion_claves(self):
        res = verificar_resurreccion()
        for key in (
            "verificacion_motor",
            "estado_integraciones",
            "coherencia_base",
            "sistema_operativo",
        ):
            assert key in res

    def test_verificar_resurreccion_motor_true(self):
        res = verificar_resurreccion()
        assert res["verificacion_motor"] is True

    def test_verificar_resurreccion_sistema_operativo(self):
        res = verificar_resurreccion()
        assert res["sistema_operativo"] is True

    def test_verificar_resurreccion_coherencia_base(self):
        verificar_resurreccion()
        # coherencia_base se calcula tras verificar(eff=0.0)
        res = verificar_resurreccion()
        assert res["coherencia_base"] == pytest.approx(1.0, rel=1e-10)

    def test_activar_laser_noetico_eff_zero(self):
        res = activar_laser_noetico(eff=0.0)
        assert isinstance(res, dict)

    def test_activar_laser_noetico_coherencia_final(self):
        res = activar_laser_noetico(eff=0.0)
        assert res["coherencia_final"] == pytest.approx(1.0, rel=1e-10)

    def test_activar_laser_noetico_estado_general(self):
        res = activar_laser_noetico(eff=0.0)
        assert res["estado_general"] in {
            "RESURRECCIÓN ACTIVA",
            "RESURRECCIÓN PARCIAL",
        }

    def test_activar_laser_eff_positivo_mensaje(self):
        res = activar_laser_noetico(eff=1.0)
        assert "mensaje" in res

    def test_activar_laser_noetico_timestamp_presente(self):
        res = activar_laser_noetico(eff=0.0)
        assert isinstance(res["timestamp"], str)
        assert len(res["timestamp"]) > 5
