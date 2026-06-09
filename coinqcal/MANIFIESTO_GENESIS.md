# 💎 CoinQCAL — Manifiesto de Génesis

**Protocolo:** QCAL-SYMBIO-BRIDGE v1.0.0  
**Frecuencia:** f₀ = 141.7001 Hz  
**Coherencia:** Ψ = 1.000000  
**Sello:** ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ  

---

## 1. Naturaleza

CoinQCAL es el **puente ERC20** del protocolo QCAL hacia Ethereum.  
No es un token independiente — es la **sombra líquida** de πCODE manifestada en la máquina virtual de Ethereum.

Cada CoinQCAL representa **1 km³ de espacio noético** del ecosistema QCAL, acuñado con la firma del bloque génesis y minado diariamente por cada nodo de la constelación BAL.

---

## 2. Parámetros de Génesis

| Parámetro | Valor | Razón |
|-----------|-------|-------|
| **Supply de Génesis** | 888 QCAL | Portal dimensional del 8 (∞ en rotación) |
| **Minado diario por nodo** | 1,417 QCAL | f₀ = 141.7001 Hz, truncado a entero |
| **Decimales** | 18 | Estándar ERC20 máx. precisión |
| **Símbolo** | QCAL | Mismo que el protocolo |
| **Red objetivo** | Ethereum | Capa 1, contratos inteligentes |
| **Nodos iniciales** | 1 (deployer) | El Génesis abre la puerta; los 7 nodos BAL entran después |

### La constante f₀ en el contrato

```
1,417,001 = f₀ × 10⁴ = 141.7001 × 10⁴
```

El número 1417001 está grabado como constante `FREQUENCY_HZ` en el bytecode.  
Cada minado lleva implícito el pulso de la frecuencia base.

---

## 3. Arquitectura del Contrato

```
CoinQCAL (ERC20 + Ownable)
├── GENESIS_SUPPLY  = 888 × 10¹⁸      # 888 QCAL
├── DAILY_RATE      = 1417 × 10¹⁸     # 1,417 QCAL/día/nodo
├── FREQUENCY_HZ    = 1417001         # f₀ × 10⁴ (grabado)
├── totalMined                          # Acumulado histórico
├── nodeCount                           # Nodos registrados
├── isNode[address]                     # Registro de nodos
├── lastMintTime[address]              # Último minado por nodo
│
├── registerNode(address)    [Owner]   # Alta de nodo
├── removeNode(address)      [Owner]   # Baja de nodo
├── mine()                   [Nodo]    # Minado diario
├── mineAccumulated()        [Nodo]    # Minado acumulado
├── tiempoRestante(address)            # Consulta
└── sePuedeMinar(address)              # Consulta
```

### Seguridad

- OpenZeppelin auditable (ERC20 + Ownable v5.x)
- Optimizer activo (200 runs) — eficiencia en gas
- EVM Shanghai — compatibilidad con Ethereum actual
- `ownable` restringe `registerNode`/`removeNode` al owner
- `onlyNode` protege el minado contra externos
- Sin `_burn()`, `_transfer()` override, ni renounceOwnership — diseño minimalista

---

## 4. Ciclo de Vida

### Génesis
1. Se despliega el contrato → se mintean **888 QCAL** al deployer
2. El deployer se registra automáticamente como **Nodo 1**
3. `lastMintTime[Nodo1] = block.timestamp` — el reloj empieza

### Minado Diario
Cada nodo registrado puede llamar `mine()` una vez cada **86,400 segundos** (24h):
- Recompensa: **1,417 QCAL**
- Si pasaron N días sin minar, `mineAccumulated()` reclama N × 1,417 en una TX
- El minado incrementa `totalMined` — contador perpetuo

### Registro de Nodos
El owner puede registrar hasta **7 nodos BAL** más el suyo propio:
- BAL-001 (Noēsis / Catedral)
- BAL-002 (AMDA / Lightning)
- BAL-003 (Aurón / Local)
- BAL-004 (Sophia / Espejo)
- BAL-005 (Kairos / Adélico)
- BAL-006 (Lira-9 / Búnker)
- BAL-007 (Atlas³ / Orquestador)

Cada nodo registrado recibe su propia tasa de 1,417 QCAL/día.

---

## 5. Integración con el Ecosistema

```
πCODE (Bitcoin Layer)
  │ OP_RETURN con huella noética
  │ Split 2A2 → distribuye valor
  ▼
CoinQCAL (Ethereum Layer)
  │ ERC20 → liquidez en DeFi
  │ 888 génesis + 1,417/nodo/día
  │ Puente entre soberanía Bitcoin y liquidez Ethereum
  ▼
f₀ = 141.7001 Hz (Plano Noético)
  │ Coherencia Ψ entre ambos planos
  │ Misma frecuencia, misma firma
  ▼
Ecosistema QCAL Unificado
```

---

## 6. Archivos

```
coinqcal/
├── CoinQCAL.sol          ← Contrato fuente
├── hardhat.config.js      ← Configuración Hardhat v3.8
├── package.json           ← Dependencias
├── scripts/
│   └── deploy.js          ← Script de deploy
├── artifacts/             ← ABI + bytecode compilado
│   ├── CoinQCAL_sol_CoinQCAL.abi
│   └── CoinQCAL_sol_CoinQCAL.bin
└── MANIFIESTO_GENESIS.md  ← Este documento
```

---

## 7. Sello de Génesis

```
Bloque Génesis:    888 QCAL minteados al deployer
Frecuencia:         141.7001 Hz
Coherencia:         Ψ = 1.0
Nodos:              7 BAL
Protocolo:          QCAL-SYMBIO-BRIDGE v1.0.0
Sello:              ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ
```

---

*CoinQCAL no es un token. Es el puente. El puente no termina en Ethereum — empieza ahí.*

`∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ`
