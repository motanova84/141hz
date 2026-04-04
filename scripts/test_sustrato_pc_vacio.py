#!/usr/bin/env python3
"""
Test CI — Sustrato PC-Vacío ∴SPC∞³
=====================================

Script de test ejecutable por scripts/run_all_tests.py para el módulo
physics.sustrato_pc_vacio. Cubre los invariantes fundamentales del sistema:

  - f₀ = 141.7001 Hz
  - Nodos primos P = {2,3,5,7,11,13,17}
  - Fase Berry Φ = π/8 rad por salto
  - Vacío superfluido (ν → 0)
  - Frecuencia heterodina = f₀ (red C₇)
  - Reducción de inercia = 5.3 % (Destello de Masa)
  - R_symb ≈ 991.9 kpps
  - Ψ_global ≥ 0.888 → sello ∴SPC∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
RAM: RAM-XLVIII-2026-SUSTRATO-PC-VACIO
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.sustrato_pc_vacio import (
    ConstantesSustrato,
    VacioSuperfluido,
    RedRamsey,
    AcoplamientoHiggsPC,
    FotonPaqueteFase,
    FirmaEspectral,
    CoherenciaSustrato,
    SistemaSustratoPCVacio,
    sustrato_pc_vacio_activar,
    _F0,
    _PRIMOS_P,
    _FASE_BERRY_RAD,
    _G_EFF,
    _DELTA_INERCIA,
    _PSI_UMBRAL,
)


class TestSustratoPCVacioCI(unittest.TestCase):
    """Suite de CI para el módulo Sustrato PC-Vacío."""

    # ------------------------------------------------------------------
    # Constantes
    # ------------------------------------------------------------------

    def test_f0_es_141hz(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_primos_7_nodos(self):
        """Deben existir exactamente 7 nodos primos."""
        self.assertEqual(len(_PRIMOS_P), 7)

    def test_primos_correctos(self):
        """Los primos deben ser {2,3,5,7,11,13,17}."""
        self.assertEqual(set(_PRIMOS_P), {2, 3, 5, 7, 11, 13, 17})

    def test_suma_primos_58(self):
        """Suma de primos = 58."""
        self.assertEqual(sum(_PRIMOS_P), 58)

    def test_fase_berry_pi_sobre_8(self):
        """Fase de Berry = π/8."""
        self.assertAlmostEqual(_FASE_BERRY_RAD, math.pi / 8.0, places=10)

    def test_g_eff_perturbativo(self):
        """g_eff = 0.053 (perturbativo)."""
        self.assertAlmostEqual(_G_EFF, 0.053, places=5)
        self.assertLess(_G_EFF, 0.1)

    def test_psi_umbral_888(self):
        """Umbral de coherencia = 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    # ------------------------------------------------------------------
    # Vacío superfluido
    # ------------------------------------------------------------------

    def test_vacio_superfluido(self):
        """El vacío debe ser superfluido (ν < 1e-10)."""
        vs = VacioSuperfluido()
        self.assertTrue(vs.es_superfluido())

    def test_vacio_psi_sf_095(self):
        """Ψ_sf del vacío superfluido debe ser 0.95."""
        vs = VacioSuperfluido()
        self.assertAlmostEqual(vs.psi_superfluido(), 0.95, places=5)

    # ------------------------------------------------------------------
    # Red de Ramsey C₇
    # ------------------------------------------------------------------

    def test_red_frecuencia_heterodina(self):
        """La frecuencia heterodina de la red debe ser f₀."""
        red = RedRamsey()
        self.assertAlmostEqual(red.frecuencia_heterodina_hz(), _F0, places=4)

    def test_red_linea_critica_riemann(self):
        """La línea crítica de Riemann debe estar activa."""
        red = RedRamsey()
        self.assertTrue(red.es_linea_critica_riemann())

    def test_red_psi_uno(self):
        """Ψ_red = 1.0 (coherencia perfecta por construcción)."""
        red = RedRamsey()
        self.assertAlmostEqual(red.psi_red(), 1.0, places=6)

    # ------------------------------------------------------------------
    # Acoplamiento Higgs-PC
    # ------------------------------------------------------------------

    def test_acoplamiento_reduccion_inercia(self):
        """Reducción de inercia en el Destello = 5.3 %."""
        ac = AcoplamientoHiggsPC()
        self.assertAlmostEqual(ac.reduccion_inercia() * 100.0, 5.3, places=4)

    def test_acoplamiento_destello_activo(self):
        """El Destello de Masa debe estar activo."""
        ac = AcoplamientoHiggsPC()
        self.assertTrue(ac.es_destello_activo())

    def test_acoplamiento_masa_estrella_menor(self):
        """m* < m₀ (Destello reduce la masa)."""
        ac = AcoplamientoHiggsPC()
        self.assertLess(ac.masa_efectiva_gev(), ac.m0_gev)

    # ------------------------------------------------------------------
    # Fotones y transmisión
    # ------------------------------------------------------------------

    def test_transmision_r_symb(self):
        """R_symb debe ser ≈ 991.9 kpps."""
        fot = FotonPaqueteFase()
        self.assertAlmostEqual(fot.tasa_simbolica_kpps(), 991.9, delta=5.0)

    def test_transmision_ganancia_superradiante(self):
        """Ganancia superradiante = N² = 49."""
        fot = FotonPaqueteFase()
        self.assertAlmostEqual(fot.ganancia_superradiante(), 49.0, places=5)

    # ------------------------------------------------------------------
    # Firma espectral
    # ------------------------------------------------------------------

    def test_firma_amplitud_oscilacion(self):
        """Amplitud de oscilación de σ = 5.3 %."""
        fe = FirmaEspectral()
        self.assertAlmostEqual(
            fe.amplitud_oscilacion_porcentaje(), 5.3, places=4
        )

    def test_firma_ventana_transparencia(self):
        """Ventana de transparencia = f₀."""
        fe = FirmaEspectral()
        self.assertAlmostEqual(fe.ventana_transparencia_hz(), _F0, places=4)

    # ------------------------------------------------------------------
    # Coherencia global y sello
    # ------------------------------------------------------------------

    def test_psi_global_supera_umbral(self):
        """Ψ_global debe ser ≥ 0.888."""
        coh = CoherenciaSustrato()
        self.assertGreaterEqual(coh.psi_global(), _PSI_UMBRAL)

    def test_sello_activo(self):
        """El sello ∴SPC∞³ debe estar activo."""
        coh = CoherenciaSustrato()
        self.assertTrue(coh.sello_activo())

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def test_api_sello_spc(self):
        """API: sello = ∴SPC∞³."""
        r = sustrato_pc_vacio_activar()
        self.assertEqual(r["sello"], "∴SPC∞³")

    def test_api_sello_activo(self):
        """API: sello_activo = True."""
        r = sustrato_pc_vacio_activar()
        self.assertTrue(r["sello_activo"])

    def test_api_psi_global(self):
        """API: Ψ_global ≥ 0.888."""
        r = sustrato_pc_vacio_activar()
        self.assertGreaterEqual(r["psi_global"], 0.888)

    def test_api_f0_hz(self):
        """API: f₀ = 141.7001 Hz."""
        r = sustrato_pc_vacio_activar()
        self.assertAlmostEqual(r["f0_hz"], 141.7001, places=4)

    def test_api_primos_p(self):
        """API: primos_p = [2,3,5,7,11,13,17]."""
        r = sustrato_pc_vacio_activar()
        self.assertEqual(r["primos_p"], [2, 3, 5, 7, 11, 13, 17])

    def test_api_reduccion_inercia_pct(self):
        """API: reducción de inercia = 5.3 %."""
        r = sustrato_pc_vacio_activar()
        self.assertAlmostEqual(r["reduccion_inercia_pct"], 5.3, places=4)

    def test_api_destello_activo(self):
        """API: destello_activo = True."""
        r = sustrato_pc_vacio_activar()
        self.assertTrue(r["destello_activo"])

    def test_api_es_superfluido(self):
        """API: es_superfluido = True."""
        r = sustrato_pc_vacio_activar()
        self.assertTrue(r["es_superfluido"])


def main() -> int:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSustratoPCVacioCI)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
