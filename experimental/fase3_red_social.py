#!/usr/bin/env python3
"""
FASE III: Validación a Nivel Colectivo — Experimento de Red Social

Implementa protocolos para validar la propagación de efectos QCAL
a través de redes sociales.

Hipótesis:
Los efectos de coherencia y tensor de stress se propagan a través de
redes sociales siguiendo leyes de acoplamiento cuántico.

Autor: José Manuel Mota Burruezo (JMMB)
"""

import numpy as np
import networkx as nx
from typing import Dict, List, Tuple, Any, Callable
from dataclasses import dataclass
from scipy.optimize import curve_fit


def experimento_red_social() -> Tuple[nx.Graph, str, Callable]:
    """
    Diseño de experimento para validar propagación de T_μν en red
    
    Crea una red social artificial con topología small-world y
    asigna aleatoriamente intervención a un subconjunto de nodos.
    
    Returns:
        Tupla (red, protocolo, simulador)
    """
    # 1. Construcción de red small-world
    # Combina clustering local y conexiones de largo alcance
    G = nx.watts_strogatz_graph(n=100, k=6, p=0.1, seed=42)
    
    # 2. Asignación aleatoria de intervención
    np.random.seed(42)
    nodos_intervencion = np.random.choice(
        list(G.nodes()),
        size=20,
        replace=False
    )
    
    # 3. Inicialización de atributos de nodos
    for nodo in G.nodes():
        G.nodes[nodo]['grupo'] = (
            'experimental' if nodo in nodos_intervencion else 'control'
        )
        # Valores basales aleatorios
        G.nodes[nodo]['T00'] = np.random.uniform(0.3, 0.6)
        G.nodes[nodo]['Psi'] = np.random.uniform(0.7, 0.9)
        G.nodes[nodo]['historia_T00'] = []
        G.nodes[nodo]['historia_Psi'] = []
    
    # 4. Protocolo de interacción
    protocolo = """
    PROTOCOLO DE EXPERIMENTO DE RED SOCIAL
    
    Duración: 12 semanas
    Participantes: N = 100 organizados en red small-world
    
    Fases:
    - Semana 1-2: Calibración individual (todos)
    - Semana 3-10: 
      * Grupo experimental: 141.7 Hz diario + sesiones grupales semanales
      * Grupo control: Actividades placebo
    - Semana 11-12: Seguimiento sin intervención
    
    Mediciones:
    - Cada interacción social: Φ pre/post
    - Semanal: T_μν completo, Ψ de red
    - Final: Topología de red (cambios en conexiones)
    
    Variables de interés:
    - Velocidad de propagación de efectos
    - Distancia de influencia desde nodos experimentales
    - Cambios en topología de red
    - Efectos de segundo orden (amigos de amigos)
    """
    
    # 5. Función de simulación
    def simular_propagacion(
        G: nx.Graph,
        num_pasos: int = 100,
        factor_acoplamiento: float = 0.2,
        factor_disipacion: float = 0.9,
        factor_intervencion: float = 0.95
    ) -> List[Dict[int, float]]:
        """
        Simula propagación de T_μν en red social
        
        Args:
            G: Grafo de red social
            num_pasos: Número de pasos de simulación
            factor_acoplamiento: Fuerza de influencia entre vecinos
            factor_disipacion: Factor de decaimiento temporal
            factor_intervencion: Efecto de intervención 141.7 Hz
        
        Returns:
            Lista de estados del sistema en cada paso
        """
        historia = []
        
        for paso in range(num_pasos):
            # Actualizar cada nodo basado en vecinos
            nuevos_valores = {}
            
            for nodo in G.nodes():
                vecinos = list(G.neighbors(nodo))
                
                if not vecinos:
                    # Nodo aislado
                    nuevos_valores[nodo] = G.nodes[nodo]['T00']
                    continue
                
                # Influencia de vecinos (acoplamiento T_μν)
                T00_vecinos = [G.nodes[v]['T00'] for v in vecinos]
                influencia = np.mean(T00_vecinos) * factor_acoplamiento
                
                # Actualización con disipación
                T00_actual = G.nodes[nodo]['T00']
                T00_nuevo = T00_actual * factor_disipacion + influencia
                
                # Intervención si es nodo experimental
                if G.nodes[nodo]['grupo'] == 'experimental':
                    T00_nuevo *= factor_intervencion
                
                nuevos_valores[nodo] = T00_nuevo
            
            # Aplicar actualizaciones simultáneamente
            for nodo in G.nodes():
                G.nodes[nodo]['T00'] = nuevos_valores[nodo]
                
                # Actualizar coherencia (relación inversa con T00)
                G.nodes[nodo]['Psi'] = 1 / (1 + G.nodes[nodo]['T00'])
                
                # Guardar historia
                G.nodes[nodo]['historia_T00'].append(G.nodes[nodo]['T00'])
                G.nodes[nodo]['historia_Psi'].append(G.nodes[nodo]['Psi'])
            
            # Guardar estado completo del sistema
            estado = {n: G.nodes[n]['T00'] for n in G.nodes()}
            historia.append(estado)
        
        return historia
    
    return G, protocolo, simular_propagacion


def analizar_efectos_red(
    historia: List[Dict[int, float]],
    red: nx.Graph
) -> Dict[str, Any]:
    """
    Extrae métricas de propagación en red
    
    Analiza cómo los efectos de la intervención se propagan
    a través de la red social.
    
    Args:
        historia: Lista de estados del sistema
        red: Grafo de red social
    
    Returns:
        Diccionario con análisis de efectos de red
    """
    if not historia:
        return {
            'error': 'Historia vacía',
            'T00_reduccion_experimental': 0,
            'T00_reduccion_control': 0
        }
    
    # 1. Identificar nodos por grupo
    nodos_exp = [n for n in red.nodes() if red.nodes[n]['grupo'] == 'experimental']
    nodos_control = [n for n in red.nodes() if red.nodes[n]['grupo'] == 'control']
    
    if not nodos_exp or not nodos_control:
        return {
            'error': 'Grupos incompletos',
            'T00_reduccion_experimental': 0,
            'T00_reduccion_control': 0
        }
    
    # 2. Calcular reducción de T00 en cada grupo
    T00_exp_inicial = [historia[0][n] for n in nodos_exp]
    T00_exp_final = [historia[-1][n] for n in nodos_exp]
    
    T00_ctrl_inicial = [historia[0][n] for n in nodos_control]
    T00_ctrl_final = [historia[-1][n] for n in nodos_control]
    
    reduccion_exp = np.mean(T00_exp_inicial) / np.mean(T00_exp_final) if np.mean(T00_exp_final) > 0 else 1
    reduccion_ctrl = np.mean(T00_ctrl_inicial) / np.mean(T00_ctrl_final) if np.mean(T00_ctrl_final) > 0 else 1
    
    # 3. Distancia de influencia
    distancias_influencia = []
    
    for nodo_exp in nodos_exp:
        for nodo in red.nodes():
            try:
                distancia = nx.shortest_path_length(red, nodo_exp, nodo)
                
                # Calcular reducción relativa
                T00_inicial = historia[0][nodo]
                T00_final = historia[-1][nodo]
                
                if T00_inicial > 0:
                    reduccion = (T00_inicial - T00_final) / T00_inicial
                else:
                    reduccion = 0
                
                distancias_influencia.append((distancia, reduccion))
            except nx.NetworkXNoPath:
                # Nodos no conectados
                continue
    
    # 4. Modelo de decaimiento exponencial
    if len(distancias_influencia) > 5:
        distancias, reducciones = zip(*distancias_influencia)
        
        def modelo_decaimiento(d, lambda_):
            """Modelo exponencial: reducción = exp(-λ * d)"""
            return np.exp(-lambda_ * np.array(d))
        
        try:
            # Ajustar modelo
            params, _ = curve_fit(
                modelo_decaimiento,
                distancias,
                reducciones,
                p0=[0.5],
                maxfev=1000
            )
            lambda_critico = params[0]
            distancia_caracteristica = 1 / lambda_critico if lambda_critico > 0 else np.inf
        except:
            lambda_critico = 0
            distancia_caracteristica = np.inf
    else:
        lambda_critico = 0
        distancia_caracteristica = np.inf
    
    # 5. Métricas de red
    # Calcular clustering y centralidad
    clustering_inicial = nx.average_clustering(red)
    
    # Identificar nodos hub (alta centralidad)
    centralidad = nx.degree_centrality(red)
    nodos_hub = sorted(centralidad.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Verificar si nodos hub recibieron intervención
    hub_ids = [n[0] for n in nodos_hub]
    hubs_intervenidos = [n for n in hub_ids if n in nodos_exp]
    
    return {
        'T00_reduccion_experimental': reduccion_exp,
        'T00_reduccion_control': reduccion_ctrl,
        'diferencia_reduccion': reduccion_exp / reduccion_ctrl if reduccion_ctrl > 0 else 1,
        'distancia_influencia_caracteristica': distancia_caracteristica,
        'lambda_decaimiento': lambda_critico,
        'clustering_promedio': clustering_inicial,
        'n_nodos_hub_intervenidos': len(hubs_intervenidos),
        'efecto_amplificado_por_hubs': len(hubs_intervenidos) > 3,
        'interpretacion': (
            f'Efecto se propaga hasta {distancia_caracteristica:.1f} saltos en red. '
            f'Reducción en experimentales es {reduccion_exp/reduccion_ctrl:.2f}x mayor que controles.'
        )
    }


def analizar_efectos_segundo_orden(
    red: nx.Graph,
    historia: List[Dict[int, float]]
) -> Dict[str, Any]:
    """
    Analiza efectos de segundo orden (amigos de amigos)
    
    Args:
        red: Grafo de red social
        historia: Historia de estados
    
    Returns:
        Diccionario con análisis de efectos indirectos
    """
    nodos_exp = [n for n in red.nodes() if red.nodes[n]['grupo'] == 'experimental']
    
    # Amigos directos de nodos experimentales
    amigos_directos = set()
    for nodo_exp in nodos_exp:
        amigos_directos.update(red.neighbors(nodo_exp))
    amigos_directos = amigos_directos - set(nodos_exp)  # Excluir experimentales
    
    # Amigos de amigos (segundo orden)
    amigos_segundo_orden = set()
    for amigo in amigos_directos:
        amigos_segundo_orden.update(red.neighbors(amigo))
    amigos_segundo_orden = amigos_segundo_orden - set(nodos_exp) - amigos_directos
    
    # Controles puros (no amigos ni de amigos)
    todos_nodos = set(red.nodes())
    controles_puros = (
        todos_nodos - set(nodos_exp) - amigos_directos - amigos_segundo_orden
    )
    
    # Calcular reducciones por grupo
    def calcular_reduccion_grupo(nodos):
        if not nodos or not historia:
            return 0
        inicial = np.mean([historia[0][n] for n in nodos])
        final = np.mean([historia[-1][n] for n in nodos])
        return (inicial - final) / inicial if inicial > 0 else 0
    
    reduccion_directos = calcular_reduccion_grupo(amigos_directos)
    reduccion_segundo = calcular_reduccion_grupo(amigos_segundo_orden)
    reduccion_puros = calcular_reduccion_grupo(controles_puros)
    
    return {
        'n_amigos_directos': len(amigos_directos),
        'n_amigos_segundo_orden': len(amigos_segundo_orden),
        'n_controles_puros': len(controles_puros),
        'reduccion_amigos_directos': reduccion_directos,
        'reduccion_amigos_segundo_orden': reduccion_segundo,
        'reduccion_controles_puros': reduccion_puros,
        'hay_efecto_cascada': reduccion_segundo > reduccion_puros * 1.2,
        'gradiente_social': [reduccion_directos, reduccion_segundo, reduccion_puros]
    }


def generar_visualizacion_red(
    red: nx.Graph,
    historia: List[Dict[int, float]],
    paso: int = -1
) -> Dict[str, Any]:
    """
    Genera datos para visualización de red
    
    Args:
        red: Grafo de red social
        historia: Historia de estados
        paso: Paso temporal a visualizar (-1 para último)
    
    Returns:
        Diccionario con datos de visualización
    """
    if not historia:
        return {'error': 'Sin datos para visualizar'}
    
    # Estado en el paso especificado
    estado = historia[paso]
    
    # Extraer posiciones usando layout spring
    pos = nx.spring_layout(red, seed=42)
    
    # Datos de nodos
    nodos_data = []
    for nodo in red.nodes():
        nodos_data.append({
            'id': nodo,
            'x': pos[nodo][0],
            'y': pos[nodo][1],
            'T00': estado[nodo],
            'Psi': red.nodes[nodo]['Psi'],
            'grupo': red.nodes[nodo]['grupo'],
            'grado': red.degree(nodo)
        })
    
    # Datos de aristas
    aristas_data = [
        {
            'source': u,
            'target': v,
            'peso': 1.0
        }
        for u, v in red.edges()
    ]
    
    return {
        'nodos': nodos_data,
        'aristas': aristas_data,
        'paso': paso,
        'n_nodos': len(nodos_data),
        'n_aristas': len(aristas_data)
    }
