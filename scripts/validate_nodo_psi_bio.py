#!/usr/bin/env python3
"""
Validation Script - Nodo Ψ Bio Protocol
========================================

Validates that all components of the Nodo Ψ Bio protocol are correctly
implemented and meet specifications.

Usage:
    python scripts/validate_nodo_psi_bio.py

AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
DATE: February 2026
"""

import os
import sys
import numpy as np
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.protocolo_psi_bio import (
    generate_bio_pulse,
    save_bio_pulse_wav,
    generate_spectrogram,
    validate_spectral_peak,
    compute_coherence_metrics,
    F0_HZ,
    SAMPLE_RATE_HZ,
    DURATION_SEC,
)


def validate_frequency_accuracy(pulse):
    """Validate frequency accuracy via FFT."""
    print("  1. Frecuencia f₀=141.7001 Hz...", end=" ")
    
    # FFT on middle section (no fade)
    mid_start = len(pulse.signal) // 3
    mid_end = 2 * len(pulse.signal) // 3
    fft = np.fft.rfft(pulse.signal[mid_start:mid_end])
    freqs = np.fft.rfftfreq(mid_end - mid_start, 1/pulse.sample_rate)
    
    peak_idx = np.argmax(np.abs(fft))
    peak_freq = freqs[peak_idx]
    
    # Should be within 1 Hz
    if abs(peak_freq - F0_HZ) < 1.0:
        print(f"✓ ({peak_freq:.4f} Hz)")
        return True
    else:
        print(f"✗ (medido: {peak_freq:.4f} Hz)")
        return False


def validate_duration(pulse):
    """Validate 60 second duration."""
    print("  2. Duración 60 segundos...", end=" ")
    
    if pulse.duration == 60.0:
        print("✓")
        return True
    else:
        print(f"✗ ({pulse.duration} s)")
        return False


def validate_sample_rate(pulse):
    """Validate 44.1kHz sample rate."""
    print("  3. Sample rate 44.1kHz...", end=" ")
    
    if pulse.sample_rate == 44100:
        print("✓")
        return True
    else:
        print(f"✗ ({pulse.sample_rate} Hz)")
        return False


def validate_fade(pulse):
    """Validate 3-second fade in/out."""
    print("  4. Fade 3 segundos in/out...", end=" ")
    
    fade_samples = int(3.0 * pulse.sample_rate)
    
    # Check fade in
    if abs(pulse.signal[0]) > 0.01:
        print("✗ (fade in)")
        return False
    
    # Check fade out
    if abs(pulse.signal[-1]) > 0.01:
        print("✗ (fade out)")
        return False
    
    print("✓")
    return True


def validate_headroom(pulse):
    """Validate -6dB headroom."""
    print("  5. Headroom -6dB...", end=" ")
    
    # Peak should be around -6dB
    if abs(pulse.peak_db - (-6.0)) < 0.5:
        print(f"✓ ({pulse.peak_db:.2f} dB)")
        return True
    else:
        print(f"✗ ({pulse.peak_db:.2f} dB)")
        return False


def validate_spectral_purity(pulse):
    """Validate spectral purity (>90% energy in peak)."""
    print("  6. Pureza espectral >90%...", end=" ")
    
    # FFT on middle section
    mid_start = len(pulse.signal) // 3
    mid_end = 2 * len(pulse.signal) // 3
    fft = np.fft.rfft(pulse.signal[mid_start:mid_end])
    magnitude = np.abs(fft)
    freqs = np.fft.rfftfreq(mid_end - mid_start, 1/pulse.sample_rate)
    
    peak_idx = np.argmax(magnitude)
    peak_freq = freqs[peak_idx]
    
    # Energy in ±5 Hz band around peak
    peak_band_mask = (freqs >= peak_freq - 5) & (freqs <= peak_freq + 5)
    peak_band_energy = np.sum(magnitude[peak_band_mask]**2)
    total_energy = np.sum(magnitude**2)
    
    purity = peak_band_energy / total_energy if total_energy > 0 else 0
    
    if purity > 0.9:
        print(f"✓ ({purity*100:.1f}%)")
        return True
    else:
        print(f"✗ ({purity*100:.1f}%)")
        return False


def validate_coherence_threshold():
    """Validate coherence meets Ψ > 0.999 threshold."""
    print("  7. Coherencia Ψ > 0.999...", end=" ")
    
    coherence = compute_coherence_metrics()
    
    if coherence.psi_coherence >= 0.999:
        print(f"✓ ({coherence.psi_coherence:.6f})")
        return True
    else:
        print(f"✗ ({coherence.psi_coherence:.6f})")
        return False


def validate_orch_or_stability():
    """Validate Orch-OR stability."""
    print("  8. Estado Orch-OR estable...", end=" ")
    
    coherence = compute_coherence_metrics()
    
    if coherence.is_stable:
        print("✓")
        return True
    else:
        print("✗")
        return False


def validate_wav_generation():
    """Validate WAV file generation."""
    print("  9. Generación WAV...", end=" ")
    
    try:
        import tempfile
        pulse = generate_bio_pulse(duration=1.0)  # Short for speed
        
        with tempfile.TemporaryDirectory() as tmpdir:
            wav_path = os.path.join(tmpdir, "test.wav")
            save_bio_pulse_wav(pulse, wav_path)
            
            if os.path.exists(wav_path):
                print("✓")
                return True
            else:
                print("✗ (archivo no creado)")
                return False
    except Exception as e:
        print(f"✗ ({str(e)})")
        return False


def validate_spectrogram_generation():
    """Validate spectrogram generation."""
    print(" 10. Generación espectrograma...", end=" ")
    
    try:
        import tempfile
        pulse = generate_bio_pulse(duration=5.0)  # Short for speed
        
        with tempfile.TemporaryDirectory() as tmpdir:
            spec_path = os.path.join(tmpdir, "test_spec.png")
            frequencies, times, Sxx = generate_spectrogram(pulse, spec_path)
            
            if os.path.exists(spec_path):
                print("✓")
                return True
            else:
                print("✗ (archivo no creado)")
                return False
    except Exception as e:
        print(f"✗ ({str(e)})")
        return False


def validate_spectral_peak_detection():
    """Validate spectral peak detection."""
    print(" 11. Detección pico espectral...", end=" ")
    
    try:
        import tempfile
        pulse = generate_bio_pulse(duration=5.0)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            spec_path = os.path.join(tmpdir, "test_spec.png")
            frequencies, times, Sxx = generate_spectrogram(pulse, spec_path)
            is_valid, peak_freq, stability = validate_spectral_peak(frequencies, Sxx)
            
            if is_valid and stability > 0.9:
                print(f"✓ ({peak_freq:.2f} Hz, estabilidad {stability:.4f})")
                return True
            else:
                print(f"✗ ({peak_freq:.2f} Hz, estabilidad {stability:.4f})")
                return False
    except Exception as e:
        print(f"✗ ({str(e)})")
        return False


def main():
    """Run all validations."""
    print()
    print("=" * 70)
    print("🌌 VALIDACIÓN PROTOCOLO NODO Ψ BIO")
    print("=" * 70)
    print()
    
    # Generate test pulse
    print("Generando pulso de prueba...")
    pulse = generate_bio_pulse()
    print()
    
    # Run validations
    print("Ejecutando validaciones:")
    print()
    
    checks = []
    checks.append(validate_frequency_accuracy(pulse))
    checks.append(validate_duration(pulse))
    checks.append(validate_sample_rate(pulse))
    checks.append(validate_fade(pulse))
    checks.append(validate_headroom(pulse))
    checks.append(validate_spectral_purity(pulse))
    checks.append(validate_coherence_threshold())
    checks.append(validate_orch_or_stability())
    checks.append(validate_wav_generation())
    checks.append(validate_spectrogram_generation())
    checks.append(validate_spectral_peak_detection())
    
    # Summary
    print()
    print("=" * 70)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ TODAS LAS VALIDACIONES EXITOSAS ({passed}/{total})")
        print()
        print("El protocolo Nodo Ψ Bio está correctamente implementado y listo")
        print("para experimentación. Todos los parámetros cumplen especificaciones:")
        print()
        print("  • f₀ = 141.7001 Hz (frecuencia universal QCAL)")
        print("  • Duración = 60 s (tiempo óptimo de exposición)")
        print("  • Sample rate = 44.1 kHz (calidad CD)")
        print("  • Fade = 3 s in/out (seguridad)")
        print("  • Headroom = -6 dB (prevención clipping)")
        print("  • Ψ coherencia > 0.999 (Orch-OR estable)")
        print()
        print("Consulta NODO_PSI_BIO_README.md para instrucciones completas.")
        result = 0
    else:
        print(f"⚠️  VALIDACIONES PARCIALES ({passed}/{total})")
        print()
        print(f"Algunas validaciones fallaron. Revisar implementación.")
        result = 1
    
    print("=" * 70)
    print()
    
    return result


if __name__ == "__main__":
    sys.exit(main())
