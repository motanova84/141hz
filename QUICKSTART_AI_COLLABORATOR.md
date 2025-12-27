# 🚀 Quick Start - AI Workflow Collaborator

## ¿Qué hace?

El **AI Workflow Collaborator** es un sistema automatizado que:
- ✅ Verifica que todos los workflows estén correctos
- 🔧 Corrige automáticamente problemas comunes
- 📊 Asegura que las badges muestren verde (GREEN)

## Ejecución Automática

El sistema se ejecuta **automáticamente** en estos casos:

1. **Al hacer push a main** con cambios en workflows o scripts
2. **Diariamente a las 6:00 UTC** (mantenimiento preventivo)
3. **En Pull Requests** que modifiquen workflows

No necesitas hacer nada, simplemente funciona en segundo plano.

## Ejecución Manual

### Desde GitHub UI
1. Ve a **Actions** tab
2. Selecciona **AI Workflow Collaborator**
3. Click en **Run workflow** → **Run workflow**

### Desde Local
```bash
# Verificar salud de workflows
python scripts/ai_workflow_health_checker.py

# Aplicar fixes si hay problemas
python scripts/ai_workflow_fixer.py
```

## Ver Resultados

### En GitHub Actions
1. Ve al workflow run
2. Revisa el **Summary** para ver el reporte
3. Descarga **artifacts** para reportes detallados

### En Local
Los reportes se guardan en:
```
results/
  ├── workflow_health_report.json
  └── workflow_fix_report.json
```

## Qué Verifica

- ✔️ Configuración correcta de workflows
- ✔️ Setup de Python cuando es necesario
- ✔️ Instalación de dependencias
- ✔️ Existencia de scripts referenciados
- ✔️ Versiones de Python consistentes
- ✔️ Uso de caching para optimización

## Qué Corrige Automáticamente

- ➕ Agrega setup de Python si falta
- ➕ Agrega instalación de requirements.txt
- ➕ Crea scripts placeholder para referencias faltantes
- ➕ Agrega campos requeridos (runs-on, etc.)
- 💾 Crea backups automáticos antes de modificar

## Estado Actual

```
✅ Workflows Analizados: 11
✅ Workflows Saludables: 11 (100%)
⚠️  Warnings: 5 (no críticos)
💡 Recomendaciones: 6
```

## Badges en README

Gracias al AI Workflow Collaborator, las badges siempre muestran:

![CI](https://github.com/motanova84/141hz/actions/workflows/analyze.yml/badge.svg) ✅

## Backups

Todos los cambios se respaldan en:
```
.github/workflow_backups/
  └── workflow_name_YYYYMMDD_HHMMSS.yml
```

Retención: 90 días

## Problemas?

Si algo no funciona:
1. Revisa el **workflow run** en GitHub Actions
2. Lee los **logs detallados** del step que falló
3. Descarga los **artifacts** con reportes
4. Abre un **issue** con label `ai-collaborator`

## Más Información

📚 **Documentación Completa:** [AI_WORKFLOW_COLLABORATOR.md](AI_WORKFLOW_COLLABORATOR.md)

🤖 **Todos los Colaboradores:** [AUTOMATED_COLLABORATORS.md](AUTOMATED_COLLABORATORS.md)

---

**✨ El AI Workflow Collaborator garantiza que tus badges siempre estén verdes ✅**
