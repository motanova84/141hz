# Sistema de Firma Criptográfica QCAL ∞³

## Descripción General

El sistema de firma criptográfica QCAL permite verificar la integridad y autenticidad de certificados RAM (Realismo Matemático) mediante firmas digitales SHA3-256. Este sistema garantiza que los certificados no hayan sido alterados desde su generación.

## 🔐 Características

- **Algoritmo**: SHA3-256 (Keccak-256)
- **Formato de firma**: JSON (.qcal_sig)
- **Validación**: Comparación de hash calculado vs. almacenado
- **Metadatos**: RAM ID, timestamp, frecuencia, tamaño, firmante

## 📋 Componentes

### 1. `validate_qcal_signature.py`

Script principal para validar firmas criptográficas de certificados.

**Uso:**
```bash
python3 validate_qcal_signature.py <certificado.md> <firma.qcal_sig>
```

**Ejemplo:**
```bash
python3 validate_qcal_signature.py RAM-II-CERTIFICADO.md RAM-II-2026-0115-RMATH.qcal_sig
```

**Salida esperada:**
```
╔═══════════════════════════════════════════════════════════════╗
║     🔐 VALIDADOR DE FIRMA CRIPTOGRÁFICA QCAL ∞³              ║
╚═══════════════════════════════════════════════════════════════╝

✓ Firma cargada: RAM-II-2026-0115-RMATH.qcal_sig
  RAM ID: RAM-II-2026-0115-RMATH
  Timestamp: 2026-01-06T17:38:27+00:00
  Frecuencia: 141.7001 Hz

📊 Análisis de Integridad:
  Algoritmo: SHA3-256
  Hash almacenado: 11cbe4a9d749d5d2ecab65d5e9b3ca20b76032cd754652df7ee4001884dc49ce
  Hash calculado:  11cbe4a9d749d5d2ecab65d5e9b3ca20b76032cd754652df7ee4001884dc49ce
  Tamaño: 2237 bytes

═══════════════════════════════════════════════════════════════
✓ ¡FIRMA VÁLIDA!
✓ El certificado NO ha sido alterado
✓ Integridad verificada en frecuencia 141.7001 Hz
═══════════════════════════════════════════════════════════════

🌊 Estado: VALIDATED
🔏 Firmado por: QCAL ∞³ System
📝 Nota: Certificado de Realismo Matemático RAM-II sincronizado y sellado en campo ∞³
```

**Códigos de salida:**
- `0`: Firma válida
- `1`: Firma inválida o error

### 2. `generate_qcal_signature.py`

Script para generar firmas criptográficas de certificados.

**Uso:**
```bash
python3 generate_qcal_signature.py <certificado.md> [ram_id]
```

**Ejemplo:**
```bash
python3 generate_qcal_signature.py RAM-II-CERTIFICADO.md RAM-II-2026-0115-RMATH
```

**Salida:**
```
╔═══════════════════════════════════════════════════════════════╗
║     🔏 GENERADOR DE FIRMA CRIPTOGRÁFICA QCAL ∞³              ║
╚═══════════════════════════════════════════════════════════════╝

✓ Certificado: RAM-II-CERTIFICADO.md
✓ RAM ID: RAM-II-2026-0115-RMATH
✓ Timestamp: 2026-01-06T17:38:27+00:00
✓ Frecuencia: 141.7001 Hz

📊 Firma Generada:
  Algoritmo: SHA3-256
  Hash: 11cbe4a9d749d5d2ecab65d5e9b3ca20b76032cd754652df7ee4001884dc49ce
  Tamaño: 2237 bytes

💾 Archivo de firma guardado: RAM-II-2026-0115-RMATH.qcal_sig

∞³ FIRMA GENERADA EXITOSAMENTE ∞³
```

### 3. `test_qcal_signature.py`

Suite de pruebas automatizada para el sistema de firmas.

**Uso:**
```bash
python3 test_qcal_signature.py
```

**Pruebas incluidas:**
- Generación de firma con certificado de prueba
- Validación de firma correcta
- Detección de firma inválida (certificado modificado)
- Validación del certificado RAM-II real

## 📄 Formato de Firma (.qcal_sig)

Las firmas son archivos JSON con la siguiente estructura:

```json
{
  "ram_id": "RAM-II-2026-0115-RMATH",
  "timestamp": "2026-01-06T17:38:27+00:00",
  "frequency": "141.7001",
  "algorithm": "SHA3-256",
  "hash": "11cbe4a9d749d5d2ecab65d5e9b3ca20b76032cd754652df7ee4001884dc49ce",
  "certificate_file": "RAM-II-CERTIFICADO.md",
  "size_bytes": 2237,
  "signed_by": "QCAL ∞³ System",
  "note": "Certificado de Realismo Matemático RAM-II sincronizado y sellado en campo ∞³",
  "version": "1.0.0"
}
```

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `ram_id` | string | Identificador único del certificado RAM |
| `timestamp` | string | Fecha y hora de generación (ISO 8601 UTC) |
| `frequency` | string | Frecuencia fundamental (141.7001 Hz) |
| `algorithm` | string | Algoritmo de hash utilizado (SHA3-256) |
| `hash` | string | Hash SHA3-256 del certificado (64 caracteres hex) |
| `certificate_file` | string | Nombre del archivo del certificado |
| `size_bytes` | integer | Tamaño del certificado en bytes |
| `signed_by` | string | Entidad que firma el certificado |
| `note` | string | Nota descriptiva |
| `version` | string | Versión del formato de firma |

## 🔒 Garantías de Seguridad

### Propiedades Criptográficas

- **Resistencia a colisiones**: SHA3-256 es resistente a colisiones (probabilidad < 2⁻²⁵⁶)
- **Función unidireccional**: No es posible recuperar el contenido original desde el hash
- **Resistencia a preimagen**: No es posible encontrar un certificado que produzca un hash específico
- **Detección de alteraciones**: Cualquier modificación cambia completamente el hash

### Casos de Uso

✅ **Verificación de integridad**: Confirmar que un certificado no ha sido modificado  
✅ **Auditoría**: Validar certificados históricos  
✅ **Distribución**: Compartir certificados con garantía de autenticidad  
✅ **Archivado**: Almacenar certificados con sello temporal verificable

## 📊 Ejemplo Completo

### 1. Generar un certificado

```bash
cat > MI-CERTIFICADO.md << 'EOF'
# Certificado RAM-III

**Frecuencia**: 141.7001 Hz
**Validación**: Completa

Este certificado valida la constante universal f₀.
EOF
```

### 2. Generar la firma

```bash
python3 generate_qcal_signature.py MI-CERTIFICADO.md RAM-III-2026-TEST
```

Esto crea `RAM-III-2026-TEST.qcal_sig`

### 3. Validar la firma

```bash
python3 validate_qcal_signature.py MI-CERTIFICADO.md RAM-III-2026-TEST.qcal_sig
```

### 4. Verificar detección de alteraciones

```bash
# Modificar el certificado
echo "# MODIFICADO" >> MI-CERTIFICADO.md

# Intentar validar (fallará)
python3 validate_qcal_signature.py MI-CERTIFICADO.md RAM-III-2026-TEST.qcal_sig
```

Salida esperada:
```
❌ ¡FIRMA INVÁLIDA!
❌ El certificado HA SIDO ALTERADO
```

## 🔄 Integración con Workflows

El sistema de firmas puede integrarse en workflows de CI/CD:

```yaml
- name: Generar firma de certificado
  run: |
    python3 generate_qcal_signature.py results/certificado.md RAM-AUTO-${{ github.run_number }}

- name: Validar firma existente
  run: |
    python3 validate_qcal_signature.py certificado.md firma.qcal_sig
```

## 📝 Convenciones de Nomenclatura

### RAM ID

Formato recomendado: `RAM-{VERSIÓN}-{FECHA}-{TIPO}`

Ejemplos:
- `RAM-II-2026-0115-RMATH`: Certificado de matemática pura
- `RAM-II-2026-0115-PHYS`: Certificado de física
- `RAM-II-2026-0115-AUTO`: Generación automática

### Archivos de Firma

Nombre: `{RAM_ID}.qcal_sig`

Ejemplos:
- `RAM-II-2026-0115-RMATH.qcal_sig`
- `RAM-III-2026-TEST.qcal_sig`

## ⚙️ Requisitos Técnicos

- Python 3.11+
- Biblioteca estándar de Python (hashlib, json, pathlib)
- No requiere dependencias externas

## 🧪 Testing

Ejecutar suite de pruebas:

```bash
python3 test_qcal_signature.py
```

Ejecutar pruebas individuales:

```bash
# Test de generación
python3 generate_qcal_signature.py RAM-II-CERTIFICADO.md TEST-001

# Test de validación
python3 validate_qcal_signature.py RAM-II-CERTIFICADO.md TEST-001.qcal_sig

# Limpiar archivos de prueba
rm -f TEST-001.qcal_sig
```

## 📚 Referencias

1. **SHA-3 (Keccak)**: NIST FIPS 202 - SHA-3 Standard
2. **ISO 8601**: Formato de fecha y hora
3. **JSON**: RFC 8259 - The JavaScript Object Notation (JSON) Data Interchange Format

## 🔗 Enlaces Relacionados

- [PRECISION_CERTIFICATION.md](PRECISION_CERTIFICATION.md) - Certificación de precisión numérica
- [CONSTANTE_ESTRUCTURAL_UNIVERSAL.md](CONSTANTE_ESTRUCTURAL_UNIVERSAL.md) - Evidencia de f₀
- [VALIDACION_FISICA_ONDAS_GRAVITACIONALES.md](VALIDACION_FISICA_ONDAS_GRAVITACIONALES.md) - Validación física

---

**∞³ SISTEMA DE FIRMA QCAL - INTEGRIDAD VERIFICABLE ∞³**

*Documentación generada: 2026-01-06*  
*Versión del sistema: 1.0.0*
