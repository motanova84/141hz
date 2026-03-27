"""
Validation script for physics.limite_ruido_disparo

Verifica en 4 fases el análisis IRS-Luna:
  Fase 1 – Parámetros del Láser (Φ_P, E_fotón)
  Fase 2 – Límite de Ruido de Disparo (δφ_SNL, brecha en décadas)
  Fase 3 – Multiplicador de Cooperatividad (G_req, 2F/π, ξ)
  Fase 4 – Ecuación de Viscosidad del Vacío (Δf_crítico) y estado final

Uso:
    python scripts/validate_limite_ruido_disparo.py
"""

import math
import sys
from pathlib import Path

# Ajuste de ruta para importar desde la raíz del repositorio
_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from physics.limite_ruido_disparo import (
    ParametrosLaser,
    LimiteRuidoDisparo,
    MultiplicadorCooperatividad,
    EcuacionViscosidadVacio,
    SistemaIRSLuna,
    limite_ruido_disparo_calcular,
    _PHI_P,
    _DELTA_PHI_SNL,
    _G_REQ,
    _FACTOR_FINEZA,
    _XI,
    _DELTA_F_CRITICO,
    _CONFIANZA_SIGMA,
    _TIEMPO_DETECCION_H,
)

# ────────────────────────────────────────────────────────────────────────────
# Utilidades de validación
# ────────────────────────────────────────────────────────────────────────────

_PASS = "✅ PASS"
_FAIL = "❌ FAIL"
_errors: list[str] = []


def check(condicion: bool, descripcion: str) -> None:
    estado = _PASS if condicion else _FAIL
    print(f"  {estado}  {descripcion}")
    if not condicion:
        _errors.append(descripcion)


def titulo(fase: str) -> None:
    ancho = 72
    print()
    print("─" * ancho)
    print(f"  {fase}")
    print("─" * ancho)


# ────────────────────────────────────────────────────────────────────────────
# FASE 1 – Parámetros del Láser
# ────────────────────────────────────────────────────────────────────────────

titulo("FASE 1 – Parámetros del Láser de 100 W (Nd:YAG, 1064 nm)")

laser = ParametrosLaser()

phi_p = laser.flujo_fotones()
e_J = laser.energia_foton_J()
e_eV = laser.energia_foton_eV()
f_laser = laser.frecuencia_laser_hz()

check(5.3e20 < phi_p < 5.4e20,
      f"Φ_P = {phi_p:.3e} /s  (esperado ≈ 5,36×10²⁰ /s)")
check(1.86e-19 < e_J < 1.88e-19,
      f"E_fotón = {e_J:.3e} J  (esperado ≈ 1,867×10⁻¹⁹ J)")
check(1.16 < e_eV < 1.17,
      f"E_fotón = {e_eV:.4f} eV  (esperado ≈ 1,165 eV)")
check(2.8e14 < f_laser < 2.9e14,
      f"f_láser = {f_laser:.3e} Hz  (esperado ≈ 2,82×10¹⁴ Hz)")
check(abs(e_J / (phi_p * 1.0) - laser.potencia_w / phi_p) < 1e-30,
      "Consistencia: E_fotón × Φ_P = P_láser")

print(f"\n  Φ_P constante del módulo: {_PHI_P:.4e} /s")

# ────────────────────────────────────────────────────────────────────────────
# FASE 2 – Límite de Ruido de Disparo (SNL)
# ────────────────────────────────────────────────────────────────────────────

titulo("FASE 2 – Límite de Ruido de Disparo (δφ_SNL = 1/√(η·Φ_P·τ))")

snl = LimiteRuidoDisparo()

delta_phi = snl.delta_phi_snl()
n_fotones = snl.fotones_detectados()
brecha = snl.brecha_ordenes_magnitud()
razon = snl.snl_sobre_senyal()

check(1.0e-13 < delta_phi < 2.0e-13,
      f"δφ_SNL = {delta_phi:.3e} rad  (rango esperado: [1×10⁻¹³, 2×10⁻¹³])")
check(n_fotones > 1.0e24,
      f"Fotones detectados N = {n_fotones:.3e}  (> 10²⁴)")
check(5.0 < brecha < 7.0,
      f"Brecha = {brecha:.2f} décadas  (esperado ≈ 6 órdenes de magnitud)")
check(razon > 1.0,
      f"δφ_SNL/Δθ_celda = {razon:.3e}  (> 1 → se requiere ganancia)")

# Verificación de la fórmula: δφ² × N = 1
producto = delta_phi**2 * n_fotones
check(abs(producto - 1.0) < 1.0e-8,
      f"Verificación fórmula: δφ²·N = {producto:.6f}  (debe ser 1.000)")

print(f"\n  δφ_SNL constante del módulo: {_DELTA_PHI_SNL:.4e} rad")

# ────────────────────────────────────────────────────────────────────────────
# FASE 3 – Multiplicador de Cooperatividad
# ────────────────────────────────────────────────────────────────────────────

titulo("FASE 3 – Multiplicador de Cooperatividad (G_req, 2F/π, ξ)")

mc = MultiplicadorCooperatividad()

g_req = mc.g_req()
factor_f = mc.factor_fineza()
coop = mc.cooperatividad_red()
xi = mc.xi()
generoso = mc.umbral_generoso()

check(g_req > 1.0e5,
      f"G_req = {g_req:.3e}  (> 10⁵, ganancia Dicke requerida)")
check(6.3e5 < factor_f < 6.4e5,
      f"2F/π = {factor_f:.3e}  (esperado ≈ 6,37×10⁵ para F=10⁶)")
check(coop > 0.0,
      f"Cooperatividad de red = {coop:.4f}  (> 0)")
check(0.0 < xi < 1.0,
      f"ξ = {xi:.6f}  (umbral sub-unitario: 0 < ξ < 1)")
check(generoso,
      f"Umbral generoso (ξ < 1): {generoso}")

# Consistencia: G_req = factor_fineza × cooperatividad × n_celdas
g_reconstruct = factor_f * coop
check(abs(g_reconstruct - g_req) / g_req < 1.0e-10,
      f"Consistencia: 2F/π × coop_red = {g_reconstruct:.4e} ≈ G_req")

print(f"\n  _G_REQ módulo:        {_G_REQ:.4e}")
print(f"  _FACTOR_FINEZA módulo: {_FACTOR_FINEZA:.4e}")
print(f"  _XI módulo:           {_XI:.6f}")

# ────────────────────────────────────────────────────────────────────────────
# FASE 4 – Ecuación de Viscosidad del Vacío y Estado Final
# ────────────────────────────────────────────────────────────────────────────

titulo("FASE 4 – Viscosidad del Vacío y Estado IRS-Luna")

evv = EcuacionViscosidadVacio()

delta_f = evv.delta_f_critico()
umbral_ok = evv.umbral_coherencia_satisfecho(0.0)
ratio_at_threshold = evv.ratio_deriva_umbral(delta_f)

check(delta_f > 0.0,
      f"Δf_crítico = {delta_f:.3e} Hz  (> 0, umbral definido)")
check(umbral_ok,
      "Coherencia con deriva=0 satisface el umbral")
check(abs(ratio_at_threshold - 1.0) < 1.0e-10,
      f"ratio_deriva_umbral(Δf_crítico) = {ratio_at_threshold:.6f}  (debe ser 1)")

# Resultado unificado vía API pública
result = limite_ruido_disparo_calcular()

check(result["senyal_localizada"],
      "API pública → senyal_localizada = True")
check(result["umbral_generoso"],
      "API pública → umbral_generoso = True")
check(result["confianza_sigma"] >= 5.0,
      f"Confianza = {result['confianza_sigma']}σ  (≥ 5σ)")
check(result["tiempo_deteccion_h"] > 0.0,
      f"Tiempo estimado de detección = {result['tiempo_deteccion_h']} h")

print(f"\n  Δf_crítico módulo: {_DELTA_F_CRITICO:.3e} Hz")
print(f"  Confianza:         {_CONFIANZA_SIGMA}σ")
print(f"  T_detección:       {_TIEMPO_DETECCION_H} h")
print(f"\n  Mensaje del sistema:")
print(f"  {result['mensaje']}")

# ────────────────────────────────────────────────────────────────────────────
# Resumen final
# ────────────────────────────────────────────────────────────────────────────

print()
print("═" * 72)
if not _errors:
    print("  ✅ VALIDACIÓN COMPLETA — 4/4 fases superadas sin errores")
    print(f"  IRS-Luna: SEÑAL LOCALIZADA | Confianza {_CONFIANZA_SIGMA}σ | "
          f"T_det ≈ {_TIEMPO_DETECCION_H} h")
    sys.exit(0)
else:
    print(f"  ❌ VALIDACIÓN FALLIDA — {len(_errors)} condición(es) no satisfecha(s):")
    for err in _errors:
        print(f"     • {err}")
    sys.exit(1)
