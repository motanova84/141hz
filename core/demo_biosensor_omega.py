#!/usr/bin/env python3
"""
Demo: Biosensor QCAL Integration - Primera Interfaz Biomecánica del Principio Emanante

Este script demuestra la integración completa de:
1. RNA Volatile Memory - memoria que emana, no almacena
2. Biosensor Hub - revela coherencia inherente
3. Disharmony Detector - detecta desarmonías, no enfermedades

Paradigma ℂ_Ω: Economía de Emanación
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from qcal.rna_volatile_memory import RNAVolatileMemory, __sello__ as rna_sello
from qcal.biosensor_hub import BiosensorHub, BiosensorType, simulate_biosensor_session
from qcal.disharmony_detector import DisharmonyDetector, demonstrate_resonance_diagnosis
from qcal.constants import F0_HZ, A0_PHI, F888_HZ


def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def demo_rna_volatile_memory():
    """Demonstrates RNA volatile memory."""
    print_header("1. RNA Volatile Memory - Memoria Emanante")
    
    print("\n📡 Creando memoria RNA que EMANA, no almacena...")
    memory = RNAVolatileMemory(
        base_frequency=F0_HZ,
        default_decay_time=30.0  # 30 segundos de decaimiento
    )
    
    print(f"✓ Memoria creada: {memory}")
    print(f"✓ Sello: {rna_sello}")
    
    # Emanate information
    print("\n🌊 Emanando información sobre estado del paciente...")
    memory.emanate(
        key="coherencia_inicial",
        amplitude=0.8,
        metadata={"paciente": "demo", "tipo": "baseline"}
    )
    
    memory.emanate(
        key="coherencia_cerebral",
        amplitude=0.7,
        metadata={"sensor": "EEG"}
    )
    
    memory.emanate(
        key="coherencia_cardiaca",
        amplitude=0.75,
        metadata={"sensor": "HRV"}
    )
    
    print(f"✓ Ondas emanadas: {len(memory)}")
    print(f"✓ Coherencia del campo: {memory.get_field_coherence():.4f}")
    
    # Resonate (read)
    print("\n🎵 Resonando con información emanada...")
    for key, coherence in memory.get_active_waves():
        print(f"  {key}: Ψ = {coherence:.4f}")
    
    return memory


def demo_biosensor_hub():
    """Demonstrates biosensor hub."""
    print_header("2. Biosensor Hub - Revelación de Coherencia")
    
    print("\n🔬 Simulando sesión de biosensores (60 segundos)...")
    hub = simulate_biosensor_session(
        duration_seconds=60,
        sampling_rate=1.0,
        base_coherence=0.7
    )
    
    print(f"✓ Hub: {hub}")
    
    # Patient coherence
    patient_coh = hub.get_patient_coherence()
    print(f"\n💫 Coherencia del paciente: {patient_coh:.4f}")
    
    # Therapeutic frequency
    therapeutic_freq = hub.calculate_therapeutic_frequency()
    print(f"🎼 Frecuencia terapéutica: {therapeutic_freq:.2f} Hz")
    print(f"   (f₀ × coherencia × Φ = {F0_HZ:.4f} × {patient_coh:.4f} × {A0_PHI:.4f})")
    
    # EEG-gamma coupling
    gamma_coupling = hub.get_eeg_gamma_coupling()
    print(f"🧠 Acoplamiento EEG-gamma: {gamma_coupling:.4f}")
    
    # Summary
    print("\n📊 Resumen de sensores:")
    summary = hub.get_sensor_summary()
    for sensor, stats in summary.items():
        if stats["count"] > 0:
            print(f"  {sensor}:")
            print(f"    Lecturas: {stats['count']}")
            print(f"    Coherencia promedio: {stats['avg_coherence']:.4f}")
            print(f"    Frecuencia promedio: {stats['avg_frequency']:.2f} Hz")
    
    return hub


def demo_disharmony_detector():
    """Demonstrates disharmony detector."""
    print_header("3. Disharmony Detector - Diagnóstico por Resonancia")
    
    print("\n⚕️ Realizando diagnóstico por resonancia...")
    diagnosis = demonstrate_resonance_diagnosis()
    
    print(f"✓ Coherencia total: {diagnosis['coherencia_total']:.4f}")
    print(f"✓ Nivel de desarmonía: {diagnosis['nivel_desarmonía']}")
    print(f"✓ Frecuencia terapéutica: {diagnosis['frecuencia_terapéutica']:.2f} Hz")
    
    print("\n🔍 Componentes individuales:")
    for name, value in diagnosis['componentes_individuales'].items():
        print(f"  Ψ_{name}: {value:.4f}")
    
    print("\n⚠️ Componentes críticos (mayor desarmonía):")
    for comp in diagnosis['componentes_críticos']:
        print(f"  {comp['nombre']}: desviación = {comp['desviación']:.4f}")
    
    # Validate emanation equation
    print("\n✨ Validando ecuación de emanación...")
    detector = DisharmonyDetector()
    validation = detector.validate_emanation_equation()
    
    print(f"✓ Ecuación: {validation['ecuación']}")
    print(f"✓ Producto: {validation['producto']:.2e}")
    print(f"✓ Significado: {validation['significado']}")
    
    return diagnosis


def demo_integrated_system():
    """Demonstrates integrated system."""
    print_header("4. Sistema Integrado - Paradigma ℂ_Ω")
    
    print("\n🌟 Integrando memoria ARN + biosensores + detector...")
    
    # Create components
    memory = RNAVolatileMemory(base_frequency=F0_HZ)
    hub = BiosensorHub(base_frequency=F0_HZ)
    detector = DisharmonyDetector(baseline_coherence=0.8)
    
    # Simulate patient data
    print("\n📈 Registrando datos del paciente...")
    hub.record_reading(BiosensorType.EEG, 0.7, 42.0, {"nota": "banda gamma"})
    hub.record_reading(BiosensorType.HRV, 0.75, 1.2, {"nota": "variabilidad cardíaca"})
    hub.record_reading(BiosensorType.GSR, 0.6, 0.5, {"nota": "respuesta galvánica"})
    hub.record_reading(BiosensorType.RESP, 0.68, 0.3, {"nota": "respiración"})
    
    # Get patient coherence
    patient_coh = hub.get_patient_coherence()
    
    # Emanate to memory
    print(f"🌊 Emanando coherencia ({patient_coh:.4f}) a memoria ARN...")
    memory.emanate("coherencia_actual", patient_coh)
    
    # Detect disharmony
    print(f"🔍 Detectando desarmonía...")
    report = detector.detect(patient_coh)
    
    print(f"\n✓ Nivel: {report.level.value}")
    print(f"✓ Desviación de línea base: {report.deviation:.2%}")
    print(f"✓ Frecuencia terapéutica recomendada: {report.recommended_frequency:.2f} Hz")
    
    # Calculate therapeutic resonance from memory
    therapeutic_from_memory = memory.calculate_therapeutic_resonance(patient_coh)
    print(f"✓ Frecuencia desde memoria ARN: {therapeutic_from_memory:.2f} Hz")
    
    print("\n🎯 Sistema operando completamente en paradigma ℂ_Ω:")
    print("   • Memoria emana (no almacena)")
    print("   • Biosensores revelan (no miden)")
    print("   • Detector diagnostica desarmonía (no enfermedad)")
    
    return {
        "patient_coherence": patient_coh,
        "disharmony_level": report.level.value,
        "therapeutic_frequency": report.recommended_frequency,
        "memory_field_coherence": memory.get_field_coherence()
    }


def create_log_entry(results: dict):
    """Creates log entry for the integration."""
    print_header("5. Registro del Sistema")
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "sello": "∴𓂀Ω∞³Φ",
        "evento": "BIOSENSOR_OMEGA_INTEGRADO",
        "capacidad": "Memoria ARN + Diagnóstico por resonancia",
        "frecuencia_base": F0_HZ,
        "phi": A0_PHI,
        "frecuencia_terapeutica": F0_HZ * A0_PHI,
        "frecuencia_proteccion": F888_HZ,
        "modulos": [
            "qcal.rna_volatile_memory",
            "qcal.biosensor_hub",
            "qcal.disharmony_detector"
        ],
        "paradigma": "ℂ_Ω",
        "ecuacion_emanacion": "Ω Hz × 888 Hz × 141.7001 Hz × Φ = ∞³",
        "resultados_demo": results
    }
    
    print("\n📝 Entrada de log generada:")
    print(json.dumps(log_entry, indent=2, ensure_ascii=False))
    
    # Save to file
    log_file = project_root / "logs" / "biosensor_omega_integration.json"
    log_file.parent.mkdir(exist_ok=True)
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_entry, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Log guardado en: {log_file}")
    
    return log_entry


def main():
    """Main demonstration."""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  BIOSENSOR OMEGA EMANACIÓN - Primera Interfaz Biomecánica  ".center(68) + "║")
    print("║" + "  del Principio Emanante                                    ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("║" + f"  Sello: ∴𓂀Ω∞³Φ".center(68) + "║")
    print("║" + f"  Ecuación: Ω Hz × 888 Hz × 141.7001 Hz × Φ = ∞³".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Run demos
    demo_rna_volatile_memory()
    demo_biosensor_hub()
    demo_disharmony_detector()
    results = demo_integrated_system()
    create_log_entry(results)
    
    print_header("Demo Completado")
    print("\n✨ El sistema opera completamente en paradigma ℂ_Ω")
    print("✨ Primera implementación de memoria emanante")
    print("✨ Primer puente biosensor-QCAL")
    print("✨ Primer diagnóstico por resonancia")
    print("\n🎯 Significado histórico: Transición de ℂₛ → ℂ_Ω\n")


if __name__ == "__main__":
    main()
