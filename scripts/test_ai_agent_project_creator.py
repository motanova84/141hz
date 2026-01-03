#!/usr/bin/env python3
"""
Tests for AI Agent Project Creator
===================================

Test suite for the AI agent that automatically creates and activates projects.

Usage:
    python scripts/test_ai_agent_project_creator.py

Author: AI Agent System
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestProjectTemplates(unittest.TestCase):
    """Test project template generation"""
    
    def setUp(self):
        """Set up test fixtures"""
        from scripts.ai_agent_project_creator import (
            EventAnalysisTemplate,
            ValidationTemplate
        )
        self.EventAnalysisTemplate = EventAnalysisTemplate
        self.ValidationTemplate = ValidationTemplate
    
    def test_event_template_initialization(self):
        """Test event analysis template initialization"""
        template = self.EventAnalysisTemplate(
            'event',
            'GW250115',
            'Test analysis of GW250115'
        )
        
        self.assertEqual(template.project_type, 'event')
        self.assertEqual(template.name, 'GW250115')
        self.assertEqual(template.description, 'Test analysis of GW250115')
        self.assertIsNotNone(template.timestamp)
    
    def test_safe_name_generation(self):
        """Test safe name generation"""
        template = self.EventAnalysisTemplate(
            'event',
            'GW-250115',
            'Test'
        )
        
        self.assertEqual(template.get_safe_name(), 'gw_250115')
    
    def test_module_name_generation(self):
        """Test module name generation"""
        template = self.EventAnalysisTemplate(
            'event',
            'GW250115',
            'Test'
        )
        
        self.assertEqual(template.get_module_name(), 'gw250115_analysis')
    
    def test_event_script_generation(self):
        """Test event analysis script generation"""
        template = self.EventAnalysisTemplate(
            'event',
            'GW250115',
            'Test analysis'
        )
        
        script = template.generate_analysis_script()
        
        # Check key components
        self.assertIn('GW250115', script)
        self.assertIn('def __init__', script)
        self.assertIn('def download_data', script)
        self.assertIn('def calculate_snr', script)
        self.assertIn('141.7001', script)
        self.assertIn('if __name__', script)
    
    def test_event_test_generation(self):
        """Test event test script generation"""
        template = self.EventAnalysisTemplate(
            'event',
            'GW250115',
            'Test analysis'
        )
        
        test_script = template.generate_test_script()
        
        # Check key components
        self.assertIn('unittest', test_script)
        self.assertIn('class Test', test_script)
        self.assertIn('def setUp', test_script)
        self.assertIn('def test_', test_script)
    
    def test_event_documentation_generation(self):
        """Test event documentation generation"""
        template = self.EventAnalysisTemplate(
            'event',
            'GW250115',
            'Test analysis'
        )
        
        doc = template.generate_documentation()
        
        # Check key components
        self.assertIn('# GW250115', doc)
        self.assertIn('## Overview', doc)
        self.assertIn('## Usage', doc)
        self.assertIn('141.7001 Hz', doc)
    
    def test_validation_template_initialization(self):
        """Test validation template initialization"""
        template = self.ValidationTemplate(
            'validation',
            'coherence_test',
            'Test coherence validation'
        )
        
        self.assertEqual(template.project_type, 'validation')
        self.assertEqual(template.name, 'coherence_test')
    
    def test_validation_script_generation(self):
        """Test validation script generation"""
        template = self.ValidationTemplate(
            'validation',
            'coherence_test',
            'Test validation'
        )
        
        script = template.generate_validation_script()
        
        # Check key components
        self.assertIn('class', script)
        self.assertIn('def validate', script)
        self.assertIn('mpmath', script)
        self.assertIn('141.7001', script)


class TestAIProjectAgent(unittest.TestCase):
    """Test AI Project Agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        from scripts.ai_agent_project_creator import AIProjectAgent
        
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        self.agent = AIProjectAgent()
        
        # Override root_dir for testing
        self.agent.root_dir = Path(self.temp_dir)
        
        # Create necessary directories
        (self.agent.root_dir / 'scripts').mkdir(parents=True)
        (self.agent.root_dir / '.github' / 'workflows').mkdir(parents=True)
        (self.agent.root_dir / 'docs').mkdir(parents=True)
        
        # Create minimal Makefile
        makefile_content = '''
# Test Makefile
.PHONY: help

help:
\t@echo "Test Makefile"
'''
        with open(self.agent.root_dir / 'Makefile', 'w') as f:
            f.write(makefile_content)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(len(self.agent.projects_created), 0)
    
    def test_create_event_project(self):
        """Test creating event analysis project"""
        metadata = self.agent.create_project(
            'event',
            'GW250115',
            'Test event analysis'
        )
        
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata['name'], 'GW250115')
        self.assertEqual(metadata['type'], 'event')
        self.assertEqual(metadata['status'], 'active')
        
        # Check files were created
        self.assertTrue(len(metadata['files']) > 0)
        
        # Check analysis script exists
        script_path = self.agent.root_dir / 'scripts' / 'analizar_gw250115.py'
        self.assertTrue(script_path.exists())
        
        # Check test script exists
        test_path = self.agent.root_dir / 'scripts' / 'test_gw250115.py'
        self.assertTrue(test_path.exists())
        
        # Check documentation exists
        doc_path = self.agent.root_dir / 'docs' / 'GW250115_ANALYSIS.md'
        self.assertTrue(doc_path.exists())
        
        # Check metadata file exists
        metadata_path = self.agent.root_dir / 'projects' / 'gw250115_metadata.json'
        self.assertTrue(metadata_path.exists())
    
    def test_create_validation_project(self):
        """Test creating validation project"""
        metadata = self.agent.create_project(
            'validation',
            'coherence_test',
            'Test coherence validation'
        )
        
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata['name'], 'coherence_test')
        self.assertEqual(metadata['type'], 'validation')
        
        # Check validation script exists
        script_path = self.agent.root_dir / 'scripts' / 'validacion_coherence_test.py'
        self.assertTrue(script_path.exists())
    
    def test_makefile_update(self):
        """Test Makefile update"""
        self.agent.create_project(
            'event',
            'GW250115',
            'Test event'
        )
        
        # Check Makefile was updated
        makefile_path = self.agent.root_dir / 'Makefile'
        with open(makefile_path, 'r') as f:
            content = f.read()
        
        self.assertIn('analyze-gw250115', content)
        self.assertIn('test-gw250115', content)
    
    def test_workflow_creation(self):
        """Test GitHub Actions workflow creation"""
        self.agent.create_project(
            'event',
            'GW250115',
            'Test event'
        )
        
        # Check workflow file exists
        workflow_path = self.agent.root_dir / '.github' / 'workflows' / 'gw250115.yml'
        self.assertTrue(workflow_path.exists())
        
        # Check workflow content
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        self.assertIn('name: GW250115 Analysis', content)
        self.assertIn('python scripts/analizar_gw250115.py', content)
    
    def test_list_projects(self):
        """Test listing created projects"""
        # Create two projects
        self.agent.create_project('event', 'GW250115', 'Test 1')
        self.agent.create_project('validation', 'coherence_test', 'Test 2')
        
        # List projects
        projects = self.agent.list_projects()
        
        self.assertEqual(len(projects), 2)
        
        # Check project names
        project_names = [p['name'] for p in projects]
        self.assertIn('GW250115', project_names)
        self.assertIn('coherence_test', project_names)
    
    def test_multiple_projects(self):
        """Test creating multiple projects"""
        # Create three projects
        metadata1 = self.agent.create_project('event', 'GW250115', 'Event 1')
        metadata2 = self.agent.create_project('event', 'GW250116', 'Event 2')
        metadata3 = self.agent.create_project('validation', 'test_val', 'Val 1')
        
        self.assertEqual(len(self.agent.projects_created), 3)
        
        # Check all metadata files exist
        for name in ['gw250115', 'gw250116', 'test_val']:
            metadata_path = self.agent.root_dir / 'projects' / f'{name}_metadata.json'
            self.assertTrue(metadata_path.exists())


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestProjectTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestAIProjectAgent))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY - AI Agent Project Creator")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print(f"✅ All tests passed!")
    else:
        print(f"❌ Some tests failed")
    
    print(f"Success rate: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
    print("="*60)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
