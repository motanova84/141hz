#!/usr/bin/env python3
"""
Protocolo de Falsación para la Teoría Ψ
Sistema de criterios de refutación científica según el principio de falsabilidad de Popper
"""
from datetime import datetime
from typing import Dict, Any, List


class ProtocoloFalsacion:
    """
    Protocolo de Falsación científica para la teoría de resonancia noésica Ψ
    
    Define condiciones claras bajo las cuales la teoría sería refutada,
    siguiendo el principio de falsabilidad de Karl Popper.
    """
    
    def __init__(self):
        """Inicializar el protocolo con condiciones de refutación"""
        self.condiciones_refutacion = {
            'bi2se3': {
                'descripcion': 'Ausencia de pico en 141.7 ± 0.2 mV',
                'condicion': 'SNR < 3 en 10 muestras independientes',
                'significancia': 'p > 0.01 después de Bonferroni',
                'consecuencia': 'Refutación acoplamiento Ψ-materia'
            },
            'cmb': {
                'descripcion': 'Ausencia de anomalía en l = 144 ± 5',
                'condicion': 'Δχ² < 5 vs ΛCDM en Planck+Simons',
                'significancia': 'Bayes factor < 1',
                'consecuencia': 'Refutación proyección cosmológica Ψ'
            },
            'gw': {
                'descripcion': 'Ausencia de modulación en GWTC-3',
                'condicion': 'SNR < 5 en todos los eventos O4',
                'significancia': 'p > 0.001 con corrección múltiple', 
                'consecuencia': 'Refutación frecuencia fundamental f₀'
            }
        }
    
    def verificar_falsacion(self, resultados_experimentales: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifica si la teoría ha sido falsada según los resultados experimentales
        
        Args:
            resultados_experimentales: Diccionario con resultados de experimentos
                                      Claves esperadas: 'bi2se3', 'cmb', 'gw'
        
        Returns:
            Diccionario con:
                - teoria_falsada: bool indicando si la teoría ha sido refutada
                - razones: lista de razones de falsación
                - timestamp: fecha de evaluación
        """
        falsada = False
        razones = []
        
        for sistema, condicion in self.condiciones_refutacion.items():
            if sistema in resultados_experimentales:
                if self.evaluar_condicion(resultados_experimentales[sistema], condicion, sistema):
                    falsada = True
                    razones.append(f"Condición de {sistema} satisfecha")
        
        return {
            'teoria_falsada': falsada,
            'razones': razones,
            'timestamp': '2025-12-31'  # Fecha límite
        }
    
    def evaluar_condicion(self, resultado: Dict[str, Any], condicion: Dict[str, str], sistema: str) -> bool:
        """
        Evalúa si un resultado experimental satisface la condición de falsación
        
        Args:
            resultado: Diccionario con datos experimentales del sistema
            condicion: Condición de refutación para el sistema
            sistema: Nombre del sistema ('bi2se3', 'cmb', 'gw')
        
        Returns:
            True si la condición de falsación se cumple, False en caso contrario
        """
        # Evaluar según el sistema
        if sistema == 'bi2se3':
            return self._evaluar_bi2se3(resultado)
        elif sistema == 'cmb':
            return self._evaluar_cmb(resultado)
        elif sistema == 'gw':
            return self._evaluar_gw(resultado)
        
        return False
    
    def _evaluar_bi2se3(self, resultado: Dict[str, Any]) -> bool:
        """
        Evalúa condición de falsación para Bi2Se3
        
        Criterios:
        - SNR < 3 en múltiples muestras independientes
        - p-value > 0.01 después de corrección Bonferroni
        """
        snr = resultado.get('snr', float('inf'))
        p_value = resultado.get('p_value', 0.0)
        n_muestras = resultado.get('n_muestras_independientes', 0)
        
        # Condición de falsación: SNR bajo Y p-value alto
        snr_bajo = snr < 3.0
        p_value_alto = p_value > 0.01
        muestras_suficientes = n_muestras >= 10
        
        return snr_bajo and p_value_alto and muestras_suficientes
    
    def _evaluar_cmb(self, resultado: Dict[str, Any]) -> bool:
        """
        Evalúa condición de falsación para CMB
        
        Criterios:
        - Δχ² < 5 vs ΛCDM
        - Bayes factor < 1
        """
        delta_chi2 = resultado.get('delta_chi2', float('inf'))
        bayes_factor = resultado.get('bayes_factor', float('inf'))
        
        # Condición de falsación: mejora insignificante sobre ΛCDM
        chi2_bajo = delta_chi2 < 5.0
        bf_bajo = bayes_factor < 1.0
        
        return chi2_bajo and bf_bajo
    
    def _evaluar_gw(self, resultado: Dict[str, Any]) -> bool:
        """
        Evalúa condición de falsación para ondas gravitacionales
        
        Criterios:
        - SNR < 5 en todos los eventos
        - p-value > 0.001 con corrección por tests múltiples
        """
        snr = resultado.get('snr', float('inf'))
        p_value = resultado.get('p_value', 0.0)
        eventos_analizados = resultado.get('n_eventos', 0)
        
        # Condición de falsación: SNR bajo Y p-value alto
        snr_bajo = snr < 5.0
        p_value_alto = p_value > 0.001
        eventos_suficientes = eventos_analizados > 0
        
        return snr_bajo and p_value_alto and eventos_suficientes
    
    def generar_reporte_falsacion(self, resultados_experimentales: Dict[str, Any]) -> str:
        """
        Genera un reporte detallado del estado de falsación
        
        Args:
            resultados_experimentales: Resultados de los experimentos
        
        Returns:
            Reporte en formato de texto
        """
        verificacion = self.verificar_falsacion(resultados_experimentales)
        
        reporte = []
        reporte.append("=" * 70)
        reporte.append("PROTOCOLO DE FALSACIÓN - TEORÍA Ψ")
        reporte.append("=" * 70)
        reporte.append(f"Fecha de evaluación: {verificacion['timestamp']}")
        reporte.append("")
        
        reporte.append("CONDICIONES DE REFUTACIÓN:")
        reporte.append("")
        
        for sistema, condicion in self.condiciones_refutacion.items():
            reporte.append(f"📋 {sistema.upper()}:")
            reporte.append(f"   • Descripción: {condicion['descripcion']}")
            reporte.append(f"   • Condición: {condicion['condicion']}")
            reporte.append(f"   • Significancia: {condicion['significancia']}")
            reporte.append(f"   • Consecuencia: {condicion['consecuencia']}")
            
            if sistema in resultados_experimentales:
                resultado = resultados_experimentales[sistema]
                cumple = self.evaluar_condicion(resultado, condicion, sistema)
                estado = "✅ CUMPLIDA" if cumple else "❌ NO CUMPLIDA"
                reporte.append(f"   • Estado: {estado}")
            else:
                reporte.append(f"   • Estado: ⏳ PENDIENTE (sin datos)")
            
            reporte.append("")
        
        reporte.append("=" * 70)
        reporte.append("RESULTADO FINAL:")
        reporte.append("=" * 70)
        
        if verificacion['teoria_falsada']:
            reporte.append("🔴 TEORÍA FALSADA")
            reporte.append("")
            reporte.append("Razones:")
            for razon in verificacion['razones']:
                reporte.append(f"   • {razon}")
        else:
            reporte.append("🟢 TEORÍA NO FALSADA")
            reporte.append("")
            reporte.append("La teoría permanece consistente con los datos experimentales")
            reporte.append("disponibles hasta la fecha.")
        
        reporte.append("")
        reporte.append("=" * 70)
        
        return "\n".join(reporte)
    
    def obtener_criterios(self) -> Dict[str, Dict[str, str]]:
        """
        Obtiene las condiciones de refutación definidas
        
        Returns:
            Diccionario con las condiciones de refutación
        """
        return self.condiciones_refutacion.copy()


# Ejecución inmediata para demostración
if __name__ == "__main__":
    print("🔬 PROTOCOLO DE FALSACIÓN - TEORÍA Ψ")
    print("=" * 70)
    print("Demostración del sistema de falsación científica")
    print("=" * 70)
    
    # Crear instancia del protocolo
    protocolo = ProtocoloFalsacion()
    
    # Ejemplo 1: Teoría NO falsada (resultados favorables)
    print("\n📊 EJEMPLO 1: Resultados favorables a la teoría")
    print("-" * 70)
    
    resultados_favorables = {
        'bi2se3': {
            'snr': 8.5,
            'p_value': 0.001,
            'n_muestras_independientes': 10
        },
        'cmb': {
            'delta_chi2': 12.0,
            'bayes_factor': 15.0
        },
        'gw': {
            'snr': 15.2,
            'p_value': 0.0001,
            'n_eventos': 20
        }
    }
    
    reporte1 = protocolo.generar_reporte_falsacion(resultados_favorables)
    print(reporte1)
    
    # Ejemplo 2: Teoría FALSADA (resultados desfavorables)
    print("\n\n📊 EJEMPLO 2: Resultados desfavorables (teoría falsada)")
    print("-" * 70)
    
    resultados_desfavorables = {
        'bi2se3': {
            'snr': 2.0,  # SNR < 3
            'p_value': 0.05,  # p > 0.01
            'n_muestras_independientes': 10
        },
        'cmb': {
            'delta_chi2': 3.0,  # Δχ² < 5
            'bayes_factor': 0.5  # BF < 1
        },
        'gw': {
            'snr': 4.0,  # SNR < 5
            'p_value': 0.002,  # p > 0.001
            'n_eventos': 15
        }
    }
    
    reporte2 = protocolo.generar_reporte_falsacion(resultados_desfavorables)
    print(reporte2)
    
    # Ejemplo 3: Datos parciales
    print("\n\n📊 EJEMPLO 3: Datos parciales (solo algunos sistemas)")
    print("-" * 70)
    
    resultados_parciales = {
        'gw': {
            'snr': 15.2,
            'p_value': 0.0001,
            'n_eventos': 20
        }
    }
    
    reporte3 = protocolo.generar_reporte_falsacion(resultados_parciales)
    print(reporte3)
    
    print("\n✅ Demostración completada")
