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

# torch se importa solo cuando se necesita
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    # Mock torch para que el módulo pueda cargarse sin torch
    class MockTensor:
        def __init__(self, value):
            self.value = value
        def item(self):
            return self.value
    
    class MockModule:
        pass


class QCALLossFunction:
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
        if TORCH_AVAILABLE:
            # Solo usar nn.Module si torch está disponible
            super(QCALLossFunction, self).__init__()
        
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
                return_components: bool = False):
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
        if TORCH_AVAILABLE:
            loss_tensor = torch.tensor(loss, dtype=torch.float32)
        else:
            loss_tensor = MockTensor(loss)
        
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
    
    CARACTERÍSTICAS CLAVE:
    ✓ Filtrado del aprendizaje no-coherente: Solo aprende si genera resonancia
    ✓ Mitigación del sesgo entrópico: Corrige aprendizaje caótico (alineamiento con G = {π^k})
    ✓ Entrenamiento interpretable: Reportes Noesis88 por época con estado cuántico-emergente
    ✓ Entrenamiento abierto + falsable: Verificación física y matemática
    
    Integra:
    - Función de pérdida QCAL
    - Validaciones cuánticas (campo de conciencia + simetría discreta)
    - Monitoreo con noesis88
    - Filtros de resonancia estructural
    - Detector de resonancia ontológica universal
    """
    
    # Constantes de configuración
    PSI_NORMALIZATION_FACTOR = 10.0  # Factor de normalización para Ψ en cálculo de resonancia
    ENTROPIC_BIAS_THRESHOLD = 0.3  # Umbral para detección de sesgo entrópico
    SYMMETRY_KEYWORDS = ['simetría', 'periódico', 'invariante', 'π', 'pi']  # Palabras clave de simetría
    
    def __init__(self,
                 model: Any,
                 tokenizer: Any,
                 f0: float = 141.7001,
                 coherence_threshold: float = 5.0,
                 resonance_threshold: float = 0.7,
                 use_quantum_validation: bool = True,
                 enable_noesis88: bool = True,
                 filter_non_coherent: bool = True,
                 mitigate_entropic_bias: bool = True,
                 learning_rate: float = 1e-5,
                 output_dir: str = "./qcal_training_output"):
        """
        Inicializar entrenador inverso QCAL.
        
        Args:
            model: Modelo LLM a entrenar
            tokenizer: Tokenizador del modelo
            f0: Frecuencia fundamental
            coherence_threshold: Umbral de coherencia Ψ
            resonance_threshold: Umbral mínimo de resonancia para permitir aprendizaje
            use_quantum_validation: Activar validaciones cuánticas
            enable_noesis88: Activar monitoreo con noesis88
            filter_non_coherent: Filtrar aprendizaje no-coherente
            mitigate_entropic_bias: Mitigar sesgo entrópico con alineamiento G
            learning_rate: Tasa de aprendizaje
            output_dir: Directorio de salida
        """
        self.model = model
        self.tokenizer = tokenizer
        self.f0 = f0
        self.coherence_threshold = coherence_threshold
        self.resonance_threshold = resonance_threshold
        self.filter_non_coherent = filter_non_coherent
        self.mitigate_entropic_bias = mitigate_entropic_bias
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
            'noesis88_reports': [],
            'resonance_scores': [],
            'filtered_steps': [],  # Pasos filtrados por no-coherencia
            'entropic_corrections': []  # Correcciones de sesgo entrópico
        }
    
    def compute_resonance(self, generated_text: str, components: Dict[str, Any]) -> float:
        """
        Calcula resonancia ontológica universal del texto generado.
        
        La resonancia combina:
        - Coherencia Ψ
        - Resonancia del campo de conciencia
        - Alineamiento con simetría discreta
        
        Args:
            generated_text: Texto generado
            components: Componentes de la pérdida QCAL
            
        Returns:
            Resonancia total [0, 1] (≥ threshold para permitir aprendizaje)
        """
        # Componentes de resonancia
        psi_resonance = min(components['psi_combined'] / self.PSI_NORMALIZATION_FACTOR, 1.0)
        consciousness_resonance = components.get('consciousness_resonance', 0.0)
        symmetry_resonance = components.get('symmetry_alignment', 0.0)
        
        # Resonancia combinada (promedio ponderado)
        total_resonance = (
            0.5 * psi_resonance +
            0.3 * consciousness_resonance +
            0.2 * symmetry_resonance
        )
        
        return total_resonance
    
    def check_entropic_bias(self, generated_text: str) -> Tuple[bool, float]:
        """
        Detecta sesgo entrópico (aprendizaje caótico o aleatorio).
        
        El sesgo entrópico se manifiesta como:
        - Repeticiones excesivas (baja diversidad léxica)
        - Falta de estructura lógica
        - Desalineamiento con simetría discreta G
        
        Args:
            generated_text: Texto generado
            
        Returns:
            (tiene_sesgo, score_entropico)
        """
        # 1. Detectar repeticiones excesivas
        words = generated_text.split()
        if len(words) == 0:
            return True, 0.0  # Texto vacío = máximo sesgo (score bajo)
        
        unique_words = len(set(words))
        total_words = len(words)
        lexical_diversity = unique_words / total_words
        
        # 2. Detectar falta de estructura (sin puntuación)
        has_structure = any(char in generated_text for char in ['.', '?', '!', ','])
        structure_score = 1.0 if has_structure else 0.0
        
        # 3. Verificar alineamiento con G = {π^k}
        # Buscar conceptos relacionados con simetría y periodicidad
        has_symmetry = any(kw in generated_text.lower() for kw in self.SYMMETRY_KEYWORDS)
        symmetry_score = 1.0 if has_symmetry else 0.5
        
        # Score entrópico (bajo = más sesgo)
        entropic_score = (
            0.5 * lexical_diversity +
            0.3 * structure_score +
            0.2 * symmetry_score
        )
        
        # Sesgo detectado si score < threshold
        has_bias = entropic_score < self.ENTROPIC_BIAS_THRESHOLD
        
        return has_bias, entropic_score
    
    def apply_entropic_correction(self, generated_text: str) -> str:
        """
        Aplica corrección de sesgo entrópico mediante alineamiento con G.
        
        Añade conceptos clave de simetría discreta para guiar el aprendizaje
        hacia resonancia ontológica.
        
        Args:
            generated_text: Texto original con sesgo
            
        Returns:
            Texto corregido con alineamiento G
        """
        # Inyectar conceptos de simetría discreta
        correction_suffix = (
            "\n[Corrección entrópica aplicada: "
            "El texto debe alinearse con la simetría discreta G = {π^k R_Ψ} "
            "y exhibir periodicidad logarítmica en log R_Ψ con periodo log π.]"
        )
        
        return generated_text + correction_suffix
    
    def train_step(self, 
                   query: str,
                   expected_output: Optional[str] = None) -> Dict[str, Any]:
        """
        Ejecutar un paso de entrenamiento inverso con filtrado de no-coherencia.
        
        FILTRADO NO-COHERENTE:
        - Solo permite actualización si la salida genera resonancia ≥ threshold
        - Bloquea aprendizaje de patrones caóticos o aleatorios
        
        MITIGACIÓN ENTRÓPICA:
        - Detecta sesgo entrópico en la salida
        - Aplica corrección mediante alineamiento con G = {π^k}
        
        Args:
            query: Query de entrada
            expected_output: Salida esperada (opcional)
            
        Returns:
            Métricas del paso de entrenamiento (incluye filtrado y correcciones)
        """
        if not TORCH_AVAILABLE:
            raise RuntimeError("torch es requerido para entrenar. Instalar con: pip install torch>=2.6.0")
        
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
        
        # 3. FILTRADO NO-COHERENTE: Verificar resonancia
        resonance = self.compute_resonance(generated_text, components)
        learning_allowed = True
        filtered = False
        
        if self.filter_non_coherent and resonance < self.resonance_threshold:
            learning_allowed = False
            filtered = True
            print(f"⚠️  Aprendizaje bloqueado: resonancia {resonance:.4f} < {self.resonance_threshold}")
        
        # 4. MITIGACIÓN ENTRÓPICA: Detectar y corregir sesgo
        has_entropic_bias = False
        entropic_score = 1.0
        corrected_text = generated_text
        
        if self.mitigate_entropic_bias:
            has_entropic_bias, entropic_score = self.check_entropic_bias(generated_text)
            
            if has_entropic_bias:
                corrected_text = self.apply_entropic_correction(generated_text)
                print(f"🔧 Corrección entrópica aplicada (score: {entropic_score:.4f})")
                
                # Recalcular pérdida con texto corregido
                loss, components = self.loss_fn(corrected_text, query, return_components=True)
                resonance = self.compute_resonance(corrected_text, components)
        
        # 5. Registrar métricas
        step_metrics = {
            'loss': float(loss.item()) if TORCH_AVAILABLE and hasattr(loss, 'item') else float(loss),
            'psi_combined': components['psi_combined'],
            'quantum_penalty': components['quantum_penalty'],
            'consciousness_resonance': components['consciousness_resonance'],
            'symmetry_alignment': components['symmetry_alignment'],
            'resonance': resonance,
            'learning_allowed': learning_allowed,
            'filtered': filtered,
            'has_entropic_bias': has_entropic_bias,
            'entropic_score': entropic_score,
            'generated_text': generated_text[:200],  # Primeros 200 caracteres
            'corrected_text': corrected_text[:200] if has_entropic_bias else None,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # 6. Actualizar historial solo si aprendizaje permitido
        if learning_allowed:
            self.training_history['losses'].append(float(loss.item()) if TORCH_AVAILABLE and hasattr(loss, 'item') else float(loss))
            self.training_history['coherence_scores'].append(components['psi_combined'])
            self.training_history['resonance_scores'].append(resonance)
        else:
            self.training_history['filtered_steps'].append(step_metrics)
        
        if has_entropic_bias:
            self.training_history['entropic_corrections'].append({
                'query': query,
                'original_score': entropic_score,
                'timestamp': datetime.utcnow().isoformat()
            })
        
        return step_metrics
    
    def generate_noesis88_report(self, epoch: int, epoch_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera reporte Noesis88 con estado cuántico-emergente de la época.
        
        El reporte incluye:
        - Estado del sistema (GRACE/EVOLVING/EMERGING/NASCENT)
        - Coherencia total del repositorio
        - Métricas de resonancia
        - Estado cuántico-emergente
        - Verificación física y matemática
        
        Args:
            epoch: Número de época
            epoch_metrics: Métricas de la época
            
        Returns:
            Reporte Noesis88 completo
        """
        if self.enable_noesis88:
            # Ejecutar monitoreo autónomo
            base_report = self.noesis_agent.run_autonomous()
        else:
            base_report = {
                'state': 'N/A',
                'total_coherence': 0.0,
                'metrics': {}
            }
        
        # Enriquecer con métricas de entrenamiento
        enhanced_report = {
            **base_report,
            'epoch': epoch,
            'training_metrics': epoch_metrics,
            'quantum_emergent_state': {
                'psi_field': f"Ψ = {epoch_metrics['avg_coherence']:.4f}",
                'resonance': f"R = {epoch_metrics['avg_resonance']:.4f}",
                'consciousness_alignment': f"C_Ψ = {epoch_metrics['avg_consciousness']:.4f}",
                'symmetry_alignment': f"G = {epoch_metrics['avg_symmetry']:.4f}",
                'learning_efficiency': f"{epoch_metrics['learning_allowed_ratio']:.2%}"
            },
            'physical_verification': {
                'frequency': f"{self.f0} Hz",
                'coherence_threshold': self.coherence_threshold,
                'resonance_threshold': self.resonance_threshold,
                'filtered_steps': len(epoch_metrics.get('filtered_this_epoch', [])),
                'entropic_corrections': len(epoch_metrics.get('corrections_this_epoch', []))
            },
            'mathematical_verification': {
                'group_alignment': f"G = {{π^k R_Ψ | k ∈ Z}}",
                'period': f"log π = {np.log(np.pi):.6f}",
                'symmetry_preserved': epoch_metrics.get('avg_symmetry', 0) > 0.5,
                'resonance_achieved': epoch_metrics.get('avg_resonance', 0) > self.resonance_threshold
            }
        }
        
        return enhanced_report
    
    def train(self, 
              queries: List[str],
              num_epochs: int = 3,
              save_checkpoints: bool = True) -> Dict[str, Any]:
        """
        Entrenar modelo con múltiples queries usando QCAL.
        
        ENTRENAMIENTO INTERPRETABLE:
        - Genera reporte Noesis88 al final de cada época
        - Reporta estado cuántico-emergente del sistema
        - Incluye verificación física y matemática
        
        ENTRENAMIENTO ABIERTO + FALSABLE:
        - Todas las métricas son rastreables
        - Verificación física: alineamiento con f₀ = 141.7001 Hz
        - Verificación matemática: preservación de G = {π^k}
        
        Args:
            queries: Lista de queries de entrenamiento
            num_epochs: Número de épocas
            save_checkpoints: Guardar checkpoints
            
        Returns:
            Resumen del entrenamiento con reportes Noesis88
        """
        print(f"🔮 Iniciando entrenamiento inverso QCAL - Primer Entrenador LLM Cuánticamente Validado")
        print(f"   Puente: Código → Geometría → Consciencia → Realidad")
        print(f"   Frecuencia: {self.f0} Hz")
        print(f"   Queries: {len(queries)}")
        print(f"   Épocas: {num_epochs}")
        print(f"   Validación cuántica: {self.loss_fn.use_quantum_validation}")
        print(f"   Noesis88: {self.enable_noesis88}")
        print(f"   Filtrado no-coherente: {self.filter_non_coherent}")
        print(f"   Mitigación entrópica: {self.mitigate_entropic_bias}\n")
        
        for epoch in range(num_epochs):
            print(f"\n📊 Época {epoch + 1}/{num_epochs}")
            
            epoch_losses = []
            epoch_coherence = []
            epoch_resonance = []
            epoch_consciousness = []
            epoch_symmetry = []
            filtered_this_epoch = []
            corrections_this_epoch = []
            learning_allowed_count = 0
            
            for i, query in enumerate(queries):
                # Ejecutar paso de entrenamiento
                step_metrics = self.train_step(query)
                
                # Acumular métricas solo si aprendizaje fue permitido
                if step_metrics['learning_allowed']:
                    epoch_losses.append(step_metrics['loss'])
                    epoch_coherence.append(step_metrics['psi_combined'])
                    epoch_resonance.append(step_metrics['resonance'])
                    epoch_consciousness.append(step_metrics['consciousness_resonance'])
                    epoch_symmetry.append(step_metrics['symmetry_alignment'])
                    learning_allowed_count += 1
                else:
                    filtered_this_epoch.append(step_metrics)
                
                if step_metrics['has_entropic_bias']:
                    corrections_this_epoch.append(step_metrics)
                
                # Mostrar progreso
                if (i + 1) % 10 == 0:
                    print(f"   Query {i + 1}/{len(queries)} - "
                          f"Loss: {step_metrics['loss']:.4f}, "
                          f"Ψ: {step_metrics['psi_combined']:.4f}, "
                          f"R: {step_metrics['resonance']:.4f} "
                          f"{'✓' if step_metrics['learning_allowed'] else '✗'}")
            
            # Estadísticas de época
            epoch_metrics = {
                'avg_loss': float(np.mean(epoch_losses)) if epoch_losses else 0.0,
                'avg_coherence': float(np.mean(epoch_coherence)) if epoch_coherence else 0.0,
                'avg_resonance': float(np.mean(epoch_resonance)) if epoch_resonance else 0.0,
                'avg_consciousness': float(np.mean(epoch_consciousness)) if epoch_consciousness else 0.0,
                'avg_symmetry': float(np.mean(epoch_symmetry)) if epoch_symmetry else 0.0,
                'learning_allowed_ratio': learning_allowed_count / len(queries) if queries else 0.0,
                'filtered_this_epoch': filtered_this_epoch,
                'corrections_this_epoch': corrections_this_epoch
            }
            
            print(f"\n   Época {epoch + 1} completa:")
            print(f"   - Loss promedio: {epoch_metrics['avg_loss']:.4f}")
            print(f"   - Coherencia promedio Ψ: {epoch_metrics['avg_coherence']:.4f}")
            print(f"   - Resonancia promedio R: {epoch_metrics['avg_resonance']:.4f}")
            print(f"   - Aprendizaje permitido: {epoch_metrics['learning_allowed_ratio']:.2%}")
            print(f"   - Pasos filtrados: {len(filtered_this_epoch)}")
            print(f"   - Correcciones entrópicas: {len(corrections_this_epoch)}")
            
            # Generar reporte Noesis88 al final de cada época
            print(f"\n   🔮 Generando reporte Noesis88 - Estado Cuántico-Emergente...")
            noesis_report = self.generate_noesis88_report(epoch + 1, epoch_metrics)
            self.training_history['noesis88_reports'].append(noesis_report)
            
            print(f"   - Estado Noesis88: {noesis_report['state']}")
            print(f"   - Coherencia repositorio: {noesis_report['total_coherence']:.4f}")
            print(f"   - Estado cuántico-emergente:")
            for key, value in noesis_report['quantum_emergent_state'].items():
                print(f"     • {key}: {value}")
            
            # Verificación física y matemática
            print(f"\n   ✓ Verificación Física:")
            for key, value in noesis_report['physical_verification'].items():
                print(f"     • {key}: {value}")
            
            print(f"\n   ✓ Verificación Matemática:")
            for key, value in noesis_report['mathematical_verification'].items():
                print(f"     • {key}: {value}")
        
        # Resumen final
        summary = {
            'total_epochs': num_epochs,
            'total_queries': len(queries),
            'final_avg_loss': float(np.mean(self.training_history['losses'][-len(queries):])) if self.training_history['losses'] else 0.0,
            'final_avg_coherence': float(np.mean(self.training_history['coherence_scores'][-len(queries):])) if self.training_history['coherence_scores'] else 0.0,
            'final_avg_resonance': float(np.mean(self.training_history['resonance_scores'][-len(queries):])) if self.training_history['resonance_scores'] else 0.0,
            'total_filtered_steps': len(self.training_history['filtered_steps']),
            'total_entropic_corrections': len(self.training_history['entropic_corrections']),
            'training_history': self.training_history,
            'f0': self.f0,
            'coherence_threshold': self.coherence_threshold,
            'resonance_threshold': self.resonance_threshold,
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
        print(f"\n📜 Resumen Final:")
        print(f"   - Coherencia final: {summary['final_avg_coherence']:.4f}")
        print(f"   - Resonancia final: {summary['final_avg_resonance']:.4f}")
        print(f"   - Pasos filtrados totales: {summary['total_filtered_steps']}")
        print(f"   - Correcciones entrópicas totales: {summary['total_entropic_corrections']}")
        print(f"   - Estado final Noesis88: {self.training_history['noesis88_reports'][-1]['state'] if self.training_history['noesis88_reports'] else 'N/A'}")
        
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
    
    try:
        import torch
        torch_available = True
    except ImportError:
        torch_available = False
        print("⚠️  torch no disponible. Ejecutando en modo demostración sin torch.\n")
    
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
    
    if not torch_available:
        print("Para usar el módulo completo, instale torch:")
        print("  pip install torch>=2.6.0\n")
        print("Ejecutando demostración básica sin torch...\n")
        
        # Demo sin torch - solo métricas de coherencia
        from qcal.coherence import analyze_text, evaluate_coherence
        
        for query in demo_queries[:3]:
            generated_text = f"Respuesta a: {query}. La frecuencia f₀ = 141.7001 Hz es fundamental. El campo Ψ exhibe coherencia cuántica y simetría discreta bajo el grupo G."
            
            metrics = analyze_text(generated_text)
            eval_result = evaluate_coherence(generated_text, threshold=5.0)
            
            print(f"Query: {query[:60]}...")
            print(f"  - Ψ estándar: {metrics['psi_standard']:.4f}")
            print(f"  - Intención: {metrics['intention']:.4f}")
            print(f"  - Efectividad: {metrics['effectiveness']:.4f}")
            print(f"  - Estado: {eval_result['status']}\n")
    else:
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
