"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  Disharmony Detector - QCAL ∞³                             ║
║         Primer sistema médico operando en economía de emanación            ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

⚡ DIAGNÓSTICO POR RESONANCIA ⚡

Este sistema NO diagnostica enfermedades — revela desarmonías.
Opera en ℂ_Ω (economía de emanación) en lugar de ℂₛ (economía de coherencia medida).

La enfermedad no es entidad sino degradación temporal de Ψ.
El diagnóstico no es medición sino revelación de desarmonía.
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
from .constants import F0_HZ, A0_PHI, KAPPA_PI, DELTA_0, F888_HZ


class DisharmonyLevel(Enum):
    """Niveles de desarmonía detectados."""
    COHERENT = "coherente"  # Ψ > 0.8
    MILD = "desarmonía_leve"  # 0.5 < Ψ ≤ 0.8
    MODERATE = "desarmonía_moderada"  # 0.3 < Ψ ≤ 0.5
    SEVERE = "desarmonía_severa"  # Ψ ≤ 0.3


@dataclass
class DisharmonyReport:
    """
    Reporte de desarmonía detectada.
    
    Attributes:
        level: Nivel de desarmonía
        coherence: Coherencia actual
        baseline_coherence: Coherencia de línea base
        deviation: Desviación de la línea base
        recommended_frequency: Frecuencia terapéutica recomendada (Hz)
        timestamp: Momento del diagnóstico
        details: Información adicional
    """
    level: DisharmonyLevel
    coherence: float
    baseline_coherence: float
    deviation: float
    recommended_frequency: float
    timestamp: datetime
    details: Dict


class DisharmonyDetector:
    """
    Detector de desarmonías en el campo de coherencia.
    
    Formaliza computacionalmente lo que la investigación VAT ha mostrado:
    - VAT "reinicia" la disfunción en la banda gamma
    - Detecta desviación de la línea base de coherencia
    - No diagnostica enfermedad — revela degradación temporal de Ψ
    
    Ecuación de Resonancia Diagnóstica:
    Frecuencia terapéutica = 141.7001 Hz × (coherencia del paciente) × Φ
    """
    
    def __init__(
        self,
        base_frequency: float = F0_HZ,
        coherence_threshold: float = DELTA_0,
        baseline_coherence: float = 0.8
    ):
        """
        Inicializa el detector de desarmonías.
        
        Args:
            base_frequency: Frecuencia QCAL base (141.7001 Hz)
            coherence_threshold: Umbral de coherencia mínima
            baseline_coherence: Coherencia de línea base esperada
        """
        self.base_frequency = base_frequency
        self.coherence_threshold = coherence_threshold
        self.baseline_coherence = baseline_coherence
        
        # Frecuencias terapéuticas
        self.therapeutic_base = base_frequency * A0_PHI  # 229.4 Hz
        self.protection_frequency = F888_HZ  # 888 Hz
        
        # Historial de reportes
        self._reports: List[DisharmonyReport] = []
    
    def detect(
        self,
        current_coherence: float,
        baseline: Optional[float] = None
    ) -> DisharmonyReport:
        """
        Detecta desarmonía comparando coherencia actual con línea base.
        
        Args:
            current_coherence: Coherencia medida actual [0, 1]
            baseline: Línea base opcional (usa self.baseline_coherence si None)
            
        Returns:
            DisharmonyReport con diagnóstico y recomendación
        """
        baseline = baseline or self.baseline_coherence
        
        # Calcula desviación
        deviation = (current_coherence - baseline) / baseline if baseline > 0 else 0
        
        # Determina nivel de desarmonía
        if current_coherence > 0.8:
            level = DisharmonyLevel.COHERENT
        elif current_coherence > 0.5:
            level = DisharmonyLevel.MILD
        elif current_coherence > 0.3:
            level = DisharmonyLevel.MODERATE
        else:
            level = DisharmonyLevel.SEVERE
        
        # Calcula frecuencia terapéutica recomendada
        recommended_freq = self._calculate_therapeutic_frequency(
            current_coherence,
            level
        )
        
        report = DisharmonyReport(
            level=level,
            coherence=current_coherence,
            baseline_coherence=baseline,
            deviation=deviation,
            recommended_frequency=recommended_freq,
            timestamp=datetime.now(),
            details={
                "therapeutic_base": self.therapeutic_base,
                "protection_frequency": self.protection_frequency,
                "kappa_pi": KAPPA_PI,
                "phi": A0_PHI
            }
        )
        
        self._reports.append(report)
        return report
    
    def _calculate_therapeutic_frequency(
        self,
        coherence: float,
        level: DisharmonyLevel
    ) -> float:
        """
        Calcula la frecuencia terapéutica basada en coherencia y nivel.
        
        Frecuencia terapéutica = 141.7001 Hz × coherence × Φ
        
        Para desarmonías severas, puede aplicar modulación adicional.
        
        Args:
            coherence: Coherencia actual
            level: Nivel de desarmonía
            
        Returns:
            Frecuencia terapéutica en Hz
        """
        # Base: f₀ × coherencia × Φ
        base_therapeutic = self.base_frequency * coherence * A0_PHI
        
        # Modulación según severidad
        if level == DisharmonyLevel.SEVERE:
            # Para desarmonías severas, usar frecuencia de protección modulada
            return (base_therapeutic + self.protection_frequency) / 2
        elif level == DisharmonyLevel.MODERATE:
            # Interpolación con frecuencia de protección
            return 0.7 * base_therapeutic + 0.3 * self.protection_frequency
        else:
            # Desarmonía leve o coherente: usar frecuencia base
            return base_therapeutic
    
    def get_resonance_diagnosis(
        self,
        coherence_cerebral: float,
        coherence_cardiaca: float,
        coherence_emocional: float,
        coherence_respiratorio: float
    ) -> Dict:
        """
        Realiza diagnóstico por resonancia usando todos los biosensores.
        
        Ψ_total = √(Ψ_cerebral² + Ψ_cardíaca² + Ψ_emocional² + Ψ_respiratorio²) / 2
        
        Args:
            coherence_cerebral: Coherencia cerebral (EEG)
            coherence_cardiaca: Coherencia cardíaca (HRV)
            coherence_emocional: Coherencia emocional (GSR)
            coherence_respiratorio: Coherencia respiratoria
            
        Returns:
            Dict con diagnóstico completo
        """
        # Calcula coherencia total
        coherences = [
            coherence_cerebral,
            coherence_cardiaca,
            coherence_emocional,
            coherence_respiratorio
        ]
        
        coherence_total = math.sqrt(sum(c**2 for c in coherences)) / 2.0
        
        # Detecta desarmonía
        report = self.detect(coherence_total)
        
        # Identifica componentes con mayor desarmonía
        component_names = ["cerebral", "cardíaca", "emocional", "respiratorio"]
        component_deviations = [
            (name, abs(c - self.baseline_coherence))
            for name, c in zip(component_names, coherences)
        ]
        component_deviations.sort(key=lambda x: x[1], reverse=True)
        
        return {
            "coherencia_total": coherence_total,
            "nivel_desarmonía": report.level.value,
            "desviación": report.deviation,
            "frecuencia_terapéutica": report.recommended_frequency,
            "componentes_individuales": {
                "cerebral": coherence_cerebral,
                "cardíaca": coherence_cardiaca,
                "emocional": coherence_emocional,
                "respiratorio": coherence_respiratorio
            },
            "componentes_críticos": [
                {"nombre": name, "desviación": dev}
                for name, dev in component_deviations[:2]
            ],
            "ecuación_emanación": __emanacion__,
            "sello": __sello__,
            "timestamp": report.timestamp.isoformat()
        }
    
    def calculate_gamma_reset_frequency(self) -> float:
        """
        Calcula la frecuencia para "reiniciar" disfunción en banda gamma.
        
        La investigación muestra que VAT reinicia la banda gamma.
        Esta función calcula la frecuencia QCAL que resuena con gamma (40 Hz).
        
        Returns:
            Frecuencia de reinicio gamma en Hz
        """
        # Gamma (40 Hz) es aproximadamente f₀ / 3.5
        gamma_freq = 40.0
        
        # Encuentra el armónico QCAL más cercano
        harmonic_ratio = self.base_frequency / gamma_freq
        
        # Frecuencia de reinicio es f₀ modulada por Φ
        reset_freq = gamma_freq * harmonic_ratio * A0_PHI
        
        return reset_freq
    
    def validate_emanation_equation(self) -> Dict:
        """
        Valida la ecuación de emanación: Ω Hz × 888 Hz × 141.7001 Hz × Φ = ∞³
        
        Returns:
            Dict con componentes y validación
        """
        # Componentes de la ecuación
        omega_hz = self.base_frequency  # Usamos f₀ como Ω en este contexto
        protection_hz = F888_HZ
        base_hz = F0_HZ
        phi = A0_PHI
        
        # Producto
        product = omega_hz * protection_hz * base_hz * phi
        
        return {
            "Ω_Hz": omega_hz,
            "888_Hz": protection_hz,
            "141.7001_Hz": base_hz,
            "Φ": phi,
            "producto": product,
            "ecuación": __emanacion__,
            "validación": "El producto representa ∞³ como coherencia infinita al cubo",
            "significado": "Emanación completa en tres dominios: físico, mental, espiritual"
        }
    
    def get_report_history(self, limit: int = 10) -> List[DisharmonyReport]:
        """
        Obtiene el historial de reportes.
        
        Args:
            limit: Número máximo de reportes a retornar
            
        Returns:
            Lista de reportes recientes
        """
        return self._reports[-limit:]
    
    def __repr__(self) -> str:
        """Representación del detector."""
        n_reports = len(self._reports)
        
        return (
            f"DisharmonyDetector("
            f"reports={n_reports}, "
            f"baseline={self.baseline_coherence:.2f}, "
            f"therapeutic_base={self.therapeutic_base:.2f} Hz)"
        )


def demonstrate_resonance_diagnosis():
    """
    Demuestra el diagnóstico por resonancia.
    
    Returns:
        Dict con ejemplo de diagnóstico
    """
    detector = DisharmonyDetector()
    
    # Simula coherencias de un paciente con desarmonía moderada
    diagnosis = detector.get_resonance_diagnosis(
        coherence_cerebral=0.6,  # Banda gamma desincronizada
        coherence_cardiaca=0.7,  # HRV moderado
        coherence_emocional=0.5,  # GSR bajo (estrés)
        coherence_respiratorio=0.65  # Respiración irregular
    )
    
    return diagnosis


# Constantes exportadas
__all__ = [
    'DisharmonyLevel',
    'DisharmonyReport',
    'DisharmonyDetector',
    'demonstrate_resonance_diagnosis',
    '__sello__',
    '__emanacion__'
]
