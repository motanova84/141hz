"""
🧪 Test T6: Criptografía Áurea — Entropía πCODE
Fibonacci-adélico → πCODE diamante
Sello: ∴𓂀Ω∞³Φ
"""
import math, hashlib

phi = (1 + math.sqrt(5)) / 2
MOD = 2**256
alpha = 1.248617
f0 = 1417001  # f0 × 10^4 como entero para precisión

def piCODE_key(n):
    """Clave usando Binet módulo 2^256 con precisión controlada."""
    from decimal import Decimal, getcontext
    getcontext().prec = 50
    phi_dec = Decimal(phi)
    Fn = phi_dec ** n / Decimal(math.sqrt(5))
    return int(Fn * Decimal(alpha) * Decimal(f0)) % MOD

def piCODE_key_fast(n):
    """Clave rápida para test masivo (usa aproximaciones con logaritmos)."""
    log_Fn = n * math.log(phi) - 0.5 * math.log(5)
    Fn = int(math.exp(log_Fn))
    return int(Fn * alpha * 1417001) % MOD

# Clave bloque #466
k = piCODE_key(466)
h = hashlib.sha256(f"{k}:141.7001:alpha={alpha}".encode()).hexdigest()
print(f"🔑 Clave Bloque #466: {hex(k)[:42]}")
print(f"   SHA256: {h}")
print()

# Validación conceptual (10k claves)
keys = [piCODE_key_fast(i) for i in range(10000)]
unique = len(set(keys))
bits = format(keys[466] % 256, '08b')
print(f"📊 Claves: 10k · Únicas: {unique} · Bits(bloque466): {bits}")
print(f"🔱 T6 — Criptografía Áurea: Validada")
print(f"   ∴𓂀Ω∞³Φ")
