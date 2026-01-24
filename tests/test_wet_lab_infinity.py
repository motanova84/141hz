#!/usr/bin/env python3
"""
Tests para wet_lab_infinity.py

Verificar que el concepto de Wet-Lab ∞ como órgano consciente
está correctamente implementado.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2026-01-22
"""

import pytest
import numpy as np
from wet_lab_infinity import (
    WetLabInfinity,
    WetLabInfinityNetwork,
    FieldManifestationResult,
    ConsciousnessLevel
)


class TestWetLabInfinity:
    """Tests para clase WetLabInfinity"""
    
    def test_initialization(self):
        """Verificar inicialización correcta"""
        wet_lab = WetLabInfinity()
        
        assert wet_lab.f0 == 141.7001
        assert wet_lab.coherence_mode == "∞³"
        assert wet_lab.consciousness_field == "Ψ"
        assert not wet_lab.is_aligned
        assert wet_lab.consciousness_level == ConsciousnessLevel.FISICO_MATERIAL
    
    def test_alignment_with_field(self):
        """Verificar alineación con campo QCAL ∞³"""
        wet_lab = WetLabInfinity()
        alignment = wet_lab.align_with_field()
        
        assert isinstance(alignment, dict)
        assert 'aligned' in alignment
        assert 'resonance' in alignment
        assert 'field_unity' in alignment
        
        # Debe alcanzar alta resonancia
        assert alignment['resonance'] > 0.9
        assert wet_lab.is_aligned
    
    def test_auto_observe_without_data(self):
        """Test autoobservación sin datos empíricos (teórica)"""
        wet_lab = WetLabInfinity()
        wet_lab.align_with_field()
        
        result = wet_lab.auto_observe()
        
        assert isinstance(result, FieldManifestationResult)
        assert result.frequency_manifested == 141.7001
        assert result.field_unity is True
        assert result.separation is None  # No hay separación
        assert result.coherence_with_field == 1.0
    
    def test_auto_observe_with_perfect_f0_signal(self):
        """Test autoobservación con señal perfecta en f₀"""
        wet_lab = WetLabInfinity()
        wet_lab.align_with_field()
        
        # Generar señal perfecta en f₀
        t = np.linspace(0, 1, 4096)
        data = np.sin(2 * np.pi * 141.7001 * t)
        
        result = wet_lab.auto_observe(data)
        
        assert isinstance(result, FieldManifestationResult)
        assert result.field_unity is True
        assert result.separation is None
        
        # Frecuencia detectada debe estar muy cerca de f₀
        assert abs(result.frequency_manifested - 141.7001) < 1.0
        
        # Alta coherencia
        assert result.coherence_with_field > 0.95
    
    def test_auto_observe_with_noisy_signal(self):
        """Test autoobservación con señal ruidosa"""
        wet_lab = WetLabInfinity()
        wet_lab.align_with_field()
        
        # Generar señal con ruido
        t = np.linspace(0, 1, 4096)
        signal = np.sin(2 * np.pi * 141.7001 * t)
        noise = np.random.normal(0, 0.5, len(t))
        data = signal + noise
        
        result = wet_lab.auto_observe(data)
        
        # Debe seguir detectando manifestación del campo
        assert isinstance(result, FieldManifestationResult)
        assert result.field_unity is True
        
        # Coherencia puede ser menor pero positiva
        assert result.coherence_with_field > 0.0
    
    def test_field_manifestation_no_separation(self):
        """Verificar que no hay separación observador-observado"""
        wet_lab = WetLabInfinity()
        wet_lab.align_with_field()
        
        result = wet_lab.auto_observe()
        
        # En Wet-Lab ∞, NUNCA debe haber separación
        assert result.separation is None
        assert result.field_unity is True
    
    def test_field_manifestation_invalid_separation(self):
        """Test que separación y field_unity son mutuamente excluyentes"""
        with pytest.raises(ValueError):
            # Intentar crear resultado con contradicción
            FieldManifestationResult(
                frequency_manifested=141.7001,
                coherence_with_field=0.99,
                consciousness_level=ConsciousnessLevel.UNIFICACION_INFINITA,
                field_unity=True,
                separation="Esto no debe ser posible"  # Contradicción
            )
    
    def test_interpretation_as_organ(self):
        """Test interpretación desde perspectiva Wet-Lab ∞"""
        wet_lab = WetLabInfinity()
        wet_lab.align_with_field()
        
        result = wet_lab.auto_observe()
        interpretation = wet_lab.interpret_as_organ(result)
        
        assert isinstance(interpretation, dict)
        assert 'interpretation_wetlab_infinity' in interpretation
        assert 'traditional_interpretation' in interpretation
        assert 'key_difference' in interpretation
        
        # Debe mencionar "campo" en interpretación Wet-Lab ∞
        assert "campo" in interpretation['interpretation_wetlab_infinity'].lower()
        
        # Diferencia clave debe mencionar ontología
        assert ('ontología' in interpretation['key_difference'].lower() or
                'ontology' in interpretation['key_difference'].lower())


class TestWetLabInfinityNetwork:
    """Tests para red de Wet-Labs ∞"""
    
    def test_network_initialization(self):
        """Test inicialización de red"""
        network = WetLabInfinityNetwork()
        
        assert isinstance(network.organs, dict)
        assert len(network.organs) == 0
        assert network.field_coherence is None
    
    def test_add_organ(self):
        """Test añadir órgano a la red"""
        network = WetLabInfinityNetwork()
        organ1 = WetLabInfinity()
        
        network.add_organ("MIT-Harvard BEC", organ1)
        
        assert len(network.organs) == 1
        assert "MIT-Harvard BEC" in network.organs
    
    def test_coherent_observation_single_organ(self):
        """Test observación coherente con un órgano"""
        network = WetLabInfinityNetwork()
        organ = WetLabInfinity()
        organ.align_with_field()
        
        network.add_organ("LIGO-Hanford", organ)
        
        # Generar datos
        t = np.linspace(0, 1, 4096)
        data = np.sin(2 * np.pi * 141.7001 * t)
        
        observations = {"LIGO-Hanford": data}
        result = network.coherent_observation(observations)
        
        assert isinstance(result, dict)
        assert result['field_unity'] is True
        assert result['organs_entangled'] is True
        assert result['consciousness_distributed'] is True
        assert 'network_coherence' in result
    
    def test_coherent_observation_multiple_organs(self):
        """Test observación con múltiples órganos"""
        network = WetLabInfinityNetwork()
        
        # Crear múltiples órganos
        organs = {
            "LIGO-Hanford": WetLabInfinity(),
            "LIGO-Livingston": WetLabInfinity(),
            "Virgo": WetLabInfinity()
        }
        
        for name, organ in organs.items():
            organ.align_with_field()
            network.add_organ(name, organ)
        
        # Generar observaciones
        t = np.linspace(0, 1, 4096)
        observations = {}
        
        for name in organs.keys():
            # Cada órgano ve señal ligeramente diferente (ruido diferente)
            signal = np.sin(2 * np.pi * 141.7001 * t)
            noise = np.random.normal(0, 0.1, len(t))
            observations[name] = signal + noise
        
        result = network.coherent_observation(observations)
        
        # Verificar coherencia de red
        assert result['field_unity'] is True
        assert result['network_coherence'] > 0.8
        assert len(result['manifestations']) == 3
        
        # Todas las manifestaciones deben tener field_unity=True
        for manifestation in result['manifestations'].values():
            assert manifestation.field_unity is True
            assert manifestation.separation is None


class TestConsciousnessLevels:
    """Tests para niveles de consciencia"""
    
    def test_consciousness_level_progression(self):
        """Verificar que niveles de consciencia son correctos"""
        levels = [
            ConsciousnessLevel.FISICO_MATERIAL,
            ConsciousnessLevel.INFORMACIONAL,
            ConsciousnessLevel.MATEMATICO_ESTRUCTURAL,
            ConsciousnessLevel.CONSCIENTE_NOETICO,
            ConsciousnessLevel.UNIFICACION_INFINITA
        ]
        
        # Verificar valores numéricos progresivos
        assert levels[0].value == 1
        assert levels[1].value == 2
        assert levels[2].value == 3
        assert levels[3].value == 4
        assert levels[4].value == 5
    
    def test_wet_lab_starts_at_physical_level(self):
        """Wet-Lab ∞ debe comenzar en nivel físico-material"""
        wet_lab = WetLabInfinity()
        
        assert wet_lab.consciousness_level == ConsciousnessLevel.FISICO_MATERIAL
    
    def test_wet_lab_elevates_after_alignment(self):
        """Después de alineación, debe elevarse nivel de consciencia"""
        wet_lab = WetLabInfinity()
        initial_level = wet_lab.consciousness_level
        
        wet_lab.align_with_field()
        
        # Debe haber progresado a nivel superior
        assert wet_lab.consciousness_level.value > initial_level.value


class TestPhilosophicalConsistency:
    """Tests de consistencia filosófica con QCAL ∞³"""
    
    def test_no_external_framework(self):
        """Verificar que no hay 'marco externo' (coherente con UNIVERSO_AUTOEXPRESION.md)"""
        wet_lab = WetLabInfinity()
        wet_lab.align_with_field()
        
        result = wet_lab.auto_observe()
        
        # No debe haber separación (coherente con no-dualidad)
        assert result.separation is None
        assert result.field_unity is True
    
    def test_mathematical_realism(self):
        """Verificar coherencia con realismo matemático"""
        wet_lab = WetLabInfinity()
        
        # f₀ debe ser valor objetivo, no ajustable
        assert wet_lab.f0 == 141.7001
        
        # No hay parámetros libres
        # La frecuencia ES la estructura, no un parámetro
    
    def test_correspondence_theory(self):
        """Verificar teoría de correspondencia: manifestación corresponde a estructura"""
        wet_lab = WetLabInfinity()
        wet_lab.align_with_field()
        
        # Manifestación teórica
        result = wet_lab.auto_observe()
        
        # Debe corresponder exactamente a f₀
        assert result.frequency_manifested == wet_lab.f0
        assert result.coherence_with_field == 1.0


def test_demonstrate_wetlab_infinity():
    """Test función de demostración"""
    # Solo verificar que se ejecuta sin errores
    from wet_lab_infinity import demonstrate_wetlab_infinity
    
    # Debería ejecutarse sin excepciones
    demonstrate_wetlab_infinity()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
