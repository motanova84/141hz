"""
QCAL Falsifiability Experimental Framework

This module implements the experimental framework for falsifying QCAL predictions
through precision energy control and frequency response measurements.

Components:
- energy_controller: Maintains constant energy (±0.03%) across frequencies
- frequency_response_analyzer: Measures ΔF(ω) with ~0.3% precision
- falsifiability_experiment: Orchestrates critical tests with statistical analysis
"""

__version__ = "1.0.0"

from .energy_controller import (
    EnergyController,
    AdaptiveAmplitudeController,
    EnergyMonitor
)
from .frequency_response_analyzer import (
    FrequencyResponseAnalyzer,
    SpectralPeakDetector,
    LorentzianResonanceModel
)
from .falsifiability_experiment import (
    FalsifiabilityExperiment,
    ExperimentResult,
    Verdict
)

__all__ = [
    'EnergyController',
    'AdaptiveAmplitudeController',
    'EnergyMonitor',
    'FrequencyResponseAnalyzer',
    'SpectralPeakDetector',
    'LorentzianResonanceModel',
    'FalsifiabilityExperiment',
    'ExperimentResult',
    'Verdict'
]
