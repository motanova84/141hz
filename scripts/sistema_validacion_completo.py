#!/usr/bin/env python3
"""
Sistema de Validación Completo
Ejecuta todos los módulos de validación de manera integrada
"""
import json
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class SistemaValidacionCompleto:
    def __init__(self):
        self.modulos = [
            'caracterizacion_bayesiana',
            'busqueda_sistematica', 
            'optimizacion_snr',
            'validacion_estadistica',
            'evidencia_concluyente'
        ]
        self.resultados_consolidados = {}
    
    def ejecutar_validacion_completa(self):
        """Ejecuta todo el sistema de validación de manera secuencial"""
        print("🚀 INICIANDO SISTEMA COMPLETO DE VALIDACIÓN GW250114")
        print("=" * 70)
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Ejecutar módulos secuencialmente
        print("\n1️⃣ Módulo 1: CARACTERIZACIÓN BAYESIANA")
        print("-" * 70)
        resultado_bayes = self.ejecutar_caracterizacion_bayesiana()
        self.resultados_consolidados['caracterizacion_bayesiana'] = resultado_bayes
        
        print("\n2️⃣ Módulo 2: BÚSQUEDA SISTEMÁTICA GWTC-1")
        print("-" * 70)
        resultado_busqueda = self.ejecutar_busqueda_sistematica()
        self.resultados_consolidados['busqueda_sistematica'] = resultado_busqueda
        
        print("\n3️⃣ Módulo 3: OPTIMIZACIÓN SNR")
        print("-" * 70)
        resultado_snr = self.ejecutar_optimizacion_snr()
        self.resultados_consolidados['optimizacion_snr'] = resultado_snr
        
        print("\n4️⃣ Módulo 4: VALIDACIÓN ESTADÍSTICA")
        print("-" * 70)
        resultado_estadistica = self.ejecutar_validacion_estadistica()
        self.resultados_consolidados['validacion_estadistica'] = resultado_estadistica
        
        print("\n5️⃣ Módulo 5: EVIDENCIA CONCLUYENTE")
        print("-" * 70)
        resultado_evidencia = self.ejecutar_validacion_evidencia_concluyente()
        self.resultados_consolidados['evidencia_concluyente'] = resultado_evidencia
        
        # Generar reporte final
        self.generar_reporte_final()
        
        return self.resultados_consolidados
    
    def ejecutar_caracterizacion_bayesiana(self):
        """Ejecuta caracterización bayesiana"""
        try:
            from caracterizacion_bayesiana import CaracterizacionBayesiana, generar_datos_sinteticos_gw250114
            
            datos, fs, params = generar_datos_sinteticos_gw250114()
            bayes = CaracterizacionBayesiana()
            resultados = bayes.estimar_q_factor(datos, fs)
            
            return {
                'estado': 'completado',
                'q_factor': resultados.get('q_factor'),
                'q_std': resultados.get('q_std'),
                'frecuencia_detectada': resultados.get('frecuencia_detectada')
            }
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {
                'estado': 'error',
                'mensaje': str(e)
            }
    
    def ejecutar_busqueda_sistematica(self):
        """Ejecuta búsqueda sistemática en GWTC-1"""
        try:
            from busqueda_sistematica_gwtc1 import BusquedaSistematicaGWTC1
            
            buscador = BusquedaSistematicaGWTC1()
            resultados = buscador.ejecutar_busqueda_completa()
            
            return {
                'estado': 'completado',
                'eventos_analizados': len(set([r['evento'] for r in resultados])),
                'total_detecciones': len(resultados),
                'detecciones_significativas': len([r for r in resultados if r.get('snr', 0) > 5])
            }
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {
                'estado': 'error',
                'mensaje': str(e)
            }
    
    def ejecutar_optimizacion_snr(self):
        """Ejecuta optimización de SNR"""
        try:
            from optimizacion_snr_avanzada import demostracion_optimizacion_completa
            
            resultados = demostracion_optimizacion_completa()
            
            return {
                'estado': 'completado',
                'snr_original': resultados.get('snr_original'),
                'snr_optimizado': resultados.get('snr_optimizado'),
                'factor_mejora': resultados.get('factor_mejora')
            }
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {
                'estado': 'error',
                'mensaje': str(e)
            }
    
    def ejecutar_validacion_estadistica(self):
        """Ejecuta validación estadística avanzada"""
        try:
            from validacion_estadistica import ValidacionEstadisticaCompleta
            
            validador = ValidacionEstadisticaCompleta()
            resultados = validador.ejecutar_validacion_completa()
            
            # Extraer métricas clave
            return {
                'estado': 'completado',
                'p_value': resultados.get('test_significancia', {}).get('p_value'),
                'bayes_factor': resultados.get('bayes_factor', {}).get('bayes_factor'),
                'coherencia': resultados.get('coherencia', {}).get('coherencia_target'),
                'significativo': bool(resultados.get('test_significancia', {}).get('significativo', False)),
                'evidencia_fuerte': bool(resultados.get('bayes_factor', {}).get('evidencia_fuerte', False))
            }
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {
                'estado': 'error',
                'mensaje': str(e)
            }
    
    def ejecutar_validacion_evidencia_concluyente(self):
        """Ejecuta validación de evidencia concluyente"""
        try:
            from evidencia_concluyente import (
                validar_estructura_evidencia,
                listar_eventos_confirmados,
                metricas_estadisticas
            )
            
            # Ejecutar validación
            validacion = validar_estructura_evidencia()
            eventos = listar_eventos_confirmados()
            metricas = metricas_estadisticas
            
            return {
                'estado': 'completado',
                'valido': validacion['valido'],
                'eventos_confirmados': len(eventos),
                'eventos': eventos,
                'p_value_global': metricas['significancia_global']['p_value'],
                'bayes_factor_global': metricas['significancia_global']['log_bayes_factor'],
                'coherencia_multi_detector': metricas['coherencia_multi_detector']['tasa_coincidencia'],
                'snr_medio': metricas['snr_consolidado']['snr_medio_h1'],
                'error_relativo_medio': metricas['precision_frecuencial']['error_relativo_medio']
            }
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {
                'estado': 'error',
                'mensaje': str(e)
            }
    
    def generar_reporte_final(self):
        """Genera reporte final consolidado"""
        print("\n" + "=" * 70)
        print("🎯 INFORME FINAL DE VALIDACIÓN GW250114")
        print("=" * 70)
        
        informe = {
            'fecha_ejecucion': datetime.now().isoformat(),
            'sistema': 'Validación Proactiva GW250114',
            'frecuencia_objetivo': '141.7001 Hz',
            'modulos_ejecutados': self.modulos,
            'resultados': self.resultados_consolidados,
            'estado_general': 'COMPLETADO'
        }
        
        # Guardar informe en JSON
        output_dir = Path(__file__).parent.parent / 'results'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        informe_file = output_dir / 'informe_validacion_gw250114.json'
        
        with open(informe_file, 'w', encoding='utf-8') as f:
            json.dump(informe, f, indent=2, ensure_ascii=False)
        
        # Generar resumen en texto
        self._generar_resumen_texto(informe)
        
        print(f"\n✅ VALIDACIÓN COMPLETADA")
        print(f"📁 Informe JSON: {informe_file}")
        print(f"📄 Resumen TXT: {output_dir / 'resumen_validacion.txt'}")
        
        return informe
    
    def _generar_resumen_texto(self, informe):
        """Genera resumen en formato texto"""
        output_dir = Path(__file__).parent.parent / 'results'
        resumen_file = output_dir / 'resumen_validacion.txt'
        
        with open(resumen_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("RESUMEN DE VALIDACIÓN GW250114 - 141.7001 Hz\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Fecha de ejecución: {informe['fecha_ejecucion']}\n")
            f.write(f"Frecuencia objetivo: {informe['frecuencia_objetivo']}\n\n")
            
            f.write("MÓDULOS EJECUTADOS:\n")
            f.write("-" * 70 + "\n\n")
            
            # Caracterización Bayesiana
            bayes = informe['resultados'].get('caracterizacion_bayesiana', {})
            f.write("1. CARACTERIZACIÓN BAYESIANA\n")
            if bayes.get('estado') == 'completado':
                f.write(f"   ✅ Completado\n")
                f.write(f"   • Q-factor: {bayes.get('q_factor', 'N/A'):.2f} ± {bayes.get('q_std', 0):.2f}\n")
                f.write(f"   • Frecuencia: {bayes.get('frecuencia_detectada', 0):.4f} Hz\n")
            else:
                f.write(f"   ❌ Error: {bayes.get('mensaje', 'Desconocido')}\n")
            f.write("\n")
            
            # Búsqueda Sistemática
            busqueda = informe['resultados'].get('busqueda_sistematica', {})
            f.write("2. BÚSQUEDA SISTEMÁTICA GWTC-1\n")
            if busqueda.get('estado') == 'completado':
                f.write(f"   ✅ Completado\n")
                f.write(f"   • Eventos analizados: {busqueda.get('eventos_analizados', 0)}\n")
                f.write(f"   • Total detecciones: {busqueda.get('total_detecciones', 0)}\n")
                f.write(f"   • Detecciones significativas: {busqueda.get('detecciones_significativas', 0)}\n")
            else:
                f.write(f"   ❌ Error: {busqueda.get('mensaje', 'Desconocido')}\n")
            f.write("\n")
            
            # Optimización SNR
            snr = informe['resultados'].get('optimizacion_snr', {})
            f.write("3. OPTIMIZACIÓN SNR\n")
            if snr.get('estado') == 'completado':
                f.write(f"   ✅ Completado\n")
                f.write(f"   • SNR original: {snr.get('snr_original', 0):.2f}\n")
                f.write(f"   • SNR optimizado: {snr.get('snr_optimizado', 0):.2f}\n")
                f.write(f"   • Factor de mejora: {snr.get('factor_mejora', 1):.2f}x\n")
            else:
                f.write(f"   ❌ Error: {snr.get('mensaje', 'Desconocido')}\n")
            f.write("\n")
            
            # Validación Estadística
            estadistica = informe['resultados'].get('validacion_estadistica', {})
            f.write("4. VALIDACIÓN ESTADÍSTICA\n")
            if estadistica.get('estado') == 'completado':
                f.write(f"   ✅ Completado\n")
                if estadistica.get('p_value') is not None:
                    f.write(f"   • p-value: {estadistica.get('p_value'):.6f}\n")
                if estadistica.get('bayes_factor') is not None:
                    f.write(f"   • Bayes Factor: {estadistica.get('bayes_factor'):.2f}\n")
                if estadistica.get('coherencia') is not None:
                    f.write(f"   • Coherencia: {estadistica.get('coherencia'):.3f}\n")
            else:
                f.write(f"   ❌ Error: {estadistica.get('mensaje', 'Desconocido')}\n")
            f.write("\n")
            
            # Evidencia Concluyente
            evidencia = informe['resultados'].get('evidencia_concluyente', {})
            f.write("5. EVIDENCIA CONCLUYENTE\n")
            if evidencia.get('estado') == 'completado':
                f.write(f"   ✅ Completado\n")
                f.write(f"   • Eventos confirmados: {evidencia.get('eventos_confirmados', 0)}\n")
                f.write(f"   • p-value global: {evidencia.get('p_value_global', 0):.2e}\n")
                f.write(f"   • Bayes Factor global: {evidencia.get('bayes_factor_global', 0):.1f}\n")
                f.write(f"   • Coherencia multi-detector: {evidencia.get('coherencia_multi_detector', 0):.1%}\n")
                f.write(f"   • SNR medio H1: {evidencia.get('snr_medio', 0):.2f}\n")
                f.write(f"   • Error relativo medio: {evidencia.get('error_relativo_medio', 0):.3f}%\n")
                if evidencia.get('eventos'):
                    f.write(f"   • Eventos: {', '.join(evidencia.get('eventos', []))}\n")
            else:
                f.write(f"   ❌ Error: {evidencia.get('mensaje', 'Desconocido')}\n")
            f.write("\n")
            
            f.write("=" * 70 + "\n")
            f.write("ESTADO GENERAL: " + informe['estado_general'] + "\n")
            f.write("=" * 70 + "\n")

# EJECUCIÓN PRINCIPAL
if __name__ == "__main__":
    print("🌌 SISTEMA DE VALIDACIÓN COMPLETO GW250114")
    print("Implementación de validación proactiva avanzada")
    print("=" * 70)
    
    try:
        sistema = SistemaValidacionCompleto()
        resultados = sistema.ejecutar_validacion_completa()
        
        print("\n" + "=" * 70)
        print("🎉 SISTEMA DE VALIDACIÓN EJECUTADO EXITOSAMENTE")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error en sistema de validación: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
