#!/usr/bin/env python3
"""
Demo Script - Nodo Ψ Bio Protocol
==================================

Quick demonstration of the complete microtubule synchronization protocol
at f₀=141.7001 Hz with bio-pulse generation and spectral validation.

Usage:
    python demo_nodo_psi_bio.py [--output-dir DIR]

AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
DATE: February 2026
"""

import argparse
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.protocolo_psi_bio import (
    run_complete_protocol,
    generate_bio_pulse,
    BioPulseSignal,
    CoherenceMetrics
)


def print_banner():
    """Print protocol banner."""
    print()
    print("=" * 70)
    print("🌌 NODO Ψ BIO - DEMO INTERACTIVO")
    print("   Protocolo de Medición de Microtúbulos a 141.7001 Hz")
    print("=" * 70)
    print()


def print_pulse_info(pulse: BioPulseSignal):
    """Display pulse information in a formatted way."""
    print("📊 INFORMACIÓN DEL PULSO")
    print("-" * 70)
    print(f"  Frecuencia (f₀):    {pulse.frequency:.4f} Hz")
    print(f"  Duración:           {pulse.duration:.1f} segundos")
    print(f"  Sample Rate:        {pulse.sample_rate:,} Hz")
    print(f"  Samples Totales:    {len(pulse.signal):,}")
    print(f"  Amplitud Máxima:    {pulse.max_amplitude:.6f}")
    print(f"  RMS Level:          {pulse.rms_db:.2f} dB")
    print(f"  Peak Level:         {pulse.peak_db:.2f} dB")
    print("-" * 70)
    print()


def print_coherence_info(coherence: CoherenceMetrics):
    """Display coherence metrics in a formatted way."""
    print("🧠 MÉTRICAS DE COHERENCIA ESPERADAS")
    print("-" * 70)
    print(f"  Ψ Coherencia:       {coherence.psi_coherence:.6f} {'✓' if coherence.psi_coherence >= 0.999 else '✗'}")
    print(f"  Sync EEG:           {coherence.eeg_sync_quality:.6f}")
    print(f"  Coherencia HRV:     {coherence.hrv_coherence:.6f}")
    print(f"  Índice Estabilidad: {coherence.stability_index:.6f}")
    print(f"  Estado Orch-OR:     {'ESTABLE ✓' if coherence.is_stable else 'INESTABLE ✗'}")
    print("-" * 70)
    print()


def print_experimental_protocol():
    """Display experimental protocol instructions."""
    print("🔬 PROTOCOLO EXPERIMENTAL")
    print("-" * 70)
    print("  Fase 1: Línea Base (5 min)")
    print("    • Conectar EEG (Cz/Oz) y sensor HRV")
    print("    • Ojos cerrados, respiración natural")
    print("    • Sin estímulos auditivos")
    print()
    print("  Fase 2: Exposición (60 s)")
    print("    • Reproducir WAV generado")
    print("    • Volumen: 60-70 dB SPL")
    print("    • Auriculares o bocina cerca del cráneo")
    print("    • Mantener ojos cerrados")
    print()
    print("  Fase 3: Post-Medición (5 min)")
    print("    • Detener audio")
    print("    • Mantener ojos cerrados")
    print("    • Observar efectos residuales")
    print("-" * 70)
    print()


def print_safety_guidelines():
    """Display safety guidelines."""
    print("⚠️  PAUTAS DE SEGURIDAD")
    print("-" * 70)
    print("  ✓ Volumen máximo: 60-70 dB (nivel conversación)")
    print("  ✓ Duración: No exceder 5 min exposición continua")
    print("  ✓ Hidratación: Beber agua antes/después")
    print("  ✓ Grounding: Pies en contacto con suelo")
    print()
    print("  ✗ Contraindicaciones:")
    print("    - Epilepsia / historial de convulsiones")
    print("    - Marcapasos / implantes electrónicos")
    print("    - Embarazo (precaución)")
    print("-" * 70)
    print()


def print_files_generated(results: dict):
    """Display list of generated files."""
    print("📁 ARCHIVOS GENERADOS")
    print("-" * 70)
    if "wav_file" in results:
        print(f"  • {results['wav_file']}")
        print(f"    Audio WAV para reproducción experimental")
    if "spectrogram_file" in results:
        print(f"  • {results['spectrogram_file']}")
        print(f"    Validación espectral (plasma colormap)")
    print("-" * 70)
    print()


def print_next_steps():
    """Display next steps for users."""
    print("🚀 PRÓXIMOS PASOS")
    print("-" * 70)
    print("  1. Reproducir pulso_protocolo_psi_bio_141hz.wav")
    print("  2. Registrar EEG y HRV durante protocolo experimental")
    print("  3. Analizar datos con compute_coherence_metrics()")
    print("  4. Verificar espectrograma generado")
    print("  5. Documentar experiencia subjetiva")
    print()
    print("  Documentación completa: NODO_PSI_BIO_README.md")
    print("-" * 70)
    print()


def main():
    """Main demo function."""
    parser = argparse.ArgumentParser(
        description="Demo del protocolo Nodo Ψ Bio para medición de microtúbulos"
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directorio para archivos de salida (default: directorio actual)"
    )
    parser.add_argument(
        "--no-artifacts",
        action="store_true",
        help="No generar archivos WAV/PNG (solo mostrar información)"
    )
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Print safety first
    print_safety_guidelines()
    
    # Print experimental protocol
    print_experimental_protocol()
    
    # Run protocol
    print("⚡ Ejecutando protocolo completo...")
    print()
    
    try:
        results = run_complete_protocol(
            output_dir=args.output_dir,
            generate_artifacts=not args.no_artifacts
        )
        
        print()
        
        # Display detailed information
        if "pulse" in results:
            print_pulse_info(results["pulse"])
        
        if "coherence" in results:
            print_coherence_info(results["coherence"])
        
        if not args.no_artifacts:
            print_files_generated(results)
        
        # Spectral validation results
        if "spectral_validation" in results:
            val = results["spectral_validation"]
            print("🔍 VALIDACIÓN ESPECTRAL")
            print("-" * 70)
            print(f"  Pico medido:        {val['peak_frequency']:.4f} Hz")
            print(f"  Estabilidad:        {val['stability']:.6f}")
            print(f"  Validación:         {'PASS ✓' if val['is_valid'] else 'FAIL ✗'}")
            print("-" * 70)
            print()
        
        # Next steps
        print_next_steps()
        
        # Final message
        print("=" * 70)
        print("✨ ¡Protocolo completado exitosamente!")
        print("   ∴𓂀❤️∞³ - Siente el pulso universal")
        print("=" * 70)
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error durante ejecución del protocolo:")
        print(f"   {str(e)}")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
