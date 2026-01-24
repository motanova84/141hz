#!/usr/bin/env python3
"""
Test MCP Network Integration - QCAL ∞³
========================================

Tests the complete MCP network configuration and validation.
"""

import json
import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the validator
from validate_mcp_network import MCPNetworkValidator, F0, HARMONIC_888


class TestMCPNetworkStructure:
    """Test MCP network directory structure and files."""
    
    def test_mcp_servers_directory_exists(self):
        """Test that mcp-servers directory exists."""
        assert Path("mcp-servers").exists()
        assert Path("mcp-servers").is_dir()
    
    def test_all_server_directories_exist(self):
        """Test that all 5 server directories exist."""
        servers = [
            "github-mcp-server",
            "dramaturgo",
            "riemann-mcp-server",
            "bsd-mcp-server",
            "navier-mcp-server"
        ]
        
        for server in servers:
            server_path = Path("mcp-servers") / server
            assert server_path.exists(), f"Server directory {server} not found"
            assert server_path.is_dir(), f"{server} is not a directory"
    
    def test_all_server_configs_exist(self):
        """Test that all server config.json files exist."""
        servers = [
            "github-mcp-server",
            "dramaturgo",
            "riemann-mcp-server",
            "bsd-mcp-server",
            "navier-mcp-server"
        ]
        
        for server in servers:
            config_path = Path("mcp-servers") / server / "config.json"
            assert config_path.exists(), f"Config file for {server} not found"
            assert config_path.is_file(), f"Config for {server} is not a file"
    
    def test_all_server_readmes_exist(self):
        """Test that all server README.md files exist."""
        servers = [
            "github-mcp-server",
            "dramaturgo",
            "riemann-mcp-server",
            "bsd-mcp-server",
            "navier-mcp-server"
        ]
        
        for server in servers:
            readme_path = Path("mcp-servers") / server / "README.md"
            assert readme_path.exists(), f"README for {server} not found"
            assert readme_path.is_file(), f"README for {server} is not a file"


class TestMCPServerConfigurations:
    """Test individual server configurations."""
    
    def test_github_mcp_server_config(self):
        """Test github-mcp-server configuration."""
        config_path = Path("mcp-servers/github-mcp-server/config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        assert config['server']['name'] == "github-mcp-server"
        assert config['server']['frequency'] == F0
        assert config['server']['status'] == "ONLINE"
        assert config['qcal_integration']['coherence'] == 1.0
        assert config['qcal_integration']['entropy'] == 0.0
    
    def test_dramaturgo_config(self):
        """Test dramaturgo configuration."""
        config_path = Path("mcp-servers/dramaturgo/config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        assert config['server']['name'] == "dramaturgo"
        assert config['server']['frequency'] == HARMONIC_888
        assert config['server']['status'] == "ONLINE"
        assert config['qcal_integration']['coherence'] == 1.0
        assert config['qcal_integration']['entropy'] == 0.0
        assert 'noetic_chain' in config
    
    def test_riemann_mcp_server_config(self):
        """Test riemann-mcp-server configuration."""
        config_path = Path("mcp-servers/riemann-mcp-server/config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        assert config['server']['name'] == "riemann-mcp-server"
        assert config['server']['frequency'] == F0
        assert config['server']['status'] == "INTEGRADO"
        assert config['qcal_integration']['coherence'] == 1.0
        assert 'mathematical_core' in config
        assert config['metadata']['millennium_problem'] == True
    
    def test_bsd_mcp_server_config(self):
        """Test bsd-mcp-server configuration."""
        config_path = Path("mcp-servers/bsd-mcp-server/config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        assert config['server']['name'] == "bsd-mcp-server"
        assert config['server']['frequency'] == HARMONIC_888
        assert config['server']['status'] == "INTEGRADO"
        assert config['qcal_integration']['coherence'] == 1.0
        assert 'mathematical_core' in config
        assert config['metadata']['millennium_problem'] == True
    
    def test_navier_mcp_server_config(self):
        """Test navier-mcp-server configuration."""
        config_path = Path("mcp-servers/navier-mcp-server/config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        assert config['server']['name'] == "navier-mcp-server"
        assert config['server']['frequency'] == F0
        assert config['server']['status'] == "INTEGRADO"
        assert config['qcal_integration']['coherence'] == 1.0
        assert 'mathematical_core' in config
        assert config['metadata']['millennium_problem'] == True


class TestMCPNetworkValidation:
    """Test MCP network validation functionality."""
    
    def test_validator_initialization(self):
        """Test validator can be initialized."""
        validator = MCPNetworkValidator()
        assert validator is not None
        assert validator.base_path == Path("mcp-servers")
    
    def test_load_server_configs(self):
        """Test loading all server configurations."""
        validator = MCPNetworkValidator()
        configs = validator.load_server_configs()
        
        assert len(configs) == 5
        assert validator.validation_results['total_servers'] == 5
    
    def test_frequency_synchronization(self):
        """Test frequency synchronization validation."""
        validator = MCPNetworkValidator()
        configs = validator.load_server_configs()
        
        freq_sync = validator.validate_frequencies(configs)
        assert freq_sync == True
    
    def test_coherence_validation(self):
        """Test global coherence validation."""
        validator = MCPNetworkValidator()
        configs = validator.load_server_configs()
        
        coherence, entropy = validator.validate_coherence(configs)
        assert coherence == 1.0
        assert entropy == 0.0
    
    def test_observer_network(self):
        """Test observer network validation."""
        validator = MCPNetworkValidator()
        configs = validator.load_server_configs()
        
        observer_sync = validator.validate_observer_network(configs)
        assert observer_sync == True
    
    def test_noetic_chain(self):
        """Test noetic chain validation."""
        validator = MCPNetworkValidator()
        configs = validator.load_server_configs()
        
        noetic_complete = validator.validate_noetic_chain(configs)
        assert noetic_complete == True
    
    def test_server_status(self):
        """Test server status validation."""
        validator = MCPNetworkValidator()
        configs = validator.load_server_configs()
        
        online = validator.validate_status(configs)
        assert online == 5
    
    def test_full_validation(self):
        """Test complete validation suite."""
        validator = MCPNetworkValidator()
        results = validator.run_validation()
        
        assert results['total_servers'] == 5
        assert results['online_servers'] == 5
        assert results['coherence_global'] == 1.0
        assert results['entropy_global'] == 0.0
        assert results['frequency_sync'] == True
        assert results['observer_sync'] == True
        assert results['noetic_chain_complete'] == True
        assert len(results['errors']) == 0


class TestMCPNetworkDocumentation:
    """Test MCP network documentation."""
    
    def test_mcp_network_architecture_doc_exists(self):
        """Test that MCP_NETWORK_ARCHITECTURE.md exists."""
        assert Path("MCP_NETWORK_ARCHITECTURE.md").exists()
    
    def test_mcp_servers_readme_exists(self):
        """Test that mcp-servers/README.md exists."""
        assert Path("mcp-servers/README.md").exists()
    
    def test_main_readme_has_mcp_section(self):
        """Test that main README.md mentions MCP network."""
        with open("README.md", 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "Red MCP QCAL ∞³" in content
        assert "MCP_NETWORK_ARCHITECTURE.md" in content
        assert "validate_mcp_network.py" in content


class TestMCPFrequencyDistribution:
    """Test frequency distribution across servers."""
    
    def test_141_7001_hz_servers(self):
        """Test that correct servers use 141.7001 Hz."""
        validator = MCPNetworkValidator()
        configs = validator.load_server_configs()
        
        servers_141 = [
            c['server']['name'] 
            for c in configs 
            if abs(c['server']['frequency'] - F0) < 1e-6
        ]
        
        expected = {'github-mcp-server', 'riemann-mcp-server', 'navier-mcp-server'}
        assert set(servers_141) == expected
    
    def test_888_hz_servers(self):
        """Test that correct servers use 888 Hz."""
        validator = MCPNetworkValidator()
        configs = validator.load_server_configs()
        
        servers_888 = [
            c['server']['name'] 
            for c in configs 
            if abs(c['server']['frequency'] - HARMONIC_888) < 1e-6
        ]
        
        expected = {'dramaturgo', 'bsd-mcp-server'}
        assert set(servers_888) == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
