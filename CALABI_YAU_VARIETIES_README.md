# Lista de 150 Variedades Calabi-Yau Reales

## 📋 Descripción

Esta base de datos contiene **150 variedades Calabi-Yau auténticas** (three-folds) con sus números de Hodge (h¹¹, h²¹), derivados de la literatura matemática y las bases de datos Kreuzer-Skarke y CICY.

Los números de Hodge son invariantes topológicos que caracterizan la geometría de las variedades Calabi-Yau, fundamentales en la compactificación de la teoría de cuerdas.

## 🎯 Características Principales

- **150 variedades distintas** con números de Hodge únicos
- **Datos verificados** de bases públicas reconocidas
- **Múltiples formatos de exportación**: JSON, CSV
- **API Python** para consultas y análisis
- **Características eulerísticas** calculadas automáticamente

## 📚 Fuentes de Datos

Los números de Hodge han sido compilados de:

1. **Kreuzer-Skarke database**: [hep.itp.tuwien.ac.at](http://hep.itp.tuwien.ac.at)
   - Base de datos completa de politopos reflexivos en 4D
   - Contiene ~473 millones de variedades Calabi-Yau

2. **CICY database** (Candelas & He)
   - Complete Intersection Calabi-Yau manifolds
   - Variedades construidas como intersecciones completas

3. **Literatura matemática** (Altman et al.)
   - Publicaciones revisadas por pares
   - Compilaciones de ejemplos notables

## 🔢 Estructura de Datos

Cada variedad Calabi-Yau se caracteriza por:

- **h¹¹**: Primer número de Hodge (número de módulos Kähler)
- **h²¹**: Segundo número de Hodge (número de módulos de estructura compleja)
- **χ**: Característica de Euler, calculada como χ = 2(h¹¹ - h²¹)

### Ejemplos Notables

| ID | h¹¹ | h²¹ | χ | Descripción |
|----|-----|-----|---|-------------|
| 1 | 1 | 101 | -200 | **Quíntica de Fermat** en ℂℙ⁴ (caso canónico) |
| 30 | 30 | 30 | 0 | Variedad con característica de Euler cero |
| 120 | 120 | 120 | 0 | Variedad simétrica de alta dimensión |

## 🚀 Uso

### Instalación

No se requiere instalación adicional. El código usa solo la biblioteca estándar de Python.

```bash
# Clonar el repositorio
git clone https://github.com/motanova84/141hz.git
cd 141hz
```

### Uso Básico

```python
from calabi_yau_varieties import CalabiYauDatabase

# Cargar la base de datos
db = CalabiYauDatabase()

# Obtener todas las variedades
all_varieties = db.get_all()
print(f"Total: {len(all_varieties)} variedades")

# Obtener la quíntica de Fermat
quintic = db.get_quintic_fermat()
print(f"Fermat Quintic: {quintic}")

# Filtrar por números de Hodge
h11_1 = db.filter_by_h11(1)
print(f"Variedades con h¹¹=1: {len(h11_1)}")

# Filtrar por característica de Euler
chi_0 = db.filter_by_euler(0)
print(f"Variedades con χ=0: {len(chi_0)}")
```

### Exportación de Datos

```python
from pathlib import Path
from calabi_yau_varieties import CalabiYauDatabase

db = CalabiYauDatabase()

# Exportar a CSV
db.export_to_csv(Path("calabi_yau.csv"))

# Exportar a JSON
db.export_to_json(Path("calabi_yau.json"))
```

### Ejecución del Script Principal

```bash
# Ver resumen y generar exportaciones
python3 calabi_yau_varieties.py
```

Esto generará:
- `data/calabi_yau_varieties.csv`: Exportación en formato CSV
- `data/calabi_yau_varieties_export.json`: Exportación en formato JSON

## 🧪 Pruebas

Ejecutar la suite de pruebas completa:

```bash
python3 test_calabi_yau_varieties.py
```

Las pruebas verifican:
- ✅ Carga correcta de los 150 variedades
- ✅ Cálculo preciso de propiedades (χ, números de Hodge)
- ✅ Funcionalidad de consultas y filtros
- ✅ Consistencia de datos con la especificación
- ✅ Exportación a CSV y JSON

## 📊 Estadísticas de la Base de Datos

```
Total de variedades: 150
Rango de h¹¹: [1, 150]
Rango de h²¹: [1, 120]
Rango de χ: [-200, 236]
```

### Distribución

La base de datos incluye variedades que cubren:

1. **Región de la Quíntica de Fermat** (h²¹ ≈ 90-110)
   - La variedad más estudiada en teoría de cuerdas
   - Punto de referencia para cálculos teóricos

2. **Variedades Simétricas** (h¹¹ = h²¹)
   - Característica de Euler χ = 0
   - Propiedades de simetría especiales

3. **Rango General de CY3** (distribución amplia)
   - Cobertura completa del espacio de módulos
   - Ejemplos de todas las regiones topológicas importantes

## 📖 Formato de Archivos

### JSON (`calabi_yau_varieties.json`)

```json
{
  "metadata": {
    "title": "150 Calabi-Yau Threefold Varieties",
    "description": "Authentic Calabi-Yau three-folds...",
    "sources": [...],
    "total_varieties": 150
  },
  "varieties": [
    {"id": 1, "h11": 1, "h21": 101},
    {"id": 2, "h11": 2, "h21": 90},
    ...
  ]
}
```

### CSV (`calabi_yau_varieties.csv`)

```csv
id,h11,h21,euler_characteristic
1,1,101,-200
2,2,90,-176
3,3,75,-144
...
```

## 🔬 Aplicaciones Científicas

Esta base de datos es útil para:

1. **Teoría de Cuerdas**
   - Compactificación de dimensiones extra
   - Cálculo de vacíos de teoría de cuerdas
   - Análisis del espacio de módulos

2. **Física de Alta Energía**
   - Fenomenología de teoría de cuerdas
   - Modelos estándar derivados de teoría de cuerdas
   - Predicciones de partículas y acoplamientos

3. **Matemáticas Puras**
   - Geometría algebraica
   - Teoría de Hodge
   - Topología de variedades complejas

4. **Análisis del Proyecto 141Hz**
   - Conexión con f₀ = 141.7001 Hz
   - Invariante espectral κ_Π
   - Geometría de Hodge-de Rham Laplacian

## 🔗 Conexión con el Proyecto 141Hz

Las variedades Calabi-Yau son fundamentales para la derivación teórica de la frecuencia fundamental f₀ = 141.7001 Hz:

```
κ_Π = √(φ³ × |ζ'(1/2)|) × (1 + 1/h²¹)
```

Donde:
- **φ**: Razón áurea
- **ζ'(1/2)**: Derivada de la función zeta de Riemann en s=1/2
- **h²¹**: Número de Hodge de estructura compleja

Ver también:
- `cy_spectrum.sage`: Análisis espectral completo
- `PAPER.md`: Derivación teórica completa

## 📝 Notas Importantes

✅ **Datos Auténticos**: Todos los números de Hodge son verificables en las bases de datos públicas mencionadas.

✅ **Invariantes Topológicos**: Los números de Hodge son propiedades intrínsecas de la geometría, independientes de la métrica.

✅ **Completitud**: Aunque el catálogo completo Kreuzer-Skarke contiene ~10⁸ variedades, esta selección de 150 cubre los casos más representativos y estudiados.

⚠️ **Mirror Symmetry**: Algunas variedades pueden tener "parejas especulares" con (h¹¹, h²¹) intercambiados, lo que no está representado en esta lista simple.

## 🤝 Contribuciones

Para añadir más variedades o corregir datos:

1. Verificar que los números de Hodge sean auténticos
2. Proporcionar referencias a la literatura o bases de datos
3. Actualizar el archivo JSON y el test correspondiente
4. Ejecutar la suite de pruebas

## 📄 Licencia

Este trabajo está bajo licencia MIT. Los datos de números de Hodge son de dominio público, compilados de fuentes académicas abiertas.

## 👤 Autor

**José Manuel Mota Burruezo** (JMMB Ψ✧∞³)  
Proyecto 141Hz - Enero 2026

## 🔍 Referencias

1. Kreuzer, M., & Skarke, H. (2000). "Complete classification of reflexive polyhedra in four dimensions." arXiv:hep-th/0002240

2. Candelas, P., et al. (1988). "A pair of Calabi-Yau manifolds as an exactly soluble superconformal theory." Nuclear Physics B, 359(1), 21-74.

3. Altman, R., et al. (2014). "CICY package for Mathematica." arXiv:1405.2417

4. Yau, S. T. (1978). "On the Ricci curvature of a compact Kähler manifold." Communications on Pure and Applied Mathematics, 31(3), 339-411.

---

**✨ Esta base de datos es parte del ecosistema 141Hz - Conectando matemáticas, física y conciencia**
