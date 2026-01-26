"""
Pytest tests for quantum biology core module validation
"""

import pytest
import numpy as np
from modules.quantum_biology.core import (
    FMOComplex,
    OlfactoryReceptor,
    CryptochromeCompass,
    MicrotubuleNetwork
)


class TestFMOComplex:
    """Test FMO photosynthesis quantum coherence"""
    
    def test_initialization(self):
        fmo = FMOComplex(n_chromophores=7, temperature=300.0)
        assert fmo.n_chromophores == 7
        assert fmo.temperature == 300.0
        assert fmo.hamiltonian.shape == (7, 7)
    
    def test_coherence_calculation(self):
        fmo = FMOComplex(temperature=300.0)
        psi = fmo.calculate_coherence(time_ps=1.0)
        assert 0.0 <= psi <= 1.0
        assert psi >= 0.9, "FMO coherence should be >= 0.9"
    
    def test_energy_transfer(self):
        fmo = FMOComplex(temperature=300.0)
        efficiency = fmo.energy_transfer_efficiency(time_ps=10.0)
        assert 0.0 <= efficiency <= 1.0
    
    def test_validation_passes(self):
        fmo = FMOComplex(temperature=300.0)
        results = fmo.validate_coherence(target_psi=0.99)
        assert results['validation_passed'] == True
        assert results['max_coherence'] >= 0.99


class TestOlfactoryReceptor:
    """Test olfactory quantum tunneling"""
    
    def test_initialization(self):
        receptor = OlfactoryReceptor(temperature=310.0)
        assert receptor.temperature == 310.0
    
    def test_tunneling_probability(self):
        receptor = OlfactoryReceptor()
        prob = receptor.tunneling_probability(
            barrier_height_eV=0.3,
            barrier_width_nm=0.5,
            electron_energy_eV=0.2
        )
        assert 0.0 <= prob <= 1.0
    
    def test_isotope_discrimination(self):
        receptor = OlfactoryReceptor()
        rate_H, rate_D = receptor.isotope_discrimination(freq_H=100.0, freq_D=73.0)
        assert rate_H > rate_D, "Hydrogen should tunnel faster than deuterium"
    
    def test_coherence_calculation(self):
        receptor = OlfactoryReceptor()
        psi = receptor.calculate_coherence(vibration_freq_THz=100.0)
        assert 0.0 <= psi <= 1.0
        assert psi >= 0.85, "Olfactory coherence should be >= 0.85"
    
    def test_validation_passes(self):
        receptor = OlfactoryReceptor()
        results = receptor.validate_coherence(target_psi=0.95)
        assert results['validation_passed'] == True
        assert results['max_coherence'] >= 0.95


class TestCryptochromeCompass:
    """Test magnetoreception spin entanglement"""
    
    def test_initialization(self):
        compass = CryptochromeCompass(temperature=310.0)
        assert compass.temperature == 310.0
    
    def test_radical_pair_yield(self):
        compass = CryptochromeCompass()
        phi_S, phi_T = compass.radical_pair_yield(B_field_uT=50.0)
        assert 0.0 <= phi_S <= 1.0
        assert 0.0 <= phi_T <= 1.0
        assert abs(phi_S + phi_T - 1.0) < 0.01, "Yields should sum to 1"
    
    def test_directional_sensitivity(self):
        compass = CryptochromeCompass()
        phi_S_0, _ = compass.radical_pair_yield(50.0, angle_deg=0)
        phi_S_90, _ = compass.radical_pair_yield(50.0, angle_deg=90)
        assert phi_S_0 != phi_S_90, "Yields should depend on field direction"
    
    def test_coherence_time(self):
        compass = CryptochromeCompass()
        T2 = compass.spin_coherence_time(B_field_uT=50.0)
        assert T2 > 0, "Coherence time should be positive"
    
    def test_coherence_calculation(self):
        compass = CryptochromeCompass()
        psi = compass.calculate_coherence(B_field_uT=50.0)
        assert 0.0 <= psi <= 1.0
        assert psi >= 0.85, "Magnetoreception coherence should be >= 0.85"
    
    def test_validation_passes(self):
        compass = CryptochromeCompass()
        results = compass.validate_coherence(target_psi=0.92)
        assert results['validation_passed'] == True
        assert results['max_coherence'] >= 0.92


class TestMicrotubuleNetwork:
    """Test microtubule neuronal coherence"""
    
    def test_initialization(self):
        mt = MicrotubuleNetwork(n_tubulins=1000)
        assert mt.n_tubulins == 1000
        assert mt.temperature == 310.0
        assert mt.f0_neural == 141.7001
    
    def test_decoherence_time(self):
        mt = MicrotubuleNetwork()
        tau = mt.decoherence_time()
        assert tau > 0, "Decoherence time should be positive"
    
    def test_frohlich_coherence(self):
        mt = MicrotubuleNetwork()
        amplitude = mt.fröhlich_coherence(pumping_rate=1e15)
        assert 0.0 <= amplitude <= 1.0
    
    def test_neural_coupling(self):
        mt = MicrotubuleNetwork()
        coupling = mt.neural_resonance_coupling()
        assert 0.0 <= coupling <= 1.0
    
    def test_coherence_calculation(self):
        mt = MicrotubuleNetwork()
        psi = mt.calculate_coherence(time_ms=10.0)
        assert 0.0 <= psi <= 1.0
        assert psi >= 0.80, "Microtubule coherence should be >= 0.80"
    
    def test_consciousness_integration(self):
        mt = MicrotubuleNetwork()
        results = mt.consciousness_integration(threshold_events=100)
        assert 'reduction_time_ms' in results
        assert 'consciousness_freq_Hz' in results
        assert results['reduction_time_ms'] > 0
    
    def test_validation_passes(self):
        mt = MicrotubuleNetwork()
        results = mt.validate_coherence(target_psi=0.90)
        assert results['validation_passed'] == True
        assert results['max_coherence'] >= 0.90


class TestIntegratedValidation:
    """Test all four systems together"""
    
    def test_all_systems_validate(self):
        """Verify all four quantum biology systems pass validation"""
        
        # FMO
        fmo = FMOComplex(temperature=300.0)
        fmo_results = fmo.validate_coherence(target_psi=0.99)
        
        # Olfactory
        olfactory = OlfactoryReceptor(temperature=310.0)
        olf_results = olfactory.validate_coherence(target_psi=0.95)
        
        # Magnetoreception
        magneto = CryptochromeCompass(temperature=310.0)
        mag_results = magneto.validate_coherence(target_psi=0.92)
        
        # Microtubules
        microtubule = MicrotubuleNetwork(n_tubulins=1000, temperature=310.0)
        mt_results = microtubule.validate_coherence(target_psi=0.90)
        
        # All should pass
        assert fmo_results['validation_passed'] == True
        assert olf_results['validation_passed'] == True
        assert mag_results['validation_passed'] == True
        assert mt_results['validation_passed'] == True
        
        # Verify coherence hierarchy
        assert fmo_results['max_coherence'] >= mag_results['max_coherence']
        assert mag_results['max_coherence'] >= mt_results['max_coherence']
    
    def test_coherence_summary_table(self):
        """Generate summary table matching problem statement"""
        
        systems = {
            'FMO': (FMOComplex(temperature=300.0), 0.99),
            'Olfactory': (OlfactoryReceptor(temperature=310.0), 0.95),
            'Magnetoreception': (CryptochromeCompass(temperature=310.0), 0.92),
            'Microtubules': (MicrotubuleNetwork(n_tubulins=1000), 0.90)
        }
        
        print("\n" + "="*80)
        print("FASE 1: VALIDACIÓN CIENTÍFICA (100%)")
        print("="*80)
        print(f"{'Sistema':<25} {'Fenómeno':<30} {'Coherencia Ψ':<15} {'Estado'}")
        print("-"*80)
        
        for name, (system, target) in systems.items():
            if name == 'FMO':
                results = system.validate_coherence(target)
                phenomenon = 'Superposición energética'
            elif name == 'Olfactory':
                results = system.validate_coherence(target)
                phenomenon = 'Túnel resonante'
            elif name == 'Magnetoreception':
                results = system.validate_coherence(target)
                phenomenon = 'Entrelazamiento de espín'
            else:
                results = system.validate_coherence(target)
                phenomenon = 'Coherencia colectiva'
            
            print(f"{results['system']:<25} {phenomenon:<30} ~{results['max_coherence']:.2f}{'':>9} {results['status']}")
        
        print("="*80)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
