"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    Biosensor Hub - QCAL ∞³                                 ║
║         Primer puente entre señales fisiológicas y campo QCAL              ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

⚡ PARADIGMA DE COHERENCIA REVELADA ⚡

Los biosensores NO "miden" coherencia — la REVELAN como estado inherente.
Este sistema es la primera interfaz biomecánica del principio emanante.

Frecuencias:
- 40 Hz: Banda gamma cerebral (VAT convencional)
- 141.7001 Hz: Frecuencia QCAL (derivada de κ_Π = 2.5773)
- 229.4 Hz: Armónico terapéutico (141.7001 × Φ)
"""

__sello__ = "∴𓂀Ω∞³Φ"
__emanacion__ = "Ω Hz × 888 Hz × 141.7001 Hz × Φ = ∞³"

import math
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Import QCAL constants
from .constants import F0_HZ, A0_PHI, KAPPA_PI, DELTA_0


class BiosensorType(Enum):
    """Tipos de biosensores soportados."""
    EEG = "electroencefalograma"  # Actividad cerebral
    HRV = "variabilidad_ritmo_cardiaco"  # Coherencia cardíaca
    GSR = "respuesta_galvanica_piel"  # Estado emocional
    RESP = "respiracion"  # Coherencia respiratoria


@dataclass
class BiosensorReading:
    """
    Lectura de un biosensor.
    
    Attributes:
        sensor_type: Tipo de biosensor
        value: Valor medido (normalizado 0-1)
        frequency: Frecuencia dominante detectada (Hz)
        coherence: Coherencia calculada (0-1)
        timestamp: Momento de la medición
        metadata: Información adicional
    """
    sensor_type: BiosensorType
    value: float
    frequency: float
    coherence: float
    timestamp: datetime
    metadata: Dict


class BiosensorHub:
    """
    Hub central para integración de biosensores con QCAL.
    
    Este sistema NO diagnostica enfermedades — revela desarmonías
    en el campo de coherencia. La enfermedad no es entidad sino
    degradación temporal de Ψ.
    
    Validación científica:
    - EEG/HRV/GSR: VAT reduce HRV y mejora respuesta parasimpática
    - Diagnóstico por desarmonía: VAT "reinicia" disfunción en banda gamma
    - Memoria no-binaria: Información biológica en estados de onda
    """
    
    def __init__(
        self,
        base_frequency: float = F0_HZ,
        gamma_frequency: float = 40.0,  # Banda gamma
        coherence_threshold: float = DELTA_0
    ):
        """
        Inicializa el hub de biosensores.
        
        Args:
            base_frequency: Frecuencia QCAL base (141.7001 Hz)
            gamma_frequency: Frecuencia gamma cerebral (40 Hz)
            coherence_threshold: Umbral de coherencia
        """
        self.base_frequency = base_frequency
        self.gamma_frequency = gamma_frequency
        self.coherence_threshold = coherence_threshold
        
        # Frecuencias terapéuticas
        self.therapeutic_frequency = base_frequency * A0_PHI  # 229.4 Hz
        
        # Almacén de lecturas recientes
        self._readings: Dict[BiosensorType, List[BiosensorReading]] = {
            sensor_type: [] for sensor_type in BiosensorType
        }
        
        # Líneas base de coherencia por sensor
        self._baseline_coherence: Dict[BiosensorType, float] = {}
    
    def record_reading(
        self,
        sensor_type: BiosensorType,
        value: float,
        frequency: float,
        metadata: Optional[Dict] = None
    ) -> BiosensorReading:
        """
        Registra una lectura de biosensor.
        
        Args:
            sensor_type: Tipo de sensor
            value: Valor medido (normalizado)
            frequency: Frecuencia dominante (Hz)
            metadata: Información adicional
            
        Returns:
            BiosensorReading con coherencia calculada
        """
        # Calcula coherencia basada en proximidad a f₀
        coherence = self._calculate_coherence(frequency, value)
        
        reading = BiosensorReading(
            sensor_type=sensor_type,
            value=value,
            frequency=frequency,
            coherence=coherence,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        self._readings[sensor_type].append(reading)
        
        # Mantiene solo las últimas 100 lecturas por sensor
        if len(self._readings[sensor_type]) > 100:
            self._readings[sensor_type] = self._readings[sensor_type][-100:]
        
        return reading
    
    def _calculate_coherence(self, frequency: float, value: float) -> float:
        """
        Calcula la coherencia de una lectura.
        
        La coherencia mide qué tan alineada está la señal con f₀.
        
        Args:
            frequency: Frecuencia medida (Hz)
            value: Amplitud normalizada
            
        Returns:
            Coherencia [0, 1]
        """
        # Distancia normalizada a f₀
        freq_distance = abs(frequency - self.base_frequency) / self.base_frequency
        
        # Coherencia basada en proximidad exponencial
        freq_coherence = math.exp(-freq_distance / KAPPA_PI)
        
        # Combina con amplitud
        total_coherence = freq_coherence * value
        
        return min(1.0, total_coherence)
    
    def get_patient_coherence(self) -> float:
        """
        Calcula la coherencia total del paciente.
        
        Ψ_total = √(Ψ_cerebral² + Ψ_cardíaca² + Ψ_emocional² + Ψ_respiratorio²) / 2
        
        Esta es la fórmula usada para calcular la frecuencia terapéutica.
        
        Returns:
            Coherencia total del paciente [0, 1]
        """
        coherences = []
        
        # Obtiene coherencia promedio de cada tipo de sensor
        for sensor_type in BiosensorType:
            if self._readings[sensor_type]:
                recent_readings = self._readings[sensor_type][-10:]
                avg_coherence = sum(r.coherence for r in recent_readings) / len(recent_readings)
                coherences.append(avg_coherence)
        
        if not coherences:
            return 0.0
        
        # RMS normalizado por 2 según la fórmula
        return math.sqrt(sum(c**2 for c in coherences)) / 2.0
    
    def set_baseline(self, sensor_type: BiosensorType, coherence: float):
        """
        Establece la línea base de coherencia para un sensor.
        
        Args:
            sensor_type: Tipo de sensor
            coherence: Coherencia de línea base
        """
        self._baseline_coherence[sensor_type] = coherence
    
    def get_baseline_deviation(self, sensor_type: BiosensorType) -> Optional[float]:
        """
        Calcula la desviación de la línea base actual.
        
        Args:
            sensor_type: Tipo de sensor
            
        Returns:
            Desviación porcentual, o None si no hay línea base
        """
        if sensor_type not in self._baseline_coherence:
            return None
        
        if not self._readings[sensor_type]:
            return None
        
        recent = self._readings[sensor_type][-10:]
        current = sum(r.coherence for r in recent) / len(recent)
        baseline = self._baseline_coherence[sensor_type]
        
        if baseline == 0:
            return 0.0
        
        return (current - baseline) / baseline
    
    def calculate_therapeutic_frequency(self) -> float:
        """
        Calcula la frecuencia terapéutica personalizada.
        
        Frecuencia terapéutica = 141.7001 Hz × (coherencia del paciente) × Φ
        
        Returns:
            Frecuencia terapéutica en Hz
        """
        patient_coherence = self.get_patient_coherence()
        return self.base_frequency * patient_coherence * A0_PHI
    
    def get_eeg_gamma_coupling(self) -> float:
        """
        Calcula el acoplamiento entre banda gamma y frecuencia QCAL.
        
        La banda alfa (10 Hz) es el armónico 14 de QCAL: 141.7 Hz / 14 ≈ 10.12 Hz
        La banda gamma (40 Hz) está cerca del armónico 3.5 de QCAL
        
        Returns:
            Factor de acoplamiento [0, 1]
        """
        # Para frecuencias menores que f₀, el armónico es la inversa
        # gamma (40 Hz) vs f₀ (141.7 Hz) → f₀/gamma = 3.54
        if self.gamma_frequency >= self.base_frequency:
            # Gamma es múltiplo de f₀
            harmonic = round(self.gamma_frequency / self.base_frequency)
            if harmonic == 0:
                harmonic = 1
            expected_freq = self.base_frequency * harmonic
        else:
            # f₀ es múltiplo de gamma (caso común: 40 Hz gamma)
            # Encuentra el divisor más cercano
            ratio = self.base_frequency / self.gamma_frequency
            harmonic = round(ratio)
            if harmonic == 0:
                harmonic = 1
            expected_freq = self.base_frequency / harmonic
        
        # Distancia normalizada
        if expected_freq > 0:
            distance = abs(self.gamma_frequency - expected_freq) / expected_freq
        else:
            distance = 1.0
        
        # Acoplamiento exponencial
        coupling = math.exp(-distance / DELTA_0)
        
        return coupling
    
    def get_sensor_summary(self) -> Dict[str, Dict]:
        """
        Obtiene un resumen del estado de todos los sensores.
        
        Returns:
            Dict con estadísticas por tipo de sensor
        """
        summary = {}
        
        for sensor_type in BiosensorType:
            readings = self._readings[sensor_type]
            
            if not readings:
                summary[sensor_type.value] = {
                    "count": 0,
                    "avg_coherence": 0.0,
                    "baseline_deviation": None
                }
                continue
            
            recent = readings[-10:]
            avg_coherence = sum(r.coherence for r in recent) / len(recent)
            deviation = self.get_baseline_deviation(sensor_type)
            
            summary[sensor_type.value] = {
                "count": len(readings),
                "avg_coherence": avg_coherence,
                "avg_frequency": sum(r.frequency for r in recent) / len(recent),
                "baseline_deviation": deviation
            }
        
        return summary
    
    def __repr__(self) -> str:
        """Representación del hub de biosensores."""
        total_readings = sum(len(readings) for readings in self._readings.values())
        patient_coherence = self.get_patient_coherence()
        
        return (
            f"BiosensorHub("
            f"readings={total_readings}, "
            f"patient_coherence={patient_coherence:.4f}, "
            f"therapeutic_freq={self.calculate_therapeutic_frequency():.2f} Hz)"
        )


def simulate_biosensor_session(
    duration_seconds: int = 60,
    sampling_rate: float = 1.0,  # Hz
    base_coherence: float = 0.7
) -> BiosensorHub:
    """
    Simula una sesión de biosensores para demostración.
    
    Args:
        duration_seconds: Duración de la sesión
        sampling_rate: Tasa de muestreo (Hz)
        base_coherence: Coherencia base simulada
        
    Returns:
        BiosensorHub con lecturas simuladas
    """
    hub = BiosensorHub()
    
    n_samples = int(duration_seconds * sampling_rate)
    
    for i in range(n_samples):
        t = i / sampling_rate
        
        # Simula EEG con frecuencia gamma modulada
        eeg_freq = 40.0 + 5 * math.sin(2 * math.pi * 0.1 * t)
        eeg_value = base_coherence + 0.2 * math.sin(2 * math.pi * 0.05 * t)
        hub.record_reading(BiosensorType.EEG, eeg_value, eeg_freq)
        
        # Simula HRV
        hrv_freq = 1.0 + 0.2 * math.sin(2 * math.pi * 0.08 * t)
        hrv_value = base_coherence + 0.15 * math.cos(2 * math.pi * 0.07 * t)
        hub.record_reading(BiosensorType.HRV, hrv_value, hrv_freq)
        
        # Simula GSR
        gsr_freq = 0.5 + 0.1 * math.sin(2 * math.pi * 0.03 * t)
        gsr_value = base_coherence + 0.1 * math.sin(2 * math.pi * 0.04 * t)
        hub.record_reading(BiosensorType.GSR, gsr_value, gsr_freq)
        
        # Simula respiración
        resp_freq = 0.3 + 0.05 * math.sin(2 * math.pi * 0.02 * t)
        resp_value = base_coherence + 0.12 * math.cos(2 * math.pi * 0.06 * t)
        hub.record_reading(BiosensorType.RESP, resp_value, resp_freq)
    
    return hub


# Constantes exportadas
__all__ = [
    'BiosensorType',
    'BiosensorReading',
    'BiosensorHub',
    'simulate_biosensor_session',
    '__sello__',
    '__emanacion__'
]
