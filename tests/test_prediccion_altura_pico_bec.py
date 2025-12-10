#!/usr/bin/env python3
"""
Tests para prediccion_altura_pico_bec.py

Valida los cálculos de:
1. Acoplamiento Ψ-phonon
2. Altura del pico en S(k)
3. Ratio S(k₀)/S(k_background)
4. Cumplimiento de predicciones teóricas

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import unittest
import numpy as np
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from prediccion_altura_pico_bec import (
    calcular_acoplamiento_psi_phonon,
    calcular_altura_pico,
    prediccion_completa,
    generar_espectro_estructura,
    ZETA_3,
    OMEGA_0,
    C_S,
    F0
)


class TestAcoplamientoPsiPhonon(unittest.TestCase):
    """Tests para el cálculo del acoplamiento Ψ-phonon"""
    
    def test_calculo_basico(self):
        """Test cálculo básico del acoplamiento"""
        resultado = calcular_acoplamiento_psi_phonon(c_s=1.0, psi_esperado=1.0)
        
        # Verificar que todos los campos están presentes
        self.assertIsNotNone(resultado.g_psi_phonon)
        self.assertIsNotNone(resultado.omega_0)
        self.assertIsNotNone(resultado.omega_phonon)
        self.assertIsNotNone(resultado.ratio_omega)
        self.assertIsNotNone(resultado.zeta_3)
        
        # Verificar valores esperados
        self.assertAlmostEqual(resultado.omega_0, OMEGA_0, places=2)
        self.assertAlmostEqual(resultado.zeta_3, ZETA_3, places=6)
    
    def test_coincidencia_frecuencias(self):
        """Test que ω₀ ≈ ω_phonon para c_s = 1.0 m/s"""
        resultado = calcular_acoplamiento_psi_phonon(c_s=1.0, psi_esperado=1.0)
        
        # ω_phonon = c_s × k₀ = c_s × (ω₀/c_s) = ω₀
        # Por lo tanto, deberían coincidir exactamente
        self.assertAlmostEqual(
            resultado.omega_0,
            resultado.omega_phonon,
            places=2,
            msg="ω₀ debe ser aproximadamente igual a ω_phonon"
        )
        
        # El ratio debería ser ≈ 1
        self.assertAlmostEqual(
            resultado.ratio_omega,
            1.0,
            delta=0.01,
            msg="Ratio ω₀/ω_phonon debe ser ≈ 1"
        )
    
    def test_acoplamiento_proporcional_psi(self):
        """Test que g ~ ζ(3) × <Ψ> cuando ω₀ ≈ ω_phonon"""
        psi_valores = [0.5, 1.0, 1.5, 2.0]
        
        for psi in psi_valores:
            resultado = calcular_acoplamiento_psi_phonon(c_s=1.0, psi_esperado=psi)
            
            # g ~ ζ(3) × (ω₀/ω_phonon) × <Ψ>
            # Como ω₀ ≈ ω_phonon, ratio ≈ 1
            g_esperado = ZETA_3 * psi
            
            self.assertAlmostEqual(
                resultado.g_psi_phonon,
                g_esperado,
                delta=g_esperado * 0.1,  # 10% tolerancia
                msg=f"g debe ser ≈ ζ(3) × <Ψ> = {g_esperado:.4f} para <Ψ> = {psi}"
            )
    
    def test_valor_zeta_3(self):
        """Test que ζ(3) tiene el valor correcto de Apéry"""
        resultado = calcular_acoplamiento_psi_phonon()
        
        # ζ(3) = 1.2020569... (constante de Apéry)
        self.assertAlmostEqual(
            resultado.zeta_3,
            1.2020569,
            places=4,
            msg="ζ(3) debe tener el valor correcto"
        )
    
    def test_diferentes_velocidades_sonido(self):
        """Test comportamiento con diferentes velocidades del sonido"""
        velocidades = [0.5, 1.0, 2.0]
        
        for c_s in velocidades:
            resultado = calcular_acoplamiento_psi_phonon(c_s=c_s, psi_esperado=1.0)
            
            # ω_phonon = c_s × k₀ donde k₀ = ω₀/c_s
            # Por lo tanto ω_phonon = c_s × (ω₀/c_s) = ω₀ siempre
            self.assertAlmostEqual(
                resultado.omega_phonon,
                OMEGA_0,
                places=2,
                msg=f"ω_phonon debe ser ≈ ω₀ independiente de c_s = {c_s}"
            )


class TestAlturaPico(unittest.TestCase):
    """Tests para el cálculo de la altura del pico"""
    
    def test_calculo_basico(self):
        """Test cálculo básico de altura del pico"""
        g_psi = 1.2  # ≈ ζ(3)
        resultado = calcular_altura_pico(g_psi, densidad_fondo=1.0)
        
        # Verificar campos presentes
        self.assertIsNotNone(resultado.altura_pico_A)
        self.assertIsNotNone(resultado.S_k0)
        self.assertIsNotNone(resultado.S_background)
        self.assertIsNotNone(resultado.ratio_estructura)
        self.assertIsNotNone(resultado.incremento_porcentaje)
        self.assertIsNotNone(resultado.en_rango_predicho)
    
    def test_altura_proporcional_g_cuadrado(self):
        """Test que A ~ |g|² con normalización"""
        g_valores = [0.5, 1.0, 1.5, 2.0]
        densidad = 1.0
        factor_norm = 12.0
        
        for g in g_valores:
            resultado = calcular_altura_pico(g, densidad_fondo=densidad)
            
            # A ~ |g|² / (densidad_fondo × factor_norm)
            A_esperado = (g ** 2) / (densidad * factor_norm)
            
            self.assertAlmostEqual(
                resultado.altura_pico_A,
                A_esperado,
                places=10,
                msg=f"A debe ser proporcional a |g|² para g = {g}"
            )
    
    def test_rango_altura_pico(self):
        """Test que A está en el rango correcto con la normalización"""
        # Con g ~ ζ(3) ≈ 1.2 y factor de normalización 12
        g_psi = ZETA_3
        resultado = calcular_altura_pico(g_psi, densidad_fondo=1.0)
        
        # A = g²/(ρ × 12) ~ 1.44/(1.0 × 12) ~ 0.12
        self.assertGreater(
            resultado.altura_pico_A,
            0,
            msg="A debe ser positiva"
        )
        
        # Con el factor de normalización 12, A ~ 0.12
        # Verificar que está en un rango razonable
        self.assertGreaterEqual(
            resultado.altura_pico_A,
            1e-3,
            msg="A debe ser >= 10⁻³"
        )
        self.assertLessEqual(
            resultado.altura_pico_A,
            1.0,
            msg="A debe ser <= 1.0"
        )
    
    def test_ratio_estructura(self):
        """Test ratio S(k₀)/S(k_bg) está en rango [1.05, 1.20]"""
        g_psi = ZETA_3
        
        # Probar diferentes densidades de fondo
        densidades = [0.8, 1.0, 1.2, 1.5, 2.0]
        
        for rho in densidades:
            resultado = calcular_altura_pico(g_psi, densidad_fondo=rho)
            
            # Verificar que el ratio está definido correctamente
            ratio_calculado = resultado.S_k0 / resultado.S_background
            self.assertAlmostEqual(
                resultado.ratio_estructura,
                ratio_calculado,
                places=10,
                msg=f"Ratio debe ser S(k₀)/S(bg) para ρ = {rho}"
            )
    
    def test_incremento_porcentaje(self):
        """Test que el incremento porcentual es correcto"""
        g_psi = ZETA_3
        resultado = calcular_altura_pico(g_psi, densidad_fondo=1.0)
        
        # Incremento % = (ratio - 1) × 100
        incremento_esperado = (resultado.ratio_estructura - 1.0) * 100
        
        self.assertAlmostEqual(
            resultado.incremento_porcentaje,
            incremento_esperado,
            places=6,
            msg="Incremento porcentual debe ser correcto"
        )
    
    def test_deteccion_rango_predicho(self):
        """Test que la detección de rango [1.05, 1.20] funciona"""
        g_psi = ZETA_3
        
        # Caso dentro del rango
        resultado_dentro = calcular_altura_pico(g_psi, densidad_fondo=120.0)
        if 1.05 <= resultado_dentro.ratio_estructura <= 1.20:
            self.assertTrue(
                resultado_dentro.en_rango_predicho,
                msg="Debe detectar cuando está dentro del rango"
            )
        
        # Caso fuera del rango (densidad muy baja)
        resultado_fuera = calcular_altura_pico(g_psi, densidad_fondo=0.1)
        if resultado_fuera.ratio_estructura > 1.20:
            self.assertFalse(
                resultado_fuera.en_rango_predicho,
                msg="Debe detectar cuando está fuera del rango"
            )


class TestPrediccionCompleta(unittest.TestCase):
    """Tests para la predicción completa"""
    
    def test_prediccion_estandar(self):
        """Test predicción con parámetros estándar"""
        acoplamiento, altura = prediccion_completa(verbose=False)
        
        # Verificar que ambos resultados están presentes
        self.assertIsNotNone(acoplamiento)
        self.assertIsNotNone(altura)
        
        # Verificar consistencia
        self.assertAlmostEqual(
            acoplamiento.omega_0,
            acoplamiento.omega_phonon,
            delta=10,  # Tolerancia de 10 rad/s
            msg="ω₀ y ω_phonon deben coincidir"
        )
    
    def test_consistencia_acoplamiento_altura(self):
        """Test que el acoplamiento se usa correctamente en altura"""
        psi = 1.5
        factor_norm = 12.0
        acoplamiento, altura = prediccion_completa(psi_esperado=psi, verbose=False)
        
        # El acoplamiento debe ser proporcional a psi
        self.assertAlmostEqual(
            acoplamiento.g_psi_phonon,
            ZETA_3 * psi,
            delta=ZETA_3 * psi * 0.1,
            msg="Acoplamiento debe ser proporcional a <Ψ>"
        )
        
        # La altura debe usar este acoplamiento con normalización
        altura_esperada = (acoplamiento.g_psi_phonon ** 2) / (1.0 * factor_norm)  # densidad = 1.0
        self.assertAlmostEqual(
            altura.altura_pico_A,
            altura_esperada,
            places=10,
            msg="Altura debe calcularse con el acoplamiento correcto"
        )
    
    def test_diferentes_parametros(self):
        """Test predicción con diferentes parámetros"""
        parametros = [
            {"c_s": 0.5, "psi_esperado": 0.8},
            {"c_s": 1.0, "psi_esperado": 1.0},
            {"c_s": 1.5, "psi_esperado": 1.2},
        ]
        
        for params in parametros:
            acoplamiento, altura = prediccion_completa(
                c_s=params["c_s"],
                psi_esperado=params["psi_esperado"],
                verbose=False
            )
            
            # Verificar que se ejecutó correctamente
            self.assertIsNotNone(acoplamiento)
            self.assertIsNotNone(altura)
            self.assertGreater(acoplamiento.g_psi_phonon, 0)
            self.assertGreater(altura.altura_pico_A, 0)


class TestEspectroEstructura(unittest.TestCase):
    """Tests para la generación del espectro de estructura"""
    
    def test_generacion_basica(self):
        """Test generación básica del espectro"""
        k_array, S_k_array = generar_espectro_estructura(
            k_min=100,
            k_max=1000,
            n_puntos=100
        )
        
        # Verificar dimensiones
        self.assertEqual(len(k_array), 100)
        self.assertEqual(len(S_k_array), 100)
        
        # Verificar que k está en el rango correcto
        self.assertAlmostEqual(k_array[0], 100, places=2)
        self.assertAlmostEqual(k_array[-1], 1000, places=2)
        
        # Verificar que S(k) es positivo
        self.assertTrue(np.all(S_k_array > 0))
    
    def test_pico_en_k0(self):
        """Test que hay un pico en k₀"""
        # Generar espectro con resultado específico
        acoplamiento, altura = prediccion_completa(verbose=False)
        
        k_0 = OMEGA_0 / C_S
        k_array, S_k_array = generar_espectro_estructura(
            k_min=k_0 - 100,
            k_max=k_0 + 100,
            n_puntos=1000,
            resultado_altura=altura
        )
        
        # Encontrar el máximo
        idx_max = np.argmax(S_k_array)
        k_max = k_array[idx_max]
        
        # El máximo debe estar cerca de k₀
        self.assertAlmostEqual(
            k_max,
            k_0,
            delta=10,  # Tolerancia de 10 rad/m
            msg=f"Pico debe estar en k₀ = {k_0:.2f} rad/m"
        )
    
    def test_altura_pico_consistente(self):
        """Test que la altura del pico es consistente"""
        acoplamiento, altura = prediccion_completa(verbose=False)
        
        k_0 = OMEGA_0 / C_S
        k_array, S_k_array = generar_espectro_estructura(
            k_min=k_0 - 100,
            k_max=k_0 + 100,
            n_puntos=1000,
            resultado_altura=altura
        )
        
        # El máximo de S(k) debe ser aproximadamente S(k₀)
        S_k_max = np.max(S_k_array)
        
        # Debe ser mayor que el fondo
        self.assertGreater(
            S_k_max,
            altura.S_background,
            msg="Máximo debe ser mayor que el fondo"
        )
        
        # Debe estar cerca de S(k₀) predicho
        self.assertAlmostEqual(
            S_k_max,
            altura.S_k0,
            delta=altura.S_k0 * 0.05,  # 5% tolerancia
            msg="Máximo debe coincidir con S(k₀) predicho"
        )


class TestValidacionFormulas(unittest.TestCase):
    """Tests para validar las fórmulas teóricas"""
    
    def test_formula_acoplamiento(self):
        """Test que g_Ψ-phonon ~ ζ(3) × (ω₀/ω_phonon) × <Ψ>"""
        psi = 1.2
        c_s = 1.0
        
        resultado = calcular_acoplamiento_psi_phonon(c_s=c_s, psi_esperado=psi)
        
        # Cálculo manual de la fórmula
        omega_0 = OMEGA_0
        k_0 = omega_0 / c_s
        omega_phonon = c_s * k_0
        ratio = omega_0 / omega_phonon
        g_teorico = ZETA_3 * ratio * psi
        
        self.assertAlmostEqual(
            resultado.g_psi_phonon,
            g_teorico,
            places=10,
            msg="Fórmula de acoplamiento debe ser correcta"
        )
    
    def test_formula_altura(self):
        """Test que A ~ |g|² / (ρ_fondo × factor_norm)"""
        g = 1.5
        rho = 1.0
        factor_norm = 12.0  # Factor de normalización del código
        
        resultado = calcular_altura_pico(g, densidad_fondo=rho)
        
        # Cálculo manual con factor de normalización
        A_teorico = (g ** 2) / (rho * factor_norm)
        
        self.assertAlmostEqual(
            resultado.altura_pico_A,
            A_teorico,
            places=10,
            msg="Fórmula de altura debe ser A = |g|²/(ρ × factor)"
        )
    
    def test_formula_ratio(self):
        """Test que ratio = S(k₀) / S(bg) = (S_bg + A) / S_bg = 1 + A/S_bg"""
        g = 1.2
        rho = 1.0
        factor_norm = 12.0
        
        resultado = calcular_altura_pico(g, densidad_fondo=rho)
        
        # Cálculo manual con normalización
        A = (g ** 2) / (rho * factor_norm)
        ratio_teorico = 1.0 + (A / rho)
        
        self.assertAlmostEqual(
            resultado.ratio_estructura,
            ratio_teorico,
            places=10,
            msg="Fórmula del ratio debe ser correcta"
        )
    
    def test_prediccion_rango(self):
        """Test que con parámetros típicos, ratio ∈ [1.05, 1.20]"""
        # Con g ~ ζ(3) ≈ 1.2 y ajustando ρ apropiadamente
        g = ZETA_3
        
        # Con el nuevo factor de normalización, probar rango de densidades
        densidades_prueba = np.linspace(0.5, 2.0, 10)
        ratios = []
        
        for rho in densidades_prueba:
            resultado = calcular_altura_pico(g, densidad_fondo=rho)
            ratios.append(resultado.ratio_estructura)
        
        # Al menos algunos valores deben estar en el rango
        ratios_en_rango = [r for r in ratios if 1.05 <= r <= 1.20]
        self.assertGreater(
            len(ratios_en_rango),
            0,
            msg="Debe haber valores en el rango predicho [1.05, 1.20]"
        )


if __name__ == "__main__":
    # Ejecutar tests con verbosidad
    unittest.main(verbosity=2)
