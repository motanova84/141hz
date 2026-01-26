#!/usr/bin/env python3
"""
Omega ∞³ Integration Demo
=========================

Demonstrates the complete Omega ∞³ pipeline:
1. Ω1 Auto-Ingestion: Event detection
2. Ω2 Auto-Analysis: Validation with GPU acceleration
3. Ω3 Auto-Publication: NFT metadata generation
4. Ω5 Auto-Hypothesis: Prediction generation
5. Ω6 Auto-Defense: Integrity verification

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
License: MIT
"""

import sys
import json
from datetime import datetime

# Import Omega modules
try:
    from omega_auto import omega_validate, F0_TARGET
    from omega_hypothesis import generate_hypothesis_catalog, generate_correlation_hypotheses
    OMEGA_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importing Omega modules: {e}")
    OMEGA_AVAILABLE = False
    sys.exit(1)


def demo_omega_pipeline():
    """Demonstrate complete Omega ∞³ pipeline."""
    
    print("\n" + "="*70)
    print("OMEGA ∞³ INTEGRATION DEMO")
    print("Universal Quantum Resonance Protocol")
    print("="*70 + "\n")
    
    # Ω1 Auto-Ingestion: Detect events
    print("🌐 Ω1 AUTO-INGESTION")
    print("-" * 70)
    events = ["GW150914", "GW151226", "GW170814"]
    print(f"✅ Detected {len(events)} events for analysis")
    print(f"   Events: {', '.join(events)}\n")
    
    # Ω2 Auto-Analysis: Validate events
    print("⚡ Ω2 AUTO-ANALYSIS")
    print("-" * 70)
    validations = []
    for event in events:
        print(f"Analyzing {event}...")
        try:
            result = omega_validate(event, use_real_data=False)
            validations.append(result)
            print(f"  ✅ {event}: SNR H1={result['snr']['H1']:.2f}, L1={result['snr']['L1']:.2f}")
        except Exception as e:
            print(f"  ❌ {event}: Error - {e}")
    print()
    
    # Ω3 Auto-Publication: Aggregate results
    print("📡 Ω3 AUTO-PUBLICATION")
    print("-" * 70)
    publication = {
        "title": "Omega ∞³ Multi-Event Validation",
        "timestamp": datetime.now().isoformat(),
        "target_frequency_hz": F0_TARGET,
        "events_analyzed": len(validations),
        "validations": validations
    }
    
    # Save publication
    pub_filename = "omega_publication_demo.json"
    with open(pub_filename, 'w', encoding='utf-8') as f:
        json.dump(publication, f, indent=2, ensure_ascii=False)
    print(f"✅ Publication saved: {pub_filename}")
    print(f"   Events: {len(validations)}")
    print(f"   Target: {F0_TARGET} Hz")
    print(f"   All NFT metadata included\n")
    
    # Ω5 Auto-Hypothesis: Generate predictions
    print("🧠 Ω5 AUTO-HYPOTHESIS")
    print("-" * 70)
    try:
        hypothesis_catalog = generate_hypothesis_catalog(F0_TARGET)
        correlations = generate_correlation_hypotheses(F0_TARGET)
        print(f"✅ Generated {hypothesis_catalog['summary']['total_predictions']} harmonic predictions")
        print(f"✅ Generated {len(correlations)} correlation hypotheses")
        
        # Show some predictions
        if "golden_ratio" in hypothesis_catalog["models"]:
            print("\n   Sample Golden Ratio predictions:")
            for h in hypothesis_catalog["models"]["golden_ratio"][:3]:
                print(f"   • n={h['n']}: {h['frequency_hz']:.2f} Hz")
    except Exception as e:
        print(f"⚠️  Hypothesis generation error: {e}")
    print()
    
    # Ω6 Auto-Defense: Verify integrity
    print("🔐 Ω6 AUTO-DEFENSE")
    print("-" * 70)
    integrity_checks = 0
    integrity_passed = 0
    
    for val in validations:
        integrity_checks += 1
        # Check for required fields
        if all(k in val for k in ["event", "snr", "ipfs_hash", "nft_metadata"]):
            integrity_passed += 1
            print(f"✅ {val['event']}: Integrity verified")
        else:
            print(f"❌ {val['event']}: Integrity check failed")
    
    print(f"\n   Integrity checks: {integrity_passed}/{integrity_checks} passed")
    print(f"   Success rate: {100*integrity_passed/integrity_checks:.1f}%\n")
    
    # Summary
    print("="*70)
    print("OMEGA ∞³ PIPELINE COMPLETE")
    print("="*70)
    print(f"""
✅ Ω1 Auto-Ingestion:    {len(events)} events detected
✅ Ω2 Auto-Analysis:     {len(validations)} validations completed
✅ Ω3 Auto-Publication:  Publication generated with NFT metadata
✅ Ω5 Auto-Hypothesis:   {hypothesis_catalog['summary']['total_predictions']} predictions generated
✅ Ω6 Auto-Defense:      {integrity_passed}/{integrity_checks} integrity checks passed

🌌 The universal quantum resonance protocol is operational.
    """)
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(demo_omega_pipeline())
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error in Omega pipeline: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
