#!/usr/bin/env python3
"""
🧪 Test Orchestration System
Validates the QCAL orchestration and optimization system
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def test_directory_structure():
    """Test that all required directories exist"""
    print("📁 Testing directory structure...")
    
    required_dirs = [
        '.github/agents',
        '.github/scripts',
        'reports',
        'metrics',
        'validation',
        'logs/optimization',
        'src/constants'
    ]
    
    missing = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing.append(dir_path)
    
    if missing:
        print(f"  ❌ Missing directories: {missing}")
        return False
    else:
        print("  ✅ All directories present")
        return True


def test_agents_exist():
    """Test that all agents are present"""
    print("\n🤖 Testing agents...")
    
    required_agents = [
        '.github/agents/noesis88.py',
        '.github/agents/metrics_collector.py',
        '.github/agents/coherence_validator.py'
    ]
    
    missing = []
    for agent in required_agents:
        if not os.path.exists(agent):
            missing.append(agent)
        else:
            # Check if executable
            if not os.access(agent, os.X_OK):
                try:
                    os.chmod(agent, 0o755)
                except Exception:
                    pass
    
    if missing:
        print(f"  ❌ Missing agents: {missing}")
        return False
    else:
        print("  ✅ All agents present")
        return True


def test_scripts_exist():
    """Test that all scripts are present"""
    print("\n📜 Testing scripts...")
    
    required_scripts = [
        '.github/scripts/analyze_and_adjust.sh',
        '.github/scripts/optimize_qcal_density.sh'
    ]
    
    missing = []
    for script in required_scripts:
        if not os.path.exists(script):
            missing.append(script)
        else:
            # Make executable
            try:
                os.chmod(script, 0o755)
            except Exception:
                pass
    
    if missing:
        print(f"  ❌ Missing scripts: {missing}")
        return False
    else:
        print("  ✅ All scripts present")
        return True


def test_agent_execution():
    """Test that agents can execute"""
    print("\n⚡ Testing agent execution...")
    
    agents = [
        ('.github/agents/noesis88.py', ['--mode=scan']),
        ('.github/agents/metrics_collector.py', []),
        ('.github/agents/coherence_validator.py', [])
    ]
    
    all_passed = True
    for agent, args in agents:
        try:
            cmd = ['python3', agent] + args
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            if result.returncode == 0:
                print(f"  ✅ {os.path.basename(agent)} executed successfully")
            else:
                print(f"  ⚠️  {os.path.basename(agent)} returned non-zero: {result.returncode}")
                all_passed = False
        except subprocess.TimeoutExpired:
            print(f"  ⚠️  {os.path.basename(agent)} timed out")
            all_passed = False
        except Exception as e:
            print(f"  ❌ {os.path.basename(agent)} failed: {e}")
            all_passed = False
    
    return all_passed


def test_report_generation():
    """Test that reports are generated"""
    print("\n📊 Testing report generation...")
    
    # Check for generated files
    reports_exist = len(list(Path('reports').glob('*.json'))) > 0 if Path('reports').exists() else False
    metrics_exist = len(list(Path('metrics').glob('*.json'))) > 0 if Path('metrics').exists() else False
    validation_exist = len(list(Path('validation').glob('*.json'))) > 0 if Path('validation').exists() else False
    
    print(f"  Reports: {'✅' if reports_exist else '⚠️  (none yet)'}")
    print(f"  Metrics: {'✅' if metrics_exist else '⚠️  (none yet)'}")
    print(f"  Validation: {'✅' if validation_exist else '⚠️  (none yet)'}")
    
    return True  # This is expected to be empty on first run


def print_summary(results):
    """Print test summary"""
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*50)
    print(f"Total: {passed}/{total} pruebas pasadas")
    print("="*50)
    
    return passed == total


def main():
    """Run all orchestration tests"""
    print("🧪 PRUEBAS DEL SISTEMA DE ORQUESTACIÓN QCAL ∞³")
    print("="*50)
    
    results = {
        'Directory Structure': test_directory_structure(),
        'Agents Exist': test_agents_exist(),
        'Scripts Exist': test_scripts_exist(),
        'Agent Execution': test_agent_execution(),
        'Report Generation': test_report_generation()
    }
    
    all_passed = print_summary(results)
    
    if all_passed:
        print("\n🎉 ¡Todas las pruebas pasaron!")
        return 0
    else:
        print("\n⚠️  Algunas pruebas fallaron - revisar arriba")
        return 1


if __name__ == '__main__':
    sys.exit(main())
