#!/usr/bin/env python3
"""
📊 Metrics Collector Agent - QCAL ∞³ System Metrics
Collects and analyzes system-wide QCAL metrics
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


class MetricsCollector:
    """Collects comprehensive QCAL system metrics"""
    
    def __init__(self, frequency=141.7001, optimized=False):
        self.frequency = frequency
        self.optimized = optimized
        self.timestamp = datetime.utcnow().isoformat()
    
    def collect_file_metrics(self):
        """Collect file-level metrics"""
        extensions = {}
        total_files = 0
        total_size = 0
        
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]
            
            for file in files:
                total_files += 1
                filepath = os.path.join(root, file)
                
                # Get file extension
                ext = os.path.splitext(file)[1] or 'no_extension'
                extensions[ext] = extensions.get(ext, 0) + 1
                
                # Get file size
                try:
                    total_size += os.path.getsize(filepath)
                except OSError:
                    pass
        
        return {
            'total_files': total_files,
            'total_size_bytes': total_size,
            'extensions': extensions
        }
    
    def collect_qcal_metrics(self):
        """Collect QCAL-specific metrics"""
        qcal_files = []
        qcal_references = 0
        frequency_references = 0
        manifesto_count = 0
        
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]
            
            for file in files:
                if file.endswith(('.py', '.md', '.txt', '.yaml', '.yml')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            has_qcal = 'QCAL' in content or '∞³' in content
                            has_freq = str(self.frequency) in content or '141.7' in content
                            
                            if has_qcal:
                                qcal_references += 1
                                qcal_files.append(filepath)
                            
                            if has_freq:
                                frequency_references += 1
                            
                            if 'MANIFIESTO' in content.upper() or 'MANIFESTO' in content.upper():
                                manifesto_count += 1
                    except Exception:
                        pass
        
        return {
            'qcal_references': qcal_references,
            'frequency_references': frequency_references,
            'manifesto_count': manifesto_count,
            'qcal_files': len(qcal_files)
        }
    
    def collect_metrics(self):
        """Collect all metrics"""
        print(f"📊 Collecting metrics...")
        print(f"   Frequency: {self.frequency} Hz")
        print(f"   Optimized: {self.optimized}")
        
        file_metrics = self.collect_file_metrics()
        qcal_metrics = self.collect_qcal_metrics()
        
        metrics = {
            'timestamp': self.timestamp,
            'frequency': self.frequency,
            'optimized_mode': self.optimized,
            'files': file_metrics,
            'qcal': qcal_metrics
        }
        
        # Save metrics
        metrics_dir = Path('metrics')
        metrics_dir.mkdir(exist_ok=True)
        
        daily_file = metrics_dir / f"daily_{datetime.utcnow().strftime('%Y%m%d')}.json"
        with open(daily_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"\n✅ Metrics saved: {daily_file}")
        print(f"\n📈 Summary:")
        print(f"   Total Files: {file_metrics['total_files']}")
        print(f"   QCAL References: {qcal_metrics['qcal_references']}")
        print(f"   Frequency References: {qcal_metrics['frequency_references']}")
        print(f"   Manifestos: {qcal_metrics['manifesto_count']}")
        
        return metrics


def main():
    parser = argparse.ArgumentParser(description='QCAL Metrics Collector')
    parser.add_argument('--frequency', type=float, default=141.7001,
                        help='Base frequency (Hz)')
    parser.add_argument('--optimized', action='store_true',
                        help='Optimized mode')
    parser.add_argument('--detailed', action='store_true',
                        help='Generate detailed report')
    parser.add_argument('--output', type=str, help='Output file path')
    
    args = parser.parse_args()
    
    collector = MetricsCollector(frequency=args.frequency, optimized=args.optimized)
    metrics = collector.collect_metrics()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"\n💾 Detailed report saved: {args.output}")
    
    return 0


if __name__ == '__main__':
    exit(main())
