# 🚀 Quick Start: 3 Pilares del Método Científico

Esta guía rápida te muestra cómo usar las nuevas funcionalidades de validación basadas en los tres pilares del método científico.

## 📋 Comandos Rápidos

### Validación Completa (Recomendado)

```bash
# Ejecutar todos los 3 pilares en un solo comando
make validate-3-pilares
```

### Validación Individual

```bash
# 1. Solo Reproducibilidad
python scripts/reproducibilidad_garantizada.py

# 2. Solo Falsabilidad
python scripts/falsabilidad_explicita.py

# 3. Solo Evidencia Empírica
python scripts/evidencia_empirica.py
```

### Tests

```bash
# Ejecutar suite completa de tests (11 tests)
make test-3-pilares

# O directamente con Python
python scripts/test_3_pilares.py
```

## 📊 Resultados Generados

Después de ejecutar `make validate-3-pilares`, encontrarás:

```
results/
├── validacion_reproducibilidad.json          # Pilar 1: Reproducibilidad
├── criterios_falsacion.json                  # Pilar 2: Falsabilidad
├── evidencia_empirica_gw150914.json          # Pilar 3: Evidencia Empírica
└── validacion_completa_3_pilares.json        # Consolidación completa
```

## 🎯 Ejemplo de Uso Completo

```bash
# 1. Clonar el repositorio
git clone https://github.com/motanova84/gw250114-141hz-analysis
cd gw250114-141hz-analysis

# 2. Configurar entorno
make setup

# 3. Ejecutar validación de 3 pilares
make validate-3-pilares

# 4. Ver resultados
cat results/validacion_completa_3_pilares.json
```

## ✅ Salida Esperada

```
======================================================================
 VALIDACIÓN COMPLETA - 3 PILARES DEL MÉTODO CIENTÍFICO
======================================================================

Implementa los requisitos del problema statement:
1. ✅ REPRODUCIBILIDAD GARANTIZADA
2. ✅ FALSABILIDAD EXPLÍCITA
3. ✅ EVIDENCIA EMPÍRICA CONCRETA

[... detalles de cada pilar ...]

======================================================================
 RESUMEN DE VALIDACIÓN
======================================================================

✅ 1. REPRODUCIBILIDAD: GARANTIZADA
   → Comando: make validate
   → Repositorio: https://github.com/motanova84/gw250114-141hz-analysis

✅ 2. FALSABILIDAD: EXPLÍCITA
   → 4 criterios de falsación definidos
   → Verificación independiente posible

✅ 3. EVIDENCIA EMPÍRICA: CONCRETA
   → Evento: GW150914
   → H1: 141.69 Hz (SNR 7.47)
   → L1: 141.75 Hz (SNR 0.95)

======================================================================
✅ VALIDACIÓN COMPLETA EXITOSA
======================================================================
```

## 🔍 Ver Detalles

Para más información sobre cada pilar, consulta:

- [TRES_PILARES_METODO_CIENTIFICO.md](TRES_PILARES_METODO_CIENTIFICO.md) - Documentación completa
- [README.md](README.md) - Documentación principal del proyecto

## 💡 Casos de Uso

### Para Investigadores

```bash
# Verificar reproducibilidad del análisis
python scripts/reproducibilidad_garantizada.py

# Examinar criterios de falsación
python scripts/falsabilidad_explicita.py

# Analizar evidencia empírica
python scripts/evidencia_empirica.py
```

### Para Revisores

```bash
# Ejecutar validación completa
make validate-3-pilares

# Ejecutar tests
make test-3-pilares

# Verificar archivos JSON generados
ls -l results/*.json
```

### Para Desarrolladores

```bash
# Ejecutar suite de tests
python scripts/test_3_pilares.py

# Verificar integración
make validate

# Limpiar y volver a ejecutar
make clean
make validate-3-pilares
```

## 📚 Documentación Adicional

- `TRES_PILARES_METODO_CIENTIFICO.md` - Documentación técnica completa
- `README.md` - Documentación general del proyecto
- `SCIENTIFIC_METHOD.md` - Marco metodológico científico

## ❓ Preguntas Frecuentes

### ¿Qué hace cada pilar?

1. **Reproducibilidad**: Demuestra que cualquiera puede verificar los resultados
2. **Falsabilidad**: Define criterios específicos para refutar la hipótesis
3. **Evidencia Empírica**: Presenta resultados cuantitativos concretos

### ¿Por qué son importantes?

Los tres pilares aseguran que el análisis cumple con los estándares más rigurosos del método científico, permitiendo verificación independiente y evaluación objetiva.

### ¿Cómo se integran con el pipeline existente?

El comando `make validate` ahora incluye automáticamente la validación de 3 pilares:

```makefile
validate: setup validate-3-pilares
    ./venv/bin/python scripts/pipeline_validacion.py
```

## 🆘 Solución de Problemas

### Error: No se encuentra el módulo

```bash
# Asegúrate de estar en el directorio correcto
cd /ruta/a/gw250114-141hz-analysis

# Verifica que los scripts existan
ls scripts/reproducibilidad_garantizada.py
```

### Error: No se generan archivos JSON

```bash
# Crea el directorio results si no existe
mkdir -p results

# Ejecuta nuevamente
python scripts/validacion_completa_3_pilares.py
```

### Tests fallan

```bash
# Verifica que tienes Python 3.6+
python3 --version

# Ejecuta tests con más verbosidad
python3 scripts/test_3_pilares.py -v
```
