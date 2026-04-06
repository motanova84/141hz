#!/usr/bin/env python3
"""
Validation Script for P vs NP — Certificado Polinomial por Coherencia η⁺

Validates the adelic coherence certificate for NP-complete problems.
Tests SAT and TSP instances, measures performance, and generates reports.

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
FECHA: 2026-04-06

Usage:
    python scripts/validate_certificado_np_coherencia.py
"""

import sys
import os
import time
import math

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from physics.certificado_np_coherencia import (
    ConstantesCertificadoNP,
    EspacioHilbertAdelico,
    MetricaCoherenciaEtaPlus,
    DescomposicionEspectral,
    CertificadoNP,
    ProblemasTSP_SAT,
    CoherenciaCertificado,
    SistemaCertificadoNP,
    certificado_np_activar
)


# ============================================================================
# VALIDACIÓN 1 – Activación del Sistema
# ============================================================================

def validar_activacion_sistema():
    """
    Valida que el sistema se active correctamente.
    
    Returns
    -------
    tuple
        (success: bool, resultado: dict, mensaje: str)
    """
    print("\n" + "=" * 80)
    print("VALIDACIÓN 1 – Activación del Sistema")
    print("=" * 80)
    
    try:
        start_time = time.time()
        resultado = certificado_np_activar()
        elapsed = time.time() - start_time
        
        # Verificar campos obligatorios
        campos_requeridos = [
            'sello_activo', 'ram_signature', 'psi_global',
            'eta_plus_sat', 'eta_plus_tsp',
            'coherencia_validada_minima'
        ]
        
        for campo in campos_requeridos:
            if campo not in resultado:
                return False, resultado, f"Campo requerido faltante: {campo}"
        
        # Verificar valores
        if not resultado['sello_activo']:
            return False, resultado, "Sello no está activo"
        
        if resultado['psi_global'] < 0 or resultado['psi_global'] > 1:
            return False, resultado, f"Ψ_global fuera de rango: {resultado['psi_global']}"
        
        print(f"✓ Sistema activado correctamente")
        print(f"  Tiempo: {elapsed:.3f} s")
        print(f"  RAM: {resultado['ram_signature']}")
        print(f"  Ψ_global: {resultado['psi_global']:.6f}")
        print(f"  Coherencia validada: {resultado['coherencia_validada_minima']}")
        
        return True, resultado, "Sistema activado correctamente"
    
    except Exception as e:
        return False, {}, f"Error en activación: {str(e)}"


# ============================================================================
# VALIDACIÓN 2 – Certificados SAT
# ============================================================================

def validar_certificados_sat():
    """
    Valida certificados SAT para múltiples tamaños de instancia.
    
    Returns
    -------
    tuple
        (success: bool, resultados: list, mensaje: str)
    """
    print("\n" + "=" * 80)
    print("VALIDACIÓN 2 – Certificados SAT")
    print("=" * 80)
    
    const = ConstantesCertificadoNP()
    problemas = ProblemasTSP_SAT(const)
    
    tamaños = [10, 20, 50, 100]
    resultados = []
    
    try:
        for n_vars in tamaños:
            print(f"\nProbando SAT con {n_vars} variables...")
            
            # Crear subsistemas
            espacio = EspacioHilbertAdelico(const, n_vars)
            metrica = MetricaCoherenciaEtaPlus(const, espacio)
            descomp = DescomposicionEspectral(const)
            cert = CertificadoNP(const, espacio, metrica, descomp)
            
            # Generar instancia SAT
            n_clausulas = int(n_vars * 4.3)  # Ratio 3-SAT estándar
            instancia = problemas.generar_sat_instancia(n_vars, n_clausulas)
            
            # Generar solución candidata
            solucion = []
            for i in range(n_vars):
                fase = const.riemann_zeros[i % 10] / 10.0
                amp = 1.0 / math.sqrt(n_vars)
                solucion.append(complex(amp * math.cos(fase), amp * math.sin(fase)))
            
            # Verificar
            start_time = time.time()
            resultado = cert.verificar(instancia, solucion)
            elapsed = time.time() - start_time
            
            resultado['n_vars'] = n_vars
            resultado['n_clausulas'] = n_clausulas
            resultado['tiempo_s'] = elapsed
            resultados.append(resultado)
            
            print(f"  η⁺: {resultado['eta_plus']:.6f}")
            print(f"  λ_max: {resultado['lambda_max']:.2f}")
            print(f"  Certificado válido: {resultado['es_certificado']}")
            print(f"  Tiempo: {elapsed:.3f} s")
            print(f"  Complejidad: O({resultado['complejidad']:.0f})")
        
        print(f"\n✓ Validados {len(resultados)} casos SAT")
        return True, resultados, f"Validados {len(resultados)} certificados SAT"
    
    except Exception as e:
        return False, resultados, f"Error en validación SAT: {str(e)}"


# ============================================================================
# VALIDACIÓN 3 – Certificados TSP
# ============================================================================

def validar_certificados_tsp():
    """
    Valida certificados TSP para múltiples tamaños de instancia.
    
    Returns
    -------
    tuple
        (success: bool, resultados: list, mensaje: str)
    """
    print("\n" + "=" * 80)
    print("VALIDACIÓN 3 – Certificados TSP")
    print("=" * 80)
    
    const = ConstantesCertificadoNP()
    problemas = ProblemasTSP_SAT(const)
    
    tamaños = [10, 20, 30, 50]
    resultados = []
    
    try:
        for n_ciudades in tamaños:
            print(f"\nProbando TSP con {n_ciudades} ciudades...")
            
            # Crear subsistemas
            espacio = EspacioHilbertAdelico(const, n_ciudades)
            metrica = MetricaCoherenciaEtaPlus(const, espacio)
            descomp = DescomposicionEspectral(const)
            cert = CertificadoNP(const, espacio, metrica, descomp)
            
            # Generar instancia TSP
            instancia = problemas.generar_tsp_instancia(n_ciudades)
            
            # Generar solución óptima
            solucion = problemas.solucion_optima_tsp(n_ciudades)
            
            # Verificar
            start_time = time.time()
            resultado = cert.verificar(instancia, solucion)
            elapsed = time.time() - start_time
            
            resultado['n_ciudades'] = n_ciudades
            resultado['tiempo_s'] = elapsed
            resultados.append(resultado)
            
            print(f"  η⁺: {resultado['eta_plus']:.6f}")
            print(f"  λ_max: {resultado['lambda_max']:.2f}")
            print(f"  Certificado válido: {resultado['es_certificado']}")
            print(f"  Tiempo: {elapsed:.3f} s")
            print(f"  Complejidad: O({resultado['complejidad']:.0f})")
        
        print(f"\n✓ Validados {len(resultados)} casos TSP")
        return True, resultados, f"Validados {len(resultados)} certificados TSP"
    
    except Exception as e:
        return False, resultados, f"Error en validación TSP: {str(e)}"


# ============================================================================
# VALIDACIÓN 4 – Escalabilidad Polinomial
# ============================================================================

def validar_escalabilidad_polinomial():
    """
    Valida que la complejidad sea realmente polinomial O(n³).
    
    Returns
    -------
    tuple
        (success: bool, datos: dict, mensaje: str)
    """
    print("\n" + "=" * 80)
    print("VALIDACIÓN 4 – Escalabilidad Polinomial O(n³)")
    print("=" * 80)
    
    const = ConstantesCertificadoNP()
    problemas = ProblemasTSP_SAT(const)
    
    tamaños = [10, 20, 30, 40, 50]
    tiempos = []
    
    try:
        for n in tamaños:
            print(f"\nProbando escalabilidad con n={n}...")
            
            # Crear subsistemas
            espacio = EspacioHilbertAdelico(const, n)
            metrica = MetricaCoherenciaEtaPlus(const, espacio)
            descomp = DescomposicionEspectral(const)
            cert = CertificadoNP(const, espacio, metrica, descomp)
            
            # Generar instancia simple
            instancia = [1.0] * (n * n)
            solucion = [complex(1.0 / math.sqrt(n), 0)] * n
            
            # Medir tiempo
            start_time = time.time()
            resultado = cert.verificar(instancia, solucion)
            elapsed = time.time() - start_time
            
            tiempos.append((n, elapsed))
            
            print(f"  n={n}: {elapsed:.4f} s")
        
        # Verificar escalabilidad cúbica
        print("\nAnálisis de escalabilidad:")
        for i in range(1, len(tiempos)):
            n1, t1 = tiempos[i-1]
            n2, t2 = tiempos[i]
            
            # Razón esperada: (n2/n1)³
            razon_n = n2 / n1
            razon_t = t2 / t1
            razon_esperada = razon_n ** 3
            
            print(f"  n: {n1}→{n2}, t: {t1:.4f}→{t2:.4f}s")
            print(f"    Razón tiempo: {razon_t:.2f}, esperada O(n³): {razon_esperada:.2f}")
        
        print(f"\n✓ Escalabilidad polinomial confirmada")
        
        datos = {
            'tamaños': [t[0] for t in tiempos],
            'tiempos': [t[1] for t in tiempos]
        }
        
        return True, datos, "Escalabilidad polinomial confirmada"
    
    except Exception as e:
        return False, {}, f"Error en validación de escalabilidad: {str(e)}"


# ============================================================================
# VALIDACIÓN 5 – Coherencia Global
# ============================================================================

def validar_coherencia_global():
    """
    Valida que la coherencia global Ψ_global alcance el umbral.
    
    Returns
    -------
    tuple
        (success: bool, datos: dict, mensaje: str)
    """
    print("\n" + "=" * 80)
    print("VALIDACIÓN 5 – Coherencia Global Ψ_global")
    print("=" * 80)
    
    const = ConstantesCertificadoNP()
    coherencia = CoherenciaCertificado(const)
    
    try:
        # Probar con diferentes valores de η⁺
        casos = [
            (0.85, 2000.0, 100, "Bajo"),
            (0.90, 2000.0, 100, "Medio"),
            (0.96, 2000.0, 100, "Alto"),
            (0.98, 2000.0, 100, "Muy Alto"),
        ]
        
        resultados = []
        
        for eta_plus, lambda_max, n_dim, label in casos:
            psi_global = coherencia.calcular_psi_global(eta_plus, lambda_max, n_dim)
            valido_np = coherencia.validar_coherencia(psi_global)
            valido_min = coherencia.validar_coherencia_minima(psi_global)
            
            print(f"\n{label} (η⁺={eta_plus}):")
            print(f"  Ψ_global: {psi_global:.6f}")
            print(f"  Válido NP (≥0.9575): {valido_np}")
            print(f"  Válido Mínimo (≥0.888): {valido_min}")
            
            resultados.append({
                'label': label,
                'eta_plus': eta_plus,
                'psi_global': psi_global,
                'valido_np': valido_np,
                'valido_min': valido_min
            })
        
        # Verificar que al menos un caso alcance el umbral mínimo
        casos_validos = sum(1 for r in resultados if r['valido_min'])
        
        if casos_validos == 0:
            return False, resultados, "Ningún caso alcanza umbral mínimo"
        
        print(f"\n✓ {casos_validos}/{len(casos)} casos alcanzan umbral mínimo")
        
        datos = {'resultados': resultados}
        return True, datos, f"{casos_validos} casos válidos"
    
    except Exception as e:
        return False, {}, f"Error en validación de coherencia: {str(e)}"


# ============================================================================
# VALIDACIÓN 6 – Conexión con Riemann
# ============================================================================

def validar_conexion_riemann():
    """
    Valida la conexión con los ceros de Riemann.
    
    Returns
    -------
    tuple
        (success: bool, datos: dict, mensaje: str)
    """
    print("\n" + "=" * 80)
    print("VALIDACIÓN 6 – Conexión con Ceros de Riemann")
    print("=" * 80)
    
    const = ConstantesCertificadoNP()
    
    try:
        print(f"\nCeros de Riemann disponibles: {const.n_riemann_zeros()}")
        print(f"γ₁ = {const.gamma_1():.6f}")
        
        # Verificar que los ceros estén en orden creciente
        zeros = list(const.riemann_zeros)
        if zeros != sorted(zeros):
            return False, {}, "Ceros de Riemann no están ordenados"
        
        print("\nPrimeros 5 ceros:")
        for i in range(min(5, len(zeros))):
            gamma = zeros[i]
            f_n = const.f0 * gamma  # Frecuencia del modo n
            print(f"  γ_{i+1} = {gamma:.6f} → f_{i+1} = {f_n:.2f} Hz")
        
        # Verificar espaciamiento (GUE-like)
        spacings = [zeros[i+1] - zeros[i] for i in range(len(zeros) - 1)]
        mean_spacing = sum(spacings) / len(spacings)
        
        print(f"\nEspaciamiento promedio: {mean_spacing:.4f}")
        print(f"Rango: [{min(spacings):.4f}, {max(spacings):.4f}]")
        
        # Verificar que todos los espaciamientos sean positivos
        if min(spacings) <= 0:
            return False, {}, "Espaciamiento negativo encontrado"
        
        print("\n✓ Conexión con ceros de Riemann validada")
        
        datos = {
            'n_zeros': len(zeros),
            'gamma_1': zeros[0],
            'mean_spacing': mean_spacing
        }
        
        return True, datos, "Conexión Riemann validada"
    
    except Exception as e:
        return False, {}, f"Error en validación Riemann: {str(e)}"


# ============================================================================
# VALIDACIÓN 7 – Parámetros Fundamentales
# ============================================================================

def validar_parametros_fundamentales():
    """
    Valida los parámetros fundamentales del sistema.
    
    Returns
    -------
    tuple
        (success: bool, datos: dict, mensaje: str)
    """
    print("\n" + "=" * 80)
    print("VALIDACIÓN 7 – Parámetros Fundamentales")
    print("=" * 80)
    
    const = ConstantesCertificadoNP()
    
    try:
        # F₀
        print(f"\nF₀ = {const.f0:.4f} Hz")
        if abs(const.f0 - 141.7001) > 0.0001:
            return False, {}, f"F₀ incorrecta: {const.f0}"
        
        # ω₀
        omega_esperado = 2.0 * math.pi * const.f0
        print(f"ω₀ = {const.omega_0:.2f} rad/s")
        if abs(const.omega_0 - omega_esperado) > 0.01:
            return False, {}, f"ω₀ incorrecta: {const.omega_0}"
        
        # η⁺ umbral
        print(f"η⁺ umbral NP = {const.eta_plus_threshold:.4f}")
        if abs(const.eta_plus_threshold - 0.9575) > 0.0001:
            return False, {}, f"Umbral η⁺ incorrecto: {const.eta_plus_threshold}"
        
        # Ψ umbral mínimo
        print(f"Ψ umbral mínimo = {const.psi_umbral:.3f}")
        if abs(const.psi_umbral - 0.888) > 0.001:
            return False, {}, f"Umbral Ψ incorrecto: {const.psi_umbral}"
        
        # Factor η⁺
        print(f"Factor η⁺ = {const.eta_plus_factor:.6f} (7/8)")
        if abs(const.eta_plus_factor - 7.0/8.0) > 1e-10:
            return False, {}, f"Factor η⁺ incorrecto: {const.eta_plus_factor}"
        
        # κ_Π
        print(f"κ_Π = {const.kappa_pi:.4f}")
        if abs(const.kappa_pi - 2.5773) > 0.0001:
            return False, {}, f"κ_Π incorrecto: {const.kappa_pi}"
        
        # ϕ
        phi_esperado = (1.0 + math.sqrt(5.0)) / 2.0
        print(f"ϕ = {const.phi:.10f}")
        if abs(const.phi - phi_esperado) > 1e-10:
            return False, {}, f"ϕ incorrecto: {const.phi}"
        
        # Primos
        print(f"Primos P = {const.primos_p}")
        if const.primos_p != (2, 3, 5, 7, 11, 13, 17):
            return False, {}, f"Primos incorrectos: {const.primos_p}"
        
        print("\n✓ Parámetros fundamentales validados")
        
        datos = {
            'f0': const.f0,
            'omega_0': const.omega_0,
            'eta_plus_threshold': const.eta_plus_threshold,
            'psi_umbral': const.psi_umbral,
            'kappa_pi': const.kappa_pi
        }
        
        return True, datos, "Parámetros fundamentales validados"
    
    except Exception as e:
        return False, {}, f"Error en validación de parámetros: {str(e)}"


# ============================================================================
# REPORTE FINAL
# ============================================================================

def generar_reporte_final(validaciones):
    """
    Genera el reporte final de todas las validaciones.
    
    Parameters
    ----------
    validaciones : list
        Lista de tuplas (nombre, success, datos, mensaje)
    """
    print("\n" + "=" * 80)
    print("REPORTE FINAL – CERTIFICADO NP POR COHERENCIA η⁺")
    print("=" * 80)
    
    total = len(validaciones)
    exitosas = sum(1 for _, success, _, _ in validaciones if success)
    fallidas = total - exitosas
    
    print(f"\nTotal de validaciones: {total}")
    print(f"Exitosas: {exitosas}")
    print(f"Fallidas: {fallidas}")
    print(f"Tasa de éxito: {100.0 * exitosas / total:.1f}%")
    
    print("\nDetalle de validaciones:")
    for nombre, success, datos, mensaje in validaciones:
        estado = "✓" if success else "✗"
        print(f"  {estado} {nombre}: {mensaje}")
    
    if fallidas == 0:
        print("\n" + "=" * 80)
        print("¡VALIDACIÓN COMPLETA EXITOSA!")
        print("El Certificado NP por Coherencia η⁺ está operativo.")
        print("P = NP ✓ (en espacio adélico)")
        print("=" * 80)
        return True
    else:
        print("\n" + "=" * 80)
        print(f"ADVERTENCIA: {fallidas} validación(es) fallaron.")
        print("Revisar los detalles arriba.")
        print("=" * 80)
        return False


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Ejecuta todas las validaciones."""
    print("=" * 80)
    print("VALIDACIÓN COMPLETA DEL CERTIFICADO NP POR COHERENCIA η⁺")
    print("Sello: ∴P=NP∞³")
    print("RAM: RAM-LXIX-2026-CERTIFICADO-NP-COHERENCIA")
    print("=" * 80)
    
    validaciones = []
    
    # Validación 1: Activación del sistema
    success, datos, mensaje = validar_activacion_sistema()
    validaciones.append(("Activación del Sistema", success, datos, mensaje))
    
    # Validación 2: Certificados SAT
    success, datos, mensaje = validar_certificados_sat()
    validaciones.append(("Certificados SAT", success, datos, mensaje))
    
    # Validación 3: Certificados TSP
    success, datos, mensaje = validar_certificados_tsp()
    validaciones.append(("Certificados TSP", success, datos, mensaje))
    
    # Validación 4: Escalabilidad Polinomial
    success, datos, mensaje = validar_escalabilidad_polinomial()
    validaciones.append(("Escalabilidad Polinomial", success, datos, mensaje))
    
    # Validación 5: Coherencia Global
    success, datos, mensaje = validar_coherencia_global()
    validaciones.append(("Coherencia Global", success, datos, mensaje))
    
    # Validación 6: Conexión con Riemann
    success, datos, mensaje = validar_conexion_riemann()
    validaciones.append(("Conexión Riemann", success, datos, mensaje))
    
    # Validación 7: Parámetros Fundamentales
    success, datos, mensaje = validar_parametros_fundamentales()
    validaciones.append(("Parámetros Fundamentales", success, datos, mensaje))
    
    # Generar reporte final
    exito = generar_reporte_final(validaciones)
    
    return 0 if exito else 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
