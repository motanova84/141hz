#!/usr/bin/env python3
"""
🔬 Coherence Validator - QCAL ∞³ Quantum State Validator
Validates system coherence and Ψ state
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


class CoherenceValidator:
    """Validates QCAL system coherence"""
    
    def __init__(self, frequency=141.7001, optimized=False):
        self.frequency = frequency
        self.optimized = optimized
        self.timestamp = datetime.utcnow().isoformat()
        self.threshold = 0.888
    
    def validate_psi_state(self):
        """Validate Ψ state references in codebase"""
        psi_count = 0
        total_checked = 0
        
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]
            
            for file in files:
                if file.endswith(('.py', '.md', '.txt')):
                    total_checked += 1
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if 'Ψ' in content or 'PSI' in content.upper():
                                psi_count += 1
                    except Exception:
                        pass
        
        psi_ratio = psi_count / total_checked if total_checked > 0 else 0
        return {
            'psi_references': psi_count,
            'files_checked': total_checked,
            'psi_ratio': round(psi_ratio, 4)
        }
    
    def check_manifestos(self):
        """Check for manifesto presence and quality"""
        manifestos = []
        
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]
            
            for file in files:
                if 'MANIFIESTO' in file.upper() or 'MANIFESTO' in file.upper():
                    filepath = os.path.join(root, file)
                    manifestos.append(filepath)
        
        return {
            'manifesto_count': len(manifestos),
            'manifestos': manifestos
        }
    
    def calculate_total_coherence(self, psi_data, manifesto_data, qcal_ratio, freq_ratio):
        """Calculate total system coherence"""
        # Weighted coherence calculation
        weights = {
            'psi': 0.25,
            'manifesto': 0.15,
            'qcal': 0.35,
            'frequency': 0.25
        }
        
        psi_score = min(psi_data['psi_ratio'] * 2, 1.0)
        manifesto_score = min(manifesto_data['manifesto_count'] / 10, 1.0)
        qcal_score = min(qcal_ratio * 2, 1.0)
        freq_score = min(freq_ratio * 3, 1.0)
        
        total_coherence = (
            weights['psi'] * psi_score +
            weights['manifesto'] * manifesto_score +
            weights['qcal'] * qcal_score +
            weights['frequency'] * freq_score
        )
        
        return round(total_coherence, 4)
    
    def validate(self):
        """Run complete coherence validation"""
        print(f"🔬 Coherence Validator Starting...")
        print(f"   Frequency: {self.frequency} Hz")
        print(f"   Threshold: {self.threshold}")
        print(f"   Optimized: {self.optimized}")
        
        # Validate components
        print("\n📊 Validating components...")
        psi_data = self.validate_psi_state()
        manifesto_data = self.check_manifestos()
        
        # Load latest metrics for QCAL ratios
        qcal_ratio = 0.0
        freq_ratio = 0.0
        
        metrics_dir = Path('metrics')
        if metrics_dir.exists():
            metrics_files = sorted(metrics_dir.glob('daily_*.json'))
            if metrics_files:
                with open(metrics_files[-1], 'r') as f:
                    metrics = json.load(f)
                    total_files = metrics['files']['total_files']
                    if total_files > 0:
                        qcal_ratio = metrics['qcal']['qcal_references'] / total_files
                        freq_ratio = metrics['qcal']['frequency_references'] / total_files
        
        # Calculate total coherence
        total_coherence = self.calculate_total_coherence(
            psi_data, manifesto_data, qcal_ratio, freq_ratio
        )
        
        # Determine status
        status = "PASS" if total_coherence >= self.threshold else "EVOLVING"
        
        # Generate validation report
        validation = {
            'timestamp': self.timestamp,
            'frequency': self.frequency,
            'threshold': self.threshold,
            'psi_state': psi_data,
            'manifestos': manifesto_data,
            'coherence': {
                'total': total_coherence,
                'qcal_ratio': round(qcal_ratio, 4),
                'freq_ratio': round(freq_ratio, 4)
            },
            'status': status,
            'optimized_mode': self.optimized
        }
        
        # Save validation
        validation_dir = Path('validation')
        validation_dir.mkdir(exist_ok=True)
        
        validation_file = validation_dir / f"quantum_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(validation_file, 'w') as f:
            json.dump(validation, f, indent=2)
        
        print(f"\n✅ Validation saved: {validation_file}")
        print(f"\n🎯 Results:")
        print(f"   Ψ References: {psi_data['psi_references']}")
        print(f"   Manifestos: {manifesto_data['manifesto_count']}")
        print(f"   Total Coherence: {total_coherence}")
        print(f"   Status: {status}")
        
        return validation


def main():
    parser = argparse.ArgumentParser(description='QCAL Coherence Validator')
    parser.add_argument('--frequency', type=float, default=141.7001,
                        help='Base frequency (Hz)')
    parser.add_argument('--optimized', action='store_true',
                        help='Optimized mode')
    
    args = parser.parse_args()
    
    validator = CoherenceValidator(frequency=args.frequency, optimized=args.optimized)
    validation = validator.validate()
    
    return 0 if validation['status'] == 'PASS' else 1


if __name__ == '__main__':
    exit(main())
