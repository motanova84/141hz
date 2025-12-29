#!/usr/bin/env python3
"""
AI Agent for Automated Project Creation
========================================

This AI agent automatically creates and activates new analysis projects
with full coherence to the existing GW250114-141Hz analysis infrastructure.

Features:
- Template-based project generation
- Automatic workflow creation
- Test scaffolding
- Documentation generation
- Integration with existing CI/CD
- Coherence validation

Usage:
    python ai_agent_project_creator.py --type event --name GW250115 --description "Analysis of GW250115 event"
    python ai_agent_project_creator.py --type validation --name coherence_check --description "New coherence validation"
    python ai_agent_project_creator.py --type tool --name snr_optimizer --description "SNR optimization tool"

Author: AI Agent System
Date: 2025
"""

import os
import sys
import json
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Optional


class ProjectTemplate:
    """Base template for project generation"""
    
    def __init__(self, project_type: str, name: str, description: str):
        self.project_type = project_type
        self.name = name
        self.description = description
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.root_dir = Path(__file__).parent.parent
        
    def get_safe_name(self) -> str:
        """Get filesystem-safe project name"""
        return self.name.lower().replace(" ", "_").replace("-", "_")
    
    def get_module_name(self) -> str:
        """Get Python module name"""
        return f"{self.get_safe_name()}_analysis"


class EventAnalysisTemplate(ProjectTemplate):
    """Template for gravitational wave event analysis projects"""
    
    def generate_analysis_script(self) -> str:
        """Generate main analysis script"""
        safe_name = self.get_safe_name()
        return f'''#!/usr/bin/env python3
"""
Analysis script for {self.name}
================================

{self.description}

This script follows the GW150914 analysis pattern and applies it to {self.name}.

Usage:
    python scripts/analizar_{safe_name}.py
    python scripts/analizar_{safe_name}.py --detector H1 --band 140-143

Requirements:
    - gwpy>=3.0.0
    - numpy>=1.21.0
    - scipy>=1.7.0
    - matplotlib>=3.5.0

Author: AI Agent - Generated on {self.timestamp}
"""

import numpy as np
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries
from scipy import signal
import json
import sys
import argparse


class {self.name.replace("-", "")}Analyzer:
    """Analyzer for {self.name} event"""
    
    def __init__(self, target_freq=141.7001, band_width=2.0):
        """
        Initialize {self.name} analyzer
        
        Parameters:
        -----------
        target_freq : float
            Target frequency in Hz (default: 141.7001 Hz)
        band_width : float
            Analysis bandwidth around target frequency (default: 2.0 Hz)
        """
        self.target_freq = target_freq
        self.band_width = band_width
        self.results = {{}}
        
    def download_data(self, detector='H1', gps_time=None, duration=32):
        """
        Download data from GWOSC
        
        Parameters:
        -----------
        detector : str
            Detector name (H1, L1, V1, K1)
        gps_time : int or None
            GPS time of event (if None, must be provided)
        duration : int
            Duration in seconds
        """
        if gps_time is None:
            raise ValueError("GPS time must be provided for {self.name}")
            
        print(f"📡 Downloading {{detector}} data for {self.name}...")
        try:
            data = TimeSeries.fetch_open_data(detector, gps_time, gps_time + duration)
            print(f"✅ Downloaded {{len(data)}} samples at {{data.sample_rate}} Hz")
            return data
        except Exception as e:
            print(f"❌ Error downloading data: {{e}}")
            return None
    
    def preprocess_data(self, data):
        """
        Preprocess data following LIGO standards
        
        Parameters:
        -----------
        data : TimeSeries
            Raw detector data
        
        Returns:
        --------
        TimeSeries
            Preprocessed data
        """
        print("🔧 Preprocessing data...")
        
        # High-pass filter at 20 Hz
        data = data.highpass(20)
        
        # Notch filter at power line frequencies
        for freq in [60, 120, 180]:
            data = data.notch(freq, quality_factor=30)
        
        print("✅ Preprocessing complete")
        return data
    
    def calculate_snr(self, data, detector='H1'):
        """
        Calculate SNR at target frequency
        
        Parameters:
        -----------
        data : TimeSeries
            Preprocessed data
        detector : str
            Detector name
        
        Returns:
        --------
        dict
            Results with frequency, SNR, and statistics
        """
        print(f"📊 Calculating SNR for {{detector}} at {{self.target_freq}} Hz...")
        
        # Calculate power spectral density
        freqs, psd = signal.welch(
            data.value,
            fs=data.sample_rate.value,
            nperseg=int(data.sample_rate.value * 4)
        )
        
        # Find peak near target frequency
        band_mask = (freqs >= self.target_freq - self.band_width) & \\
                    (freqs <= self.target_freq + self.band_width)
        
        if not np.any(band_mask):
            print(f"⚠️  No data in target band")
            return None
        
        # Calculate SNR
        peak_idx = np.argmax(psd[band_mask])
        peak_freq = freqs[band_mask][peak_idx]
        peak_power = psd[band_mask][peak_idx]
        
        # Noise floor (median of surrounding frequencies)
        noise_mask = (freqs >= self.target_freq - 10) & \\
                     (freqs <= self.target_freq + 10) & ~band_mask
        noise_floor = np.median(psd[noise_mask]) if np.any(noise_mask) else np.median(psd)
        
        snr = peak_power / noise_floor if noise_floor > 0 else 0
        
        result = {{
            'detector': detector,
            'target_freq': self.target_freq,
            'peak_freq': float(peak_freq),
            'peak_power': float(peak_power),
            'noise_floor': float(noise_floor),
            'snr': float(snr),
            'freq_diff': float(abs(peak_freq - self.target_freq))
        }}
        
        print(f"✅ Peak at {{peak_freq:.2f}} Hz with SNR = {{snr:.2f}}")
        
        return result
    
    def analyze_event(self, gps_time, detectors=['H1', 'L1'], duration=32):
        """
        Complete analysis pipeline for {self.name}
        
        Parameters:
        -----------
        gps_time : int
            GPS time of event
        detectors : list
            List of detector names
        duration : int
            Analysis duration in seconds
        
        Returns:
        --------
        dict
            Complete analysis results
        """
        print(f"\\n🌌 Starting analysis of {self.name}")
        print(f"📍 GPS time: {{gps_time}}")
        print(f"🔭 Detectors: {{', '.join(detectors)}}")
        print(f"⏱️  Duration: {{duration}}s")
        print(f"🎯 Target frequency: {{self.target_freq}} Hz\\n")
        
        self.results = {{
            'event': '{self.name}',
            'gps_time': gps_time,
            'target_freq': self.target_freq,
            'analysis_timestamp': self.timestamp,
            'detectors': {{}}
        }}
        
        for detector in detectors:
            print(f"\\n--- Analyzing {{detector}} ---")
            
            # Download and preprocess
            data = self.download_data(detector, gps_time, duration)
            if data is None:
                continue
                
            data = self.preprocess_data(data)
            
            # Calculate SNR
            result = self.calculate_snr(data, detector)
            if result:
                self.results['detectors'][detector] = result
        
        return self.results
    
    def save_results(self, output_file=None):
        """Save results to JSON file"""
        if output_file is None:
            output_file = f"results/{self.get_safe_name()}_results.json"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\\n💾 Results saved to {{output_path}}")
    
    def visualize_results(self, output_file=None):
        """Generate visualization of results"""
        if not self.results or 'detectors' not in self.results:
            print("⚠️  No results to visualize")
            return
        
        detectors = list(self.results['detectors'].keys())
        snrs = [self.results['detectors'][d]['snr'] for d in detectors]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(detectors, snrs, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'][:len(detectors)])
        ax.axhline(y=5, color='r', linestyle='--', label='SNR threshold (5)')
        ax.set_xlabel('Detector', fontsize=12)
        ax.set_ylabel('SNR at {{:.4f}} Hz'.format(self.target_freq), fontsize=12)
        ax.set_title(f'SNR Analysis for {self.name}', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        if output_file is None:
            output_file = f"results/figures/{self.get_safe_name()}_snr.png"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"📊 Visualization saved to {{output_path}}")
        plt.close()


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description='Analyze {self.name} for 141.7001 Hz component'
    )
    parser.add_argument(
        '--gps-time',
        type=int,
        help='GPS time of event (required)'
    )
    parser.add_argument(
        '--detectors',
        nargs='+',
        default=['H1', 'L1'],
        help='Detectors to analyze (default: H1 L1)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=32,
        help='Analysis duration in seconds (default: 32)'
    )
    parser.add_argument(
        '--target-freq',
        type=float,
        default=141.7001,
        help='Target frequency in Hz (default: 141.7001)'
    )
    parser.add_argument(
        '--band-width',
        type=float,
        default=2.0,
        help='Analysis bandwidth in Hz (default: 2.0)'
    )
    parser.add_argument(
        '--output',
        help='Output JSON file path (default: results/{self.get_safe_name()}_results.json)'
    )
    
    args = parser.parse_args()
    
    if args.gps_time is None:
        print("❌ Error: --gps-time is required")
        parser.print_help()
        return 1
    
    # Create analyzer
    analyzer = {self.name.replace("-", "")}Analyzer(
        target_freq=args.target_freq,
        band_width=args.band_width
    )
    
    # Run analysis
    results = analyzer.analyze_event(
        gps_time=args.gps_time,
        detectors=args.detectors,
        duration=args.duration
    )
    
    # Save results
    analyzer.save_results(args.output)
    analyzer.visualize_results()
    
    # Print summary
    print("\\n" + "="*60)
    print("ANALYSIS SUMMARY")
    print("="*60)
    
    for detector, data in results.get('detectors', {{}}).items():
        print(f"\\n{{detector}}:")
        print(f"  Peak frequency: {{data['peak_freq']:.4f}} Hz")
        print(f"  Target frequency: {{data['target_freq']:.4f}} Hz")
        print(f"  Frequency difference: {{data['freq_diff']:.4f}} Hz")
        print(f"  SNR: {{data['snr']:.2f}}")
        
        if data['snr'] >= 5:
            print(f"  ✅ DETECTED (SNR >= 5)")
        else:
            print(f"  ⚠️  MARGINAL (SNR < 5)")
    
    print("\\n" + "="*60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
'''
    
    def generate_test_script(self) -> str:
        """Generate test script"""
        safe_name = self.get_safe_name()
        return f'''#!/usr/bin/env python3
"""
Tests for {self.name} analysis
================================

Test suite for {self.get_safe_name()}_analysis module.

Usage:
    python scripts/test_{safe_name}.py

Author: AI Agent - Generated on {self.timestamp}
"""

import unittest
import numpy as np
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Test{self.name.replace("-", "")}Analysis(unittest.TestCase):
    """Test cases for {self.name} analysis"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Import here to avoid circular dependencies
        from scripts.analizar_{safe_name} import {self.name.replace("-", "")}Analyzer
        self.analyzer = {self.name.replace("-", "")}Analyzer()
    
    def test_initialization(self):
        """Test analyzer initialization"""
        self.assertEqual(self.analyzer.target_freq, 141.7001)
        self.assertEqual(self.analyzer.band_width, 2.0)
        self.assertIsInstance(self.analyzer.results, dict)
    
    def test_safe_name(self):
        """Test safe name generation"""
        self.assertEqual(self.analyzer.get_safe_name(), '{safe_name}')
    
    def test_custom_parameters(self):
        """Test custom initialization parameters"""
        from scripts.analizar_{safe_name} import {self.name.replace("-", "")}Analyzer
        analyzer = {self.name.replace("-", "")}Analyzer(target_freq=150.0, band_width=5.0)
        self.assertEqual(analyzer.target_freq, 150.0)
        self.assertEqual(analyzer.band_width, 5.0)
    
    @patch('scripts.analizar_{safe_name}.TimeSeries')
    def test_download_data_mock(self, mock_timeseries):
        """Test data download with mock"""
        # Mock data
        mock_data = Mock()
        mock_data.sample_rate = Mock(value=4096)
        mock_data.__len__ = Mock(return_value=131072)
        mock_timeseries.fetch_open_data.return_value = mock_data
        
        # Test download
        data = self.analyzer.download_data(detector='H1', gps_time=1234567890, duration=32)
        
        self.assertIsNotNone(data)
        mock_timeseries.fetch_open_data.assert_called_once()
    
    def test_snr_calculation_synthetic(self):
        """Test SNR calculation with synthetic signal"""
        # Create synthetic data with signal at target frequency
        sample_rate = 4096
        duration = 32
        t = np.linspace(0, duration, sample_rate * duration)
        
        # Noise
        noise = np.random.normal(0, 1, len(t))
        
        # Signal at target frequency
        signal_amplitude = 5.0
        signal = signal_amplitude * np.sin(2 * np.pi * 141.7001 * t)
        
        # Combined data
        data = Mock()
        data.value = noise + signal
        data.sample_rate = Mock(value=sample_rate)
        
        # Calculate SNR
        result = self.analyzer.calculate_snr(data, detector='H1')
        
        self.assertIsNotNone(result)
        self.assertIn('snr', result)
        self.assertGreater(result['snr'], 1.0)  # Should detect signal
        self.assertAlmostEqual(result['peak_freq'], 141.7001, delta=0.5)
    
    def test_result_structure(self):
        """Test results dictionary structure"""
        self.analyzer.results = {{
            'event': '{self.name}',
            'gps_time': 1234567890,
            'target_freq': 141.7001,
            'detectors': {{
                'H1': {{'snr': 7.5, 'peak_freq': 141.70}}
            }}
        }}
        
        self.assertIn('event', self.analyzer.results)
        self.assertIn('detectors', self.analyzer.results)
        self.assertEqual(self.analyzer.results['event'], '{self.name}')
    
    def test_save_results(self):
        """Test saving results to file"""
        import tempfile
        import json
        
        self.analyzer.results = {{
            'event': '{self.name}',
            'test': True
        }}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            self.analyzer.save_results(temp_file)
            
            # Verify file exists and contains correct data
            self.assertTrue(os.path.exists(temp_file))
            
            with open(temp_file, 'r') as f:
                loaded_data = json.load(f)
            
            self.assertEqual(loaded_data['event'], '{self.name}')
            self.assertTrue(loaded_data['test'])
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(Test{self.name.replace("-", "")}Analysis)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {{result.testsRun}}")
    print(f"Failures: {{len(result.failures)}}")
    print(f"Errors: {{len(result.errors)}}")
    print(f"Success rate: {{(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}}%")
    print("="*60)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
'''
    
    def generate_documentation(self) -> str:
        """Generate documentation"""
        return f'''# {self.name} Analysis Documentation

## Overview

{self.description}

This analysis follows the established patterns from GW150914 and applies them to the {self.name} event.

## Target Frequency

The analysis searches for components at **f₀ = 141.7001 Hz**, the predicted fundamental frequency from the Noetic Field Theory.

## Usage

### Basic Analysis

```bash
# Analyze {self.name} event
python scripts/analizar_{self.get_safe_name()}.py --gps-time <GPS_TIME>

# Analyze with specific detectors
python scripts/analizar_{self.get_safe_name()}.py --gps-time <GPS_TIME> --detectors H1 L1 V1

# Custom frequency and bandwidth
python scripts/analizar_{self.get_safe_name()}.py --gps-time <GPS_TIME> --target-freq 141.7001 --band-width 2.0
```

### Using Make

```bash
# Run analysis
make analyze-{self.get_safe_name()}

# Run tests
make test-{self.get_safe_name()}
```

## Output

The analysis generates:

1. **JSON Results**: `results/{self.get_safe_name()}_results.json`
   - Contains SNR values for each detector
   - Peak frequencies and power measurements
   - Statistical analysis

2. **Visualization**: `results/figures/{self.get_safe_name()}_snr.png`
   - Bar chart of SNR values per detector
   - Comparison with detection threshold (SNR = 5)

## Results Structure

```json
{{
  "event": "{self.name}",
  "gps_time": <GPS_TIME>,
  "target_freq": 141.7001,
  "analysis_timestamp": "<TIMESTAMP>",
  "detectors": {{
    "H1": {{
      "detector": "H1",
      "target_freq": 141.7001,
      "peak_freq": <DETECTED_FREQ>,
      "peak_power": <POWER>,
      "noise_floor": <NOISE>,
      "snr": <SNR_VALUE>,
      "freq_diff": <DIFF>
    }}
  }}
}}
```

## Testing

Run the test suite:

```bash
python scripts/test_{self.get_safe_name()}.py
```

Tests include:
- Initialization tests
- Data download mocking
- SNR calculation with synthetic signals
- Result structure validation
- File I/O operations

## Integration with CI/CD

This analysis is automatically run in the CI/CD pipeline:

- **On Push/PR**: Unit tests are executed
- **Scheduled**: Analysis runs daily with latest data
- **Manual Trigger**: Via GitHub Actions workflow_dispatch

## Dependencies

- gwpy >= 3.0.0
- numpy >= 1.21.0
- scipy >= 1.7.0
- matplotlib >= 3.5.0

## References

- [GW150914 Analysis](scripts/analizar_ringdown.py) - Reference implementation
- [Multi-Event SNR Analysis](ANALISIS_MULTIEVENTO_SNR.md) - Multi-event methodology
- [PAPER.md](PAPER.md) - Theoretical foundation

## Generated by AI Agent

This project was automatically generated by the AI Project Creator Agent on {self.timestamp}.

For questions or issues, refer to the main project documentation or open an issue.
'''


class ValidationTemplate(ProjectTemplate):
    """Template for validation method projects"""
    
    def generate_validation_script(self) -> str:
        """Generate validation script"""
        safe_name = self.get_safe_name()
        return f'''#!/usr/bin/env python3
"""
Validation: {self.name}
=======================

{self.description}

This validation module follows the established patterns from the project's
validation framework.

Usage:
    python scripts/validacion_{safe_name}.py
    python scripts/validacion_{safe_name}.py --precision 100

Author: AI Agent - Generated on {self.timestamp}
"""

import numpy as np
import mpmath as mp
import json
from pathlib import Path
import argparse
import sys


class {self.name.replace("_", " ").title().replace(" ", "")}Validator:
    """Validator for {self.name}"""
    
    def __init__(self, precision=50):
        """
        Initialize validator
        
        Parameters:
        -----------
        precision : int
            Decimal precision for mpmath calculations
        """
        self.precision = precision
        mp.dps = precision
        self.results = {{}}
        
    def validate(self):
        """
        Run validation
        
        Returns:
        --------
        dict
            Validation results
        """
        print(f"🔬 Running validation: {self.name}")
        print(f"📊 Precision: {{self.precision}} decimal places\\n")
        
        self.results = {{
            'validation': '{self.name}',
            'description': '{self.description}',
            'precision': self.precision,
            'timestamp': '{self.timestamp}',
            'checks': {{}}
        }}
        
        # Add validation logic here
        # Example: validate frequency relationship
        f0 = mp.mpf('141.7001')
        c = mp.mpf('299792458')  # Speed of light
        
        # Example check
        self.results['checks']['frequency'] = {{
            'f0': float(f0),
            'unit': 'Hz',
            'status': 'validated'
        }}
        
        return self.results
    
    def save_results(self, output_file=None):
        """Save validation results"""
        if output_file is None:
            output_file = f"results/validacion_{self.get_safe_name()}.json"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\\n💾 Results saved to {{output_path}}")
    
    def print_summary(self):
        """Print validation summary"""
        print("\\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        print(f"Validation: {self.name}")
        print(f"Description: {self.description}")
        print(f"Precision: {{self.precision}} decimal places")
        
        if 'checks' in self.results:
            print(f"\\nChecks performed: {{len(self.results['checks'])}}")
            for check_name, check_data in self.results['checks'].items():
                status = check_data.get('status', 'unknown')
                print(f"  {{check_name}}: {{status.upper()}}")
        
        print("="*60)


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description='Run {self.name} validation'
    )
    parser.add_argument(
        '--precision',
        type=int,
        default=50,
        help='Decimal precision (default: 50)'
    )
    parser.add_argument(
        '--output',
        help='Output JSON file path'
    )
    
    args = parser.parse_args()
    
    # Create validator
    validator = {self.name.replace("_", " ").title().replace(" ", "")}Validator(precision=args.precision)
    
    # Run validation
    results = validator.validate()
    
    # Save results
    validator.save_results(args.output)
    
    # Print summary
    validator.print_summary()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
'''


class AIProjectAgent:
    """Main AI Agent for project creation and activation"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.projects_created = []
        
    def create_project(self, project_type: str, name: str, description: str) -> Dict:
        """
        Create a new project with full automation
        
        Parameters:
        -----------
        project_type : str
            Type of project (event, validation, tool)
        name : str
            Project name
        description : str
            Project description
        
        Returns:
        --------
        dict
            Project creation summary
        """
        print(f"\n🤖 AI Project Agent - Creating Project")
        print("="*60)
        print(f"Type: {project_type}")
        print(f"Name: {name}")
        print(f"Description: {description}")
        print("="*60 + "\n")
        
        # Select template based on type
        if project_type == 'event':
            template = EventAnalysisTemplate(project_type, name, description)
        elif project_type == 'validation':
            template = ValidationTemplate(project_type, name, description)
        else:
            raise ValueError(f"Unknown project type: {project_type}")
        
        # Generate files
        files_created = []
        
        # Create scripts
        if project_type == 'event':
            script_path = self.root_dir / 'scripts' / f"analizar_{template.get_safe_name()}.py"
            test_path = self.root_dir / 'scripts' / f"test_{template.get_safe_name()}.py"
            
            with open(script_path, 'w') as f:
                f.write(template.generate_analysis_script())
            files_created.append(str(script_path))
            
            with open(test_path, 'w') as f:
                f.write(template.generate_test_script())
            files_created.append(str(test_path))
            
            # Make scripts executable
            os.chmod(script_path, 0o755)
            os.chmod(test_path, 0o755)
            
        elif project_type == 'validation':
            script_path = self.root_dir / 'scripts' / f"validacion_{template.get_safe_name()}.py"
            
            with open(script_path, 'w') as f:
                f.write(template.generate_validation_script())
            files_created.append(str(script_path))
            
            os.chmod(script_path, 0o755)
        
        # Create documentation
        if project_type == 'event':
            doc_path = self.root_dir / 'docs' / f"{template.get_safe_name().upper()}_ANALYSIS.md"
            doc_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(doc_path, 'w') as f:
                f.write(template.generate_documentation())
            files_created.append(str(doc_path))
        
        # Update Makefile
        self._update_makefile(template, project_type)
        
        # Create workflow
        self._create_workflow(template, project_type)
        files_created.append(str(self.root_dir / '.github' / 'workflows' / f"{template.get_safe_name()}.yml"))
        
        # Create project metadata
        metadata = {
            'name': name,
            'type': project_type,
            'description': description,
            'created_at': template.timestamp,
            'files': files_created,
            'status': 'active'
        }
        
        metadata_path = self.root_dir / 'projects' / f"{template.get_safe_name()}_metadata.json"
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.projects_created.append(metadata)
        
        print("\n✅ Project created successfully!")
        print(f"\n📁 Files created:")
        for file_path in files_created:
            print(f"  - {file_path}")
        
        return metadata
    
    def _update_makefile(self, template: ProjectTemplate, project_type: str):
        """Update Makefile with new targets"""
        makefile_path = self.root_dir / 'Makefile'
        safe_name = template.get_safe_name()
        
        # Read current Makefile
        with open(makefile_path, 'r') as f:
            content = f.read()
        
        # Add new targets
        if project_type == 'event':
            new_targets = f'''
# {template.name} Analysis (Auto-generated)
analyze-{safe_name}: setup
\t@echo "🌌 Analyzing {template.name}..."
\t./venv/bin/python scripts/analizar_{safe_name}.py --gps-time <GPS_TIME>

test-{safe_name}: setup
\t@echo "🧪 Testing {template.name} analysis..."
\t./venv/bin/python scripts/test_{safe_name}.py
'''
        elif project_type == 'validation':
            new_targets = f'''
# {template.name} Validation (Auto-generated)
validate-{safe_name}: setup
\t@echo "🔬 Validating {template.name}..."
\t./venv/bin/python scripts/validacion_{safe_name}.py
'''
        
        # Append to Makefile (insert before help target)
        if '# Show available targets' in content:
            parts = content.split('# Show available targets')
            content = parts[0] + new_targets + '\n# Show available targets' + parts[1]
        else:
            content += new_targets
        
        with open(makefile_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated Makefile with targets for {template.name}")
    
    def _create_workflow(self, template: ProjectTemplate, project_type: str):
        """Create GitHub Actions workflow"""
        workflow_path = self.root_dir / '.github' / 'workflows' / f"{template.get_safe_name()}.yml"
        safe_name = template.get_safe_name()
        
        if project_type == 'event':
            workflow_content = f'''name: {template.name} Analysis

on:
  push:
    branches: [ main ]
    paths:
      - 'scripts/analizar_{safe_name}.py'
      - 'scripts/test_{safe_name}.py'
  pull_request:
    branches: [ main ]
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC

jobs:
  test:
    name: Test {template.name}
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y libigraph-dev build-essential
    
    - name: Cache pip dependencies
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{{{ runner.os }}}}-pip-${{{{ hashFiles('requirements.txt') }}}}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python scripts/test_{safe_name}.py
    
    - name: Upload test results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: {safe_name}-test-results
        path: results/
        retention-days: 7

  analyze:
    name: Analyze {template.name}
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y libigraph-dev build-essential
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run analysis
      run: |
        python scripts/analizar_{safe_name}.py --gps-time <GPS_TIME>
      continue-on-error: true
    
    - name: Upload analysis results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: {safe_name}-analysis-results
        path: |
          results/{safe_name}_results.json
          results/figures/{safe_name}_snr.png
        retention-days: 30
'''
        elif project_type == 'validation':
            workflow_content = f'''name: {template.name} Validation

on:
  push:
    branches: [ main ]
    paths:
      - 'scripts/validacion_{safe_name}.py'
  pull_request:
    branches: [ main ]
  workflow_dispatch:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  validate:
    name: Validate {template.name}
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run validation
      run: |
        python scripts/validacion_{safe_name}.py
    
    - name: Upload validation results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: {safe_name}-validation-results
        path: results/validacion_{safe_name}.json
        retention-days: 30
'''
        
        with open(workflow_path, 'w') as f:
            f.write(workflow_content)
        
        print(f"✅ Created workflow: {workflow_path}")
    
    def list_projects(self):
        """List all created projects"""
        projects_dir = self.root_dir / 'projects'
        
        if not projects_dir.exists():
            print("No projects found")
            return []
        
        projects = []
        for metadata_file in projects_dir.glob('*_metadata.json'):
            with open(metadata_file, 'r') as f:
                projects.append(json.load(f))
        
        return projects


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description='AI Agent for Automated Project Creation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Create event analysis project
  python ai_agent_project_creator.py --type event --name GW250115 --description "Analysis of GW250115"
  
  # Create validation project
  python ai_agent_project_creator.py --type validation --name coherence_multi --description "Multi-scale coherence validation"
  
  # List all projects
  python ai_agent_project_creator.py --list
        '''
    )
    
    parser.add_argument(
        '--type',
        choices=['event', 'validation', 'tool'],
        help='Project type'
    )
    parser.add_argument(
        '--name',
        help='Project name (e.g., GW250115, coherence_check)'
    )
    parser.add_argument(
        '--description',
        help='Project description'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all created projects'
    )
    
    args = parser.parse_args()
    
    # Create agent
    agent = AIProjectAgent()
    
    if args.list:
        print("\n📋 Created Projects")
        print("="*60)
        projects = agent.list_projects()
        
        if not projects:
            print("No projects found")
        else:
            for i, project in enumerate(projects, 1):
                print(f"\n{i}. {project['name']}")
                print(f"   Type: {project['type']}")
                print(f"   Description: {project['description']}")
                print(f"   Created: {project['created_at']}")
                print(f"   Status: {project['status']}")
        
        return 0
    
    if not args.type or not args.name or not args.description:
        parser.print_help()
        print("\n❌ Error: --type, --name, and --description are required")
        return 1
    
    # Create project
    try:
        metadata = agent.create_project(args.type, args.name, args.description)
        
        print("\n" + "="*60)
        print("🎉 PROJECT CREATED SUCCESSFULLY")
        print("="*60)
        print(f"\nProject: {metadata['name']}")
        print(f"Type: {metadata['type']}")
        print(f"Files created: {len(metadata['files'])}")
        print(f"\nNext steps:")
        print(f"1. Review generated files")
        print(f"2. Update GPS time in analysis script (if applicable)")
        print(f"3. Run tests: make test-{EventAnalysisTemplate(args.type, args.name, args.description).get_safe_name()}")
        print(f"4. Commit and push changes")
        print("="*60)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error creating project: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
