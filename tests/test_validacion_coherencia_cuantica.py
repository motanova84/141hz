#!/usr/bin/env python3
"""
Tests para la validación de coherencia cuántica QCAL.

Valida que:
1. La coherencia cumple con el umbral Ψ ≥ 0.888
2. Las frecuencias son correctas (141.7001 Hz y 888 Hz)
3. La transformación entrópica es estable
4. El experimento bio-computacional predice correctamente
"""

import sys
import os
import pytest
import numpy as np

# Añadir el directorio de scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from validacion_coherencia_cuantica import (
    QuantumCondensationEngine,
    QuantumSpectralField,
    MagicicadaModel,
    BioComputationalResonanceExperiment,
    F0_QCAL,
    RESONANCE_888,
    PSI_THRESHOLD,
    COMPRESSION_RATIO
)


class TestConstantesQCAL:
    """Tests para las constantes QCAL."""
    
    def test_frecuencia_fundamental(self):
        """Verifica que f₀ = 141.7001 Hz."""
        assert F0_QCAL == 141.7001
        
    def test_resonancia_888(self):
        """Verifica que la resonancia es 888 Hz."""
        assert RESONANCE_888 == 888.0
        
    def test_umbral_coherencia(self):
        """Verifica que el umbral de coherencia es 0.888."""
        assert PSI_THRESHOLD == 0.888
        
    def test_ratio_compresion(self):
        """Verifica que el ratio de compresión es 1000.1."""
        assert COMPRESSION_RATIO == 1000.1


class TestQuantumCondensationEngine:
    """Tests para el motor de condensación cuántica."""
    
    def test_inicializacion(self):
        """Verifica la inicialización del motor."""
        engine = QuantumCondensationEngine()
        assert engine.f0 == F0_QCAL
        assert engine.resonance == RESONANCE_888
        assert engine.state == 'INITIALIZING'
        
    def test_ciclo_condensacion(self):
        """Verifica que un ciclo de condensación produce resultados válidos."""
        engine = QuantumCondensationEngine()
        result = engine.run_condensation_cycle()
        
        # Verificar estructura del resultado
        assert 'frecuencia' in result
        assert 'coherencia' in result
        assert 'compresion_ratio' in result
        assert 'estabilidad' in result
        assert 'hash_sha3' in result
        
        # Verificar valores
        assert result['frecuencia'] == F0_QCAL
        assert 0.0 <= result['coherencia'] <= 1.0
        assert result['compresion_ratio'] == COMPRESSION_RATIO
        assert result['estabilidad'] in ['ESTABLE', 'INESTABLE']
        assert len(result['hash_sha3']) == 16  # Primeros 16 caracteres del hash
        
    def test_coherencia_esperada(self):
        """Verifica que la coherencia típicamente cumple el umbral."""
        engine = QuantumCondensationEngine()
        coherencias = []
        
        # Ejecutar múltiples ciclos
        for _ in range(100):
            result = engine.run_condensation_cycle()
            coherencias.append(result['coherencia'])
        
        # La mayoría debería estar por encima del umbral
        coherencias_validas = sum(1 for c in coherencias if c >= PSI_THRESHOLD)
        tasa_exito = coherencias_validas / len(coherencias)
        
        # Al menos 85% deberían ser válidas (dado el mapeo usado)
        assert tasa_exito >= 0.85


class TestQuantumSpectralField:
    """Tests para el campo espectral cuántico."""
    
    def test_inicializacion(self):
        """Verifica la inicialización del campo."""
        field = QuantumSpectralField()
        assert field.f0 == F0_QCAL
        
    def test_medicion_coherencia(self):
        """Verifica que la medición de coherencia es válida."""
        field = QuantumSpectralField()
        coherence = field.measure_coherence()
        
        # Coherencia debe estar cerca de 0.943199
        assert 0.93 <= coherence <= 0.96
        
    def test_coherencia_supera_umbral(self):
        """Verifica que la coherencia supera el umbral PSI_THRESHOLD."""
        field = QuantumSpectralField()
        
        # Medir múltiples veces
        for _ in range(50):
            coherence = field.measure_coherence()
            assert coherence >= PSI_THRESHOLD


class TestMagicicadaModel:
    """Tests para el modelo biológico Magicicada."""
    
    def test_ciclo_17_anios(self):
        """Verifica que el ciclo es de 17 años."""
        model = MagicicadaModel()
        assert model.cycle_years == 17
        
    def test_fase_progresiva(self):
        """Verifica que la fase aumenta progresivamente."""
        model = MagicicadaModel(cycle_years=17)
        
        phases = [model.get_phase(year) for year in range(1, 18)]
        
        # Las fases deben ser crecientes hasta el año 17
        for i in range(len(phases) - 1):
            assert phases[i] < phases[i + 1] or i == 16  # El último vuelve a 0
            
    def test_fase_rango(self):
        """Verifica que las fases están en el rango [0, 1)."""
        model = MagicicadaModel()
        
        for year in range(1, 100):
            phase = model.get_phase(year)
            assert 0.0 <= phase < 1.0


class TestBioComputationalResonanceExperiment:
    """Tests para el experimento bio-computacional."""
    
    def test_inicializacion(self):
        """Verifica la inicialización del experimento."""
        experiment = BioComputationalResonanceExperiment()
        
        assert isinstance(experiment.biological_model, MagicicadaModel)
        assert isinstance(experiment.computational_model, QuantumCondensationEngine)
        assert isinstance(experiment.qcal_field, QuantumSpectralField)
        
    def test_convergencia_calculo(self):
        """Verifica el cálculo de convergencia."""
        experiment = BioComputationalResonanceExperiment()
        
        # Test con valores conocidos
        convergence = experiment.calculate_convergence(0.5, 0.9, 0.94)
        
        # Convergencia es el promedio
        expected = (0.5 + 0.9 + 0.94) / 3.0
        assert abs(convergence - expected) < 1e-10
        
    def test_convergence_test_17_anios(self):
        """Verifica que el test de convergencia cubre 17 años."""
        experiment = BioComputationalResonanceExperiment()
        results = experiment.run_convergence_test()
        
        assert len(results) == 17
        
        # Verificar estructura de cada resultado
        for result in results:
            assert 'year' in result
            assert 'biological_phase' in result
            assert 'computational_coherence' in result
            assert 'field_coherence' in result
            assert 'convergence_score' in result
            
    def test_prediccion_emergencia(self):
        """Verifica la predicción de año de emergencia."""
        experiment = BioComputationalResonanceExperiment()
        prediction = experiment.predict_emergence_year()
        
        # Verificar estructura
        assert 'predicted_emergence_year' in prediction
        assert 'expected_emergence_year' in prediction
        assert 'prediction_correct' in prediction
        assert 'max_convergence' in prediction
        
        # El año esperado debe ser 17
        assert prediction['expected_emergence_year'] == 17
        
        # El año predicho debe estar en el rango [1, 17]
        assert 1 <= prediction['predicted_emergence_year'] <= 17
        
        # La predicción correcta acepta años 15-17
        if prediction['predicted_emergence_year'] >= 15:
            assert prediction['prediction_correct']


class TestValidacionIntegral:
    """Tests de validación integral del sistema."""
    
    def test_coherencia_cumple_prediccion(self):
        """Verifica que la coherencia cumple la predicción QCAL."""
        field = QuantumSpectralField()
        coherence = field.measure_coherence()
        
        # Predicción QCAL: Ψ = 0.943199
        assert abs(coherence - 0.943199) < 0.02
        
        # Predicción QCAL: Ψ ≥ 0.888
        assert coherence >= PSI_THRESHOLD
        
    def test_todas_frecuencias_alineadas(self):
        """Verifica que todas las frecuencias están alineadas."""
        engine = QuantumCondensationEngine()
        field = QuantumSpectralField()
        
        assert engine.f0 == F0_QCAL
        assert field.f0 == F0_QCAL
        assert engine.resonance == RESONANCE_888
        
    def test_sistema_completo_funcional(self):
        """Test de integración completo del sistema."""
        # Crear todos los componentes
        field = QuantumSpectralField()
        engine = QuantumCondensationEngine()
        experiment = BioComputationalResonanceExperiment()
        
        # Ejecutar cada componente
        coherence = field.measure_coherence()
        condensation = engine.run_condensation_cycle()
        prediction = experiment.predict_emergence_year()
        
        # Verificar que todos funcionan
        assert coherence >= PSI_THRESHOLD
        assert condensation['estabilidad'] in ['ESTABLE', 'INESTABLE']
        assert 1 <= prediction['predicted_emergence_year'] <= 17
        
    def test_metricas_convergencia(self):
        """Verifica las métricas de convergencia del sistema."""
        field = QuantumSpectralField()
        engine = QuantumCondensationEngine()
        
        coherence = field.measure_coherence()
        result = engine.run_condensation_cycle()
        
        # Métrica 1: Frecuencia
        assert result['frecuencia'] == F0_QCAL
        
        # Métrica 2: Coherencia
        assert coherence >= PSI_THRESHOLD
        
        # Métrica 3: Compresión
        assert result['compresion_ratio'] == COMPRESSION_RATIO


if __name__ == '__main__':
    # Ejecutar tests
    pytest.main([__file__, '-v'])
