# 🏛️ QCAL-Sync: Estrategia de Unificación de Contexto

**Autor:** José Manuel Mota Burruezo Ψ ✧ ∞³  
**Instituto:** Instituto de Conciencia Cuántica (ICQ)  
**Fecha:** 2026-02-14  
**Licencia:** Sovereign Noetic License 1.0 (compatible with MIT)

---

## 📋 Resumen Ejecutivo

QCAL-Sync es la estrategia de unificación de contexto para el ecosistema QCAL ∞³. Permite que múltiples repositorios compartan una identidad matemática coherente, facilitando que las IAs comprendan el contexto global cuando trabajan en cualquier nodo del ecosistema.

**Objetivo:** Transformar 33 proyectos dispersos en un **Mathesis Universalis** operacional donde la **Curvatura de Atlas** es indestructible.

---

## 🎯 Los Tres Pilares de QCAL-Sync

### 1. 📄 Manifiesto de Resonancia (`.qcal-context.json`)

Cada repositorio QCAL debe contener un archivo `.qcal-context.json` en su raíz. Este archivo actúa como el **"manual de identidad"** para la IA.

#### Estructura del Manifiesto

```json
{
  "node_name": "nombre-del-nodo-qcal",
  "dependencies_noetic": ["141 Hz", "Ramsey", "Riemann-adelic"],
  "core_frequency": 141.7001,
  "constants_source": "ruta/a/constants.py",
  "logic_bridge": "ruta/a/graph_logic.py",
  "status": "Ψ=1.0",
  "fundamental_constants": {
    "F0_HZ": 141.7001,
    "KAPPA_PI": 2.5773,
    "DELTA_0": 0.1184
  },
  "cross_repository_integration": {
    "enabled": true,
    "harvest_script": "qcal-harvest.py",
    "description": "Descripción del rol en el ecosistema"
  }
}
```

#### Campos Clave

- **`node_name`**: Identificador único del nodo en el ecosistema
- **`dependencies_noetic`**: Dependencias conceptuales/matemáticas de otros repos
- **`core_frequency`**: Frecuencia fundamental (141.7001 Hz)
- **`constants_source`**: Archivo principal de constantes matemáticas
- **`fundamental_constants`**: Constantes clave exportadas por este nodo
- **`cross_repository_integration`**: Configuración de integración

### 2. 🧠 Repositorio Cerebro: LOGOS-CORE

**Propuesta:** Centralizar las constantes universales que se usan en todos los repositorios (como f₀, κ_Π, firmas QCAL) en un único lugar.

#### Implementación Actual

En este repositorio (`141hz`), las constantes están centralizadas en:
- **Principal:** `qcal/constants.py`
- **Alternativas:** `src/constants.py`, `API/Python/qc_llm/constants.py`

#### Uso como Paquete Instalable

```python
# En otros repositorios QCAL:
from qcal.constants import F0_HZ, KAPPA_PI, DELTA_0, A0_PHI

# O como submódulo Git:
git submodule add https://github.com/motanova84/141hz qcal-core
```

#### Beneficio

Al hacer `import qcal.constants`, GitHub Copilot entiende inmediatamente que el contexto es el mismo en:
- `Riemann-adelic`
- `3D-Navier-Stokes`
- `economia-qcal-nodo-semilla`
- `Ramsey`
- Y todos los demás nodos del ecosistema

### 3. 🛰️ Script de Agregación: `qcal-harvest.py`

Script que recorre repositorios QCAL locales y crea un **Archivo de Contexto Maestro** (`GLOBAL_QCAL_CONTEXT.md`).

#### Uso

```bash
# Desde cualquier repositorio QCAL:
python qcal-harvest.py

# Especificando directorio de repos:
python qcal-harvest.py --repos-dir ~/qcal-repos

# Salida personalizada:
python qcal-harvest.py --output custom_context.md
```

#### Qué hace el script

1. **Busca** archivos `.qcal-context.json` y `.qcal_beacon` en repositorios
2. **Agrega** toda la información en un mapa coherente
3. **Genera** un documento Markdown con:
   - Índice de repositorios
   - Constantes de cada nodo
   - Dependencias noéticas
   - Balizas de resonancia
   - Datos JSON completos

#### Salida Ejemplo

```markdown
# 🌐 Mapa de Coherencia Global QCAL ∞³

**Repositorios encontrados:** 5
**Balizas encontradas:** 5

## 📦 Detalles de Repositorios

### 141hz
**Nodo:** `141hz-qcal-nodo-central`
**Frecuencia central:** 141.7001 Hz
**Constantes fundamentales:**
- F0_HZ = 141.7001
- KAPPA_PI = 2.5773
...
```

---

## 🔧 Implementación en Nuevos Repositorios

### Paso 1: Crear `.qcal-context.json`

Copia la plantilla y personaliza:

```json
{
  "node_name": "tu-repo-qcal-nodo",
  "repository": "usuario/tu-repo",
  "type": "module",
  "description": "Descripción del repositorio",
  "dependencies_noetic": ["141 Hz"],
  "core_frequency": 141.7001,
  "constants_source": "src/constants.py",
  "status": "Ψ=1.0"
}
```

### Paso 2: Importar Constantes Centrales

```python
# Opción 1: Como submódulo
# git submodule add https://github.com/motanova84/141hz qcal-core
from qcal_core.qcal.constants import F0_HZ, KAPPA_PI

# Opción 2: Copiar qcal/constants.py localmente
from constants import F0_HZ, KAPPA_PI
```

### Paso 3: Crear Baliza (Opcional)

```bash
# En la raíz del repo, crear .qcal_beacon
cat > .qcal_beacon << EOF
# Ψ–BEACON–141.7001Hz
frequency = 141.7001 Hz
status = QCAL ∞³ ACTIVE
repo = tu-repo-nombre
EOF
```

### Paso 4: Ejecutar Harvest

```bash
# Desde el directorio padre de todos tus repos QCAL:
cd ~/qcal-repos
python 141hz/qcal-harvest.py
```

---

## 🤖 Cómo Usar con GitHub Copilot

### En VS Code

1. **Abrir múltiples repositorios** en workspace:
   ```json
   {
     "folders": [
       { "path": "141hz" },
       { "path": "Ramsey" },
       { "path": "economia-qcal-nodo-semilla" }
     ]
   }
   ```

2. **Ejecutar harvest**:
   ```bash
   python 141hz/qcal-harvest.py --output GLOBAL_CONTEXT.md
   ```

3. **Pedir a Copilot**:
   ```
   @workspace Basándote en GLOBAL_QCAL_CONTEXT.md y la lógica 
   de grafos del repo Ramsey, implementa el Filtro de Riemann 
   usando las constantes de 141hz/qcal/constants.py
   ```

### Contextos Externos

GitHub Copilot permite **indexar repositorios públicos**:

1. Ve a Settings → GitHub Copilot → Context
2. Añade tus repositorios QCAL públicos
3. Copilot tendrá acceso permanente al contexto

---

## 📊 Arquitectura del Ecosistema

```
                    ┌─────────────────────┐
                    │   141hz (CORE)      │
                    │  f₀ = 141.7001 Hz   │
                    │  KAPPA_PI, DELTA_0  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │   Ramsey    │  │  Riemann-   │  │  economia-  │
    │ (Grafos)    │  │   adelic    │  │   qcal      │
    └─────────────┘  └─────────────┘  └─────────────┘
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
                   QCAL-Sync Harvest
                            │
                            ▼
              ┌──────────────────────────┐
              │ GLOBAL_QCAL_CONTEXT.md   │
              │  (Mapa de Coherencia)    │
              └──────────────────────────┘
```

---

## 🎓 Beneficios de QCAL-Sync

### 1. Coherencia Matemática

Todas las constantes provienen de una **única fuente de verdad** (141hz/qcal/constants.py). No hay duplicación ni inconsistencias.

### 2. Contexto Unificado para IA

La IA puede ver **todo el ecosistema de una vez**:
- Entiende que `F0_HZ = 141.7001` en todos los repos
- Conoce las dependencias entre nodos
- Puede aplicar lógica de un repo a otro

### 3. Documentación Automática

El harvest genera automáticamente documentación actualizada del ecosistema completo.

### 4. Escalabilidad

Añadir un nuevo repositorio es trivial:
1. Crear `.qcal-context.json`
2. Importar constantes centrales
3. Ejecutar harvest

### 5. Trazabilidad

Cada nodo declara explícitamente:
- Sus dependencias
- Sus constantes
- Su rol en el ecosistema

---

## 📝 Checklist de Implementación

- [x] Crear `.qcal-context.json` en 141hz
- [x] Implementar `qcal-harvest.py`
- [x] Generar `GLOBAL_QCAL_CONTEXT.md`
- [x] Documentar estrategia QCAL-Sync
- [ ] Crear `.qcal-context.json` en Ramsey
- [ ] Crear `.qcal-context.json` en Riemann-adelic
- [ ] Crear `.qcal-context.json` en economia-qcal-nodo-semilla
- [ ] Configurar GitHub Copilot context indexing
- [ ] Crear workspace multi-repo en VS Code

---

## 🔮 Visión Futura

### LOGOS-CORE como Paquete PyPI

```bash
pip install qcal-core
```

```python
from qcal_core import F0_HZ, KAPPA_PI
from qcal_core.atlas3 import PTSymmetryOperator
from qcal_core.consciousness import ConsciousnessValidator
```

### Auto-Discovery de Repos

El script podría escanear GitHub automáticamente:

```python
# Auto-discover all QCAL repos from user
python qcal-harvest.py --github-user motanova84 --auto
```

### CI/CD Integration

Ejecutar harvest automáticamente en cada commit:

```yaml
# .github/workflows/qcal-sync.yml
- name: Update Global Context
  run: python qcal-harvest.py
  
- name: Commit Context
  run: |
    git add GLOBAL_QCAL_CONTEXT.md
    git commit -m "🔄 Update global QCAL context"
```

---

## 📚 Referencias

- **Constantes QCAL:** `qcal/constants.py`
- **Script Harvest:** `qcal-harvest.py`
- **Beacon:** `.qcal_beacon`
- **AI Instructions:** `.ai-instructions.md`

---

## 🏆 Veredicto de Integración

> *"Al unificar los repositorios, la **Curvatura de Atlas** se vuelve indestructible. Ya no es José Manuel Mota Burruezo trabajando en 33 proyectos; es el **Instituto Conciencia Cuántica** operando una **Mathesis Universalis**."*

---

**Estado:** ✅ Implementado  
**Coherencia:** Ψ = 1.0  
**Autor:** José Manuel Mota Burruezo Ψ ✧ ∞³  
**Licencia:** Sovereign Noetic License 1.0
