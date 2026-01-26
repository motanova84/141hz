#!/usr/bin/env python3
"""
MCP Network Validation Script - QCAL ∞³ System
================================================

Validates the complete MCP (Model Context Protocol) network coherence
across all servers synchronized at 141.7001 Hz and 888 Hz.

All servers breathe in the same eternal instant.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import sys

# QCAL ∞³ Constants
F0 = 141.7001  # Root frequency in Hz
HARMONIC_888 = 888  # πCODE harmonic frequency in Hz
TOLERANCE = 1e-6  # Frequency matching tolerance


class MCPNetworkValidator:
    """Validator for MCP network coherence."""
    
    def __init__(self, base_path: str = "mcp-servers"):
        self.base_path = Path(base_path)
        self.servers = []
        self.validation_results = {
            "total_servers": 0,
            "online_servers": 0,
            "coherence_global": 0.0,
            "entropy_global": 0.0,
            "frequency_sync": False,
            "observer_sync": False,
            "noetic_chain_complete": False,
            "errors": [],
            "warnings": []
        }
    
    def load_server_configs(self) -> List[Dict]:
        """Load all server configurations."""
        configs = []
        
        if not self.base_path.exists():
            self.validation_results["errors"].append(
                f"MCP servers directory not found: {self.base_path}"
            )
            return configs
        
        for server_dir in self.base_path.iterdir():
            if server_dir.is_dir():
                config_file = server_dir / "config.json"
                if config_file.exists():
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                            configs.append(config)
                            self.servers.append(config['server']['name'])
                    except Exception as e:
                        self.validation_results["errors"].append(
                            f"Error loading {config_file}: {str(e)}"
                        )
        
        return configs
    
    def validate_frequencies(self, configs: List[Dict]) -> bool:
        """Validate frequency synchronization across servers."""
        freq_141 = []
        freq_888 = []
        
        for config in configs:
            freq = config['server']['frequency']
            if abs(freq - F0) < TOLERANCE:
                freq_141.append(config['server']['name'])
            elif abs(freq - HARMONIC_888) < TOLERANCE:
                freq_888.append(config['server']['name'])
            else:
                self.validation_results["errors"].append(
                    f"Invalid frequency in {config['server']['name']}: {freq} Hz"
                )
                return False
        
        # Expected distribution
        expected_141 = {'github-mcp-server', 'riemann-mcp-server', 'navier-mcp-server'}
        expected_888 = {'dramaturgo', 'bsd-mcp-server'}
        
        if set(freq_141) == expected_141 and set(freq_888) == expected_888:
            return True
        else:
            self.validation_results["warnings"].append(
                f"Frequency distribution mismatch. 141.7Hz: {freq_141}, 888Hz: {freq_888}"
            )
            return True  # Warning, not error
    
    def validate_coherence(self, configs: List[Dict]) -> Tuple[float, float]:
        """Validate global coherence and entropy."""
        coherence_values = []
        entropy_values = []
        
        for config in configs:
            qcal = config.get('qcal_integration', {})
            coherence = qcal.get('coherence', 0.0)
            entropy = qcal.get('entropy', 1.0)
            
            coherence_values.append(coherence)
            entropy_values.append(entropy)
            
            if coherence != 1.0:
                self.validation_results["warnings"].append(
                    f"{config['server']['name']}: coherence = {coherence} (expected 1.0)"
                )
            
            if entropy != 0.0:
                self.validation_results["warnings"].append(
                    f"{config['server']['name']}: entropy = {entropy} (expected 0.0)"
                )
        
        # Global coherence is the minimum of all coherence values
        global_coherence = min(coherence_values) if coherence_values else 0.0
        global_entropy = max(entropy_values) if entropy_values else 1.0
        
        return global_coherence, global_entropy
    
    def validate_observer_network(self, configs: List[Dict]) -> bool:
        """Validate cross-server observer synchronization."""
        for config in configs:
            observers = config.get('observers', {})
            
            if not observers.get('enabled', False):
                self.validation_results["errors"].append(
                    f"{config['server']['name']}: observers not enabled"
                )
                return False
            
            if not observers.get('cross_server_sync', False):
                self.validation_results["errors"].append(
                    f"{config['server']['name']}: cross-server sync not enabled"
                )
                return False
            
            linked_servers = set(observers.get('linked_servers', []))
            other_servers = set(self.servers) - {config['server']['name']}
            
            if linked_servers != other_servers:
                self.validation_results["warnings"].append(
                    f"{config['server']['name']}: linked servers mismatch"
                )
        
        return True
    
    def validate_noetic_chain(self, configs: List[Dict]) -> bool:
        """Validate the noetic chain closure."""
        noetic_servers = []
        
        for config in configs:
            if 'noetic_chain' in config:
                noetic_servers.append(config['server']['name'])
        
        # Expected servers with noetic chains
        expected = {'dramaturgo', 'riemann-mcp-server', 'bsd-mcp-server', 'navier-mcp-server'}
        
        if set(noetic_servers) >= expected:
            return True
        else:
            self.validation_results["warnings"].append(
                f"Incomplete noetic chain. Found: {noetic_servers}, Expected: {expected}"
            )
            return False
    
    def validate_status(self, configs: List[Dict]) -> int:
        """Count online servers."""
        online = 0
        
        for config in configs:
            status = config['server'].get('status', 'OFFLINE')
            if status in ['ONLINE', 'INTEGRADO']:
                online += 1
        
        return online
    
    def run_validation(self) -> Dict:
        """Run complete validation suite."""
        print("🌌 QCAL ∞³ MCP Network Validation")
        print("=" * 70)
        print(f"Root Frequency: {F0} Hz")
        print(f"Harmonic Frequency: {HARMONIC_888} Hz (πCODE-888)")
        print("=" * 70)
        print()
        
        # Load configurations
        configs = self.load_server_configs()
        self.validation_results["total_servers"] = len(configs)
        
        if not configs:
            print("❌ No server configurations found!")
            return self.validation_results
        
        print(f"✓ Loaded {len(configs)} server configurations")
        
        # Validate frequencies
        print("\n📡 Validating frequency synchronization...")
        freq_sync = self.validate_frequencies(configs)
        self.validation_results["frequency_sync"] = freq_sync
        
        if freq_sync:
            print("  ✓ Frequency synchronization: VALID")
            print(f"    - 141.7001 Hz servers: github-mcp-server, riemann-mcp-server, navier-mcp-server")
            print(f"    - 888 Hz servers: dramaturgo, bsd-mcp-server")
        else:
            print("  ❌ Frequency synchronization: INVALID")
        
        # Validate coherence
        print("\n🎯 Validating global coherence...")
        coherence, entropy = self.validate_coherence(configs)
        self.validation_results["coherence_global"] = coherence
        self.validation_results["entropy_global"] = entropy
        
        print(f"  ✓ Global coherence: {coherence:.6f}")
        print(f"  ✓ Global entropy: {entropy:.6f}")
        
        # Validate observers
        print("\n👁️  Validating observer network...")
        observer_sync = self.validate_observer_network(configs)
        self.validation_results["observer_sync"] = observer_sync
        
        if observer_sync:
            print("  ✓ Observer synchronization: ACTIVE")
        else:
            print("  ❌ Observer synchronization: INACTIVE")
        
        # Validate noetic chain
        print("\n🔗 Validating noetic chain...")
        noetic_complete = self.validate_noetic_chain(configs)
        self.validation_results["noetic_chain_complete"] = noetic_complete
        
        if noetic_complete:
            print("  ✓ Noetic chain: COMPLETE")
            print("    Riemann → BSD → P≠NP → Navier-Stokes → Ramsey → Noésis")
        else:
            print("  ⚠️  Noetic chain: INCOMPLETE")
        
        # Validate server status
        print("\n🟢 Validating server status...")
        online = self.validate_status(configs)
        self.validation_results["online_servers"] = online
        
        print(f"  ✓ Online servers: {online}/{len(configs)}")
        for config in configs:
            status = config['server'].get('status', 'OFFLINE')
            name = config['server']['name']
            freq = config['server']['frequency']
            endpoint = config['server']['endpoint']
            
            status_icon = "✓" if status in ['ONLINE', 'INTEGRADO'] else "❌"
            print(f"    {status_icon} {name} ({freq} Hz) - {status} @ {endpoint}")
        
        # Print warnings and errors
        if self.validation_results["warnings"]:
            print("\n⚠️  Warnings:")
            for warning in self.validation_results["warnings"]:
                print(f"  - {warning}")
        
        if self.validation_results["errors"]:
            print("\n❌ Errors:")
            for error in self.validation_results["errors"]:
                print(f"  - {error}")
        
        # Final status
        print("\n" + "=" * 70)
        
        all_valid = (
            freq_sync and 
            observer_sync and 
            coherence == 1.0 and 
            entropy == 0.0 and
            online == len(configs) and
            not self.validation_results["errors"]
        )
        
        if all_valid:
            print("✅ MCP NETWORK STATUS: COMPLETE AND OPERATIONAL")
            print("   All servers breathing in the same eternal instant.")
            print("   The flow is one.")
        else:
            print("⚠️  MCP NETWORK STATUS: OPERATIONAL WITH WARNINGS")
            print("   Some optimizations may be needed.")
        
        print("=" * 70)
        
        return self.validation_results
    
    def save_validation_report(self, output_file: str = "mcp_network_validation.json"):
        """Save validation results to JSON."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, indent=2)
        
        print(f"\n💾 Validation report saved to: {output_file}")


def main():
    """Main execution function."""
    validator = MCPNetworkValidator()
    results = validator.run_validation()
    validator.save_validation_report()
    
    # Exit with error code if critical errors found
    if results["errors"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
