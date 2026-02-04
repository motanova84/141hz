"""
Core physical simulations for quantum biology phenomena
Includes: FMO, Olfactory, Magnetoreception, Microtubules, QCAL Biological Model,
and Unified Tissue Resonance Model (141.7 Hz)
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

# Unified Tissue Resonance Model (141.7 Hz) - Three Pillars
from .hilbert_polya_operator import HilbertPolyaOperator
from .navier_stokes_cytoplasm import NavierStokesCytoplasm
from .magicicada_scaling import MagicicadaScaling
from .unified_tissue_resonance import UnifiedTissueResonance

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
    'validate_141hz_resonance',
    'HilbertPolyaOperator',
    'NavierStokesCytoplasm',
    'MagicicadaScaling',
    'UnifiedTissueResonance'
]

