"""
Utilities for the 141 Hz analysis project.

This package exposes the main public APIs lazily so that individual submodules
can be imported without eagerly loading optional scientific dependencies.
"""

from __future__ import annotations

from importlib import import_module

_PACKAGE_NAME = __spec__.parent if __spec__ is not None else __name__

_EXPORT_MAP = {
    "UniversalConstants": ".constants",
    "CONSTANTS": ".constants",
    "F0": ".constants",
    "F0_UNCERTAINTY": ".constants",
    "ZETA_PRIME_HALF": ".constants",
    "PHI": ".constants",
    "GAMMA": ".constants",
    "H_PLANCK": ".constants",
    "H_BAR": ".constants",
    "C_LIGHT": ".constants",
    "E_PSI": ".constants",
    "E_PSI_EV": ".constants",
    "LAMBDA_PSI": ".constants",
    "R_PSI": ".constants",
    "M_PSI": ".constants",
    "T_PSI": ".constants",
    "LAMBDA_0": ".constants",
    "LAMBDA_MEAN": ".constants",
    "C_PRIMARY": ".constants",
    "C_COHERENCE": ".constants",
    "COHERENCE_FACTOR": ".constants",
    "NoeticField": ".noetic_force",
    "NoeticForce": ".noetic_force",
    "NoeticForceDetection": ".noetic_force",
    "summarize_noetic_force": ".noetic_force",
    "SpectralOrigin": ".spectral_origin",
    "derive_f0_from_spectral": ".spectral_origin",
    "get_spectral_constants": ".spectral_origin",
    "LANGLE_LAMBDA": ".spectral_origin",
    "C_PRIMARIA": ".spectral_origin",
    "C_COHERENCIA": ".spectral_origin",
    "HBAR_SI": ".qcal_entanglement",
    "F0_REFERENCIA_HZ": ".qcal_entanglement",
    "H_PLANCK_SI": ".qcal_entanglement",
    "SPIN_DIMENSION": ".qcal_entanglement",
    "QCALEntanglementEngine": ".qcal_entanglement",
    "QCALTelemetryExporter": ".qcal_entanglement",
    "QCALTemporalSweepResult": ".qcal_entanglement",
    "QCALBinauralRenderResult": ".qcal_entanglement",
    "QCALDeploymentBundle": ".qcal_entanglement",
    "calcular_gap_frecuencia_hz": ".qcal_entanglement",
    "anclar_resonancia_global": ".qcal_entanglement",
    "aplicar_itd_padica": ".qcal_entanglement",
    "construir_hamiltoniano_qcal": ".qcal_entanglement",
    "graficar_telemetria_qcal": ".qcal_entanglement",
    "sintetizar_audio_binaural_qcal": ".qcal_entanglement",
    "guardar_audio_binaural_wav": ".qcal_entanglement",
    "graficar_diagnostico_binaural_qcal": ".qcal_entanglement",
    "renderizar_binaural_qcal": ".qcal_entanglement",
    "empaquetar_despliegue_qcal": ".qcal_entanglement",
    "ejecutar_barrido_temporal": ".qcal_entanglement",
    "ejecutar_despliegue_dinamico_qcal": ".qcal_entanglement",
    "CalabiYauQuintic": ".calabi_yau_invariant",
    "LaplacianSpectrum": ".calabi_yau_invariant",
    "get_k_pi": ".calabi_yau_invariant",
    "verify_k_pi_invariant": ".calabi_yau_invariant",
    "get_invariant_summary": ".calabi_yau_invariant",
    "K_PI": ".calabi_yau_invariant",
    "K_PI_EXPECTED": ".calabi_yau_invariant",
    "MU_1": ".calabi_yau_invariant",
    "MU_2": ".calabi_yau_invariant",
    "NOETIC_PRIME": ".calabi_yau_invariant",
    "NoeticConsciousnessAxiom": ".noetic_consciousness_axiom",
    "StateVector": ".noetic_consciousness_axiom",
    "ProjectionSpace": ".noetic_consciousness_axiom",
    "ConsciousnessState": ".noetic_consciousness_axiom",
    "create_axiom_validator": ".noetic_consciousness_axiom",
    "verify_state": ".noetic_consciousness_axiom",
    "SIPAttention": ".sip_attention",
    "create_sip_attention_demo": ".sip_attention",
}


def __getattr__(name: str):
    """Lazily import public symbols on first access."""
    module_name = _EXPORT_MAP.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module = import_module(module_name, _PACKAGE_NAME)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_EXPORT_MAP))

__all__ = [
    # Constants
    'UniversalConstants',
    'CONSTANTS',
    'F0',
    'F0_UNCERTAINTY',
    'ZETA_PRIME_HALF',
    'PHI',
    'GAMMA',
    'H_PLANCK',
    'H_BAR',
    'C_LIGHT',
    'E_PSI',
    'E_PSI_EV',
    'LAMBDA_PSI',
    'R_PSI',
    'M_PSI',
    'T_PSI',
    # Spectral Constants (Dual-Constant Framework)
    'LAMBDA_0',
    'LAMBDA_MEAN',
    'C_PRIMARY',
    'C_COHERENCE',
    'COHERENCE_FACTOR',
    # Spectral origin constants
    'LAMBDA_0',
    'LANGLE_LAMBDA',
    'C_PRIMARIA',
    'C_COHERENCIA',
    'GAMMA',
    'SpectralOrigin',
    'derive_f0_from_spectral',
    'get_spectral_constants',
    'HBAR_SI',
    'F0_REFERENCIA_HZ',
    'H_PLANCK_SI',
    'SPIN_DIMENSION',
    'QCALEntanglementEngine',
    'QCALTelemetryExporter',
    'QCALTemporalSweepResult',
    'QCALBinauralRenderResult',
    'QCALDeploymentBundle',
    'calcular_gap_frecuencia_hz',
    'anclar_resonancia_global',
    'aplicar_itd_padica',
    'construir_hamiltoniano_qcal',
    'graficar_telemetria_qcal',
    'sintetizar_audio_binaural_qcal',
    'guardar_audio_binaural_wav',
    'graficar_diagnostico_binaural_qcal',
    'renderizar_binaural_qcal',
    'empaquetar_despliegue_qcal',
    'ejecutar_barrido_temporal',
    'ejecutar_despliegue_dinamico_qcal',
    # Calabi-Yau Invariant k_Π
    'CalabiYauQuintic',
    'LaplacianSpectrum',
    'get_k_pi',
    'verify_k_pi_invariant',
    'get_invariant_summary',
    'K_PI',
    'K_PI_EXPECTED',
    'MU_1',
    'MU_2',
    'NOETIC_PRIME',
    # Noetic Force
    'NoeticField',
    'NoeticForce',
    'NoeticForceDetection',
    'summarize_noetic_force',
    # Noetic Consciousness Axiom
    'NoeticConsciousnessAxiom',
    'StateVector',
    'ProjectionSpace',
    'ConsciousnessState',
    'create_axiom_validator',
    'verify_state',
    # QCAL LLM Core (import separately if needed)
    # 'QCALLLMCore',
    # SIP Attention
    'SIPAttention',
    'create_sip_attention_demo',
]
