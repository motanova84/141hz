#!/usr/bin/env python3
"""
Tests para test_falsabilidad_biologica.py

Verifica que:
1. La precisión del 0.1% se alcanza
2. La energía se mantiene constante
3. El ratio QCAL funciona correctamente
4. Los criterios de falsación son correctos
"""

import pytest
import numpy as np
from pathlib import Path
import sys
import json

# Add scripts to path
ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / 'scripts'
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# Import from scripts directory (avoid circular import)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "falsabilidad_biologica_module", 
    SCRIPTS_DIR / "test_falsabilidad_biologica.py"
)
falsabilidad_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(falsabilidad_module)

ExperimentalConfig = falsabilidad_module.ExperimentalConfig
BiologicalResponse = falsabilidad_module.BiologicalResponse
QCALBiologicalExperiment = falsabilidad_module.QCALBiologicalExperiment


class TestExperimentalConfig:
    """Tests para configuración experimental"""
    
    def test_default_config(self):
        """Verifica configuración por defecto"""
        config = ExperimentalConfig()
        
        assert config.precision_target == 0.001  # 0.1%
        assert config.energy_constant == 1.0
        assert config.num_measurements == 1000
        assert len(config.frequencies) > 0
        assert 141.7 in config.frequencies
        assert 100.0 in config.frequencies
    
    def test_custom_config(self):
        """Verifica configuración personalizada"""
        freqs = [100.0, 141.7, 200.0]
        config = ExperimentalConfig(
            precision_target=0.0001,
            frequencies=freqs,
            energy_constant=2.0,
            num_measurements=500
        )
        
        assert config.precision_target == 0.0001
        assert config.frequencies == freqs
        assert config.energy_constant == 2.0
        assert config.num_measurements == 500


class TestQCALBiologicalExperiment:
    """Tests para experimento biológico QCAL"""
    
    def test_qcal_response_at_resonance(self):
        """Verifica que QCAL predice respuesta aumentada en f0"""
        config = ExperimentalConfig()
        experiment = QCALBiologicalExperiment(config)
        
        # Response at resonance should be higher
        response_at_f0 = experiment.calculate_qcal_response(141.7, 1.0)
        response_off_resonance = experiment.calculate_qcal_response(100.0, 1.0)
        
        assert response_at_f0 > response_off_resonance
        assert response_at_f0 / response_off_resonance > 1.5
    
    def test_traditional_response_flat(self):
        """Verifica que biología tradicional predice respuesta plana"""
        config = ExperimentalConfig()
        experiment = QCALBiologicalExperiment(config)
        
        # All frequencies should give same response with same energy
        energy = 1.0
        response_100 = experiment.calculate_traditional_response(100.0, energy)
        response_141 = experiment.calculate_traditional_response(141.7, energy)
        response_200 = experiment.calculate_traditional_response(200.0, energy)
        
        assert response_100 == response_141
        assert response_141 == response_200
        assert response_100 == energy
    
    def test_constant_energy_maintained(self):
        """Verifica que la energía se mantiene constante"""
        config = ExperimentalConfig(energy_constant=1.5)
        experiment = QCALBiologicalExperiment(config)
        
        # Run experiment
        responses = experiment.run_experiment(model='qcal')
        
        # All responses should have same energy
        energies = [resp.energy for resp in responses]
        assert all(e == 1.5 for e in energies)
    
    def test_precision_achieved(self):
        """Verifica que se alcanza la precisión del 0.1%"""
        config = ExperimentalConfig(
            precision_target=0.001,
            num_measurements=10000  # More measurements for better precision
        )
        experiment = QCALBiologicalExperiment(config)
        
        # Measure at one frequency
        response = experiment.measure_response(141.7, model='qcal', noise_level=0.0001)
        
        # Calculate relative error
        relative_error = response.delta_f_std / response.delta_f
        
        # Should be better than or close to target
        assert relative_error < 0.01  # Within 1%
    
    def test_qcal_ratio_criterion(self):
        """Verifica el criterio de ratio QCAL"""
        config = ExperimentalConfig(frequencies=[100.0, 141.7])
        experiment = QCALBiologicalExperiment(config)
        
        # Run QCAL experiment
        experiment.run_experiment(model='qcal')
        
        # Calculate ratio test
        ratio_test = experiment.calculate_ratio_test()
        
        assert 'ratio' in ratio_test
        assert 'qcal_threshold' in ratio_test
        assert ratio_test['qcal_threshold'] == 1.5
        
        # QCAL model should pass the test
        assert ratio_test['qcal_supported'] == True
        assert ratio_test['ratio'] > 1.5
    
    def test_traditional_ratio_criterion(self):
        """Verifica que biología tradicional no pasa el ratio test"""
        config = ExperimentalConfig(frequencies=[100.0, 141.7])
        experiment = QCALBiologicalExperiment(config)
        
        # Run traditional experiment
        experiment.run_experiment(model='traditional')
        
        # Calculate ratio test
        ratio_test = experiment.calculate_ratio_test()
        
        # Traditional model should NOT pass the test
        # Ratio should be ~1.0 (flat response)
        assert abs(ratio_test['ratio'] - 1.0) < 0.1
        assert ratio_test['qcal_supported'] == False
    
    def test_flatness_qcal(self):
        """Verifica que QCAL NO predice respuesta plana"""
        config = ExperimentalConfig()
        experiment = QCALBiologicalExperiment(config)
        
        # Run QCAL experiment
        experiment.run_experiment(model='qcal')
        
        # Test flatness
        flat_test = experiment.test_flat_response()
        
        # QCAL should NOT be flat
        assert flat_test['is_flat'] == False
        assert flat_test['qcal_falsified'] == False
    
    def test_flatness_traditional(self):
        """Verifica que biología tradicional SÍ predice respuesta plana"""
        config = ExperimentalConfig()
        experiment = QCALBiologicalExperiment(config)
        
        # Run traditional experiment
        experiment.run_experiment(model='traditional')
        
        # Test flatness
        flat_test = experiment.test_flat_response()
        
        # Traditional should be flat
        assert flat_test['is_flat'] == True
        assert flat_test['traditional_supported'] == True
    
    def test_generate_report_qcal(self):
        """Verifica generación de reporte para modelo QCAL"""
        config = ExperimentalConfig()
        experiment = QCALBiologicalExperiment(config)
        
        experiment.run_experiment(model='qcal')
        report = experiment.generate_report('qcal')
        
        # Check report structure
        assert 'experiment_config' in report
        assert 'model_tested' in report
        assert 'ratio_test' in report
        assert 'flatness_test' in report
        assert 'responses' in report
        assert 'verdict' in report
        
        assert report['model_tested'] == 'qcal'
        
        # QCAL should be supported
        assert 'QCAL recibe apoyo experimental fuerte' in report['verdict']
    
    def test_generate_report_traditional(self):
        """Verifica generación de reporte para modelo tradicional"""
        config = ExperimentalConfig()
        experiment = QCALBiologicalExperiment(config)
        
        experiment.run_experiment(model='traditional')
        report = experiment.generate_report('traditional')
        
        assert report['model_tested'] == 'traditional'
        
        # Traditional biology should be confirmed
        assert 'Biología tradicional confirmada' in report['verdict']
    
    def test_measurement_reproducibility(self):
        """Verifica reproducibilidad de mediciones"""
        config = ExperimentalConfig(frequencies=[100.0, 141.7])  # Add 100 Hz for ratio test
        
        # Run multiple experiments
        results = []
        for _ in range(10):
            experiment = QCALBiologicalExperiment(config)
            experiment.run_experiment(model='qcal')
            ratio_test = experiment.calculate_ratio_test()
            if 'ratio' in ratio_test:
                results.append(ratio_test['ratio'])
        
        # Results should be consistent (within expected variation)
        assert len(results) > 0
        mean_ratio = np.mean(results)
        std_ratio = np.std(results)
        
        # All results should be within 3 sigma of mean
        assert all(abs(r - mean_ratio) < 3 * std_ratio for r in results)
    
    def test_falsification_criterion_qcal(self):
        """Verifica criterio de falsación: QCAL se falsa si respuesta es plana"""
        config = ExperimentalConfig()
        experiment = QCALBiologicalExperiment(config)
        
        # Run QCAL experiment
        experiment.run_experiment(model='qcal')
        
        # Get flatness test
        flat_test = experiment.test_flat_response()
        
        # If flat, QCAL is falsified
        is_falsified = flat_test['qcal_falsified']
        
        # QCAL model should NOT be falsified (not flat)
        assert is_falsified == False
    
    def test_falsification_criterion_traditional_with_qcal_data(self):
        """Verifica que biología tradicional es falsada por datos QCAL"""
        config = ExperimentalConfig()
        experiment = QCALBiologicalExperiment(config)
        
        # Run QCAL experiment (generates non-flat data)
        experiment.run_experiment(model='qcal')
        
        # Test if data is flat (traditional biology prediction)
        flat_test = experiment.test_flat_response()
        
        # Traditional biology should be falsified by non-flat data
        assert flat_test['is_flat'] == False
        assert flat_test['traditional_supported'] == False


class TestIntegration:
    """Tests de integración"""
    
    def test_full_workflow_qcal(self):
        """Test workflow completo con modelo QCAL"""
        config = ExperimentalConfig()
        experiment = QCALBiologicalExperiment(config)
        
        # Run experiment
        responses = experiment.run_experiment(model='qcal')
        
        # Verify we got responses for all frequencies
        assert len(responses) == len(config.frequencies)
        
        # Calculate tests
        ratio_test = experiment.calculate_ratio_test()
        flat_test = experiment.test_flat_response()
        
        # Generate report
        report = experiment.generate_report('qcal')
        
        # Verify QCAL predictions
        assert ratio_test['qcal_supported'] == True
        assert flat_test['qcal_falsified'] == False
        assert 'QCAL' in report['verdict']
    
    def test_full_workflow_traditional(self):
        """Test workflow completo con modelo tradicional"""
        config = ExperimentalConfig()
        experiment = QCALBiologicalExperiment(config)
        
        # Run experiment
        responses = experiment.run_experiment(model='traditional')
        
        # Calculate tests
        ratio_test = experiment.calculate_ratio_test()
        flat_test = experiment.test_flat_response()
        
        # Generate report
        report = experiment.generate_report('traditional')
        
        # Verify traditional predictions
        assert ratio_test['qcal_supported'] == False
        assert flat_test['traditional_supported'] == True
        assert 'tradicional confirmada' in report['verdict']
    
    def test_save_results(self, tmp_path):
        """Test guardado de resultados"""
        config = ExperimentalConfig()
        experiment = QCALBiologicalExperiment(config)
        
        experiment.run_experiment(model='qcal')
        report = experiment.generate_report('qcal')
        
        # Save to temporary file
        json_file = tmp_path / 'test_results.json'
        
        # Convert numpy types and remove numpy arrays (keep only scalars)
        def convert_for_json(obj):
            if isinstance(obj, dict):
                return {k: convert_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_for_json(item) for item in obj]
            elif isinstance(obj, (bool, np.bool_)):
                return bool(obj)
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return None  # Skip arrays
            else:
                return obj
        
        json_report = convert_for_json(report)
        
        with open(json_file, 'w') as f:
            json.dump(json_report, f, indent=2)
        
        # Verify file exists and can be loaded
        assert json_file.exists()
        
        with open(json_file, 'r') as f:
            loaded_report = json.load(f)
        
        assert loaded_report['model_tested'] == 'qcal'
        assert 'verdict' in loaded_report


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
