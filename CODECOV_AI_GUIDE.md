# Codecov AI Integration Guide

Este documento explica cómo usar Codecov AI en el proyecto 141Hz para revisiones automáticas de código y generación de pruebas.

## 🤖 ¿Qué es Codecov AI?

Codecov AI es un asistente de IA generativa desarrollado por Codecov (Sentry) que:
- Revisa cambios en pull requests
- Genera sugerencias de mejora automáticamente
- Crea pruebas unitarias para nuevo código
- Analiza cobertura de código y calidad

## 📋 Requisitos Previos

### Para Administradores

La organización **ya no requiere tokens de carga** para Codecov. Los administradores pueden gestionar tokens globalmente.

### Instalación de Codecov AI (Solo Administradores)

Para habilitar Codecov AI en tu organización de GitHub:

1. **Instalar la aplicación de GitHub:**
   - Visita: https://github.com/apps/codecov-ai
   - Haz clic en "Install" o "Configure"
   - Selecciona tu organización (motanova84)
   - Elige los repositorios donde deseas activar Codecov AI

2. **Si no eres administrador:**
   Comparte este mensaje con el administrador de la organización:

   > Hola, ¿podrían ayudarnos a aprobar la instalación de la aplicación Codecov AI Reviewer en GitHub para nuestra organización? Aquí tienen el enlace: [Instalación de Codecov AI](https://github.com/apps/codecov-ai)

## 🚀 Uso de Codecov AI

Una vez instalada la aplicación, puedes usar estos comandos en los **comentarios de pull requests**:

### Comando: Revisar PR

```
@codecov-ai-reviewer review
```

**Qué hace:**
- Analiza todos los cambios en el PR
- Identifica problemas potenciales
- Sugiere mejoras de código
- Revisa patrones de diseño
- Verifica buenas prácticas

**Ejemplo de uso:**
1. Abre un pull request
2. Agrega un comentario con: `@codecov-ai-reviewer review`
3. Espera la respuesta del bot (puede tardar unos minutos)
4. Revisa las sugerencias y aplica las que consideres relevantes

### Comando: Generar Pruebas

```
@codecov-ai-reviewer test
```

**Qué hace:**
- Genera pruebas unitarias automáticamente
- Cubre casos edge y escenarios comunes
- Sigue las convenciones del proyecto
- Mejora la cobertura de código

**Ejemplo de uso:**
1. Crea un PR con código nuevo
2. Comenta: `@codecov-ai-reviewer test`
3. El bot generará sugerencias de pruebas
4. Copia y adapta las pruebas sugeridas

## 📊 Cobertura de Código

### Configuración Actual

El proyecto está configurado con los siguientes objetivos de cobertura (ver `codecov.yml`):

- **Target del proyecto:** Automático (mantener nivel actual)
- **Target de patches:** 70% de cobertura en código nuevo
- **Umbral de cambio:** ±1% para el proyecto, ±5% para patches

### Visualizar Cobertura

1. **En GitHub:**
   - Los PRs muestran automáticamente cambios en cobertura
   - Checks de GitHub indican si la cobertura cumple objetivos

2. **En Codecov Dashboard:**
   - Visita: https://codecov.io/gh/motanova84/141hz
   - Ver cobertura por archivo, función y línea
   - Analizar tendencias históricas

## 🔧 Configuración del Proyecto

### Archivos de Configuración

1. **`codecov.yml`** - Configuración principal de Codecov
   - Define objetivos de cobertura
   - Configura flags para diferentes componentes
   - Establece rutas a ignorar

2. **`pyproject.toml`** - Configuración de pytest-cov
   - Define qué código se mide
   - Excluye archivos de prueba
   - Configura formato de reportes

### Workflows de GitHub Actions

El proyecto incluye integración de Codecov en:

- **`.github/workflows/tests.yml`** - Tests de matriz Python
- **`.github/workflows/analyze.yml`** - Análisis completo
- **`.github/workflows/qc-llm-ci.yml`** - Tests QC-LLM

Todos estos workflows suben automáticamente reportes de cobertura a Codecov.

## 📈 Mejores Prácticas

### Para Contribuidores

1. **Ejecuta tests localmente antes de hacer PR:**
   ```bash
   pytest tests/ -v --cov=. --cov-report=term --cov-report=xml
   ```

2. **Revisa la cobertura local:**
   ```bash
   coverage report
   coverage html  # Genera reporte HTML interactivo
   ```

3. **Mantén cobertura alta en código nuevo:**
   - Apunta a >70% de cobertura en nuevas funciones
   - Escribe pruebas para casos edge
   - Documenta por qué ciertas líneas no se prueban (use `# pragma: no cover`)

### Para Revisores

1. **Usa Codecov AI para segunda opinión:**
   - Ejecuta `@codecov-ai-reviewer review` en PRs complejos
   - Compara sugerencias del bot con tu análisis
   - No dependas exclusivamente del bot

2. **Revisa cambios de cobertura:**
   - Verifica que código nuevo tenga tests
   - Investiga caídas significativas de cobertura
   - Pide más tests si la cobertura es baja

## 🐛 Solución de Problemas

### El bot no responde

1. Verifica que la app esté instalada en el repositorio
2. Asegúrate de usar el comando exacto: `@codecov-ai-reviewer`
3. Espera 2-5 minutos (la generación puede tardar)
4. Revisa permisos de la aplicación en GitHub

### La cobertura no se sube

1. Verifica que el workflow ejecute `pytest-cov`
2. Confirma que el archivo `coverage.xml` se genera
3. Revisa logs del step "Upload coverage to Codecov"
4. Para repos públicos, no se necesita token

### Sugerencias del bot no son útiles

- Codecov AI es una herramienta de asistencia, no reemplazo
- Usa tu criterio para filtrar sugerencias
- Proporciona feedback al equipo si el bot genera ruido

## 🔗 Enlaces Útiles

- [Documentación de Codecov](https://docs.codecov.com/)
- [Codecov AI Documentation](https://docs.codecov.com/docs/codecov-ai)
- [Dashboard del Proyecto](https://codecov.io/gh/motanova84/141hz)
- [GitHub App - Codecov AI](https://github.com/apps/codecov-ai)

## 📝 Notas Adicionales

### Tokens de Carga

**Nota importante sobre tokens:**
> "Tu organización ya no requiere tokens de carga. Puedes subir archivos sin token. Los administradores gestionan el token."

Esto significa que los workflows pueden subir cobertura sin configurar `CODECOV_TOKEN` en secrets para repositorios públicos, simplificando la configuración. Los administradores pueden configurar tokens globalmente a nivel de organización si es necesario.

### Privacidad y Seguridad

- Codecov AI solo analiza cambios en PRs
- No accede a código privado fuera del contexto del PR
- Sigue las políticas de privacidad de Sentry/Codecov
- Ver: https://docs.codecov.com/docs/privacy

## 🆘 Soporte

Para problemas o preguntas:
1. Abre un issue en el repositorio
2. Contacta al equipo de mantenimiento
3. Consulta la documentación de Codecov
