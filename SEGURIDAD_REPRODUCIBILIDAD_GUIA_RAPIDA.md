# Guía Rápida: Seguridad y Reproducibilidad - QCAL

## 🎯 Para Usuarios Rápidos

### Instalación Segura y Reproducible

```bash
# 1. Clonar repositorio
git clone https://github.com/motanova84/141hz.git
cd 141hz

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar desde ENV.lock (REPRODUCIBLE)
pip install -r ENV.lock

# 4. Validar
python scripts/validate_reproducibility.py
```

### Ejecutar Análisis Reproducible

```bash
# Generar snapshot de entorno
python scripts/validate_reproducibility.py --generate-snapshot --output env.json

# Ejecutar análisis
python validate_v5_coronacion.py --precision 50

# Generar checksums
find results/ -type f -name "*.json" -exec sha256sum {} \; > results/checksums.txt

# Archivar todo
tar -czf analysis-$(date +%Y%m%d).tar.gz results/ env.json ENV.lock
```

## 📚 Documentación Completa

### Seguridad

| Documento | Descripción |
|-----------|-------------|
| [SEGURIDAD.md](SEGURIDAD.md) | Política completa de seguridad (español) |
| [SECURITY.md](SECURITY.md) | Security policy (English) |
| [RESUMEN DE SEGURIDAD.md](RESUMEN%20DE%20SEGURIDAD.md) | Resumen de implementación (español) |
| [SECURITY_SUMMARY.md](SECURITY_SUMMARY.md) | Implementation summary (English) |

### Reproducibilidad

| Documento | Descripción |
|-----------|-------------|
| [REPRODUCIBILIDAD.md](REPRODUCIBILIDAD.md) | Guía completa de reproducibilidad |
| [ENV.lock](ENV.lock) | Dependencias exactas con instrucciones |
| [repro/GWTC-1/README.md](repro/GWTC-1/README.md) | Pipeline reproducible GWTC-1 |

### Scripts y Herramientas

| Script | Propósito |
|--------|-----------|
| `scripts/validate_reproducibility.py` | Validación automática de reproducibilidad |
| `repro/GWTC-1/run.sh` | Pipeline reproducible completo |
| `.github/workflows/production-qcal.yml` | Workflow de producción reproducible |

## ✅ Checklist de Verificación

### Antes de Publicar Resultados

- [ ] Instalado desde ENV.lock
- [ ] Generado snapshot de entorno
- [ ] Ejecutado con precisión fija (--precision 50)
- [ ] Generado checksums SHA256 de resultados
- [ ] Documentado commit de Git usado
- [ ] Archivado env.json + ENV.lock + resultados

### Validación de Seguridad

- [ ] Ejecutado `pip-audit -r ENV.lock`
- [ ] Sin vulnerabilidades críticas
- [ ] Sin tokens en código (test_security_no_tokens.py)
- [ ] Workflows CI/CD pasan

## 🔍 Comandos Útiles

### Seguridad

```bash
# Escanear vulnerabilidades
pip-audit -r ENV.lock

# Verificar tokens no confirmados
python tests/test_security_no_tokens.py

# Ver reportes de salud
ls -la artifacts/dependency-health-report-*
```

### Reproducibilidad

```bash
# Validar entorno
python scripts/validate_reproducibility.py --strict

# Generar snapshot
python scripts/validate_reproducibility.py --generate-snapshot

# Verificar checksums
cd results/
sha256sum -c checksums.txt

# Pipeline GWTC-1
cd repro/GWTC-1/
./run.sh
```

## ⚠️ Problemas Comunes

### "Dependency version mismatch"

**Solución**:
```bash
pip uninstall -y -r <(pip freeze)
pip install -r ENV.lock
```

### "Checksum mismatch"

**Causa**: Diferentes versiones de dependencias o semillas aleatorias

**Solución**:
```bash
python scripts/validate_reproducibility.py --strict
# Si pasa, el problema es otro (revisar seeds aleatorios)
```

### "Python version not supported"

**Solución**:
```bash
# Instalar Python 3.11 o 3.12
# Ubuntu/Debian
sudo apt-get install python3.11

# Crear venv con versión correcta
python3.11 -m venv venv
```

## 📞 Soporte

- **Email**: institutoconsciencia@proton.me
- **Issues**: https://github.com/motanova84/141hz/issues
- **Seguridad**: Usar [GitHub Security Advisory](https://github.com/motanova84/141hz/security/advisories/new)

## 🔗 Enlaces Rápidos

- 📖 [README Principal](README.md)
- 🔒 [Política de Seguridad](SEGURIDAD.md)
- 🔁 [Guía de Reproducibilidad](REPRODUCIBILIDAD.md)
- 🧪 [Pipeline GWTC-1](repro/GWTC-1/)
- ⚙️ [Workflows CI/CD](.github/workflows/)

---

**Última actualización**: 2025-01-06  
**Versión**: 1.0.0  
**Mantenedor**: QCAL Team
