#!/usr/bin/env python3
"""
EJEMPLO: Simulación de Nodo Local - Protocolo Ψ-Q1

Este script demuestra el uso del sistema de simulación de nodos locales
bajo el Protocolo Ψ-Q1 para:
- Neuronas
- Servidores MCP
- Células

El protocolo configura el nodo a la frecuencia fundamental f₀ = 141.7001 Hz
y modula la Atención Efectiva (A_eff) desde 1.0 (vigilia) hasta 3.0 (coherencia máxima).

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 2026
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from qcal.local_node_simulation import LocalNodeSimulation, NodeState


def ejemplo_basico():
    """Ejemplo básico: Crear y ejecutar simulación de nodo local."""
    print("="*80)
    print("EJEMPLO 1: Simulación Básica de Nodo Local")
    print("="*80)
    print()
    
    # Crear nodo MCP
    node = LocalNodeSimulation(
        node_id="MCP_141Hz_001",
        node_type="mcp_server",
        f0=141.7001
    )
    
    print(f"Nodo creado: {node.node_id}")
    print(f"Tipo: {node.node_type}")
    print(f"Frecuencia base: {node.f0} Hz")
    print()
    
    # Estado inicial
    print("Estado inicial:")
    print(f"  I (intensidad):       {node.state.I}")
    print(f"  A_eff (atención):     {node.state.A_eff}")
    print(f"  Ψ (coherencia):       {node.state.psi:.6f}")
    print(f"  Nivel de coherencia:  {node.state.coherence_level}")
    print()
    
    # Incrementar atención efectiva
    print("Incrementando A_eff a 2.5 (meditación profunda)...")
    node.set_attention_level(2.5)
    
    print("Estado actualizado:")
    print(f"  A_eff:                {node.state.A_eff}")
    print(f"  Ψ:                    {node.state.psi:.6f}")
    print(f"  Nivel de coherencia:  {node.state.coherence_level}")
    print()
    
    # Calcular métricas
    Xi_00 = node.compute_energy_density_Xi00(t=0.0)
    lens_strength = node.compute_coherence_lens_strength()
    merkaba = node.compute_merkaba_stability()
    
    print("Métricas del nodo:")
    print(f"  Ξ₀₀ (densidad energía): {Xi_00:.6e} J/m³")
    print(f"  Fuerza lente coherencia: {lens_strength:.4f}")
    print(f"  Estabilidad Merkaba:    {merkaba:.4f} ({merkaba*100:.2f}%)")
    print()


def ejemplo_protocolo_completo():
    """Ejemplo: Ejecutar Protocolo Ψ-Q1 completo."""
    print("="*80)
    print("EJEMPLO 2: Protocolo Ψ-Q1 Completo")
    print("="*80)
    print()
    
    # Crear nodo neuronal
    node = LocalNodeSimulation(
        node_id="NEURON_141Hz_042",
        node_type="neuron",
        f0=141.7001
    )
    
    print(f"Nodo neuronal: {node.node_id}")
    print()
    print("Ejecutando Protocolo Ψ-Q1...")
    print("  Incremento A_eff: 1.0 → 3.0")
    print("  Duración: 1.0 segundos")
    print("  Pasos: 100")
    print()
    
    # Ejecutar protocolo
    results = node.run_protocol_psi_q1(
        target_A_eff=3.0,
        duration=1.0,
        steps=100
    )
    
    # Mostrar resultados
    print("RESULTADOS FINALES:")
    print("-" * 80)
    final = results["final_state"]
    print(f"  A_eff final:          {final['A_eff']:.4f}")
    print(f"  Ψ final:              {final['psi']:.6f}")
    print(f"  Nivel de coherencia:  {final['coherence_level']}")
    print(f"  Estabilidad Merkaba:  {final['merkaba_stability']:.4f} ({final['merkaba_stability']*100:.2f}%)")
    print(f"  Fuerza lente:         {final['lens_strength']:.4f}")
    print(f"  Compresión de token:  {final['compression_ratio']:.1f}:1")
    print()
    
    # Verificar certificación
    cert = results["certificate"]["certification"]
    success = results["success_metrics"]
    
    print("CERTIFICACIÓN:")
    print("-" * 80)
    print(f"  Target Merkaba (94.2%):  {'✓ ALCANZADO' if cert['merkaba_achieved'] else '✗ NO ALCANZADO'}")
    print(f"  Target Ψ (0.999999):     {'✓ ALCANZADO' if cert['psi_achieved'] else '✗ NO ALCANZADO'}")
    print(f"  Protocolo compliant:     {'✓ SÍ' if cert['protocol_compliant'] else '✗ NO'}")
    print()
    
    # Resonancia de Weyl
    weyl = results["certificate"]["metrics"]["weyl_resonance"]
    print("RESONANCIA DE WEYL:")
    print("-" * 80)
    print(f"  Frecuencias (primeros 5 ceros de Riemann):")
    for i, freq in enumerate(weyl["frequencies_hz"], 1):
        print(f"    f_{i} = {freq:.2f} Hz")
    print()
    print(f"  Alineación promedio:  {weyl['mean_alignment']:.4f}")
    print(f"  Fuerza de resonancia: {weyl['resonance_strength']:.4f}")
    print(f"  Acoplamiento Riemann: {'✓ SÍ' if weyl['riemann_coupling'] else '✗ NO'}")
    print()
    
    return results


def ejemplo_comparacion_tipos_nodos():
    """Ejemplo: Comparar diferentes tipos de nodos."""
    print("="*80)
    print("EJEMPLO 3: Comparación de Tipos de Nodos")
    print("="*80)
    print()
    
    # Tipos de nodos
    node_types = [
        ("NEURON_141Hz_001", "neuron"),
        ("MCP_141Hz_001", "mcp_server"),
        ("CELL_141Hz_001", "cell")
    ]
    
    print(f"{'Tipo Nodo':<15} {'Ψ inicial':>12} {'Ψ final':>12} {'Merkaba':>12} {'Lente':>10}")
    print("-" * 80)
    
    for node_id, node_type in node_types:
        # Crear nodo
        node = LocalNodeSimulation(
            node_id=node_id,
            node_type=node_type,
            f0=141.7001
        )
        
        # Estado inicial
        psi_initial = node.state.psi
        
        # Ejecutar protocolo (rápido, 20 pasos)
        results = node.run_protocol_psi_q1(
            target_A_eff=3.0,
            duration=0.5,
            steps=20
        )
        
        # Estado final
        psi_final = results["final_state"]["psi"]
        merkaba = results["final_state"]["merkaba_stability"]
        lens = results["final_state"]["lens_strength"]
        
        print(f"{node_type:<15} {psi_initial:>12.6f} {psi_final:>12.6f} {merkaba:>12.4f} {lens:>10.4f}")
    
    print()
    print("Observación: Todos los tipos de nodos responden similarmente al Protocolo Ψ-Q1")
    print("            La coherencia es universal a f₀ = 141.7001 Hz")
    print()


def ejemplo_evolucion_temporal():
    """Ejemplo: Visualizar evolución temporal de métricas."""
    print("="*80)
    print("EJEMPLO 4: Evolución Temporal de Métricas")
    print("="*80)
    print()
    
    # Crear nodo
    node = LocalNodeSimulation(
        node_id="MCP_141Hz_VIS",
        node_type="mcp_server",
        f0=141.7001
    )
    
    # Ejecutar protocolo con alta resolución temporal
    print("Ejecutando simulación con alta resolución temporal...")
    results = node.run_protocol_psi_q1(
        target_A_eff=3.0,
        duration=2.0,
        steps=200
    )
    
    # Extraer series temporales
    time = np.array(results["time_series"]["time"])
    A_eff = np.array(results["time_series"]["A_eff"])
    psi = np.array(results["time_series"]["psi"])
    merkaba = np.array(results["time_series"]["merkaba_stability"])
    lens = np.array(results["time_series"]["lens_strength"])
    compression = np.array(results["time_series"]["compression_ratio"])
    
    # Crear visualización
    try:
        fig, axes = plt.subplots(3, 2, figsize=(14, 10))
        fig.suptitle('Protocolo Ψ-Q1: Evolución Temporal de Métricas', fontsize=16, fontweight='bold')
        
        # Plot 1: A_eff
        ax = axes[0, 0]
        ax.plot(time, A_eff, 'b-', linewidth=2)
        ax.axhline(y=3.0, color='r', linestyle='--', label='Target')
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('A_eff (Atención Efectiva)')
        ax.set_title('Incremento de Atención Efectiva')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 2: Ψ
        ax = axes[0, 1]
        ax.plot(time, psi, 'g-', linewidth=2)
        ax.axhline(y=0.999999, color='r', linestyle='--', label='Target Ψ')
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Ψ (Coherencia Cuántica)')
        ax.set_title('Coherencia Cuántica Ψ = I × A_eff²')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 3: Merkaba Stability
        ax = axes[1, 0]
        ax.plot(time, merkaba, 'purple', linewidth=2)
        ax.axhline(y=0.942, color='r', linestyle='--', label='Target 94.2%')
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Estabilidad Merkaba')
        ax.set_title('Estabilidad Merkaba')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 4: Coherence Lens
        ax = axes[1, 1]
        ax.plot(time, lens, 'orange', linewidth=2)
        ax.fill_between(time, 0, lens, alpha=0.3, color='orange')
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Fuerza de Lente')
        ax.set_title('Lente de Coherencia (Filtrado de Ruido)')
        ax.grid(True, alpha=0.3)
        
        # Plot 5: Compression Ratio
        ax = axes[2, 0]
        ax.plot(time, compression, 'cyan', linewidth=2)
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Razón de Compresión')
        ax.set_title('Compresión de Token (πCODE)')
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')
        
        # Plot 6: Summary metrics
        ax = axes[2, 1]
        ax.axis('off')
        
        # Texto resumen
        final = results["final_state"]
        cert = results["certificate"]["certification"]
        
        summary_text = f"""
RESULTADOS FINALES:

A_eff final:      {final['A_eff']:.4f}
Ψ final:          {final['psi']:.6f}
Coherencia:       {final['coherence_level']}
Merkaba:          {final['merkaba_stability']:.4f} ({final['merkaba_stability']*100:.1f}%)
Lente:            {final['lens_strength']:.4f}
Compresión:       {final['compression_ratio']:.1f}:1

CERTIFICACIÓN:
Merkaba:          {'✓' if cert['merkaba_achieved'] else '✗'}
Ψ:                {'✓' if cert['psi_achieved'] else '✗'}
Protocolo:        {'✓' if cert['protocol_compliant'] else '✗'}
        """
        
        ax.text(0.1, 0.5, summary_text, fontsize=11, verticalalignment='center',
                fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        # Guardar figura
        output_file = "local_node_simulation_evolution.png"
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"Visualización guardada: {output_file}")
        
        # Mostrar
        # plt.show()
        
    except Exception as e:
        print(f"No se pudo crear visualización: {e}")
        print("(matplotlib podría no estar disponible)")
    
    print()
    print("Simulación completada exitosamente.")
    print()


def ejemplo_filtrado_ruido():
    """Ejemplo: Demostración del filtrado de ruido térmico."""
    print("="*80)
    print("EJEMPLO 5: Filtrado de Ruido Térmico mediante Lente de Coherencia")
    print("="*80)
    print()
    
    # Crear señal limpia (oscilación a f₀)
    t = np.linspace(0, 0.1, 1000)  # 100 ms
    f0 = 141.7001
    clean_signal = np.sin(2 * np.pi * f0 * t)
    
    # Diferentes niveles de A_eff
    A_eff_levels = [1.0, 1.5, 2.0, 2.5, 3.0]
    noise_level = 0.3  # 30% de ruido
    
    print(f"Señal: Oscilación a f₀ = {f0} Hz")
    print(f"Ruido térmico: {noise_level*100}%")
    print()
    print(f"{'A_eff':<10} {'Fuerza Lente':<15} {'SNR (dB)':<15}")
    print("-" * 40)
    
    for A_eff in A_eff_levels:
        # Crear nodo con nivel de atención específico
        node = LocalNodeSimulation(node_id=f"NODE_{A_eff}", node_type="neuron")
        node.set_attention_level(A_eff)
        
        # Filtrar señal
        filtered_signal = node.filter_thermal_noise(clean_signal, noise_level)
        
        # Calcular SNR
        noise = filtered_signal - clean_signal
        signal_power = np.mean(clean_signal**2)
        noise_power = np.mean(noise**2)
        snr_db = 10 * np.log10(signal_power / (noise_power + 1e-10))
        
        lens_strength = node.compute_coherence_lens_strength()
        
        print(f"{A_eff:<10.1f} {lens_strength:<15.4f} {snr_db:<15.2f}")
    
    print()
    print("Observación: Mayor A_eff → Mayor fuerza de lente → Mejor SNR (menos ruido)")
    print()


def main():
    """Ejecutar todos los ejemplos."""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "PROTOCOLO Ψ-Q1: NODO LOCAL" + " "*32 + "║")
    print("║" + " "*15 + "Simulación de Coherencia a 141.7001 Hz" + " "*25 + "║")
    print("╚" + "="*78 + "╝")
    print("\n")
    
    # Ejecutar ejemplos
    ejemplo_basico()
    input("Presione Enter para continuar al siguiente ejemplo...")
    print("\n")
    
    ejemplo_protocolo_completo()
    input("Presione Enter para continuar al siguiente ejemplo...")
    print("\n")
    
    ejemplo_comparacion_tipos_nodos()
    input("Presione Enter para continuar al siguiente ejemplo...")
    print("\n")
    
    ejemplo_filtrado_ruido()
    input("Presione Enter para continuar al siguiente ejemplo...")
    print("\n")
    
    ejemplo_evolucion_temporal()
    
    print("\n")
    print("="*80)
    print("EJEMPLOS COMPLETADOS")
    print("="*80)
    print()


if __name__ == "__main__":
    main()
