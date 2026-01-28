"""
Core physical simulations for quantum biology phenomena
Includes: FMO, Olfactory, Magnetoreception, Microtubules, QCAL Biological Model
"""

from .fmo_photosynthesis import FMOComplex
from .olfactory_tunneling import OlfactoryReceptor
from .magnetoreception import CryptochromeCompass
from .microtubules import MicrotubuleNetwork

# QCAL biological model
from .qcal_biological_model import (
    SpectralField,
    BiologicalFilter,
    PhaseAccumulator,
    MagicicadaModel,
    create_environmental_cycles,
    validate_141hz_resonance
)

__all__ = [
    'FMOComplex', 
    'OlfactoryReceptor', 
    'CryptochromeCompass', 
    'MicrotubuleNetwork',
    'SpectralField',
    'BiologicalFilter',
    'PhaseAccumulator',
    'MagicicadaModel',
    'create_environmental_cycles',
    'validate_141hz_resonance'
]

