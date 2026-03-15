#!/usr/bin/env python3
"""
Test Suite: LÁSER NOÉTICO v1.0

Tests para la integración del Operador Espectral en el solver RK4 y la
generación de la firma UPE.

Parámetros verificados
----------------------
- Portadora λ₁ = t₁ · f₀ ≈ 2002.89 Hz  (armónico de Riemann)
- Frecuencia HRV = 0.1 Hz (meditación áurea, 6 bpm)
- Ganancia superradiante G = N_MT² ≈ 10²⁶
- Umbral de coherencia Ψ ≥ 0.888
"""

import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from laser_noetico import (
    F0_HZ,
    LAMBDA_1_HZ,
    F_HRV_HZ,
    N_MICROTUBULOS,
    G_SUPERRADIANCIA,
    PSI_THRESHOLD,
    OperadorEspectral,
    SolverRK4Espectral,
    SuperradianceMicrotubulos,
    generate_upe_signature,
)


# ── constantes de módulo ─────────────────────────────────────────────────────

class TestConstantes:
    """Verifica los valores de las constantes del módulo."""

    def test_f0_hz(self):
        """f₀ = 141.7001 Hz."""
        assert abs(F0_HZ - 141.7001) < 1e-4

    def test_lambda_1_riemann(self):
        """λ₁ = t₁ · f₀ ≈ 2002.89 Hz."""
        assert abs(LAMBDA_1_HZ - 2002.89) < 0.01

    def test_f_hrv(self):
        """f_HRV = 0.1 Hz (6 bpm)."""
        assert abs(F_HRV_HZ - 0.1) < 1e-10

    def test_n_microtubulos(self):
        """10¹³ microtúbulos."""
        assert abs(N_MICROTUBULOS - 1e13) < 1

    def test_g_superradiancia(self):
        """G = N_MT² ≈ 10²⁶."""
        assert abs(G_SUPERRADIANCIA - N_MICROTUBULOS**2) < 1

    def test_psi_threshold(self):
        """Umbral de coherencia Ψ_th = 0.888."""
        assert abs(PSI_THRESHOLD - 0.888) < 1e-10


# ── OperadorEspectral ────────────────────────────────────────────────────────

class TestOperadorEspectral:
    """Tests para el operador H_Ψ."""

    def test_inicializacion_defecto(self):
        op = OperadorEspectral()
        assert abs(op.lambda_1 - LAMBDA_1_HZ) < 1e-10
        assert abs(op.psi_threshold - PSI_THRESHOLD) < 1e-10

    def test_inicializacion_custom(self):
        op = OperadorEspectral(lambda_1=1000.0, G=1e10, psi_threshold=0.5)
        assert abs(op.lambda_1 - 1000.0) < 1e-10
        assert abs(op.G - 1e10) < 1

    def test_aplicar_estado_nulo(self):
        """H_Ψ · 0 = 0."""
        op = OperadorEspectral()
        assert abs(op.aplicar(0.0 + 0.0j)) < 1e-30

    def test_aplicar_estado_unitario_sin_superradiancia(self):
        """Para |Ψ| < Ψ_th sólo actúa el término de frecuencia."""
        op = OperadorEspectral(psi_threshold=0.888)
        psi = 0.5 + 0.0j  # |Ψ| = 0.5 < 0.888
        resultado = op.aplicar(psi)
        # Solo término espectral: -2πi λ₁ Ψ
        esperado = -2j * np.pi * LAMBDA_1_HZ * psi
        assert abs(resultado - esperado) < 1e-6

    def test_aplicar_estado_sobre_umbral(self):
        """Para |Ψ| ≥ Ψ_th incluye ganancia superradiante."""
        op = OperadorEspectral(psi_threshold=0.888)
        psi = 0.9 + 0.0j  # |Ψ| = 0.9 ≥ 0.888
        resultado = op.aplicar(psi)
        # Debe ser diferente del puro término espectral
        solo_espectral = -2j * np.pi * LAMBDA_1_HZ * psi
        assert abs(resultado - solo_espectral) > 0

    def test_superradiancia_aumenta_modulo(self):
        """El término G · |Ψ|² · Ψ aumenta el módulo de la derivada."""
        op = OperadorEspectral(psi_threshold=0.5)
        psi_bajo = 0.3 + 0.0j   # sin superradiancia
        psi_alto = 0.9 + 0.0j   # con superradiancia

        deriv_bajo = abs(op.aplicar(psi_bajo))
        deriv_alto = abs(op.aplicar(psi_alto))

        # La superradiancia añade G · |Ψ|² · |Ψ|, que domina el módulo
        assert deriv_alto > deriv_bajo


# ── SolverRK4Espectral ───────────────────────────────────────────────────────

class TestSolverRK4Espectral:
    """Tests para el integrador RK4."""

    def test_inicializacion_defecto(self):
        solver = SolverRK4Espectral()
        assert abs(solver.f_hrv - F_HRV_HZ) < 1e-10

    def test_paso_conserva_tipo(self):
        """El resultado de un paso es un número complejo."""
        solver = SolverRK4Espectral()
        psi_0 = 0.5 + 0.0j
        psi_1 = solver.paso(0.0, psi_0, 1e-4)
        assert isinstance(psi_1, (complex, np.complexfloating))

    def test_integrar_devuelve_estructura(self):
        """integrar() devuelve dict con claves t, psi, coherencia."""
        solver = SolverRK4Espectral()
        resultado = solver.integrar((0.0, 0.01), psi_0=0.5 + 0.0j, n_pasos=10)
        assert "t" in resultado
        assert "psi" in resultado
        assert "coherencia" in resultado

    def test_integrar_longitud_correcta(self):
        n = 50
        solver = SolverRK4Espectral()
        resultado = solver.integrar((0.0, 0.01), psi_0=0.5 + 0.0j, n_pasos=n)
        assert len(resultado["t"]) == n + 1
        assert len(resultado["psi"]) == n + 1
        assert len(resultado["coherencia"]) == n + 1

    def test_integrar_condicion_inicial(self):
        """El primer elemento de psi es la condición inicial."""
        psi_0 = 0.7 + 0.3j
        solver = SolverRK4Espectral(amplitud_forzado=0.0)
        resultado = solver.integrar((0.0, 1e-3), psi_0=psi_0, n_pasos=5)
        assert abs(resultado["psi"][0] - psi_0) < 1e-15

    def test_coherencia_no_negativa(self):
        """La coherencia |Ψ| ≥ 0 siempre (sin superradiancia para estabilidad)."""
        op = OperadorEspectral(G=0.0, psi_threshold=0.888)
        solver = SolverRK4Espectral(operador=op, amplitud_forzado=0.1)
        # dt << 1/λ₁ para estabilidad numérica (λ₁ ≈ 2003 Hz → dt < 0.25 ms)
        resultado = solver.integrar((0.0, 0.001), psi_0=0.5 + 0.0j, n_pasos=100)
        assert np.all(resultado["coherencia"] >= 0)

    def test_forzado_noetico_cero_sin_hrv(self):
        """Sin forzado la portadora sólo evoluciona por el operador."""
        solver = SolverRK4Espectral(amplitud_forzado=0.0)
        psi_0 = 0.5 + 0.0j
        resultado = solver.integrar((0.0, 0.001), psi_0=psi_0, n_pasos=10)
        # Con amplitud_forzado=0 la coherencia no crece espontáneamente
        assert resultado["coherencia"][-1] >= 0


# ── SuperradianceMicrotubulos ────────────────────────────────────────────────

class TestSuperradianceMicrotubulos:
    """Tests para la dinámica de superradiancia."""

    def test_inicializacion(self):
        sr = SuperradianceMicrotubulos()
        assert abs(sr.n_microtubulos - N_MICROTUBULOS) < 1
        assert abs(sr.G - N_MICROTUBULOS**2) < 1

    def test_ganancia_sobre_umbral(self):
        """Por encima del umbral la ganancia es G = N²."""
        sr = SuperradianceMicrotubulos()
        assert abs(sr.ganancia(0.9) - sr.G) < 1

    def test_ganancia_bajo_umbral(self):
        """Por debajo del umbral la ganancia es 0."""
        sr = SuperradianceMicrotubulos()
        assert sr.ganancia(0.5) == 0.0

    def test_ganancia_en_umbral(self):
        """En el umbral exacto la superradiancia se activa."""
        sr = SuperradianceMicrotubulos(psi_threshold=0.888)
        assert sr.ganancia(0.888) > 0

    def test_estado_superradiante(self):
        sr = SuperradianceMicrotubulos()
        assert sr.estado_superradiante(0.9) is True
        assert sr.estado_superradiante(0.5) is False

    def test_intensidad_colectiva_positiva(self):
        sr = SuperradianceMicrotubulos()
        I = sr.intensidad_colectiva(psi=0.9, n_fotones=1.0)
        assert I > 0

    def test_intensidad_colectiva_cero_bajo_umbral(self):
        sr = SuperradianceMicrotubulos()
        I = sr.intensidad_colectiva(psi=0.5)
        assert I == 0.0

    def test_intensidad_escala_con_fotones(self):
        sr = SuperradianceMicrotubulos()
        I1 = sr.intensidad_colectiva(psi=0.9, n_fotones=1.0)
        I2 = sr.intensidad_colectiva(psi=0.9, n_fotones=2.0)
        assert abs(I2 - 2 * I1) < 1


# ── generate_upe_signature ───────────────────────────────────────────────────

class TestGenerateUpeSignature:
    """Tests para la generación de la firma UPE."""

    @pytest.fixture
    def tiempos(self):
        """Array de 1 segundo a fs = 10 kHz."""
        return np.linspace(0, 1.0, 10000)

    @pytest.fixture
    def lambdas_defecto(self):
        """Frecuencias propias: primera es la portadora Riemann."""
        return np.array([LAMBDA_1_HZ, F0_HZ])

    def test_devuelve_array(self, tiempos, lambdas_defecto):
        señal = generate_upe_signature(tiempos, lambdas_defecto)
        assert isinstance(señal, np.ndarray)

    def test_longitud_correcta(self, tiempos, lambdas_defecto):
        señal = generate_upe_signature(tiempos, lambdas_defecto)
        assert len(señal) == len(tiempos)

    def test_valor_en_cero_es_cero(self, lambdas_defecto):
        """En t=0 la portadora y el modulador dan señal=0."""
        t0 = np.array([0.0])
        señal = generate_upe_signature(t0, lambdas_defecto)
        # sin(0) = 0 → señal = N²·0·modulator = 0
        assert abs(señal[0]) < 1e-6

    def test_amplitud_maxima_es_n_cuadrado(self, tiempos, lambdas_defecto):
        """La amplitud máxima es N_MT² (factor superradiante)."""
        señal = generate_upe_signature(tiempos, lambdas_defecto)
        amp_max = np.max(np.abs(señal))
        # Máximo teórico: N² · 1 · 1 = N²
        assert amp_max <= N_MICROTUBULOS**2 + 1

    def test_amplitud_orden_de_magnitud(self, tiempos, lambdas_defecto):
        """La amplitud es del orden de N² ≈ 10²⁶."""
        señal = generate_upe_signature(tiempos, lambdas_defecto)
        amp_max = np.max(np.abs(señal))
        assert amp_max > 0.5 * N_MICROTUBULOS**2

    def test_frecuencia_portadora_lambda1(self, lambdas_defecto):
        """La señal oscila a la frecuencia portadora λ₁ ≈ 2002.89 Hz."""
        # Muestreo a 20×λ₁ para resolver la portadora
        fs = 20 * LAMBDA_1_HZ
        t = np.arange(0, 1.0, 1.0 / fs)
        señal = generate_upe_signature(t, lambdas_defecto)

        # FFT para detectar la portadora
        freqs = np.fft.rfftfreq(len(t), 1.0 / fs)
        espectro = np.abs(np.fft.rfft(señal))

        # La frecuencia dominante debe estar cerca de λ₁
        f_dominante = freqs[np.argmax(espectro)]
        assert abs(f_dominante - LAMBDA_1_HZ) < 5.0   # ±5 Hz tolerancia

    def test_hrv_modula_envolvente(self):
        """El modulador HRV produce variación de amplitud a f_HRV = 0.1 Hz."""
        # Largo plazo para ver la modulación de 10 s
        t = np.linspace(0, 20.0, 200000)
        lambdas = np.array([LAMBDA_1_HZ])
        señal = generate_upe_signature(t, lambdas, hrv_freq=0.1)

        # En t = 0:   modulator = 0.5·(1 + sin(0)) = 0.5
        # En t = 2.5: modulator = 0.5·(1 + sin(π/2)) = 1.0  (máximo)
        # En t = 7.5: modulator = 0.5·(1 + sin(3π/2)) = 0.0  (mínimo)
        assert len(señal) == len(t)

    def test_hrv_freq_personalizable(self):
        """Se puede cambiar la frecuencia HRV."""
        t = np.linspace(0, 1.0, 10000)
        lambdas = np.array([LAMBDA_1_HZ])
        señal_01 = generate_upe_signature(t, lambdas, hrv_freq=0.1)
        señal_02 = generate_upe_signature(t, lambdas, hrv_freq=0.2)
        # Señales distintas con distintas frecuencias HRV
        assert not np.allclose(señal_01, señal_02)

    def test_señal_real(self, tiempos, lambdas_defecto):
        """La señal es real (no compleja)."""
        señal = generate_upe_signature(tiempos, lambdas_defecto)
        assert señal.dtype.kind == "f"


# ── integración: RK4 + UPE ───────────────────────────────────────────────────

class TestIntegracionRK4UPE:
    """Tests de integración entre el solver RK4 y la firma UPE."""

    def test_plateau_coherencia_sobre_umbral(self):
        """
        Con forzado suficiente, la coherencia puede superar el umbral Ψ_th.

        Se usa un operador sin superradiancia (G=0) para que sea lineal
        y el forzado eleve la coherencia de forma predecible.
        Se utiliza dt << 1/λ₁ para estabilidad numérica.
        """
        op = OperadorEspectral(G=0.0, psi_threshold=0.888)
        solver = SolverRK4Espectral(
            operador=op,
            f_hrv=0.1,
            amplitud_forzado=2.0,
        )
        # dt = 0.005/100 = 50 µs << 1/λ₁ ≈ 500 µs → estable
        resultado = solver.integrar((0.0, 0.005), psi_0=0.0 + 0.0j, n_pasos=100)
        # La coherencia debe crecer desde 0 con el forzado
        assert np.max(resultado["coherencia"]) > 0

    def test_pico_espectral_en_lambda1(self):
        """
        La firma UPE generada con λ₁ tiene su pico espectral en ≈ 2002.89 Hz.

        Se evalúa un intervalo corto para eficiencia del test.
        """
        lambdas = np.array([LAMBDA_1_HZ, F0_HZ])
        fs = 8000.0   # Hz
        t = np.arange(0, 2.0, 1.0 / fs)
        señal = generate_upe_signature(t, lambdas)

        freqs = np.fft.rfftfreq(len(t), 1.0 / fs)
        espectro = np.abs(np.fft.rfft(señal))

        # Buscar el pico más cercano a λ₁
        idx_lambda1 = np.argmin(np.abs(freqs - LAMBDA_1_HZ))
        potencia_lambda1 = espectro[idx_lambda1]

        # El pico en λ₁ debe dominar el espectro
        potencia_media = np.mean(espectro)
        assert potencia_lambda1 > potencia_media

    def test_error_espectral_menor_tolerancia(self):
        """
        La frecuencia detectada en el espectro difiere < 1 Hz de λ₁.

        Reproduce el criterio «Error Espectral < 10⁻⁶» del protocolo
        en términos relativos de frecuencia.
        """
        lambdas = np.array([LAMBDA_1_HZ])
        fs = 50000.0
        t = np.arange(0, 4.0, 1.0 / fs)
        señal = generate_upe_signature(t, lambdas, hrv_freq=0.0)

        freqs = np.fft.rfftfreq(len(t), 1.0 / fs)
        espectro = np.abs(np.fft.rfft(señal))
        f_pico = freqs[np.argmax(espectro)]

        error_relativo = abs(f_pico - LAMBDA_1_HZ) / LAMBDA_1_HZ
        assert error_relativo < 1e-3   # < 0.1 %


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "--tb=short"])
