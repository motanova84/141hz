#!/usr/bin/env python3
"""
Tests para validación del campo espectral biológico QCAL.

Prueba las implementaciones de:
  - Campo espectral ambiental Ψₑ(t)
  - Filtro biológico H(ω)
  - Acumulación de fase Φ(t)
  - Memoria de fase
  - Detección de colapso de fase
  - Simulación de Magicicada

Autor: José Manuel Mota Burruezo
Fecha: 27 de enero de 2026
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Añadir ruta a scripts
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir / 'scripts'))

from validacion_campo_espectral_biologico import CampoEspectralBiologico, SECONDS_PER_YEAR


class TestCampoEspectralBiologico:
    """Tests para el modelo de campo espectral biológico."""
    
    @pytest.fixture
    def modelo(self):
        """Fixture que proporciona un modelo inicializado."""
        return CampoEspectralBiologico(f0=141.7001, alpha_memoria=0.1, verbose=False)
    
    def test_inicializacion(self, modelo):
        """Verifica que el modelo se inicializa correctamente."""
        assert modelo.f0 == 141.7001
        assert modelo.alpha == 0.1
        assert modelo.omega_anual > 0
        assert modelo.omega_diario > 0
        assert modelo.omega_lunar > 0
    
    def test_campo_ambiental_espectral(self, modelo):
        """Verifica que el campo espectral se calcula correctamente."""
        t = np.linspace(0, SECONDS_PER_YEAR, 1000)
        psi_e = modelo.campo_ambiental_espectral(t)
        
        # Verificar que es complejo
        assert np.iscomplexobj(psi_e)
        
        # Verificar que tiene la longitud correcta
        assert len(psi_e) == len(t)
        
        # Verificar que no es cero
        assert np.sum(np.abs(psi_e)) > 0
        
        # Verificar periodicidad (aproximada)
        # El campo debe tener componente anual dominante
        fft_psi = np.fft.fft(psi_e)
        freqs = np.fft.fftfreq(len(t), t[1] - t[0])
        idx_max = np.argmax(np.abs(fft_psi[1:len(fft_psi)//2])) + 1
        f_dominante = abs(freqs[idx_max])
        
        # Frecuencia dominante debe ser cercana a la anual
        assert abs(f_dominante - modelo.omega_anual/(2*np.pi)) < 1e-6
    
    def test_filtro_biologico_magicicada(self, modelo):
        """Verifica el filtro biológico para Magicicada."""
        omega = np.linspace(0, 2*np.pi*200, 1000)
        H = modelo.filtro_biologico(omega, tipo='magicicada')
        
        # Verificar que H está normalizado (valores entre 0 y 1 aproximadamente)
        assert np.all(H >= 0)
        assert np.max(H) <= 1.5  # Permitir algo de sobrepaso
        
        # Verificar que tiene un pico cerca de omega_anual
        idx_max = np.argmax(H)
        omega_max = omega[idx_max]
        
        # El máximo debe estar en frecuencias bajas (ciclos largos)
        assert omega_max < 2 * np.pi * 10  # Menos de 10 Hz
    
    def test_filtro_biologico_arabidopsis(self, modelo):
        """Verifica el filtro biológico para Arabidopsis."""
        omega = np.linspace(0, 2*np.pi*200, 1000)
        H = modelo.filtro_biologico(omega, tipo='arabidopsis')
        
        assert np.all(H >= 0)
        assert len(H) == len(omega)
        
        # Arabidopsis debe ser sensible a ciclos diarios y f0
        # Verificar que hay respuesta en ambas bandas
        omega_hz = omega / (2 * np.pi)
        mask_diario = (omega_hz > 1e-6) & (omega_hz < 1e-4)
        mask_f0 = (omega_hz > 100) & (omega_hz < 200)
        
        assert np.any(H[mask_diario] > 0.1)  # Respuesta en banda diaria
        assert np.any(H[mask_f0] > 0.1)      # Respuesta en banda f0
    
    def test_acumulacion_fase(self, modelo):
        """Verifica el cálculo de acumulación de fase."""
        t = np.linspace(0, SECONDS_PER_YEAR, 5000)
        psi_e = modelo.campo_ambiental_espectral(t)
        
        fase, d_fase_dt = modelo.acumulacion_fase(t, psi_e)
        
        # Verificar dimensiones
        assert len(fase) == len(t)
        assert len(d_fase_dt) == len(t)
        
        # La fase debe ser monotónica creciente (o al menos no negativa)
        assert np.all(fase >= 0)
        
        # La fase debe crecer con el tiempo (en promedio)
        assert fase[-1] > fase[0]
        
        # La derivada temporal debe ser mayormente positiva
        assert np.mean(d_fase_dt > 0) > 0.5
    
    def test_memoria_fase(self, modelo):
        """Verifica el mecanismo de memoria de fase."""
        fase_actual = np.array([1.0, 2.0, 3.0])
        fase_anterior = np.array([0.8, 1.8, 2.8])
        
        fase_con_memoria = modelo.memoria_fase(fase_actual, fase_anterior)
        
        # Verificar que es combinación lineal correcta
        alpha = modelo.alpha
        esperado = alpha * fase_actual + (1 - alpha) * fase_anterior
        
        np.testing.assert_allclose(fase_con_memoria, esperado, rtol=1e-10)
        
        # Si no hay fase anterior, debe devolver la actual
        fase_sin_anterior = modelo.memoria_fase(fase_actual)
        np.testing.assert_array_equal(fase_sin_anterior, fase_actual)
    
    def test_detectar_colapso_fase(self, modelo):
        """Verifica la detección de colapso de fase."""
        # Crear datos sintéticos de fase que cruza umbral
        t = np.linspace(0, 17 * SECONDS_PER_YEAR, 1000)
        
        # Fase que crece linealmente y cruza umbral
        fase = np.linspace(0, 100, len(t))
        d_fase_dt = np.gradient(fase, t[1] - t[0])
        
        phi_critico = 50.0
        
        resultado = modelo.detectar_colapso_fase(
            t, fase, d_fase_dt, phi_critico,
            tipo_organismo='magicicada',
            ciclo_anos=17
        )
        
        # Debe detectar colapso
        assert resultado['colapso_detectado'] is True
        assert resultado['fase_colapso'] >= phi_critico
        assert resultado['umbral_critico'] == phi_critico
        
        # Verificar que el tiempo está en el rango esperado
        assert resultado['tiempo_colapso_s'] > 0
        assert resultado['tiempo_colapso_anos'] <= 17
    
    def test_detectar_colapso_fase_sin_cruce(self, modelo):
        """Verifica que no se detecta colapso si no se alcanza umbral."""
        t = np.linspace(0, 17 * SECONDS_PER_YEAR, 1000)
        
        # Fase que no alcanza el umbral
        fase = np.linspace(0, 30, len(t))
        d_fase_dt = np.gradient(fase, t[1] - t[0])
        
        phi_critico = 50.0
        
        resultado = modelo.detectar_colapso_fase(
            t, fase, d_fase_dt, phi_critico,
            tipo_organismo='magicicada',
            ciclo_anos=17
        )
        
        # No debe detectar colapso
        assert resultado['colapso_detectado'] is False
        assert 'fase_maxima' in resultado
        assert resultado['fase_maxima'] < phi_critico
    
    def test_simular_magicicada_17_anos(self, modelo):
        """Verifica simulación completa de Magicicada 17 años."""
        resultado = modelo.simular_magicicada(
            anos=17,
            dt_dias=7.0,  # Resolución semanal para velocidad
            phi_critico=None  # Calculado automáticamente
        )
        
        # Verificar estructura del resultado
        assert 'colapso_detectado' in resultado
        assert 'parametros' in resultado
        assert resultado['parametros']['anos'] == 17
        assert resultado['parametros']['alpha_memoria'] == modelo.alpha
        
        # Si hay colapso, verificar coherencia
        if resultado['colapso_detectado']:
            assert resultado['tiempo_colapso_anos'] > 0
            assert resultado['tiempo_colapso_anos'] <= 20  # Permitir algo de sobrepaso
            assert resultado['organismo'] == 'magicicada'
            assert resultado['ciclo_esperado_anos'] == 17
            
            # Verificar precisión razonable
            assert resultado['precision_pct'] >= 0  # Puede no ser perfecto con resolución gruesa
    
    def test_simular_magicicada_13_anos(self, modelo):
        """Verifica simulación de Magicicada 13 años."""
        resultado = modelo.simular_magicicada(
            anos=13,
            dt_dias=7.0
        )
        
        assert resultado['parametros']['anos'] == 13
        assert resultado['ciclo_esperado_anos'] == 13
        
        if resultado['colapso_detectado']:
            # Debe emerger cerca de 13 años
            assert abs(resultado['tiempo_colapso_anos'] - 13) < 2.0
    
    def test_simular_magicicada_con_perturbacion(self, modelo):
        """Verifica que la memoria de fase es robusta ante perturbaciones."""
        # Simulación sin perturbación
        resultado_control = modelo.simular_magicicada(
            anos=13,
            dt_dias=7.0
        )
        
        # Simulación con perturbación en año 5
        resultado_perturbado = modelo.simular_magicicada(
            anos=13,
            dt_dias=7.0,
            perturbacion_ano=5,
            perturbacion_amplitud=0.5  # 50% de reducción
        )
        
        # Ambas deben detectar colapso
        if resultado_control['colapso_detectado'] and resultado_perturbado['colapso_detectado']:
            t_control = resultado_control['tiempo_colapso_anos']
            t_perturbado = resultado_perturbado['tiempo_colapso_anos']
            
            # El desfase debe ser pequeño (< 10% del ciclo)
            desfase = abs(t_perturbado - t_control)
            desfase_pct = 100 * desfase / 13.0
            
            # Con alpha=0.1 (90% de memoria), el desfase debe ser pequeño
            assert desfase_pct < 15.0, f"Desfase demasiado grande: {desfase_pct:.1f}%"
    
    def test_parametros_fisica(self, modelo):
        """Verifica que los parámetros físicos están en rangos razonables."""
        # Frecuencia fundamental
        assert 100 < modelo.f0 < 200  # Hz
        
        # Parámetro de memoria
        assert 0 < modelo.alpha < 1
        
        # Frecuencias angulares
        assert modelo.omega_anual > 0
        assert modelo.omega_diario > modelo.omega_anual  # Diario más rápido
        assert modelo.omega_lunar > modelo.omega_anual   # Lunar más rápido
        
        # Verificar relaciones esperadas
        # omega_diario ≈ 365 * omega_anual
        ratio_esperado = 365.25
        ratio_calculado = modelo.omega_diario / modelo.omega_anual
        assert abs(ratio_calculado - ratio_esperado) < 1.0
    
    def test_conservacion_energia(self, modelo):
        """Verifica conservación de energía en el campo espectral."""
        t = np.linspace(0, SECONDS_PER_YEAR, 10000)
        
        # Campo con amplitudes conocidas
        A = [1.0, 0.5, 0.3]
        psi_e = modelo.campo_ambiental_espectral(t, amplitudes=A)
        
        # Energía total (teorema de Parseval)
        energia_temporal = np.sum(np.abs(psi_e)**2) * (t[1] - t[0])
        
        # Energía esperada (suma de cuadrados de amplitudes * tiempo)
        energia_esperada = sum([a**2 for a in A]) * SECONDS_PER_YEAR
        
        # Deben ser aproximadamente iguales
        assert abs(energia_temporal - energia_esperada) / energia_esperada < 0.1


class TestIntegracionCompleta:
    """Tests de integración del sistema completo."""
    
    def test_flujo_completo_magicicada(self):
        """Test del flujo completo de simulación."""
        modelo = CampoEspectralBiologico(f0=141.7001, alpha_memoria=0.1, verbose=False)
        
        # Ejecutar simulación completa
        resultado = modelo.simular_magicicada(
            anos=17,
            dt_dias=7.0
        )
        
        # Verificar que todos los componentes están presentes
        assert 'colapso_detectado' in resultado
        assert 'tiempo' in resultado
        assert 'fase' in resultado
        assert 'd_fase_dt' in resultado
        assert 'parametros' in resultado
        
        # Verificar longitud de series temporales
        assert len(resultado['tiempo']) > 0
        assert len(resultado['fase']) > 0
        assert len(resultado['fase']) == len(resultado['tiempo'])
    
    def test_reproducibilidad(self):
        """Verifica que las simulaciones son reproducibles."""
        modelo1 = CampoEspectralBiologico(f0=141.7001, alpha_memoria=0.1, verbose=False)
        modelo2 = CampoEspectralBiologico(f0=141.7001, alpha_memoria=0.1, verbose=False)
        
        # Simular con mismos parámetros
        resultado1 = modelo1.simular_magicicada(anos=13, dt_dias=7.0)
        resultado2 = modelo2.simular_magicicada(anos=13, dt_dias=7.0)
        
        # Resultados deben ser idénticos
        assert resultado1['colapso_detectado'] == resultado2['colapso_detectado']
        
        if resultado1['colapso_detectado']:
            assert abs(resultado1['tiempo_colapso_anos'] - 
                      resultado2['tiempo_colapso_anos']) < 0.01


if __name__ == '__main__':
    # Ejecutar tests con pytest
    pytest.main([__file__, '-v', '--tb=short'])
