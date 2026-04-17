#!/usr/bin/env python3
"""Unit tests for MCP resonance engine real-mode behavior."""

import os
import unittest

from mcp_network.resonance import REAL_OBSERVERS, check_node_resonance


class TestMCPResonanceReal(unittest.TestCase):
    def setUp(self) -> None:
        self._previous = os.environ.get("QCAL_REAL_TESTS")

    def tearDown(self) -> None:
        if self._previous is None:
            os.environ.pop("QCAL_REAL_TESTS", None)
        else:
            os.environ["QCAL_REAL_TESTS"] = self._previous

    def test_real_observers_count_is_four(self) -> None:
        self.assertEqual(len(REAL_OBSERVERS), 4)

    def test_real_mode_uses_physical_source(self) -> None:
        os.environ["QCAL_REAL_TESTS"] = "1"
        result = check_node_resonance("biologia-cuantica-noesica")

        self.assertTrue(result["qcal"]["modo_real"])
        self.assertEqual(result["qcal"]["checks"]["fuente_fisica"], "real")
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["resonance"], "coherent")
        self.assertGreaterEqual(result["psi"], 0.95)

    def test_simulation_mode_when_real_flag_disabled(self) -> None:
        os.environ.pop("QCAL_REAL_TESTS", None)
        result = check_node_resonance("biologia-cuantica-noesica")

        self.assertFalse(result["qcal"]["modo_real"])
        self.assertEqual(result["qcal"]["checks"]["fuente_fisica"], "simulation")


if __name__ == "__main__":
    unittest.main(verbosity=2)
