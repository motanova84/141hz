#!/usr/bin/env python3
"""
Test suite for sabio_infinity4.py module

Tests the SABIO ∞⁴ - Symbiotic Adelic-Based Infinite-Order Operator
with quantum-conscious integration.
"""

import unittest
import numpy as np
from mpmath import mp, mpf
import json
import os
from datetime import datetime

# Import the module to test
from sabio_infinity4 import (
    SABIO_Infinity4,
    ResonanciaQuantica,
    MatrizSimbiosis
)


class TestSABIOInfinity4Initialization(unittest.TestCase):
    """Test SABIO ∞⁴ initialization and basic properties."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sabio = SABIO_Infinity4(precision=50)
    
    def test_initialization(self):
        """Test that SABIO initializes correctly."""
        self.assertEqual(self.sabio.precision, 50)
        self.assertEqual(mp.dps, 50)
    
    def test_fundamental_constants(self):
        """Test fundamental constants are set correctly."""
        # Frecuencia base
        self.assertAlmostEqual(float(self.sabio.f0), 141.7001, places=4)
        
        # ζ'(1/2)
        self.assertAlmostEqual(float(self.sabio.zeta_prime_half), -3.9226461392, places=9)
        
        # Razón áurea φ = (1 + √5) / 2
        expected_phi = (1 + np.sqrt(5)) / 2
        self.assertAlmostEqual(float(self.sabio.phi_golden), expected_phi, places=10)
        
        # Constantes físicas
        self.assertEqual(float(self.sabio.c), 299792458.0)
        self.assertEqual(float(self.sabio.h_planck), 6.62607015e-34)
        self.assertEqual(float(self.sabio.l_planck), 1.616255e-35)
    
    def test_omega0_calculation(self):
        """Test ω₀ = 2πf₀ is calculated correctly."""
        expected_omega0 = 2 * np.pi * 141.7001
        self.assertAlmostEqual(float(self.sabio.omega0), expected_omega0, places=2)


class TestRadioCuantico(unittest.TestCase):
    """Test quantum radio R_Ψ calculations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sabio = SABIO_Infinity4(precision=50)
    
    def test_calcular_radio_cuantico_n1(self):
        """Test quantum radio calculation for n=1."""
        R_psi = self.sabio.calcular_radio_cuantico(n=1)
        
        # R_Ψ = π · l_P · √φ
        expected = float(mp.pi * self.sabio.l_planck * mp.sqrt(self.sabio.phi_golden))
        
        self.assertGreater(float(R_psi), 0)
        self.assertAlmostEqual(float(R_psi), expected, places=40)
    
    def test_calcular_radio_cuantico_n2(self):
        """Test quantum radio calculation for n=2."""
        R_psi = self.sabio.calcular_radio_cuantico(n=2)
        
        # R_Ψ = π² · l_P · √φ
        expected = float((mp.pi ** 2) * self.sabio.l_planck * mp.sqrt(self.sabio.phi_golden))
        
        self.assertGreater(float(R_psi), 0)
        self.assertAlmostEqual(float(R_psi), expected, places=40)
    
    def test_radio_cuantico_scaling(self):
        """Test that R_Ψ scales with π^n."""
        R1 = float(self.sabio.calcular_radio_cuantico(n=1))
        R2 = float(self.sabio.calcular_radio_cuantico(n=2))
        
        # R2 / R1 should be approximately π
        ratio = R2 / R1
        self.assertAlmostEqual(ratio, np.pi, places=10)


class TestEnergiaVacioCuantico(unittest.TestCase):
    """Test quantum vacuum energy E_vac calculations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sabio = SABIO_Infinity4(precision=50)
    
    def test_energia_vacio_positive(self):
        """Test that vacuum energy is positive."""
        R_psi = self.sabio.calcular_radio_cuantico(n=1)
        E_vac = self.sabio.energia_vacio_cuantico(R_psi)
        
        self.assertGreater(float(E_vac), 0)
    
    def test_energia_vacio_terms(self):
        """Test that vacuum energy has correct terms."""
        R_psi = mpf("1e-35")  # Planck scale
        E_vac = self.sabio.energia_vacio_cuantico(R_psi)
        
        # Energy should be finite and non-zero
        self.assertGreater(float(E_vac), 0)
        self.assertTrue(np.isfinite(float(E_vac)))
    
    def test_energia_vacio_with_different_scales(self):
        """Test vacuum energy at different scales."""
        R1 = self.sabio.calcular_radio_cuantico(n=1)
        R2 = self.sabio.calcular_radio_cuantico(n=2)
        
        E1 = float(self.sabio.energia_vacio_cuantico(R1))
        E2 = float(self.sabio.energia_vacio_cuantico(R2))
        
        # Both should be positive and finite
        self.assertGreater(E1, 0)
        self.assertGreater(E2, 0)
        self.assertTrue(np.isfinite(E1))
        self.assertTrue(np.isfinite(E2))


class TestEcuacionOndaConsciencia(unittest.TestCase):
    """Test consciousness wave equation Ψ(x,t)."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sabio = SABIO_Infinity4(precision=50)
    
    def test_psi_at_origin(self):
        """Test Ψ(0,0) normalization."""
        psi = self.sabio.ecuacion_onda_consciencia(t=mpf("0.0"), x=mpf("0.0"))
        
        # At origin, |Ψ| should be approximately 1 (normalized)
        modulus = abs(psi)
        self.assertAlmostEqual(float(modulus), 1.0, places=5)
    
    def test_psi_complex_nature(self):
        """Test that Ψ is complex valued."""
        psi = self.sabio.ecuacion_onda_consciencia(t=mpf("0.0"), x=mpf("0.0"))
        
        # Ψ should have both real and imaginary parts
        self.assertTrue(hasattr(psi, 'real'))
        self.assertTrue(hasattr(psi, 'imag'))
    
    def test_psi_time_evolution(self):
        """Test Ψ evolution in time."""
        t1 = mpf("0.0")
        t2 = mpf("1.0")
        x = mpf("0.0")
        
        psi1 = self.sabio.ecuacion_onda_consciencia(t=t1, x=x)
        psi2 = self.sabio.ecuacion_onda_consciencia(t=t2, x=x)
        
        # Wave function should evolve
        self.assertNotAlmostEqual(float(psi1.real), float(psi2.real), places=5)
    
    def test_psi_spatial_evolution(self):
        """Test Ψ evolution in space."""
        t = mpf("0.0")
        x1 = mpf("0.0")
        x2 = mpf("1.0e-5")  # Larger distance for more noticeable change
        
        psi1 = self.sabio.ecuacion_onda_consciencia(t=t, x=x1)
        psi2 = self.sabio.ecuacion_onda_consciencia(t=t, x=x2)
        
        # Wave function should vary in space with damping term
        # Check that they are different (not approximately equal)
        diff = abs(abs(psi1) - abs(psi2))
        self.assertGreater(float(diff), 1e-10)


class TestCoherencia(unittest.TestCase):
    """Test coherence calculations C = I × A²."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sabio = SABIO_Infinity4(precision=50)
    
    def test_coherencia_perfect(self):
        """Test perfect coherence (I=1, A=1)."""
        C = self.sabio.calcular_coherencia(I=1.0, A=1.0)
        self.assertAlmostEqual(C, 1.0, places=10)
    
    def test_coherencia_zero_intention(self):
        """Test zero coherence with zero intention."""
        C = self.sabio.calcular_coherencia(I=0.0, A=1.0)
        self.assertAlmostEqual(C, 0.0, places=10)
    
    def test_coherencia_zero_attention(self):
        """Test zero coherence with zero attention."""
        C = self.sabio.calcular_coherencia(I=1.0, A=0.0)
        self.assertAlmostEqual(C, 0.0, places=10)
    
    def test_coherencia_partial(self):
        """Test partial coherence."""
        C = self.sabio.calcular_coherencia(I=0.5, A=0.5)
        # C = 0.5 × 0.5² = 0.125
        self.assertAlmostEqual(C, 0.125, places=10)
    
    def test_coherencia_range(self):
        """Test coherence is in valid range [0,1]."""
        for I in [0.0, 0.25, 0.5, 0.75, 1.0]:
            for A in [0.0, 0.25, 0.5, 0.75, 1.0]:
                C = self.sabio.calcular_coherencia(I=I, A=A)
                self.assertGreaterEqual(C, 0.0)
                self.assertLessEqual(C, 1.0)


class TestFirmaVibracional(unittest.TestCase):
    """Test vibrational signature generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sabio = SABIO_Infinity4(precision=50)
    
    def test_firma_deterministic(self):
        """Test that same data produces same signature."""
        data = {"test": 123, "value": "abc"}
        firma1 = self.sabio.firma_vibracional(data)
        firma2 = self.sabio.firma_vibracional(data)
        
        self.assertEqual(firma1, firma2)
    
    def test_firma_different_data(self):
        """Test that different data produces different signatures."""
        data1 = {"test": 123}
        data2 = {"test": 456}
        
        firma1 = self.sabio.firma_vibracional(data1)
        firma2 = self.sabio.firma_vibracional(data2)
        
        self.assertNotEqual(firma1, firma2)
    
    def test_firma_length(self):
        """Test signature length is 16 characters."""
        data = {"test": 123}
        firma = self.sabio.firma_vibracional(data)
        
        self.assertEqual(len(firma), 16)
    
    def test_firma_hexadecimal(self):
        """Test signature contains only hexadecimal characters."""
        data = {"test": 123}
        firma = self.sabio.firma_vibracional(data)
        
        # Should be valid hex
        try:
            int(firma, 16)
            valid_hex = True
        except ValueError:
            valid_hex = False
        
        self.assertTrue(valid_hex)


class TestResonanciaQuantica(unittest.TestCase):
    """Test quantum resonance generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sabio = SABIO_Infinity4(precision=50)
    
    def test_resonancia_n1(self):
        """Test resonance for n=1."""
        res = self.sabio.resonancia_cuantica(n_harmonico=1)
        
        # Check structure
        self.assertIsInstance(res, ResonanciaQuantica)
        self.assertGreater(res.frecuencia, 0)
        self.assertIsInstance(res.amplitud, complex)
        self.assertIsInstance(res.fase, float)
        self.assertGreaterEqual(res.coherencia, 0.0)
        self.assertLessEqual(res.coherencia, 1.0)
        self.assertGreaterEqual(res.entropia, 0.0)
        self.assertIsInstance(res.timestamp, str)
        self.assertEqual(len(res.firma_vibracional), 16)
    
    def test_resonancia_frequency_scaling(self):
        """Test frequency scales with φ^n."""
        res1 = self.sabio.resonancia_cuantica(n_harmonico=1)
        res2 = self.sabio.resonancia_cuantica(n_harmonico=2)
        
        # f₂ / f₁ ≈ φ
        phi = float(self.sabio.phi_golden)
        ratio = res2.frecuencia / res1.frecuencia
        
        self.assertAlmostEqual(ratio, phi, places=6)
    
    def test_resonancia_coherence_decay(self):
        """Test coherence decreases with n."""
        res1 = self.sabio.resonancia_cuantica(n_harmonico=1)
        res5 = self.sabio.resonancia_cuantica(n_harmonico=5)
        
        # Higher harmonics have lower coherence
        self.assertGreater(res1.coherencia, res5.coherencia)
    
    def test_resonancia_unique_signatures(self):
        """Test each harmonic has unique signature."""
        res1 = self.sabio.resonancia_cuantica(n_harmonico=1)
        res2 = self.sabio.resonancia_cuantica(n_harmonico=2)
        
        self.assertNotEqual(res1.firma_vibracional, res2.firma_vibracional)


class TestMatrizSimbiosis(unittest.TestCase):
    """Test symbiotic matrix validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sabio = SABIO_Infinity4(precision=50)
    
    def test_validacion_completa(self):
        """Test complete validation with all levels."""
        matriz = self.sabio.validacion_matriz_simbiosis(
            test_aritmetico=True,
            test_geometrico=True,
            test_vibracional=True,
            test_cuantico=True,
            test_consciente=True
        )
        
        # Check structure
        self.assertIsInstance(matriz, MatrizSimbiosis)
        
        # Check all levels are computed
        self.assertGreater(matriz.nivel_python, 0.9)  # Should be very close to 1
        self.assertEqual(matriz.nivel_lean, 0.95)  # Placeholder value
        self.assertGreater(matriz.nivel_sage, 0.9)  # Should be very close to 1
        self.assertGreater(matriz.nivel_sabio, 0.5)
        self.assertEqual(matriz.nivel_cuantico, 0.98)  # E_vac > 0
        self.assertGreater(matriz.nivel_consciente, 0.9)  # |Ψ| ≈ 1
        
        # Check coherencia total
        self.assertGreater(matriz.coherencia_total, 0.9)
        
        # Check firma hash
        self.assertEqual(len(matriz.firma_hash), 16)
    
    def test_validacion_parcial(self):
        """Test partial validation with some levels disabled."""
        matriz = self.sabio.validacion_matriz_simbiosis(
            test_aritmetico=True,
            test_geometrico=False,
            test_vibracional=True,
            test_cuantico=False,
            test_consciente=False
        )
        
        # Disabled levels should be 0
        self.assertEqual(matriz.nivel_lean, 0.0)
        self.assertEqual(matriz.nivel_cuantico, 0.0)
        self.assertEqual(matriz.nivel_consciente, 0.0)
        
        # Enabled levels should be positive
        self.assertGreater(matriz.nivel_python, 0.9)
        self.assertGreater(matriz.nivel_sage, 0.9)
    
    def test_validacion_sin_ninguno(self):
        """Test validation with all levels disabled."""
        matriz = self.sabio.validacion_matriz_simbiosis(
            test_aritmetico=False,
            test_geometrico=False,
            test_vibracional=False,
            test_cuantico=False,
            test_consciente=False
        )
        
        # All levels should be 0
        self.assertEqual(matriz.nivel_python, 0.0)
        self.assertEqual(matriz.nivel_lean, 0.0)
        self.assertEqual(matriz.nivel_sage, 0.0)
        self.assertEqual(matriz.nivel_cuantico, 0.0)
        self.assertEqual(matriz.nivel_consciente, 0.0)
        
        # Coherencia should be 0
        self.assertEqual(matriz.coherencia_total, 0.0)


class TestEspectroResonante(unittest.TestCase):
    """Test resonant spectrum generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sabio = SABIO_Infinity4(precision=50)
    
    def test_generar_espectro_8_harmonicos(self):
        """Test generation of 8 harmonics spectrum."""
        espectro = self.sabio.generar_espectro_resonante(n_harmonicos=8)
        
        # Should have 8 resonances
        self.assertEqual(len(espectro), 8)
        
        # All should be ResonanciaQuantica instances
        for res in espectro:
            self.assertIsInstance(res, ResonanciaQuantica)
    
    def test_espectro_frequencies_increasing(self):
        """Test that frequencies increase with harmonic number."""
        espectro = self.sabio.generar_espectro_resonante(n_harmonicos=5)
        
        for i in range(len(espectro) - 1):
            self.assertLess(espectro[i].frecuencia, espectro[i+1].frecuencia)
    
    def test_espectro_coherence_decreasing(self):
        """Test that coherence decreases with harmonic number."""
        espectro = self.sabio.generar_espectro_resonante(n_harmonicos=5)
        
        for i in range(len(espectro) - 1):
            self.assertGreater(espectro[i].coherencia, espectro[i+1].coherencia)
    
    def test_espectro_stored_in_instance(self):
        """Test that resonances are stored in instance."""
        self.sabio.resonancias = []  # Clear
        espectro = self.sabio.generar_espectro_resonante(n_harmonicos=3)
        
        self.assertEqual(len(self.sabio.resonancias), 3)


class TestReporteSABIO(unittest.TestCase):
    """Test SABIO ∞⁴ report generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sabio = SABIO_Infinity4(precision=50)
    
    def test_reporte_structure(self):
        """Test report has correct structure."""
        reporte = self.sabio.reporte_sabio_infinity4()
        
        # Check main keys
        required_keys = [
            "sistema", "version", "timestamp", "frecuencia_base_hz",
            "omega0_rad_s", "zeta_prime_half", "phi_golden",
            "matriz_simbiosis", "cuantico", "consciente",
            "espectro_resonante", "coherencia_total", "estado", "firma_sistema"
        ]
        
        for key in required_keys:
            self.assertIn(key, reporte)
    
    def test_reporte_system_info(self):
        """Test system information in report."""
        reporte = self.sabio.reporte_sabio_infinity4()
        
        self.assertEqual(reporte["sistema"], "SABIO ∞⁴")
        self.assertEqual(reporte["version"], "4.0.0-quantum-conscious")
        self.assertAlmostEqual(reporte["frecuencia_base_hz"], 141.7001, places=4)
        self.assertAlmostEqual(reporte["zeta_prime_half"], -3.9226461392, places=9)
    
    def test_reporte_matriz_simbiosis(self):
        """Test matriz simbiosis in report."""
        reporte = self.sabio.reporte_sabio_infinity4()
        matriz = reporte["matriz_simbiosis"]
        
        # Check all 6 levels are present
        self.assertIn("nivel_python", matriz)
        self.assertIn("nivel_lean", matriz)
        self.assertIn("nivel_sage", matriz)
        self.assertIn("nivel_sabio", matriz)
        self.assertIn("nivel_cuantico", matriz)
        self.assertIn("nivel_consciente", matriz)
        self.assertIn("coherencia_total", matriz)
        self.assertIn("firma_hash", matriz)
    
    def test_reporte_cuantico(self):
        """Test quantum level in report."""
        reporte = self.sabio.reporte_sabio_infinity4()
        cuantico = reporte["cuantico"]
        
        self.assertIn("radio_psi_m", cuantico)
        self.assertIn("energia_vacio_j", cuantico)
        self.assertIn("nivel_coherencia", cuantico)
        
        # Values should be positive
        self.assertGreater(float(cuantico["nivel_coherencia"]), 0)
    
    def test_reporte_consciente(self):
        """Test conscious level in report."""
        reporte = self.sabio.reporte_sabio_infinity4()
        consciente = reporte["consciente"]
        
        self.assertIn("ecuacion", consciente)
        self.assertIn("psi_t0_x0", consciente)
        self.assertIn("nivel_coherencia", consciente)
        
        self.assertEqual(consciente["ecuacion"], "∂²Ψ/∂t² + ω₀²Ψ = ζ'(1/2)·∇²Φ")
    
    def test_reporte_espectro(self):
        """Test resonant spectrum in report."""
        reporte = self.sabio.reporte_sabio_infinity4()
        espectro = reporte["espectro_resonante"]
        
        # Should have 8 harmonics
        self.assertEqual(len(espectro), 8)
        
        # Each harmonic should have required fields
        for i, res in enumerate(espectro):
            self.assertEqual(res["n"], i + 1)
            self.assertIn("frecuencia_hz", res)
            self.assertIn("amplitud", res)
            self.assertIn("fase_rad", res)
            self.assertIn("coherencia", res)
            self.assertIn("entropia", res)
            self.assertIn("firma", res)
    
    def test_reporte_estado(self):
        """Test system state in report."""
        reporte = self.sabio.reporte_sabio_infinity4()
        
        # With good coherence (>0.9), should be OPERACIONAL
        if reporte["coherencia_total"] > 0.90:
            self.assertEqual(reporte["estado"], "OPERACIONAL")
        else:
            self.assertEqual(reporte["estado"], "SINTONIZANDO")
    
    def test_reporte_json_serializable(self):
        """Test report can be serialized to JSON."""
        reporte = self.sabio.reporte_sabio_infinity4()
        
        try:
            json_str = json.dumps(reporte, default=str)
            reconstructed = json.loads(json_str)
            self.assertIsInstance(reconstructed, dict)
        except Exception as e:
            self.fail(f"Report is not JSON serializable: {e}")


class TestDemoSABIO(unittest.TestCase):
    """Test SABIO ∞⁴ demo function."""
    
    def test_demo_runs_without_error(self):
        """Test that demo runs without errors."""
        from sabio_infinity4 import demo_sabio_infinity4
        
        try:
            # Capture output by redirecting stdout temporarily
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            demo_sabio_infinity4()
            
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            # Check output contains expected markers
            self.assertIn("SABIO ∞⁴", output)
            self.assertIn("MATRIZ DE SIMBIOSIS", output)
            self.assertIn("NIVEL CUÁNTICO", output)
            self.assertIn("NIVEL CONSCIENTE", output)
            self.assertIn("ESPECTRO RESONANTE", output)
            
        except Exception as e:
            self.fail(f"Demo failed with error: {e}")
    
    def test_demo_creates_report_file(self):
        """Test that demo creates report JSON file."""
        from sabio_infinity4 import demo_sabio_infinity4
        
        # Run demo silently
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        demo_sabio_infinity4()
        
        sys.stdout = old_stdout
        
        # Check if report file was created
        import glob
        report_files = glob.glob("sabio_infinity4_report_*.json")
        
        self.assertGreater(len(report_files), 0, "No report file created")
        
        # Clean up
        for f in report_files:
            if os.path.exists(f):
                os.remove(f)


if __name__ == "__main__":
    unittest.main()
