# 🔱 PILAR DE WALLETS INMUTABLE — CONTROL DIRECTO DEL DIRECTOR

**Fecha de anclaje:** 2026-08-14 · **Root Fingerprint:** `4a96ddf0`

## Nodo Consolidador (ecosistema — BAL-003)
- **CATEDRAL_BAL003** (`bc1qkmyhx4eml9j7c5g6g332kl7vu0hnj9jayhg8lv`) — consolidador de la masa emitida M(cov).

## Terminales del Director (control directo, mismas semillas/raíz, BIP32/44)
| # | Wallet | Red | Dirección / Identificador |
|---|--------|-----|---------------------------|
| 1 | Ledger Nano S/X (fingerprint `4a96ddf0`) | Bitcoin L1 Cold | `bc1qklmax4ezdgtjk3wfkypd0n7w0ksxn6ke0warxs` |
| 2 | BlueWallet | Bitcoin L1 Hot/Liquid | `bc1qk9qywdngajmy4q3lr6zsncq7kzem6wexy7d308` |
| 3 | Wallet of Satoshi | Lightning L2 | `haltingopen426@walletofsatoshi.com` |

## Oráculo PoPC (K_oracle)
- **Curva:** secp256k1 · **Custodia:** clave privada local en BAL-003 (permisos 600), NUNCA publicada.
- **Fingerprint SHA256 (pub):** `4fa2a70a2546dbd557e6c103048a0db97ac78a07a92d10b4b3bfeb3f6911d0f4`
- **Payload firmado:** `SHA256(EventID ‖ cov ‖ ts ‖ 4a96ddf0 ‖ Wallet_Address)`

## Axionas de emisión
- **Genética inmutable:** POPC-000000…000015 = Fase Génesis de Metrología (sin balances).
- **Emisión activa:** desde POPC-000016, solo sobre evento real (cov<1e-4) del canal vivo — jamás sintético.
- **Masa normalizada:** `M(cov) = floor(100 / (cov * 10^4))` πCODE.
- **No-duplicidad:** ninguna clave privada del Director en repo; solo direcciones públicas.

∴𓂀Ω∞³Φ · PILAR DE WALLETS INMUTABLE · ORÁCULO PoPC · TUYOYOTU · f₀=141.7001 Hz · HECHO ESTÁ
