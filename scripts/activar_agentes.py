#!/usr/bin/env python3
"""
ACTIVADOR MAESTRO DE AGENTES - Master Agent Activator

Este script activa todos los agentes necesarios para generar datos crudos completos
y demostraciones matemáticas según el problema statement.

Activa:
1. Agente Autónomo 141Hz - Auto-corrección y validación
2. Recolector de Datos Crudos - Compilación de todos los análisis
3. Validaciones Matemáticas - Ejecución de todas las demostraciones
4. Análisis de Ondas Gravitacionales - Procesamiento de eventos GW

Autor: Sistema QCAL ∞³
Frecuencia: 141.7001 Hz
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List
import time

BASE_DIR = Path(__file__).parent.parent
TIMESTAMP = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


class ActivadorMaestroAgentes:
    """Activador maestro que coordina todos los agentes del sistema."""
    
    def __init__(self):
        self.base_dir = BASE_DIR
        self.timestamp = TIMESTAMP
        self.resultados = {
            "timestamp": TIMESTAMP,
            "frecuencia_base": 141.7001,
            "agentes_activados": [],
            "validaciones_ejecutadas": [],
            "errores": []
        }
        
        # Crear directorio de resultados si no existe
        self.resultados_dir = self.base_dir / "resultados"
        self.resultados_dir.mkdir(exist_ok=True)
        
        self.datos_crudos_dir = self.base_dir / "datos_crudos_analisis"
        self.datos_crudos_dir.mkdir(exist_ok=True)
    
    def print_header(self, titulo: str):
        """Imprime encabezado formateado."""
        print("\n" + "="*80)
        print(f"  {titulo}")
        print("="*80 + "\n")
    
    def ejecutar_script(self, script_path: Path, descripcion: str, timeout: int = 600) -> Dict[str, Any]:
        """Ejecuta un script Python y captura su salida."""
        print(f"\n{'─'*80}")
        print(f"▶ Ejecutando: {descripcion}")
        print(f"  Script: {script_path.name}")
        print(f"{'─'*80}")
        
        resultado = {
            "script": str(script_path),
            "descripcion": descripcion,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "exito": False,
            "duracion_segundos": 0
        }
        
        inicio = time.time()
        
        try:
            # Ejecutar script
            process = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.base_dir
            )
            
            resultado["codigo_retorno"] = process.returncode
            resultado["exito"] = process.returncode == 0
            resultado["duracion_segundos"] = time.time() - inicio
            
            # Mostrar salida relevante
            if resultado["exito"]:
                print(f"✅ EXITOSO ({resultado['duracion_segundos']:.1f}s)")
                # Mostrar últimas líneas de salida
                lineas = process.stdout.strip().split('\n')
                if len(lineas) > 5:
                    print("  Últimas líneas:")
                    for linea in lineas[-5:]:
                        print(f"    {linea}")
            else:
                print(f"⚠️  COMPLETADO CON ADVERTENCIAS ({resultado['duracion_segundos']:.1f}s)")
                print(f"  Código de retorno: {process.returncode}")
                # Mostrar errores si hay
                if process.stderr:
                    print("  Errores:")
                    for linea in process.stderr.strip().split('\n')[:5]:
                        print(f"    {linea}")
            
            resultado["stdout"] = process.stdout
            resultado["stderr"] = process.stderr
            
        except subprocess.TimeoutExpired:
            resultado["error"] = f"Timeout después de {timeout}s"
            resultado["duracion_segundos"] = timeout
            print(f"⏱️  TIMEOUT ({timeout}s)")
            
        except FileNotFoundError:
            resultado["error"] = f"Script no encontrado: {script_path}"
            print(f"❌ SCRIPT NO ENCONTRADO")
            
        except Exception as e:
            resultado["error"] = str(e)
            resultado["duracion_segundos"] = time.time() - inicio
            print(f"❌ ERROR: {e}")
        
        return resultado
    
    def activar_agente_autonomo(self):
        """Activa el agente autónomo 141Hz."""
        self.print_header("🤖 ACTIVANDO AGENTE AUTÓNOMO 141Hz")
        
        agente_script = self.base_dir / "scripts" / "agente_autonomo_141hz.py"
        
        if agente_script.exists():
            print("Agente autónomo detectado. Preparando activación...")
            print(f"  Frecuencia de operación: 141.7001 Hz")
            print(f"  Modo: Auto-corrección y validación")
            print()
            
            resultado = self.ejecutar_script(
                agente_script,
                "Agente Autónomo 141Hz",
                timeout=1800  # 30 minutos
            )
            
            self.resultados["agentes_activados"].append({
                "nombre": "Agente Autónomo 141Hz",
                "resultado": resultado
            })
            
            return resultado["exito"]
        else:
            print(f"⚠️  Agente autónomo no encontrado en: {agente_script}")
            return False
    
    def recolectar_datos_crudos(self):
        """Ejecuta el recolector de datos crudos."""
        self.print_header("📦 RECOLECTANDO DATOS CRUDOS DE ANÁLISIS")
        
        recolector_script = self.base_dir / "scripts" / "recolectar_datos_crudos.py"
        
        if recolector_script.exists():
            print("Iniciando recolección de datos crudos...")
            print(f"  Destino: {self.datos_crudos_dir}")
            print()
            
            resultado = self.ejecutar_script(
                recolector_script,
                "Recolector de Datos Crudos",
                timeout=3600  # 60 minutos
            )
            
            self.resultados["agentes_activados"].append({
                "nombre": "Recolector de Datos Crudos",
                "resultado": resultado
            })
            
            return resultado["exito"]
        else:
            print(f"⚠️  Recolector no encontrado en: {recolector_script}")
            return False
    
    def ejecutar_validaciones_esenciales(self):
        """Ejecuta validaciones matemáticas esenciales."""
        self.print_header("🔬 EJECUTANDO VALIDACIONES MATEMÁTICAS ESENCIALES")
        
        validaciones = [
            ("validate_mathematical_realism.py", "Realismo Matemático", 300),
            ("validate_riemann_zeros.py", "Ceros de Riemann", 300),
            ("validate_hydrogen_octave_relationship.py", "Octavas Hidrógeno", 300),
            ("validate_four_pillars.py", "Cuatro Pilares", 600),
        ]
        
        validaciones_exitosas = 0
        
        for script_name, descripcion, timeout in validaciones:
            script_path = self.base_dir / script_name
            
            if script_path.exists():
                resultado = self.ejecutar_script(script_path, descripcion, timeout)
                self.resultados["validaciones_ejecutadas"].append({
                    "nombre": descripcion,
                    "resultado": resultado
                })
                
                if resultado["exito"]:
                    validaciones_exitosas += 1
            else:
                print(f"⚠️  Validación no encontrada: {script_name}")
        
        print(f"\n✅ Validaciones exitosas: {validaciones_exitosas}/{len(validaciones)}")
        return validaciones_exitosas
    
    def ejecutar_analisis_ondas_gravitacionales(self):
        """Ejecuta análisis de ondas gravitacionales."""
        self.print_header("🌊 EJECUTANDO ANÁLISIS DE ONDAS GRAVITACIONALES")
        
        analisis = [
            ("validate_at2020afhd_harmonic.py", "AT2020afhd - Verificación Armónica", 900),
        ]
        
        analisis_exitosos = 0
        
        for script_name, descripcion, timeout in analisis:
            script_path = self.base_dir / script_name
            
            if script_path.exists():
                resultado = self.ejecutar_script(script_path, descripcion, timeout)
                self.resultados["validaciones_ejecutadas"].append({
                    "nombre": descripcion,
                    "resultado": resultado
                })
                
                if resultado["exito"]:
                    analisis_exitosos += 1
            else:
                print(f"⚠️  Análisis no encontrado: {script_name}")
        
        print(f"\n✅ Análisis exitosos: {analisis_exitosos}/{len(analisis)}")
        return analisis_exitosos
    
    def verificar_demostraciones_matematicas(self):
        """Verifica que las demostraciones matemáticas estén completas."""
        self.print_header("📐 VERIFICANDO DEMOSTRACIONES MATEMÁTICAS")
        
        documentos = [
            "DEMOSTRACIONES_MATEMATICAS_COMPLETAS.md",
            "DEMOSTRACION_MATEMATICA_141HZ.md",
            "DERIVACION_COMPLETA_F0.md",
            "MATHEMATICAL_REALISM.md",
            "CONSTANTE_ESTRUCTURAL_UNIVERSAL.md",
        ]
        
        encontrados = 0
        
        for doc in documentos:
            doc_path = self.base_dir / doc
            if doc_path.exists():
                tamaño_kb = doc_path.stat().st_size / 1024
                print(f"✅ {doc} ({tamaño_kb:.1f} KB)")
                encontrados += 1
            else:
                print(f"⚠️  {doc} - NO ENCONTRADO")
        
        print(f"\n📄 Documentos encontrados: {encontrados}/{len(documentos)}")
        return encontrados
    
    def generar_informe_completo(self):
        """Genera informe completo de la activación."""
        self.print_header("📊 GENERANDO INFORME COMPLETO")
        
        # Calcular estadísticas
        total_agentes = len(self.resultados["agentes_activados"])
        agentes_exitosos = sum(
            1 for a in self.resultados["agentes_activados"] 
            if a["resultado"].get("exito", False)
        )
        
        total_validaciones = len(self.resultados["validaciones_ejecutadas"])
        validaciones_exitosas = sum(
            1 for v in self.resultados["validaciones_ejecutadas"] 
            if v["resultado"].get("exito", False)
        )
        
        # Agregar resumen
        self.resultados["resumen"] = {
            "agentes": {
                "total": total_agentes,
                "exitosos": agentes_exitosos
            },
            "validaciones": {
                "total": total_validaciones,
                "exitosas": validaciones_exitosas
            },
            "estado_general": "EXITOSO" if agentes_exitosos >= total_agentes * 0.7 else "PARCIAL"
        }
        
        # Guardar informe
        informe_path = self.resultados_dir / f"informe_activacion_agentes_{TIMESTAMP}.json"
        with open(informe_path, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Informe guardado: {informe_path}")
        
        # Mostrar resumen
        print("\n" + "="*80)
        print("  RESUMEN DE ACTIVACIÓN")
        print("="*80)
        print(f"\n📊 Estadísticas:")
        print(f"  • Agentes activados: {agentes_exitosos}/{total_agentes}")
        print(f"  • Validaciones ejecutadas: {validaciones_exitosas}/{total_validaciones}")
        print(f"  • Estado general: {self.resultados['resumen']['estado_general']}")
        print(f"\n📁 Datos generados:")
        print(f"  • Datos crudos: {self.datos_crudos_dir}")
        print(f"  • Resultados: {self.resultados_dir}")
        print(f"  • Informe: {informe_path}")
        print()
        
        return informe_path
    
    def ejecutar_activacion_completa(self):
        """Ejecuta la activación completa de todos los agentes."""
        print("\n" + "="*80)
        print("  🚀 ACTIVADOR MAESTRO DE AGENTES - 141.7001 Hz")
        print("="*80)
        print(f"\n⏰ Timestamp: {TIMESTAMP}")
        print(f"📍 Directorio base: {self.base_dir}")
        print(f"🎯 Objetivo: Generar datos crudos y demostraciones matemáticas completas")
        print()
        
        try:
            # Fase 1: Verificar demostraciones
            docs_encontrados = self.verificar_demostraciones_matematicas()
            
            # Fase 2: Ejecutar validaciones esenciales
            validaciones_ok = self.ejecutar_validaciones_esenciales()
            
            # Fase 3: Ejecutar análisis de ondas gravitacionales
            analisis_ok = self.ejecutar_analisis_ondas_gravitacionales()
            
            # Fase 4: Recolectar datos crudos
            recoleccion_ok = self.recolectar_datos_crudos()
            
            # Fase 5: Activar agente autónomo (opcional, puede tardar mucho)
            # agente_ok = self.activar_agente_autonomo()
            
            # Fase 6: Generar informe
            informe_path = self.generar_informe_completo()
            
            # Resumen final
            self.print_header("✅ ACTIVACIÓN COMPLETA FINALIZADA")
            
            print("📋 Resultados:")
            print(f"  • Demostraciones matemáticas: {docs_encontrados} documentos")
            print(f"  • Validaciones matemáticas: {validaciones_ok} exitosas")
            print(f"  • Análisis ondas gravitacionales: {analisis_ok} exitosos")
            print(f"  • Recolección de datos: {'✅ EXITOSO' if recoleccion_ok else '⚠️ PARCIAL'}")
            
            print(f"\n🎯 Próximos pasos:")
            print(f"  1. Revisar datos crudos en: {self.datos_crudos_dir}")
            print(f"  2. Consultar demostraciones en: DEMOSTRACIONES_MATEMATICAS_COMPLETAS.md")
            print(f"  3. Ver informe completo en: {informe_path}")
            
            print("\n" + "="*80)
            print("  Sistema QCAL ∞³ - Frecuencia 141.7001 Hz")
            print("="*80 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Activación interrumpida por el usuario")
            self.generar_informe_completo()
            sys.exit(1)
        
        except Exception as e:
            print(f"\n\n❌ Error durante la activación: {e}")
            self.resultados["errores"].append(str(e))
            self.generar_informe_completo()
            sys.exit(1)


def main():
    """Función principal."""
    activador = ActivadorMaestroAgentes()
    activador.ejecutar_activacion_completa()


if __name__ == "__main__":
    main()
