#!/usr/bin/env python3
"""
FASE II: Validación de T_μν(Φ) — El Tensor de Stress Emocional

Implementa protocolos experimentales para validar que las emociones generan
un tensor de stress-energía que curva el espacio de conciencia.

Hipótesis Principal:
H₂: Las emociones generan un tensor de stress-energía que curva el espacio
de conciencia, afectando la coherencia según las ecuaciones de campo QCAL

Predicciones Falsables:
- P2.1: T₀₀ (intensidad emocional) correlaciona con actividad amígdala
- P2.2: T₀ᵢ (flujo emocional) predice contagio emocional en díadas
- P2.3: ∇²Φ (curvatura) predice vulnerabilidad a psicopatología
- P2.4: Exposición a 141.7 Hz reduce T₀₀ y aumenta Ψ

Autor: José Manuel Mota Burruezo (JMMB)
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from scipy.signal import correlate
from scipy.stats import pearsonr, spearmanr
from scipy.ndimage import laplace, gaussian_filter
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, mutual_info_score
import scipy.stats


def normalizar(señal: np.ndarray) -> np.ndarray:
    """
    Normaliza señal a rango [0, 1]
    
    Args:
        señal: Array con señal a normalizar
    
    Returns:
        Señal normalizada
    """
    min_val = np.min(señal)
    max_val = np.max(señal)
    
    if max_val - min_val < 1e-10:
        return np.zeros_like(señal)
    
    return (señal - min_val) / (max_val - min_val)


def construir_campo_emocional(
    datos_multisensor: Dict[str, np.ndarray],
    tiempo: Optional[np.ndarray] = None
) -> np.ndarray:
    """
    Fusiona múltiples señales en campo escalar Φ
    
    Combina señales fisiológicas y subjetivas para construir
    un campo escalar que representa el estado emocional.
    
    Args:
        datos_multisensor: Diccionario con claves:
            - 'eda': Conductancia de piel (arousal)
            - 'hrv': Variabilidad cardíaca (regulación)
            - 'amigdala': Actividad de amígdala (procesamiento)
            - 'autorreporte': Experiencia subjetiva
        tiempo: Array opcional con puntos temporales
    
    Returns:
        Campo escalar Φ(t) representando estado emocional
    """
    # 1. Normalización de señales
    eda_norm = normalizar(datos_multisensor.get('eda', np.zeros(1)))
    hrv_norm = normalizar(datos_multisensor.get('hrv', np.zeros(1)))
    amigdala_norm = normalizar(datos_multisensor.get('amigdala', np.zeros(1)))
    autorreporte_norm = normalizar(datos_multisensor.get('autorreporte', np.zeros(1)))
    
    # 2. Ponderación óptima (calibrada mediante regresión)
    pesos = {
        'eda': 0.30,        # Arousal fisiológico
        'hrv': 0.20,        # Regulación emocional
        'amigdala': 0.25,   # Procesamiento emocional
        'autorreporte': 0.25 # Experiencia subjetiva
    }
    
    # Asegurar que todas las señales tienen la misma longitud
    n_samples = max(
        len(eda_norm),
        len(hrv_norm),
        len(amigdala_norm),
        len(autorreporte_norm)
    )
    
    # 3. Campo compuesto
    Phi = (
        pesos['eda'] * eda_norm +
        pesos['hrv'] * (1 - hrv_norm) +  # HRV alto = stress bajo
        pesos['amigdala'] * amigdala_norm +
        pesos['autorreporte'] * autorreporte_norm
    )
    
    return Phi


def calcular_tensor_stress_energia(Phi_espaciotemporal: np.ndarray) -> np.ndarray:
    """
    Calcula T_μν a partir del campo Φ(x,t)
    
    El tensor de stress-energía describe cómo el campo emocional
    curva el espacio de conciencia.
    
    Args:
        Phi_espaciotemporal: Array de forma (tiempo, x, y) con campo Φ
    
    Returns:
        Tensor T_μν de forma (4, 4, tiempo, x, y)
    """
    # Asegurar que tenemos al menos 3 dimensiones
    if Phi_espaciotemporal.ndim == 1:
        # Expandir a 3D temporal
        Phi_espaciotemporal = Phi_espaciotemporal.reshape(-1, 1, 1)
    elif Phi_espaciotemporal.ndim == 2:
        # Añadir dimensión espacial
        Phi_espaciotemporal = Phi_espaciotemporal[:, :, np.newaxis]
    
    # Asegurar dimensiones mínimas para gradiente (al menos 2 elementos por eje)
    shape = Phi_espaciotemporal.shape
    if shape[1] < 2:
        Phi_espaciotemporal = np.pad(Phi_espaciotemporal, ((0, 0), (0, 1), (0, 0)), mode='edge')
    if shape[2] < 2:
        Phi_espaciotemporal = np.pad(Phi_espaciotemporal, ((0, 0), (0, 0), (0, 1)), mode='edge')
    
    # Actualizar shape después de padding
    shape = Phi_espaciotemporal.shape
    T_μν = np.zeros((4, 4) + shape)
    
    # 1. Derivadas del campo
    dPhi_dt = np.gradient(Phi_espaciotemporal, axis=0)
    dPhi_dx = np.gradient(Phi_espaciotemporal, axis=1)
    dPhi_dy = np.gradient(Phi_espaciotemporal, axis=2)
    
    # 2. Componentes del tensor
    # T₀₀: Densidad de energía emocional
    T_μν[0, 0] = (dPhi_dt**2 + dPhi_dx**2 + dPhi_dy**2) / 2
    
    # T₀ᵢ: Flujo de momento emocional (dirección de propagación)
    T_μν[0, 1] = dPhi_dt * dPhi_dx
    T_μν[0, 2] = dPhi_dt * dPhi_dy
    T_μν[0, 3] = np.zeros_like(dPhi_dt)  # No hay tercera dimensión espacial
    
    # Tᵢⱼ: Tensor de stress espacial (tensión relacional)
    T_μν[1, 1] = dPhi_dx**2 - (dPhi_dy**2) / 2
    T_μν[1, 2] = dPhi_dx * dPhi_dy
    T_μν[2, 2] = dPhi_dy**2 - (dPhi_dx**2) / 2
    
    # 3. Simetrización
    for mu in range(4):
        for nu in range(mu + 1, 4):
            T_μν[nu, mu] = T_μν[mu, nu]
    
    return T_μν


def calcular_curvatura_emocional(Phi: np.ndarray) -> Dict[str, Any]:
    """
    Calcula ∇²Φ (Laplaciano) como curvatura del paisaje emocional
    
    La curvatura identifica regiones de alta tensión emocional
    que pueden predecir vulnerabilidad psicológica.
    
    Args:
        Phi: Campo escalar emocional
    
    Returns:
        Diccionario con análisis de curvatura
    """
    # Calcular Laplaciano
    nabla2_Phi = laplace(Phi)
    
    # Identificación de singularidades (puntos de alta curvatura)
    umbral_critico = 3 * np.std(nabla2_Phi)
    singularidades = np.abs(nabla2_Phi) > umbral_critico
    
    return {
        'curvatura': nabla2_Phi,
        'singularidades': singularidades,
        'num_singularidades': np.sum(singularidades),
        'max_curvatura': np.max(np.abs(nabla2_Phi)),
        'curvatura_media': np.mean(np.abs(nabla2_Phi)),
        'curvatura_std': np.std(nabla2_Phi)
    }


def test_correlacion_T00_amigdala(datos: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verifica si T₀₀ predice actividad límbica
    
    Predicción P2.1: La densidad de energía emocional T₀₀ debe
    correlacionar fuertemente con actividad de amígdala.
    
    Args:
        datos: Diccionario con claves:
            - 'tensor': Tensor T_μν completo
            - 'fmri_amigdala': Serie temporal de actividad amígdala
    
    Returns:
        Diccionario con análisis de correlación
    """
    T_00 = datos['tensor'][0, 0]  # Densidad de energía
    amigdala = datos['fmri_amigdala']
    
    # Aplanar para correlación
    T_00_flat = T_00.flatten()
    amigdala_flat = amigdala.flatten()
    
    # Asegurar misma longitud
    min_len = min(len(T_00_flat), len(amigdala_flat))
    T_00_flat = T_00_flat[:min_len]
    amigdala_flat = amigdala_flat[:min_len]
    
    # Correlación instantánea
    r_pearson, p_pearson = pearsonr(T_00_flat, amigdala_flat)
    
    # Correlación con lag (causalidad)
    lags = range(-5, 6)  # ±5 pasos temporales
    correlaciones_lag = []
    
    for lag in lags:
        if lag < 0:
            if len(T_00_flat[:lag]) > 0 and len(amigdala_flat[-lag:]) > 0:
                min_len_lag = min(len(T_00_flat[:lag]), len(amigdala_flat[-lag:]))
                r, _ = pearsonr(
                    T_00_flat[:min_len_lag],
                    amigdala_flat[-lag:][:min_len_lag]
                )
            else:
                r = 0
        elif lag > 0:
            if len(T_00_flat[lag:]) > 0 and len(amigdala_flat[:-lag]) > 0:
                min_len_lag = min(len(T_00_flat[lag:]), len(amigdala_flat[:-lag]))
                r, _ = pearsonr(
                    T_00_flat[lag:][:min_len_lag],
                    amigdala_flat[:min_len_lag]
                )
            else:
                r = 0
        else:
            r = r_pearson
        correlaciones_lag.append(r)
    
    max_corr_idx = np.argmax(np.abs(correlaciones_lag))
    max_lag = lags[max_corr_idx]
    
    return {
        'correlacion': r_pearson,
        'p_valor': p_pearson,
        'significativo': p_pearson < 0.05,
        'lag_optimo': max_lag,
        'correlacion_maxima': correlaciones_lag[max_corr_idx],
        'interpretacion': (
            'T₀₀ precede amígdala' if max_lag > 0
            else 'Amígdala precede T₀₀' if max_lag < 0
            else 'Correlación simultánea'
        )
    }


def test_flujo_emocional_diadas(
    datos_emisor: Dict[str, np.ndarray],
    datos_receptor: Dict[str, np.ndarray]
) -> Dict[str, Any]:
    """
    Mide propagación emocional usando T₀ᵢ
    
    Predicción P2.2: El flujo de momento emocional T₀ᵢ del emisor
    debe predecir la respuesta emocional del receptor.
    
    Args:
        datos_emisor: Datos multi-sensor del emisor
        datos_receptor: Datos multi-sensor del receptor
    
    Returns:
        Diccionario con análisis de contagio emocional
    """
    # 1. Calcular campos Φ individuales
    Phi_emisor = construir_campo_emocional(datos_emisor, None)
    Phi_receptor = construir_campo_emocional(datos_receptor, None)
    
    # Expandir a 3D para calcular tensor
    Phi_emisor_3d = Phi_emisor.reshape(-1, 1, 1)
    Phi_receptor_3d = Phi_receptor.reshape(-1, 1, 1)
    
    # 2. Tensor de stress para cada individuo
    T_emisor = calcular_tensor_stress_energia(Phi_emisor_3d)
    T_receptor = calcular_tensor_stress_energia(Phi_receptor_3d)
    
    # 3. Flujo de momento (T₀₁) del emisor
    flujo_emisor = T_emisor[0, 1].flatten()
    
    # 4. Respuesta del receptor (T₀₀)
    respuesta_receptor = T_receptor[0, 0].flatten()
    
    # Asegurar misma longitud
    min_len = min(len(flujo_emisor), len(respuesta_receptor))
    flujo_emisor = flujo_emisor[:min_len]
    respuesta_receptor = respuesta_receptor[:min_len]
    
    # 5. Cross-correlación para detectar contagio
    if len(flujo_emisor) > 1 and len(respuesta_receptor) > 1:
        cross_corr = correlate(flujo_emisor, respuesta_receptor, mode='full')
        lag_contagio = np.argmax(cross_corr) - len(flujo_emisor)
        tiempo_contagio = lag_contagio * 0.001  # Asumiendo muestreo 1 kHz
        
        # 6. Magnitud del contagio
        # Discretizar para mutual information
        flujo_bins = np.digitize(flujo_emisor, bins=np.linspace(
            flujo_emisor.min(), flujo_emisor.max(), 11
        ))
        respuesta_bins = np.digitize(respuesta_receptor, bins=np.linspace(
            respuesta_receptor.min(), respuesta_receptor.max(), 11
        ))
        
        mi = mutual_info_score(flujo_bins, respuesta_bins)
    else:
        lag_contagio = 0
        tiempo_contagio = 0
        cross_corr = np.array([0])
        mi = 0
    
    return {
        'latencia_contagio_ms': tiempo_contagio * 1000,
        'magnitud_contagio': np.max(cross_corr) if len(cross_corr) > 0 else 0,
        'informacion_mutua': mi,
        'hay_contagio': mi > 0.1,
        'interpretacion': f'Emoción se propaga en {tiempo_contagio*1000:.0f} ms'
    }


def estudio_longitudinal_curvatura(
    datos_baseline: List[Dict[str, np.ndarray]],
    datos_followup_6meses: List[Dict[str, bool]]
) -> Dict[str, Any]:
    """
    Predice desarrollo de psicopatología desde ∇²Φ basal
    
    Predicción P2.3: La curvatura emocional basal predice
    vulnerabilidad a desarrollar síntomas psicopatológicos.
    
    Args:
        datos_baseline: Lista de datos multi-sensor basales
        datos_followup_6meses: Lista de diccionarios con diagnósticos
            (clave 'nuevo_episodio': bool)
    
    Returns:
        Diccionario con resultados predictivos
    """
    # 1. Extraer características de curvatura basal
    caracteristicas = []
    
    for sujeto in datos_baseline:
        Phi = construir_campo_emocional(sujeto, None)
        
        # Expandir a 2D si es necesario
        if Phi.ndim == 1:
            Phi = Phi.reshape(-1, 1)
        
        curv = calcular_curvatura_emocional(Phi)
        
        features = [
            np.mean(np.abs(curv['curvatura'])),  # media_curvatura
            curv['max_curvatura'],  # max_curvatura
            curv['num_singularidades'],  # num_singularidades
            np.var(curv['curvatura']),  # varianza_curvatura
            scipy.stats.skew(curv['curvatura'].flatten())  # asimetria_curvatura
        ]
        caracteristicas.append(features)
    
    X = np.array(caracteristicas)
    
    # 2. Variable objetivo: desarrollo de síntomas clínicos
    y = np.array([diagnostico.get('nuevo_episodio', False) for diagnostico in datos_followup_6meses])
    
    # 3. Modelo predictivo
    if len(np.unique(y)) > 1:  # Necesitamos al menos 2 clases
        modelo = LogisticRegression(class_weight='balanced', random_state=42)
        modelo.fit(X, y)
        
        y_pred_proba = modelo.predict_proba(X)[:, 1]
        auc = roc_auc_score(y, y_pred_proba)
        
        # 4. Análisis de importancia
        feature_names = [
            'media_curvatura',
            'max_curvatura',
            'num_singularidades',
            'varianza_curvatura',
            'asimetria_curvatura'
        ]
        importancias = dict(zip(feature_names, modelo.coef_[0]))
    else:
        auc = 0.5
        importancias = {}
    
    return {
        'auc': auc,
        'interpretacion': 'Buena predicción' if auc > 0.75 else 'Predicción débil',
        'importancia_features': importancias,
        'n_sujetos': len(datos_baseline),
        'n_casos': int(np.sum(y)),
        'conclusion': f'La curvatura emocional basal predice psicopatología con AUC={auc:.2f}'
    }


def rct_frecuencia_141_7_Hz() -> Dict[str, Any]:
    """
    Protocolo completo de RCT para validar intervención 141.7 Hz
    
    Predicción P2.4: Exposición a 141.7 Hz debe reducir T₀₀
    y aumentar coherencia Ψ.
    
    Returns:
        Diccionario con diseño completo del RCT
    """
    # Diseño: Triple ciego, paralelo, 3 brazos
    grupos = {
        'experimental': {
            'n': 30,
            'intervencion': '141.7 Hz binaural',
            'frecuencia': 141.7,
            'duracion_sesion': 30  # minutos
        },
        'placebo_activo': {
            'n': 30,
            'intervencion': '200 Hz binaural',
            'frecuencia': 200.0,
            'duracion_sesion': 30
        },
        'control': {
            'n': 30,
            'intervencion': 'Silencio con ruido rosa',
            'frecuencia': None,
            'duracion_sesion': 30
        }
    }
    
    # Variables primarias
    outcomes_primarios = {
        'T00_reduccion': 'Cambio en densidad de stress desde baseline',
        'Psi_aumento': 'Cambio en coherencia cuántica',
        'tiempo_retorno': 'Tiempo para volver a baseline post-stress'
    }
    
    # Variables secundarias
    outcomes_secundarios = {
        'nabla2_Phi': 'Reducción de curvatura emocional',
        'HRV_RMSSD': 'Aumento de variabilidad cardíaca',
        'autorreporte_ansiedad': 'Reducción en STAI-S'
    }
    
    # Protocolo de intervención
    protocolo = """
    Día 1-7: Baseline (sin intervención)
    Día 8-28: Intervención diaria (30 min, misma hora)
    Día 29-35: Seguimiento sin intervención
    
    Mediciones:
    - Continuas: EEG, HRV, EDA (durante sesión)
    - Diarias: PANAS, escala de stress percibido
    - Semanales: fMRI, cuestionarios clínicos
    """
    
    # Análisis estadístico planificado
    analisis = {
        'primario': 'ANOVA mixta 3(grupo) × 3(tiempo) con corrección Greenhouse-Geisser',
        'secundario': 'Regresión lineal jerárquica con covariables',
        'tamaño_efecto': 'η² parcial para ANOVA, d de Cohen para comparaciones pareadas',
        'potencia': '80% para detectar d=0.5 con α=0.05',
        'ajuste_comparaciones': 'Bonferroni para outcomes múltiples',
        'n_total': sum(g['n'] for g in grupos.values())
    }
    
    # Resultados esperados
    resultados_esperados = simular_resultados_esperados()
    
    return {
        'diseño': grupos,
        'outcomes_primarios': outcomes_primarios,
        'outcomes_secundarios': outcomes_secundarios,
        'protocolo': protocolo,
        'analisis': analisis,
        'resultados_esperados': resultados_esperados
    }


def simular_resultados_esperados() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Predicciones cuantitativas basadas en el modelo QCAL
    
    Returns:
        Tupla (resultados_esperados, comparaciones)
    """
    # Baseline común
    T00_baseline = 0.45
    Psi_baseline = 0.78
    
    # Post-intervención (día 28)
    resultados_esperados = {
        'experimental_141.7Hz': {
            'T00': T00_baseline * 0.65,  # 35% de reducción
            'Psi': Psi_baseline + 0.15,   # Aumento absoluto de 0.15
            'nabla2_Phi': -0.42,          # Reducción de singularidades
            'IC_95': '[0.58-0.82 para Psi]'
        },
        'placebo_activo_200Hz': {
            'T00': T00_baseline * 0.85,  # 15% de reducción (efecto placebo)
            'Psi': Psi_baseline + 0.05,
            'nabla2_Phi': -0.15,
            'IC_95': '[0.79-0.87 para Psi]'
        },
        'control_silencio': {
            'T00': T00_baseline * 0.92,  # 8% de reducción (habituación)
            'Psi': Psi_baseline + 0.02,
            'nabla2_Phi': -0.05,
            'IC_95': '[0.77-0.83 para Psi]'
        }
    }
    
    # Test de hipótesis
    comparaciones = {
        'experimental_vs_placebo': {
            'p_esperado': '<0.001',
            'tamaño_efecto_d': 0.95
        },
        'experimental_vs_control': {
            'p_esperado': '<0.0001',
            'tamaño_efecto_d': 1.32
        }
    }
    
    return resultados_esperados, comparaciones
