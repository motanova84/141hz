# 🔧 Guía de Configuración de Colaboradores Automatizados

Esta guía explica cómo configurar y habilitar los **8 bots inteligentes** en el proyecto GW250114-141Hz.

## ⚡ Inicio Rápido

### 1. Crear Etiquetas Requeridas (Automático/Manual)

✅ **Las etiquetas se crean automáticamente** mediante un workflow dedicado.

El workflow `.github/workflows/create-labels.yml` crea todas las etiquetas necesarias para Dependabot y otros workflows.

**Opción A - Automático (Recomendado):**
1. Las etiquetas se crean automáticamente al mergear el PR
2. El workflow se ejecuta también cuando se modifica `dependabot.yml`
3. Se puede ejecutar manualmente desde `Actions` → `Create Required Labels` → `Run workflow`

**Opción B - Manual con script Python:**
```bash
# Requiere gh CLI instalado y autenticado
python scripts/create_github_labels.py
```

**Verificar:**
1. Ir a `Issues` → `Labels`
2. Verificar que existen las etiquetas: `automated`, `dependencies`, `github-actions`, `python`, etc.
3. Total esperado: 16 etiquetas con colores y descripciones

### 2. Habilitar Dependabot (Automático)

✅ **Dependabot ya está habilitado automáticamente** al mergear este PR.

El archivo `.github/dependabot.yml` será detectado por GitHub y comenzará a funcionar inmediatamente.

**Verificar:**
1. Ir a `Settings` → `Security` → `Dependabot`
2. Verificar que "Dependabot alerts" y "Dependabot security updates" están habilitados
3. Ver primera ejecución en `Insights` → `Dependency graph` → `Dependabot`

### 3. Habilitar Workflows (Automático)

✅ **Todos los workflows se habilitan automáticamente** al mergear el PR.

Los archivos en `.github/workflows/` serán detectados automáticamente.

**Verificar:**
1. Ir a `Actions` tab
2. Ver lista de workflows en sidebar izquierdo
3. Todos los nuevos workflows aparecerán listados

### 4. Configurar Permisos de Workflows

⚙️ **Verificar permisos de GitHub Actions:**

1. Ir a `Settings` → `Actions` → `General`
2. En "Workflow permissions", seleccionar:
   - ✅ **"Read and write permissions"** (recomendado)
   - ✅ "Allow GitHub Actions to create and approve pull requests"
3. Guardar cambios

### 5. Configurar Secrets (Opcional)

Algunos workflows requieren secrets para funcionalidades avanzadas:

#### HF_TOKEN (Hugging Face)
**Requerido para**: Workflow de producción QCAL (subir datasets)

```bash
# Obtener token de Hugging Face
1. Ir a https://huggingface.co/settings/tokens
2. Crear token con permisos "write"
3. Copiar token

# Añadir a GitHub
1. Ir a Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: HF_TOKEN
4. Value: [pegar token]
5. Click "Add secret"
```

#### DOCKERHUB_TOKEN y DOCKERHUB_USERNAME
**Requerido para**: Workflow de producción QCAL (push Docker images)

```bash
# Obtener token de Docker Hub
1. Ir a https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Nombre: "github-actions"
4. Permisos: "Read, Write, Delete"
5. Copiar token

# Añadir a GitHub
1. Settings → Secrets and variables → Actions
2. Añadir DOCKERHUB_USERNAME con tu username
3. Añadir DOCKERHUB_TOKEN con el access token
```

## 📋 Checklist de Configuración Completa

### Configuración Básica (Requerida)
- [x] Mergear PR con archivos de workflows
- [ ] Verificar que etiquetas se crearon correctamente (automated, dependencies, github-actions)
- [ ] Verificar Dependabot habilitado en Settings
- [ ] Verificar workflows aparecen en Actions tab
- [ ] Configurar permisos "Read and write" para workflows
- [ ] Habilitar "Allow GitHub Actions to create and approve pull requests"

### Configuración Avanzada (Opcional)
- [ ] Añadir HF_TOKEN para Hugging Face uploads
- [ ] Añadir DOCKERHUB_TOKEN y DOCKERHUB_USERNAME
- [ ] Configurar notificaciones de workflow en Settings → Notifications

### Personalización (Opcional)
- [ ] Ajustar frecuencia de Dependabot en `.github/dependabot.yml`
- [ ] Personalizar etiquetas en `.github/labeler.yml`
- [ ] Modificar cron schedules en workflows si necesario

## 🧪 Probar Configuración

### 1. Probar Auto-Labeler

```bash
# Crear un PR de prueba
git checkout -b test/auto-labeler
echo "# Test" >> test.md
git add test.md
git commit -m "test: Probar auto-labeler"
git push origin test/auto-labeler

# Crear PR en GitHub
# Verificar que el bot añade etiquetas automáticamente
```

### 2. Probar Issue Management Bot

```bash
# Crear issue de prueba
Ir a Issues → New issue
Título: "Test: Probar bot de gestión"
Descripción: Incluir palabras clave como "steps", "expected", "python"
Crear issue
Verificar que el bot comenta automáticamente
```

### 3. Probar Workflow Intelligence

```bash
# Ejecutar manualmente
1. Ir a Actions → Workflow Intelligence
2. Click "Run workflow"
3. Click "Run workflow" (verde)
4. Esperar resultado
5. Verificar summary con análisis de rendimiento
```

### 4. Probar Dependency Health Check

```bash
# Ejecutar manualmente
1. Ir a Actions → Dependency Health Check
2. Click "Run workflow"
3. Esperar resultado
4. Verificar reporte de salud en artifacts
```

## 🔍 Verificar que Todo Funciona

### Dashboard de Verificación

Ir a `Actions` tab y verificar:

| Workflow | Primera Ejecución | Estado Esperado |
|----------|-------------------|-----------------|
| Auto Label PRs | Al crear PR | ✅ Success |
| Issue Management | Diaria 00:00 UTC | ✅ Success |
| Workflow Intelligence | Semanal Lunes | ⏳ Pendiente primera ejecución |
| Auto-Update Documentation | Semanal Domingo | ⏳ Pendiente primera ejecución |
| PR Review Automation | Al abrir PR | ✅ Success |
| Dependency Health | Semanal Miércoles | ⏳ Pendiente primera ejecución |
| Update Coherence Viz | Diaria 00:00 UTC | ✅ Success |

### Logs Útiles

Para debug de workflows:

```bash
# Ver logs de workflow específico
1. Ir a Actions
2. Click en workflow específico
3. Click en ejecución más reciente
4. Expandir steps para ver logs detallados
```

## 🐛 Troubleshooting

### Error: "Label not found" en Dependabot

**Síntoma:**
Dependabot muestra error: "No se encontraron las siguientes etiquetas: automated, dependencies, github-actions"

**Solución:**
1. Ir a `Actions` → `Create Required Labels`
2. Click "Run workflow"
3. Click "Run workflow" (verde)
4. Esperar que termine (debería tardar <1 minuto)
5. Verificar en `Issues` → `Labels` que las etiquetas existen

**Alternativa manual:**
```bash
# Usando el script Python
python scripts/create_github_labels.py
```

### Error: "Workflow requires permissions"

**Solución:**
1. Settings → Actions → General
2. Workflow permissions → "Read and write permissions"
3. Guardar cambios
4. Re-ejecutar workflow

### Error: "Unable to create pull request"

**Solución:**
1. Settings → Actions → General
2. Habilitar "Allow GitHub Actions to create and approve pull requests"
3. Re-ejecutar workflow

### Dependabot no crea PRs

**Verificar:**
1. Settings → Security → Dependabot
2. Verificar que "Dependabot alerts" está habilitado
3. Verificar que no hay límite de PRs abiertos (máximo 5)
4. Esperar ejecución semanal o ejecutar manualmente

### Workflow no se ejecuta en schedule

**Nota:** GitHub Actions tiene limitaciones:
- Workflows en repos con poca actividad pueden retrasarse
- Cron schedules tienen margen de ±15 minutos
- Repos con mucha actividad tienen prioridad

**Solución temporal:**
- Usar `workflow_dispatch` para ejecutar manualmente
- Verificar sintaxis de cron en workflow
- Esperar 24-48h para primera ejecución programada

### Bot no comenta en PRs/Issues

**Verificar permisos:**
1. Settings → Actions → General
2. Workflow permissions debe ser "Read and write permissions"
3. Re-ejecutar workflow después de cambiar permisos

## 🔐 Seguridad

### Secrets Seguros

✅ **Buenas prácticas:**
- Usar tokens con permisos mínimos necesarios
- Rotar tokens cada 90 días
- Nunca exponer tokens en logs
- Usar secrets de GitHub (nunca hardcodear)

❌ **Evitar:**
- Tokens con permisos "admin"
- Passwords en vez de tokens
- Compartir tokens entre múltiples servicios
- Logs de debug que muestren secrets

### Permisos de Workflows

Los workflows usan permisos específicos:

```yaml
permissions:
  contents: write        # Para push de cambios
  issues: write          # Para crear/comentar issues
  pull-requests: write   # Para crear/comentar PRs
  actions: read          # Para leer workflow runs
```

## 📊 Monitoreo

### Métricas a Observar

1. **Tasa de éxito de workflows**
   - Ir a `Actions` → Ver historial
   - Objetivo: >95% success rate

2. **PRs de Dependabot**
   - Insights → Dependency graph → Dependabot
   - Verificar que se crean y mergean regularmente

3. **Issues gestionados por bots**
   - Issues → Filter: `label:automated`
   - Verificar que se cierran apropiadamente

4. **Tiempo de respuesta en PRs**
   - Pull requests → Ver tiempo desde open hasta merge
   - Objetivo: <48h con recordatorios de bot

### Dashboards Recomendados

#### En GitHub
1. `Actions` - Ver ejecuciones de workflows
2. `Insights → Pulse` - Actividad general
3. `Insights → Community` - Health check del repo
4. `Security → Dependabot` - Alertas de seguridad

#### Externo (Opcional)
- **GitHub CLI**: `gh pr list`, `gh issue list`
- **API de GitHub**: Crear dashboards custom
- **Webhooks**: Integrar con Slack/Discord

## 🚀 Próximos Pasos

Después de configurar los bots:

1. **Crear PR de prueba** para verificar auto-labeling
2. **Crear issue de prueba** para verificar issue management
3. **Esperar primera ejecución programada** (24-48h)
4. **Monitorear Actions tab** durante primera semana
5. **Ajustar configuración** según necesidades

## 📚 Recursos Adicionales

- [AUTOMATED_COLLABORATORS.md](AUTOMATED_COLLABORATORS.md) - Documentación completa de cada bot
- [.github/copilot-instructions.md](.github/copilot-instructions.md) - Instrucciones para GitHub Copilot
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guía de contribución
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 💬 Soporte

Si necesitas ayuda con la configuración:

1. **Abrir issue** con etiqueta `question` y `automated`
2. **Incluir:**
   - Workflow que falla
   - Logs del error
   - Capturas de pantalla de configuración
3. **Mantenedores responderán** en <24h

---

**¡Configuración completada! 🎉**

Los bots están listos para mejorar el flujo de trabajo del proyecto.

*Última actualización: 2025-10-25*
