#!/usr/bin/env python3
"""
RECOLECTOR MAESTRO DE DATOS CRUDOS - Master Raw Data Collector

Este script ejecuta todas las validaciones matemáticas y análisis de ondas gravitacionales,
recopilando los datos crudos en un directorio centralizado para facilitar el acceso y análisis.

Genera:
- Datos crudos de todas las validaciones matemáticas
- Resultados de análisis de ondas gravitacionales (GW150914, AT2020afhd, etc.)
- Demostraciones matemáticas completas
- Manifiesto JSON con inventario completo de datos

Autor: Sistema QCAL ∞³
Frecuencia: 141.7001 Hz
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
import shutil

# Configuración
BASE_DIR = Path(__file__).parent.parent
DATOS_CRUDOS_DIR = BASE_DIR / "datos_crudos_analisis"
TIMESTAMP = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


class RecolectorDatosCrudos:
    """Recolector maestro de todos los datos crudos de análisis."""
    
    def __init__(self):
        self.datos_crudos_dir = DATOS_CRUDOS_DIR
        self.resultados = {
            "timestamp": TIMESTAMP,
            "frecuencia_base": 141.7001,
            "validaciones_matematicas": {},
            "analisis_ondas_gravitacionales": {},
            "demostraciones_completas": {},
            "errores": []
        }
        
        # Crear directorio principal
        self.datos_crudos_dir.mkdir(exist_ok=True)
        
        # Crear subdirectorios
        (self.datos_crudos_dir / "matematicas").mkdir(exist_ok=True)
        (self.datos_crudos_dir / "ondas_gravitacionales").mkdir(exist_ok=True)
        (self.datos_crudos_dir / "demostraciones").mkdir(exist_ok=True)
        (self.datos_crudos_dir / "visualizaciones").mkdir(exist_ok=True)
    
    def ejecutar_script(self, script_path: Path, descripcion: str, timeout: int = 600) -> Dict[str, Any]:
        """Ejecuta un script y captura su salida."""
        print(f"\n{'='*80}")
        print(f"Ejecutando: {descripcion}")
        print(f"Script: {script_path}")
        print(f"{'='*80}\n")
        
        resultado = {
            "script": str(script_path),
            "descripcion": descripcion,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "exito": False,
            "salida": "",
            "error": ""
        }
        
        try:
            # Ejecutar el script
            process = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=BASE_DIR
            )
            
            resultado["salida"] = process.stdout
            resultado["error"] = process.stderr
            resultado["codigo_retorno"] = process.returncode
            resultado["exito"] = process.returncode == 0
            
            if resultado["exito"]:
                print(f"✅ {descripcion} - EXITOSO")
            else:
                print(f"⚠️  {descripcion} - COMPLETADO CON ADVERTENCIAS")
                print(f"   Código de retorno: {process.returncode}")
            
        except subprocess.TimeoutExpired:
            resultado["error"] = f"Timeout después de {timeout} segundos"
            print(f"⏱️  {descripcion} - TIMEOUT")
            
        except Exception as e:
            resultado["error"] = str(e)
            print(f"❌ {descripcion} - ERROR: {e}")
        
        return resultado
    
    def copiar_archivos_resultados(self, origen: Path, destino: Path, patron: str = "*"):
        """Copia archivos de resultados al directorio de datos crudos."""
        if not origen.exists():
            return
        
        destino.mkdir(exist_ok=True, parents=True)
        
        for archivo in origen.glob(patron):
            if archivo.is_file():
                try:
                    shutil.copy2(archivo, destino / archivo.name)
                    print(f"  📁 Copiado: {archivo.name}")
                except Exception as e:
                    print(f"  ⚠️  Error copiando {archivo.name}: {e}")
    
    def recolectar_validaciones_matematicas(self):
        """Ejecuta y recolecta validaciones matemáticas."""
        print("\n" + "="*80)
        print("🔬 VALIDACIONES MATEMÁTICAS")
        print("="*80)
        
        validaciones = [
            ("validate_mathematical_realism.py", "Realismo Matemático"),
            ("validate_riemann_zeros.py", "Ceros de Riemann"),
            ("validate_hydrogen_octave_relationship.py", "Relación Octavas Hidrógeno"),
            ("validate_four_pillars.py", "Cuatro Pilares"),
            ("verify_kappa.py", "Verificación Kappa"),
            ("formalizacion_teorema_qcal_pi.py", "Formalización Teorema QCAL-π"),
            ("pozo_infinito_cuantico.py", "Pozo Infinito Cuántico"),
        ]
        
        for script, desc in validaciones:
            script_path = BASE_DIR / script
            if script_path.exists():
                resultado = self.ejecutar_script(script_path, desc, timeout=600)
                self.resultados["validaciones_matematicas"][desc] = resultado
            else:
                print(f"⚠️  Script no encontrado: {script}")
        
        # Copiar resultados
        self.copiar_archivos_resultados(
            BASE_DIR / "results",
            self.datos_crudos_dir / "matematicas",
            "*.json"
        )
        self.copiar_archivos_resultados(
            BASE_DIR / "results",
            self.datos_crudos_dir / "visualizaciones",
            "*.png"
        )
    
    def recolectar_analisis_ondas_gravitacionales(self):
        """Ejecuta y recolecta análisis de ondas gravitacionales."""
        print("\n" + "="*80)
        print("🌊 ANÁLISIS DE ONDAS GRAVITACIONALES")
        print("="*80)
        
        analisis = [
            ("validate_at2020afhd.py", "AT2020afhd - Análisis TDE"),
            ("validate_at2020afhd_harmonic.py", "AT2020afhd - Verificación Armónica"),
            ("validate_at2020afhd_periodicity.py", "AT2020afhd - Periodicidad"),
            ("AT2020afhd_Real_Data_Analysis.py", "AT2020afhd - Análisis de Datos Reales"),
            ("validate_riemann_ringdown_gw250114.py", "GW250114 - Ringdown Riemann"),
        ]
        
        for script, desc in analisis:
            script_path = BASE_DIR / script
            if script_path.exists():
                resultado = self.ejecutar_script(script_path, desc, timeout=900)
                self.resultados["analisis_ondas_gravitacionales"][desc] = resultado
            else:
                print(f"⚠️  Script no encontrado: {script}")
        
        # Copiar resultados de AT2020afhd
        self.copiar_archivos_resultados(
            BASE_DIR / "results" / "at2020afhd",
            self.datos_crudos_dir / "ondas_gravitacionales" / "at2020afhd"
        )
        
        # Copiar archivos de resultados generales
        for patron in ["at2020afhd*.json", "at2020afhd*.png", "*gw250114*.json"]:
            self.copiar_archivos_resultados(
                BASE_DIR,
                self.datos_crudos_dir / "ondas_gravitacionales",
                patron
            )
    
    def recolectar_demostraciones_matematicas(self):
        """Recolecta y ejecuta demostraciones matemáticas completas."""
        print("\n" + "="*80)
        print("📐 DEMOSTRACIONES MATEMÁTICAS COMPLETAS")
        print("="*80)
        
        # Buscar script de demostración matemática si existe
        demo_script = BASE_DIR / "scripts" / "demostracion_matematica_141hz.py"
        if demo_script.exists():
            resultado = self.ejecutar_script(
                demo_script, 
                "Demostración Matemática 141Hz",
                timeout=600
            )
            self.resultados["demostraciones_completas"]["demo_141hz"] = resultado
        
        # Copiar documentos de demostración
        documentos_demo = [
            "DEMOSTRACION_MATEMATICA_141HZ.md",
            "DEMOSTRACION_RIGUROSA_ECUACION_GENERADORA_UNIVERSAL_141_7001_HZ.pdf",
            "DERIVACION_COMPLETA_F0.md",
            "DESCUBRIMIENTO_MATEMATICO_141_7001_HZ.md",
            "MATHEMATICAL_REALISM.md",
        ]
        
        for doc in documentos_demo:
            doc_path = BASE_DIR / doc
            if doc_path.exists():
                try:
                    shutil.copy2(doc_path, self.datos_crudos_dir / "demostraciones")
                    print(f"  📄 Copiado: {doc}")
                except Exception as e:
                    print(f"  ⚠️  Error copiando {doc}: {e}")
    
    def generar_manifiesto(self):
        """Genera manifiesto JSON con inventario completo de datos."""
        print("\n" + "="*80)
        print("📋 GENERANDO MANIFIESTO DE DATOS CRUDOS")
        print("="*80)
        
        # Inventariar archivos generados
        inventario = {
            "matematicas": [],
            "ondas_gravitacionales": [],
            "demostraciones": [],
            "visualizaciones": []
        }
        
        for categoria in inventario.keys():
            categoria_dir = self.datos_crudos_dir / categoria
            if categoria_dir.exists():
                for archivo in categoria_dir.rglob("*"):
                    if archivo.is_file():
                        inventario[categoria].append({
                            "archivo": str(archivo.relative_to(self.datos_crudos_dir)),
                            "tamaño_bytes": archivo.stat().st_size,
                            "modificado": datetime.fromtimestamp(
                                archivo.stat().st_mtime, 
                                tz=timezone.utc
                            ).isoformat()
                        })
        
        self.resultados["inventario_archivos"] = inventario
        
        # Guardar manifiesto
        manifiesto_path = self.datos_crudos_dir / "MANIFIESTO_DATOS_CRUDOS.json"
        with open(manifiesto_path, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Manifiesto guardado: {manifiesto_path}")
        
        # Generar README
        self.generar_readme()
    
    def generar_readme(self):
        """Genera README explicativo del directorio de datos crudos."""
        readme_content = f"""# Datos Crudos de Análisis - 141.7001 Hz

**Generado:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}  
**Frecuencia Base:** 141.7001 Hz  
**Sistema:** QCAL ∞³

## 📁 Estructura de Directorios

```
datos_crudos_analisis/
├── matematicas/                 # Resultados de validaciones matemáticas
├── ondas_gravitacionales/       # Análisis de eventos GW
├── demostraciones/              # Documentos de demostraciones matemáticas
├── visualizaciones/             # Gráficos y figuras
├── MANIFIESTO_DATOS_CRUDOS.json # Inventario completo
└── README.md                    # Este archivo
```

## 🔬 Validaciones Matemáticas Incluidas

- **Realismo Matemático**: Validación de la frecuencia 141.7001 Hz como constante estructural
- **Ceros de Riemann**: Relación entre función Zeta y f₀
- **Relación Octavas Hidrógeno**: 23.257 octavas desde línea 21cm
- **Cuatro Pilares**: Validación de pilares fundamentales de la teoría
- **Verificación Kappa**: Constante topológica κ
- **Formalización QCAL-π**: Teorema principal formalizado
- **Pozo Infinito Cuántico**: Solución cuántica del pozo de potencial

## 🌊 Análisis de Ondas Gravitacionales

- **AT2020afhd**: Análisis completo del TDE (Tidal Disruption Event)
  - Verificación armónica
  - Análisis de periodicidad
  - Datos reales de precesión Lense-Thirring
- **GW250114**: Análisis de ringdown y nodo Riemann

## 📐 Demostraciones Matemáticas

- Demostración rigurosa de la ecuación generadora universal
- Derivación completa de f₀ desde primeros principios
- Descubrimiento matemático de 141.7001 Hz
- Fundamentos de realismo matemático

## 📊 Uso de los Datos

Todos los archivos JSON pueden ser leídos con:

```python
import json

with open('MANIFIESTO_DATOS_CRUDOS.json') as f:
    datos = json.load(f)
```

Las visualizaciones están en formato PNG de alta resolución.

## 🔗 Referencias

- **CONSTANTE_ESTRUCTURAL_UNIVERSAL.md**: Evidencia consolidada
- **EVIDENCIA_CONSOLIDADA_141HZ.md**: Evidencia experimental
- **VERIFICACION_REQUISITOS.md**: Verificación de requisitos del proyecto

## 📝 Nota sobre Reproducibilidad

Todos los análisis son completamente reproducibles ejecutando:

```bash
python scripts/recolectar_datos_crudos.py
```

---

**"El universo no es un modelo; es su propia demostración."**  
*Sistema QCAL ∞³ - Frecuencia 141.7001 Hz*
"""
        
        readme_path = self.datos_crudos_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ README generado: {readme_path}")
    
    def ejecutar_recoleccion_completa(self):
        """Ejecuta la recolección completa de datos crudos."""
        print("\n" + "="*80)
        print("🚀 INICIANDO RECOLECCIÓN DE DATOS CRUDOS")
        print("="*80)
        print(f"Directorio de salida: {self.datos_crudos_dir}")
        print(f"Timestamp: {TIMESTAMP}")
        print()
        
        # Ejecutar cada fase
        self.recolectar_validaciones_matematicas()
        self.recolectar_analisis_ondas_gravitacionales()
        self.recolectar_demostraciones_matematicas()
        
        # Generar manifiesto
        self.generar_manifiesto()
        
        # Resumen final
        print("\n" + "="*80)
        print("✅ RECOLECCIÓN COMPLETA")
        print("="*80)
        print(f"\n📁 Datos guardados en: {self.datos_crudos_dir}")
        print(f"📋 Manifiesto: {self.datos_crudos_dir / 'MANIFIESTO_DATOS_CRUDOS.json'}")
        print(f"📄 README: {self.datos_crudos_dir / 'README.md'}")
        
        # Estadísticas
        total_validaciones = len(self.resultados["validaciones_matematicas"])
        validaciones_exitosas = sum(
            1 for v in self.resultados["validaciones_matematicas"].values() 
            if v.get("exito", False)
        )
        
        total_analisis = len(self.resultados["analisis_ondas_gravitacionales"])
        analisis_exitosos = sum(
            1 for a in self.resultados["analisis_ondas_gravitacionales"].values() 
            if a.get("exito", False)
        )
        
        print(f"\n📊 Estadísticas:")
        print(f"  - Validaciones matemáticas: {validaciones_exitosas}/{total_validaciones} exitosas")
        print(f"  - Análisis ondas gravitacionales: {analisis_exitosos}/{total_analisis} exitosos")
        
        print("\n" + "="*80)


def main():
    """Función principal."""
    recolector = RecolectorDatosCrudos()
    recolector.ejecutar_recoleccion_completa()


if __name__ == "__main__":
    main()
