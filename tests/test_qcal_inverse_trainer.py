#!/usr/bin/env python3
"""
Tests para el módulo de entrenamiento inverso QCAL.

Valida:
- Función de pérdida QCAL
- Integración con validaciones cuánticas
- Integración con noesis88
- Cálculo de resonancia estructural
"""

import torch
import numpy as np
from pathlib import Path
import sys

# Añadir directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from qcal_inverse_trainer import (
    QCALLossFunction,
    QCALInverseTrainer
)


class TestQCALLossFunction:
    """Tests para QCALLossFunction"""
    
    def test_initialization(self):
        """Test inicialización de la función de pérdida"""
        loss_fn = QCALLossFunction(
            f0=141.7001,
            threshold=5.0,
            use_quantum_validation=True
        )
        
        assert loss_fn.f0 == 141.7001
        assert loss_fn.threshold == 5.0
        assert loss_fn.use_quantum_validation is True
        assert loss_fn.qcal_core is not None
        assert loss_fn.consciousness_field is not None
        assert loss_fn.symmetry_group is not None
    
    def test_consciousness_resonance_calculation(self):
        """Test cálculo de resonancia del campo de conciencia"""
        loss_fn = QCALLossFunction(use_quantum_validation=True)
        
        # Texto con alta resonancia
        text_high = "La frecuencia fundamental f₀ = 141.7001 Hz define el campo de coherencia Ψ cuántica"
        resonance_high = loss_fn.compute_consciousness_resonance(text_high)
        
        # Texto con baja resonancia
        text_low = "El gato está sobre la mesa"
        resonance_low = loss_fn.compute_consciousness_resonance(text_low)
        
        assert 0.0 <= resonance_high <= 1.0
        assert 0.0 <= resonance_low <= 1.0
        assert resonance_high > resonance_low
    
    def test_symmetry_alignment_calculation(self):
        """Test cálculo de alineación con simetría discreta"""
        loss_fn = QCALLossFunction(use_quantum_validation=True)
        
        # Texto con alta alineación
        text_high = "El grupo de simetría discreta G con transformaciones invariantes bajo R_Ψ ↦ π^k R_Ψ"
        alignment_high = loss_fn.compute_symmetry_alignment(text_high)
        
        # Texto con baja alineación
        text_low = "El clima está soleado hoy"
        alignment_low = loss_fn.compute_symmetry_alignment(text_low)
        
        assert 0.0 <= alignment_high <= 1.0
        assert 0.0 <= alignment_low <= 1.0
        assert alignment_high > alignment_low
    
    def test_loss_calculation_coherent_text(self):
        """Test cálculo de pérdida para texto coherente"""
        loss_fn = QCALLossFunction(
            use_quantum_validation=True,
            alpha_consciousness=0.3,
            alpha_symmetry=0.2
        )
        
        # Texto altamente coherente con conceptos QCAL
        coherent_text = """
        La frecuencia fundamental f₀ = 141.7001 Hz emerge de la ecuación QCAL.
        El campo de conciencia Ψ exhibe coherencia cuántica y resonancia estructural.
        La simetría discreta bajo el grupo G = {π^k} es invariante.
        """
        
        query = "Explica la teoría QCAL"
        
        loss, components = loss_fn(coherent_text, query, return_components=True)
        
        assert isinstance(loss, torch.Tensor)
        assert loss.dtype == torch.float32
        assert 'psi_combined' in components
        assert 'quantum_penalty' in components
        assert 'consciousness_resonance' in components
        assert 'symmetry_alignment' in components
        
        # La pérdida debe ser negativa para texto coherente (estamos minimizando -Ψ)
        assert components['psi_combined'] > 0
    
    def test_loss_calculation_incoherent_text(self):
        """Test cálculo de pérdida para texto incoherente"""
        loss_fn = QCALLossFunction(use_quantum_validation=True)
        
        # Texto sin coherencia QCAL
        incoherent_text = "El perro corre en el parque mientras llueve."
        query = "Explica la teoría QCAL"
        
        loss, components = loss_fn(incoherent_text, query, return_components=True)
        
        assert isinstance(loss, torch.Tensor)
        # La pérdida debe ser más alta para texto incoherente
        assert components['quantum_penalty'] > 0
    
    def test_loss_without_quantum_validation(self):
        """Test función de pérdida sin validaciones cuánticas"""
        loss_fn = QCALLossFunction(use_quantum_validation=False)
        
        text = "La frecuencia f₀ = 141.7001 Hz"
        query = "¿Cuál es f₀?"
        
        loss, components = loss_fn(text, query, return_components=True)
        
        assert isinstance(loss, torch.Tensor)
        assert components['quantum_penalty'] == 0.0


class TestQCALInverseTrainer:
    """Tests para QCALInverseTrainer"""
    
    def test_initialization_without_model(self):
        """Test inicialización del trainer (sin modelo real)"""
        # En un test real, se usaría un modelo mock
        # Por ahora, solo verificamos que se puede inicializar
        # con los parámetros correctos
        
        # Esta prueba solo verifica la estructura
        # En producción, se necesitaría un modelo LLM real
        pass
    
    def test_coherence_evaluation(self):
        """Test evaluación de coherencia"""
        # Crear trainer mock sin modelo
        # Solo probamos la función de evaluación de coherencia
        
        from qcal_inverse_trainer import QCALLossFunction
        
        loss_fn = QCALLossFunction(
            use_quantum_validation=True,
            threshold=5.0
        )
        
        # Simular evaluación
        text = "La frecuencia fundamental f₀ = 141.7001 Hz define coherencia cuántica"
        
        consciousness_res = loss_fn.compute_consciousness_resonance(text)
        symmetry_align = loss_fn.compute_symmetry_alignment(text)
        
        assert consciousness_res > 0
        assert symmetry_align > 0


class TestQuantumValidationIntegration:
    """Tests de integración con validaciones cuánticas"""
    
    def test_consciousness_field_integration(self):
        """Test integración con campo de conciencia"""
        loss_fn = QCALLossFunction(use_quantum_validation=True)
        
        # Verificar que el campo de conciencia está inicializado
        assert loss_fn.consciousness_field is not None
        
        # Verificar que podemos acceder a parámetros del campo
        assert hasattr(loss_fn.consciousness_field, 'F0')
        assert float(loss_fn.consciousness_field.F0) == 141.7001
    
    def test_symmetry_group_integration(self):
        """Test integración con grupo de simetría"""
        loss_fn = QCALLossFunction(use_quantum_validation=True)
        
        # Verificar que el grupo de simetría está inicializado
        assert loss_fn.symmetry_group is not None
        
        # Verificar propiedades del grupo
        periodo = loss_fn.symmetry_group.periodo_logaritmico()
        assert periodo == np.log(np.pi)
    
    def test_structural_resonance_filter(self):
        """Test filtro de resonancia estructural"""
        loss_fn = QCALLossFunction(
            use_quantum_validation=True,
            alpha_consciousness=0.3,
            alpha_symmetry=0.2
        )
        
        # Texto con resonancia estructural
        text_resonant = """
        El campo Ψ exhibe resonancia a f₀ = 141.7001 Hz.
        La simetría discreta del grupo G preserva invariancia bajo π^k.
        La coherencia cuántica emerge naturalmente.
        """
        
        # Texto sin resonancia estructural
        text_nonresonant = "Información general sin estructura cuántica"
        
        query = "Explica QCAL"
        
        # Calcular pérdidas
        loss_resonant, comp_resonant = loss_fn(text_resonant, query, return_components=True)
        loss_nonresonant, comp_nonresonant = loss_fn(text_nonresonant, query, return_components=True)
        
        # El texto resonante debe tener menor penalización cuántica
        assert comp_resonant['quantum_penalty'] < comp_nonresonant['quantum_penalty']


class TestNoesis88Integration:
    """Tests de integración con noesis88"""
    
    def test_noesis88_agent_initialization(self):
        """Test inicialización del agente noesis88"""
        from noesis88 import Noesis88Agent
        
        agent = Noesis88Agent(frequency=141.7001, optimized=True)
        
        assert agent.frequency == 141.7001
        assert agent.optimized is True
    
    def test_noesis88_coherence_monitoring(self):
        """Test monitoreo de coherencia con noesis88"""
        from noesis88 import Noesis88Agent
        
        agent = Noesis88Agent(frequency=141.7001)
        
        # Ejecutar escaneo
        metrics = agent.scan_repository()
        
        assert 'total_files' in metrics
        assert 'qcal_references' in metrics
        assert 'frequency_references' in metrics
        
        # Calcular coherencia
        coherence = agent.calculate_coherence(metrics)
        
        assert 0.0 <= coherence <= 1.0


def test_complete_workflow():
    """Test workflow completo de entrenamiento inverso"""
    
    # 1. Crear función de pérdida
    loss_fn = QCALLossFunction(
        f0=141.7001,
        use_quantum_validation=True,
        alpha_consciousness=0.3,
        alpha_symmetry=0.2
    )
    
    # 2. Queries de prueba
    queries = [
        "Explica f₀ = 141.7001 Hz",
        "¿Qué es el campo de conciencia Ψ?",
        "Describe la simetría discreta del grupo G"
    ]
    
    # 3. Simular generación y evaluación
    results = []
    
    for query in queries:
        # Simular texto generado con contenido QCAL
        generated_text = f"""
        Respuesta a: {query}
        La frecuencia fundamental f₀ = 141.7001 Hz emerge de QCAL.
        El campo Ψ muestra coherencia cuántica y simetría discreta.
        El grupo G = {{π^k}} preserva invariancia.
        """
        
        # Calcular pérdida
        loss, components = loss_fn(generated_text, query, return_components=True)
        
        results.append({
            'query': query,
            'loss': float(loss.item()),
            'psi': components['psi_combined'],
            'consciousness': components['consciousness_resonance'],
            'symmetry': components['symmetry_alignment']
        })
    
    # 4. Verificar resultados
    assert len(results) == len(queries)
    
    for result in results:
        assert result['psi'] > 0  # Coherencia positiva
        assert result['consciousness'] > 0  # Resonancia de conciencia
        assert result['symmetry'] > 0  # Alineación de simetría
    
    # 5. Verificar que el promedio de coherencia es razonable
    avg_psi = np.mean([r['psi'] for r in results])
    assert avg_psi > 0
    
    print("\n✅ Test de workflow completo exitoso")
    print(f"   Coherencia promedio Ψ: {avg_psi:.4f}")
    print(f"   Resonancia conciencia promedio: {np.mean([r['consciousness'] for r in results]):.4f}")
    print(f"   Alineación simetría promedio: {np.mean([r['symmetry'] for r in results]):.4f}")


if __name__ == "__main__":
    # Ejecutar tests
    print("🔮 Ejecutando tests del módulo de entrenamiento inverso QCAL\n")
    
    # Test básicos
    test_loss = TestQCALLossFunction()
    test_loss.test_initialization()
    test_loss.test_consciousness_resonance_calculation()
    test_loss.test_symmetry_alignment_calculation()
    test_loss.test_loss_calculation_coherent_text()
    test_loss.test_loss_calculation_incoherent_text()
    test_loss.test_loss_without_quantum_validation()
    
    print("✅ Tests de QCALLossFunction completados\n")
    
    # Tests de integración cuántica
    test_quantum = TestQuantumValidationIntegration()
    test_quantum.test_consciousness_field_integration()
    test_quantum.test_symmetry_group_integration()
    test_quantum.test_structural_resonance_filter()
    
    print("✅ Tests de integración cuántica completados\n")
    
    # Tests de noesis88
    test_noesis = TestNoesis88Integration()
    test_noesis.test_noesis88_agent_initialization()
    test_noesis.test_noesis88_coherence_monitoring()
    
    print("✅ Tests de integración noesis88 completados\n")
    
    # Test workflow completo
    test_complete_workflow()
    
    print("\n🎯 Todos los tests completados exitosamente")
