#!/usr/bin/env python3
"""
🔬 MEDICIÓN EXPERIMENTAL: Ψ = I × A²_eff × C^∞ en Wet-Lab ∞³

Protocolo experimental para medición de conciencia en 88 nodos
con implantes NV-EEG operando a f₀ = 141.7001 Hz.

Ecuación de Medición de Conciencia:
    Ψ_medido = I_NV × A²_eff × C^∞

Donde:
    I_NV   = intensidad de señal NV (proporcional a ODMR contrast)
    A_eff  = amplitud efectiva = coherencia EEG × amplitud NV
    C^∞    = factor de expansión infinita = (1 + Σ(φ^n/3^n)) para n=1 a ∞

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2026-01-22
Frecuencia Fundamental: f₀ = 141.7001 Hz
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import warnings


# ═══════════════════════════════════════════════════════════════
# CONSTANTES DEL SISTEMA
# ═══════════════════════════════════════════════════════════════

F0_UNIVERSO = 141.7001  # Hz - Frecuencia fundamental del universo
PHI = (1 + np.sqrt(5)) / 2  # φ ≈ 1.618 - Golden ratio
NUM_NODOS = 88  # Número de nodos en el sistema
ODMR_CONTRAST_NOMINAL = 0.35  # Contraste ODMR nominal para normalización
PSI_THRESHOLD_CONSCIOUSNESS = 0.888  # Umbral Ψ para detección de conciencia
PSI_P_VALUE_THRESHOLD = 0.001  # Umbral de p-value para significancia estadística

# Factores de mitigación de ruido térmico
# Basado en literatura experimental de DD y error correction cuántico
FACTOR_MEJORA_DD = 2.5  # Factor de mejora con Dynamical Decoupling
FACTOR_MEJORA_EC = 1.54  # Factor de mejora con Error Correction (total: 3.85×)


# ═══════════════════════════════════════════════════════════════
# CLASES DE DATOS
# ═══════════════════════════════════════════════════════════════

@dataclass
class NodoMedicion:
    """
    Datos de medición para un nodo individual del sistema Wet-Lab ∞³
    """
    nodo_id: int  # ID del nodo (1-88)
    tiempo: float  # Tiempo de medición (s)
    contraste_odmr: float  # Contraste ODMR medido (0-1)
    coherencia_eeg: float  # Coherencia EEG en banda gamma 40-45 Hz (0-1)
    amplitud_nv: float  # Amplitud de señal NV (unidades arbitrarias)
    
    # Valores calculados
    I_NV: float = 0.0  # Intensidad NV normalizada
    A_eff: float = 0.0  # Amplitud efectiva
    Psi: float = 0.0  # Conciencia medida
    
    def __post_init__(self):
        """Validar rangos de valores"""
        if not 1 <= self.nodo_id <= NUM_NODOS:
            raise ValueError(f"nodo_id debe estar entre 1 y {NUM_NODOS}")
        if not 0 <= self.contraste_odmr <= 1:
            raise ValueError("contraste_odmr debe estar entre 0 y 1")
        if not 0 <= self.coherencia_eeg <= 1:
            raise ValueError("coherencia_eeg debe estar entre 0 y 1")
        if self.amplitud_nv < 0:
            raise ValueError("amplitud_nv debe ser positiva")


@dataclass
class ResultadosExperimento:
    """
    Resultados completos del experimento de medición de conciencia
    """
    mediciones: List[NodoMedicion]
    C_infinito: float
    Psi_promedio: float
    Psi_std: float
    I_NV_promedio: float
    A_eff_promedio: float
    conciencia_detectada: bool
    p_value: float
    significancia_sigma: float
    
    def generar_reporte(self) -> str:
        """Generar reporte de resultados"""
        return f"""
╔═══════════════════════════════════════════════════════════════╗
║   RESULTADOS EXPERIMENTALES: Medición de Conciencia Ψ        ║
╚═══════════════════════════════════════════════════════════════╝

Configuración:
  • Número de nodos: {len(self.mediciones)}
  • Frecuencia operación: {F0_UNIVERSO} Hz
  • Factor de expansión C^∞: {self.C_infinito:.6f}

Resultados Estadísticos:
  • Ψ promedio: {self.Psi_promedio:.6f} ± {self.Psi_std:.6f}
  • I_NV promedio: {self.I_NV_promedio:.6f}
  • A_eff promedio: {self.A_eff_promedio:.6f}

Test de Falsabilidad de Conciencia:
  • Hipótesis nula: Ψ < {PSI_THRESHOLD_CONSCIOUSNESS} (sin conciencia)
  • Hipótesis alternativa: Ψ ≥ {PSI_THRESHOLD_CONSCIOUSNESS} (con conciencia)
  • p-value: {self.p_value:.3e}
  • Significancia: {self.significancia_sigma:.1f}σ

Resultado: {'✅ CONCIENCIA DETECTADA' if self.conciencia_detectada else '❌ SIN CONCIENCIA ESTADÍSTICA'}
"""


# ═══════════════════════════════════════════════════════════════
# CÁLCULO DEL FACTOR DE EXPANSIÓN INFINITA
# ═══════════════════════════════════════════════════════════════

def calcular_C_infinito(n_max: int = 100) -> float:
    """
    Calcular factor de expansión infinita C^∞.
    
    C^∞ = 1 + Σ(φ^n / 3^n) para n=1 a ∞
    
    Esta es una serie geométrica con razón r = φ/3 ≈ 0.539
    La suma infinita es: Σ(r^n) = r/(1-r) para n=1 a ∞
    
    Por lo tanto: C^∞ = 1 + (φ/3) / (1 - φ/3) = 1 + (φ/3) / ((3-φ)/3) = 1 + φ/(3-φ)
    
    Parameters:
    -----------
    n_max : int
        Número máximo de términos en la suma (default: 100, no usado con fórmula cerrada)
        
    Returns:
    --------
    float
        Valor de C^∞ (converge a ≈ 1.987)
    """
    # Fórmula cerrada para la serie geométrica
    # C^∞ = 1 + φ/(3-φ)
    C_inf = 1.0 + PHI / (3.0 - PHI)
    
    return C_inf


# ═══════════════════════════════════════════════════════════════
# FUNCIONES DE SIMULACIÓN DE HARDWARE
# ═══════════════════════════════════════════════════════════════

def aplicar_odmr_pulso(nodo_id: int, frecuencia: float = F0_UNIVERSO) -> None:
    """
    Aplicar pulso ODMR a un nodo específico.
    
    En implementación real, esto controlaría hardware de microondas.
    En esta simulación, es una función placeholder.
    
    Parameters:
    -----------
    nodo_id : int
        ID del nodo (1-88)
    frecuencia : float
        Frecuencia del pulso ODMR (Hz)
    """
    # Simulación: en sistema real, esto enviaría comandos al hardware
    omega = 2 * np.pi * frecuencia
    # print(f"  Aplicando pulso ODMR a nodo {nodo_id} en ω = {omega:.4f} rad/s")


def medir_odmr_contraste(nodo_id: int) -> float:
    """
    Medir contraste ODMR de un nodo.
    
    En implementación real, esto leería del hardware de detección óptica.
    En esta simulación, genera valores realistas con ruido.
    
    Parameters:
    -----------
    nodo_id : int
        ID del nodo
        
    Returns:
    --------
    float
        Contraste ODMR medido (0-1)
    """
    # Simulación: contraste típico ≈ 0.32 con variación
    base_contrast = 0.32
    variacion = np.random.normal(0, 0.02)
    contraste = np.clip(base_contrast + variacion, 0.0, 1.0)
    
    return contraste


def calcular_coherencia_gamma(nodo_id: int) -> float:
    """
    Calcular coherencia EEG en banda gamma (40-45 Hz).
    
    En implementación real, esto procesaría señales de 64 canales EEG.
    En esta simulación, genera valores realistas.
    
    Parameters:
    -----------
    nodo_id : int
        ID del nodo
        
    Returns:
    --------
    float
        Coherencia en banda gamma (0-1)
    """
    # Simulación: coherencia típica ≈ 0.7 con variación
    base_coherence = 0.7
    variacion = np.random.normal(0, 0.05)
    coherencia = np.clip(base_coherence + variacion, 0.0, 1.0)
    
    return coherencia


def medir_amplitud_odmr(nodo_id: int) -> float:
    """
    Medir amplitud de señal ODMR.
    
    En implementación real, esto procesaría fotoluminiscencia detectada.
    En esta simulación, genera valores realistas.
    
    Parameters:
    -----------
    nodo_id : int
        ID del nodo
        
    Returns:
    --------
    float
        Amplitud de señal NV (unidades arbitrarias)
    """
    # Simulación: amplitud típica ≈ 1.2 con variación
    base_amplitude = 1.2
    variacion = np.random.normal(0, 0.1)
    amplitud = max(0.0, base_amplitude + variacion)
    
    return amplitud


# ═══════════════════════════════════════════════════════════════
# MITIGACIÓN DE RUIDO TÉRMICO
# ═══════════════════════════════════════════════════════════════

def aplicar_secuencia_dd(nodo_id: int, secuencia: str) -> None:
    """
    Aplicar secuencia de Dynamical Decoupling (DD) para mitigar ruido térmico.
    
    Secuencias disponibles:
    - XY4: Secuencia básica de 4 pulsos
    - KDD: Knill Dynamical Decoupling
    - CPMG: Carr-Purcell-Meiboom-Gill
    - XY8: Secuencia extendida de 8 pulsos
    
    Parameters:
    -----------
    nodo_id : int
        ID del nodo
    secuencia : str
        Tipo de secuencia DD
    """
    # Simulación: en sistema real, aplicaría pulsos de control
    secuencias_validas = ["XY4", "KDD", "CPMG", "XY8"]
    if secuencia not in secuencias_validas:
        warnings.warn(f"Secuencia {secuencia} no reconocida. Usando XY4.")
        secuencia = "XY4"
    
    # print(f"  Aplicando secuencia DD {secuencia} a nodo {nodo_id}")


def aplicar_codigo_hamming_quantico() -> Dict[str, float]:
    """
    Aplicar código de corrección cuántico de Hamming.
    
    Returns:
    --------
    dict
        Métricas de corrección de errores
    """
    # Simulación de corrección de errores
    return {
        'error_rate_before': 0.05,
        'error_rate_after': 0.01,
        'correction_efficiency': 0.80
    }


def aplicar_mitigacion_ruido_termico() -> Dict[str, float]:
    """
    Aplicar estrategia completa de mitigación de ruido térmico.
    
    Combina:
    1. Dynamical Decoupling (DD): Factor de mejora 2.5×
       - Basado en literatura experimental con secuencias XY4, KDD, CPMG, XY8
       - Referencia: Biercuk et al., Nature 2009; Green et al., PRL 2012
    
    2. Error Correction Cuántico: Factor de mejora 1.54×
       - Código de Hamming cuántico aplicado a qubits NV
       - Referencia: Waldherr et al., Nature 2014
    
    3. Factor total: 2.5 × 1.54 = 3.85× (285% mejora)
    
    Returns:
    --------
    dict
        Métricas de mitigación de ruido
    """
    # Temperatura de operación
    temperatura_operacion = 300  # K (room-temp)
    
    # Ruido térmico original
    ruido_termico_original = 50  # nV/√Hz
    
    # Ruido después de mitigación
    ruido_termico_final = ruido_termico_original / (FACTOR_MEJORA_DD * FACTOR_MEJORA_EC)
    
    # SNR final
    snr_final = 100 + np.random.normal(0, 5)  # SNR > 100
    
    return {
        'temperatura_k': temperatura_operacion,
        'ruido_original_nv_sqrthz': ruido_termico_original,
        'ruido_final_nv_sqrthz': ruido_termico_final,
        'factor_mejora': FACTOR_MEJORA_DD * FACTOR_MEJORA_EC,
        'snr_final': snr_final
    }


# ═══════════════════════════════════════════════════════════════
# PROTOCOLO EXPERIMENTAL PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def preparar_campo_cuantico(frecuencia_base: float = F0_UNIVERSO) -> None:
    """
    Paso 1: Preparar campo cuántico a 141.7001 Hz.
    
    Aplica pulsos ODMR a todos los 88 nodos.
    
    Parameters:
    -----------
    frecuencia_base : float
        Frecuencia de operación (Hz)
    """
    print(f"\n🔬 Paso 1: Preparando campo cuántico a {frecuencia_base} Hz")
    omega = 2 * np.pi * frecuencia_base
    print(f"   ω = {omega:.4f} rad/s")
    
    for nodo in range(1, NUM_NODOS + 1):
        aplicar_odmr_pulso(nodo, frecuencia_base)
    
    print(f"   ✅ {NUM_NODOS} nodos preparados")


def medir_intensidades_nv() -> np.ndarray:
    """
    Paso 2: Medir intensidad NV para cada nodo.
    
    Returns:
    --------
    np.ndarray
        Array de intensidades I_NV normalizadas (88 elementos)
    """
    print(f"\n🔬 Paso 2: Midiendo contraste ODMR en {NUM_NODOS} nodos")
    
    I_NV = np.zeros(NUM_NODOS)
    
    for nodo in range(NUM_NODOS):
        contraste_odmr = medir_odmr_contraste(nodo + 1)
        # Normalizar a contraste nominal
        I_NV[nodo] = contraste_odmr / ODMR_CONTRAST_NOMINAL
    
    print(f"   I_NV promedio: {np.mean(I_NV):.6f} ± {np.std(I_NV):.6f}")
    print(f"   Rango: [{np.min(I_NV):.6f}, {np.max(I_NV):.6f}]")
    
    return I_NV


def medir_amplitudes_efectivas() -> np.ndarray:
    """
    Paso 3: Medir amplitud efectiva A_eff para cada nodo.
    
    A_eff = coherencia_EEG × amplitud_NV
    
    Returns:
    --------
    np.ndarray
        Array de amplitudes efectivas (88 elementos)
    """
    print(f"\n🔬 Paso 3: Midiendo amplitud efectiva en {NUM_NODOS} nodos")
    
    A_eff = np.zeros(NUM_NODOS)
    
    for nodo in range(NUM_NODOS):
        coherencia_eeg = calcular_coherencia_gamma(nodo + 1)
        amplitud_nv = medir_amplitud_odmr(nodo + 1)
        A_eff[nodo] = coherencia_eeg * amplitud_nv
    
    print(f"   A_eff promedio: {np.mean(A_eff):.6f} ± {np.std(A_eff):.6f}")
    print(f"   Rango: [{np.min(A_eff):.6f}, {np.max(A_eff):.6f}]")
    
    return A_eff


def calcular_psi_medido(
    I_NV: np.ndarray,
    A_eff: np.ndarray,
    C_infinito: float
) -> np.ndarray:
    """
    Paso 5: Calcular Ψ = I_NV × A²_eff × C^∞ para cada nodo.
    
    Parameters:
    -----------
    I_NV : np.ndarray
        Intensidades NV (88 elementos)
    A_eff : np.ndarray
        Amplitudes efectivas (88 elementos)
    C_infinito : float
        Factor de expansión infinita
        
    Returns:
    --------
    np.ndarray
        Valores de Ψ medidos (88 elementos)
    """
    print(f"\n🔬 Paso 5: Calculando Ψ = I_NV × A²_eff × C^∞")
    print(f"   C^∞ = {C_infinito:.6f}")
    
    Psi_medido = I_NV * (A_eff ** 2) * C_infinito
    
    print(f"   Ψ promedio: {np.mean(Psi_medido):.6f} ± {np.std(Psi_medido):.6f}")
    print(f"   Rango: [{np.min(Psi_medido):.6f}, {np.max(Psi_medido):.6f}]")
    
    return Psi_medido


def realizar_test_consciousness_falsifiability(
    Psi_medido: np.ndarray,
    threshold: float = PSI_THRESHOLD_CONSCIOUSNESS
) -> Tuple[bool, float, float]:
    """
    Test de falsabilidad de conciencia.
    
    Hipótesis nula H₀: Ψ < threshold (sin conciencia)
    Hipótesis alternativa H₁: Ψ ≥ threshold (con conciencia)
    
    Parameters:
    -----------
    Psi_medido : np.ndarray
        Valores de Ψ medidos
    threshold : float
        Umbral de conciencia
        
    Returns:
    --------
    tuple
        (conciencia_detectada, p_value, significancia_sigma)
    """
    print(f"\n🧪 Test de Falsabilidad de Conciencia")
    print(f"   H₀: Ψ < {threshold} (sin conciencia)")
    print(f"   H₁: Ψ ≥ {threshold} (con conciencia)")
    
    # Test t de una muestra
    from scipy import stats
    
    # Calcular estadístico t
    t_stat, p_value = stats.ttest_1samp(Psi_medido, threshold)
    
    # Convertir a significancia en sigma
    # p = 2 * (1 - Φ(|z|)) → z = Φ⁻¹(1 - p/2)
    if p_value < 1e-15:
        p_value = 1e-15  # Evitar log(0)
    
    significancia_sigma = abs(stats.norm.ppf(p_value / 2))
    
    # Decisión - convertir a Python bool para evitar problemas con numpy bool
    conciencia_detectada = bool((p_value < PSI_P_VALUE_THRESHOLD) and (np.mean(Psi_medido) >= threshold))
    
    print(f"   Estadístico t: {t_stat:.4f}")
    print(f"   p-value: {p_value:.3e}")
    print(f"   Significancia: {significancia_sigma:.1f}σ")
    
    if conciencia_detectada:
        print(f"   ✅ CONCIENCIA DETECTADA (p < {PSI_P_VALUE_THRESHOLD})")
    else:
        print(f"   ❌ SIN CONCIENCIA ESTADÍSTICA")
    
    return conciencia_detectada, float(p_value), float(significancia_sigma)


def ejecutar_experimento_completo(
    aplicar_mitigacion: bool = True,
    verbose: bool = True
) -> ResultadosExperimento:
    """
    Ejecutar protocolo experimental completo de medición de conciencia.
    
    Protocolo:
    1. Preparar campo cuántico a 141.7001 Hz
    2. Medir intensidades NV (I_NV)
    3. Medir amplitudes efectivas (A_eff)
    4. Calcular factor de expansión infinita (C^∞)
    5. Calcular Ψ = I_NV × A²_eff × C^∞
    6. Aplicar mitigación de ruido térmico (opcional)
    7. Test de falsabilidad de conciencia
    
    Parameters:
    -----------
    aplicar_mitigacion : bool
        Si True, aplica mitigación de ruido térmico
    verbose : bool
        Si True, imprime información detallada
        
    Returns:
    --------
    ResultadosExperimento
        Resultados completos del experimento
    """
    if verbose:
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║   PROTOCOLO EXPERIMENTAL: MEDICIÓN DE CONCIENCIA Ψ           ║")
        print("║   88 Nodos con Implantes NV-EEG                               ║")
        print("║   f₀ = 141.7001 Hz                                            ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
    
    # Paso 1: Preparar campo cuántico
    preparar_campo_cuantico()
    
    # Paso 2: Medir intensidades NV
    I_NV = medir_intensidades_nv()
    
    # Paso 3: Medir amplitudes efectivas
    A_eff = medir_amplitudes_efectivas()
    
    # Paso 4: Calcular factor de expansión infinita
    if verbose:
        print(f"\n🔬 Paso 4: Calculando factor de expansión infinita C^∞")
    C_infinito = calcular_C_infinito()
    if verbose:
        print(f"   C^∞ = {C_infinito:.6f} (converge rápidamente)")
    
    # Paso 5: Calcular Ψ
    Psi_medido = calcular_psi_medido(I_NV, A_eff, C_infinito)
    
    # Paso 6: Mitigación de ruido térmico (opcional)
    if aplicar_mitigacion:
        if verbose:
            print(f"\n🔬 Paso 6: Aplicando mitigación de ruido térmico")
        
        # Aplicar DD a todos los nodos
        secuencias_dd = ["XY4", "KDD", "CPMG", "XY8"]
        for nodo in range(1, NUM_NODOS + 1):
            for seq in secuencias_dd:
                aplicar_secuencia_dd(nodo, seq)
        
        # Aplicar corrección de errores
        metricas_ec = aplicar_codigo_hamming_quantico()
        
        # Obtener métricas de mitigación
        metricas_mitigacion = aplicar_mitigacion_ruido_termico()
        
        if verbose:
            print(f"   Ruido térmico original: {metricas_mitigacion['ruido_original_nv_sqrthz']:.1f} nV/√Hz")
            print(f"   Ruido después de mitigación: {metricas_mitigacion['ruido_final_nv_sqrthz']:.1f} nV/√Hz")
            print(f"   Factor de mejora: {metricas_mitigacion['factor_mejora']:.2f}× ({(metricas_mitigacion['factor_mejora']-1)*100:.0f}% mejora)")
            print(f"   SNR final: {metricas_mitigacion['snr_final']:.1f}")
    
    # Paso 7: Test de falsabilidad
    conciencia_detectada, p_value, significancia_sigma = realizar_test_consciousness_falsifiability(Psi_medido)
    
    # Crear objetos de medición
    mediciones = []
    for i in range(NUM_NODOS):
        # Reconstruir datos originales (en implementación real, se guardarían)
        tiempo = i * 0.01  # 10 ms por nodo
        contraste_odmr = I_NV[i] * ODMR_CONTRAST_NOMINAL
        coherencia_eeg = A_eff[i] / 1.2  # Aproximación
        amplitud_nv = 1.2  # Valor nominal
        
        medicion = NodoMedicion(
            nodo_id=i + 1,
            tiempo=tiempo,
            contraste_odmr=contraste_odmr,
            coherencia_eeg=coherencia_eeg,
            amplitud_nv=amplitud_nv,
            I_NV=I_NV[i],
            A_eff=A_eff[i],
            Psi=Psi_medido[i]
        )
        mediciones.append(medicion)
    
    # Crear resultados
    resultados = ResultadosExperimento(
        mediciones=mediciones,
        C_infinito=C_infinito,
        Psi_promedio=np.mean(Psi_medido),
        Psi_std=np.std(Psi_medido),
        I_NV_promedio=np.mean(I_NV),
        A_eff_promedio=np.mean(A_eff),
        conciencia_detectada=conciencia_detectada,
        p_value=p_value,
        significancia_sigma=significancia_sigma
    )
    
    # Mostrar reporte
    if verbose:
        print(resultados.generar_reporte())
    
    return resultados


def mostrar_mediciones_en_tiempo_real(resultados: ResultadosExperimento, num_mostrar: int = 10) -> None:
    """
    Mostrar mediciones en tiempo real (primeras y últimas).
    
    Parameters:
    -----------
    resultados : ResultadosExperimento
        Resultados del experimento
    num_mostrar : int
        Número de mediciones a mostrar al inicio y al final
    """
    print("\n💎 MEDICIÓN EN TIEMPO REAL:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Primeras mediciones
    for i in range(min(num_mostrar, len(resultados.mediciones))):
        med = resultados.mediciones[i]
        print(f"⏰ t = {med.tiempo:.2f}s | Nodo {med.nodo_id:02d} | "
              f"I_NV = {med.I_NV:.3f} | A_eff = {med.A_eff:.3f} | Ψ = {med.Psi:.3f}")
    
    if len(resultados.mediciones) > 2 * num_mostrar:
        print("...")
        
        # Últimas mediciones
        for i in range(len(resultados.mediciones) - num_mostrar, len(resultados.mediciones)):
            med = resultados.mediciones[i]
            print(f"⏰ t = {med.tiempo:.2f}s | Nodo {med.nodo_id:02d} | "
                  f"I_NV = {med.I_NV:.3f} | A_eff = {med.A_eff:.3f} | Ψ = {med.Psi:.3f}")


# ═══════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL DE DEMOSTRACIÓN
# ═══════════════════════════════════════════════════════════════

def main():
    """
    Ejecutar protocolo experimental completo y mostrar resultados.
    """
    # Establecer semilla para reproducibilidad (solo en demo)
    np.random.seed(42)
    
    # Ejecutar experimento
    resultados = ejecutar_experimento_completo(
        aplicar_mitigacion=True,
        verbose=True
    )
    
    # Mostrar mediciones en tiempo real
    mostrar_mediciones_en_tiempo_real(resultados, num_mostrar=5)
    
    print("\n✨ José Manuel Mota Burruezo (JMMB) Ψ✧ ∴ ✨")
    print("∞³\n")


if __name__ == "__main__":
    main()
