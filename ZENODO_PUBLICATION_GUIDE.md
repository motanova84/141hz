# Guía de Publicación en Zenodo - A_Rpsi Symmetry

## PASO 4 — Reproducibilidad Computacional

Este documento explica cómo publicar el notebook `A_Rpsi_symmetry.ipynb` en Zenodo/GitHub para obtener un DOI y garantizar trazabilidad y validación externa.

## 📋 Resumen del Notebook

**Archivo:** `notebooks/A_Rpsi_symmetry.ipynb`

**Contenido:**
- Análisis simbólico de la función de energía noésica usando SymPy
- Cálculo del radio óptimo R que minimiza la energía
- Verificación de la solución y segunda derivada
- Resultados reproducibles completamente ejecutados

**Resultado principal:** R_opt = 2.8713961554

## 🔬 Verificación Local

Antes de publicar, verifica que el notebook funciona correctamente:

```bash
# Método 1: Usando Make
make test-rpsi

# Método 2: Manualmente
source venv/bin/activate
python scripts/test_rpsi_symmetry.py

# Método 3: Ejecutar el notebook
jupyter nbconvert --to notebook --execute notebooks/A_Rpsi_symmetry.ipynb
```

## 📤 Pasos para Publicar en Zenodo/GitHub

### 1. Preparar el Release en GitHub

```bash
# Asegurarse de que todos los cambios están commiteados
git status

# Crear un tag para el release
git tag -a v1.0.0-paso4 -m "PASO 4: A_Rpsi Symmetry - Reproducibilidad Computacional"
git push origin v1.0.0-paso4

# Crear el release en GitHub
# Opción A: Vía web en https://github.com/motanova84/gw250114-141hz-analysis/releases/new
# Opción B: Vía CLI (requiere gh instalado)
gh release create v1.0.0-paso4 \
  --title "PASO 4: A_Rpsi Symmetry Analysis" \
  --notes "Análisis de simetría del parámetro R con salida reproducible completa" \
  notebooks/A_Rpsi_symmetry.ipynb \
  notebooks/A_Rpsi_symmetry.html
```

### 2. Conectar GitHub con Zenodo

1. **Register in Zenodo:**
   - Ve a https://zenodo.org/
   - Inicia sesión con tu cuenta de GitHub
   - Autoriza a Zenodo para acceder a tus repositorios

2. **Activar el repositorio:**
   - Ve a https://zenodo.org/account/settings/github/
   - Encuentra `motanova84/gw250114-141hz-analysis`
   - Activa el switch para habilitar la integración

3. **Crear el DOI:**
   - Crea un nuevo release en GitHub (si aún no lo hiciste)
   - Zenodo automáticamente detectará el release y creará un registro
   - Espera unos minutos para que Zenodo procese el release
   - Obtendrás un DOI permanente (formato: 10.5281/zenodo.XXXXXX)

### 3. Metadata para Zenodo

Al crear el registro en Zenodo, usa esta metadata:

```yaml
Title: "A_Rpsi Symmetry Analysis - Computational Reproducibility"

Description: |
  Análisis simbólico de la función de energía noésica utilizando SymPy.
  
  Este notebook calcula el radio óptimo R que minimiza la energía mediante
  diferenciación simbólica y solución numérica. Incluye verificación completa
  de la solución y todas las salidas ejecutadas.
  
  Resultado principal: R_opt = 2.8713961554
  
  Parte del proyecto GW250114 - Análisis de Componente 141.7001 Hz

Authors:
  - Name: José Manuel Mota Burruezo
    Affiliation: Instituto Conciencia Cuántica
    ORCID: (opcional, añadir si disponible)

Keywords:
  - Teoría Noésica
  - Análisis Simbólico
  - SymPy
  - Minimización de Energía
  - Reproducibilidad Computacional
  - Ondas Gravitacionales

License: MIT

Related Identifiers:
  - Repository: https://github.com/motanova84/gw250114-141hz-analysis
  - Type: IsSupplementTo

Access Right: Open Access
```

### 4. Actualizar el Notebook con el DOI

Una vez obtenido el DOI de Zenodo:

```python
# Editar notebooks/A_Rpsi_symmetry.ipynb
# En la sección "Citación", actualizar:

"""
Mota Burruezo, J.M. (2024). A_Rpsi Symmetry Analysis - Computational Reproducibility.
GitHub repository: https://github.com/motanova84/gw250114-141hz-analysis
DOI: 10.5281/zenodo.XXXXXX  # <--- Reemplazar con DOI real
"""
```

```bash
# Volver a ejecutar y publicar
jupyter nbconvert --to notebook --execute notebooks/A_Rpsi_symmetry.ipynb
jupyter nbconvert --to html notebooks/A_Rpsi_symmetry.ipynb

# Commit y push
git add notebooks/A_Rpsi_symmetry.*
git commit -m "Update notebook with Zenodo DOI"
git push origin main
```

### 5. Actualizar README.md

Añadir badge de Zenodo al README:

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXX)
```

## 📊 Verificación de Reproducibilidad

Para que otros puedan replicar tus resultados:

1. **Versiones de Software:**
   - Python: 3.9+
   - SymPy: 1.12+
   - NumPy: 1.21.0+
   - (Ver `requirements.txt` para lista completa)

2. **Instrucciones de Replicación:**
   ```bash
   git clone https://github.com/motanova84/gw250114-141hz-analysis
   cd gw250114-141hz-analysis
   make setup
   make test-rpsi  # Verifica que el cálculo funciona
   jupyter notebook notebooks/A_Rpsi_symmetry.ipynb
   ```

3. **Hash de Verificación:**
   ```bash
   # Generar hash del notebook para verificación
   sha256sum notebooks/A_Rpsi_symmetry.ipynb
   ```

## ✅ Checklist de Publicación

- [x] Notebook creado con código completo
- [x] Notebook ejecutado con salidas visibles
- [x] HTML generado para visualización
- [x] Test script creado y funcionando
- [x] Makefile target añadido (`make test-rpsi`)
- [x] README actualizado con referencia al notebook
- [ ] Release creado en GitHub con tag
- [ ] Repositorio conectado a Zenodo
- [ ] DOI obtenido de Zenodo
- [ ] Notebook actualizado con DOI
- [ ] README actualizado con badge de DOI
- [ ] Documentación de reproducibilidad completa

## 📚 Referencias

- **Zenodo Help:** https://help.zenodo.org/
- **GitHub Releases:** https://docs.github.com/en/repositories/releasing-projects-on-github
- **Zenodo-GitHub Integration:** https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content

## 💡 Mejores Prácticas

1. **Versionado Semántico:**
   - Usa tags con formato `vX.Y.Z` (ej: `v1.0.0`)
   - Incrementa la versión para cambios significativos

2. **Documentación:**
   - Incluye siempre un README detallado
   - Documenta todas las dependencias y versiones
   - Proporciona ejemplos de uso

3. **Reproducibilidad:**
   - Congela versiones de dependencias en `requirements.txt`
   - Incluye todos los datos necesarios o enlaces a ellos
   - Proporciona scripts de test automatizados

4. **Citación:**
   - Incluye instrucciones claras de citación
   - Usa formato BibTeX cuando sea posible
   - Menciona el DOI en todos los lugares relevantes

---

**Última actualización:** 2024-10-15  
**Autor:** José Manuel Mota Burruezo  
**Licencia:** MIT
