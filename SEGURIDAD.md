# Política de Seguridad

## Reporte de Problemas de Seguridad

Si descubre una vulnerabilidad de seguridad en este proyecto, por favor repórtela mediante:

1. **Correo Electrónico**: institutoconsciencia@proton.me (tiempo de respuesta: 7 días)
2. **GitHub Security Advisory**: Utilice la [función de reporte privado](https://github.com/motanova84/141hz/security/advisories/new)

**Objetivo de Tiempo de Respuesta**: 7 días para la respuesta inicial a reportes de vulnerabilidades.

Por favor NO reporte vulnerabilidades de seguridad a través de issues públicos de GitHub.

## Seguridad de Dependencias

Este proyecto utiliza escaneo automatizado de dependencias para identificar y abordar vulnerabilidades de seguridad en las dependencias.

### Escaneo Automatizado

El proyecto ejecuta verificaciones de salud de dependencias semanalmente utilizando:
- **pip-audit**: Escanea vulnerabilidades de seguridad conocidas en dependencias de Python
- **GitHub Dependabot**: Monitorea actualizaciones de seguridad (si está habilitado)

### Flujo de Trabajo

1. El workflow `dependency-health.yml` se ejecuta semanalmente los miércoles a las 10:00 UTC
2. Escanea todas las dependencias listadas en `requirements.txt`
3. Si se encuentran vulnerabilidades, se crea automáticamente un issue con:
   - Detalles de los paquetes vulnerables
   - Versiones afectadas
   - Correcciones disponibles
   - Enlaces a avisos de seguridad
4. El workflow cierra automáticamente issues de falsos positivos cuando no existen vulnerabilidades reales

### Verificaciones de Seguridad Manuales

Puede ejecutar una verificación de seguridad manualmente:

```bash
# Instalar pip-audit
pip install pip-audit

# Ejecutar escaneo de seguridad
pip-audit --desc --format json

# O con archivo de requirements
pip-audit -r requirements.txt
```

## Versiones Soportadas

Soportamos las siguientes versiones de Python:
- Python 3.11 (estándar de producción)
- Python 3.12 (preparación para el futuro)

## Mejores Prácticas de Seguridad

### Para Contribuyentes

Al contribuir a este proyecto:

1. **Mantener dependencias actualizadas**: Verifique regularmente actualizaciones de seguridad
2. **Revisar avisos de seguridad**: Consulte la [Base de Datos de Avisos de GitHub](https://github.com/advisories)
3. **Seguir prácticas de codificación segura**: 
   - Validar entradas de usuario
   - Usar consultas parametrizadas
   - Evitar credenciales codificadas
   - Usar generadores de números aleatorios seguros
4. **Probar actualizaciones de seguridad**: Ejecute la suite completa de pruebas después de actualizar dependencias

### Para Mantenedores

1. **Monitorear issues de seguridad**: Revise regularmente los issues de seguridad automatizados
2. **Actualizar prontamente**: Aplique parches de seguridad lo antes posible
3. **Verificar compatibilidad**: Pruebe actualizaciones con Python 3.11 y 3.12
4. **Documentar cambios**: Actualice CHANGELOG.md con correcciones de seguridad
5. **Comunicar**: Notifique a los usuarios sobre actualizaciones de seguridad críticas

## Mejoras de Seguridad Recientes

### 2025-10-26: Corrección del Workflow de Salud de Dependencias

**Problema**: El workflow de salud de dependencias creaba issues de seguridad de falsos positivos incluso cuando no existían vulnerabilidades.

**Causa Raíz**: El workflow verificaba si existía el archivo de reporte JSON de pip-audit, pero no verificaba si algún paquete realmente tenía vulnerabilidades. pip-audit genera un archivo de reporte incluso cuando todos los paquetes son seguros (con arrays `vulns` vacíos).

**Corrección**: 
- Se agregó análisis JSON adecuado para verificar si algún paquete tiene un array `vulns` no vacío
- Se mejoró la creación de issues para incluir resúmenes detallados de vulnerabilidades
- Se agregó cierre automático de issues de falsos positivos
- Se mejoró el reporte para distinguir claramente entre paquetes con y sin vulnerabilidades

**Impacto**: Reduce el ruido de alertas de seguridad de falsos positivos y proporciona información más accionable cuando se detectan vulnerabilidades reales.

## Línea de Tiempo de Respuesta de Seguridad

- **Vulnerabilidades críticas**: Corrección en 24-48 horas
- **Severidad alta**: Corrección en 7 días
- **Severidad media**: Corrección en 30 días
- **Severidad baja**: Corrección en el siguiente ciclo de actualización regular

## Política de Divulgación

Cuando abordamos una vulnerabilidad de seguridad:

1. Reconoceremos la recepción del reporte en 48 horas
2. Proporcionaremos una línea de tiempo estimada para una corrección
3. Liberaremos un parche y aviso de seguridad
4. Acreditaremos al reportero (a menos que se solicite anonimato)

## Política de Secretos

### Gestión de Tokens y Credenciales

**Política**: Todos los tokens de autenticación y credenciales DEBEN proporcionarse solo mediante variables de entorno. Los argumentos de línea de comandos y archivos de configuración están explícitamente prohibidos por razones de seguridad.

### Métodos de Autenticación Soportados

1. **Token de Hugging Face** (`HF_TOKEN`)
   - Usado para: Descargas de modelos Llama 4 e inferencia
   - **Requerido**: Solo cuando se usa `use_llama4=True` en QCAL-LLM
   - **Formato**: `hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXX` (34+ caracteres)
   - **Configuración**: `export HF_TOKEN=your_token_here`
   - **Nunca**: Pasar vía `--token`, `--hf-token`, o almacenar en código

2. **Clave API de OpenAI** (`OPENAI_API_KEY`)
   - Usado para: Comparaciones de benchmarks (opcional)
   - **Configuración**: `export OPENAI_API_KEY=your_key_here`

3. **Clave API de Anthropic** (`ANTHROPIC_API_KEY`)
   - Usado para: Comparaciones de benchmarks (opcional)
   - **Configuración**: `export ANTHROPIC_API_KEY=your_key_here`

### Detección Automatizada de Tokens

El proyecto incluye pruebas automatizadas que fallan si se detectan patrones de tokens en el repositorio:

```bash
# Ejecutar prueba de detección de tokens
python tests/test_security_no_tokens.py
```

**Qué verifica**:
- Tokens de Hugging Face: `hf_[A-Za-z0-9]{30,}`
- Claves API de OpenAI: `sk-[A-Za-z0-9]{32,}`
- Secretos genéricos: Cadenas de alta entropía en contextos sospechosos

**Integración CI/CD**: Esta prueba se ejecuta en cada push y pull request. Los PRs que contengan tokens serán rechazados automáticamente.

### Si Accidentalmente Confirma un Token

1. **Revoque inmediatamente** el token en el proveedor del servicio
2. **Genere un nuevo token** con los scopes apropiados
3. **Elimine del historial** usando `git filter-branch` o BFG Repo-Cleaner
4. **Reporte** el incidente a los mantenedores si está en un repositorio público

### Mejores Prácticas

✅ **HACER**:
- Almacenar tokens en variables de entorno
- Usar archivos `.env` (asegúrese de que estén en `.gitignore`)
- Usar servicios de gestión de secretos (GitHub Secrets, AWS Secrets Manager, etc.)
- Rotar tokens regularmente
- Usar los scopes/permisos mínimos requeridos

❌ **NO HACER**:
- Codificar tokens en archivos fuente
- Pasar tokens vía argumentos de línea de comandos
- Confirmar archivos `.env` en control de versiones
- Compartir tokens en issues, PRs o discusiones
- Usar tokens de producción para pruebas

### Plantilla de Archivo .env

Cree un archivo `.env` en la raíz del proyecto (nunca confirme este archivo):

```bash
# Token de Hugging Face (opcional, solo para integración Llama 4)
HF_TOKEN=hf_your_token_here

# Clave API de OpenAI (opcional, solo para benchmarks)
OPENAI_API_KEY=sk-your_key_here

# Clave API de Anthropic (opcional, solo para benchmarks)
ANTHROPIC_API_KEY=sk-ant-your_key_here
```

Cargar con:
```python
from dotenv import load_dotenv
load_dotenv()  # Carga automáticamente el archivo .env
```

## Reproducibilidad y Verificación de Integridad

### ENV.lock - Gestión de Entornos Reproducibles

El proyecto utiliza `ENV.lock` para asegurar la reproducibilidad exacta de los resultados en diferentes entornos:

1. **Versiones Exactas**: Todas las dependencias están fijadas a versiones específicas
2. **Verificación de Hashes**: Soporte para instalación con verificación de hashes SHA256
3. **Múltiples Entornos**: Compatible con Python 3.11 y 3.12

#### Uso de ENV.lock

```bash
# Instalación estándar
pip install -r ENV.lock

# Instalación con verificación de hashes (máxima seguridad)
pip download --dest wheels -r ENV.lock
pip hash wheels/* >> ENV.lock.hashes
pip install --require-hashes -r ENV.lock.hashes
```

#### Regeneración de ENV.lock

```bash
# 1. Crear entorno virtual fresco
python3 -m venv venv

# 2. Instalar requirements
pip install -r requirements.txt

# 3. Congelar versiones
pip freeze > ENV.lock

# 4. Probar instalación
pip install -r ENV.lock

# 5. Ejecutar pruebas
pytest tests/
```

### Verificación de Integridad de Datos

El proyecto implementa verificación de integridad de datos mediante checksums SHA256:

1. **Pipeline Reproducible**: El directorio `repro/` contiene pipelines con verificación de checksums
2. **Validación Automática**: Los workflows generan y validan checksums de resultados
3. **Proveniencia de Datos**: Registro completo del origen y procesamiento de datos

#### Verificación Manual de Integridad

```bash
# Generar checksums de resultados
find artifacts/ -type f -name "*.json" -exec sha256sum {} \; > checksums.txt

# Verificar integridad
sha256sum -c checksums.txt
```

### Workflows de Producción

Los workflows de producción (`production-qcal.yml`) incluyen:

- Instalación desde ENV.lock para reproducibilidad
- Generación de snapshots de entorno
- Checksums de todos los artefactos
- Retención de 30 días para resultados de producción

## Recursos Adicionales

- [Mejores Prácticas de Seguridad en Python](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Funciones de Seguridad de GitHub](https://docs.github.com/en/code-security)
- [Documentación de pip-audit](https://github.com/pypa/pip-audit)
- [Git Secrets](https://github.com/awslabs/git-secrets) - Prevenir commits de secretos

---

Última actualización: 2025-01-06
