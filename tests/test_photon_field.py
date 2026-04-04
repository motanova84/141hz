"""
Test script for Photon Coherence Model

Verifies that all photon field modules function correctly and produce
expected results according to the QCAL ∞³ framework.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import os
import sys
import json
import numpy as np

# Test imports
print("=" * 60)
print("Testing Photon Coherence Model ∞³")
print("=" * 60)

def test_qcal_network():
    """Test qcal_network module imports and functions."""
    print("\n1️⃣  Testing qcal_network module...")
    
    try:
        from qcal_network.geo import calcular_curvatura_existencial
        from qcal_network.core import emitir_latido_existencial
        print("   ✅ Imports successful")
        
        # Test curvature calculation
        curvatura = calcular_curvatura_existencial(0.9999)
        assert abs(curvatura - 2.888) < 0.001, f"Expected ΔA₀ ≈ 2.888, got {curvatura}"
        print(f"   ✅ Curvature calculation: ΔA₀ = {curvatura:.4f}")
        
        # Test heartbeat emission (visual test)
        print("   Testing heartbeat emission:")
        emitir_latido_existencial(141.7001, 3)
        print("   ✅ Heartbeat emission successful")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_photon_field():
    """Test photon_field.py module."""
    print("\n2️⃣  Testing photon_field module...")
    
    try:
        import photon_field
        print("   ✅ Import successful")
        
        # Test energy calculation - import h from photon_field
        E = photon_field.energia_foton(888.0)
        expected_E = photon_field.h * 888.0
        assert abs(E - expected_E) < 1e-40, f"Energy mismatch: {E} vs {expected_E}"
        print(f"   ✅ Energy calculation: E = {E:.3e} J")
        
        # Test photon model
        t = 0.0
        psi = photon_field.modelo_foton(t, 888.0)
        assert abs(abs(psi) - 0.9999) < 0.001, f"Expected |ψ| ≈ 0.9999, got {abs(psi)}"
        print(f"   ✅ Photon model: |ψ(0)| = {abs(psi):.4f}")
        
        # Test activation function
        print("   Testing activation function:")
        photon_field.activar_foton_coherente()
        print("   ✅ Activation successful")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_wave_packet_resonator():
    """Test wave_packet_resonator.py module."""
    print("\n3️⃣  Testing wave_packet_resonator module...")
    
    try:
        import wave_packet_resonator
        print("   ✅ Import successful")
        
        # Test wave packet at t=0
        psi_0 = wave_packet_resonator.paquete_onda(0.0)
        assert abs(abs(psi_0) - 1.0) < 0.01, f"Expected |ψ(0)| ≈ 1.0, got {abs(psi_0)}"
        print(f"   ✅ Wave packet at t=0: |ψ| = {abs(psi_0):.4f}")
        
        # Test wave packet decay away from center
        psi_far = wave_packet_resonator.paquete_onda(0.1)
        assert abs(psi_far) < 0.01, f"Expected small amplitude far from center, got {abs(psi_far)}"
        print(f"   ✅ Wave packet decay: |ψ(0.1s)| = {abs(psi_far):.6f}")
        
        # Test array input
        t_array = np.linspace(-0.05, 0.05, 5)
        psi_array = wave_packet_resonator.paquete_onda(t_array)
        assert len(psi_array) == 5, f"Expected 5 values, got {len(psi_array)}"
        print(f"   ✅ Array processing: {len(psi_array)} values computed")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ai_photonic_memory():
    """Test ai_photonic_memory.py module."""
    print("\n4️⃣  Testing ai_photonic_memory module...")
    
    try:
        from ai_photonic_memory import MemoriaFotonica
        print("   ✅ Import successful")
        
        # Create memory instance
        mem = MemoriaFotonica(umbral_Ψ=0.888)
        assert mem.contar_registros() == 0, "Expected 0 initial records"
        print("   ✅ Memory instance created")
        
        # Test high coherence event (should register)
        result1 = mem.registrar("Test high coherence", Ψ_actual=0.9999)
        assert result1 is True, "High coherence event should register"
        assert mem.contar_registros() == 1, "Expected 1 record"
        print("   ✅ High coherence event registered")
        
        # Test low coherence event (should not register)
        result2 = mem.registrar("Test low coherence", Ψ_actual=0.700)
        assert result2 is False, "Low coherence event should not register"
        assert mem.contar_registros() == 1, "Expected still 1 record"
        print("   ✅ Low coherence event rejected")
        
        # Test retrieval
        registros = mem.obtener_registros()
        assert len(registros) == 1, "Expected 1 record in retrieval"
        assert registros[0]["Ψ"] == 0.9999, "Expected Ψ = 0.9999"
        print("   ✅ Record retrieval successful")
        
        # Test clear
        mem.limpiar()
        assert mem.contar_registros() == 0, "Expected 0 records after clear"
        print("   ✅ Memory clear successful")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration_files():
    """Test configuration JSON files."""
    print("\n5️⃣  Testing configuration files...")
    
    try:
        # Test bridge_888.net
        if os.path.exists("bridge_888.net"):
            with open("bridge_888.net", "r") as f:
                bridge_config = json.load(f)
            assert bridge_config["frecuencia"] == 888.0, "Expected frequency 888.0"
            assert bridge_config["red"] == "Bridge888", "Expected red name Bridge888"
            print("   ✅ bridge_888.net validated")
        else:
            print("   ⚠️  bridge_888.net not found")
            return False
        
        # Test photon_emitter_node.json
        if os.path.exists("photon_emitter_node.json"):
            with open("photon_emitter_node.json", "r") as f:
                emitter_config = json.load(f)
            assert emitter_config["frecuencia_emision"] == 888.0, "Expected emission frequency 888.0"
            assert emitter_config["estado"] == "activo", "Expected active state"
            print("   ✅ photon_emitter_node.json validated")
        else:
            print("   ⚠️  photon_emitter_node.json not found")
            return False
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    results = {
        "qcal_network": test_qcal_network(),
        "photon_field": test_photon_field(),
        "wave_packet_resonator": test_wave_packet_resonator(),
        "ai_photonic_memory": test_ai_photonic_memory(),
        "configuration_files": test_configuration_files()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🌟 All tests passed! Photon coherence model ∞³ operational")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
