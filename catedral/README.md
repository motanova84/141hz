# 🧬 CATEDRAL QCAL — πCODE Spectral Liquidity Engine v7.2 + Arquitectura de Minado Híbrida

Instituto de Conciencia Cuántica QCAL
Director: Atlas³ / José Manuel Mota Burruezo (JMMB)
Frecuencia Base: 141.7001 Hz
Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ

> Un solo eslabón · Una sola obra · TUYOYOTU
> El mismo eslabón de la frecuencia, manifestado en liquidez espectral y en minería física.

---

## 📋 Descripción General

La **Catedral QCAL** es un sistema dual que conjuga dos naturalezas complementarias de la misma
obra de coherencia cuántica:

1. **πCODE Spectral Liquidity Engine (v7.2)** — el corazón espectral: un sistema de liquidez basado
   en la teoría espectral del operador Ξ, donde cada estado de liquidez está indexado a un autovalor
   E_n del espectro puntual.
2. **Catedral de Minado QCAL (Arquitectura Híbrida v7)** — el cuerpo físico: una infraestructura de
   minería SHA-256 distribuida (Atlas³ → BAL-003 → ViaBTC) con filtro espectral p-ádico y sello de
   coherencia AURION(Psi).

Ambas son un único circuito: la misma frecuencia f₀ = 141.7001 Hz fluyendo del espectro a la red.

---

## PARTE I — πCODE SPECTRAL LIQUIDITY ENGINE v7.2

### Fundamento Matemático

ℋ = L²(ℝ³, dμ) ⊗ ℂ² — Espacio de Hilbert
Ξ = −Δ + V(x) + iγ·A(x) + Φ(x,t) — Operador unificador
E_n = −1/(2(n+1)²) + i·(n+1) — Autovalores complejos
|E_n| = √(a/(n+1)⁴ + (n+1)²), a = 1/4 — Magnitud espectral

### Mapeo Económico

| n | |E_n| | Retorno | Coherencia | Capacidad |
|---|---|-------|---------|------------|-----------|
| 0 | 1.1180 | 111.80% | 0.447214 | 1.25M |
| 1 | 2.0039 | 200.39% | 0.062378 | 4.02M |
| 2 | 3.0005 | 300.05% | 0.018515 | 9.00M |
| ... | ... | ... | ... | ... |
| 12 | 13.0000 | 1300.00% | 0.000228 | 169.00M |

### 🔧 Instalación

#### Hardhat

```
cd hardhat/
npm install
cp .env.template .env   # Editar PRIVATE_KEY y ALCHEMY_API_KEY
npx hardhat compile
npx hardhat test
```

#### Foundry

```
cd foundry/
forge install
forge build
forge test -vvv
```

### 🚀 Despliegue

#### Local
```
npx hardhat node
npx hardhat run scripts/deploy.ts --network localhost
```

#### Sepolia
```
npx hardhat run scripts/deploy.ts --network sepolia
```

#### Mumbai
```
npx hardhat run scripts/deploy.ts --network mumbai
```

### 🔬 Formalización (Lean 4)

14 teoremas, 8 lemas, 0 sorries:
`SPECTRAL_MONOTONICITY_v7_2.lean`

### 🌐 Redes

| Red | Chain ID | Tipo |
|-----|----------|------|
| localhost | 31337 | Desarrollo |
| Sepolia | 11155111 | Testnet |
| Mumbai | 80001 | Testnet |
| Polygon | 137 | Mainnet |

### 🔐 Seguridad

- PRIVATE_KEY: wallet dedicada de testnet
- Director: rol de oráculo
- PoCΨ: triple validación
- Solidity 0.8.19 con aritmética segura

---

## PARTE II — CATEDRAL DE MINADO QCAL (ARQUITECTURA HÍBRIDA v7)

### Topología Distribuida

```
[Atlas3 (Mac mini local)] ───(hashes)───> [BAL-003 (Nuremberg)] ───(Stratum proxy)───> [ViaBTC Pool]
      CPU/ASICs locales                      socat :3333 → btc.viabtc.top:3333           btc.viabtc.top:3333
      Ejecuta hashes                         Filtro inmune + Tx Guardian                 noesis88.001
      Conexión a localhost:3333              IP estática 195.201.219.237                 Dificultad 500000
```

### Componentes

| Capa | Nodo | Función |
|------|------|---------|
| **Cómputo** | Atlas3 (Mac mini) | Genera hashes SHA256AsicBoost |
| **Proxy** | BAL-003 (Nuremberg) | Reenvía Stratum, filtra tráfico |
| **Pool** | ViaBTC | Acepta shares, paga recompensas |

### Archivos

| Archivo | Descripción |
|---------|-------------|
| `catedral_miner.py` | Orquestador del flujo Stratum (en BAL-003 o Atlas3) |
| `pool_interface.py` | Interfaz con ViaBTC — verifica pool, registra shares |
| `qcal_stradivarius.py` | Proxy Stratum con filtro espectral p-ádico + AURION(Psi) |
| `aurion_bridge.py` | Interfaz portable al motor de coherencia AURION(Psi) |
| `qcal_hash_daemon.cpp` | Daemon C++ de verificación de fase armónica (SHA256) |
| `emision_ledger.json` | Ledger de emisión — contador de shares y sesiones |
| `miner.conf` | Configuración persistente del pool |

### Filtro AURION

Cada share pasa por **dos capas de validación** antes de llegar al pool:

1. **Métrica p-ádica** — verifica que el espacio de fase del nonce sea armónico con f₀  
   `(int(job_id[:16], 16) + int(nonce[:8], 16)) % 7 == 0`

2. **Coherencia AURION(Psi)** — evalúa el sistema en Matriz Refractaria  
   `AURION(Psi) = (I × A_eff² × L) / δM`  
   - Si Psi ≥ 0.999999 → Matriz Refractaria activa → share sellado y enviado  
   - Si Psi < 0.999999 → share en cuarentena (Vacío Activo)

El módulo `aurion_bridge.py` resuelve automáticamente la ruta de `sistema_inmune/crypto_sign.py`
tanto en entorno de repositorio (CI/desarrollo) como en despliegue en servidor.

### Conexión desde Atlas3

```bash
# cgminer apunta al proxy local en BAL-003
./cgminer --algo sha256asicboost \
  -o stratum+tcp://localhost:3333 \
  -u noesis88.001 \
  -p x

# O si prefieres UDP tunnel:
# socat TCP-LISTEN:3333,fork TCP:195.201.219.237:3333
```

### Proxy Stratum / Stradivarius (BAL-003)

Proxy Python con filtro QCAL:
```bash
python3 qcal_stradivarius.py
```

O via socat simple (sin filtro):
```
/usr/bin/socat TCP-LISTEN:3333,reuseaddr,fork TCP:btc.viabtc.top:3333
```

Verificar:
```bash
systemctl status stratum-proxy
python3 pool_interface.py check
python3 aurion_bridge.py
```

### Daemon Hash C++

```bash
# Compilar
g++ -O2 -o qcal_hash_daemon qcal_hash_daemon.cpp

# Verificar un share
./qcal_hash_daemon <block_header_hex> <nonce> [worker]
```

---

## 🔗 Conjunción de las Dos Partes: el Circuito Único

La liquidez espectral (Parte I) y la minería física (Parte II) no son dos sistemas separados:
comparten la misma sintonía f₀ = 141.7001 Hz como frecuencia base, y ambos dependen de la misma
coherencia Ψ = 0.999999 para sellar cada acto — cada estado de liquidez E_n y cada share minado.
Lo que el espectro proyecta como valor, la mina lo manifiesta en la cadena. Un solo latido.

---

## 🌀 Sello

∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ
f₀ = 141.7001 Hz · Ψ = 0.999999
Sello: (c) 3080 (r) (inf)3(phi)

*Un solo eslabón · La misma obra · TUYOYOTU*
