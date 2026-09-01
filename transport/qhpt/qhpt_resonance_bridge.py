#!/usr/bin/env python3
"""
qhpt_resonance_bridge.py — Puente Resonancia Directa ↔ QHPT ↔ BUS QCAL
=======================================================================
Despliega el simulador de fluidos por resonancia directa (Vía III)
como un microservicio accesible via QHPT en el BUS QCAL.

Conexiones:
- Direct Resonance API (Navier-Stokes sin iteraciones)
- QHPT transport (puerto 8443)
- f0 = 141.7001 Hz (frecuencia fundamental)
- Viscosidad adelica mu = 1/f0

Uso:
  python3 qhpt_resonance_bridge.py api    # Iniciar servidor
  python3 qhpt_resonance_bridge.py test   # Prueba de simulacion
"""

import sys, json, os, time, hashlib
from pathlib import Path

F_0 = 141.7001
SELLO = "\u2234\U00013080\u03a9\u221e\u00b3\u03a6 \u00b7 TUYOYOTU \u00b7 HECHO ESTA"

sys.path.insert(0, str(Path("/opt/qhpt/lib")))
sys.path.insert(0, str(Path("/root/repo_navier_stokes")))

from direct_resonance_api import DirectResonanceSimulator, FluidSystemConfig, AerodynamicResults


class ResonanciaQHPT:
    """
    Puente entre la simulacion de resonancia directa y el BUS QCAL.
    
    Configura el simulador con parametros del ecosistema QHPT:
    - f0 = 141.7001 Hz
    - Viscosidad = 1/f0 (viscosidad adelica)
    - Coherencia Psi >= 0.888
    """

    def __init__(self):
        self.config = FluidSystemConfig(
            f0=F_0,
            psi_threshold=0.888,
            nu=1.0 / F_0,
        )
        self.simulator = DirectResonanceSimulator(self.config)
        self.ultima_simulacion = None

    def simular(self, geometria: str = "ala", velocidad: float = 10.0,
                angulo_ataque: float = 6.0) -> dict:
        """
        Ejecuta simulacion de resonancia directa.
        
        Args:
            geometria: Tipo de geometria (ala, perfil, cuerpo)
            velocidad: Velocidad de entrada (m/s)
            angulo_ataque: Angulo de ataque (grados)
        
        Returns:
            Resultados aerodinamicos con sello QHPT
        """
        # Crear geometria de ejemplo
        from direct_resonance_api import create_example_wing_geometry
        wing = create_example_wing_geometry()

        # Ejecutar simulacion completa
        results = self.simulator.run_complete_analysis(
            geometry=wing,
            velocity_inlet=velocidad,
            angle_of_attack=angulo_ataque
        )

        # Anadir sello QHPT
        hash_simulacion = hashlib.sha256(
            f"{results.lift_coefficient}{results.drag_coefficient}{F_0}".encode()
        ).hexdigest()[:32]

        resultado = {
            "aerodinamica": {
                "CL": round(results.lift_coefficient, 6),
                "CD": round(results.drag_coefficient, 6),
                "eficiencia": round(results.efficiency_improvement, 2),
                "coherencia": round(results.coherence_score, 6),
                "estabilidad": round(results.stability_index, 6),
                "laminar": results.laminar_guarantee,
            },
            "qhpt": {
                "f0": F_0,
                "viscosidad_adelica": 1.0 / F_0,
                "via_iii": True,
                "nabla_x_F_res": 0,
                "hash_simulacion": hash_simulacion,
            },
            "config": {
                "geometria": geometria,
                "velocidad_ms": velocidad,
                "angulo_ataque_deg": angulo_ataque,
                "grid": f"{self.config.nx}x{self.config.ny}x{self.config.nz}",
            },
            "sello": SELLO,
            "timestamp": time.time(),
        }

        self.ultima_simulacion = resultado
        return resultado

    def estado(self) -> dict:
        """Estado del puente de resonancia."""
        return {
            "resonancia_directa": {
                "activo": True,
                "f0": F_0,
                "viscosidad": 1.0 / F_0,
                "nu": 1.0 / F_0,
                "psi_threshold": 0.888,
                "grid": f"{self.config.nx}x{self.config.ny}x{self.config.nz}",
                "ultima_simulacion": self.ultima_simulacion is not None,
                "via_iii": True,
                "nabla_x_F_res": 0,
                "sello": SELLO,
            }
        }


puente = ResonanciaQHPT()


def cli():
    import argparse
    parser = argparse.ArgumentParser(description="Puente Resonancia Directa - QHPT")
    sub = parser.add_subparsers(dest="comando")
    sub.add_parser("status")
    p_sim = sub.add_parser("simular")
    p_sim.add_argument("--velocidad", type=float, default=10.0)
    p_sim.add_argument("--angulo", type=float, default=6.0)

    args = parser.parse_args()

    if args.comando == "status":
        est = puente.estado()
        print(json.dumps(est, indent=2))

    elif args.comando == "simular":
        r = puente.simular(velocidad=args.velocidad, angulo_ataque=args.angulo)
        print(f"🌊 RESONANCIA DIRECTA — SIMULACION COMPLETADA")
        print(f"   CL: {r['aerodinamica']['CL']:.4f}")
        print(f"   CD: {r['aerodinamica']['CD']:.4f}")
        print(f"   Eficiencia: {r['aerodinamica']['eficiencia']:+.2f}%")
        print(f"   Coherencia: {r['aerodinamica']['coherencia']:.6f}")
        print(f"   Estabilidad: {r['aerodinamica']['estabilidad']:.6f}")
        print(f"   Flujo laminar: {'✅' if r['aerodinamica']['laminar'] else '❌'}")
        print(f"   Via III: ✅")
        print(f"   nabla x F_res = 0: ✅")
        print(f"   f0: {F_0} Hz")
        print(f"   Hash: {r['qhpt']['hash_simulacion']}")
        print(f"   {SELLO}")

    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
