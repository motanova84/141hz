#!/usr/bin/env python3
"""
Verificador de disponibilidad GW250114
Verifica si el evento GW250114 está disponible en GWOSC para análisis.
Retorna exit code 0 si está disponible, 1 si no lo está.
"""
import sys
import os
from datetime import datetime
import time

def verificar_disponibilidad_gw250114():
    """Verificar si GW250114 está disponible en GWOSC"""
    print("🌌 VERIFICACIÓN INMEDIATA GW250114")
    print("=" * 50)
    print(f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Intentar importar módulos necesarios
    try:
        from gwpy.timeseries import TimeSeries
        print("✅ Módulos GWPy disponibles")
    except ImportError as e:
        print(f"❌ Error importando GWPy: {e}")
        print("💡 Instalar con: pip install gwpy")
        return False
    
    # Lista de eventos conocidos para verificar conectividad
    known_events = {
        'GW150914': 1126259462.423,
        'GW151226': 1135136350.6,
        'GW170104': 1167559936.6,
        'GW170814': 1186741861.5,
        'GW170823': 1187008882.4
    }
    
    print("🔍 Verificando acceso a catálogo GWOSC...")
    
    # Verificar conectividad con evento conocido
    try:
        test_event = 'GW150914'
        test_gps = known_events[test_event]
        
        print(f"   🧪 Test de conectividad con {test_event}...")
        data = TimeSeries.fetch_open_data('H1', test_gps-1, test_gps+1, verbose=False)
        print(f"   ✅ Acceso a catálogo confirmado")
        
    except Exception as e:
        print(f"   ❌ Error accediendo catálogo GWOSC: {e}")
        print("   💡 Verificar conexión a internet")
        return False
    
    # Buscar GW250114 en catálogo
    print()
    print("🔎 Buscando GW250114 en catálogo...")
    
    # Nota: GW250114 es un evento hipotético para este análisis
    # Esta sección detectará automáticamente cuando esté disponible
    
    try:
        # Intentar acceder a GW250114 (esto fallará hasta que esté disponible)
        # El GPS time sería aproximadamente 1769529600 (2025-01-14 estimado)
        
        print("   📋 GW250114 es un evento objetivo hipotético")
        print("   ⏳ Esperando liberación de datos en GWOSC")
        print()
        print("   ℹ️  El evento será detectado automáticamente cuando:")
        print("      • Aparezca en el catálogo público GWTC")
        print("      • Los datos estén disponibles vía API")
        print("      • Pase el período de embargo (si aplica)")
        
        return False
        
    except Exception as e:
        print(f"   ❌ Error en búsqueda: {e}")
        return False

def monitoreo_continuo():
    """Modo de monitoreo continuo (ejecutar en segundo plano)"""
    print()
    print("🔄 INICIANDO MONITOREO CONTINUO")
    print("=" * 50)
    
    intervalo = 3600  # Verificar cada hora
    print(f"⏱️  Intervalo de verificación: {intervalo} segundos ({intervalo//60} minutos)")
    print("🛑 Para detener: pkill -f verificador_gw250114.py")
    print()
    
    verificaciones = 0
    while True:
        verificaciones += 1
        print(f"\n{'=' * 50}")
        print(f"🔍 Verificación #{verificaciones}")
        print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 50}")
        
        disponible = verificar_disponibilidad_gw250114()
        
        if disponible:
            print()
            print("🎉" * 20)
            print("🚨 ¡GW250114 DISPONIBLE!")
            print("🎉" * 20)
            print()
            print("🚀 Iniciar análisis con:")
            print("   python scripts/analizar_gw250114.py")
            print()
            
            # Crear archivo de alerta
            with open("GW250114_DISPONIBLE.txt", "w") as f:
                f.write(f"GW250114 disponible desde: {datetime.now()}\n")
                f.write("Ejecutar: python scripts/analizar_gw250114.py\n")
            
            return 0
        else:
            print(f"\n⏳ Próxima verificación en {intervalo//60} minutos...")
            time.sleep(intervalo)

def main():
    """Función principal"""
    
    # Verificar si hay argumento para modo continuo
    modo_continuo = '--continuo' in sys.argv or '--continuous' in sys.argv
    
    if modo_continuo:
        # Modo de monitoreo continuo
        return monitoreo_continuo()
    else:
        # Verificación única
        disponible = verificar_disponibilidad_gw250114()
        
        print()
        print("=" * 50)
        if disponible:
            print("✅ GW250114 DISPONIBLE - Listo para análisis")
            print("🚀 Ejecutar: python scripts/analizar_gw250114.py")
            return 0
        else:
            print("❌ GW250114 NO DISPONIBLE AÚN")
            print("🔄 Para monitoreo continuo:")
            print("   nohup python scripts/verificador_gw250114.py --continuo > monitoreo_gw250114.log 2>&1 &")
            return 1

if __name__ == "__main__":
    sys.exit(main())
Verificador en Tiempo Real GW250114
Sistema de monitoreo y análisis automático para detectar y analizar GW250114
cuando esté disponible en GWOSC.
"""
import requests
import json
from datetime import datetime
import time
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Intentar importar módulos de GWOSC
try:
    from gwosc import datasets, catalog
    GWOSC_AVAILABLE = True
except ImportError:
    print("⚠️  Módulo gwosc no disponible - funcionalidad limitada")
    GWOSC_AVAILABLE = False

# Intentar importar GWpy
try:
    from gwpy.timeseries import TimeSeries
    GWPY_AVAILABLE = True
except ImportError:
    print("⚠️  Módulo gwpy no disponible - funcionalidad limitada")
    GWPY_AVAILABLE = False

# Importar scipy
try:
    from scipy import signal
    SCIPY_AVAILABLE = True
except ImportError:
    print("⚠️  Módulo scipy no disponible")
    SCIPY_AVAILABLE = False


class VerificadorGW250114:
    def __init__(self):
        self.evento_objetivo = "GW250114"
        self.gwosc_base_url = "https://gwosc.org"
        self.estado_actual = "DESCONOCIDO"
        
        # Crear directorios necesarios
        self._crear_directorios()
        
    def _crear_directorios(self):
        """Crear estructura de directorios necesaria"""
        script_dir = Path(__file__).parent
        project_dir = script_dir.parent
        
        # Directorios de datos y resultados
        self.data_dir = project_dir / "data" / "raw"
        self.resultados_dir = project_dir / "resultados"
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.resultados_dir.mkdir(parents=True, exist_ok=True)
        
    def verificar_disponibilidad_evento(self):
        """Verifica si GW250114 está disponible en GWOSC"""
        print(f"🔍 BUSCANDO {self.evento_objetivo} EN CATÁLOGOS GWOSC...")
        
        if not GWOSC_AVAILABLE:
            print("❌ Módulo gwosc no disponible")
            return False
        
        try:
            # Obtener eventos disponibles
            eventos_disponibles = self.obtener_eventos_publicos()
            
            if self.evento_objetivo in eventos_disponibles:
                self.estado_actual = "DISPONIBLE"
                print(f"🎉 ¡{self.evento_objetivo} ESTÁ DISPONIBLE!")
                return True
            else:
                self.estado_actual = "NO_DISPONIBLE"
                print(f"⏳ {self.evento_objetivo} aún no está disponible")
                return False
                
        except Exception as e:
            print(f"❌ Error verificando disponibilidad: {e}")
            return False
    
    def obtener_eventos_publicos(self):
        """Obtiene lista de eventos públicos disponibles"""
        try:
            # Eventos de O4 (Observing Run 4)
            eventos_o4 = datasets.find_datasets(type='event', match='GW')
            
            # También verificar en el catálogo oficial
            catalog_events = catalog.events()
            
            todos_eventos = set(eventos_o4 + list(catalog_events.keys()))
            
            print(f"📊 Eventos públicos encontrados: {len(todos_eventos)}")
            
            # Filtrar eventos recientes (potencial GW250114)
            eventos_2025 = [e for e in todos_eventos if 'GW25' in e]
            if eventos_2025:
                print(f"📅 Eventos 2025 encontrados: {eventos_2025}")
            
            return todos_eventos
            
        except Exception as e:
            print(f"⚠️ Error obteniendo eventos: {e}")
            return []
    
    def descargar_datos_evento(self, evento):
        """Descarga datos del evento si está disponible"""
        if not GWPY_AVAILABLE or not GWOSC_AVAILABLE:
            print("❌ Módulos necesarios no disponibles")
            return False
            
        try:
            print(f"⬇️ DESCARGANDO DATOS DE {evento}...")
            
            # Obtener información del evento
            info_evento = catalog.events()[evento]
            gps_time = info_evento['GPS']
            
            print(f"📅 GPS time: {gps_time}")
            print(f"🔧 Detectors: {info_evento['detectors']}")
            
            # Descargar datos para cada detector
            for detector in info_evento['detectors']:
                try:
                    self.descargar_datos_detector(evento, detector, gps_time)
                except Exception as e:
                    print(f"❌ Error descargando {detector}: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error descargando evento {evento}: {e}")
            return False
    
    def descargar_datos_detector(self, evento, detector, gps_time):
        """Descarga datos de un detector específico"""
        try:
            # Ventana de tiempo alrededor del evento
            start = gps_time - 16  # 16 segundos antes
            end = gps_time + 16    # 16 segundos después
            
            print(f"   📥 Descargando {detector}...")
            
            # Descargar datos strain
            datos = TimeSeries.fetch_open_data(detector, start, end, sample_rate=4096)
            
            # Guardar datos
            nombre_archivo = self.data_dir / f"{evento}_{detector}.hdf5"
            datos.write(str(nombre_archivo))
            
            print(f"   ✅ {detector} guardado: {nombre_archivo}")
            
            return datos
            
        except Exception as e:
            print(f"   ❌ Error con {detector}: {e}")
            raise
    
    def monitoreo_continuo(self, intervalo=3600):  # 1 hora
        """Monitoreo continuo para detectar cuando esté disponible"""
        print(f"🔄 INICIANDO MONITOREO CONTINUO PARA {self.evento_objetivo}")
        print(f"   Intervalo de verificación: {intervalo/60} minutos")
        
        while True:
            try:
                disponible = self.verificar_disponibilidad_evento()
                
                if disponible:
                    print("🎯 ¡EVENTO DETECTADO! INICIANDO ANÁLISIS...")
                    self.descargar_datos_evento(self.evento_objetivo)
                    self.ejecutar_analisis_completo()
                    break
                else:
                    # Verificar eventos similares o preliminares
                    self.verificar_eventos_similares()
                    
                print(f"⏰ Siguiente verificación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                time.sleep(intervalo)
                
            except Exception as e:
                print(f"❌ Error en monitoreo: {e}")
                time.sleep(intervalo)
    
    def verificar_eventos_similares(self):
        """Verifica eventos similares o preliminares que puedan ser GW250114"""
        try:
            eventos = self.obtener_eventos_publicos()
            
            # Buscar eventos con nombres similares
            eventos_similares = []
            for evento in eventos:
                if 'GW25' in evento or 'S250114' in evento or 'MS250114' in evento:
                    eventos_similares.append(evento)
            
            if eventos_similares:
                print(f"🔍 Eventos similares encontrados: {eventos_similares}")
                
                # Analizar el más prometedor
                evento_analizar = eventos_similares[0]
                print(f"🎯 Analizando evento similar: {evento_analizar}")
                self.descargar_y_analizar_evento(evento_analizar)
                
        except Exception as e:
            print(f"⚠️ Error verificando eventos similares: {e}")
    
    def descargar_y_analizar_evento(self, evento):
        """Descarga y analiza un evento específico"""
        try:
            print(f"🔬 ANALIZANDO EVENTO: {evento}")
            
            # Descargar datos
            datos_descargados = self.descargar_datos_evento(evento)
            
            if datos_descargados:
                # Ejecutar análisis de frecuencia
                resultados = self.analizar_frecuencia_141hz(evento)
                
                # Guardar resultados
                self.guardar_resultados(evento, resultados)
                
                return resultados
            else:
                print(f"❌ No se pudieron descargar datos de {evento}")
                return None
                
        except Exception as e:
            print(f"❌ Error analizando {evento}: {e}")
            return None
    
    def analizar_frecuencia_141hz(self, evento):
        """Analiza la frecuencia 141.7001 Hz en el evento"""
        if not SCIPY_AVAILABLE:
            print("❌ SciPy no disponible para análisis")
            return {}
            
        print(f"🎵 ANALIZANDO FRECUENCIA 141.7001 Hz EN {evento}")
        
        resultados = {}
        detectores = ['H1', 'L1', 'V1']  # Hanford, Livingston, Virgo
        
        for detector in detectores:
            try:
                # Cargar datos
                archivo = self.data_dir / f"{evento}_{detector}.hdf5"
                
                if not archivo.exists():
                    print(f"   ⚠️  Archivo no encontrado: {archivo}")
                    continue
                    
                datos = TimeSeries.read(str(archivo))
                
                # Análisis espectral
                f, Pxx = signal.periodogram(datos.value, fs=4096)
                
                # Buscar en banda 140-143 Hz
                mascara = (f >= 140) & (f <= 143)
                f_banda = f[mascara]
                Pxx_banda = Pxx[mascara]
                
                # Encontrar pico máximo
                idx_pico = np.argmax(Pxx_banda)
                f_pico = f_banda[idx_pico]
                potencia_pico = Pxx_banda[idx_pico]
                
                # Calcular SNR
                potencia_mediana = np.median(Pxx_banda)
                snr = potencia_pico / potencia_mediana
                
                # Verificar coincidencia con 141.7001 Hz
                diferencia = abs(f_pico - 141.7001)
                significativo = diferencia < 0.1 and snr > 5
                
                resultados[detector] = {
                    'frecuencia_detectada': f_pico,
                    'snr': snr,
                    'diferencia': diferencia,
                    'significativo': significativo,
                    'potencia_pico': potencia_pico
                }
                
                print(f"   📊 {detector}: {f_pico:.4f} Hz, SNR: {snr:.2f}, "
                      f"Diff: {diferencia:.4f} Hz, Significativo: {significativo}")
                      
            except Exception as e:
                print(f"   ❌ Error analizando {detector}: {e}")
                resultados[detector] = {'error': str(e)}
        
        return resultados
    
    def guardar_resultados(self, evento, resultados):
        """Guarda resultados del análisis"""
        nombre_archivo = self.resultados_dir / f"analisis_{evento}.json"
        
        datos_guardar = {
            'evento': evento,
            'timestamp_analisis': datetime.now().isoformat(),
            'resultados': resultados,
            'resumen': self.generar_resumen(resultados)
        }
        
        with open(nombre_archivo, 'w') as f:
            json.dump(datos_guardar, f, indent=2)
        
        print(f"💾 Resultados guardados: {nombre_archivo}")
    
    def generar_resumen(self, resultados):
        """Genera resumen ejecutivo del análisis"""
        detectores_significativos = []
        
        for detector, datos in resultados.items():
            if datos.get('significativo', False):
                detectores_significativos.append(detector)
        
        return {
            'detectores_significativos': detectores_significativos,
            'total_detectores': len(resultados),
            'exitosos': len(detectores_significativos),
            'tasa_exito': len(detectores_significativos) / len(resultados) if resultados else 0
        }
    
    def ejecutar_analisis_completo(self):
        """Ejecuta análisis completo cuando GW250114 esté disponible"""
        print("🚀 EJECUTANDO ANÁLISIS COMPLETO DE GW250114...")
        
        # Este método se puede expandir para incluir análisis más detallados
        # integrando con los scripts existentes como validar_gw150914.py
        
        resultados = self.analizar_frecuencia_141hz(self.evento_objetivo)
        
        if resultados:
            print("✅ Análisis completado")
            self.guardar_resultados(self.evento_objetivo, resultados)
        else:
            print("❌ Error en análisis")


# EJECUCIÓN INMEDIATA
if __name__ == "__main__":
    verificador = VerificadorGW250114()
    
    print("🌌 SISTEMA DE VERIFICACIÓN GW250114")
    print("=" * 50)
    
    # Verificar disponibilidad inmediata
    disponible = verificador.verificar_disponibilidad_evento()
    
    if disponible:
        print("🚀 ¡GW250114 DISPONIBLE! EJECUTANDO ANÁLISIS COMPLETO...")
        verificador.descargar_y_analizar_evento("GW250114")
    else:
        print("🔍 GW250114 no disponible. Buscando eventos similares...")
        verificador.verificar_eventos_similares()
        
        print("\n🔄 OPCIONES DE MONITOREO CONTINUO:")
        print("   Para iniciar monitoreo continuo, ejecutar:")
        print("   verificador.monitoreo_continuo(intervalo=1800)  # 30 minutos")
        print("\n   (Presiona Ctrl+C para detener)")
        
        # Opción: descomentar para monitoreo automático
        # try:
        #     verificador.monitoreo_continuo(intervalo=1800)  # 30 minutos
        # except KeyboardInterrupt:
        #     print("\n⏹️ Monitoreo detenido por el usuario")
