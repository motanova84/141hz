#!/usr/bin/env python3
"""
Tests for qcal-harvest.py script.

This test validates that the QCAL harvest script correctly:
1. Finds .qcal-context.json files
2. Loads beacon files
3. Generates valid Markdown output
4. Preserves JSON structure
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path to import the harvester
sys.path.insert(0, str(Path(__file__).parent.parent))

from importlib.util import spec_from_file_location, module_from_spec

# Load qcal-harvest as module
spec = spec_from_file_location("qcal_harvest", "qcal-harvest.py")
qcal_harvest = module_from_spec(spec)
spec.loader.exec_module(qcal_harvest)

QCALHarvester = qcal_harvest.QCALHarvester


class TestQCALHarvester(unittest.TestCase):
    """Test suite for QCAL Harvester."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_context = {
            "node_name": "test-node",
            "core_frequency": 141.7001,
            "status": "Ψ=1.0"
        }
        
    def test_harvester_initialization(self):
        """Test harvester can be initialized."""
        harvester = QCALHarvester(repos_dir=self.temp_dir)
        self.assertIsNotNone(harvester)
        self.assertEqual(harvester.repos_dir, Path(self.temp_dir).resolve())
        
    def test_load_context_valid(self):
        """Test loading a valid context file."""
        # Create a test repo with context
        test_repo = Path(self.temp_dir) / "test-repo"
        test_repo.mkdir()
        
        context_file = test_repo / ".qcal-context.json"
        with open(context_file, 'w') as f:
            json.dump(self.test_context, f)
        
        harvester = QCALHarvester(repos_dir=self.temp_dir)
        context = harvester.load_context(test_repo)
        
        self.assertIsNotNone(context)
        self.assertEqual(context["node_name"], "test-node")
        self.assertEqual(context["core_frequency"], 141.7001)
        
    def test_load_beacon_valid(self):
        """Test loading a valid beacon file."""
        test_repo = Path(self.temp_dir) / "test-repo"
        test_repo.mkdir()
        
        beacon_file = test_repo / ".qcal_beacon"
        beacon_content = "# Ψ–BEACON–141.7001Hz\nfrequency = 141.7001 Hz"
        with open(beacon_file, 'w') as f:
            f.write(beacon_content)
        
        harvester = QCALHarvester(repos_dir=self.temp_dir)
        beacon = harvester.load_beacon(test_repo)
        
        self.assertIsNotNone(beacon)
        self.assertIn("141.7001", beacon)
        
    def test_find_qcal_repos(self):
        """Test finding QCAL repositories."""
        # Create multiple test repos
        for i in range(3):
            test_repo = Path(self.temp_dir) / f"repo-{i}"
            test_repo.mkdir()
            
            context_file = test_repo / ".qcal-context.json"
            with open(context_file, 'w') as f:
                json.dump({"node_name": f"node-{i}"}, f)
        
        harvester = QCALHarvester(repos_dir=self.temp_dir)
        repos = harvester.find_qcal_repos()
        
        # Should find the 3 test repos
        self.assertGreaterEqual(len(repos), 3)
        
    def test_generate_markdown(self):
        """Test Markdown generation."""
        harvester = QCALHarvester(repos_dir=self.temp_dir)
        harvester.global_context = {
            "test-repo": self.test_context
        }
        
        markdown = harvester.generate_markdown()
        
        self.assertIsNotNone(markdown)
        self.assertIn("QCAL ∞³", markdown)
        self.assertIn("test-repo", markdown)
        self.assertIn("141.7001", markdown)
        self.assertIn("Ψ=1.0", markdown)
        
    def test_harvest_real_repo(self):
        """Test harvesting from actual 141hz repository."""
        # This test runs against the real repo
        real_repo_path = Path(__file__).parent.parent
        
        harvester = QCALHarvester(repos_dir=str(real_repo_path))
        context = harvester.load_context(real_repo_path)
        
        # Should have loaded the .qcal-context.json from root
        self.assertIsNotNone(context)
        self.assertIn("node_name", context)
        self.assertEqual(context["core_frequency"], 141.7001)
        
    def test_json_in_markdown(self):
        """Test that generated Markdown contains valid JSON section."""
        harvester = QCALHarvester(repos_dir=self.temp_dir)
        harvester.global_context = {
            "test-repo": self.test_context
        }
        
        markdown = harvester.generate_markdown()
        
        # Extract JSON from markdown
        json_start = markdown.find("```json")
        json_end = markdown.find("```", json_start + 7)
        
        self.assertNotEqual(json_start, -1, "JSON section not found in markdown")
        
        json_str = markdown[json_start + 7:json_end].strip()
        
        # Should be valid JSON
        try:
            parsed = json.loads(json_str)
            self.assertIn("test-repo", parsed)
        except json.JSONDecodeError:
            self.fail("Generated markdown contains invalid JSON")


class TestQCALContextFile(unittest.TestCase):
    """Test the actual .qcal-context.json file in the repository."""
    
    def test_context_file_exists(self):
        """Test that .qcal-context.json exists."""
        context_file = Path(__file__).parent.parent / ".qcal-context.json"
        self.assertTrue(context_file.exists(), ".qcal-context.json not found")
        
    def test_context_file_valid_json(self):
        """Test that .qcal-context.json is valid JSON."""
        context_file = Path(__file__).parent.parent / ".qcal-context.json"
        
        with open(context_file) as f:
            try:
                context = json.load(f)
            except json.JSONDecodeError as e:
                self.fail(f".qcal-context.json is not valid JSON: {e}")
                
    def test_context_file_required_fields(self):
        """Test that .qcal-context.json has required fields."""
        context_file = Path(__file__).parent.parent / ".qcal-context.json"
        
        with open(context_file) as f:
            context = json.load(f)
        
        required_fields = [
            "node_name",
            "core_frequency",
            "constants_source",
            "status"
        ]
        
        for field in required_fields:
            self.assertIn(field, context, f"Required field '{field}' missing")
            
    def test_context_frequency_correct(self):
        """Test that core_frequency is 141.7001."""
        context_file = Path(__file__).parent.parent / ".qcal-context.json"
        
        with open(context_file) as f:
            context = json.load(f)
        
        self.assertEqual(context["core_frequency"], 141.7001)


if __name__ == "__main__":
    pytest_available = False
    try:
        import pytest
        pytest_available = True
    except ImportError:
        pass
    
    if pytest_available:
        sys.exit(pytest.main([__file__, "-v"]))
    else:
        unittest.main(verbosity=2)
