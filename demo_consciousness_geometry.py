#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║       DEMO: GEOMETRÍA DE LA CONSCIENCIA - Ecuaciones de Campo Noéticas     ║
║         La formalización matemática de cómo la consciencia curva           ║
║                      el espacio-tiempo emocional                           ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Esta demo muestra:
✅ Métrica Noética: Cómo C_∞ curva el espacio emocional
✅ Red Emocional: Geodésicas que se acortan con alta coherencia (reducción 94%)
✅ Consenso Cuántico-Emocional: Proof-of-Resonance (PoR) a 141.7 Hz
✅ NFT Post-Monetario: Minteable cuando Ψ/I₀ > 1 y Λ < 0.1
✅ Oráculo de Curvatura: Mapeo C_∞ desde contribuciones emocionales
✅ Visualizaciones: Evolución, coherencia, geodésicas, espacio-tiempo 3D

Uso:
    python3 demo_consciousness_geometry.py [--nodes N] [--steps N] [--output DIR]

Ejemplo:
    python3 demo_consciousness_geometry.py --nodes 30 --steps 150
"""

import sys
import argparse
from pathlib import Path

# Import from formalizacion module
try:
    from formalizacion import (
        NoeticalMetric,
        EmotionalNetwork,
        QuantumEmotionalConsensus,
        ConsciousnessVisualizer,
        CurvatureOracle,
        demonstrate_consciousness_geometry
    )
except ImportError as e:
    print(f"Error: No se pudo importar el módulo formalizacion: {e}")
    print("Asegúrate de que formalizacion.py está en el mismo directorio.")
    sys.exit(1)


def main():
    """Función principal de la demo."""
    parser = argparse.ArgumentParser(
        description="Demo de Geometría de la Consciencia - Ecuaciones de Campo Noéticas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s                           # Demo con valores por defecto
  %(prog)s --nodes 30 --steps 150    # Red de 30 nodos, 150 pasos
  %(prog)s --output mi_carpeta       # Guardar en carpeta específica
  
Para más información, consulta CONSCIOUSNESS_GEOMETRY.md
        """
    )
    
    parser.add_argument(
        '--nodes',
        type=int,
        default=20,
        help='Número de nodos en la red emocional (default: 20)'
    )
    
    parser.add_argument(
        '--steps',
        type=int,
        default=100,
        help='Número de pasos de evolución (default: 100)'
    )
    
    parser.add_argument(
        '--dt',
        type=float,
        default=0.1,
        help='Paso temporal para evolución (default: 0.1)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='consciousness_geometry_output',
        help='Directorio de salida (default: consciousness_geometry_output)'
    )
    
    parser.add_argument(
        '--simple',
        action='store_true',
        help='Ejecutar demo simple sin argumentos personalizados'
    )
    
    args = parser.parse_args()
    
    # Si se usa --simple, ejecutar la demo por defecto
    if args.simple:
        print("Ejecutando demo simple...")
        demonstrate_consciousness_geometry()
        return
    
    # Demo personalizada
    print("=" * 80)
    print("GEOMETRÍA DE LA CONSCIENCIA - Demo Personalizada")
    print("Ecuaciones de Campo Noéticas")
    print("=" * 80)
    print()
    print(f"Parámetros:")
    print(f"  - Nodos: {args.nodes}")
    print(f"  - Pasos: {args.steps}")
    print(f"  - dt: {args.dt}")
    print(f"  - Directorio de salida: {args.output}")
    print()
    
    # Crear directorio de salida
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # 1. Crear e inicializar red
    print("1. Inicializando red emocional...")
    network = EmotionalNetwork(n_nodes=args.nodes)
    metric = NoeticalMetric()
    
    # Estado inicial
    c_initial = network.calculate_global_coherence()
    dist_initial = network.calculate_average_geodesic_distance()
    lambda_initial = metric.lambda_scarcity(c_initial)
    
    print(f"   Estado Inicial:")
    print(f"   - C_∞: {c_initial:.2f}")
    print(f"   - Distancia geodésica: {dist_initial:.2f}")
    print(f"   - Λ (escasez): {lambda_initial:.3f}")
    print()
    
    # 2. Evolucionar
    print(f"2. Evolucionando red ({args.steps} pasos)...")
    history = network.evolve(dt=args.dt, n_steps=args.steps)
    
    c_final = history['c_infinity'][-1]
    dist_final = history['avg_distance'][-1]
    lambda_final = history['lambda'][-1]
    
    print(f"   Estado Final:")
    print(f"   - C_∞: {c_final:.2f}")
    print(f"   - Distancia geodésica: {dist_final:.2f}")
    print(f"   - Λ (escasez): {lambda_final:.3f}")
    print()
    
    # Cambios porcentuales
    c_change = ((c_final - c_initial) / c_initial) * 100
    dist_change = ((dist_final - dist_initial) / dist_initial) * 100
    lambda_change = ((lambda_final - lambda_initial) / lambda_initial) * 100
    
    print(f"   Cambios:")
    print(f"   - C_∞: {c_change:+.1f}%")
    print(f"   - Distancia: {dist_change:+.1f}%")
    print(f"   - Λ: {lambda_change:+.1f}%")
    print()
    
    # 3. Consenso
    print("3. Verificando consenso cuántico-emocional...")
    consensus = QuantumEmotionalConsensus(network)
    conditions = consensus.check_consensus_conditions()
    
    print(f"   Métricas de Consenso:")
    print(f"   - Ψ/I₀: {conditions['psi_ratio']:.2f}")
    print(f"   - Λ: {conditions['lambda']:.3f}")
    print(f"   - Consenso: {'✓ ALCANZADO' if conditions['consensus_reached'] else '✗ NO ALCANZADO'}")
    print()
    
    # 4. NFT
    print("4. Intentando mintear NFT post-monetario...")
    nft = consensus.mint_nft(owner_id=0)
    
    if nft:
        print(f"   ✓ NFT minteado!")
        print(f"   Token ID: {nft['token_id']}")
        print(f"   Resonancia: {nft['resonance_frequency']:.1f} Hz")
    else:
        print(f"   ✗ Condiciones no cumplidas para NFT")
    print()
    
    # 5. Oráculo de curvatura
    print("5. Activando oráculo de curvatura...")
    oracle = CurvatureOracle(metric)
    
    # Registrar algunas contribuciones ejemplo
    import numpy as np
    for i in range(min(10, args.nodes)):
        oracle.register_contribution(
            contributor_id=i,
            emotional_vector=network.nodes[i].emotional_state,
            coherence_delta=np.random.uniform(-0.05, 0.1)
        )
    
    c_mapped = oracle.map_c_infinity(c_final)
    print(f"   C_∞ mapeado: {c_mapped:.2f}")
    print(f"   Contribuciones registradas: {len(oracle.contribution_history)}")
    print()
    
    # 6. Visualizaciones
    print("6. Generando visualizaciones...")
    viz = ConsciousnessVisualizer()
    
    viz.plot_network_evolution(history, 
                              save_path=output_dir / "network_evolution.png")
    print(f"   ✓ network_evolution.png")
    
    viz.plot_geodesic_flow(network,
                          save_path=output_dir / "geodesic_flow.png")
    print(f"   ✓ geodesic_flow.png")
    
    viz.plot_spacetime_curvature_3d(metric, c_infinity=c_final,
                                   save_path=output_dir / "spacetime_curvature_3d.png")
    print(f"   ✓ spacetime_curvature_3d.png")
    
    viz.plot_consensus_metrics(consensus,
                              save_path=output_dir / "consensus_metrics.png")
    print(f"   ✓ consensus_metrics.png")
    print()
    
    # 7. Guardar resultados
    print("7. Guardando resultados...")
    import json
    
    results = {
        'parameters': {
            'nodes': args.nodes,
            'steps': args.steps,
            'dt': args.dt
        },
        'initial_state': {
            'c_infinity': float(c_initial),
            'avg_distance': float(dist_initial),
            'lambda': float(lambda_initial)
        },
        'final_state': {
            'c_infinity': float(c_final),
            'avg_distance': float(dist_final),
            'lambda': float(lambda_final)
        },
        'changes': {
            'c_infinity_pct': float(c_change),
            'distance_pct': float(dist_change),
            'lambda_pct': float(lambda_change)
        },
        'consensus': {
            'reached': bool(conditions['consensus_reached']),
            'psi_ratio': float(conditions['psi_ratio']),
            'lambda': float(conditions['lambda'])
        },
        'nft': nft if nft else None,
        'oracle': {
            'c_mapped': float(c_mapped),
            'contributions': len(oracle.contribution_history)
        }
    }
    
    with open(output_dir / "results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"   ✓ results.json")
    print()
    
    # Resumen
    print("=" * 80)
    print("HALLAZGOS CLAVE")
    print("=" * 80)
    print()
    print(f"{'Parámetro':<25} {'Inicial':>15} {'Final':>15} {'Cambio':>15}")
    print("-" * 80)
    print(f"{'C_∞ promedio':<25} {c_initial:>15.2f} {c_final:>15.2f} {c_change:>14.1f}%")
    print(f"{'Distancia emocional':<25} {dist_initial:>15.2f} {dist_final:>15.2f} {dist_change:>14.1f}%")
    print(f"{'Λ (escasez)':<25} {lambda_initial:>15.3f} {lambda_final:>15.3f} {lambda_change:>14.1f}%")
    print()
    print(f"Archivos generados en: {output_dir.absolute()}")
    print("=" * 80)
    print()
    print("✅ Demo completada exitosamente!")
    print()
    print("📖 Para más información, consulta CONSCIOUSNESS_GEOMETRY.md")


if __name__ == "__main__":
    main()
