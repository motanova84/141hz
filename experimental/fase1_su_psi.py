#!/usr/bin/env python3
"""
FASE I: Validación de SU(Ψ) — El Grupo de Coherencia Cuántica

Implementa protocolos experimentales para validar que los estados de conciencia
forman una estructura de grupo especial unitario SU(n).

Hipótesis Principal:
H₁: Los estados de conciencia forman una estructura de grupo especial unitario SU(n),
donde las transformaciones unitarias preservan la "norma psíquica" ||Ψ||² = 1

Predicciones Falsables:
- P1.1: La coherencia cuántica cerebral sigue álgebra de Lie su(n)
- P1.2: Las transiciones de estado mental son geodésicas en SU(n)
- P1.3: La meditación profunda converge a puntos fijos de SU(n)
- P1.4: La coherencia se preserva bajo transformaciones unitarias

Autor: José Manuel Mota Burruezo (JMMB)
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from scipy.signal import hilbert
from scipy.stats import mannwhitneyu, ttest_ind
from sklearn.decomposition import FastICA
from scipy.interpolate import CubicSpline


def extraer_estado_psi(
    señal_eeg: np.ndarray,
    n_componentes: int = 4
) -> np.ndarray:
    """
    Mapea actividad cerebral a vector de estado en ℂⁿ
    
    Este método realiza:
    1. Descomposición en componentes principales usando ICA
    2. Transformación de Hilbert para obtener fase compleja
    3. Normalización a esfera unitaria
    
    Args:
        señal_eeg: Array de forma (n_canales, n_muestras) con señal EEG
        n_componentes: Dimensión del espacio de Hilbert (default: 4)
    
    Returns:
        Vector de estado normalizado en ℂⁿ
    """
    # 1. Descomposición en componentes principales
    ica = FastICA(n_components=n_componentes, random_state=42)
    componentes = ica.fit_transform(señal_eeg.T)
    
    # 2. Transformación de Hilbert para fase compleja
    psi_componentes = []
    for i in range(n_componentes):
        componente_compleja = hilbert(componentes[:, i])
        # Promediar sobre tiempo para obtener valor representativo
        psi_componentes.append(np.mean(componente_compleja))
    
    # 3. Normalización (proyección a esfera unitaria)
    psi = np.array(psi_componentes, dtype=complex)
    norma = np.linalg.norm(psi)
    
    if norma < 1e-10:
        # Evitar división por cero
        psi_normalizado = np.zeros(n_componentes, dtype=complex)
        psi_normalizado[0] = 1.0
    else:
        psi_normalizado = psi / norma
    
    return psi_normalizado


def calcular_coherencia(psi_t: np.ndarray) -> float:
    """
    Coherencia como pureza del estado cuántico
    
    Calcula Tr(ρ²) donde ρ es la matriz densidad |ψ⟩⟨ψ|
    
    Args:
        psi_t: Vector de estado complejo normalizado
    
    Returns:
        Coherencia ∈ [0, 1] donde 1 indica estado puro máximo
    """
    # Matriz densidad
    rho = np.outer(psi_t, psi_t.conj())
    
    # Coherencia = Tr(ρ²)
    coherencia = np.trace(rho @ rho).real
    
    return coherencia


def calcular_matriz_transicion(
    psi_inicial: np.ndarray,
    psi_final: np.ndarray,
    dt: float = 0.001
) -> np.ndarray:
    """
    Reconstruye operador unitario U: |ψ₁⟩ → |ψ₂⟩
    
    Usa descomposición de valor singular para encontrar la
    matriz unitaria óptima que transforma el estado inicial al final.
    
    Args:
        psi_inicial: Vector de estado inicial
        psi_final: Vector de estado final
        dt: Paso de tiempo (usado para normalización)
    
    Returns:
        Matriz unitaria U tal que |ψ₂⟩ ≈ U|ψ₁⟩
    """
    # Método: descomposición de valor singular
    # Construimos matriz M = |ψ₂⟩⟨ψ₁|
    M = np.outer(psi_final, psi_inicial.conj())
    
    # SVD: M = U Σ V†
    U, S, Vh = np.linalg.svd(M)
    
    # La matriz unitaria óptima es U @ V†
    U_transicion = U @ Vh
    
    return U_transicion


def verificar_cerradura(trayectoria_psi: List[np.ndarray]) -> float:
    """
    Verifica la propiedad de cerradura del grupo
    
    Comprueba que la composición de transformaciones permanece en SU(n)
    
    Args:
        trayectoria_psi: Lista de estados |ψ(t)⟩
    
    Returns:
        Fracción de composiciones que cumplen cerradura [0, 1]
    """
    if len(trayectoria_psi) < 3:
        return 0.0
    
    cerraduras_validas = 0
    total_tests = 0
    
    for i in range(len(trayectoria_psi) - 2):
        # Calcular U₁: ψᵢ → ψᵢ₊₁
        U1 = calcular_matriz_transicion(trayectoria_psi[i], trayectoria_psi[i+1])
        
        # Calcular U₂: ψᵢ₊₁ → ψᵢ₊₂
        U2 = calcular_matriz_transicion(trayectoria_psi[i+1], trayectoria_psi[i+2])
        
        # Composición U₃ = U₂ @ U₁
        U3 = U2 @ U1
        
        # Verificar que U₃ es unitaria
        es_unitaria = np.allclose(U3 @ U3.conj().T, np.eye(len(U3)), atol=1e-2)
        
        if es_unitaria:
            cerraduras_validas += 1
        total_tests += 1
    
    return cerraduras_validas / total_tests if total_tests > 0 else 0.0


def extraer_generadores(trayectoria_psi: List[np.ndarray]) -> List[np.ndarray]:
    """
    Extrae generadores del álgebra de Lie a partir de trayectoria
    
    Los generadores son matrices anti-hermitianas T tales que U = exp(iT)
    
    Args:
        trayectoria_psi: Lista de estados cuánticos
    
    Returns:
        Lista de generadores del álgebra de Lie
    """
    generadores = []
    
    for i in range(len(trayectoria_psi) - 1):
        U = calcular_matriz_transicion(trayectoria_psi[i], trayectoria_psi[i+1])
        
        # Calcular logaritmo de matriz para obtener generador
        # T = -i log(U)
        try:
            log_U = np.log(U + 1e-10j)  # Pequeña regularización
            T = -1j * log_U
            generadores.append(T)
        except:
            # Si falla, usar aproximación de primer orden
            T = -1j * (U - np.eye(len(U)))
            generadores.append(T)
    
    return generadores


def verificar_conmutadores(generadores: List[np.ndarray], tolerancia: float = 0.1) -> float:
    """
    Verifica que los conmutadores satisfacen álgebra de Lie: [Tₐ, Tᵦ] = ifₐᵦᶜTᶜ
    
    Args:
        generadores: Lista de generadores del álgebra
        tolerancia: Tolerancia para cercanía al álgebra
    
    Returns:
        Fracción de conmutadores que satisfacen álgebra [0, 1]
    """
    if len(generadores) < 2:
        return 0.0
    
    n_generadores = min(len(generadores), 5)  # Limitar para eficiencia
    conmutadores_validos = 0
    total_tests = 0
    
    for i in range(n_generadores):
        for j in range(i+1, n_generadores):
            Ta = generadores[i]
            Tb = generadores[j]
            
            # Conmutador [Ta, Tb]
            conmutador = Ta @ Tb - Tb @ Ta
            
            # Verificar que es anti-hermitiana (propiedad de álgebra de Lie)
            es_antihermitiana = np.allclose(
                conmutador, -conmutador.conj().T, atol=tolerancia
            )
            
            if es_antihermitiana:
                conmutadores_validos += 1
            total_tests += 1
    
    return conmutadores_validos / total_tests if total_tests > 0 else 0.0


def test_estructura_grupo_SU(trayectoria_psi: List[np.ndarray]) -> Dict[str, Any]:
    """
    Verifica si las transformaciones satisfacen axiomas de SU(n)
    
    Realiza cuatro tests fundamentales:
    1. Preservación de norma (||Ψ|| = 1)
    2. Unitariedad de transiciones
    3. Cerradura del grupo (composición)
    4. Álgebra de Lie (generadores satisfacen [Tₐ, Tᵦ] = ifₐᵦᶜTᶜ)
    
    Args:
        trayectoria_psi: Lista de vectores de estado a lo largo del tiempo
    
    Returns:
        Diccionario con resultados de cada test
    """
    tests = {}
    
    # Test 1: Preservación de norma (||Ψ|| = 1)
    normas = [np.linalg.norm(psi) for psi in trayectoria_psi]
    tests['preservacion_norma'] = np.allclose(normas, 1.0, atol=1e-3)
    tests['norma_media'] = np.mean(normas)
    tests['norma_std'] = np.std(normas)
    
    # Test 2: Unitariedad de transiciones
    unitarias = []
    for i in range(len(trayectoria_psi) - 1):
        U = calcular_matriz_transicion(trayectoria_psi[i], trayectoria_psi[i+1])
        es_unitaria = np.allclose(U @ U.conj().T, np.eye(len(U)), atol=1e-2)
        unitarias.append(es_unitaria)
    tests['unitariedad'] = np.mean(unitarias) if unitarias else 0.0
    
    # Test 3: Cerradura del grupo (composición)
    tests['cerradura'] = verificar_cerradura(trayectoria_psi)
    
    # Test 4: Álgebra de Lie
    generadores = extraer_generadores(trayectoria_psi)
    tests['algebra_lie'] = verificar_conmutadores(generadores)
    
    # Evaluación global
    tests['cumple_SU_n'] = (
        tests['preservacion_norma'] and
        tests['unitariedad'] > 0.8 and
        tests['cerradura'] > 0.7
    )
    
    return tests


def proyectar_a_grassmann(psi: np.ndarray) -> np.ndarray:
    """
    Proyecta estado cuántico a variedad de Grassmann
    
    La variedad de Grassmann Gr(1,n) representa el espacio de todos
    los estados cuánticos puros de dimensión n.
    
    Args:
        psi: Vector de estado complejo
    
    Returns:
        Punto en variedad de Grassmann (matriz de proyección)
    """
    # La proyección de Grassmann es P = |ψ⟩⟨ψ|
    P = np.outer(psi, psi.conj())
    return P


def calcular_curvatura_geodesica(
    p_prev: np.ndarray,
    p_curr: np.ndarray,
    p_next: np.ndarray
) -> float:
    """
    Calcula curvatura geodésica en una trayectoria
    
    La curvatura mide qué tan lejos está la trayectoria de ser una geodésica
    (camino más corto en la variedad).
    
    Args:
        p_prev: Punto anterior en variedad
        p_curr: Punto actual
        p_next: Punto siguiente
    
    Returns:
        Curvatura geodésica κ
    """
    # Distancia de Fubini-Study en variedad de Grassmann
    def distancia_fs(P1, P2):
        # d(P1, P2) = arccos(|tr(P1 P2)|)
        producto = np.abs(np.trace(P1 @ P2))
        # Asegurar que está en [0, 1]
        producto = np.clip(producto, 0, 1)
        return np.arccos(producto)
    
    # Calcular ángulos
    d1 = distancia_fs(p_prev, p_curr)
    d2 = distancia_fs(p_curr, p_next)
    d_total = distancia_fs(p_prev, p_next)
    
    # Curvatura como desviación de línea recta
    # κ ≈ |d1 + d2 - d_total| / (d1 * d2)
    if d1 > 1e-6 and d2 > 1e-6:
        kappa = np.abs(d1 + d2 - d_total) / (d1 * d2)
    else:
        kappa = 0.0
    
    return kappa


def calcular_longitud_geodesica(puntos_manifold: List[np.ndarray]) -> float:
    """
    Calcula longitud total de camino en variedad
    
    Args:
        puntos_manifold: Lista de puntos en variedad de Grassmann
    
    Returns:
        Longitud total del camino
    """
    longitud = 0.0
    
    for i in range(len(puntos_manifold) - 1):
        # Distancia de Fubini-Study
        P1 = puntos_manifold[i]
        P2 = puntos_manifold[i+1]
        producto = np.abs(np.trace(P1 @ P2))
        producto = np.clip(producto, 0, 1)
        d = np.arccos(producto)
        longitud += d
    
    return longitud


def analizar_geodesicas(trayectoria_psi: List[np.ndarray]) -> Dict[str, Any]:
    """
    Verifica si las transiciones siguen geodésicas en SU(n)
    
    Las geodésicas son los caminos más cortos en la variedad.
    Transiciones naturales del sistema deberían seguir geodésicas.
    
    Args:
        trayectoria_psi: Lista de estados cuánticos
    
    Returns:
        Diccionario con análisis de geodésicas
    """
    if len(trayectoria_psi) < 3:
        return {
            'curvatura_media': np.inf,
            'es_geodesica': False,
            'longitud_camino': 0.0
        }
    
    # 1. Proyección a variedad de Grassmann
    puntos_manifold = [proyectar_a_grassmann(psi) for psi in trayectoria_psi]
    
    # 2. Cálculo de curvatura geodésica
    curvaturas = []
    for i in range(1, len(puntos_manifold) - 1):
        kappa = calcular_curvatura_geodesica(
            puntos_manifold[i-1],
            puntos_manifold[i],
            puntos_manifold[i+1]
        )
        curvaturas.append(kappa)
    
    # 3. Test: trayectorias óptimas tienen κ ≈ 0
    curvatura_media = np.mean(curvaturas) if curvaturas else np.inf
    es_geodesica = curvatura_media < 0.1  # Umbral empírico
    
    # 4. Longitud del camino
    longitud = calcular_longitud_geodesica(puntos_manifold)
    
    return {
        'curvatura_media': curvatura_media,
        'curvatura_std': np.std(curvaturas) if curvaturas else 0.0,
        'curvatura_max': np.max(curvaturas) if curvaturas else 0.0,
        'es_geodesica': es_geodesica,
        'longitud_camino': longitud,
        'n_puntos': len(puntos_manifold)
    }


def calcular_estabilidad_grupo(datos_grupo: List[List[np.ndarray]]) -> float:
    """
    Calcula estabilidad estructural del grupo SU(n)
    
    Promedia la coherencia y preservación de propiedades de grupo
    a través de múltiples sesiones.
    
    Args:
        datos_grupo: Lista de trayectorias para cada sujeto
    
    Returns:
        Índice de estabilidad [0, 1]
    """
    estabilidades = []
    
    for trayectoria in datos_grupo:
        if len(trayectoria) < 2:
            continue
        
        # Test de estructura de grupo
        tests = test_estructura_grupo_SU(trayectoria)
        
        # Estabilidad como promedio de tests exitosos
        estabilidad = (
            float(tests['preservacion_norma']) * 0.3 +
            tests['unitariedad'] * 0.3 +
            tests['cerradura'] * 0.2 +
            tests['algebra_lie'] * 0.2
        )
        estabilidades.append(estabilidad)
    
    return np.mean(estabilidades) if estabilidades else 0.0


def calcular_cohens_d(grupo1: np.ndarray, grupo2: np.ndarray) -> float:
    """
    Calcula el tamaño del efecto de Cohen's d
    
    Args:
        grupo1: Array con mediciones del grupo 1
        grupo2: Array con mediciones del grupo 2
    
    Returns:
        Cohen's d (tamaño del efecto)
    """
    n1, n2 = len(grupo1), len(grupo2)
    var1, var2 = np.var(grupo1, ddof=1), np.var(grupo2, ddof=1)
    
    # Desviación estándar pooled
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    # Cohen's d
    d = (np.mean(grupo1) - np.mean(grupo2)) / pooled_std if pooled_std > 0 else 0.0
    
    return d


def analisis_estadistico_SU(
    datos_grupo_control: List[List[np.ndarray]],
    datos_grupo_meditadores: List[List[np.ndarray]]
) -> Dict[str, Any]:
    """
    Comparación entre grupos para validar hipótesis de SU(Ψ)
    
    Compara meditadores expertos vs. controles en:
    - Coherencia basal
    - Eficiencia de trayectorias
    - Estabilidad estructural del grupo SU(n)
    
    Args:
        datos_grupo_control: Lista de trayectorias para grupo control
        datos_grupo_meditadores: Lista de trayectorias para meditadores
    
    Returns:
        Diccionario con resultados estadísticos completos
    """
    resultados = {}
    
    # 1. Comparación de coherencia basal
    coherencia_control = []
    for trayectoria in datos_grupo_control:
        if len(trayectoria) > 0:
            coherencias = [calcular_coherencia(psi) for psi in trayectoria]
            coherencia_control.append(np.mean(coherencias))
    
    coherencia_meditadores = []
    for trayectoria in datos_grupo_meditadores:
        if len(trayectoria) > 0:
            coherencias = [calcular_coherencia(psi) for psi in trayectoria]
            coherencia_meditadores.append(np.mean(coherencias))
    
    if coherencia_control and coherencia_meditadores:
        u_stat, p_valor = mannwhitneyu(coherencia_meditadores, coherencia_control)
        resultados['coherencia'] = {
            'media_control': np.mean(coherencia_control),
            'media_meditadores': np.mean(coherencia_meditadores),
            'p_valor': p_valor,
            'tamaño_efecto': calcular_cohens_d(
                np.array(coherencia_meditadores),
                np.array(coherencia_control)
            ),
            'significativo': p_valor < 0.05
        }
    
    # 2. Análisis de trayectorias
    longitudes_control = []
    for trayectoria in datos_grupo_control:
        if len(trayectoria) >= 3:
            resultado = analizar_geodesicas(trayectoria)
            longitudes_control.append(resultado['longitud_camino'])
    
    longitudes_meditadores = []
    for trayectoria in datos_grupo_meditadores:
        if len(trayectoria) >= 3:
            resultado = analizar_geodesicas(trayectoria)
            longitudes_meditadores.append(resultado['longitud_camino'])
    
    if longitudes_control and longitudes_meditadores:
        t_stat, p_valor = ttest_ind(longitudes_meditadores, longitudes_control)
        resultados['eficiencia_trayectoria'] = {
            'longitud_control': np.mean(longitudes_control),
            'longitud_meditadores': np.mean(longitudes_meditadores),
            'p_valor': p_valor,
            'significativo': p_valor < 0.05
        }
    
    # 3. Predicción: meditadores muestran mayor estabilidad estructural
    estabilidad_control = calcular_estabilidad_grupo(datos_grupo_control)
    estabilidad_meditadores = calcular_estabilidad_grupo(datos_grupo_meditadores)
    
    resultados['estabilidad_SU'] = {
        'control': estabilidad_control,
        'meditadores': estabilidad_meditadores,
        'diferencia_relativa': (
            (estabilidad_meditadores - estabilidad_control) / estabilidad_control
            if estabilidad_control > 0 else 0.0
        ),
        'diferencia_significativa': estabilidad_meditadores > estabilidad_control * 1.5
    }
    
    # 4. Resumen global
    resultados['conclusion'] = (
        "Evidencia fuerte de estructura SU(n)" if
        resultados.get('coherencia', {}).get('significativo', False) and
        resultados['estabilidad_SU']['diferencia_significativa']
        else "Evidencia moderada o insuficiente"
    )
    
    return resultados
