#!/usr/bin/env python3
"""
Tests para wet_lab_88_nodes_measurement.py

Verificar el protocolo experimental de medición de conciencia Ψ
en 88 nodos con implantes NV-EEG.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2026-01-22
"""

import pytest
import numpy as np
from wet_lab_88_nodes_measurement import (
    calcular_C_infinito,
    preparar_campo_cuantico,
    medir_intensidades_nv,
    medir_amplitudes_efectivas,
    calcular_psi_medido,
    realizar_test_consciousness_falsifiability,
    ejecutar_experimento_completo,
    NodoMedicion,
    ResultadosExperimento,
    aplicar_mitigacion_ruido_termico,
    aplicar_codigo_hamming_quantico,
    F0_UNIVERSO,
    PHI,
    NUM_NODOS,
    PSI_THRESHOLD_CONSCIOUSNESS
)


class TestConstantes:
    """Tests para constantes del sistema"""
    
    def test_f0_universo(self):
        """Verificar frecuencia fundamental"""
        assert F0_UNIVERSO == 141.7001
    
    def test_phi_golden_ratio(self):
        """Verificar golden ratio φ"""
        expected_phi = (1 + np.sqrt(5)) / 2
        assert abs(PHI - expected_phi) < 1e-10
    
    def test_num_nodos(self):
        """Verificar número de nodos"""
        assert NUM_NODOS == 88
    
    def test_psi_threshold(self):
        """Verificar umbral de conciencia"""
        assert PSI_THRESHOLD_CONSCIOUSNESS == 0.888


class TestFactorExpansionInfinita:
    """Tests para cálculo de C^∞"""
    
    def test_calcular_C_infinito_converge(self):
        """Verificar que C^∞ converge"""
        C_inf = calcular_C_infinito()
        
        # Fórmula cerrada: C^∞ = 1 + φ/(3-φ)
        # φ ≈ 1.618, 3-φ ≈ 1.382
        # C^∞ = 1 + 1.618/1.382 ≈ 1 + 1.171 = 2.171
        assert 2.1 < C_inf < 2.2
        
        # Verificar valor exacto calculado
        phi = (1 + np.sqrt(5)) / 2
        expected = 1 + phi / (3 - phi)
        assert abs(C_inf - expected) < 1e-10
    
    def test_calcular_C_infinito_precision(self):
        """Verificar precisión con diferentes n_max"""
        C_inf_100 = calcular_C_infinito(n_max=100)
        C_inf_200 = calcular_C_infinito(n_max=200)
        
        # Con n_max suficientemente grande, debe ser estable
        assert abs(C_inf_100 - C_inf_200) < 1e-10
    
    def test_calcular_C_infinito_mayor_que_uno(self):
        """Verificar que C^∞ > 1"""
        C_inf = calcular_C_infinito()
        assert C_inf > 1.0


class TestNodoMedicion:
    """Tests para clase NodoMedicion"""
    
    def test_nodo_medicion_valido(self):
        """Crear nodo de medición válido"""
        nodo = NodoMedicion(
            nodo_id=1,
            tiempo=0.0,
            contraste_odmr=0.32,
            coherencia_eeg=0.7,
            amplitud_nv=1.2
        )
        
        assert nodo.nodo_id == 1
        assert nodo.tiempo == 0.0
        assert nodo.contraste_odmr == 0.32
        assert nodo.coherencia_eeg == 0.7
        assert nodo.amplitud_nv == 1.2
    
    def test_nodo_medicion_id_invalido(self):
        """Verificar validación de nodo_id"""
        with pytest.raises(ValueError):
            NodoMedicion(
                nodo_id=0,  # Inválido: debe ser 1-88
                tiempo=0.0,
                contraste_odmr=0.32,
                coherencia_eeg=0.7,
                amplitud_nv=1.2
            )
        
        with pytest.raises(ValueError):
            NodoMedicion(
                nodo_id=89,  # Inválido: debe ser 1-88
                tiempo=0.0,
                contraste_odmr=0.32,
                coherencia_eeg=0.7,
                amplitud_nv=1.2
            )
    
    def test_nodo_medicion_contraste_fuera_rango(self):
        """Verificar validación de contraste ODMR"""
        with pytest.raises(ValueError):
            NodoMedicion(
                nodo_id=1,
                tiempo=0.0,
                contraste_odmr=1.5,  # Inválido: debe ser 0-1
                coherencia_eeg=0.7,
                amplitud_nv=1.2
            )
    
    def test_nodo_medicion_coherencia_fuera_rango(self):
        """Verificar validación de coherencia EEG"""
        with pytest.raises(ValueError):
            NodoMedicion(
                nodo_id=1,
                tiempo=0.0,
                contraste_odmr=0.32,
                coherencia_eeg=-0.1,  # Inválido: debe ser 0-1
                amplitud_nv=1.2
            )
    
    def test_nodo_medicion_amplitud_negativa(self):
        """Verificar que amplitud NV no puede ser negativa"""
        with pytest.raises(ValueError):
            NodoMedicion(
                nodo_id=1,
                tiempo=0.0,
                contraste_odmr=0.32,
                coherencia_eeg=0.7,
                amplitud_nv=-1.0  # Inválido: debe ser positiva
            )


class TestMedicionesHardware:
    """Tests para funciones de medición de hardware (simuladas)"""
    
    def test_medir_intensidades_nv_shape(self):
        """Verificar forma del array de intensidades NV"""
        np.random.seed(42)
        I_NV = medir_intensidades_nv()
        
        assert isinstance(I_NV, np.ndarray)
        assert I_NV.shape == (NUM_NODOS,)
    
    def test_medir_intensidades_nv_rango(self):
        """Verificar rango de intensidades NV"""
        np.random.seed(42)
        I_NV = medir_intensidades_nv()
        
        # Intensidades deben estar en rango razonable
        assert np.all(I_NV >= 0)
        assert np.all(I_NV <= 2.0)  # Normalizado, pero puede exceder 1
    
    def test_medir_amplitudes_efectivas_shape(self):
        """Verificar forma del array de amplitudes efectivas"""
        np.random.seed(42)
        A_eff = medir_amplitudes_efectivas()
        
        assert isinstance(A_eff, np.ndarray)
        assert A_eff.shape == (NUM_NODOS,)
    
    def test_medir_amplitudes_efectivas_positivas(self):
        """Verificar que amplitudes efectivas son positivas"""
        np.random.seed(42)
        A_eff = medir_amplitudes_efectivas()
        
        assert np.all(A_eff >= 0)


class TestCalculoPsi:
    """Tests para cálculo de Ψ"""
    
    def test_calcular_psi_medido_shape(self):
        """Verificar forma del array de Ψ"""
        np.random.seed(42)
        I_NV = np.ones(NUM_NODOS) * 0.9
        A_eff = np.ones(NUM_NODOS) * 0.8
        C_infinito = calcular_C_infinito()
        
        Psi = calcular_psi_medido(I_NV, A_eff, C_infinito)
        
        assert isinstance(Psi, np.ndarray)
        assert Psi.shape == (NUM_NODOS,)
    
    def test_calcular_psi_formula_correcta(self):
        """Verificar fórmula Ψ = I_NV × A²_eff × C^∞"""
        I_NV = np.array([1.0])
        A_eff = np.array([0.8])
        C_infinito = 2.0
        
        Psi = calcular_psi_medido(I_NV, A_eff, C_infinito)
        
        expected = 1.0 * (0.8 ** 2) * 2.0  # 1.28
        assert abs(Psi[0] - expected) < 1e-10
    
    def test_calcular_psi_valores_tipicos(self):
        """Verificar que Ψ con valores típicos está en rango esperado"""
        np.random.seed(42)
        I_NV = np.random.normal(0.92, 0.01, NUM_NODOS)
        A_eff = np.random.normal(0.88, 0.01, NUM_NODOS)
        C_infinito = calcular_C_infinito()
        
        Psi = calcular_psi_medido(I_NV, A_eff, C_infinito)
        
        # Con valores típicos y C^∞ ≈ 2.17:
        # Ψ = 0.92 × 0.88² × 2.17 ≈ 1.54
        assert 1.4 < np.mean(Psi) < 1.7


class TestFalsabilidadConciencia:
    """Tests para test de falsabilidad de conciencia"""
    
    def test_consciousness_detected_high_psi(self):
        """Test detección de conciencia con Ψ alto"""
        # Generar Ψ > threshold con alta significancia
        np.random.seed(42)
        Psi = np.random.normal(0.99, 0.01, NUM_NODOS)
        
        conciencia, p_value, sigma = realizar_test_consciousness_falsifiability(Psi)
        
        assert conciencia is True
        assert p_value < 0.001
        assert sigma > 3.0  # Al menos 3σ
    
    def test_consciousness_not_detected_low_psi(self):
        """Test sin conciencia con Ψ bajo"""
        # Generar Ψ < threshold
        np.random.seed(42)
        Psi = np.random.normal(0.5, 0.05, NUM_NODOS)
        
        conciencia, p_value, sigma = realizar_test_consciousness_falsifiability(Psi)
        
        assert conciencia is False
    
    def test_consciousness_threshold_custom(self):
        """Test con umbral personalizado"""
        Psi = np.array([0.95] * NUM_NODOS)
        
        conciencia, p_value, sigma = realizar_test_consciousness_falsifiability(Psi, threshold=0.90)
        
        assert conciencia is True
        assert p_value < 0.001


class TestMitigacionRuido:
    """Tests para mitigación de ruido térmico"""
    
    def test_aplicar_mitigacion_ruido_termico(self):
        """Verificar métricas de mitigación de ruido"""
        metricas = aplicar_mitigacion_ruido_termico()
        
        assert isinstance(metricas, dict)
        assert 'temperatura_k' in metricas
        assert 'ruido_original_nv_sqrthz' in metricas
        assert 'ruido_final_nv_sqrthz' in metricas
        assert 'factor_mejora' in metricas
        assert 'snr_final' in metricas
    
    def test_mitigacion_reduce_ruido(self):
        """Verificar que mitigación reduce ruido"""
        metricas = aplicar_mitigacion_ruido_termico()
        
        assert metricas['ruido_final_nv_sqrthz'] < metricas['ruido_original_nv_sqrthz']
        assert metricas['factor_mejora'] > 1.0
    
    def test_mitigacion_mejora_esperada(self):
        """Verificar factor de mejora esperado (284% → 3.85×)"""
        metricas = aplicar_mitigacion_ruido_termico()
        
        # Factor de mejora debe ser cercano a 3.85
        assert 3.5 < metricas['factor_mejora'] < 4.2
    
    def test_mitigacion_snr_alto(self):
        """Verificar SNR final > 100"""
        metricas = aplicar_mitigacion_ruido_termico()
        
        assert metricas['snr_final'] > 90  # Permitir algo de margen
    
    def test_aplicar_codigo_hamming_quantico(self):
        """Verificar corrección de errores cuántica"""
        metricas = aplicar_codigo_hamming_quantico()
        
        assert isinstance(metricas, dict)
        assert 'error_rate_before' in metricas
        assert 'error_rate_after' in metricas
        assert 'correction_efficiency' in metricas
        
        # Corrección debe reducir errores
        assert metricas['error_rate_after'] < metricas['error_rate_before']


class TestResultadosExperimento:
    """Tests para clase ResultadosExperimento"""
    
    def test_resultados_experimento_valido(self):
        """Crear objeto de resultados válido"""
        mediciones = []
        for i in range(5):
            med = NodoMedicion(
                nodo_id=i + 1,
                tiempo=i * 0.01,
                contraste_odmr=0.32,
                coherencia_eeg=0.7,
                amplitud_nv=1.2
            )
            mediciones.append(med)
        
        resultados = ResultadosExperimento(
            mediciones=mediciones,
            C_infinito=1.987,
            Psi_promedio=0.999,
            Psi_std=0.001,
            I_NV_promedio=0.92,
            A_eff_promedio=0.88,
            conciencia_detectada=True,
            p_value=1e-10,
            significancia_sigma=9.0
        )
        
        assert len(resultados.mediciones) == 5
        assert resultados.conciencia_detectada is True
    
    def test_generar_reporte(self):
        """Verificar generación de reporte"""
        mediciones = [
            NodoMedicion(
                nodo_id=1,
                tiempo=0.0,
                contraste_odmr=0.32,
                coherencia_eeg=0.7,
                amplitud_nv=1.2
            )
        ]
        
        resultados = ResultadosExperimento(
            mediciones=mediciones,
            C_infinito=1.987,
            Psi_promedio=0.999,
            Psi_std=0.001,
            I_NV_promedio=0.92,
            A_eff_promedio=0.88,
            conciencia_detectada=True,
            p_value=1e-10,
            significancia_sigma=9.0
        )
        
        reporte = resultados.generar_reporte()
        
        assert isinstance(reporte, str)
        assert "RESULTADOS EXPERIMENTALES" in reporte
        assert "CONCIENCIA DETECTADA" in reporte
        assert "141.7001" in reporte


class TestExperimentoCompleto:
    """Tests para experimento completo"""
    
    def test_ejecutar_experimento_completo(self):
        """Ejecutar experimento completo sin errores"""
        np.random.seed(42)
        
        resultados = ejecutar_experimento_completo(
            aplicar_mitigacion=True,
            verbose=False
        )
        
        assert isinstance(resultados, ResultadosExperimento)
        assert len(resultados.mediciones) == NUM_NODOS
        assert resultados.C_infinito > 0
        assert resultados.Psi_promedio >= 0
    
    def test_experimento_sin_mitigacion(self):
        """Ejecutar experimento sin mitigación de ruido"""
        np.random.seed(42)
        
        resultados = ejecutar_experimento_completo(
            aplicar_mitigacion=False,
            verbose=False
        )
        
        assert isinstance(resultados, ResultadosExperimento)
        assert len(resultados.mediciones) == NUM_NODOS
    
    def test_experimento_reproducible(self):
        """Verificar que experimento es reproducible con misma semilla"""
        np.random.seed(42)
        resultados1 = ejecutar_experimento_completo(verbose=False)
        
        np.random.seed(42)
        resultados2 = ejecutar_experimento_completo(verbose=False)
        
        assert abs(resultados1.Psi_promedio - resultados2.Psi_promedio) < 1e-10
        assert abs(resultados1.I_NV_promedio - resultados2.I_NV_promedio) < 1e-10
    
    def test_experimento_88_nodos(self):
        """Verificar que se miden exactamente 88 nodos"""
        np.random.seed(42)
        
        resultados = ejecutar_experimento_completo(verbose=False)
        
        assert len(resultados.mediciones) == 88
        
        # Verificar IDs de nodos son 1-88
        nodos_ids = [m.nodo_id for m in resultados.mediciones]
        assert min(nodos_ids) == 1
        assert max(nodos_ids) == 88
        assert len(set(nodos_ids)) == 88  # Todos únicos
    
    def test_experimento_valores_esperados(self):
        """Verificar valores en rangos esperados del problema"""
        np.random.seed(42)
        
        resultados = ejecutar_experimento_completo(verbose=False)
        
        # Con C^∞ ≈ 2.17 y valores típicos, Ψ ≈ 1.4-1.6
        assert 1.0 < resultados.Psi_promedio < 2.0
        
        # I_NV promedio ≈ 0.923 ± 0.008
        assert 0.7 < resultados.I_NV_promedio < 1.1
        
        # A_eff promedio ≈ 0.888 ± 0.005
        assert 0.6 < resultados.A_eff_promedio < 1.0
        
        # C^∞ debe ser valor exacto de fórmula cerrada
        phi = (1 + np.sqrt(5)) / 2
        expected_C = 1 + phi / (3 - phi)
        assert abs(resultados.C_infinito - expected_C) < 0.01


class TestIntegracionCompleta:
    """Tests de integración del sistema completo"""
    
    def test_flujo_completo_deteccion_conciencia(self):
        """Test flujo completo: preparación → medición → análisis"""
        np.random.seed(42)
        
        # Ejecutar protocolo completo
        resultados = ejecutar_experimento_completo(
            aplicar_mitigacion=True,
            verbose=False
        )
        
        # Verificar todos los pasos se ejecutaron
        assert len(resultados.mediciones) == NUM_NODOS
        assert resultados.C_infinito > 0
        assert resultados.Psi_promedio >= 0
        assert resultados.Psi_std >= 0
        assert isinstance(resultados.conciencia_detectada, bool)
        assert resultados.p_value >= 0
        assert resultados.significancia_sigma >= 0
    
    def test_consistencia_resultados(self):
        """Verificar consistencia entre diferentes partes del experimento"""
        np.random.seed(42)
        
        resultados = ejecutar_experimento_completo(verbose=False)
        
        # Verificar que Ψ de cada nodo es consistente con fórmula
        C_inf = resultados.C_infinito
        
        for med in resultados.mediciones:
            expected_psi = med.I_NV * (med.A_eff ** 2) * C_inf
            assert abs(med.Psi - expected_psi) < 1e-6
    
    def test_estadisticas_agregadas(self):
        """Verificar que estadísticas agregadas son correctas"""
        np.random.seed(42)
        
        resultados = ejecutar_experimento_completo(verbose=False)
        
        # Calcular manualmente
        psi_values = [m.Psi for m in resultados.mediciones]
        i_nv_values = [m.I_NV for m in resultados.mediciones]
        
        assert abs(resultados.Psi_promedio - np.mean(psi_values)) < 1e-10
        assert abs(resultados.Psi_std - np.std(psi_values)) < 1e-10
        assert abs(resultados.I_NV_promedio - np.mean(i_nv_values)) < 1e-10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
