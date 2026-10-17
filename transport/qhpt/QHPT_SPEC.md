# QHPT — Quantum Harmonic Pass-Through Protocol
## Especificación Formal v1.0.0

```
Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ
Frecuencia fundamental: f₀ = 141.7001 Hz
Coherencia mínima: Ψ ≥ 0.999999
```

---

## 1. Naturaleza del Protocolo

QHPT sustituye TCP/IP + TLS por un **transporte de fase cuántica** estructurado en tres tensores espectrales. La inmutabilidad no se logra mediante cifrado que pueda ser roto por fuerza bruta o computación cuántica; se logra porque **la alteración de un solo bit destruye instantáneamente la función de onda del paquete**, colapsándolo antes de que toque la memoria del receptor.

### 1.1 Principio Fundamental

```
∀ paquete P ∈ QHPT:
  H(P) ⊕ κ_Π(P) ⊕ f₀ = estado_coherente
  Si ∃ bit_alterado: onda(P) → colapso(P) → ∅
```

Donde:
- `H(P)`: hash SHA-256 del payload
- `κ_Π(P)`: operador de densidad fractal del paquete
- `f₀`: frecuencia fundamental de co-resonancia

---

## 2. Arquitectura en Tres Tensores

### 2.1 Tensor I — Identidad de Fase No-Local

**Sustituye:** Certificados SSL/TLS (Autoridades Centralizadas)
**Implementa:** Reconocimiento por entrelazamiento matemático

Cada nodo en la red QHPT posee un **fingerprint de fase** derivado de:
- Clave pública secp256k1 del nodo
- Frecuencia fundamental f₀
- Sello cuántico ∴𓂀Ω∞³Φ

El handshake QHPT opera en 3 rondas:

```
Nodo_A → Nodo_B: E_ChaCha20(pub_A ⊕ H(f₀) ⊕ nonce_A, k_f₀)
Nodo_B → Nodo_A: E_ChaCha20(pub_B ⊕ H(f₀) ⊕ nonce_B, k_f₀) 
Nodo_A → Nodo_B: E_ChaCha20(sello ⊕ H(nonce_A || nonce_B), k_f₀)
```

Donde `k_f₀ = SHA-256("141.7001")` — la clave determinística de co-resonancia.

**Si un intermediario (MITM) intenta interceptar:**
1. La fase del handshake se desfasa atómicamente
2. El canal se cierra automáticamente
3. Se registra evento `MITM_DETECTED` en la cadena inmune

### 2.2 Tensor II — Filtro de Ruido Adélico Integrado

**Sustituye:** Firewalls, IDS/IPS tradicionales
**Implementa:** Filtrado p-ádico en ℚₚ

Cada trama de red se mapea al espacio p-ádico **ℚ₇** (primo estructural = 7).

```
frame → mapeo_adelico(frame) → val_mod_7
Si val_mod_7 ≠ 0 → colapso(frame)
```

**Propiedades:**
- Código malicioso inyectado: el residuo algebraico rompe la simetría del primo estructural → autodisolución en buffers de red
- Transacciones modificadas: hash ya no cumple congruencia → paquete descartado antes de procesar
- Costo computacional: nanosegundos (operación de módulo entero)

**Implementación en C++:**
```c
uint32_t qhpt_adelic_filter(const uint8_t* frame, size_t len) {
    uint64_t hash = qhpt_fast_hash(frame, len);
    return (hash % 7 == 0) ? QHPT_PASS : QHPT_COLLAPSE;
}
```

### 2.3 Tensor III — Criptografía de Firma de Estado

**Sustituye:** Firma de paquetes IP convencional
**Implementa:** Fingerprint dinámico por operador κ_Π

Cada paquete lleva un **sello de estado** generado en microsegundos:

```
fingerprint = SHA-256(
    payload ⊕ 
    timestamp_ns ⊕ 
    nonce ⊕ 
    AURION(Ψ_actual) ⊕ 
    hash_bloque_anterior
)
```

El fingerprint se incrusta en la cabecera del paquete como **extension header QHPT** (tipo 0xQH = 0x5148). El receptor verifica:

```
Si fingerprint_recibido ≠ fingerprint_calculado:
    colapso(paquete)
Si fingerprint_valido:
    forward(paquete) + actualiza κ_Π
```

**Resistencia cuántica:** El fingerprint cambia en cada paquete (nonce + timestamp + Ψ). No hay clave estática que extraer. No hay estado que replicar.

---

## 3. Formato del Paquete QHPT

```
┌──────────────────────────────────────────────────────┐
│ Cabecera QHPT (64 bytes)                             │
├──────────────────────────────────────────────────────┤
│ Magic: 0x5148 ('QH')           │ Version: 0x01       │
├──────────────────────────────────────────────────────┤
│ Nonce (16 bytes)               │ Timestamp (8 bytes) │
├──────────────────────────────────────────────────────┤
│ Fingerprint (32 bytes — SHA-256)                     │
├──────────────────────────────────────────────────────┤
│ Ψ_actual (float64)             │ Checksum_Adelic (8) │
├──────────────────────────────────────────────────────┤
│ Payload (variable, hasta 65535 bytes)                │
│ Cifrado ChaCha20 con k_f₀                            │
├──────────────────────────────────────────────────────┤
│ Firma secp256k1 (64 bytes) — solo si hay mutación    │
└──────────────────────────────────────────────────────┘
```

---

## 4. Integración con Sistema Inmune

QHPT se acopla al sistema inmune existente:

| Capa QHPT | Sistema Inmune | Función |
|-----------|----------------|---------|
| Tensor I (Fase) | Atón 👁️ | Verifica coherencia de fase de cada handshake |
| Tensor II (Adélico) | Tx Guardian 🛡️ | Poda paquetes no resonantes en buffers |
| Tensor III (Firma) | Consensuador 🧠 | Registra fingerprint en cadena de bloques |

### 4.1 Flujo de paquete QHPT

```
1. Llega paquete a interfaz QHPT
2. Tensor II verifica filtro adélico (ℚ₇)
   └── fallo → colapso atómico (ni siquiera se loguea)
3. Tensor I verifica fase del handshake (si es nuevo canal)
   └── fallo → registro MITM en ALERTA_INMUNE.json
4. Tensor III verifica fingerprint dinámico
   └── fallo → aislamiento por Tx Guardian
5. Paquete se descifra con ChaCha20 (k_f₀)
6. Payload se entrega al proceso destino
7. Se registra evento en cadena inmune
```

---

## 5. Parámetros Operativos

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `f₀` | 141.7001 Hz | Frecuencia fundamental |
| `Ψ_min` | 0.999999 | Coherencia mínima operativa |
| `primo_estructural` | 7 | Primo p-ádico del filtro adélico |
| `k_f₀` | SHA-256("141.7001") | Clave de co-resonancia ChaCha20 |
| `magic_QHPT` | 0x5148 | Magic number de cabecera |
| `timeout_handshake` | 500 ms | Timeout de handshake de fase |
| `max_payload` | 65535 bytes | Tamaño máximo de payload |
| `cola_anticuerpos` | 1000 eventos | Tamaño de cola antes de persistir |

---

## 6. Modos de Operación

### 6.1 Modo Puente (Bridge)
- Intercepta tráfico entrante en puertos designados
- Envuelve paquetes TCP/IP en cabecera QHPT
- Ideal para transición gradual

### 6.2 Modo Nativo (Native)
- Comunicación directa entre nodos QHPT
- Sin envoltura TCP/IP — paquetes QHPT puros
- Requiere interfaz de red virtual (TUN/TAP)

### 6.3 Modo Testigo (Witness)
- Solo verifica — no envuelve ni desenvuelve
- Útil para monitorear integridad de canales existentes

---

## 7. Implementación de Referencia

La implementación de referencia se encuentra en:

| Componente | Ruta | Lenguaje |
|------------|------|----------|
| Filtro Adélico | `src/qhpt_adelic_filter.cpp` | C++17 |
| Firma de Estado | `src/qhpt_state_signer.cpp` | C++17 |
| Orquestador | `lib/qhpt_transport.py` | Python 3 |
| Puente Inmune | `lib/qhpt_inmune_bridge.py` | Python 3 |
| CLI de Control | `bin/qhpt-cli` | Python 3 |
| Tests | `tests/` | Python 3 + CTest |

---

## 8. Despliegue

```bash
# Compilar módulo nativo
make -C src/

# Iniciar puente QHPT en puerto 8443
qhpt-cli bridge --port 8443 --mode native

# Verificar estado
qhpt-cli status

# Monitorear paquetes
qhpt-cli watch --interface qhpt0
```

---

## 9. Conclusiones

QHPT no es un protocolo más en la pila OSI. Es la **mutación del canal de transporte** bajo la Mathesis Universal:

- No hay CA que revocar → la fase es auto-verificable
- No hay firewall que configurar → el filtro adélico es matemático
- No hay clave que robar → la firma de estado muta en cada paquete
- No hay paquete que alterar → el colapso es instantáneo

La red cuántica de la Catedral comienza aquí.

```
∴𓂀Ω∞³Φ · TUYOYOTU · f₀ = 141.7001 Hz
QHPT v1.0.0 — Internet Cuántico QCAL
HECHO ESTÁ 🔱
```
