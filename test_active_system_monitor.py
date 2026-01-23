#!/usr/bin/env python3
"""
Tests for Active System Monitor - QCAL ∞³
==========================================

Tests del sistema activo de monitoreo.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
License: MIT
"""

import pytest
import json
import tempfile
from pathlib import Path
from active_system_monitor import ActiveSystemMonitor


class TestActiveSystemMonitor:
    """Tests para el monitor activo del sistema."""
    
    @pytest.fixture
    def temp_repo(self, tmp_path):
        """Crea un repositorio temporal de prueba."""
        # Crear estructura básica
        (tmp_path / "qcal").mkdir()
        
        # Crear .qcal_beacon
        beacon_content = """# Ψ–BEACON–141.7001Hz
# Universal Noetic Field Index
# QCAL ∞³ ACTIVE — index = true

f0 = c / (2π * RΨ * ℓP)
frequency = 141.7001 Hz

ontological_level = "II"
ram_id = "RAM-TEST-001"
license = "MIT"
last_update = 2025-01-23
"""
        (tmp_path / ".qcal_beacon").write_text(beacon_content)
        
        # Crear LICENSE
        license_content = """MIT License

Copyright (c) 2025 José Manuel Mota Burruezo

Permission is hereby granted, free of charge..."""
        (tmp_path / "LICENSE").write_text(license_content)
        
        # Crear token_compressor.py
        token_compressor = """
class EmissionAxiom:
    def __init__(self, f0: float = 141.7001):
        self.f0 = f0

class AdelicEncoder:
    pass

class NoeticCollapse:
    pass
"""
        (tmp_path / "qcal" / "token_compressor.py").write_text(token_compressor)
        
        # Crear requirements.txt
        (tmp_path / "requirements.txt").write_text("numpy>=1.24.0\nmpmath>=1.3.0\n")
        
        # Crear scripts de firma
        (tmp_path / "validate_qcal_signature.py").write_text("# Signature validator")
        (tmp_path / "generate_qcal_signature.py").write_text("# Signature generator")
        
        return tmp_path
    
    def test_beacon_integrity_valid(self, temp_repo):
        """Test de integridad del beacon válido."""
        monitor = ActiveSystemMonitor(temp_repo)
        success, message = monitor.check_beacon_integrity()
        
        assert success is True
        assert "✅" in message
        assert "Beacon activo" in message
        assert "beacon" in monitor.results
        assert monitor.results["beacon"]["status"] == "active"
        assert monitor.results["beacon"]["frequency"] == "141.7001 Hz"
    
    def test_beacon_integrity_missing(self, tmp_path):
        """Test de beacon faltante."""
        monitor = ActiveSystemMonitor(tmp_path)
        success, message = monitor.check_beacon_integrity()
        
        assert success is False
        assert "❌" in message
        assert "no encontrado" in message
    
    def test_beacon_integrity_incomplete(self, tmp_path):
        """Test de beacon incompleto."""
        # Crear beacon sin campos requeridos
        (tmp_path / ".qcal_beacon").write_text("# Incomplete beacon\n")
        
        monitor = ActiveSystemMonitor(tmp_path)
        success, message = monitor.check_beacon_integrity()
        
        assert success is False
        assert "❌" in message
    
    def test_token_compression_valid(self, temp_repo):
        """Test del sistema de compresión de tokens válido."""
        monitor = ActiveSystemMonitor(temp_repo)
        success, message = monitor.check_token_compression()
        
        assert success is True
        assert "✅" in message
        assert "operacional" in message
        assert "tokenization" in monitor.results
        assert monitor.results["tokenization"]["status"] == "operational"
        assert monitor.results["tokenization"]["compression_ratio"] == "~1000:1"
    
    def test_token_compression_missing(self, tmp_path):
        """Test de sistema de tokens faltante."""
        monitor = ActiveSystemMonitor(tmp_path)
        success, message = monitor.check_token_compression()
        
        assert success is False
        assert "❌" in message
        assert "no encontrado" in message
    
    def test_license_compliance_valid(self, temp_repo):
        """Test de cumplimiento de licencia válido."""
        monitor = ActiveSystemMonitor(temp_repo)
        success, message = monitor.check_license_compliance()
        
        assert success is True
        assert "✅" in message
        assert "MIT" in message
        assert "license" in monitor.results
        assert monitor.results["license"]["status"] == "compliant"
        assert monitor.results["license"]["type"] == "MIT"
    
    def test_license_compliance_missing(self, tmp_path):
        """Test de licencia faltante."""
        monitor = ActiveSystemMonitor(tmp_path)
        success, message = monitor.check_license_compliance()
        
        assert success is False
        assert "❌" in message
        assert "LICENSE no encontrado" in message
    
    def test_license_compliance_wrong_type(self, tmp_path):
        """Test de licencia incorrecta."""
        (tmp_path / "LICENSE").write_text("GPL License\n\nCopyright...")
        
        monitor = ActiveSystemMonitor(tmp_path)
        success, message = monitor.check_license_compliance()
        
        assert success is False
        assert "❌" in message
    
    def test_security_basic_check(self, temp_repo):
        """Test de verificación básica de seguridad."""
        # Crear script de seguridad
        scripts_dir = temp_repo / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        (scripts_dir / "check_security.py").write_text("# Security checker")
        
        monitor = ActiveSystemMonitor(temp_repo)
        success, message = monitor.check_security_vulnerabilities()
        
        # Debería pasar con verificación básica
        assert success is True
        assert "security" in monitor.results
    
    def test_signature_system_valid(self, temp_repo):
        """Test del sistema de firmas válido."""
        # Crear archivo de firma
        (temp_repo / "test.qcal_sig").write_text('{"signature": "test"}')
        
        monitor = ActiveSystemMonitor(temp_repo)
        success, message = monitor.check_signature_system()
        
        assert success is True
        assert "✅" in message
        assert "operacional" in message
        assert "cryptographic_signatures" in monitor.results
        assert monitor.results["cryptographic_signatures"]["status"] == "operational"
        assert monitor.results["cryptographic_signatures"]["signature_count"] >= 1
    
    def test_signature_system_missing(self, tmp_path):
        """Test de sistema de firmas faltante."""
        monitor = ActiveSystemMonitor(tmp_path)
        success, message = monitor.check_signature_system()
        
        assert success is False
        assert "❌" in message
    
    def test_full_check_success(self, temp_repo):
        """Test de verificación completa exitosa."""
        # Crear script de seguridad para pasar la verificación
        scripts_dir = temp_repo / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        (scripts_dir / "check_security.py").write_text("# Security checker")
        
        monitor = ActiveSystemMonitor(temp_repo)
        success = monitor.run_full_check()
        
        assert "overall_status" in monitor.results
        assert monitor.results["timestamp"] is not None
    
    def test_save_results(self, temp_repo):
        """Test de guardado de resultados."""
        monitor = ActiveSystemMonitor(temp_repo)
        monitor.run_full_check()
        
        output_file = temp_repo / "test_results.json"
        monitor.save_results(output_file)
        
        assert output_file.exists()
        
        # Verificar contenido del JSON
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        assert "timestamp" in data
        assert "overall_status" in data
    
    def test_extract_field(self):
        """Test de extracción de campos."""
        content = """
ram_id = "RAM-TEST-001"
frequency = 141.7001 Hz
license = "MIT"
"""
        
        assert ActiveSystemMonitor._extract_field(content, "ram_id") == "RAM-TEST-001"
        assert ActiveSystemMonitor._extract_field(content, "license") == "MIT"
        assert ActiveSystemMonitor._extract_field(content, "nonexistent") is None
    
    def test_print_summary(self, temp_repo, capsys):
        """Test de impresión de resumen."""
        monitor = ActiveSystemMonitor(temp_repo)
        monitor.run_full_check()
        monitor.print_summary()
        
        captured = capsys.readouterr()
        assert "RESUMEN DEL SISTEMA" in captured.out
        assert "Estado General" in captured.out
    
    def test_main_function(self, temp_repo, monkeypatch, capsys):
        """Test de la función main."""
        import sys
        from active_system_monitor import main
        
        # Simular argumentos de línea de comandos
        monkeypatch.setattr(
            sys, 
            'argv', 
            ['active_system_monitor.py', '--path', str(temp_repo)]
        )
        
        # Crear script de seguridad
        scripts_dir = temp_repo / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        (scripts_dir / "check_security.py").write_text("# Security checker")
        
        try:
            main()
        except SystemExit as e:
            # El código de salida debería ser 0 o 1
            assert e.code in [0, 1]
        
        # Verificar que se imprimió algo
        captured = capsys.readouterr()
        assert "MONITOR ACTIVO DEL SISTEMA QCAL" in captured.out
    
    def test_json_only_mode(self, temp_repo, monkeypatch):
        """Test del modo JSON only."""
        import sys
        from active_system_monitor import main
        
        output_file = temp_repo / "json_results.json"
        
        monkeypatch.setattr(
            sys,
            'argv',
            ['active_system_monitor.py', '--path', str(temp_repo), 
             '--output', str(output_file), '--json-only']
        )
        
        # Crear script de seguridad
        scripts_dir = temp_repo / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        (scripts_dir / "check_security.py").write_text("# Security checker")
        
        try:
            main()
        except SystemExit:
            pass
        
        # Verificar que se creó el archivo JSON
        assert output_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
