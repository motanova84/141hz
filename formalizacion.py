"""
╔════════════════════════════════════════════════════════════════════════════╗
║              GEOMETRÍA DE LA CONSCIENCIA - Ecuaciones de Campo Noéticas    ║
║         Formalización matemática de la curvatura del espacio-tiempo        ║
║                            emocional por consciencia                       ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

⚡ ECUACIÓN FUNDAMENTAL DE CAMPO NOÉTICO ⚡

    G_μν = κ_Π(T_μν(Φ) - 1/2 g_μν T) + Λ(C_∞)g_μν

Donde:
    - G_μν: Tensor de Einstein noético (curvatura del espacio emocional)
    - κ_Π: Constante de acoplamiento noético (relacionado con κ_π = 2.5773)
    - T_μν(Φ): Tensor energía-momento emocional (depende del campo Φ)
    - Λ(C_∞): Constante cosmológica emocional dependiente de consciencia
    - C_∞: Coherencia infinita (C_∞ → ∞ resuelve singularidad de escasez)

Resolución de Singularidad de Escasez:
    Λ(C_∞) = Λ_0 · e^(-C_∞/C_0) → 0 cuando C_∞ → ∞

Características principales:
    ✅ Métrica Noética: Cómo C_∞ curva el espacio emocional
    ✅ Red Emocional: Geodésicas que se acortan con alta coherencia (94%)
    ✅ Consenso Cuántico-Emocional: Proof-of-Resonance (PoR) a 141.7 Hz
    ✅ NFT Post-Monetario: Minteable cuando Ψ/I₀ > 1 y Λ < 0.1
    ✅ Oráculo de Curvatura: Mapeo C_∞ desde contribuciones emocionales
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import json
from pathlib import Path

# QCAL Constants
F0_HZ = 141.7001  # Fundamental frequency
KAPPA_PI = 2.5773  # QCAL constant
PHI = 1.618033988749895  # Golden ratio
OMEGA_0 = 2 * np.pi * F0_HZ  # Angular frequency


@dataclass
class NoeticalMetric:
    """
    Métrica Noética del espacio-tiempo emocional.
    
    Implementa la métrica que describe cómo la consciencia infinita C_∞
    curva el espacio emocional, similar a como la masa curva el espacio-tiempo.
    
    Métrica: ds² = -(1 - 2Λ(C_∞)/r) dt² + dr²/(1 - 2Λ(C_∞)/r) + r²dΩ²
    """
    
    lambda_0: float = 1.0  # Constante cosmológica base
    c_0: float = 1.0  # Escala de coherencia característica
    
    def lambda_scarcity(self, c_infinity: float) -> float:
        """
        Calcula la constante cosmológica emocional Λ(C_∞).
        
        Λ(C_∞) = Λ_0 · e^(-C_∞/C_0) → 0 cuando C_∞ → ∞
        
        Args:
            c_infinity: Coherencia infinita actual
            
        Returns:
            Valor de Λ (escasez emocional)
        """
        return self.lambda_0 * np.exp(-c_infinity / self.c_0)
    
    def metric_tensor(self, c_infinity: float, r: float) -> np.ndarray:
        """
        Calcula el tensor métrico g_μν del espacio-tiempo emocional.
        
        Args:
            c_infinity: Coherencia infinita
            r: Distancia emocional radial
            
        Returns:
            Tensor métrico 2x2 simplificado (t, r)
        """
        lambda_eff = self.lambda_scarcity(c_infinity)
        # Evitar división por cero
        r_safe = max(r, 1e-10)
        factor = 1 - 2 * lambda_eff / r_safe
        
        # Métrica simplificada (t, r)
        g = np.array([
            [-factor, 0],
            [0, 1/max(factor, 1e-10)]
        ])
        return g
    
    def curvature_scalar(self, c_infinity: float, r: float) -> float:
        """
        Calcula la curvatura escalar R del espacio emocional.
        
        Args:
            c_infinity: Coherencia infinita
            r: Distancia emocional
            
        Returns:
            Curvatura escalar R
        """
        lambda_eff = self.lambda_scarcity(c_infinity)
        r_safe = max(r, 1e-10)
        # R ∝ Λ/r²
        R = 4 * lambda_eff / (r_safe ** 2)
        return R
    
    def emotional_geodesic_length(self, c_infinity: float, 
                                  point_a: np.ndarray, 
                                  point_b: np.ndarray) -> float:
        """
        Calcula la longitud de la geodésica emocional entre dos puntos.
        
        Con alta coherencia C_∞, las geodésicas se acortan significativamente.
        
        Args:
            c_infinity: Coherencia infinita
            point_a: Punto inicial [x, y]
            point_b: Punto final [x, y]
            
        Returns:
            Longitud de la geodésica
        """
        # Distancia euclidiana base
        euclidean_dist = np.linalg.norm(point_b - point_a)
        
        # Factor de reducción debido a alta coherencia
        lambda_eff = self.lambda_scarcity(c_infinity)
        reduction_factor = np.exp(-c_infinity / (2 * self.c_0))
        
        # Longitud de geodésica reducida
        geodesic_length = euclidean_dist * (reduction_factor + lambda_eff)
        return geodesic_length


@dataclass
class EmotionalNode:
    """Nodo en la red emocional."""
    position: np.ndarray
    emotional_state: np.ndarray  # Vector de estado emocional
    coherence: float = 0.0
    
    
class EmotionalNetwork:
    """
    Red emocional que evoluciona según geodésicas en espacio-tiempo curvado.
    
    La red muestra cómo las conexiones emocionales se fortalecen y las distancias
    se reducen con el incremento de coherencia colectiva C_∞.
    """
    
    def __init__(self, n_nodes: int = 20, dimension: int = 2):
        """
        Inicializa la red emocional.
        
        Args:
            n_nodes: Número de nodos en la red
            dimension: Dimensión del espacio emocional
        """
        self.n_nodes = n_nodes
        self.dimension = dimension
        self.metric = NoeticalMetric()
        
        # Inicializar nodos con posiciones y estados aleatorios
        self.nodes = [
            EmotionalNode(
                position=np.random.randn(dimension),
                emotional_state=np.random.randn(dimension),
                coherence=np.random.uniform(0.3, 0.6)
            )
            for _ in range(n_nodes)
        ]
        
        # Matriz de adyacencia (conexiones emocionales)
        self.adjacency = np.zeros((n_nodes, n_nodes))
        self._initialize_connections()
        
    def _initialize_connections(self):
        """Inicializa conexiones emocionales basadas en proximidad."""
        for i in range(self.n_nodes):
            for j in range(i + 1, self.n_nodes):
                distance = np.linalg.norm(
                    self.nodes[i].position - self.nodes[j].position
                )
                # Conexión inversamente proporcional a la distancia
                if distance < 2.0:
                    strength = np.exp(-distance / 2.0)
                    self.adjacency[i, j] = strength
                    self.adjacency[j, i] = strength
    
    def calculate_global_coherence(self) -> float:
        """
        Calcula la coherencia global C_∞ de la red.
        
        Returns:
            Coherencia infinita C_∞
        """
        # Coherencia promedio ponderada por conexiones
        total_coherence = 0.0
        total_weight = 0.0
        
        for i in range(self.n_nodes):
            for j in range(i + 1, self.n_nodes):
                if self.adjacency[i, j] > 0:
                    weight = self.adjacency[i, j]
                    coherence_pair = (self.nodes[i].coherence + 
                                     self.nodes[j].coherence) / 2
                    total_coherence += weight * coherence_pair
                    total_weight += weight
        
        c_infinity = total_coherence / max(total_weight, 1e-10)
        return c_infinity
    
    def update_node_coherence(self, dt: float):
        """
        Actualiza la coherencia de cada nodo basándose en sus vecinos.
        
        Args:
            dt: Paso temporal
        """
        new_coherences = []
        
        for i in range(self.n_nodes):
            # Influencia de vecinos
            neighbor_influence = 0.0
            total_strength = 0.0
            
            for j in range(self.n_nodes):
                if i != j and self.adjacency[i, j] > 0:
                    neighbor_influence += (self.adjacency[i, j] * 
                                          self.nodes[j].coherence)
                    total_strength += self.adjacency[i, j]
            
            if total_strength > 0:
                avg_neighbor_coherence = neighbor_influence / total_strength
                # Actualización con retroalimentación positiva
                delta_c = 0.1 * dt * (avg_neighbor_coherence - 
                                      self.nodes[i].coherence)
                new_coherence = self.nodes[i].coherence + delta_c
                # Mantener en rango [0, 1]
                new_coherence = max(0.0, min(1.0, new_coherence))
            else:
                new_coherence = self.nodes[i].coherence
            
            new_coherences.append(new_coherence)
        
        # Aplicar nuevas coherencias
        for i, coherence in enumerate(new_coherences):
            self.nodes[i].coherence = coherence
    
    def calculate_average_geodesic_distance(self) -> float:
        """
        Calcula la distancia geodésica promedio en la red.
        
        Returns:
            Distancia promedio
        """
        c_infinity = self.calculate_global_coherence()
        total_distance = 0.0
        count = 0
        
        for i in range(self.n_nodes):
            for j in range(i + 1, self.n_nodes):
                if self.adjacency[i, j] > 0:
                    distance = self.metric.emotional_geodesic_length(
                        c_infinity,
                        self.nodes[i].position,
                        self.nodes[j].position
                    )
                    total_distance += distance
                    count += 1
        
        avg_distance = total_distance / max(count, 1)
        return avg_distance
    
    def evolve(self, dt: float = 0.1, n_steps: int = 100) -> Dict[str, List]:
        """
        Evoluciona la red emocional en el tiempo.
        
        Args:
            dt: Paso temporal
            n_steps: Número de pasos
            
        Returns:
            Diccionario con historia de evolución
        """
        history = {
            'time': [],
            'c_infinity': [],
            'avg_distance': [],
            'lambda': [],
            'coherence_nodes': []
        }
        
        for step in range(n_steps):
            time = step * dt
            c_infinity = self.calculate_global_coherence()
            avg_distance = self.calculate_average_geodesic_distance()
            lambda_val = self.metric.lambda_scarcity(c_infinity)
            
            history['time'].append(time)
            history['c_infinity'].append(c_infinity)
            history['avg_distance'].append(avg_distance)
            history['lambda'].append(lambda_val)
            history['coherence_nodes'].append(
                [node.coherence for node in self.nodes]
            )
            
            # Evolucionar red
            self.update_node_coherence(dt)
        
        return history


class QuantumEmotionalConsensus:
    """
    Sistema de consenso cuántico-emocional mediante Proof-of-Resonance (PoR).
    
    El consenso se alcanza cuando la red emocional resuena a la frecuencia
    fundamental f₀ = 141.7 Hz, permitiendo el minteo de NFTs post-monetarios.
    """
    
    def __init__(self, network: EmotionalNetwork, f0: float = F0_HZ):
        """
        Inicializa el sistema de consenso.
        
        Args:
            network: Red emocional
            f0: Frecuencia de resonancia fundamental
        """
        self.network = network
        self.f0 = f0
        self.omega_0 = 2 * np.pi * f0
        
    def calculate_coherence_field(self, t: float = 0.0) -> float:
        """
        Calcula el campo de coherencia Ψ de la red.
        
        Ψ = Σ A_i · cos(ω₀·t + φ_i) · coherence_i
        
        Args:
            t: Tiempo
            
        Returns:
            Valor del campo de coherencia Ψ
        """
        psi = 0.0
        for i, node in enumerate(self.network.nodes):
            phase = 2 * np.pi * np.random.random()  # Fase aleatoria inicial
            amplitude = 1.0
            contribution = (amplitude * np.cos(self.omega_0 * t + phase) * 
                          node.coherence)
            psi += contribution
        
        return psi
    
    def calculate_incoherence_baseline(self) -> float:
        """
        Calcula la línea base de incoherencia I₀.
        
        Returns:
            Valor de I₀
        """
        # Línea base: coherencia promedio sin sincronización
        i_0 = np.mean([node.coherence for node in self.network.nodes])
        return max(i_0, 0.1)
    
    def check_consensus_conditions(self) -> Dict[str, Any]:
        """
        Verifica las condiciones para alcanzar consenso y mintear NFT.
        
        Condiciones:
        1. Ψ/I₀ > 1 (coherencia supera línea base)
        2. Λ < 0.1 (escasez emocional resuelta)
        
        Returns:
            Diccionario con resultados de verificación
        """
        c_infinity = self.network.calculate_global_coherence()
        psi = self.calculate_coherence_field()
        i_0 = self.calculate_incoherence_baseline()
        lambda_val = self.network.metric.lambda_scarcity(c_infinity)
        
        psi_ratio = psi / i_0
        condition_1 = psi_ratio > 1.0
        condition_2 = lambda_val < 0.1
        consensus_reached = condition_1 and condition_2
        
        return {
            'consensus_reached': consensus_reached,
            'psi': psi,
            'i_0': i_0,
            'psi_ratio': psi_ratio,
            'lambda': lambda_val,
            'c_infinity': c_infinity,
            'condition_1': condition_1,  # Ψ/I₀ > 1
            'condition_2': condition_2,  # Λ < 0.1
        }
    
    def mint_nft(self, owner_id: int) -> Optional[Dict[str, Any]]:
        """
        Mintea un NFT post-monetario si se cumplen las condiciones.
        
        Args:
            owner_id: ID del propietario del NFT
            
        Returns:
            Metadata del NFT si se mintea, None si no se cumplen condiciones
        """
        conditions = self.check_consensus_conditions()
        
        if not conditions['consensus_reached']:
            return None
        
        # Crear metadata del NFT
        nft = {
            'token_id': f"QCAL-NFT-{owner_id}-{np.random.randint(1000, 9999)}",
            'owner_id': owner_id,
            'minted_at': 0.0,  # En implementación real sería timestamp
            'coherence_snapshot': conditions['c_infinity'],
            'psi_ratio': conditions['psi_ratio'],
            'lambda': conditions['lambda'],
            'resonance_frequency': self.f0,
            'network_size': self.network.n_nodes,
            'post_monetary': True,
            'consensus_type': 'Proof-of-Resonance',
        }
        
        return nft


class CurvatureOracle:
    """
    Oráculo de curvatura que mapea C_∞ desde contribuciones emocionales.
    
    El oráculo analiza las contribuciones individuales y calcula cómo
    afectan la curvatura global del espacio-tiempo emocional.
    """
    
    def __init__(self, metric: NoeticalMetric):
        """
        Inicializa el oráculo de curvatura.
        
        Args:
            metric: Métrica noética
        """
        self.metric = metric
        self.contribution_history: List[Dict] = []
    
    def register_contribution(self, contributor_id: int, 
                            emotional_vector: np.ndarray,
                            coherence_delta: float):
        """
        Registra una contribución emocional.
        
        Args:
            contributor_id: ID del contribuyente
            emotional_vector: Vector de estado emocional
            coherence_delta: Cambio en coherencia aportado
        """
        contribution = {
            'contributor_id': contributor_id,
            'emotional_vector': emotional_vector.tolist(),
            'coherence_delta': coherence_delta,
            'timestamp': len(self.contribution_history)
        }
        self.contribution_history.append(contribution)
    
    def map_c_infinity(self, current_c: float) -> float:
        """
        Mapea C_∞ basándose en contribuciones históricas.
        
        Args:
            current_c: Coherencia actual
            
        Returns:
            C_∞ mapeado
        """
        if not self.contribution_history:
            return current_c
        
        # Acumular delta de coherencia de contribuciones
        total_delta = sum(c['coherence_delta'] 
                         for c in self.contribution_history[-10:])
        
        # C_∞ crece con contribuciones positivas
        c_infinity = current_c + total_delta
        return max(0.0, c_infinity)
    
    def get_curvature_map(self, grid_size: int = 20) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Genera un mapa de curvatura del espacio emocional.
        
        Args:
            grid_size: Tamaño de la rejilla
            
        Returns:
            Tupla (X, Y, curvature) para visualización
        """
        x = np.linspace(-5, 5, grid_size)
        y = np.linspace(-5, 5, grid_size)
        X, Y = np.meshgrid(x, y)
        
        # Calcular curvatura en cada punto
        curvature = np.zeros_like(X)
        c_infinity = 2.0  # Valor ejemplo
        
        for i in range(grid_size):
            for j in range(grid_size):
                r = np.sqrt(X[i, j]**2 + Y[i, j]**2) + 0.1
                curvature[i, j] = self.metric.curvature_scalar(c_infinity, r)
        
        return X, Y, curvature


class ConsciousnessVisualizer:
    """
    Herramientas de visualización para geometría de consciencia.
    
    Genera gráficos de:
    - Evolución temporal de la red
    - Coherencia colectiva
    - Flujo de geodésicas
    - Espacio-tiempo emocional 3D
    """
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Inicializa el visualizador.
        
        Args:
            figsize: Tamaño de las figuras
        """
        self.figsize = figsize
    
    def plot_network_evolution(self, history: Dict[str, List], 
                               save_path: Optional[Path] = None) -> Figure:
        """
        Grafica la evolución temporal de la red emocional.
        
        Args:
            history: Diccionario con historia de evolución
            save_path: Ruta opcional para guardar la figura
            
        Returns:
            Figura de matplotlib
        """
        fig, axes = plt.subplots(2, 2, figsize=self.figsize)
        
        # C_∞ vs tiempo
        axes[0, 0].plot(history['time'], history['c_infinity'], 'b-', linewidth=2)
        axes[0, 0].set_xlabel('Tiempo')
        axes[0, 0].set_ylabel('C_∞ (Coherencia Infinita)')
        axes[0, 0].set_title('Evolución de Coherencia')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Distancia geodésica promedio
        axes[0, 1].plot(history['time'], history['avg_distance'], 'r-', linewidth=2)
        axes[0, 1].set_xlabel('Tiempo')
        axes[0, 1].set_ylabel('Distancia Geodésica Promedio')
        axes[0, 1].set_title('Acortamiento de Geodésicas')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Λ (escasez) vs tiempo
        axes[1, 0].plot(history['time'], history['lambda'], 'g-', linewidth=2)
        axes[1, 0].set_xlabel('Tiempo')
        axes[1, 0].set_ylabel('Λ (Escasez Emocional)')
        axes[1, 0].set_title('Resolución de Singularidad de Escasez')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].axhline(y=0.1, color='r', linestyle='--', 
                          label='Umbral NFT (Λ < 0.1)')
        axes[1, 0].legend()
        
        # Coherencia de nodos individuales (últimos valores)
        if history['coherence_nodes']:
            final_coherences = history['coherence_nodes'][-1]
            axes[1, 1].bar(range(len(final_coherences)), final_coherences)
            axes[1, 1].set_xlabel('ID de Nodo')
            axes[1, 1].set_ylabel('Coherencia')
            axes[1, 1].set_title('Coherencia por Nodo (Estado Final)')
            axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_geodesic_flow(self, network: EmotionalNetwork,
                          save_path: Optional[Path] = None) -> Figure:
        """
        Visualiza el flujo de geodésicas en la red emocional.
        
        Args:
            network: Red emocional
            save_path: Ruta opcional para guardar
            
        Returns:
            Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Dibujar nodos
        positions = np.array([node.position for node in network.nodes])
        coherences = np.array([node.coherence for node in network.nodes])
        
        scatter = ax.scatter(positions[:, 0], positions[:, 1], 
                           c=coherences, cmap='viridis', 
                           s=200, alpha=0.7, edgecolors='black', linewidth=2)
        
        # Dibujar geodésicas como conexiones
        c_infinity = network.calculate_global_coherence()
        for i in range(network.n_nodes):
            for j in range(i + 1, network.n_nodes):
                if network.adjacency[i, j] > 0:
                    # Calcular longitud de geodésica
                    length = network.metric.emotional_geodesic_length(
                        c_infinity,
                        network.nodes[i].position,
                        network.nodes[j].position
                    )
                    
                    # Grosor de línea proporcional a fuerza de conexión
                    linewidth = network.adjacency[i, j] * 3
                    
                    # Color basado en longitud (rojo = largo, verde = corto)
                    color = plt.cm.RdYlGn(1 - min(length / 5.0, 1.0))
                    
                    ax.plot([positions[i, 0], positions[j, 0]],
                           [positions[i, 1], positions[j, 1]],
                           color=color, linewidth=linewidth, alpha=0.5)
        
        ax.set_xlabel('Dimensión Emocional 1')
        ax.set_ylabel('Dimensión Emocional 2')
        ax.set_title(f'Flujo de Geodésicas (C_∞ = {c_infinity:.2f})')
        plt.colorbar(scatter, ax=ax, label='Coherencia de Nodo')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_spacetime_curvature_3d(self, metric: NoeticalMetric,
                                   c_infinity: float = 2.0,
                                   save_path: Optional[Path] = None) -> Figure:
        """
        Visualiza la curvatura del espacio-tiempo emocional en 3D.
        
        Args:
            metric: Métrica noética
            c_infinity: Valor de coherencia infinita
            save_path: Ruta opcional para guardar
            
        Returns:
            Figura de matplotlib
        """
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # Crear rejilla
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        
        # Calcular curvatura
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                r = np.sqrt(X[i, j]**2 + Y[i, j]**2) + 0.1
                Z[i, j] = metric.curvature_scalar(c_infinity, r)
        
        # Superficie de curvatura
        surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8,
                              edgecolor='none', antialiased=True)
        
        ax.set_xlabel('Dimensión Emocional X')
        ax.set_ylabel('Dimensión Emocional Y')
        ax.set_zlabel('Curvatura R')
        ax.set_title(f'Curvatura Espacio-Tiempo Emocional (C_∞ = {c_infinity:.2f})')
        fig.colorbar(surf, ax=ax, label='Curvatura Escalar', shrink=0.5)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_consensus_metrics(self, consensus: QuantumEmotionalConsensus,
                              save_path: Optional[Path] = None) -> Figure:
        """
        Visualiza métricas del consenso cuántico-emocional.
        
        Args:
            consensus: Sistema de consenso
            save_path: Ruta opcional para guardar
            
        Returns:
            Figura de matplotlib
        """
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        conditions = consensus.check_consensus_conditions()
        
        # Gráfico de barras con condiciones
        conditions_names = ['Ψ/I₀ > 1', 'Λ < 0.1', 'Consenso']
        conditions_values = [
            conditions['psi_ratio'],
            1 - conditions['lambda'] / 0.1,  # Normalizar para visualización
            1.0 if conditions['consensus_reached'] else 0.0
        ]
        colors = ['green' if conditions['condition_1'] else 'red',
                 'green' if conditions['condition_2'] else 'red',
                 'green' if conditions['consensus_reached'] else 'red']
        
        axes[0].bar(conditions_names, conditions_values, color=colors, alpha=0.7)
        axes[0].axhline(y=1.0, color='k', linestyle='--', linewidth=1)
        axes[0].set_ylabel('Valor Normalizado')
        axes[0].set_title('Condiciones de Consenso')
        axes[0].grid(True, alpha=0.3, axis='y')
        
        # Resonancia a f₀
        t = np.linspace(0, 0.1, 1000)
        psi_wave = np.array([consensus.calculate_coherence_field(ti) for ti in t])
        
        axes[1].plot(t * 1000, psi_wave, 'b-', linewidth=1.5)
        axes[1].set_xlabel('Tiempo (ms)')
        axes[1].set_ylabel('Ψ (Campo de Coherencia)')
        axes[1].set_title(f'Resonancia a f₀ = {consensus.f0:.1f} Hz')
        axes[1].grid(True, alpha=0.3)
        
        # Agregar línea base I₀
        i_0 = conditions['i_0']
        axes[1].axhline(y=i_0, color='r', linestyle='--', 
                       label=f'I₀ = {i_0:.2f}')
        axes[1].axhline(y=-i_0, color='r', linestyle='--')
        axes[1].legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig


def demonstrate_consciousness_geometry():
    """
    Función de demostración completa del sistema de geometría de consciencia.
    
    Ejecuta una simulación completa mostrando:
    - Evolución de red emocional
    - Reducción de geodésicas
    - Consenso cuántico-emocional
    - Minteo de NFT post-monetario
    - Visualizaciones
    """
    print("=" * 80)
    print("GEOMETRÍA DE LA CONSCIENCIA - Demostración Completa")
    print("Ecuaciones de Campo Noéticas")
    print("=" * 80)
    print()
    
    # 1. Crear red emocional
    print("1. Inicializando red emocional con 20 nodos...")
    network = EmotionalNetwork(n_nodes=20)
    
    # Estado inicial
    c_initial = network.calculate_global_coherence()
    dist_initial = network.calculate_average_geodesic_distance()
    lambda_initial = network.metric.lambda_scarcity(c_initial)
    
    print(f"   Estado Inicial:")
    print(f"   - C_∞: {c_initial:.2f}")
    print(f"   - Distancia geodésica promedio: {dist_initial:.2f}")
    print(f"   - Λ (escasez): {lambda_initial:.3f}")
    print()
    
    # 2. Evolucionar red
    print("2. Evolucionando red emocional (100 pasos)...")
    history = network.evolve(dt=0.1, n_steps=100)
    
    # Estado final
    c_final = history['c_infinity'][-1]
    dist_final = history['avg_distance'][-1]
    lambda_final = history['lambda'][-1]
    
    print(f"   Estado Final:")
    print(f"   - C_∞: {c_final:.2f}")
    print(f"   - Distancia geodésica promedio: {dist_final:.2f}")
    print(f"   - Λ (escasez): {lambda_final:.3f}")
    print()
    
    # Calcular cambios
    c_change = ((c_final - c_initial) / c_initial) * 100
    dist_change = ((dist_final - dist_initial) / dist_initial) * 100
    lambda_change = ((lambda_final - lambda_initial) / lambda_initial) * 100
    
    print(f"   Cambios:")
    print(f"   - C_∞: {c_change:+.1f}%")
    print(f"   - Distancia: {dist_change:+.1f}%")
    print(f"   - Λ: {lambda_change:+.1f}%")
    print()
    
    # 3. Consenso cuántico-emocional
    print("3. Verificando consenso cuántico-emocional...")
    consensus = QuantumEmotionalConsensus(network)
    conditions = consensus.check_consensus_conditions()
    
    print(f"   Métricas:")
    print(f"   - Ψ (coherencia): {conditions['psi']:.2f}")
    print(f"   - I₀ (línea base): {conditions['i_0']:.2f}")
    print(f"   - Ψ/I₀: {conditions['psi_ratio']:.2f}")
    print()
    print(f"   Condiciones:")
    print(f"   - Ψ/I₀ > 1: {'✓' if conditions['condition_1'] else '✗'}")
    print(f"   - Λ < 0.1: {'✓' if conditions['condition_2'] else '✗'}")
    print(f"   - Consenso alcanzado: {'✓' if conditions['consensus_reached'] else '✗'}")
    print()
    
    # 4. Minteo de NFT
    print("4. Intentando mintear NFT post-monetario...")
    nft = consensus.mint_nft(owner_id=0)
    
    if nft:
        print(f"   ✓ NFT minteado exitosamente!")
        print(f"   Token ID: {nft['token_id']}")
        print(f"   Tipo: {nft['consensus_type']}")
        print(f"   Frecuencia de resonancia: {nft['resonance_frequency']:.1f} Hz")
    else:
        print(f"   ✗ No se cumplen condiciones para mintear NFT")
        print(f"     (Se requiere Ψ/I₀ > 1 y Λ < 0.1)")
    print()
    
    # 5. Visualizaciones
    print("5. Generando visualizaciones...")
    viz = ConsciousnessVisualizer()
    
    # Crear directorio de salida
    output_dir = Path("consciousness_geometry_output")
    output_dir.mkdir(exist_ok=True)
    
    # Evolución de red
    viz.plot_network_evolution(history, 
                              save_path=output_dir / "network_evolution.png")
    print(f"   ✓ Evolución de red: {output_dir / 'network_evolution.png'}")
    
    # Flujo de geodésicas
    viz.plot_geodesic_flow(network,
                          save_path=output_dir / "geodesic_flow.png")
    print(f"   ✓ Flujo de geodésicas: {output_dir / 'geodesic_flow.png'}")
    
    # Curvatura 3D
    viz.plot_spacetime_curvature_3d(network.metric, c_infinity=c_final,
                                   save_path=output_dir / "spacetime_curvature_3d.png")
    print(f"   ✓ Curvatura 3D: {output_dir / 'spacetime_curvature_3d.png'}")
    
    # Métricas de consenso
    viz.plot_consensus_metrics(consensus,
                              save_path=output_dir / "consensus_metrics.png")
    print(f"   ✓ Métricas de consenso: {output_dir / 'consensus_metrics.png'}")
    print()
    
    # 6. Guardar resultados
    print("6. Guardando resultados...")
    results = {
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
        'nft': nft if nft else None
    }
    
    with open(output_dir / "results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"   ✓ Resultados guardados: {output_dir / 'results.json'}")
    print()
    
    # Resumen final
    print("=" * 80)
    print("RESUMEN DE HALLAZGOS CLAVE")
    print("=" * 80)
    print()
    print(f"{'Parámetro':<25} {'Estado Inicial':>15} {'Estado Final':>15} {'Cambio':>15}")
    print("-" * 80)
    print(f"{'C_∞ promedio':<25} {c_initial:>15.2f} {c_final:>15.2f} {c_change:>14.1f}%")
    print(f"{'Distancia emocional':<25} {dist_initial:>15.2f} {dist_final:>15.2f} {dist_change:>14.1f}%")
    print(f"{'Coherencia Ψ':<25} {conditions['i_0']:>15.2f} {conditions['psi']:>15.2f} {((conditions['psi']/conditions['i_0']-1)*100):>14.1f}%")
    print(f"{'Λ (escasez)':<25} {lambda_initial:>15.3f} {lambda_final:>15.3f} {lambda_change:>14.1f}%")
    print()
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    # Ejecutar demostración cuando se ejecuta el módulo directamente
    demonstrate_consciousness_geometry()
