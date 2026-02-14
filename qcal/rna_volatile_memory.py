"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    RNA Volatile Memory - QCAL ∞³                           ║
║         Primera implementación de memoria no-binaria basada en             ║
║                      coherencia cuántica                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

⚡ PARADIGMA DE EMANACIÓN SOBRE POSESIÓN ⚡

Este módulo implementa memoria que NO almacena — EMANA.
La información no se guarda como bits estáticos, sino como ondas coherentes
que se propagan y decaen naturalmente en el tiempo.

Memoria ARN: Primer sistema de computación no-binaria basado en coherencia.
"""

__sello__ = "∴𓂀Ω∞³Φ"
__emanacion__ = "Ω Hz × 888 Hz × 141.7001 Hz × Φ = ∞³"

import math
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

# Import QCAL constants
from .constants import F0_HZ, A0_PHI, KAPPA_PI, F888_HZ, OMEGA_0


@dataclass
class RNAWavePacket:
    """
    Paquete de onda de información ARN.
    
    La información no se almacena — se emana como onda coherente que decae.
    Ψ(t) = Ψ₀ · exp(-t/τ) · cos(2πf₀t)
    
    Attributes:
        amplitude: Amplitud inicial Ψ₀
        frequency: Frecuencia de oscilación (Hz)
        decay_time: Tiempo de decaimiento τ (seconds)
        phase: Fase inicial φ₀ (radianes)
        created_at: Momento de emanación (kairos, no cronos)
        metadata: Información contextual
    """
    amplitude: float
    frequency: float
    decay_time: float
    phase: float
    created_at: datetime
    metadata: Dict[str, Any]

    def get_coherence(self, t: float) -> float:
        """
        Calcula la coherencia en el tiempo t.
        
        Ψ(t) = Ψ₀ · exp(-t/τ) · cos(2πf₀t + φ₀)
        
        Args:
            t: Tiempo desde la emanación (segundos)
            
        Returns:
            Coherencia en el tiempo t
        """
        decay = math.exp(-t / self.decay_time)
        oscillation = math.cos(2 * math.pi * self.frequency * t + self.phase)
        return self.amplitude * decay * oscillation
    
    def is_coherent(self, t: float, threshold: float = 0.05) -> bool:
        """
        Determina si la onda sigue siendo coherente.
        
        Args:
            t: Tiempo desde la emanación (segundos)
            threshold: Umbral de coherencia mínima
            
        Returns:
            True si |Ψ(t)| > threshold
        """
        return abs(self.get_coherence(t)) > threshold


class RNAVolatileMemory:
    """
    Memoria volátil ARN - Primera implementación computacional de memoria emanante.
    
    Paradigma:
    - La información NO se posee — se emana
    - Los datos NO se guardan — irradian
    - La memoria NO es estática — es dinámica y coherente
    
    Tiempo:
    - Opera en kairos (tiempo cualitativo) no cronos (tiempo cuantitativo)
    - El decaimiento natural es feature, no bug
    - La volatilidad es coherencia, no pérdida
    """
    
    def __init__(
        self,
        base_frequency: float = F0_HZ,
        default_decay_time: float = 60.0,  # 1 minuto
        coherence_threshold: float = 0.05,
    ):
        """
        Inicializa la memoria ARN.
        
        Args:
            base_frequency: Frecuencia base de emanación (Hz)
            default_decay_time: Tiempo de decaimiento por defecto (segundos)
            coherence_threshold: Umbral de coherencia para considerar onda activa
        """
        self.base_frequency = base_frequency
        self.default_decay_time = default_decay_time
        self.coherence_threshold = coherence_threshold
        
        # Almacén de ondas emanantes (no es "storage" — es campo de radiación)
        self._wave_field: Dict[str, RNAWavePacket] = {}
        
        # Frecuencias terapéuticas derivadas
        self.therapeutic_frequency = base_frequency * A0_PHI  # 141.7001 × Φ = 229.4 Hz
        
    def emanate(
        self,
        key: str,
        amplitude: float,
        frequency: Optional[float] = None,
        decay_time: Optional[float] = None,
        phase: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> RNAWavePacket:
        """
        Emana información como paquete de onda coherente.
        
        Args:
            key: Identificador de la emanación
            amplitude: Amplitud inicial de la onda
            frequency: Frecuencia de oscilación (usa base_frequency si None)
            decay_time: Tiempo de decaimiento (usa default si None)
            phase: Fase inicial
            metadata: Información contextual
            
        Returns:
            RNAWavePacket emanado
        """
        wave = RNAWavePacket(
            amplitude=amplitude,
            frequency=frequency or self.base_frequency,
            decay_time=decay_time or self.default_decay_time,
            phase=phase,
            created_at=datetime.now(),
            metadata=metadata or {}
        )
        
        self._wave_field[key] = wave
        return wave
    
    def resonate(self, key: str) -> Optional[float]:
        """
        Resuena con la onda emanada (lectura no-destructiva).
        
        En lugar de "leer" la información, resonamos con ella.
        La resonancia no destruye la onda — la revela.
        
        Args:
            key: Identificador de la emanación
            
        Returns:
            Coherencia actual de la onda, o None si ya decayó
        """
        if key not in self._wave_field:
            return None
        
        wave = self._wave_field[key]
        elapsed = (datetime.now() - wave.created_at).total_seconds()
        
        # Auto-limpieza: remueve ondas que ya no son coherentes
        if not wave.is_coherent(elapsed, self.coherence_threshold):
            del self._wave_field[key]
            return None
        
        return wave.get_coherence(elapsed)
    
    def get_field_coherence(self) -> float:
        """
        Calcula la coherencia total del campo de ondas.
        
        Ψ_total = √(Σ Ψᵢ²) / N
        
        Returns:
            Coherencia normalizada del campo completo
        """
        if not self._wave_field:
            return 0.0
        
        coherences = []
        now = datetime.now()
        
        for key, wave in list(self._wave_field.items()):
            elapsed = (now - wave.created_at).total_seconds()
            if wave.is_coherent(elapsed, self.coherence_threshold):
                coherences.append(wave.get_coherence(elapsed))
            else:
                # Auto-limpieza
                del self._wave_field[key]
        
        if not coherences:
            return 0.0
        
        # RMS de las coherencias
        return math.sqrt(sum(c**2 for c in coherences)) / len(coherences)
    
    def cleanup(self) -> int:
        """
        Limpia ondas que han decaído completamente.
        
        Returns:
            Número de ondas removidas
        """
        removed = 0
        now = datetime.now()
        
        for key, wave in list(self._wave_field.items()):
            elapsed = (now - wave.created_at).total_seconds()
            if not wave.is_coherent(elapsed, self.coherence_threshold):
                del self._wave_field[key]
                removed += 1
        
        return removed
    
    def get_active_waves(self) -> List[Tuple[str, float]]:
        """
        Obtiene todas las ondas actualmente coherentes.
        
        Returns:
            Lista de tuplas (key, coherencia_actual)
        """
        active = []
        now = datetime.now()
        
        for key, wave in self._wave_field.items():
            elapsed = (now - wave.created_at).total_seconds()
            coherence = wave.get_coherence(elapsed)
            if wave.is_coherent(elapsed, self.coherence_threshold):
                active.append((key, coherence))
        
        return active
    
    def calculate_therapeutic_resonance(
        self,
        patient_coherence: float
    ) -> float:
        """
        Calcula la frecuencia terapéutica personalizada.
        
        En el contexto médico, la ecuación de emanación se convierte en:
        Frecuencia terapéutica = 141.7001 Hz × (coherencia del paciente) × Φ
        
        Args:
            patient_coherence: Coherencia medida del paciente [0, 1]
            
        Returns:
            Frecuencia terapéutica en Hz
        """
        return self.base_frequency * patient_coherence * A0_PHI
    
    def __len__(self) -> int:
        """Retorna el número de ondas activas."""
        return len(self._wave_field)
    
    def __repr__(self) -> str:
        """Representación del campo de memoria ARN."""
        field_coherence = self.get_field_coherence()
        return (
            f"RNAVolatileMemory("
            f"waves={len(self._wave_field)}, "
            f"field_coherence={field_coherence:.4f}, "
            f"f₀={self.base_frequency} Hz)"
        )


def create_coherent_memory_field(
    memories: Dict[str, float],
    base_frequency: float = F0_HZ,
    decay_time: float = 60.0
) -> RNAVolatileMemory:
    """
    Crea un campo de memoria coherente a partir de múltiples emanaciones.
    
    Args:
        memories: Dict de {key: amplitude} para emanar
        base_frequency: Frecuencia base de todas las ondas
        decay_time: Tiempo de decaimiento compartido
        
    Returns:
        RNAVolatileMemory con ondas emanadas
    """
    memory = RNAVolatileMemory(
        base_frequency=base_frequency,
        default_decay_time=decay_time
    )
    
    for key, amplitude in memories.items():
        memory.emanate(key, amplitude)
    
    return memory


# Constantes exportadas del módulo
__all__ = [
    'RNAWavePacket',
    'RNAVolatileMemory',
    'create_coherent_memory_field',
    '__sello__',
    '__emanacion__'
]
