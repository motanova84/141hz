#!/usr/bin/env python3
"""
Tests para el Axioma de la Masa Noética.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Sistema QCAL ∞³
Fecha: Febrero 2026
"""

import sys
import os
import pytest
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.masa_noetica import (
    MasaNoetica,
    h, c, eV,
    F0_HZ, M_QCAL_KG, E_QCAL_J,
    calcular_masa_qcal,
    validar_consistencia_dimensional,
    comparar_con_particulas_conocidas
)


class TestMasaQCAL:
    """Tests para la masa QCAL fundamental."""
    
    def test_calculo_masa_qcal(self):
        """Test cálculo de masa QCAL."""
        m_kg, m_eV = calcular_masa_qcal(F0_HZ)
        
        # Verificar valor esperado
        esperado_kg = (h * F0_HZ) / (c ** 2)
        assert abs(m_kg - esperado_kg) < 1e-60
        
        # Verificar conversión a eV
        esperado_eV = m_kg / eV
        assert abs(m_eV - esperado_eV) < 1e-70
        
    def test_constantes_globales(self):
        """Test constantes globales están definidas correctamente."""
        assert M_QCAL_KG > 0
        assert E_QCAL_J > 0
        # Usar tolerancia relativa apropiada para floating point
        assert abs(E_QCAL_J - M_QCAL_KG * c**2) / E_QCAL_J < 1e-10
        
    def test_orden_magnitud_masa_qcal(self):
        """Test orden de magnitud de m_QCAL."""
        # m_QCAL debe estar en el rango 1e-50 a 1e-46 kg
        assert 1e-50 < M_QCAL_KG < 1e-46
        
    def test_consistencia_dimensional(self):
        """Test consistencia dimensional."""
        validaciones = validar_consistencia_dimensional()
        
        # Todas las validaciones deben ser True
        assert all(validaciones.values())


class TestMasaNoetica:
    """Tests para la clase MasaNoetica."""
    
    @pytest.fixture
    def masa_noetica(self):
        """Fixture para crear instancia de MasaNoetica."""
        return MasaNoetica(f0=F0_HZ)
    
    def test_inicializacion(self, masa_noetica):
        """Test inicialización correcta."""
        assert masa_noetica.f0 == F0_HZ
        assert masa_noetica.m_qcal == M_QCAL_KG
        assert masa_noetica.E_qcal == E_QCAL_J
        
    def test_masa_einstein_planck(self, masa_noetica):
        """Test perspectiva Einstein-Planck: m ∝ f."""
        f1 = 100.0
        f2 = 200.0
        
        m1 = masa_noetica.masa_einstein_planck(f1)
        m2 = masa_noetica.masa_einstein_planck(f2)
        
        # m ∝ f → m2/m1 = f2/f1
        razon_masas = m2 / m1
        razon_frecuencias = f2 / f1
        
        assert abs(razon_masas - razon_frecuencias) < 1e-10
        
    def test_masa_noetica_inversa(self, masa_noetica):
        """Test perspectiva noética: m ∝ 1/f."""
        f1 = 100.0
        f2 = 200.0
        
        m1 = masa_noetica.masa_noetica_inversa(f1)
        m2 = masa_noetica.masa_noetica_inversa(f2)
        
        # m ∝ 1/f → m2/m1 = f1/f2
        razon_masas = m2 / m1
        razon_frecuencias_inv = f1 / f2
        
        assert abs(razon_masas - razon_frecuencias_inv) < 1e-10
        
    def test_masa_noetica_inversa_f0(self, masa_noetica):
        """Test masa noética en f₀."""
        m = masa_noetica.masa_noetica_inversa(F0_HZ)
        
        # En f₀, m_noesis = m_QCAL
        assert abs(m - M_QCAL_KG) < 1e-60
        
    def test_masa_noetica_inversa_frecuencia_negativa(self, masa_noetica):
        """Test error con frecuencia negativa."""
        with pytest.raises(ValueError):
            masa_noetica.masa_noetica_inversa(-1.0)
            
    def test_masa_noetica_inversa_frecuencia_cero(self, masa_noetica):
        """Test error con frecuencia cero."""
        with pytest.raises(ValueError):
            masa_noetica.masa_noetica_inversa(0.0)
        
    def test_masa_unificada_constante(self, masa_noetica):
        """Test masa unificada es constante."""
        frecuencias = np.logspace(-5, 20, 100)
        
        masas = [masa_noetica.masa_unificada(f) for f in frecuencias]
        
        # Todas las masas deben ser iguales a m_QCAL
        for m in masas:
            assert abs(m - M_QCAL_KG) < 1e-60
            
    def test_masa_unificada_sin_frecuencia(self, masa_noetica):
        """Test masa unificada sin parámetro de frecuencia."""
        m = masa_noetica.masa_unificada()
        
        assert abs(m - M_QCAL_KG) < 1e-60


class TestDualidad:
    """Tests para la dualidad masa-frecuencia."""
    
    @pytest.fixture
    def masa_noetica(self):
        """Fixture para crear instancia de MasaNoetica."""
        return MasaNoetica(f0=F0_HZ)
    
    def test_convergencia_en_f0(self, masa_noetica):
        """Test que las tres perspectivas convergen en f₀."""
        m_einstein = masa_noetica.masa_einstein_planck(F0_HZ)
        m_noesis = masa_noetica.masa_noetica_inversa(F0_HZ)
        m_unificada = masa_noetica.masa_unificada(F0_HZ)
        
        # Las tres deben ser iguales a m_QCAL
        assert abs(m_einstein - M_QCAL_KG) < 1e-60
        assert abs(m_noesis - M_QCAL_KG) < 1e-60
        assert abs(m_unificada - M_QCAL_KG) < 1e-60
        
    def test_tendencias_opuestas(self, masa_noetica):
        """Test tendencias opuestas lejos de f₀."""
        # Alta frecuencia
        f_alta = F0_HZ * 1e6
        m_einstein_alta = masa_noetica.masa_einstein_planck(f_alta)
        m_noesis_alta = masa_noetica.masa_noetica_inversa(f_alta)
        
        # Baja frecuencia
        f_baja = F0_HZ * 1e-6
        m_einstein_baja = masa_noetica.masa_einstein_planck(f_baja)
        m_noesis_baja = masa_noetica.masa_noetica_inversa(f_baja)
        
        # Einstein: m aumenta con f
        assert m_einstein_alta > m_einstein_baja
        
        # Noesis: m disminuye con f
        assert m_noesis_alta < m_noesis_baja
        
    def test_analizar_dualidad(self, masa_noetica):
        """Test análisis de dualidad completo."""
        analisis = masa_noetica.analizar_dualidad(F0_HZ)
        
        # Verificar estructura del resultado
        assert 'frecuencia_hz' in analisis
        assert 'perspectivas' in analisis
        assert 'razones' in analisis
        
        # Verificar perspectivas
        perspectivas = analisis['perspectivas']
        assert 'einstein_planck' in perspectivas
        assert 'noetica' in perspectivas
        assert 'unificada_qcal' in perspectivas
        
        # En f₀, todas las masas deben ser iguales
        m_einstein = perspectivas['einstein_planck']['masa_kg']
        m_noesis = perspectivas['noetica']['masa_kg']
        m_unificada = perspectivas['unificada_qcal']['masa_kg']
        
        assert abs(m_einstein - m_noesis) < 1e-60
        assert abs(m_einstein - m_unificada) < 1e-60


class TestInterpretaciones:
    """Tests para interpretaciones físicas."""
    
    @pytest.fixture
    def masa_noetica(self):
        """Fixture para crear instancia de MasaNoetica."""
        return MasaNoetica(f0=F0_HZ)
    
    def test_interpretar_particula_fotonica(self, masa_noetica):
        """Test interpretación de fotón (alta frecuencia)."""
        f_luz = 5e14  # Hz (luz visible)
        
        interp = masa_noetica.interpretar_particula(f_luz)
        
        assert interp['tipo'] == "Fotónica"
        assert interp['frecuencia_hz'] == f_luz
        assert interp['razon_f_f0'] > 1e12  # f >> f₀
        
        # Masa noética debe ser muy pequeña
        assert interp['masa_noesis_kg'] < M_QCAL_KG
        
    def test_interpretar_particula_coherencia_primordial(self, masa_noetica):
        """Test interpretación en f₀."""
        interp = masa_noetica.interpretar_particula(F0_HZ)
        
        assert interp['tipo'] == "Coherencia primordial"
        assert abs(interp['razon_f_f0'] - 1.0) < 0.01
        
    def test_interpretar_particula_baja_frecuencia(self, masa_noetica):
        """Test interpretación a baja frecuencia."""
        f_baja = 1.0  # Hz
        
        interp = masa_noetica.interpretar_particula(f_baja)
        
        assert interp['tipo'] == "Vibracional lenta"
        assert interp['razon_f_f0'] < 1.0
        
        # Masa noética debe ser mayor que m_QCAL
        assert interp['masa_noesis_kg'] > M_QCAL_KG
        
    def test_gravedad_emergente(self, masa_noetica):
        """Test gravedad emergente."""
        # Alta frecuencia: sin gravedad
        f_alta = 1e15
        grav_alta = masa_noetica.gravedad_emergente(f_alta)
        
        assert grav_alta['factor_ralentizacion'] == 1.0
        assert grav_alta['intensidad_gravitacional_relativa'] == 0.0
        
        # Baja frecuencia: gravedad emergente
        f_baja = 1.0
        grav_baja = masa_noetica.gravedad_emergente(f_baja)
        
        assert grav_baja['factor_ralentizacion'] > 1.0
        assert grav_baja['intensidad_gravitacional_relativa'] > 0.0


class TestComparacionesParticulas:
    """Tests para comparaciones con partículas conocidas."""
    
    def test_comparar_con_particulas(self):
        """Test comparación con partículas del modelo estándar."""
        comparaciones = comparar_con_particulas_conocidas()
        
        # Verificar que m_qcal está en las comparaciones
        assert 'm_qcal' in comparaciones
        
        # Verificar estructura de datos
        for particula, datos in comparaciones.items():
            if particula == 'm_qcal':
                continue  # Skip m_qcal itself
            
            assert 'masa_kg' in datos
            assert 'razon_m_qcal_sobre_particula' in datos
            assert 'ordenes_magnitud_diferencia' in datos
            
            # m_QCAL debe ser más pequeña que todas las partículas (excepto fotón)
            assert datos['razon_m_qcal_sobre_particula'] < 1.0
            
    def test_masa_qcal_menor_que_neutrino(self):
        """Test que m_QCAL < m_neutrino."""
        comparaciones = comparar_con_particulas_conocidas()
        
        # m_QCAL debe ser ~12 órdenes de magnitud menor que el neutrino
        neutrino = comparaciones['neutrino_electron_max']
        ordenes_diferencia = abs(neutrino['ordenes_magnitud_diferencia'])
        
        assert ordenes_diferencia > 10.0
        assert ordenes_diferencia < 15.0


class TestValidacionFisica:
    """Tests de validación física."""
    
    @pytest.fixture
    def masa_noetica(self):
        """Fixture para crear instancia de MasaNoetica."""
        return MasaNoetica(f0=F0_HZ)
    
    def test_relacion_E_mc2(self, masa_noetica):
        """Test relación E = mc² para m_QCAL."""
        E_calculada = masa_noetica.m_qcal * c ** 2
        
        # Usar tolerancia relativa apropiada
        assert abs(E_calculada - E_QCAL_J) / E_QCAL_J < 1e-10
        
    def test_formula_unificada_matematica(self, masa_noetica):
        """Test fórmula unificada matemáticamente."""
        # Para cualquier f: m(f) = (hf/c²) · (f₀/f) = hf₀/c²
        
        frecuencias = [0.01, 1.0, 100.0, 1e6, 1e15]
        
        for f in frecuencias:
            # Calcular manualmente
            m_manual = (h * f / c**2) * (F0_HZ / f)
            
            # Debe ser igual a m_QCAL
            assert abs(m_manual - M_QCAL_KG) < 1e-60
            
    def test_limite_fotones(self, masa_noetica):
        """Test límite para fotones (f → ∞)."""
        # A medida que f aumenta, m_noesis → 0
        frecuencias = [1e10, 1e15, 1e20]
        
        masas_noesis = [masa_noetica.masa_noetica_inversa(f) for f in frecuencias]
        
        # Verificar que disminuye monotónicamente
        for i in range(len(masas_noesis) - 1):
            assert masas_noesis[i] > masas_noesis[i + 1]
            
    def test_limite_ultra_baja_frecuencia(self, masa_noetica):
        """Test límite para ultra-baja frecuencia."""
        # A medida que f disminuye, m_noesis aumenta
        frecuencias = [1e-5, 1e-10, 1e-15]
        
        masas_noesis = [masa_noetica.masa_noetica_inversa(f) for f in frecuencias]
        
        # Verificar que aumenta monotónicamente
        for i in range(len(masas_noesis) - 1):
            assert masas_noesis[i] < masas_noesis[i + 1]


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
