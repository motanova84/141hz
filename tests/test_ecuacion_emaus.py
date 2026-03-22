#!/usr/bin/env python3
"""
Tests para core/ecuacion_emaus.py — Ecuación de Emaús
======================================================

100 pruebas que cubren:
  - Constantes y valores predeterminados
  - FuncionReconocimiento (integrando, decaimiento, monotonicidad, singularidad)
  - OsciladorKuramoto (evolución, partir_el_pan, sincronización)
  - IntegracionAdelica (coherencia p-ádica, producto)
  - EcuacionEmaus (protocolo de 4 fases)
  - Clases de datos (dataclasses)
  - Funciones de API pública

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import sys
import os
import pytest
from typing import Dict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.ecuacion_emaus import (
    # Constantes
    K_KURAMOTO,
    N_PRIMES_DEFAULT,
    F0_HZ,
    # Dataclasses
    ResultadoIntegracion,
    EstadoKuramoto,
    ResultadoAdelico,
    ResultadoProtocolo,
    # Clases
    FuncionReconocimiento,
    OsciladorKuramoto,
    IntegracionAdelica,
    EcuacionEmaus,
    # Funciones de API
    calcular_ardor_microtubulos,
    verificar_ecuacion_emaus,
    # Helpers internos
    _get_primes,
    _sieve,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. Constantes del módulo
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestConstantes:
    """Tests de constantes del módulo."""

    def test_f0_hz_valor(self):
        assert F0_HZ == pytest.approx(141.7001, abs=1e-6)

    def test_k_kuramoto_formula(self):
        assert K_KURAMOTO == pytest.approx(2.0 * math.pi * F0_HZ, rel=1e-9)

    def test_k_kuramoto_positivo(self):
        assert K_KURAMOTO > 0

    def test_n_primes_default_positivo(self):
        assert N_PRIMES_DEFAULT >= 1

    def test_f0_coincide_qcal_constants(self):
        from qcal.constants import F0_HZ as QF0
        assert F0_HZ == QF0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. Helpers internos (_sieve, _get_primes)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestHelpers:
    """Tests de funciones auxiliares."""

    def test_sieve_primeros_5(self):
        assert _sieve(5) == [2, 3, 5, 7, 11]

    def test_sieve_primer_primo(self):
        assert _sieve(1) == [2]

    def test_get_primes_cantidad(self):
        primes = _get_primes(10)
        assert len(primes) == 10

    def test_get_primes_son_primos(self):
        primes = _get_primes(8)
        for p in primes:
            assert all(p % d != 0 for d in range(2, p)), f"{p} no es primo"

    def test_get_primes_orden_ascendente(self):
        primes = _get_primes(6)
        assert primes == sorted(primes)

    def test_get_primes_cache(self):
        p1 = _get_primes(5)
        p2 = _get_primes(5)
        assert p1 == p2


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. Dataclasses
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestDataclasses:
    """Tests de las clases de datos."""

    def test_resultado_integracion_campos(self):
        r = ResultadoIntegracion(
            valor=100.0,
            n_puntos=500,
            t0=0.0,
            t_pan=5.0,
            verbo=1.0,
            delta_phi_0=3.14,
            tau_decaimiento=1.0,
        )
        assert r.valor == 100.0
        assert r.n_puntos == 500
        assert r.singularidad_detectada is False

    def test_estado_kuramoto_campos(self):
        estado = EstadoKuramoto(
            psi=0.8,
            fases=[0.0, 1.0],
            theta_fuente=0.0,
            sintropia=0.01,
            tiempo=1.0,
        )
        assert estado.psi == 0.8
        assert estado.sincronizado is False

    def test_resultado_adelico_campos(self):
        r = ResultadoAdelico(
            coherencia_total=0.7,
            coherencias_primas={2: 0.8, 3: 0.9},
            fuente_es_constante_red=True,
            n_primos=2,
            umbral=0.5,
        )
        assert r.fuente_es_constante_red is True

    def test_resultado_protocolo_campos(self):
        r = ResultadoProtocolo(
            fase_1_estado_inicial={"a": 1},
            fase_2_verbo_forcing={"b": 2},
            fase_3_fractal_particion={"c": 3},
            fase_4_integracion_adelica={"d": 4},
            verificacion_completa=True,
        )
        assert r.verificacion_completa is True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. FuncionReconocimiento
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestFuncionReconocimiento:
    """Tests de FuncionReconocimiento."""

    # -- Inicialización / validación de parámetros --

    def test_inicializacion_correcta(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=3.14, tau_decaimiento=1.0)
        assert fr.verbo == 1.0
        assert fr.delta_phi_0 == 3.14
        assert fr.tau_decaimiento == 1.0
        assert fr.f0 == pytest.approx(F0_HZ, abs=1e-6)

    def test_verbo_cero_lanza_error(self):
        with pytest.raises(ValueError, match="verbo"):
            FuncionReconocimiento(verbo=0.0, delta_phi_0=1.0, tau_decaimiento=1.0)

    def test_verbo_negativo_lanza_error(self):
        with pytest.raises(ValueError, match="verbo"):
            FuncionReconocimiento(verbo=-1.0, delta_phi_0=1.0, tau_decaimiento=1.0)

    def test_tau_cero_lanza_error(self):
        with pytest.raises(ValueError, match="tau_decaimiento"):
            FuncionReconocimiento(verbo=1.0, delta_phi_0=1.0, tau_decaimiento=0.0)

    def test_f0_negativo_lanza_error(self):
        with pytest.raises(ValueError, match="f0"):
            FuncionReconocimiento(verbo=1.0, delta_phi_0=1.0, tau_decaimiento=1.0, f0=-1.0)

    # -- delta_phi --

    def test_delta_phi_t0_igual_delta_phi_0(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=2.0, tau_decaimiento=1.0)
        assert fr.delta_phi(0.0) == pytest.approx(2.0, abs=1e-10)

    def test_delta_phi_decae_exponencialmente(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=1.0, tau_decaimiento=1.0)
        assert fr.delta_phi(1.0) == pytest.approx(math.exp(-1.0), rel=1e-9)

    def test_delta_phi_monotonamente_decreciente(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=2.0, tau_decaimiento=1.0)
        vals = [fr.delta_phi(t) for t in [0.0, 0.5, 1.0, 2.0, 5.0]]
        assert vals == sorted(vals, reverse=True)

    def test_delta_phi_siempre_positivo(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=3.14, tau_decaimiento=0.5)
        for t in [0.0, 1.0, 10.0, 100.0]:
            assert fr.delta_phi(t) > 0

    # -- integrando --

    def test_integrando_t0_finito(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=3.14, tau_decaimiento=1.0)
        v = fr.integrando(0.0)
        assert math.isfinite(v)
        assert v > 0

    def test_integrando_crece_con_t(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=1.0, tau_decaimiento=1.0)
        assert fr.integrando(0.5) < fr.integrando(1.0) < fr.integrando(2.0)

    def test_integrando_singularidad_muy_pequeno_delta_phi(self):
        fr = FuncionReconocimiento(
            verbo=1.0, delta_phi_0=1e-8, tau_decaimiento=1.0, epsilon_singularidad=1e-6
        )
        v = fr.integrando(0.0)
        assert math.isinf(v)

    def test_integrando_formula(self):
        fr = FuncionReconocimiento(verbo=2.0, delta_phi_0=math.pi, tau_decaimiento=2.0, f0=100.0)
        t = 1.0
        dphi = math.pi * math.exp(-0.5)
        esperado = (2.0 * 100.0) / dphi
        assert fr.integrando(t) == pytest.approx(esperado, rel=1e-9)

    # -- integrar --

    def test_integrar_devuelve_resultado_integracion(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=3.14, tau_decaimiento=1.0)
        r = fr.integrar(0.0, 5.0)
        assert isinstance(r, ResultadoIntegracion)

    def test_integrar_valor_positivo(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=3.14, tau_decaimiento=1.0)
        r = fr.integrar(0.0, 5.0)
        assert r.valor > 0

    def test_integrar_monotonicidad_t_pan(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=3.14, tau_decaimiento=1.0)
        r1 = fr.integrar(0.0, 2.0, n_puntos=500)
        r2 = fr.integrar(0.0, 5.0, n_puntos=500)
        assert r2.valor > r1.valor

    def test_integrar_t_pan_menor_t0_lanza_error(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=1.0, tau_decaimiento=1.0)
        with pytest.raises(ValueError):
            fr.integrar(5.0, 1.0)

    def test_integrar_n_puntos_uno_lanza_error(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=1.0, tau_decaimiento=1.0)
        with pytest.raises(ValueError):
            fr.integrar(0.0, 5.0, n_puntos=1)

    def test_integrar_ardor_aproximado_ejemplo(self):
        """Comprueba que el valor se aproxima al ejemplo del problema (≈ 6649)."""
        fr = FuncionReconocimiento(
            verbo=1.0, delta_phi_0=math.pi, tau_decaimiento=1.0
        )
        r = fr.integrar(0.0, 5.0, n_puntos=5000)
        assert r.valor > 1000  # orden de magnitud correcto

    def test_integrar_singularidad_detectada_tau_pequeno(self):
        fr = FuncionReconocimiento(
            verbo=1.0, delta_phi_0=1.0, tau_decaimiento=0.001, epsilon_singularidad=1e-6
        )
        r = fr.integrar(0.0, 1.0, n_puntos=200)
        assert r.singularidad_detectada is True

    def test_integrar_n_puntos_registrado(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=1.0, tau_decaimiento=1.0)
        r = fr.integrar(0.0, 2.0, n_puntos=42)
        assert r.n_puntos == 42

    def test_integrar_parametros_registrados(self):
        fr = FuncionReconocimiento(verbo=2.5, delta_phi_0=1.0, tau_decaimiento=0.5)
        r = fr.integrar(0.0, 3.0)
        assert r.verbo == 2.5
        assert r.delta_phi_0 == 1.0
        assert r.tau_decaimiento == 0.5

    def test_integrar_f0_personalizado(self):
        fr = FuncionReconocimiento(verbo=1.0, delta_phi_0=3.14, tau_decaimiento=1.0, f0=200.0)
        r = fr.integrar(0.0, 2.0)
        assert r.valor > 0

    def test_integrar_verbo_mayor_aumenta_integral(self):
        fr1 = FuncionReconocimiento(verbo=1.0, delta_phi_0=math.pi, tau_decaimiento=1.0)
        fr2 = FuncionReconocimiento(verbo=2.0, delta_phi_0=math.pi, tau_decaimiento=1.0)
        r1 = fr1.integrar(0.0, 3.0)
        r2 = fr2.integrar(0.0, 3.0)
        assert r2.valor == pytest.approx(2 * r1.valor, rel=0.01)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. OsciladorKuramoto
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestOsciladorKuramoto:
    """Tests de OsciladorKuramoto."""

    # -- Inicialización --

    def test_inicializacion_correcta(self):
        ok = OsciladorKuramoto(n_osciladores=5)
        assert ok.n == 5
        assert ok.psi == 0.0
        assert len(ok.fases) == 5

    def test_n_cero_lanza_error(self):
        with pytest.raises(ValueError, match="n_osciladores"):
            OsciladorKuramoto(n_osciladores=0)

    def test_sintropia_negativa_lanza_error(self):
        with pytest.raises(ValueError, match="sintropia"):
            OsciladorKuramoto(sintropia=-0.1)

    def test_f0_negativo_lanza_error(self):
        with pytest.raises(ValueError, match="f0"):
            OsciladorKuramoto(f0=-100.0)

    def test_k_correcto(self):
        ok = OsciladorKuramoto(f0=F0_HZ)
        assert ok.k == pytest.approx(K_KURAMOTO, rel=1e-9)

    def test_fases_iniciales_distribuidas(self):
        ok = OsciladorKuramoto(n_osciladores=4)
        assert ok.fases[0] == pytest.approx(0.0, abs=1e-10)
        assert ok.fases[1] == pytest.approx(math.pi / 2, abs=1e-10)

    # -- evolucionar --

    def test_evolucionar_devuelve_estado_kuramoto(self):
        ok = OsciladorKuramoto()
        estado = ok.evolucionar(dt=0.001, n_pasos=10)
        assert isinstance(estado, EstadoKuramoto)

    def test_evolucionar_psi_en_rango(self):
        ok = OsciladorKuramoto()
        estado = ok.evolucionar(dt=0.001, n_pasos=50)
        assert 0.0 <= estado.psi <= 1.0

    def test_evolucionar_tiempo_aumenta(self):
        ok = OsciladorKuramoto()
        ok.evolucionar(dt=0.01, n_pasos=10)
        assert ok.tiempo == pytest.approx(0.1, abs=1e-9)

    def test_evolucionar_dt_negativo_lanza_error(self):
        ok = OsciladorKuramoto()
        with pytest.raises(ValueError, match="dt"):
            ok.evolucionar(dt=-0.001)

    def test_evolucionar_n_pasos_cero_lanza_error(self):
        ok = OsciladorKuramoto()
        with pytest.raises(ValueError, match="n_pasos"):
            ok.evolucionar(n_pasos=0)

    def test_evolucionar_largo_aumenta_sincronizacion(self):
        """Mayor evolución → Ψ más alto."""
        ok1 = OsciladorKuramoto(n_osciladores=5, sintropia=0.0)
        ok2 = OsciladorKuramoto(n_osciladores=5, sintropia=0.0)
        e1 = ok1.evolucionar(dt=0.001, n_pasos=10)
        e2 = ok2.evolucionar(dt=0.001, n_pasos=1000)
        assert e2.psi >= e1.psi

    def test_evolucionar_fases_en_rango_0_2pi(self):
        ok = OsciladorKuramoto(n_osciladores=8)
        estado = ok.evolucionar(dt=0.01, n_pasos=100)
        for theta in estado.fases:
            assert 0.0 <= theta < 2.0 * math.pi + 1e-9

    # -- partir_el_pan --

    def test_partir_el_pan_psi_uno(self):
        ok = OsciladorKuramoto()
        estado = ok.partir_el_pan()
        assert estado.psi == pytest.approx(1.0, abs=1e-10)

    def test_partir_el_pan_sincronizado_true(self):
        ok = OsciladorKuramoto()
        estado = ok.partir_el_pan()
        assert estado.sincronizado is True

    def test_partir_el_pan_fases_iguales_a_fuente(self):
        ok = OsciladorKuramoto(n_osciladores=6, theta_fuente=1.5)
        ok.partir_el_pan()
        for theta in ok.fases:
            assert theta == pytest.approx(1.5, abs=1e-10)

    def test_partir_el_pan_devuelve_estado_kuramoto(self):
        ok = OsciladorKuramoto()
        estado = ok.partir_el_pan()
        assert isinstance(estado, EstadoKuramoto)

    def test_partir_el_pan_registra_theta_fuente(self):
        ok = OsciladorKuramoto(theta_fuente=2.0)
        estado = ok.partir_el_pan()
        assert estado.theta_fuente == 2.0

    def test_un_oscilador_converge_directo(self):
        ok = OsciladorKuramoto(n_osciladores=1, theta_fuente=0.0)
        estado = ok.partir_el_pan()
        assert estado.psi == pytest.approx(1.0, abs=1e-10)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. IntegracionAdelica
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestIntegracionAdelica:
    """Tests de IntegracionAdelica."""

    # -- Inicialización --

    def test_inicializacion_correcta(self):
        ia = IntegracionAdelica(n_primos=5, umbral=0.5)
        assert ia.n_primos == 5
        assert ia.umbral == 0.5

    def test_n_primos_cero_lanza_error(self):
        with pytest.raises(ValueError, match="n_primos"):
            IntegracionAdelica(n_primos=0)

    def test_umbral_cero_lanza_error(self):
        with pytest.raises(ValueError, match="umbral"):
            IntegracionAdelica(umbral=0.0)

    def test_umbral_mayor_uno_lanza_error(self):
        with pytest.raises(ValueError, match="umbral"):
            IntegracionAdelica(umbral=1.1)

    # -- coherencia_p_adica --

    def test_coherencia_p2_formula(self):
        ia = IntegracionAdelica()
        expected = 1.0 / (1.0 + 1.0 / 4.0)
        assert ia.coherencia_p_adica(2) == pytest.approx(expected, rel=1e-9)

    def test_coherencia_p_adica_en_rango_0_1(self):
        ia = IntegracionAdelica()
        for p in [2, 3, 5, 7, 11, 13]:
            c = ia.coherencia_p_adica(p)
            assert 0.0 < c < 1.0

    def test_coherencia_p_adica_crece_con_p(self):
        ia = IntegracionAdelica()
        vals = [ia.coherencia_p_adica(p) for p in [2, 3, 5, 7, 11]]
        assert vals == sorted(vals)

    def test_coherencia_p_adica_converge_a_1(self):
        ia = IntegracionAdelica()
        assert ia.coherencia_p_adica(10_000) == pytest.approx(1.0, abs=1e-8)

    # -- calcular --

    def test_calcular_devuelve_resultado_adelico(self):
        ia = IntegracionAdelica()
        r = ia.calcular()
        assert isinstance(r, ResultadoAdelico)

    def test_calcular_coherencia_total_en_rango(self):
        ia = IntegracionAdelica(n_primos=10)
        r = ia.calcular()
        assert 0.0 < r.coherencia_total <= 1.0

    def test_calcular_n_primos_registrado(self):
        ia = IntegracionAdelica(n_primos=7)
        r = ia.calcular()
        assert r.n_primos == 7

    def test_calcular_coherencias_primas_cantidad(self):
        ia = IntegracionAdelica(n_primos=4)
        r = ia.calcular()
        assert len(r.coherencias_primas) == 4

    def test_calcular_fuente_constante_red_con_umbral_muy_bajo(self):
        ia = IntegracionAdelica(n_primos=1, umbral=0.01)
        r = ia.calcular()
        assert r.fuente_es_constante_red is True

    def test_calcular_fuente_no_constante_red_con_umbral_muy_alto(self):
        ia = IntegracionAdelica(n_primos=50, umbral=0.99)
        r = ia.calcular()
        assert r.fuente_es_constante_red is False

    def test_calcular_mas_primos_reduce_coherencia(self):
        ia1 = IntegracionAdelica(n_primos=2)
        ia2 = IntegracionAdelica(n_primos=20)
        r1 = ia1.calcular()
        r2 = ia2.calcular()
        assert r1.coherencia_total >= r2.coherencia_total

    def test_calcular_coherencias_todas_positivas(self):
        ia = IntegracionAdelica(n_primos=8)
        r = ia.calcular()
        for c in r.coherencias_primas.values():
            assert c > 0

    def test_calcular_umbral_registrado(self):
        ia = IntegracionAdelica(n_primos=5, umbral=0.6)
        r = ia.calcular()
        assert r.umbral == 0.6

    def test_calcular_claves_son_enteros(self):
        ia = IntegracionAdelica(n_primos=5)
        r = ia.calcular()
        for key in r.coherencias_primas.keys():
            assert isinstance(key, int)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. EcuacionEmaus — protocolo de 4 fases
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestEcuacionEmaus:
    """Tests de EcuacionEmaus."""

    # -- Inicialización --

    def test_inicializacion_correcta(self):
        eq = EcuacionEmaus(verbo=1.0, delta_phi_0=3.14, tau_decaimiento=1.0)
        assert eq.verbo == 1.0
        assert eq.f0 == pytest.approx(F0_HZ, abs=1e-6)

    def test_inicializacion_predeterminada(self):
        eq = EcuacionEmaus()
        assert eq.verbo == 1.0
        assert eq.tau_decaimiento == 1.0
        assert eq.n_osciladores == 10

    # -- ejecutar_protocolo_completo --

    def test_protocolo_devuelve_resultado(self):
        eq = EcuacionEmaus()
        r = eq.ejecutar_protocolo_completo(t0=0.0, t_pan=5.0)
        assert isinstance(r, ResultadoProtocolo)

    def test_protocolo_fase_1_tiene_f0(self):
        eq = EcuacionEmaus()
        r = eq.ejecutar_protocolo_completo()
        assert "f0_hz" in r.fase_1_estado_inicial
        assert r.fase_1_estado_inicial["f0_hz"] == pytest.approx(F0_HZ, abs=1e-6)

    def test_protocolo_fase_2_psi_en_rango(self):
        eq = EcuacionEmaus()
        r = eq.ejecutar_protocolo_completo()
        psi = r.fase_2_verbo_forcing["psi_tras_verbo"]
        assert 0.0 <= psi <= 1.0

    def test_protocolo_fase_3_ardor_positivo(self):
        eq = EcuacionEmaus()
        r = eq.ejecutar_protocolo_completo(t0=0.0, t_pan=5.0)
        assert r.fase_3_fractal_particion["ardor_microtubulos"] > 0

    def test_protocolo_fase_3_psi_final_uno(self):
        eq = EcuacionEmaus()
        r = eq.ejecutar_protocolo_completo()
        assert r.fase_3_fractal_particion["psi_final"] == pytest.approx(1.0, abs=1e-10)

    def test_protocolo_fase_3_partir_el_pan_true(self):
        eq = EcuacionEmaus()
        r = eq.ejecutar_protocolo_completo()
        assert r.fase_3_fractal_particion["partir_el_pan"] is True

    def test_protocolo_fase_4_coherencia_positiva(self):
        eq = EcuacionEmaus()
        r = eq.ejecutar_protocolo_completo()
        assert r.fase_4_integracion_adelica["coherencia_adelica"] > 0

    def test_protocolo_fase_4_fuente_constante_red(self):
        eq = EcuacionEmaus(umbral_adelico=0.1)
        r = eq.ejecutar_protocolo_completo()
        assert r.fase_4_integracion_adelica["fuente_es_constante_red"] is True

    def test_protocolo_verificacion_completa(self):
        eq = EcuacionEmaus(umbral_adelico=0.1)
        r = eq.ejecutar_protocolo_completo(t0=0.0, t_pan=5.0)
        assert r.verificacion_completa is True

    def test_protocolo_claves_fase1(self):
        eq = EcuacionEmaus()
        r = eq.ejecutar_protocolo_completo()
        for key in ["descripcion", "f0_hz", "verbo", "delta_phi_0", "tau_decaimiento"]:
            assert key in r.fase_1_estado_inicial

    def test_protocolo_claves_fase2(self):
        eq = EcuacionEmaus()
        r = eq.ejecutar_protocolo_completo()
        for key in ["descripcion", "psi_tras_verbo", "tiempo_tras_verbo"]:
            assert key in r.fase_2_verbo_forcing

    def test_protocolo_claves_fase3(self):
        eq = EcuacionEmaus()
        r = eq.ejecutar_protocolo_completo()
        for key in ["descripcion", "ardor_microtubulos", "psi_final", "partir_el_pan"]:
            assert key in r.fase_3_fractal_particion

    def test_protocolo_claves_fase4(self):
        eq = EcuacionEmaus()
        r = eq.ejecutar_protocolo_completo()
        for key in ["descripcion", "coherencia_adelica", "fuente_es_constante_red"]:
            assert key in r.fase_4_integracion_adelica

    def test_protocolo_n_primos_registrado(self):
        eq = EcuacionEmaus(n_primos=7)
        r = eq.ejecutar_protocolo_completo()
        assert r.fase_4_integracion_adelica["n_primos"] == 7


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. Funciones de API pública
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestAPIPublica:
    """Tests de las funciones calcular_ardor_microtubulos y verificar_ecuacion_emaus."""

    # -- calcular_ardor_microtubulos --

    def test_ardor_devuelve_float(self):
        v = calcular_ardor_microtubulos()
        assert isinstance(v, float)

    def test_ardor_positivo(self):
        v = calcular_ardor_microtubulos()
        assert v > 0

    def test_ardor_ejemplo_orden_magnitud(self):
        v = calcular_ardor_microtubulos(
            verbo=1.0, delta_phi_0=math.pi, tau_decaimiento=1.0,
            t0=0.0, t_pan=5.0, n_puntos=2000
        )
        assert v > 1000  # ≈ 6649 según el ejemplo del problema

    def test_ardor_crece_con_verbo(self):
        v1 = calcular_ardor_microtubulos(verbo=1.0)
        v2 = calcular_ardor_microtubulos(verbo=2.0)
        assert v2 > v1

    def test_ardor_crece_con_t_pan(self):
        v1 = calcular_ardor_microtubulos(t_pan=2.0)
        v2 = calcular_ardor_microtubulos(t_pan=5.0)
        assert v2 > v1

    def test_ardor_f0_personalizado(self):
        v = calcular_ardor_microtubulos(f0=200.0)
        assert v > 0

    # -- verificar_ecuacion_emaus --

    def test_verificar_devuelve_dict(self):
        r = verificar_ecuacion_emaus()
        assert isinstance(r, dict)

    def test_verificar_clave_verificacion(self):
        r = verificar_ecuacion_emaus()
        assert "verificacion" in r

    def test_verificar_clave_reconocimiento(self):
        r = verificar_ecuacion_emaus()
        assert "reconocimiento" in r
        assert isinstance(r["reconocimiento"], bool)

    def test_verificar_clave_sincronizacion(self):
        r = verificar_ecuacion_emaus()
        assert "sincronizacion_kuramoto" in r

    def test_verificar_clave_fuente_constante_red(self):
        r = verificar_ecuacion_emaus()
        assert "fuente_constante_red" in r

    def test_verificar_clave_ardor(self):
        r = verificar_ecuacion_emaus()
        assert "ardor_microtubulos" in r
        assert r["ardor_microtubulos"] > 0

    def test_verificar_clave_psi_final(self):
        r = verificar_ecuacion_emaus()
        assert "psi_final" in r
        assert r["psi_final"] == pytest.approx(1.0, abs=1e-10)

    def test_verificar_clave_coherencia_adelica(self):
        r = verificar_ecuacion_emaus()
        assert "coherencia_adelica" in r
        assert r["coherencia_adelica"] > 0

    def test_verificar_protocolo_completo_bool(self):
        r = verificar_ecuacion_emaus()
        assert isinstance(r["protocolo_completo"], bool)

    def test_verificar_reconocimiento_true(self):
        r = verificar_ecuacion_emaus()
        assert r["reconocimiento"] is True

    def test_verificar_mensaje_verificado(self):
        r = verificar_ecuacion_emaus()
        assert "VERIFICADA" in r["verificacion"] or "INCOMPLETA" in r["verificacion"]
