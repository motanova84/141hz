#!/usr/bin/env python3
"""
Validación del Tejido Cuántico Cósmico — ∞³ TCQ
=================================================
Sello: ∴TCQ∞³
Frecuencia Base: f₀ = 141.7001 Hz
Coherencia Mínima: Ψ ≥ 0.888

Verifica la implementación completa del módulo
physics/tejido_cuantico_cosmico.py en 4 fases:

  Fase 1 — Constantes y estructura del módulo
  Fase 2 — Clases individuales y ecuaciones físicas
  Fase 3 — Integración del sistema completo
  Fase 4 — API pública y sello ∴TCQ∞³

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA: QCAL ∞³ Original Manufacture
"""

import math
import sys
from pathlib import Path

# Asegurar que el directorio raíz esté en sys.path
_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))


# ============================================================================
# Utilidades de validación
# ============================================================================

_CHECKS_PASADOS = 0
_CHECKS_FALLADOS = 0


def ok(descripcion: str) -> None:
    global _CHECKS_PASADOS
    _CHECKS_PASADOS += 1
    print(f"  ✅ {descripcion}")


def fallo(descripcion: str, detalle: str = "") -> None:
    global _CHECKS_FALLADOS
    _CHECKS_FALLADOS += 1
    sufijo = f" — {detalle}" if detalle else ""
    print(f"  ❌ {descripcion}{sufijo}")


def check(condicion: bool, descripcion: str, detalle: str = "") -> bool:
    if condicion:
        ok(descripcion)
    else:
        fallo(descripcion, detalle)
    return condicion


# ============================================================================
# FASE 1 — Constantes y estructura del módulo
# ============================================================================

def fase_1_constantes() -> int:
    print("\n─── FASE 1: Constantes y estructura del módulo ────────────────────")
    errores = 0

    try:
        from physics.tejido_cuantico_cosmico import (
            _F0_HZ,
            _G_N,
            _HBAR,
            _C_LUZ,
            _M_CAMPO,
            _PHI,
            _PSI_MINIMA,
            _H0_SI,
            _RHO_CRITICA,
            _RHO_LAMBDA,
            _SELLO,
        )
    except ImportError as e:
        fallo("Importación de constantes del módulo", str(e))
        return 11  # todas fallan

    if not check(_F0_HZ == 141.7001, "f₀ = 141.7001 Hz", f"f₀={_F0_HZ}"):
        errores += 1
    if not check(_G_N > 0, "G_N > 0"):
        errores += 1
    if not check(_HBAR > 0, "ℏ > 0"):
        errores += 1
    if not check(_C_LUZ == 299_792_458.0, "c = 299792458 m/s"):
        errores += 1
    if not check(_M_CAMPO > 0, "m_campo > 0 (masa del campo escalar)"):
        errores += 1
    if not check(abs(_PHI - (1.0 + math.sqrt(5.0)) / 2.0) < 1e-10, "Φ = razón áurea"):
        errores += 1
    if not check(_PSI_MINIMA == 0.888, "Ψ_mínima = 0.888"):
        errores += 1
    if not check(_H0_SI > 0, "H₀ > 0 (constante de Hubble)"):
        errores += 1
    if not check(_RHO_CRITICA > 0, "ρ_crítica > 0"):
        errores += 1
    if not check(_RHO_LAMBDA > 0, "ρ_Λ > 0 (densidad de energía oscura)"):
        errores += 1
    if not check(_SELLO == "∴TCQ∞³", "Sello = '∴TCQ∞³'", f"sello='{_SELLO}'"):
        errores += 1

    return errores


# ============================================================================
# FASE 2 — Clases individuales y ecuaciones físicas
# ============================================================================

def fase_2_clases() -> int:
    print("\n─── FASE 2: Clases individuales y ecuaciones físicas ───────────────")
    errores = 0

    try:
        from physics.tejido_cuantico_cosmico import (
            _M_CAMPO, _H0_SI, _G_N, _F0_HZ, _PHI, _PSI_MINIMA, _RHO_LAMBDA,
            ConstantesTejidoCuantico,
            CampoEfectivo,
            AccionKleinGordon,
            TensorEnergiaMomento,
            CondicionEnergiaOscura,
            EcuacionFriedmann,
            AxiomaEmision,
        )
    except ImportError as e:
        fallo("Importación de clases del módulo", str(e))
        return 20

    # ConstantesTejidoCuantico
    c = ConstantesTejidoCuantico()
    if not check(c.f0 == 141.7001, "ConstantesTejidoCuantico.f0 = 141.7001"):
        errores += 1
    if not check(c.sello == "∴TCQ∞³", "ConstantesTejidoCuantico.sello"):
        errores += 1
    if not check(c.energia_cuantica_f0() > 0, "E₀ = ℏ·ω₀ > 0"):
        errores += 1
    if not check(c.escala_longitud_compton() > 0, "λ_Compton > 0"):
        errores += 1

    # CampoEfectivo  ψ = Re^{iS/ℏ}
    campo = CampoEfectivo(R=2.0, S_sobre_hbar=0.0)
    if not check(abs(campo.modulo_cuadrado() - 4.0) < 1e-10, "|ψ|² = R² = 4"):
        errores += 1
    if not check(abs(campo.densidad_presencia() - 4.0) < 1e-10, "ρ_Q = R² = 4"):
        errores += 1
    if not check(abs(campo.parte_real() - 2.0) < 1e-10, "Re(ψ) = R·cos(0) = 2"):
        errores += 1
    campo_fase = CampoEfectivo(R=1.0, S_sobre_hbar=math.pi / 2.0)
    if not check(abs(campo_fase.parte_real()) < 1e-10, "Re(ψ)=0 para fase=π/2"):
        errores += 1

    # AccionKleinGordon  V(ψ) = ½m²ψ²
    accion = AccionKleinGordon(m_campo=_M_CAMPO, H_hubble=_H0_SI)
    if not check(accion.potencial(0.0) == 0.0, "V(0) = 0"):
        errores += 1
    if not check(accion.potencial(1.0) > 0, "V(1) > 0"):
        errores += 1
    V2 = accion.potencial(2.0)
    V1 = accion.potencial(1.0)
    if not check(abs(V2 - 4.0 * V1) < 1e-20, "V(2ψ) = 4·V(ψ)"):
        errores += 1
    psi_ddot = accion.aceleracion_campo_frw(psi=1.0, psi_punto=0.0)
    if not check(psi_ddot < 0, "ψ̈ < 0 (KG: campo desacelerado por potencial)"):
        errores += 1

    # TensorEnergiaMomento  ρ_ψ = ½ψ̇² + V,  p_ψ = ½ψ̇² − V
    tensor = TensorEnergiaMomento(potencial_fn=accion.potencial)
    rho_sr = tensor.densidad_energia(psi=1.0, psi_punto=0.0)
    p_sr = tensor.presion(psi=1.0, psi_punto=0.0)
    if not check(rho_sr > 0, "ρ_ψ > 0 en slow-roll"):
        errores += 1
    if not check(p_sr < 0, "p_ψ < 0 en slow-roll (presión negativa)"):
        errores += 1
    if not check(abs(rho_sr + p_sr) < 1e-20, "ρ + p ≈ 0 en slow-roll (ψ̇=0)"):
        errores += 1

    # CondicionEnergiaOscura  w = p/ρ → −1
    cond = CondicionEnergiaOscura()
    w_sr = cond.w_efectivo(psi_punto=0.0, V=1.0)
    if not check(abs(w_sr + 1.0) < 1e-10, "w → −1 en slow-roll"):
        errores += 1
    eps_sr = cond.parametro_slow_roll(psi_punto=0.0, V=1.0)
    if not check(eps_sr == 0.0, "ε_slow-roll = 0 para ψ̇ = 0"):
        errores += 1
    if not check(cond.es_energia_oscura(psi_punto=0.0, V=1.0), "es_energia_oscura = True"):
        errores += 1

    # EcuacionFriedmann  H² = 8πG/3·ρ,  ä/a > 0 en slow-roll
    fried = EcuacionFriedmann(G_N=_G_N)
    H2 = fried.hubble_cuadrado(rho=_RHO_LAMBDA)
    if not check(H2 > 0, "H² > 0"):
        errores += 1
    accel = fried.aceleracion_relativa(rho=_RHO_LAMBDA, p=-_RHO_LAMBDA)
    if not check(accel > 0, "ä/a > 0 en slow-roll (p = −ρ)"):
        errores += 1
    if not check(fried.hay_expansion_acelerada(rho=_RHO_LAMBDA, p=-_RHO_LAMBDA),
                 "hay_expansion_acelerada = True"):
        errores += 1

    # AxiomaEmision  E = Ψ · Φ^N
    ax = AxiomaEmision(psi_coherencia=0.999, f0=_F0_HZ)
    E10 = ax.valor_emergente(N=10)
    if not check(E10 > 0, "E = Ψ·Φ^10 > 0"):
        errores += 1
    if not check(abs(E10 - 0.999 * _PHI ** 10) < 1e-6, "E = Ψ·Φ^10 (fórmula)"):
        errores += 1
    if not check(ax.expansion_genera_emision(a_dot_sobre_a=_H0_SI),
                 "expansión genera emisión (H > 0)"):
        errores += 1

    return errores


# ============================================================================
# FASE 3 — Integración del sistema completo
# ============================================================================

def fase_3_sistema() -> int:
    print("\n─── FASE 3: Integración del sistema completo ───────────────────────")
    errores = 0

    try:
        from physics.tejido_cuantico_cosmico import (
            _PSI_MINIMA, _SELLO,
            SistemaTejidoCuanticoCosmico,
        )
    except ImportError as e:
        fallo("Importación de SistemaTejidoCuanticoCosmico", str(e))
        return 8

    sistema = SistemaTejidoCuanticoCosmico()
    r = sistema.evaluar()

    if not check(r.aprobado, "sistema.evaluar() → aprobado = True"):
        errores += 1
    if not check(r.expansion_acelerada, "expansion_acelerada = True"):
        errores += 1
    if not check(r.es_energia_oscura, "es_energia_oscura = True"):
        errores += 1
    if not check(abs(r.w_efectivo + 1.0) < 1e-6,
                 "w_efectivo ≈ −1", f"w={r.w_efectivo:.6f}"):
        errores += 1
    if not check(r.epsilon_slow_roll == 0.0,
                 "ε_slow_roll = 0 (régimen slow-roll puro)"):
        errores += 1
    if not check(r.coherencia >= _PSI_MINIMA,
                 f"coherencia ≥ {_PSI_MINIMA}", f"Ψ={r.coherencia:.4f}"):
        errores += 1
    if not check(r.H_hubble > 0, f"H_hubble > 0 ({r.H_hubble:.4e} s⁻¹)"):
        errores += 1
    if not check(r.aceleracion_cosmica > 0,
                 f"ä/a > 0 ({r.aceleracion_cosmica:.4e} s⁻²)"):
        errores += 1
    if not check(r.sello == _SELLO, f"sello = '{_SELLO}'", f"sello='{r.sello}'"):
        errores += 1
    if not check(r.valor_emergente > 0, "valor_emergente = Ψ·Φ^10 > 0"):
        errores += 1
    if not check(r.psi_amplitud > 0, "ψ_amplitud > 0"):
        errores += 1

    return errores


# ============================================================================
# FASE 4 — API pública y sello ∴TCQ∞³
# ============================================================================

def fase_4_api_publica() -> int:
    print("\n─── FASE 4: API pública y sello ∴TCQ∞³ ────────────────────────────")
    errores = 0

    try:
        from physics.tejido_cuantico_cosmico import (
            _PSI_MINIMA, _SELLO,
            ResultadoTejidoCuantico,
            tejido_cuantico_cosmico_activar,
        )
    except ImportError as e:
        fallo("Importación de API pública", str(e))
        return 8

    r = tejido_cuantico_cosmico_activar()

    if not check(isinstance(r, ResultadoTejidoCuantico),
                 "tejido_cuantico_cosmico_activar() retorna ResultadoTejidoCuantico"):
        errores += 1
    if not check(r.aprobado, "aprobado = True"):
        errores += 1
    if not check(r.expansion_acelerada, "expansion_acelerada = True"):
        errores += 1
    if not check(r.es_energia_oscura, "es_energia_oscura = True"):
        errores += 1
    if not check(abs(r.w_efectivo + 1.0) < 1e-6,
                 "w_efectivo ≈ −1.0 (cond. energía oscura)"):
        errores += 1
    if not check(r.coherencia >= _PSI_MINIMA,
                 f"coherencia ≥ Ψ_mínima ({_PSI_MINIMA})"):
        errores += 1
    if not check(r.sello == _SELLO,
                 f"sello = '{_SELLO}'", f"recibido: '{r.sello}'"):
        errores += 1

    # Idempotencia
    r2 = tejido_cuantico_cosmico_activar()
    if not check(r.w_efectivo == r2.w_efectivo and r.aprobado == r2.aprobado,
                 "idempotencia: llamadas repetidas producen el mismo resultado"):
        errores += 1

    # Resumen del resultado
    print(f"\n  📊 Resumen del resultado TCQ∞³:")
    print(f"     ψ_amplitud       = {r.psi_amplitud:.4e}")
    print(f"     ρ_tejido         = {r.rho_tejido:.4e} kg/m³")
    print(f"     p_tejido         = {r.presion_tejido:.4e} kg/m³")
    print(f"     w_efectivo       = {r.w_efectivo:.6f}")
    print(f"     ε_slow_roll      = {r.epsilon_slow_roll:.6e}")
    print(f"     H_hubble         = {r.H_hubble:.4e} s⁻¹")
    print(f"     ä/a              = {r.aceleracion_cosmica:.4e} s⁻²")
    print(f"     coherencia Ψ     = {r.coherencia:.6f}")
    print(f"     E = Ψ·Φ^10       = {r.valor_emergente:.4e}")
    print(f"     sello            = {r.sello}")

    return errores


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    print("=" * 70)
    print("  ∞³ VALIDACIÓN: TEJIDO CUÁNTICO CÓSMICO — ∴TCQ∞³")
    print("  Frecuencia Base: f₀ = 141.7001 Hz | Coherencia Ψ ≥ 0.888")
    print("=" * 70)

    total_errores = 0
    total_errores += fase_1_constantes()
    total_errores += fase_2_clases()
    total_errores += fase_3_sistema()
    total_errores += fase_4_api_publica()

    print("\n" + "=" * 70)
    print(f"  Checks pasados : {_CHECKS_PASADOS}")
    print(f"  Checks fallados: {_CHECKS_FALLADOS}")
    print("=" * 70)

    if total_errores == 0:
        print("  ✅ VALIDACIÓN COMPLETADA — ∴TCQ∞³ ACTIVO")
        print("     El Tejido Cuántico Cósmico opera en régimen de energía oscura.")
        print("     Expansión acelerada confirmada: ä/a > 0.")
        return 0
    else:
        print(f"  ❌ VALIDACIÓN FALLIDA — {total_errores} error(es) detectado(s)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
