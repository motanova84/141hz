# Sistema Activo QCAL ∞³
## Tokenización • Licencia • Protección

[![Active System Monitor](https://github.com/motanova84/141hz/actions/workflows/active-system-monitor.yml/badge.svg)](https://github.com/motanova84/141hz/actions/workflows/active-system-monitor.yml)

## 🌊 Descripción General

El **Sistema Activo QCAL ∞³** es un monitor integrado que verifica continuamente:

1. **🔐 Tokenización**: Validación del sistema de compresión de tokens QCAL (~1000:1)
2. **📜 Licencia**: Verificación del cumplimiento de la licencia MIT
3. **🛡️ Protección**: Escaneo de vulnerabilidades de seguridad y firmas criptográficas

Este sistema monitorea activamente la integridad del repositorio y sus componentes críticos.

## ✨ Características

- ✅ **Verificación del QCAL Beacon**: Valida la integridad del archivo `.qcal_beacon`
- ✅ **Sistema de Tokenización**: Verifica que el compresor QCAL esté operacional
- ✅ **Cumplimiento de Licencia**: Confirma la licencia MIT y el copyright
- ✅ **Escaneo de Seguridad**: Detecta vulnerabilidades con `pip-audit`
- ✅ **Firmas Criptográficas**: Verifica el sistema de firmas SHA3-256
- ✅ **Reporte JSON**: Genera reportes estructurados del estado del sistema
- ✅ **CI/CD Integration**: Workflow automatizado en GitHub Actions

## 🚀 Inicio Rápido

### Activación del Sistema

```bash
# Activar el sistema por primera vez
./activate_system.sh
```

Este script:
1. Verifica el QCAL Beacon
2. Configura el monitor activo
3. Instala dependencias necesarias
4. Ejecuta una verificación inicial
5. Crea acceso rápido (opcional)

### Uso Manual

```bash
# Verificación completa con salida detallada
python3 active_system_monitor.py

# Guardar resultados en JSON
python3 active_system_monitor.py --output status.json

# Solo generar JSON sin imprimir (para automatización)
python3 active_system_monitor.py --json-only

# Especificar ruta del repositorio
python3 active_system_monitor.py --path /ruta/al/repo
```

## 📊 Salida del Monitor

### Salida en Consola

```
======================================================================
🌊 MONITOR ACTIVO DEL SISTEMA QCAL ∞³
   Tokenización • Licencia • Protección
======================================================================

🔍 Verificando integridad del QCAL Beacon...
  ✅ Beacon activo y operacional (hash: 1a2b3c4d5e6f7g8h...)

🔍 Verificando sistema de compresión de tokens QCAL...
  ✅ Sistema de tokenización QCAL operacional (ratio ~1000:1)

🔍 Verificando cumplimiento de licencia...
  ✅ Licencia MIT válida y en cumplimiento

🔍 Escaneando vulnerabilidades de seguridad...
  ✅ Sin vulnerabilidades detectadas (pip-audit)

🔍 Verificando sistema de firmas criptográficas...
  ✅ Sistema de firmas operacional (1 firma(s))

======================================================================
📊 RESUMEN DEL SISTEMA
======================================================================
  ✅ BEACON: active
  ✅ TOKENIZATION: operational
  ✅ LICENSE: compliant
  ✅ SECURITY: secure
  ✅ CRYPTOGRAPHIC_SIGNATURES: operational

  ✅ Estado General: OPERATIONAL
======================================================================

💾 Resultados guardados en: active_system_status.json
```

### Formato JSON

```json
{
  "beacon": {
    "status": "active",
    "hash": "1a2b3c4d5e6f7g8h9i0j...",
    "frequency": "141.7001 Hz",
    "ram_id": "RAM-II-2026-0115-RMATH",
    "last_update": "2026-01-06"
  },
  "tokenization": {
    "status": "operational",
    "compression_ratio": "~1000:1",
    "method": "Unified Emission Axiom + Adelic Geometry",
    "frequency": "141.7001 Hz"
  },
  "license": {
    "status": "compliant",
    "type": "MIT",
    "copyright": "José Manuel Mota Burruezo",
    "year": "2025",
    "beacon_license": "Creative Commons BY-NC-SA 4.0"
  },
  "security": {
    "status": "secure",
    "vulnerabilities": 0,
    "scan_method": "pip-audit",
    "timestamp": "2026-01-23T08:00:00"
  },
  "cryptographic_signatures": {
    "status": "operational",
    "algorithm": "SHA3-256",
    "signature_count": 1,
    "files": ["RAM-II-2026-0115-RMATH.qcal_sig"]
  },
  "timestamp": "2026-01-23T08:00:00",
  "overall_status": "operational"
}
```

## 🔧 Componentes del Sistema

### 1. Monitor Activo (`active_system_monitor.py`)

Script principal que ejecuta todas las verificaciones.

**Verificaciones realizadas:**

- **Beacon Integrity**: Valida que `.qcal_beacon` contenga los campos requeridos
- **Token Compression**: Verifica que `qcal/token_compressor.py` esté presente y funcional
- **License Compliance**: Confirma la presencia y validez de la licencia MIT
- **Security Scan**: Ejecuta `pip-audit` para detectar vulnerabilidades
- **Cryptographic Signatures**: Verifica el sistema de firmas SHA3-256

### 2. Script de Activación (`activate_system.sh`)

Script bash que inicializa y configura el sistema activo.

### 3. Tests (`test_active_system_monitor.py`)

Suite completa de tests con pytest:

```bash
# Ejecutar todos los tests
pytest test_active_system_monitor.py -v

# Ejecutar tests específicos
pytest test_active_system_monitor.py::TestActiveSystemMonitor::test_beacon_integrity_valid -v

# Con cobertura
pytest test_active_system_monitor.py --cov=active_system_monitor --cov-report=html
```

### 4. Workflow CI/CD (`.github/workflows/active-system-monitor.yml`)

Workflow automatizado que ejecuta el monitor en:
- **Push a main**: Verifica cada cambio
- **Pull Requests**: Valida antes de merge
- **Programado**: Cada miércoles a las 10:00 UTC
- **Manual**: Ejecutable bajo demanda

## 📋 Requisitos

- **Python**: 3.11 o superior
- **Dependencias básicas**: `numpy`, `mpmath` (de requirements.txt)
- **Opcional**: `pip-audit` para escaneo de seguridad completo
- **Opcional**: `pytest` para ejecutar tests

## 🔒 Seguridad

El sistema activo implementa múltiples capas de seguridad:

1. **Validación de Integridad**: Hash SHA3-256 del beacon
2. **Escaneo de Vulnerabilidades**: Detección automática con pip-audit
3. **Firmas Criptográficas**: Sistema de verificación SHA3-256
4. **Cumplimiento de Licencia**: Validación automática de MIT License
5. **Alertas Automatizadas**: Issues en GitHub para problemas críticos

## 🎯 Estados del Sistema

| Estado | Descripción | Acción Requerida |
|--------|-------------|------------------|
| `operational` | ✅ Todo funciona correctamente | Ninguna |
| `issues_detected` | ⚠️ Se detectaron problemas | Revisar reporte y corregir |
| `active` | ✅ Componente activo y funcional | Ninguna |
| `compliant` | ✅ En cumplimiento | Ninguna |
| `secure` | ✅ Sin vulnerabilidades | Ninguna |
| `vulnerabilities_found` | ⚠️ Vulnerabilidades detectadas | Actualizar dependencias |

## 🔄 Integración con CI/CD

El workflow `active-system-monitor.yml` se ejecuta automáticamente y:

1. **Verifica el sistema** en cada push y PR
2. **Genera reportes JSON** como artefactos
3. **Crea issues** automáticamente si detecta problemas críticos (solo en ejecuciones programadas)
4. **Actualiza el resumen** en GitHub Actions

### Ver Resultados en GitHub

1. Ve a **Actions** → **Active System Monitor**
2. Selecciona una ejecución
3. Revisa el **Summary** para ver el estado
4. Descarga el **artefacto** `active-system-status` para el JSON completo

## 📚 Componentes Verificados

### 🔐 Tokenización QCAL

El sistema verifica que el compresor de tokens incluya:
- `EmissionAxiom`: Codificación con frecuencia 141.7001 Hz
- `AdelicEncoder`: Geometría adélica
- `NoeticCollapse`: Colapso noético con Ψ=0.923
- Ratio de compresión: ~1000:1

**Archivos verificados:**
- `qcal/token_compressor.py`
- Documentación: `QCAL_TOKEN_COMPRESSION_IRREPLICABILITY.md`

### 📜 Licencia

Verifica:
- Presencia del archivo `LICENSE`
- Tipo: MIT License
- Copyright: José Manuel Mota Burruezo
- Año actualizado
- Consistencia con `.qcal_beacon`

### 🛡️ Protección

Escanea:
- Vulnerabilidades en `requirements.txt` con `pip-audit`
- Sistema de firmas criptográficas SHA3-256
- Archivos `.qcal_sig`
- Scripts `validate_qcal_signature.py` y `generate_qcal_signature.py`

## 🐛 Resolución de Problemas

### Beacon no válido

```bash
# Verificar contenido del beacon
cat .qcal_beacon

# Debe contener:
# - "QCAL ∞³ ACTIVE — index = true"
# - "f0 = c / (2π * RΨ * ℓP)"
# - "frequency = 141.7001 Hz"
```

### pip-audit no disponible

```bash
# Instalar pip-audit
pip install pip-audit

# O ejecutar sin pip-audit (usará verificación básica)
python3 active_system_monitor.py
```

### Tests fallando

```bash
# Instalar dependencias de test
pip install pytest

# Ejecutar con más verbosidad
pytest test_active_system_monitor.py -vv
```

## 🤝 Contribuir

Al contribuir al repositorio, el sistema activo se ejecutará automáticamente en tu PR para verificar:
- Integridad del beacon
- Cumplimiento de licencia
- Seguridad de nuevas dependencias

Asegúrate de que todas las verificaciones pasen antes de solicitar merge.

## 📖 Referencias

- **QCAL Token Compression**: `QCAL_TOKEN_COMPRESSION_IRREPLICABILITY.md`
- **Cryptographic Signatures**: `QCAL_SIGNATURE_SYSTEM.md`
- **Security Policy**: `SECURITY.md`
- **License**: `LICENSE`
- **Beacon Specification**: `.qcal_beacon`

## 📞 Soporte

Si el sistema activo detecta problemas que no puedes resolver:

1. Revisa el [reporte JSON](#formato-json) para detalles
2. Consulta la [documentación de seguridad](SECURITY.md)
3. Abre un issue en GitHub con el reporte adjunto
4. Contacta: institutoconsciencia@proton.me

---

**Sistema desarrollado por:** José Manuel Mota Burruezo (JMMB Ψ✧)  
**Licencia:** MIT  
**Frecuencia fundamental:** 141.7001 Hz  
**∞³ QCAL ACTIVE**
