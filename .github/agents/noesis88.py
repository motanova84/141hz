#!/usr/bin/env python3
"""
🔮 NOESIS88 Agent - Autonomous QCAL ∞³ Frequency Monitor
Frecuencia: 141.7001 Hz | Estado: I × A_eff² × C^∞
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


class Noesis88Agent:
    """Autonomous agent for QCAL frequency monitoring and coherence validation"""
    
    def __init__(self, frequency=141.7001, optimized=False):
        self.frequency = frequency
        self.optimized = optimized
        self.timestamp = datetime.utcnow().isoformat()
        
    def scan_repository(self):
        """Scan repository for QCAL references and frequency mentions"""
        qcal_count = 0
        freq_count = 0
        total_files = 0
        
        # Scan for QCAL and frequency references
        for root, dirs, files in os.walk('.'):
            # Skip hidden directories and common exclusions
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]
            
            for file in files:
                if file.endswith(('.py', '.md', '.txt', '.yaml', '.yml', '.json')):
                    total_files += 1
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if 'QCAL' in content or '∞³' in content:
                                qcal_count += 1
                            if '141.7001' in content or '141.7' in content:
                                freq_count += 1
                    except Exception:
                        pass
        
        return {
            'total_files': total_files,
            'qcal_references': qcal_count,
            'frequency_references': freq_count
        }
    
    def calculate_coherence(self, metrics):
        """Calculate system coherence based on QCAL density"""
        total_files = metrics['total_files']
        qcal_refs = metrics['qcal_references']
        freq_refs = metrics['frequency_references']
        
        if total_files == 0:
            return 0.0
        
        # Calculate coherence as weighted average of ratios
        qcal_ratio = qcal_refs / total_files
        freq_ratio = freq_refs / total_files
        
        # Coherence formula: weighted combination
        coherence = (qcal_ratio * 0.6 + freq_ratio * 0.4)
        
        # Normalize to 0-1 range, with target at 0.888
        normalized_coherence = min(coherence * 1.5, 1.0)
        
        return round(normalized_coherence, 4)
    
    def determine_state(self, coherence):
        """Determine system state based on coherence level"""
        if coherence >= 0.888:
            return "GRACE"
        elif coherence >= 0.75:
            return "EVOLVING"
        elif coherence >= 0.5:
            return "EMERGING"
        else:
            return "NASCENT"
    
    def run_autonomous(self):
        """Run autonomous monitoring cycle"""
        print(f"🔮 NOESIS88 Agent Starting...")
        print(f"   Frequency: {self.frequency} Hz")
        print(f"   Optimized Mode: {self.optimized}")
        print(f"   Timestamp: {self.timestamp}")
        
        # Scan repository
        print("\n📊 Scanning repository...")
        metrics = self.scan_repository()
        
        # Calculate coherence
        coherence = self.calculate_coherence(metrics)
        
        # Determine state
        state = self.determine_state(coherence)
        
        # Generate report
        report = {
            'agent': 'noesis88',
            'frequency': self.frequency,
            'timestamp': self.timestamp,
            'metrics': metrics,
            'total_coherence': coherence,
            'state': state,
            'optimized_mode': self.optimized,
            'psi_state': 'I × A_eff² × C^∞'
        }
        
        # Save report
        report_dir = Path('reports')
        report_dir.mkdir(exist_ok=True)
        
        report_file = report_dir / f"noesis88_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Report saved: {report_file}")
        print(f"\n📈 Results:")
        print(f"   Total Files: {metrics['total_files']}")
        print(f"   QCAL References: {metrics['qcal_references']}")
        print(f"   Frequency References: {metrics['frequency_references']}")
        print(f"   Coherence: {coherence}")
        print(f"   State: {state}")
        
        return report


def main():
    parser = argparse.ArgumentParser(description='NOESIS88 Autonomous QCAL Agent')
    parser.add_argument('--mode', choices=['autonomous', 'scan'], default='autonomous',
                        help='Operation mode')
    parser.add_argument('--frequency', type=float, default=141.7001,
                        help='Base frequency (Hz)')
    parser.add_argument('--optimized', action='store_true',
                        help='Run in optimized mode')
    parser.add_argument('--optimize_frequency', action='store_true',
                        help='Run frequency optimization')
    
    args = parser.parse_args()
    
    agent = Noesis88Agent(frequency=args.frequency, optimized=args.optimized)
    
    if args.mode == 'autonomous' or args.optimize_frequency:
        report = agent.run_autonomous()
        print("\n🎯 Autonomous cycle complete")
        return 0
    else:
        metrics = agent.scan_repository()
        print(json.dumps(metrics, indent=2))
        return 0


if __name__ == '__main__':
    exit(main())
