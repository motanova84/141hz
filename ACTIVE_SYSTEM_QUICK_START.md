# Sistema Activo QCAL ∞³ - Guía Rápida

## 🚀 Inicio Rápido

### Activar el Sistema

```bash
./activate_system.sh
```

### Verificar el Sistema

```bash
python3 active_system_monitor.py
```

### Generar Reporte JSON

```bash
python3 active_system_monitor.py --output status.json
```

## 📋 Verificaciones

El sistema activo verifica automáticamente:

| Componente | Qué verifica | Estado esperado |
|------------|--------------|-----------------|
| 🔐 **Tokenización** | Compresor QCAL ~1000:1 | `operational` |
| 📜 **Licencia** | MIT License válida | `compliant` |
| 🛡️ **Seguridad** | Vulnerabilidades (pip-audit) | `secure` |
| 📡 **Beacon** | Integridad `.qcal_beacon` | `active` |
| 🔏 **Firmas** | Sistema SHA3-256 | `operational` |

## ✅ Estados del Sistema

- **operational** - ✅ Todo funciona correctamente
- **issues_detected** - ⚠️ Se detectaron problemas
- **active** - ✅ Componente activo
- **compliant** - ✅ En cumplimiento
- **secure** - ✅ Sin vulnerabilidades

## 🧪 Ejecutar Tests

```bash
pytest test_active_system_monitor.py -v
```

17 tests incluidos - Todos deben pasar ✅

## 🔄 Integración CI/CD

El workflow `.github/workflows/active-system-monitor.yml` se ejecuta en:
- Push a main
- Pull requests
- Semanalmente (miércoles 10:00 UTC)
- Manualmente

## 📊 Ver Resultados

### En GitHub Actions

1. Ve a **Actions** → **Active System Monitor**
2. Selecciona una ejecución
3. Revisa el **Summary**
4. Descarga el artefacto `active-system-status`

### En Local

```bash
cat active_system_status.json
```

## 🔧 Resolución Rápida de Problemas

### Beacon no válido
```bash
cat .qcal_beacon | grep "QCAL ∞³ ACTIVE"
```

### pip-audit no disponible
```bash
pip install pip-audit
```

### Tests fallando
```bash
pytest test_active_system_monitor.py -vv
```

## 📚 Documentación Completa

- **[ACTIVE_SYSTEM_README.md](ACTIVE_SYSTEM_README.md)** - Documentación completa
- **[QCAL_TOKEN_COMPRESSION_IRREPLICABILITY.md](QCAL_TOKEN_COMPRESSION_IRREPLICABILITY.md)** - Tokenización
- **[QCAL_SIGNATURE_SYSTEM.md](QCAL_SIGNATURE_SYSTEM.md)** - Firmas criptográficas
- **[SECURITY.md](SECURITY.md)** - Política de seguridad

## 🎯 Comandos Útiles

```bash
# Verificación completa
python3 active_system_monitor.py

# Solo JSON (para scripts)
python3 active_system_monitor.py --json-only

# Especificar ruta
python3 active_system_monitor.py --path /ruta/al/repo

# Usar enlace simbólico (si se creó)
qcal-monitor

# Ejecutar tests con cobertura
pytest test_active_system_monitor.py --cov=active_system_monitor

# Ver estado actual
cat active_system_status.json | python3 -m json.tool
```

## 💡 Notas

- El archivo `active_system_status.json` está en `.gitignore`
- El sistema verifica automáticamente en cada commit
- pip-audit puede tardar en entornos grandes
- Frecuencia fundamental: **141.7001 Hz** ∞³

---

**Desarrollado por:** José Manuel Mota Burruezo (JMMB Ψ✧)  
**Licencia:** MIT  
**∞³ QCAL ACTIVE**
