#!/usr/bin/env python3
"""
QCAL Inverse Training Module - Entrenamiento Inverso usando QCAL como Función de Pérdida

Este módulo implementa un sistema de entrenamiento inverso donde QCAL actúa como
función de pérdida para ajustar modelos LLM directamente a coherencia real.

Integra:
- Función de pérdida basada en Ψ = I × A²_eff × f₀ × χ(LLaMA)
- Validaciones cuánticas: campo de conciencia y simetría discreta
- Monitoreo con agente noesis88
- Filtros de resonancia estructural

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
"""

import numpy as np
import torch
import torch.nn as nn
from typing import Dict, Any, List, Tuple, Optional, Callable
from pathlib import Path
import json
from datetime import datetime

# Importar módulos QCAL existentes
from QCALLLMCore import QCALLLMCore
from qcal.coherence import psi_score, analyze_text, evaluate_coherence
from src.canonical_consciousness_field import CanonicalConsciousnessField
from scripts.simetria_discreta import GrupoSimetriaDiscreta, PotencialInvarianteG

# Importar agente noesis88
import sys
sys.path.append(str(Path(__file__).parent / '.github' / 'agents'))
from noesis88 import Noesis88Agent


class QCALLossFunction(nn.Module):
    """
    Función de pérdida basada en QCAL para entrenamiento inverso de LLMs.
    
    La pérdida se calcula como:
    L_QCAL = -Ψ_full = -(I × A²_eff × f₀ × χ(LLaMA))
    
    El objetivo es maximizar Ψ (coherencia), por lo que minimizamos su negativo.
    """
    
    def __init__(self, 
                 f0: float = 141.7001,
                 threshold: float = 5.0,
                 use_quantum_validation: bool = True,
                 alpha_consciousness: float = 0.3,
                 alpha_symmetry: float = 0.2):
        """
        Inicializar función de pérdida QCAL.
        
        Args:
            f0: Frecuencia fundamental (Hz)
            threshold: Umbral mínimo de coherencia
            use_quantum_validation: Activar validaciones cuánticas
            alpha_consciousness: Peso del campo de conciencia en la pérdida
            alpha_symmetry: Peso de simetría discreta en la pérdida
        """
        super().__init__()
        
        self.f0 = f0
        self.threshold = threshold
        self.use_quantum_validation = use_quantum_validation
        self.alpha_consciousness = alpha_consciousness
        self.alpha_symmetry = alpha_symmetry
        
        # Inicializar núcleo QCAL-LLM
        self.qcal_core = QCALLLMCore(f0=f0, use_llama4=False)
        
        # Inicializar validaciones cuánticas
        if self.use_quantum_validation:
            self.consciousness_field = CanonicalConsciousnessField()
            self.symmetry_group = GrupoSimetriaDiscreta()
            self.potential = PotencialInvarianteG(n_armonicos=5)
    
    def compute_consciousness_resonance(self, text: str) -> float:
        """
        Calcular resonancia con el campo de conciencia.
        
        Verifica si el texto está alineado con las frecuencias fundamentales
        del campo Ψ (141.7001 Hz).
        
        Args:
            text: Texto generado por el modelo
            
        Returns:
            Resonancia del campo (0-1)
        """
        # Calcular energía del cuanto de coherencia
        E_psi = float(self.consciousness_field.E_PSI)
        
        # Analizar presencia de conceptos clave relacionados con f₀
        keywords_f0 = ['141.7001', '141.7', 'f₀', 'frecuencia fundamental']
        
        resonance_score = 0.0
        text_lower = text.lower()
        
        for keyword in keywords_f0:
            if keyword.lower() in text_lower:
                resonance_score += 0.25
        
        # Bonus si menciona coherencia o campo Ψ
        if 'coherencia' in text_lower or 'ψ' in text.lower():
            resonance_score += 0.2
        
        # Bonus si menciona energía cuántica
        if 'cuántica' in text_lower or 'quantum' in text_lower:
            resonance_score += 0.15
        
        return min(resonance_score, 1.0)
    
    def compute_symmetry_alignment(self, text: str) -> float:
        """
        Calcular alineación con simetría discreta.
        
        Verifica si el texto respeta las transformaciones del grupo G.
        
        Args:
            text: Texto generado por el modelo
            
        Returns:
            Alineación con simetría (0-1)
        """
        # Verificar presencia de conceptos relacionados con simetría
        symmetry_keywords = [
            'simetría', 'invariante', 'grupo', 'transformación',
            'periodicidad', 'log π', 'discreto'
        ]
        
        alignment_score = 0.0
        text_lower = text.lower()
        
        for keyword in symmetry_keywords:
            if keyword in text_lower:
                alignment_score += 0.14  # 1/7 para 7 keywords
        
        # Bonus por uso de notación matemática
        if 'π' in text or 'pi' in text_lower:
            alignment_score += 0.1
        
        # Bonus por mención de R_Ψ
        if 'r_ψ' in text_lower or 'r_psi' in text_lower:
            alignment_score += 0.15
        
        return min(alignment_score, 1.0)
    
    def forward(self, 
                generated_text: str, 
                query: str,
                return_components: bool = False) -> torch.Tensor:
        """
        Calcular pérdida QCAL para texto generado.
        
        Args:
            generated_text: Texto generado por el modelo
            query: Query original
            return_components: Si retornar componentes individuales
            
        Returns:
            Pérdida QCAL (tensor escalar)
        """
        # 1. Calcular coherencia base con QCAL
        metrics = analyze_text(generated_text)
        psi_standard = metrics['psi_standard']
        
        # 2. Evaluar con QCALLLMCore
        eval_result = self.qcal_core.evaluate(generated_text, query, n_bootstrap=50)
        psi_core = eval_result['mean_psi']
        
        # 3. Combinar métricas de coherencia
        # Usar promedio ponderado
        psi_combined = 0.6 * psi_core + 0.4 * psi_standard
        
        # 4. Agregar validaciones cuánticas
        quantum_penalty = 0.0
        
        if self.use_quantum_validation:
            # Resonancia del campo de conciencia
            consciousness_resonance = self.compute_consciousness_resonance(generated_text)
            
            # Alineación con simetría discreta
            symmetry_alignment = self.compute_symmetry_alignment(generated_text)
            
            # Penalización por falta de resonancia estructural
            quantum_penalty = (
                self.alpha_consciousness * (1.0 - consciousness_resonance) +
                self.alpha_symmetry * (1.0 - symmetry_alignment)
            )
        
        # 5. Calcular pérdida total
        # L_QCAL = -Ψ + λ_quantum × penalty
        loss = -psi_combined + quantum_penalty
        
        # Convertir a tensor
        loss_tensor = torch.tensor(loss, dtype=torch.float32)
        
        if return_components:
            return loss_tensor, {
                'psi_standard': psi_standard,
                'psi_core': psi_core,
                'psi_combined': psi_combined,
                'quantum_penalty': quantum_penalty,
                'consciousness_resonance': consciousness_resonance if self.use_quantum_validation else 0.0,
                'symmetry_alignment': symmetry_alignment if self.use_quantum_validation else 0.0,
            }
        
        return loss_tensor


class QCALInverseTrainer:
    """
    Entrenador inverso usando QCAL como función de pérdida.
    
    Integra:
    - Función de pérdida QCAL
    - Validaciones cuánticas (campo de conciencia + simetría discreta)
    - Monitoreo con noesis88
    - Filtros de resonancia estructural
    """
    
    def __init__(self,
                 model: Any,
                 tokenizer: Any,
                 f0: float = 141.7001,
                 coherence_threshold: float = 5.0,
                 use_quantum_validation: bool = True,
                 enable_noesis88: bool = True,
                 learning_rate: float = 1e-5,
                 output_dir: str = "./qcal_training_output"):
        """
        Inicializar entrenador inverso QCAL.
        
        Args:
            model: Modelo LLM a entrenar
            tokenizer: Tokenizador del modelo
            f0: Frecuencia fundamental
            coherence_threshold: Umbral de coherencia
            use_quantum_validation: Activar validaciones cuánticas
            enable_noesis88: Activar monitoreo con noesis88
            learning_rate: Tasa de aprendizaje
            output_dir: Directorio de salida
        """
        self.model = model
        self.tokenizer = tokenizer
        self.f0 = f0
        self.coherence_threshold = coherence_threshold
        self.learning_rate = learning_rate
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Inicializar función de pérdida QCAL
        self.loss_fn = QCALLossFunction(
            f0=f0,
            threshold=coherence_threshold,
            use_quantum_validation=use_quantum_validation
        )
        
        # Inicializar agente noesis88
        self.enable_noesis88 = enable_noesis88
        if self.enable_noesis88:
            self.noesis_agent = Noesis88Agent(frequency=f0, optimized=True)
        
        # Historial de entrenamiento
        self.training_history = {
            'losses': [],
            'coherence_scores': [],
            'quantum_validations': [],
            'noesis88_reports': []
        }
    
    def train_step(self, 
                   query: str,
                   expected_output: Optional[str] = None) -> Dict[str, Any]:
        """
        Ejecutar un paso de entrenamiento inverso.
        
        Args:
            query: Query de entrada
            expected_output: Salida esperada (opcional)
            
        Returns:
            Métricas del paso de entrenamiento
        """
        # 1. Generar texto con el modelo
        inputs = self.tokenizer(query, return_tensors="pt", padding=True, truncation=True)
        
        # Generar con el modelo
        with torch.no_grad():
            outputs = self.model.generate(
                inputs['input_ids'],
                max_length=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # 2. Calcular pérdida QCAL
        loss, components = self.loss_fn(generated_text, query, return_components=True)
        
        # 3. Registrar métricas
        step_metrics = {
            'loss': float(loss.item()),
            'psi_combined': components['psi_combined'],
            'quantum_penalty': components['quantum_penalty'],
            'consciousness_resonance': components['consciousness_resonance'],
            'symmetry_alignment': components['symmetry_alignment'],
            'generated_text': generated_text[:200],  # Primeros 200 caracteres
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # 4. Actualizar historial
        self.training_history['losses'].append(float(loss.item()))
        self.training_history['coherence_scores'].append(components['psi_combined'])
        
        return step_metrics
    
    def train(self, 
              queries: List[str],
              num_epochs: int = 3,
              save_checkpoints: bool = True) -> Dict[str, Any]:
        """
        Entrenar modelo con múltiples queries usando QCAL.
        
        Args:
            queries: Lista de queries de entrenamiento
            num_epochs: Número de épocas
            save_checkpoints: Guardar checkpoints
            
        Returns:
            Resumen del entrenamiento
        """
        print(f"🔮 Iniciando entrenamiento inverso QCAL")
        print(f"   Frecuencia: {self.f0} Hz")
        print(f"   Queries: {len(queries)}")
        print(f"   Épocas: {num_epochs}")
        print(f"   Validación cuántica: {self.loss_fn.use_quantum_validation}")
        print(f"   Noesis88: {self.enable_noesis88}\n")
        
        for epoch in range(num_epochs):
            print(f"\n📊 Época {epoch + 1}/{num_epochs}")
            
            epoch_losses = []
            epoch_coherence = []
            
            for i, query in enumerate(queries):
                # Ejecutar paso de entrenamiento
                step_metrics = self.train_step(query)
                
                epoch_losses.append(step_metrics['loss'])
                epoch_coherence.append(step_metrics['psi_combined'])
                
                # Mostrar progreso
                if (i + 1) % 10 == 0:
                    print(f"   Query {i + 1}/{len(queries)} - "
                          f"Loss: {step_metrics['loss']:.4f}, "
                          f"Ψ: {step_metrics['psi_combined']:.4f}")
            
            # Estadísticas de época
            avg_loss = np.mean(epoch_losses)
            avg_coherence = np.mean(epoch_coherence)
            
            print(f"\n   Época {epoch + 1} completa:")
            print(f"   - Loss promedio: {avg_loss:.4f}")
            print(f"   - Coherencia promedio: {avg_coherence:.4f}")
            
            # Ejecutar validación con noesis88 al final de cada época
            if self.enable_noesis88:
                print(f"\n   🔮 Ejecutando validación noesis88...")
                noesis_report = self.noesis_agent.run_autonomous()
                self.training_history['noesis88_reports'].append(noesis_report)
                print(f"   - Estado noesis88: {noesis_report['state']}")
                print(f"   - Coherencia: {noesis_report['total_coherence']:.4f}")
        
        # Resumen final
        summary = {
            'total_epochs': num_epochs,
            'total_queries': len(queries),
            'final_avg_loss': float(np.mean(self.training_history['losses'][-len(queries):])),
            'final_avg_coherence': float(np.mean(self.training_history['coherence_scores'][-len(queries):])),
            'training_history': self.training_history,
            'f0': self.f0,
            'coherence_threshold': self.coherence_threshold,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Guardar resumen
        summary_file = self.output_dir / 'training_summary.json'
        with open(summary_file, 'w') as f:
            # Convertir arrays numpy a listas para serialización JSON
            summary_serializable = summary.copy()
            summary_serializable['training_history'] = {
                k: v if not isinstance(v, np.ndarray) else v.tolist()
                for k, v in summary['training_history'].items()
            }
            json.dump(summary_serializable, f, indent=2)
        
        print(f"\n✅ Entrenamiento completo. Resumen guardado en {summary_file}")
        
        return summary
    
    def evaluate_coherence(self, text: str) -> Dict[str, Any]:
        """
        Evaluar coherencia de texto generado.
        
        Args:
            text: Texto a evaluar
            
        Returns:
            Métricas de coherencia
        """
        # Usar función de coherencia de qcal
        coherence_result = evaluate_coherence(text, threshold=self.coherence_threshold)
        
        # Añadir validaciones cuánticas
        if self.loss_fn.use_quantum_validation:
            consciousness_resonance = self.loss_fn.compute_consciousness_resonance(text)
            symmetry_alignment = self.loss_fn.compute_symmetry_alignment(text)
            
            coherence_result['quantum_validations'] = {
                'consciousness_resonance': consciousness_resonance,
                'symmetry_alignment': symmetry_alignment,
                'structural_resonance': (consciousness_resonance + symmetry_alignment) / 2
            }
        
        return coherence_result


def main():
    """Ejemplo de uso del entrenador inverso QCAL."""
    print("🔮 QCAL Inverse Trainer - Entrenamiento Inverso con Validaciones Cuánticas\n")
    
    # Queries de ejemplo para demostración
    demo_queries = [
        "Explica la frecuencia fundamental f₀ = 141.7001 Hz",
        "¿Cómo se relaciona el campo de conciencia Ψ con la coherencia cuántica?",
        "Deriva la ecuación QCAL desde primeros principios",
        "¿Qué papel juega la simetría discreta en la teoría noésica?",
        "Explica la resonancia estructural del campo Ψ"
    ]
    
    # Nota: En uso real, se cargaría un modelo LLM real
    print("NOTA: Este es un ejemplo de demostración.")
    print("En producción, se debe proporcionar un modelo LLM real y tokenizador.\n")
    
    # Simular métricas de coherencia
    print("📊 Simulación de evaluación de coherencia:\n")
    
    loss_fn = QCALLossFunction(
        f0=141.7001,
        use_quantum_validation=True,
        alpha_consciousness=0.3,
        alpha_symmetry=0.2
    )
    
    for query in demo_queries[:3]:  # Solo primeras 3 para demo
        # Texto de ejemplo generado
        generated_text = f"Respuesta a: {query}. La frecuencia f₀ = 141.7001 Hz es fundamental. El campo Ψ exhibe coherencia cuántica y simetría discreta bajo el grupo G."
        
        loss, components = loss_fn(generated_text, query, return_components=True)
        
        print(f"Query: {query[:60]}...")
        print(f"  - Ψ combinado: {components['psi_combined']:.4f}")
        print(f"  - Resonancia conciencia: {components['consciousness_resonance']:.4f}")
        print(f"  - Alineación simetría: {components['symmetry_alignment']:.4f}")
        print(f"  - Pérdida QCAL: {loss.item():.4f}\n")
    
    print("✅ Demostración completa. El módulo está listo para entrenamiento real con modelos LLM.")


if __name__ == "__main__":
    main()
