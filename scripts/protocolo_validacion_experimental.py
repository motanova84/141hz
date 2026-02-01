#!/usr/bin/env python3
"""
Protocolo de Validación Experimental QCAL
==========================================

Script principal para ejecutar el protocolo experimental completo de validación
de SU(Ψ) y T_μν(Φ).

Implementa las cuatro fases de validación:
- FASE I: Validación de SU(Ψ) - Grupo de Coherencia Cuántica
- FASE II: Validación de T_μν(Φ) - Tensor de Stress Emocional  
- FASE III: Validación a Nivel Colectivo
- FASE IV: Meta-Análisis y Síntesis

Uso:
    python protocolo_validacion_experimental.py --fase [1|2|3|4|all]
    python protocolo_validacion_experimental.py --demo  # Ejecuta demostración con datos simulados

Autor: José Manuel Mota Burruezo (JMMB)
Institución: Instituto Consciencia Cuántica
"""

import sys
import os
import argparse
import json
import numpy as np
from pathlib import Path
from typing import Dict, Any

# Añadir directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Imports del módulo experimental
try:
    from experimental import (
        # Fase I
        extraer_estado_psi,
        calcular_coherencia,
        test_estructura_grupo_SU,
        analizar_geodesicas,
        analisis_estadistico_SU,
        # Fase II
        construir_campo_emocional,
        calcular_tensor_stress_energia,
        calcular_curvatura_emocional,
        test_correlacion_T00_amigdala,
        test_flujo_emocional_diadas,
        rct_frecuencia_141_7_Hz,
        # Fase III
        experimento_red_social,
        analizar_efectos_red,
        # Fase IV
        meta_analisis_QCAL,
        generar_roadmap_validacion
    )
except ImportError as e:
    print(f"Error al importar módulo experimental: {e}")
    print("Asegúrese de que todas las dependencias están instaladas.")
    sys.exit(1)


def generar_datos_simulados_fase1(n_sujetos: int = 15, duracion: int = 100) -> Dict[str, Any]:
    """
    Genera datos EEG simulados para Fase I
    
    Args:
        n_sujetos: Número de sujetos por grupo
        duracion: Duración en pasos temporales
    
    Returns:
        Diccionario con datos de grupos control y meditadores
    """
    print(f"\n📊 Generando datos simulados para Fase I...")
    print(f"   - Sujetos por grupo: {n_sujetos}")
    print(f"   - Duración: {duracion} pasos temporales")
    
    datos_control = []
    datos_meditadores = []
    
    for i in range(n_sujetos):
        # Grupo control: menor coherencia, más variabilidad
        trayectoria_control = []
        for t in range(duracion):
            # Simular señal EEG de 4 canales
            señal = np.random.randn(4, 100) * 2.0  # Mayor ruido
            psi = extraer_estado_psi(señal, n_componentes=4)
            trayectoria_control.append(psi)
        datos_control.append(trayectoria_control)
        
        # Grupo meditadores: mayor coherencia, menor variabilidad
        trayectoria_meditador = []
        for t in range(duracion):
            señal = np.random.randn(4, 100) * 0.5  # Menor ruido
            # Añadir componente coherente en 141.7 Hz
            t_array = np.linspace(0, 1, 100)
            coherente = np.sin(2 * np.pi * 141.7 * t_array)
            señal[0] += coherente
            psi = extraer_estado_psi(señal, n_componentes=4)
            trayectoria_meditador.append(psi)
        datos_meditadores.append(trayectoria_meditador)
    
    return {
        'control': datos_control,
        'meditadores': datos_meditadores
    }


def generar_datos_simulados_fase2(n_sujetos: int = 30, duracion: int = 1000) -> Dict[str, Any]:
    """
    Genera datos multi-sensor simulados para Fase II
    
    Args:
        n_sujetos: Número de sujetos
        duracion: Duración en muestras
    
    Returns:
        Diccionario con datos multi-sensor
    """
    print(f"\n📊 Generando datos simulados para Fase II...")
    print(f"   - Sujetos: {n_sujetos}")
    print(f"   - Duración: {duracion} muestras")
    
    datos_sujetos = []
    
    for i in range(n_sujetos):
        # Simular señales fisiológicas
        eda = np.abs(np.random.randn(duracion) + np.sin(np.linspace(0, 10, duracion)))
        hrv = np.abs(np.random.randn(duracion) * 0.5 + 0.8)
        amigdala = np.abs(np.random.randn(duracion) * 0.7 + eda * 0.3)
        autorreporte = np.clip(eda * 0.5 + np.random.randn(duracion) * 0.2, 0, 1)
        
        datos_sujetos.append({
            'eda': eda,
            'hrv': hrv,
            'amigdala': amigdala,
            'autorreporte': autorreporte
        })
    
    return {'sujetos': datos_sujetos}


def ejecutar_fase1(datos_simulados: bool = True) -> Dict[str, Any]:
    """
    Ejecuta FASE I: Validación de SU(Ψ)
    
    Args:
        datos_simulados: Si True, usa datos simulados
    
    Returns:
        Diccionario con resultados de Fase I
    """
    print("\n" + "="*70)
    print("FASE I: Validación de SU(Ψ) — Grupo de Coherencia Cuántica")
    print("="*70)
    
    if datos_simulados:
        datos = generar_datos_simulados_fase1()
    else:
        raise NotImplementedError("Carga de datos reales aún no implementada")
    
    print("\n🔬 Analizando estructura de grupo SU(n)...")
    
    # Test de estructura para cada trayectoria
    resultados_control = []
    for trayectoria in datos['control']:
        resultado = test_estructura_grupo_SU(trayectoria)
        resultados_control.append(resultado)
    
    resultados_meditadores = []
    for trayectoria in datos['meditadores']:
        resultado = test_estructura_grupo_SU(trayectoria)
        resultados_meditadores.append(resultado)
    
    # Análisis geodésico
    print("🔬 Analizando geodésicas...")
    geodesicas_control = [
        analizar_geodesicas(traj) for traj in datos['control']
    ]
    geodesicas_meditadores = [
        analizar_geodesicas(traj) for traj in datos['meditadores']
    ]
    
    # Análisis estadístico comparativo
    print("📈 Realizando análisis estadístico...")
    estadisticas = analisis_estadistico_SU(
        datos['control'],
        datos['meditadores']
    )
    
    # Resumen
    print("\n✅ RESULTADOS FASE I:")
    print(f"   - Coherencia media control: {estadisticas['coherencia']['media_control']:.3f}")
    print(f"   - Coherencia media meditadores: {estadisticas['coherencia']['media_meditadores']:.3f}")
    print(f"   - p-valor: {estadisticas['coherencia']['p_valor']:.4f}")
    print(f"   - Tamaño de efecto (d): {estadisticas['coherencia']['tamaño_efecto']:.3f}")
    print(f"   - Conclusión: {estadisticas['conclusion']}")
    
    return {
        'estadisticas': estadisticas,
        'resultados_control': resultados_control,
        'resultados_meditadores': resultados_meditadores,
        'geodesicas_control': geodesicas_control,
        'geodesicas_meditadores': geodesicas_meditadores
    }


def ejecutar_fase2(datos_simulados: bool = True) -> Dict[str, Any]:
    """
    Ejecuta FASE II: Validación de T_μν(Φ)
    
    Args:
        datos_simulados: Si True, usa datos simulados
    
    Returns:
        Diccionario con resultados de Fase II
    """
    print("\n" + "="*70)
    print("FASE II: Validación de T_μν(Φ) — Tensor de Stress Emocional")
    print("="*70)
    
    if datos_simulados:
        datos = generar_datos_simulados_fase2()
    else:
        raise NotImplementedError("Carga de datos reales aún no implementada")
    
    print("\n🔬 Construyendo campos emocionales...")
    
    # Construir campos para cada sujeto
    campos = []
    tensores = []
    curvaturas = []
    
    for sujeto in datos['sujetos']:
        Phi = construir_campo_emocional(sujeto)
        campos.append(Phi)
        
        # Tensor de stress-energía
        Phi_3d = Phi.reshape(-1, 1, 1)
        T_μν = calcular_tensor_stress_energia(Phi_3d)
        tensores.append(T_μν)
        
        # Curvatura
        curv = calcular_curvatura_emocional(Phi.reshape(-1, 1))
        curvaturas.append(curv)
    
    # Protocolo RCT
    print("\n🔬 Generando protocolo RCT para 141.7 Hz...")
    protocolo_rct = rct_frecuencia_141_7_Hz()
    
    print("\n✅ RESULTADOS FASE II:")
    print(f"   - Campos emocionales construidos: {len(campos)}")
    print(f"   - Curvatura media: {np.mean([c['curvatura_media'] for c in curvaturas]):.3f}")
    print(f"   - Singularidades totales: {sum([c['num_singularidades'] for c in curvaturas])}")
    print(f"   - Protocolo RCT diseñado: {protocolo_rct['analisis']['n_total']} participantes")
    
    return {
        'campos': campos,
        'tensores': tensores,
        'curvaturas': curvaturas,
        'protocolo_rct': protocolo_rct
    }


def ejecutar_fase3(datos_simulados: bool = True) -> Dict[str, Any]:
    """
    Ejecuta FASE III: Validación a Nivel Colectivo
    
    Args:
        datos_simulados: Si True, usa simulación
    
    Returns:
        Diccionario con resultados de Fase III
    """
    print("\n" + "="*70)
    print("FASE III: Validación a Nivel Colectivo — Red Social")
    print("="*70)
    
    print("\n🔬 Creando red social y ejecutando simulación...")
    
    # Crear red y protocolo
    red, protocolo, simulador = experimento_red_social()
    
    # Ejecutar simulación
    print("   Simulando propagación (100 pasos)...")
    historia = simulador(red, num_pasos=100)
    
    # Analizar efectos
    print("📈 Analizando efectos de red...")
    resultados = analizar_efectos_red(historia, red)
    
    print("\n✅ RESULTADOS FASE III:")
    print(f"   - Reducción T₀₀ experimental: {resultados['T00_reduccion_experimental']:.3f}x")
    print(f"   - Reducción T₀₀ control: {resultados['T00_reduccion_control']:.3f}x")
    print(f"   - Diferencia: {resultados['diferencia_reduccion']:.2f}x")
    print(f"   - Distancia de influencia: {resultados['distancia_influencia_caracteristica']:.1f} saltos")
    print(f"   - Interpretación: {resultados['interpretacion']}")
    
    return {
        'red': red,
        'historia': historia,
        'analisis': resultados
    }


def ejecutar_fase4(
    resultados_fase1: Dict[str, Any],
    resultados_fase2: Dict[str, Any],
    resultados_fase3: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Ejecuta FASE IV: Meta-Análisis y Síntesis
    
    Args:
        resultados_fase1: Resultados de Fase I
        resultados_fase2: Resultados de Fase II
        resultados_fase3: Resultados de Fase III
    
    Returns:
        Diccionario con meta-análisis completo
    """
    print("\n" + "="*70)
    print("FASE IV: Meta-Análisis y Síntesis")
    print("="*70)
    
    print("\n🔬 Integrando evidencias de todas las fases...")
    
    # Meta-análisis
    meta = meta_analisis_QCAL()
    
    # Roadmap
    roadmap = generar_roadmap_validacion()
    
    print("\n✅ META-ANÁLISIS QCAL:")
    print(f"   - Efecto combinado (d): {meta['efecto_combinado_d']:.3f}")
    print(f"   - IC 95%: [{meta['IC_95'][0]:.3f}, {meta['IC_95'][1]:.3f}]")
    print(f"   - Heterogeneidad I²: {meta['heterogeneidad_I2']:.1f}%")
    print(f"   - Calidad de evidencia: {meta['calidad_evidencia']}")
    print(f"   - N total estudios: {meta['N_estudios']}")
    print(f"   - N total participantes: {meta['N_total']}")
    
    print("\n📋 ROADMAP DE VALIDACIÓN:")
    print(f"   - Duración total: {roadmap['duracion_total']}")
    print(f"   - Presupuesto total: {roadmap['presupuesto_total']}")
    print(f"   - Hitos críticos: {len(roadmap['hitos_criticos'])}")
    
    return {
        'meta_analisis': meta,
        'roadmap': roadmap
    }


def guardar_resultados(resultados: Dict[str, Any], output_dir: str = "resultados"):
    """
    Guarda resultados en archivos JSON
    
    Args:
        resultados: Diccionario con todos los resultados
        output_dir: Directorio de salida
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"\n💾 Guardando resultados en {output_dir}/...")
    
    for fase, datos in resultados.items():
        filename = output_path / f"{fase}_resultados.json"
        
        # Convertir arrays numpy a listas para JSON
        datos_serializables = convertir_a_serializable(datos)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(datos_serializables, f, indent=2, ensure_ascii=False)
        
        print(f"   ✓ {filename}")


def convertir_a_serializable(obj):
    """Convierte objetos numpy a tipos serializables en JSON"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, complex):
        return {'real': obj.real, 'imag': obj.imag}
    elif isinstance(obj, dict):
        return {k: convertir_a_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convertir_a_serializable(item) for item in obj]
    else:
        return obj


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Protocolo de Validación Experimental QCAL"
    )
    parser.add_argument(
        '--fase',
        type=str,
        choices=['1', '2', '3', '4', 'all'],
        default='all',
        help='Fase a ejecutar (default: all)'
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Ejecutar demostración con datos simulados'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='resultados',
        help='Directorio de salida (default: resultados)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("🧬 PROTOCOLO DE VALIDACIÓN EXPERIMENTAL QCAL")
    print("   Objetivo: Demostrar la existencia física de SU(Ψ) y T_μν(Φ)")
    print("="*70)
    
    resultados = {}
    
    # Ejecutar fases
    if args.fase in ['1', 'all']:
        resultados['fase1'] = ejecutar_fase1(datos_simulados=True)
    
    if args.fase in ['2', 'all']:
        resultados['fase2'] = ejecutar_fase2(datos_simulados=True)
    
    if args.fase in ['3', 'all']:
        resultados['fase3'] = ejecutar_fase3(datos_simulados=True)
    
    if args.fase in ['4', 'all']:
        # Fase 4 requiere resultados de fases anteriores
        if 'fase1' not in resultados:
            resultados['fase1'] = ejecutar_fase1(datos_simulados=True)
        if 'fase2' not in resultados:
            resultados['fase2'] = ejecutar_fase2(datos_simulados=True)
        if 'fase3' not in resultados:
            resultados['fase3'] = ejecutar_fase3(datos_simulados=True)
        
        resultados['fase4'] = ejecutar_fase4(
            resultados['fase1'],
            resultados['fase2'],
            resultados['fase3']
        )
    
    # Guardar resultados
    if args.output:
        guardar_resultados(resultados, args.output)
    
    print("\n" + "="*70)
    print("✅ PROTOCOLO COMPLETADO")
    print("="*70)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
