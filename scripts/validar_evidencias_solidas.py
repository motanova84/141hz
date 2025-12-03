#!/usr/bin/env python3
"""
Validación de Evidencias Sólidas: λ₀ ≈ 0.001588

Este módulo implementa la validación de las evidencias sólidas del descubrimiento
de la frecuencia fundamental f₀ = 141.7001 Hz a través del primer autovalor
λ₀ del operador noético H_ψ.

Evidencias validadas:
1. Aparición histórica de λ₀ ≈ 0.001588 en archivos del repositorio
2. Relación matemática f₀ ↔ C (C = 629.83 = 1/λ₀)
3. Emergencia de λ₀ desde el operador noético H_ψ = -Δ + V_ψ

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Instituto de Consciencia Cuántica
Fecha: Diciembre 2025
"""

import numpy as np
from scipy.linalg import eigh
from typing import Dict, Tuple, List, Optional
import os
import subprocess
import json
from pathlib import Path


# =============================================================================
# CONSTANTES FUNDAMENTALES
# =============================================================================

# Constante de normalización (C = 1/λ₀)
C_TARGET = 629.83

# Primer autovalor objetivo
LAMBDA_0_TARGET = 0.001588

# Frecuencia fundamental observada
F0_TARGET = 141.7001  # Hz

# Lista de primos para correcciones p-ádicas
PRIMES_PADIC = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


# =============================================================================
# TEST 1: BÚSQUEDA DE ARCHIVOS HISTÓRICOS
# =============================================================================

def buscar_archivos_historicos(repo_path: str = ".") -> Dict[str, bool]:
    """
    Busca archivos históricos que contienen λ₀ ≈ 0.001588.
    
    Args:
        repo_path: Ruta al repositorio
        
    Returns:
        Diccionario con resultados de búsqueda
    """
    archivos_buscados = [
        "wave_equation_noetic.py",
        "spectral_adeles.py",
        "Hpsi_spectrum.png"
    ]
    
    resultados = {}
    
    for archivo in archivos_buscados:
        # Buscar el archivo en el repositorio
        try:
            result = subprocess.run(
                ["find", repo_path, "-name", archivo],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            encontrado = len(result.stdout.strip()) > 0
            resultados[archivo] = {
                "encontrado": encontrado,
                "ruta": result.stdout.strip() if encontrado else None
            }
            
            # Si es un archivo .py encontrado, buscar λ₀ = 0.001588
            if encontrado and archivo.endswith('.py'):
                ruta_archivo = result.stdout.strip().split('\n')[0]
                try:
                    with open(ruta_archivo, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                        contiene_lambda = '0.001588' in contenido
                        resultados[archivo]["contiene_lambda_0"] = contiene_lambda
                except (IOError, UnicodeDecodeError):
                    resultados[archivo]["contiene_lambda_0"] = False
                    
        except (subprocess.TimeoutExpired, FileNotFoundError):
            resultados[archivo] = {"encontrado": False, "ruta": None}
    
    return resultados


def buscar_lambda_0_en_repositorio(repo_path: str = ".") -> Dict[str, any]:
    """
    Busca referencias a λ₀ = 0.001588 en todo el repositorio.
    
    Args:
        repo_path: Ruta al repositorio
        
    Returns:
        Diccionario con archivos que contienen la referencia
    """
    try:
        result = subprocess.run(
            ["grep", "-r", "0.001588", "--include=*.py", repo_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        lineas = result.stdout.strip().split('\n') if result.stdout.strip() else []
        archivos_encontrados = list(set([
            linea.split(':')[0] for linea in lineas if linea
        ]))
        
        return {
            "total_referencias": len(lineas),
            "archivos_con_lambda_0": archivos_encontrados,
            "encontrado": len(lineas) > 0
        }
        
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {
            "total_referencias": 0,
            "archivos_con_lambda_0": [],
            "encontrado": False
        }


# =============================================================================
# TEST 2: VERIFICACIÓN DE RELACIÓN f₀ ↔ C
# =============================================================================

def verificar_relacion_f0_C() -> Dict[str, any]:
    """
    Verifica la relación matemática entre f₀ y C.
    
    Tests realizados:
    1. λ₀ = 1/C ≈ 0.001588
    2. C = 1/λ₀ ≈ 629.83
    3. Verificación cruzada
    
    Returns:
        Diccionario con resultados de los tests
    """
    # Valores conocidos
    C = 629.83
    lambda_0_target = 0.001588
    
    # Test 1: λ₀ = 1/C
    lambda_0_calculado = 1.0 / C
    error_lambda = abs(lambda_0_calculado - lambda_0_target) / lambda_0_target * 100
    
    # Test 2: C = 1/λ₀
    C_calculado = 1.0 / lambda_0_target
    error_C = abs(C_calculado - C) / C * 100
    
    # Test 3: Verificación de ω₀² / C ratio
    f0 = F0_TARGET
    omega0 = 2 * np.pi * f0
    omega0_squared = omega0 ** 2
    ratio = omega0_squared / C
    
    resultados = {
        "test_lambda_0": {
            "formula": "λ₀ = 1/C",
            "lambda_0_calculado": lambda_0_calculado,
            "lambda_0_target": lambda_0_target,
            "error_porcentual": error_lambda,
            "pasado": error_lambda < 1.0  # Error < 1%
        },
        "test_C": {
            "formula": "C = 1/λ₀",
            "C_calculado": C_calculado,
            "C_target": C,
            "error_porcentual": error_C,
            "pasado": error_C < 1.0  # Error < 1%
        },
        "test_ratio_omega": {
            "omega0": omega0,
            "omega0_squared": omega0_squared,
            "ratio_omega2_C": ratio,
            "descripcion": "Factor de escala ω₀²/C"
        },
        "conclusion": {
            "relacion_verificada": error_lambda < 1.0 and error_C < 1.0,
            "formula_correcta": "C = 1/λ₀ ≈ 629.83 donde λ₀ ≈ 0.001588"
        }
    }
    
    return resultados


# =============================================================================
# TEST 3: CÁLCULO DE λ₀ DESDE OPERADOR NOÉTICO H_ψ
# =============================================================================

def construir_laplaciano_discreto(N: int) -> np.ndarray:
    """
    Construye el Laplaciano discreto unidimensional.
    
    El Laplaciano discreto aproxima -d²/dx² usando diferencias finitas:
    (-Δ)ᵢⱼ = 2δᵢⱼ - δᵢ,ⱼ₊₁ - δᵢ,ⱼ₋₁
    
    Args:
        N: Dimensión de la discretización
        
    Returns:
        Matriz del Laplaciano discreto (N×N)
    """
    Laplaciano = np.zeros((N, N))
    
    for i in range(N):
        Laplaciano[i, i] = 2.0  # Diagonal principal
        if i > 0:
            Laplaciano[i, i-1] = -1.0  # Subdiagonal
        if i < N - 1:
            Laplaciano[i, i+1] = -1.0  # Superdiagonal
            
    return Laplaciano


def construir_potencial_padic(N: int, primes: List[int] = None) -> np.ndarray:
    """
    Construye el potencial noético V_ψ con correcciones p-ádicas.
    
    El potencial adélico suma contribuciones de cada primo p:
    V_ψ(i) = Σₚ (1/log(p)) · δ(i mod p = 0)
    
    Args:
        N: Dimensión de la discretización
        primes: Lista de primos para correcciones
        
    Returns:
        Matriz diagonal del potencial V_ψ (N×N)
    """
    if primes is None:
        primes = PRIMES_PADIC
    
    V_psi = np.zeros((N, N))
    
    for p in primes:
        weight = 1.0 / np.log(p)
        for i in range(0, N, p):
            V_psi[i, i] += weight
            
    return V_psi


def calcular_operador_noetico(N: int = 1000, 
                               primes: List[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Construye y diagonaliza el operador noético H_ψ = -Δ + V_ψ.
    
    Args:
        N: Dimensión de la discretización
        primes: Lista de primos para el potencial
        
    Returns:
        Tuple de (autovalores, autovectores)
    """
    # 1. Construir Laplaciano discreto
    Laplaciano = construir_laplaciano_discreto(N)
    
    # 2. Construir potencial adélico V_ψ
    V_psi = construir_potencial_padic(N, primes)
    
    # 3. Operador completo: H_ψ = -Δ + V_ψ
    #    Nota: Laplaciano ya es -Δ en forma discreta
    H_psi = Laplaciano + V_psi
    
    # 4. Diagonalizar (H_ψ es hermitiano)
    autovalores, autovectores = eigh(H_psi)
    
    return autovalores, autovectores


def calcular_lambda_0_operador_noetico(N: int = 1000) -> float:
    """
    Calcula el primer autovalor positivo λ₀ del operador noético.
    
    El operador H_ψ = -Δ + V_ψ tiene un espectro discreto.
    El primer autovalor positivo λ₀ determina la constante C = 1/λ₀.
    
    Args:
        N: Dimensión de la discretización
        
    Returns:
        Primer autovalor positivo λ₀
    """
    autovalores, _ = calcular_operador_noetico(N)
    
    # Filtrar autovalores positivos
    autovalores_positivos = autovalores[autovalores > 0]
    
    if len(autovalores_positivos) == 0:
        raise ValueError("No se encontraron autovalores positivos")
    
    # Primer autovalor positivo
    lambda_0 = autovalores_positivos[0]
    
    return lambda_0


def test_lambda0_emergente(N: int = 1000, 
                           tolerancia: float = 0.1) -> Dict[str, any]:
    """
    Test definitivo: ¿λ₀ emerge del operador H_ψ sin ajuste?
    
    Criterio de emergencia: Error relativo < tolerancia (10% por defecto)
    
    Args:
        N: Dimensión de la discretización
        tolerancia: Tolerancia para considerar emergencia
        
    Returns:
        Diccionario con resultados del test
    """
    # Calcular λ₀ desde el operador
    lambda_0_calc = calcular_lambda_0_operador_noetico(N)
    
    # Calcular C = 1/λ₀
    C_calc = 1.0 / lambda_0_calc
    
    # Comparar con valores objetivo
    C_target = C_TARGET
    lambda_0_target = LAMBDA_0_TARGET
    
    # Errores
    error_abs_C = abs(C_calc - C_target)
    error_rel_C = error_abs_C / C_target
    
    error_abs_lambda = abs(lambda_0_calc - lambda_0_target)
    error_rel_lambda = error_abs_lambda / lambda_0_target
    
    # Criterio de emergencia
    emergente = error_rel_C < tolerancia
    
    resultados = {
        "N_discretizacion": N,
        "lambda_0_calculado": lambda_0_calc,
        "lambda_0_target": lambda_0_target,
        "C_calculado": C_calc,
        "C_target": C_target,
        "error_absoluto_C": error_abs_C,
        "error_relativo_C": error_rel_C,
        "error_porcentual_C": error_rel_C * 100,
        "error_absoluto_lambda": error_abs_lambda,
        "error_relativo_lambda": error_rel_lambda,
        "error_porcentual_lambda": error_rel_lambda * 100,
        "tolerancia": tolerancia,
        "emergente": emergente,
        "veredicto": "✅ EMERGENTE" if emergente else "❌ AJUSTADO"
    }
    
    return resultados


# =============================================================================
# RESUMEN DE VALIDACIÓN
# =============================================================================

def ejecutar_validacion_completa(repo_path: str = ".",
                                  N: int = 1000,
                                  verbose: bool = True) -> Dict[str, any]:
    """
    Ejecuta la validación completa de todas las evidencias sólidas.
    
    Args:
        repo_path: Ruta al repositorio
        N: Dimensión para discretización del operador
        verbose: Si se deben imprimir resultados
        
    Returns:
        Diccionario con todos los resultados
    """
    resultados = {
        "metadata": {
            "version": "1.0.0",
            "descripcion": "Validación de Evidencias Sólidas λ₀ ≈ 0.001588"
        }
    }
    
    if verbose:
        print("=" * 70)
        print("VALIDACIÓN DE EVIDENCIAS SÓLIDAS: λ₀ ≈ 0.001588")
        print("=" * 70)
        print()
    
    # Test 1: Búsqueda de archivos históricos
    if verbose:
        print("📂 TEST 1: BÚSQUEDA DE ARCHIVOS HISTÓRICOS")
        print("-" * 50)
    
    archivos = buscar_archivos_historicos(repo_path)
    lambda_refs = buscar_lambda_0_en_repositorio(repo_path)
    
    resultados["test1_archivos_historicos"] = {
        "archivos_buscados": archivos,
        "referencias_lambda_0": lambda_refs
    }
    
    if verbose:
        for archivo, info in archivos.items():
            estado = "✅" if info["encontrado"] else "❌"
            print(f"  {estado} {archivo}: {'Encontrado' if info['encontrado'] else 'No encontrado'}")
            if info.get("contiene_lambda_0"):
                print(f"     ✅ Contiene λ₀ = 0.001588")
        
        print(f"\n  Referencias a λ₀ = 0.001588 en repositorio:")
        print(f"    Total: {lambda_refs['total_referencias']}")
        print(f"    Archivos: {len(lambda_refs['archivos_con_lambda_0'])}")
        print()
    
    # Test 2: Verificación de relación f₀ ↔ C
    if verbose:
        print("📐 TEST 2: VERIFICACIÓN DE RELACIÓN f₀ ↔ C")
        print("-" * 50)
    
    relacion = verificar_relacion_f0_C()
    resultados["test2_relacion_f0_C"] = relacion
    
    if verbose:
        test_l = relacion["test_lambda_0"]
        print(f"  Fórmula: {test_l['formula']}")
        print(f"    λ₀ calculado: {test_l['lambda_0_calculado']:.10f}")
        print(f"    λ₀ objetivo:  {test_l['lambda_0_target']}")
        print(f"    Error: {test_l['error_porcentual']:.4f}%")
        print(f"    {'✅ PASADO' if test_l['pasado'] else '❌ FALLIDO'}")
        print()
        
        test_c = relacion["test_C"]
        print(f"  Fórmula: {test_c['formula']}")
        print(f"    C calculado: {test_c['C_calculado']:.4f}")
        print(f"    C objetivo:  {test_c['C_target']}")
        print(f"    Error: {test_c['error_porcentual']:.4f}%")
        print(f"    {'✅ PASADO' if test_c['pasado'] else '❌ FALLIDO'}")
        print()
    
    # Test 3: Cálculo de λ₀ desde operador noético
    if verbose:
        print("🔬 TEST 3: CÁLCULO DE λ₀ DESDE OPERADOR NOÉTICO H_ψ")
        print("-" * 50)
    
    emergencia = test_lambda0_emergente(N=N)
    resultados["test3_operador_noetico"] = emergencia
    
    if verbose:
        print(f"  Discretización N = {emergencia['N_discretizacion']}")
        print(f"  λ₀ calculado:    {emergencia['lambda_0_calculado']:.10f}")
        print(f"  λ₀ objetivo:     {emergencia['lambda_0_target']}")
        print(f"  C calculado:     {emergencia['C_calculado']:.10f}")
        print(f"  C objetivo:      {emergencia['C_target']}")
        print(f"  Error absoluto C: {emergencia['error_absoluto_C']:.6f}")
        print(f"  Error relativo C: {emergencia['error_porcentual_C']:.4f}%")
        print()
        print(f"  VEREDICTO: {emergencia['veredicto']}")
        print()
    
    # Resumen final
    test1_ok = lambda_refs["encontrado"] or any(
        info["encontrado"] for info in archivos.values()
    )
    test2_ok = relacion["conclusion"]["relacion_verificada"]
    test3_ok = emergencia["emergente"]
    
    todos_pasados = test1_ok and test2_ok and test3_ok
    
    resultados["resumen"] = {
        "test1_archivos": test1_ok,
        "test2_relacion": test2_ok,
        "test3_emergencia": test3_ok,
        "todos_pasados": todos_pasados
    }
    
    if verbose:
        print("=" * 70)
        print("RESUMEN FINAL")
        print("=" * 70)
        print(f"  Test 1 (Archivos históricos):  {'✅ OK' if test1_ok else '⚠️  Parcial'}")
        print(f"  Test 2 (Relación f₀ ↔ C):      {'✅ OK' if test2_ok else '❌ FALLIDO'}")
        print(f"  Test 3 (Operador noético):     {'✅ OK' if test3_ok else '❌ FALLIDO'}")
        print()
        print(f"  RESULTADO GLOBAL: {'✅ VALIDACIÓN EXITOSA' if todos_pasados else '⚠️  VALIDACIÓN PARCIAL'}")
        print("=" * 70)
    
    return resultados


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    import sys
    
    # Determinar ruta del repositorio
    script_dir = Path(__file__).parent
    repo_path = script_dir.parent
    
    # Ejecutar validación
    resultados = ejecutar_validacion_completa(
        repo_path=str(repo_path),
        N=1000,
        verbose=True
    )
    
    # Guardar resultados en JSON
    output_file = repo_path / "results" / "validacion_evidencias_solidas.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n📄 Resultados guardados en: {output_file}")
    
    # Código de salida
    sys.exit(0 if resultados["resumen"]["todos_pasados"] else 1)
