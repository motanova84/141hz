#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Mutaciones Resonantes: Análisis y Optimización de Secuencias ADN
==========================================================================
Este módulo implementa el análisis de mutaciones en secuencias de ADN
desde la perspectiva de la resonancia con f₀ = 141.7001 Hz.

Conceptos clave:
1. Analizar mutaciones (cambios de base) y su impacto en resonancia
2. Optimizar secuencias para maximizar coherencia cuántica
3. Predecir mutaciones que mejoran propiedades espectrales

Autor: QCAL ∞³ System
Fecha: 2026-03-08
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from adn_riemann import (
    CodificadorADNRiemann, CalculadorCerosRiemann,
    calcular_coherencia_cuantica_adn,
    BASE_A_NUMERO, NUMERO_A_BASE, COMPLEMENTO,
    FRECUENCIA_BASE, PSI_OPTIMO
)


class AnalizadorMutaciones:
    """
    Analiza mutaciones en secuencias de ADN y su impacto en propiedades espectrales.
    
    Evalúa cómo cambios puntuales (SNPs - Single Nucleotide Polymorphisms)
    afectan la resonancia con f₀ y la coherencia cuántica.
    """
    
    def __init__(self, codificador: CodificadorADNRiemann):
        """
        Inicializa el analizador de mutaciones.
        
        Args:
            codificador: Instancia de CodificadorADNRiemann
        """
        self.codificador = codificador
    
    def analizar_mutacion_puntual(self, secuencia: str, posicion: int,
                                  nueva_base: str) -> Dict:
        """
        Analiza el efecto de una mutación puntual.
        
        Args:
            secuencia: Secuencia original
            posicion: Posición a mutar (0-indexed)
            nueva_base: Nueva base (A, T, G, C)
            
        Returns:
            Dict con análisis comparativo
        """
        if posicion < 0 or posicion >= len(secuencia):
            raise ValueError(f"Posición {posicion} fuera de rango")
        
        nueva_base = nueva_base.upper()
        if nueva_base not in BASE_A_NUMERO:
            raise ValueError(f"Base inválida: {nueva_base}")
        
        # Crear secuencia mutada
        secuencia_mutada = (
            secuencia[:posicion] + nueva_base + secuencia[posicion + 1:]
        )
        
        # Propiedades originales
        props_orig = self.codificador.propiedades_espectrales(secuencia)
        coherencia_orig = calcular_coherencia_cuantica_adn(secuencia)
        
        # Propiedades mutadas
        props_mut = self.codificador.propiedades_espectrales(secuencia_mutada)
        coherencia_mut = calcular_coherencia_cuantica_adn(secuencia_mutada)
        
        # Cambios
        delta_resonancia = props_mut['resonancia_f0'] - props_orig['resonancia_f0']
        delta_coherencia = coherencia_mut['psi_efectivo'] - coherencia_orig['psi_efectivo']
        delta_frecuencia = props_mut['frecuencia_riemann_hz'] - props_orig['frecuencia_riemann_hz']
        
        return {
            'secuencia_original': secuencia,
            'secuencia_mutada': secuencia_mutada,
            'posicion': posicion,
            'base_original': secuencia[posicion],
            'base_nueva': nueva_base,
            'resonancia_original': props_orig['resonancia_f0'],
            'resonancia_mutada': props_mut['resonancia_f0'],
            'delta_resonancia': delta_resonancia,
            'coherencia_original': coherencia_orig['psi_efectivo'],
            'coherencia_mutada': coherencia_mut['psi_efectivo'],
            'delta_coherencia': delta_coherencia,
            'frecuencia_original_hz': props_orig['frecuencia_riemann_hz'],
            'frecuencia_mutada_hz': props_mut['frecuencia_riemann_hz'],
            'delta_frecuencia_hz': delta_frecuencia,
            'mejora_resonancia': delta_resonancia > 0,
            'mejora_coherencia': delta_coherencia > 0,
            'mejora_total': delta_resonancia > 0 and delta_coherencia > 0
        }
    
    def encontrar_mejores_mutaciones(self, secuencia: str,
                                     num_mejores: int = 5) -> List[Dict]:
        """
        Encuentra las mejores mutaciones puntuales para una secuencia.
        
        Args:
            secuencia: Secuencia original
            num_mejores: Número de mejores mutaciones a retornar
            
        Returns:
            Lista de diccionarios con las mejores mutaciones
        """
        mutaciones = []
        bases = ['A', 'T', 'G', 'C']
        
        for pos in range(len(secuencia)):
            base_actual = secuencia[pos]
            for nueva_base in bases:
                if nueva_base != base_actual:
                    analisis = self.analizar_mutacion_puntual(secuencia, pos, nueva_base)
                    mutaciones.append(analisis)
        
        # Ordenar por mejora combinada (resonancia + coherencia)
        mutaciones.sort(
            key=lambda x: x['delta_resonancia'] + x['delta_coherencia'],
            reverse=True
        )
        
        return mutaciones[:num_mejores]
    
    def analizar_complementariedad(self, secuencia: str) -> Dict:
        """
        Analiza la simetría de complementariedad (Watson-Crick).
        
        Args:
            secuencia: Secuencia de ADN
            
        Returns:
            Dict con análisis de complementariedad
        """
        # Generar complemento
        complemento = ''.join([COMPLEMENTO[base] for base in secuencia])
        
        # Propiedades de ambas
        props_seq = self.codificador.propiedades_espectrales(secuencia)
        props_comp = self.codificador.propiedades_espectrales(complemento)
        
        # Simetría
        diferencia_resonancia = abs(
            props_seq['resonancia_f0'] - props_comp['resonancia_f0']
        )
        diferencia_frecuencia = abs(
            props_seq['frecuencia_riemann_hz'] - props_comp['frecuencia_riemann_hz']
        )
        
        return {
            'secuencia': secuencia,
            'complemento': complemento,
            'resonancia_secuencia': props_seq['resonancia_f0'],
            'resonancia_complemento': props_comp['resonancia_f0'],
            'diferencia_resonancia': diferencia_resonancia,
            'frecuencia_secuencia_hz': props_seq['frecuencia_riemann_hz'],
            'frecuencia_complemento_hz': props_comp['frecuencia_riemann_hz'],
            'diferencia_frecuencia_hz': diferencia_frecuencia,
            'simetrica': diferencia_resonancia < 0.01
        }


class OptimizadorSecuencias:
    """
    Optimiza secuencias de ADN para maximizar resonancia y coherencia.
    
    Implementa algoritmos de búsqueda para encontrar secuencias óptimas
    dentro de restricciones biológicas.
    """
    
    def __init__(self, codificador: CodificadorADNRiemann,
                 analizador: AnalizadorMutaciones):
        """
        Inicializa el optimizador.
        
        Args:
            codificador: Instancia de CodificadorADNRiemann
            analizador: Instancia de AnalizadorMutaciones
        """
        self.codificador = codificador
        self.analizador = analizador
    
    def optimizar_local(self, secuencia: str, max_iteraciones: int = 100) -> Dict:
        """
        Optimiza una secuencia mediante búsqueda local (hill climbing).
        
        Args:
            secuencia: Secuencia inicial
            max_iteraciones: Número máximo de iteraciones
            
        Returns:
            Dict con la mejor secuencia encontrada
        """
        secuencia_actual = secuencia
        mejor_score = self._calcular_score(secuencia_actual)
        
        historial = [{'iteracion': 0, 'secuencia': secuencia_actual, 'score': mejor_score}]
        
        for iteracion in range(1, max_iteraciones + 1):
            # Encontrar mejor mutación puntual
            mutaciones = self.analizador.encontrar_mejores_mutaciones(secuencia_actual, num_mejores=1)
            
            if not mutaciones:
                break
            
            mejor_mutacion = mutaciones[0]
            
            # Solo aceptar si mejora
            nuevo_score = self._calcular_score(mejor_mutacion['secuencia_mutada'])
            
            if nuevo_score > mejor_score:
                secuencia_actual = mejor_mutacion['secuencia_mutada']
                mejor_score = nuevo_score
                historial.append({
                    'iteracion': iteracion,
                    'secuencia': secuencia_actual,
                    'score': mejor_score,
                    'mutacion': f"{mejor_mutacion['base_original']}{mejor_mutacion['posicion']}{mejor_mutacion['base_nueva']}"
                })
            else:
                # Mínimo local alcanzado
                break
        
        props_final = self.codificador.propiedades_espectrales(secuencia_actual)
        coherencia_final = calcular_coherencia_cuantica_adn(secuencia_actual)
        
        return {
            'secuencia_original': secuencia,
            'secuencia_optimizada': secuencia_actual,
            'score_original': self._calcular_score(secuencia),
            'score_final': mejor_score,
            'mejora_score': mejor_score - self._calcular_score(secuencia),
            'iteraciones_totales': len(historial) - 1,
            'resonancia_final': props_final['resonancia_f0'],
            'coherencia_final': coherencia_final['psi_efectivo'],
            'historial': historial
        }
    
    def buscar_secuencia_optima(self, longitud: int, num_candidatos: int = 1000) -> Dict:
        """
        Busca la secuencia óptima de una longitud dada mediante muestreo.
        
        Args:
            longitud: Longitud de la secuencia
            num_candidatos: Número de secuencias aleatorias a evaluar
            
        Returns:
            Dict con la mejor secuencia encontrada
        """
        mejor_secuencia = None
        mejor_score = -np.inf
        
        bases = ['A', 'T', 'G', 'C']
        
        for _ in range(num_candidatos):
            # Generar secuencia aleatoria
            secuencia = ''.join(np.random.choice(bases, size=longitud))
            
            # Evaluar
            score = self._calcular_score(secuencia)
            
            if score > mejor_score:
                mejor_score = score
                mejor_secuencia = secuencia
        
        props = self.codificador.propiedades_espectrales(mejor_secuencia)
        coherencia = calcular_coherencia_cuantica_adn(mejor_secuencia)
        
        return {
            'secuencia_optima': mejor_secuencia,
            'longitud': longitud,
            'score': mejor_score,
            'resonancia_f0': props['resonancia_f0'],
            'coherencia': coherencia['psi_efectivo'],
            'frecuencia_riemann_hz': props['frecuencia_riemann_hz'],
            'candidatos_evaluados': num_candidatos
        }
    
    def _calcular_score(self, secuencia: str) -> float:
        """
        Calcula el score de una secuencia (mayor es mejor).
        
        Combina resonancia y coherencia.
        
        Args:
            secuencia: Secuencia de ADN
            
        Returns:
            Score combinado
        """
        props = self.codificador.propiedades_espectrales(secuencia)
        coherencia = calcular_coherencia_cuantica_adn(secuencia)
        
        # Score combinado: 60% resonancia + 40% coherencia
        score = 0.6 * props['resonancia_f0'] + 0.4 * coherencia['psi_efectivo']
        
        return score


def demo_mutaciones_resonantes():
    """Demostración del módulo de mutaciones resonantes."""
    print("=" * 80)
    print("MUTACIONES RESONANTES: Optimización de Secuencias ADN")
    print("=" * 80)
    
    # Inicializar sistema
    calculador = CalculadorCerosRiemann(num_ceros=1000)
    codificador = CodificadorADNRiemann(calculador)
    analizador = AnalizadorMutaciones(codificador)
    optimizador = OptimizadorSecuencias(codificador, analizador)
    
    # Secuencia de prueba
    secuencia_test = "ATGC"
    
    print("\n1. Análisis de Mutación Puntual:")
    print("-" * 80)
    
    mutacion = analizador.analizar_mutacion_puntual(secuencia_test, 0, 'G')
    print(f"   Secuencia original: {mutacion['secuencia_original']}")
    print(f"   Secuencia mutada: {mutacion['secuencia_mutada']}")
    print(f"   Mutación: {mutacion['base_original']}{mutacion['posicion']} → {mutacion['base_nueva']}")
    print(f"   Δ Resonancia: {mutacion['delta_resonancia']:+.6f}")
    print(f"   Δ Coherencia: {mutacion['delta_coherencia']:+.6f}")
    print(f"   Mejora total: {mutacion['mejora_total']}")
    
    print("\n2. Mejores Mutaciones:")
    print("-" * 80)
    
    mejores = analizador.encontrar_mejores_mutaciones(secuencia_test, num_mejores=3)
    for i, mut in enumerate(mejores, 1):
        print(f"\n   #{i}: {mut['base_original']}{mut['posicion']} → {mut['base_nueva']}")
        print(f"       Secuencia: {mut['secuencia_mutada']}")
        print(f"       Δ Resonancia: {mut['delta_resonancia']:+.6f}")
        print(f"       Δ Coherencia: {mut['delta_coherencia']:+.6f}")
    
    print("\n3. Análisis de Complementariedad:")
    print("-" * 80)
    
    comp = analizador.analizar_complementariedad(secuencia_test)
    print(f"   Secuencia: {comp['secuencia']}")
    print(f"   Complemento: {comp['complemento']}")
    print(f"   Resonancia secuencia: {comp['resonancia_secuencia']:.6f}")
    print(f"   Resonancia complemento: {comp['resonancia_complemento']:.6f}")
    print(f"   Diferencia: {comp['diferencia_resonancia']:.6f}")
    print(f"   Simétrica: {comp['simetrica']}")
    
    print("\n4. Optimización Local:")
    print("-" * 80)
    
    resultado = optimizador.optimizar_local("AAAA", max_iteraciones=10)
    print(f"   Secuencia original: {resultado['secuencia_original']}")
    print(f"   Secuencia optimizada: {resultado['secuencia_optimizada']}")
    print(f"   Score original: {resultado['score_original']:.6f}")
    print(f"   Score final: {resultado['score_final']:.6f}")
    print(f"   Mejora: {resultado['mejora_score']:+.6f}")
    print(f"   Iteraciones: {resultado['iteraciones_totales']}")
    print(f"   Resonancia final: {resultado['resonancia_final']:.6f}")
    
    print("\n5. Búsqueda de Secuencia Óptima (longitud=4):")
    print("-" * 80)
    
    optima = optimizador.buscar_secuencia_optima(longitud=4, num_candidatos=256)
    print(f"   Secuencia óptima: {optima['secuencia_optima']}")
    print(f"   Score: {optima['score']:.6f}")
    print(f"   Resonancia: {optima['resonancia_f0']:.6f}")
    print(f"   Coherencia: {optima['coherencia']:.6f}")
    print(f"   Candidatos evaluados: {optima['candidatos_evaluados']}")
    
    print("\n" + "=" * 80)
    print("DEMOSTRACIÓN COMPLETADA")
    print("=" * 80)


if __name__ == "__main__":
    demo_mutaciones_resonantes()
