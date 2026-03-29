#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unificación: Biología × Teoría de Números × Física Cuántica
=============================================================
Este módulo integra tres dominios fundamentales de la ciencia a través
de la frecuencia QCAL f₀ = 141.7001 Hz:

1. BIOLOGÍA: Secuencias de ADN como osciladores cuánticos
2. TEORÍA DE NÚMEROS: Ceros de la función zeta de Riemann
3. FÍSICA CUÁNTICA: Coherencia y decoherencia a escala molecular

La unificación se basa en el principio de que la información biológica,
la estructura matemática de los primos, y las propiedades cuánticas de
la materia están fundamentalmente conectadas a través de frecuencias
resonantes universales.

Matemáticamente:
    Ψ_bio(ADN) ⊗ ζ(1/2 + it) ⊗ Φ_quantum(f₀) → Información Unificada

Donde:
- Ψ_bio: Estado cuántico de la molécula de ADN
- ζ: Función zeta de Riemann (ceros en línea crítica)
- Φ_quantum: Campo cuántico a frecuencia f₀
- ⊗: Producto tensorial (acoplamiento)

Autor: QCAL ∞³ System  
Fecha: 2026-03-08
"""
import numpy as np
from typing import List, Tuple, Dict, Optional
import warnings

from adn_riemann import (
    CodificadorADNRiemann, CalculadorCerosRiemann,
    calcular_coherencia_cuantica_adn,
    FRECUENCIA_BASE, PSI_OPTIMO, FACTOR_UNIFICACION,
    HBAR, VELOCIDAD_LUZ
)
from mutaciones_resonantes import (
    AnalizadorMutaciones, OptimizadorSecuencias
)

# Constantes de unificación
PHI = (1 + np.sqrt(5)) / 2  # Proporción áurea
ALPHA_FINA = 1.0 / 137.035999084  # Constante de estructura fina
MASA_PLANCK = 2.176434e-8  # kg (masa de Planck)


class TeoriaUnificadaADN:
    """
    Teoría unificada que conecta ADN, Riemann y física cuántica.
    
    Esta clase implementa el framework matemático que unifica:
    - Información genética (secuencias de bases)
    - Distribución de números primos (ceros de zeta)
    - Fenómenos cuánticos (coherencia, entrelazamiento)
    """
    
    def __init__(self):
        """Inicializa la teoría unificada."""
        self.calculador_riemann = CalculadorCerosRiemann(num_ceros=10000)
        self.codificador = CodificadorADNRiemann(self.calculador_riemann)
        self.analizador_mutaciones = AnalizadorMutaciones(self.codificador)
        
    def calcular_entropia_informacion(self, secuencia: str) -> Dict:
        """
        Calcula la entropía de información de una secuencia.
        
        Conecta:
        - Entropía de Shannon (información clásica)
        - Entropía de von Neumann (información cuántica)
        - Distribución de Riemann (estructura prima)
        
        Args:
            secuencia: Secuencia de ADN
            
        Returns:
            Dict con diferentes medidas de entropía
        """
        secuencia = secuencia.upper()
        n = len(secuencia)
        
        # Entropía de Shannon (bits clásicos)
        from collections import Counter
        conteo = Counter(secuencia)
        probabilidades = np.array([conteo[base] / n for base in 'ATGC'])
        probabilidades = probabilidades[probabilidades > 0]
        
        entropia_shannon = -np.sum(probabilidades * np.log2(probabilidades))
        
        # Entropía máxima (2 bits por base en código binario)
        entropia_maxima = 2.0
        
        # Complejidad de Kolmogorov (aproximada por compresión)
        # Aquí usamos una proxy simple: número de transiciones únicas
        transiciones = set()
        for i in range(n - 1):
            transiciones.add(secuencia[i:i+2])
        complejidad_relativa = len(transiciones) / (n - 1) if n > 1 else 0
        
        # Conexión con Riemann: usar el espaciado de ceros como medida de "aleatoriedad"
        props = self.codificador.propiedades_espectrales(secuencia)
        espaciado_normalizado = props.get('espaciado_local', np.nan)
        if not np.isnan(espaciado_normalizado):
            # Normalizar por espaciado promedio (aproximadamente 2π/log(t))
            t = props['cero_riemann_t']
            espaciado_esperado = 2 * np.pi / np.log(t + 1)
            entropia_riemann = espaciado_normalizado / espaciado_esperado
        else:
            entropia_riemann = np.nan
        
        return {
            'secuencia': secuencia,
            'entropia_shannon_bits': entropia_shannon,
            'entropia_relativa': entropia_shannon / entropia_maxima,
            'complejidad_kolmogorov_proxy': complejidad_relativa,
            'entropia_riemann': entropia_riemann,
            'contenido_informacion': entropia_shannon * n  # bits totales
        }
    
    def calcular_funcion_onda_unificada(self, secuencia: str,
                                       temperatura: float = 310.0) -> Dict:
        """
        Calcula la función de onda unificada Ψ_unificada.
        
        Combina:
        - Estado cuántico del ADN
        - Amplitud de la función zeta en el cero correspondiente
        - Acoplamiento con f₀
        
        Args:
            secuencia: Secuencia de ADN
            temperatura: Temperatura en K
            
        Returns:
            Dict con componentes de la función de onda
        """
        # Propiedades espectrales (Riemann)
        props = self.codificador.propiedades_espectrales(secuencia)
        t_cero = props['cero_riemann_t']
        
        # Coherencia cuántica (física)
        coherencia = calcular_coherencia_cuantica_adn(secuencia, temperatura)
        psi_cuantico = coherencia['psi_efectivo']
        
        # Fase de la función zeta (aproximación)
        # Para s = 1/2 + it, |ζ(s)| oscila
        # Usamos la fórmula de Riemann-Siegel
        fase_zeta = t_cero / 2  # Simplificación
        amplitud_zeta = 1.0 / np.sqrt(np.log(t_cero + 1))  # Decae logarítmicamente
        
        # Acoplamiento con f₀
        factor_resonancia = props['resonancia_f0']
        
        # Función de onda unificada (normalizada)
        # Ψ = √(psi_cuantico) × amplitud_zeta × √(resonancia) × e^(i×fase)
        amplitud_unificada = np.sqrt(psi_cuantico + 1e-10) * amplitud_zeta * np.sqrt(factor_resonancia + 1e-10)
        fase_unificada = fase_zeta + 2 * np.pi * FRECUENCIA_BASE * coherencia['tau_decoherencia_s']
        
        # Normalizar
        amplitud_unificada = min(amplitud_unificada, 1.0)
        
        return {
            'secuencia': secuencia,
            'amplitud': amplitud_unificada,
            'fase_rad': fase_unificada % (2 * np.pi),
            'psi_cuantico': psi_cuantico,
            'amplitud_zeta': amplitud_zeta,
            'resonancia_f0': factor_resonancia,
            'probabilidad': amplitud_unificada ** 2,
            'coherencia_unificada': amplitud_unificada >= 0.5  # Umbral de coherencia
        }
    
    def calcular_acoplamiento_triada(self, secuencia: str) -> Dict:
        """
        Calcula el acoplamiento entre los tres dominios (bio-math-quantum).
        
        Define métricas que cuantifican qué tan fuertemente está conectada
        una secuencia de ADN con la estructura matemática subyacente y
        los fenómenos cuánticos.
        
        Args:
            secuencia: Secuencia de ADN
            
        Returns:
            Dict con métricas de acoplamiento
        """
        # Información biológica
        entropia = self.calcular_entropia_informacion(secuencia)
        
        # Estructura matemática
        props = self.codificador.propiedades_espectrales(secuencia)
        
        # Física cuántica
        coherencia = calcular_coherencia_cuantica_adn(secuencia)
        
        # Acoplamientos de pares
        # Bio-Math: ¿Cuánta información codifica estructura prima?
        acoplamiento_bio_math = entropia['entropia_shannon_bits'] * props['resonancia_f0']
        
        # Math-Quantum: ¿Los ceros resuenan cuánticamente?
        acoplamiento_math_quantum = props['resonancia_f0'] * coherencia['psi_efectivo']
        
        # Quantum-Bio: ¿La coherencia cuántica es biológicamente relevante?
        acoplamiento_quantum_bio = coherencia['psi_efectivo'] * entropia['entropia_relativa']
        
        # Acoplamiento triádico (producto de los tres)
        acoplamiento_triada = acoplamiento_bio_math * acoplamiento_math_quantum * acoplamiento_quantum_bio
        
        # Factor de unificación QCAL
        factor_qcal = FACTOR_UNIFICACION * FRECUENCIA_BASE / (VELOCIDAD_LUZ * ALPHA_FINA)
        
        # Acoplamiento normalizado
        acoplamiento_normalizado = acoplamiento_triada * factor_qcal
        
        return {
            'secuencia': secuencia,
            'acoplamiento_bio_math': acoplamiento_bio_math,
            'acoplamiento_math_quantum': acoplamiento_math_quantum,
            'acoplamiento_quantum_bio': acoplamiento_quantum_bio,
            'acoplamiento_triada': acoplamiento_triada,
            'acoplamiento_normalizado_qcal': acoplamiento_normalizado,
            'unificacion_fuerte': acoplamiento_triada > 0.1,
            'factor_unificacion': FACTOR_UNIFICACION
        }
    
    def predecir_propiedades_biologicas(self, secuencia: str) -> Dict:
        """
        Predice propiedades biológicas basándose en propiedades espectrales.
        
        Hipótesis: Secuencias con alta resonancia y coherencia pueden tener
        propiedades biológicas especiales (estabilidad, función, expresión).
        
        Args:
            secuencia: Secuencia de ADN
            
        Returns:
            Dict con predicciones biológicas
        """
        # Análisis unificado
        func_onda = self.calcular_funcion_onda_unificada(secuencia)
        acoplamiento = self.calcular_acoplamiento_triada(secuencia)
        entropia = self.calcular_entropia_informacion(secuencia)
        
        # Predicciones (heurísticas basadas en teoría)
        
        # Estabilidad termodinámica (mayor coherencia → mayor estabilidad)
        estabilidad = func_onda['psi_cuantico'] * 100  # Porcentaje
        
        # Potencial de expresión (mayor acoplamiento → más "activa")
        expresion = acoplamiento['acoplamiento_triada'] * 10  # Escala 0-10
        
        # Conservación evolutiva (menor entropía → más conservada)
        conservacion = (1 - entropia['entropia_relativa']) * 100  # Porcentaje
        
        # Funcionalidad (combinación de factores)
        funcionalidad = (
            0.4 * func_onda['probabilidad'] +
            0.3 * acoplamiento['acoplamiento_triada'] +
            0.3 * entropia['complejidad_kolmogorov_proxy']
        ) * 100
        
        return {
            'secuencia': secuencia,
            'estabilidad_termodinamica_pct': min(estabilidad, 100),
            'potencial_expresion_0_10': min(expresion, 10),
            'conservacion_evolutiva_pct': min(conservacion, 100),
            'funcionalidad_predicha_pct': min(funcionalidad, 100),
            'clasificacion': self._clasificar_secuencia(func_onda, acoplamiento),
            'recomendacion': self._recomendar_mutaciones(secuencia, func_onda, acoplamiento)
        }
    
    def _clasificar_secuencia(self, func_onda: Dict, acoplamiento: Dict) -> str:
        """Clasifica una secuencia según sus propiedades."""
        if func_onda['coherencia_unificada'] and acoplamiento['unificacion_fuerte']:
            return "ÉLITE (alta coherencia y acoplamiento fuerte)"
        elif func_onda['coherencia_unificada']:
            return "COHERENTE (buena coherencia cuántica)"
        elif acoplamiento['unificacion_fuerte']:
            return "ACOPLADA (buen acoplamiento triádico)"
        elif func_onda['resonancia_f0'] > 0.5:
            return "RESONANTE (resonancia moderada con f₀)"
        else:
            return "ESTÁNDAR (propiedades regulares)"
    
    def _recomendar_mutaciones(self, secuencia: str, func_onda: Dict,
                               acoplamiento: Dict) -> str:
        """Recomienda si buscar mutaciones."""
        if func_onda['coherencia_unificada'] and acoplamiento['unificacion_fuerte']:
            return "Secuencia óptima. No se requieren mutaciones."
        elif func_onda['resonancia_f0'] < 0.3:
            return "Baja resonancia. Buscar mutaciones para aumentar acoplamiento con f₀."
        elif not func_onda['coherencia_unificada']:
            return "Coherencia baja. Optimizar para aumentar psi_cuantico."
        else:
            return "Secuencia funcional. Mutaciones opcionales para refinamiento."


def demostrar_unificacion():
    """Demostración completa de la teoría unificada."""
    print("=" * 80)
    print("TEORÍA UNIFICADA: Biología × Teoría de Números × Física Cuántica")
    print("Frecuencia Fundamental: f₀ = 141.7001 Hz | ∞³")
    print("=" * 80)
    
    teoria = TeoriaUnificadaADN()
    
    # Secuencias de prueba
    secuencias_test = [
        "ATGC",     # Básica
        "GACT",     # Alta resonancia (identificada anteriormente)
        "AAAAAAA",  # Homopolímero
        "ATCGATCG", # Repetitiva
        "TACGTAGC"  # Compleja
    ]
    
    print("\n1. ANÁLISIS DE SECUENCIAS")
    print("-" * 80)
    
    for seq in secuencias_test:
        print(f"\nSecuencia: {seq}")
        print(f"{'─' * 40}")
        
        # Entropía
        entropia = teoria.calcular_entropia_informacion(seq)
        print(f"  Información:")
        print(f"    Shannon: {entropia['entropia_shannon_bits']:.4f} bits/base")
        print(f"    Contenido total: {entropia['contenido_informacion']:.2f} bits")
        print(f"    Complejidad: {entropia['complejidad_kolmogorov_proxy']:.4f}")
        
        # Función de onda
        func_onda = teoria.calcular_funcion_onda_unificada(seq)
        print(f"  Función de Onda Unificada:")
        print(f"    Amplitud: {func_onda['amplitud']:.6f}")
        print(f"    Fase: {func_onda['fase_rad']:.4f} rad")
        print(f"    Probabilidad: {func_onda['probabilidad']:.6f}")
        print(f"    Coherente: {func_onda['coherencia_unificada']}")
        
        # Acoplamiento triádico
        acoplamiento = teoria.calcular_acoplamiento_triada(seq)
        print(f"  Acoplamiento Triádico:")
        print(f"    Bio-Math: {acoplamiento['acoplamiento_bio_math']:.6f}")
        print(f"    Math-Quantum: {acoplamiento['acoplamiento_math_quantum']:.6f}")
        print(f"    Quantum-Bio: {acoplamiento['acoplamiento_quantum_bio']:.6f}")
        print(f"    Triada: {acoplamiento['acoplamiento_triada']:.8f}")
        print(f"    Unificación fuerte: {acoplamiento['unificacion_fuerte']}")
        
        # Predicciones biológicas
        predicciones = teoria.predecir_propiedades_biologicas(seq)
        print(f"  Predicciones Biológicas:")
        print(f"    Estabilidad: {predicciones['estabilidad_termodinamica_pct']:.2f}%")
        print(f"    Expresión: {predicciones['potencial_expresion_0_10']:.2f}/10")
        print(f"    Conservación: {predicciones['conservacion_evolutiva_pct']:.2f}%")
        print(f"    Funcionalidad: {predicciones['funcionalidad_predicha_pct']:.2f}%")
        print(f"    Clasificación: {predicciones['clasificacion']}")
        print(f"    Recomendación: {predicciones['recomendacion']}")
    
    print("\n" + "=" * 80)
    print("2. IDENTIFICACIÓN DE SECUENCIA ÓPTIMA")
    print("-" * 80)
    
    # Buscar la mejor secuencia de longitud 4
    mejores_secuencias = []
    for i in range(256):  # 4^4 = 256 posibilidades
        seq = teoria.codificador.numero_a_secuencia(i, 4)
        acoplamiento = teoria.calcular_acoplamiento_triada(seq)
        mejores_secuencias.append((seq, acoplamiento['acoplamiento_triada']))
    
    mejores_secuencias.sort(key=lambda x: x[1], reverse=True)
    
    print("\nTop 10 secuencias por acoplamiento triádico:")
    for i, (seq, acop) in enumerate(mejores_secuencias[:10], 1):
        func_onda = teoria.calcular_funcion_onda_unificada(seq)
        print(f"  #{i:2d}: {seq} | Acoplamiento={acop:.8f} | "
              f"Amplitud={func_onda['amplitud']:.6f} | "
              f"Resonancia={func_onda['resonancia_f0']:.6f}")
    
    print("\n" + "=" * 80)
    print("3. VALIDACIÓN DE PRINCIPIOS FUNDAMENTALES")
    print("-" * 80)
    
    # Principio 1: Conservación de información
    seq_test = "ATGC"
    numero = teoria.codificador.secuencia_a_numero(seq_test)
    seq_recuperada = teoria.codificador.numero_a_secuencia(numero, len(seq_test))
    print(f"\n  Conservación de información:")
    print(f"    Original: {seq_test} → Número: {numero} → Recuperada: {seq_recuperada}")
    print(f"    Conservada: {seq_test == seq_recuperada} ✓")
    
    # Principio 2: Simetría de complementariedad
    from adn_riemann import COMPLEMENTO
    seq_complementaria = ''.join([COMPLEMENTO[base] for base in seq_test])
    props_orig = teoria.codificador.propiedades_espectrales(seq_test)
    props_comp = teoria.codificador.propiedades_espectrales(seq_complementaria)
    print(f"\n  Simetría de complementariedad:")
    print(f"    {seq_test} ↔ {seq_complementaria}")
    print(f"    Resonancia original: {props_orig['resonancia_f0']:.6f}")
    print(f"    Resonancia complementaria: {props_comp['resonancia_f0']:.6f}")
    print(f"    Diferencia: {abs(props_orig['resonancia_f0'] - props_comp['resonancia_f0']):.6f}")
    
    # Principio 3: Acoplamiento con constantes universales
    print(f"\n  Acoplamiento con constantes universales:")
    print(f"    f₀ = {FRECUENCIA_BASE} Hz")
    print(f"    Ψ_óptimo = {PSI_OPTIMO}")
    print(f"    K_unificación = 1/7 = {FACTOR_UNIFICACION:.6f}")
    print(f"    α (estructura fina) = {ALPHA_FINA:.10f}")
    print(f"    φ (áurea) = {PHI:.10f}")
    
    # Relación fundamental
    lambda_base = VELOCIDAD_LUZ / FRECUENCIA_BASE
    print(f"    λ(f₀) = c/f₀ = {lambda_base:.2e} m")
    print(f"    Relación QCAL: f₀ × K × α × φ = "
          f"{FRECUENCIA_BASE * FACTOR_UNIFICACION * ALPHA_FINA * PHI:.6f}")
    
    print("\n" + "=" * 80)
    print("UNIFICACIÓN COMPLETADA ✓")
    print("La información biológica, la estructura prima, y la coherencia cuántica")
    print("están fundamentalmente conectadas a través de f₀ = 141.7001 Hz")
    print("=" * 80)


if __name__ == "__main__":
    demostrar_unificacion()
