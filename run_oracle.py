"""
Script principal para ejecutar el oráculo en diferentes modos.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import numpy as np

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from qcal_gravitational_oracle import GravitationalOracle
from real_time_oracle import RealTimeGravitationalOracle, RealTimeSimulator, RealTimeVisualizer


def parse_arguments(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    """Parse argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description="Oráculo Espectral Gravitacional")
    parser.add_argument("--mode", type=str, choices=["single", "realtime", "simulate"], default="single", help="Modo de operación")
    parser.add_argument("--evento", type=str, default="GW150914", help="Nombre del evento")
    parser.add_argument("--gps", type=float, default=1126259462.4, help="Tiempo GPS del evento")
    parser.add_argument("--duracion", type=float, default=32, help="Duración del análisis en segundos")
    parser.add_argument("--frecuencia", type=float, default=141.7001, help="Frecuencia objetivo en Hz")
    parser.add_argument("--buffer", type=int, default=32, help="Duración del buffer en tiempo real")
    parser.add_argument("--interfaz", type=str, nargs="+", default=["H1", "L1"], help="Interferómetros a usar")
    parser.add_argument("--plot", dest="plot", action="store_true", help="Generar gráficos")
    parser.add_argument("--no-plot", dest="plot", action="store_false", help="Desactivar gráficos")
    parser.set_defaults(plot=True)
    parser.add_argument("--output", type=str, default=None, help="Archivo de salida para resultados")
    parser.add_argument("--simulate-duration", type=float, default=60, help="Duración de simulación en segundos")
    parser.add_argument("--inject-time", type=float, default=20, help="Tiempo de inyección de señal (simulación)")
    return parser.parse_args(list(argv) if argv is not None else None)


def _to_serializable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _to_serializable(subvalue) for key, subvalue in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_serializable(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.float16, np.float32, np.float64)):
        return float(value)
    if isinstance(value, (np.int8, np.int16, np.int32, np.int64)):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if hasattr(value, "value") and hasattr(value, "sample_rate"):
        return {
            "name": getattr(value, "name", "timeseries"),
            "sample_rate": float(getattr(getattr(value, "sample_rate", 0.0), "value", 0.0)),
            "t0": float(getattr(getattr(value, "t0", 0.0), "value", 0.0)),
            "values": np.asarray(getattr(value, "value", []), dtype=float).tolist(),
        }
    return value


def run_single_analysis(args: argparse.Namespace) -> Dict[str, Any]:
    print("\n" + "=" * 60)
    print("ORÁCULO GRAVITACIONAL - MODO ANÁLISIS ÚNICO")
    print("=" * 60)
    oracle = GravitationalOracle(f_target=args.frecuencia)
    results = oracle.analyze(
        evento=args.evento,
        t_gps=args.gps,
        duracion=args.duracion,
        ifos=args.interfaz,
        plot=args.plot,
    )
    if args.output:
        save_results(results, args.output)
    return results


def run_realtime_analysis(args: argparse.Namespace) -> list[Dict[str, Any]]:
    print("\n" + "=" * 60)
    print("ORÁCULO GRAVITACIONAL - MODO TIEMPO REAL")
    print("=" * 60)
    oracle = RealTimeGravitationalOracle(
        f_target=args.frecuencia,
        buffer_duration=args.buffer,
        update_interval=2,
    )
    oracle.start_acquisition(args.interfaz)
    visualizer = RealTimeVisualizer(oracle)
    try:
        visualizer.run()
    except KeyboardInterrupt:
        print("\nDeteniendo análisis en tiempo real...")
    finally:
        oracle.stop_acquisition()
        if args.output and oracle.history:
            save_realtime_history(oracle.history, args.output)
    return oracle.history


def run_simulation(args: argparse.Namespace) -> list[Dict[str, Any]]:
    print("\n" + "=" * 60)
    print("ORÁCULO GRAVITACIONAL - MODO SIMULACIÓN")
    print("=" * 60)
    print(f"Duración: {args.simulate_duration}s, Inyección en: {args.inject_time}s")
    print("=" * 60)
    oracle = RealTimeGravitationalOracle(
        f_target=args.frecuencia,
        buffer_duration=args.buffer,
        update_interval=1,
    )
    oracle.ifos = list(args.interfaz)
    simulator = RealTimeSimulator(oracle)
    visualizer = RealTimeVisualizer(oracle)
    import threading

    sim_thread = threading.Thread(
        target=simulator.start_simulation,
        kwargs={
            "duration": args.simulate_duration,
            "injection_time": args.inject_time,
            "injection_duration": 5,
        },
        daemon=True,
    )
    sim_thread.start()
    try:
        visualizer.run()
    except KeyboardInterrupt:
        print("\nDeteniendo simulación...")
    finally:
        simulator.stop_simulation()
        oracle.stop_acquisition()
        sim_thread.join(timeout=2.0)
        if args.output and oracle.history:
            save_realtime_history(oracle.history, args.output)
    return oracle.history


def save_results(results: Dict[str, Any], filename: str) -> None:
    serializable = _to_serializable(results)
    with open(filename, "w", encoding="utf-8") as handle:
        json.dump(serializable, handle, indent=2, default=str)
    print(f"Resultados guardados en: {filename}")


def save_realtime_history(history: list[Dict[str, Any]], filename: str) -> None:
    data = []
    for entry in history:
        if isinstance(entry, dict):
            classification = entry.get("classification", {})
            data.append(
                {
                    "timestamp": entry.get("timestamp", 0),
                    "coherence": classification.get("coherence", 0),
                    "snr": classification.get("snr", 0),
                    "phase": classification.get("phase", 0),
                    "status": classification.get("status", "Unknown"),
                }
            )
    with open(filename, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    print(f"Historial guardado en: {filename}")


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_arguments(argv)
    if args.mode == "single":
        run_single_analysis(args)
    elif args.mode == "realtime":
        run_realtime_analysis(args)
    elif args.mode == "simulate":
        run_simulation(args)
    else:
        print("Modo no soportado")
        return 1
    print("\n" + "=" * 60)
    print("ANÁLISIS COMPLETADO")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
