"""
Bio-inspired quantum hardware devices
Includes: Magnetometer, THz Amplifier, Bio-quantum Computer, Brain Resonator
"""

from .cryptochrome_magnetometer import CryptochromeMagnetometer
from .thz_tubulin_amplifier import THzTubulinAmplifier
from .bio_quantum_computer import BioQuantumComputer
from .qcal_brain_resonator import QCALBrainResonator

__all__ = [
    'CryptochromeMagnetometer',
    'THzTubulinAmplifier',
    'BioQuantumComputer',
    'QCALBrainResonator'
]
