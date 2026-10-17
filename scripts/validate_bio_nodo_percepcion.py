#!/usr/bin/env python3
"""
Validación Completa: Bio-Nodo y Percepción como Invariante Geométrico ∴BNP∞³
═══════════════════════════════════════════════════════════════════════════════
Sello: ∴BNP∞³
F0: 141.7001 Hz

Valida la implementación completa del Bio-Nodo en 4 fases:

    Fase 1: Identidad Espectral — Ĥ_π|Ψ⟩ = γₙ|Ψ⟩
    Fase 2: Toro Adélico — Colapso de órbita del flujo de dilatación
    Fase 3: Invariante de Fase — Ψ(t) ≥ 0.999 (umbral diamantino)
    Fase 4: Punto Fijo Soberano + Sistema Integrado — Certificación ∴BNP∞³

Criterio de éxito:
    - Todas las fases deben pasar (✓)
    - Ψ_global ≥ 0.888 (umbral noético)
    - Ψ_fase ≥ 0.999 (umbral diamantino)
    - Certificado: BNP-BIONODO-VERIFIED

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.bio_nodo_percepcion import (
    # Constantes de módulo
    _F0,
    _PHI,
    _PSI_UMBRAL,
    _PSI_DIAMANTE,
    _ZEROS_20,
    _SELLO,
    _CERT_MARK,
    # Utilidades
    _theta_rs,
    _criba_eratostenes,
    # Clases
    ConstantesBioNodo,
    IdentidadEspectral,
    ToroAdelico,
    MatrizDensidad,
    InvarianteFase,
    PuntoFijoSoberano,
    CoherenciaBioNodo,
    SistemaBioNodo,
    ResultadoBioNodo,
    # API pública
    bio_nodo_percepcion_activar,
)


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades de presentación
# ─────────────────────────────────────────────────────────────────────────────

def separador(titulo: str) -> None:
    print("\n" + "=" * 80)
    print(titulo)
    print("=" * 80)


def check(descripcion: str, condicion: bool, valor: str = "") -> None:
    estado = "✓" if condicion else "✗"
    sufijo = f"  [{valor}]" if valor else ""
    print(f"  {estado} {descripcion}{sufijo}")
    if not condicion:
        raise AssertionError(f"FALLO: {descripcion}")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 1: Identidad Espectral — Ĥ_π|Ψ⟩ = γₙ|Ψ⟩
# ─────────────────────────────────────────────────────────────────────────────

def validacion_fase1_identidad_espectral() -> None:
    separador("FASE 1: Identidad Espectral — Ĥ_π|Ψ⟩ = γₙ|Ψ⟩")

    # 1a. Constantes del módulo
    check("F₀ = 141.7001 Hz",
          abs(_F0 - 141.7001) < 1e-4, f"{_F0:.4f}")
    check("φ = (1+√5)/2 ≈ 1.618034",
          abs(_PHI - 1.618033988) < 1e-6, f"{_PHI:.9f}")
    check("Umbral noético Ψ = 0.888",
          abs(_PSI_UMBRAL - 0.888) < 1e-10, f"{_PSI_UMBRAL}")
    check("Umbral diamantino Ψ = 0.999",
          abs(_PSI_DIAMANTE - 0.999) < 1e-10, f"{_PSI_DIAMANTE}")
    check("20 ceros de Riemann cargados",
          len(_ZEROS_20) == 20, str(len(_ZEROS_20)))
    check("γ₁ ≈ 14.134725",
          abs(_ZEROS_20[0] - 14.134725) < 1e-4, f"{_ZEROS_20[0]:.6f}")
    check("γ₂₀ ≈ 77.144840",
          abs(_ZEROS_20[-1] - 77.144840) < 1e-4, f"{_ZEROS_20[-1]:.6f}")
    check("Sello ∴BNP∞³",
          _SELLO == "∴BNP∞³", _SELLO)
    check("CertMark = BNP-BIONODO-VERIFIED",
          _CERT_MARK == "BNP-BIONODO-VERIFIED")

    # 1b. ConstantesBioNodo
    cte = ConstantesBioNodo()
    check("ConstantesBioNodo.f0 = 141.7001",
          abs(cte.f0 - 141.7001) < 1e-4)
    check("ConstantesBioNodo.n_zeros = 20",
          cte.n_zeros == 20, str(cte.n_zeros))
    check("Resonancia F₀/γ₁ ∈ (10.0, 10.1)",
          10.0 < cte.resonancia_f0_gamma1() < 10.1,
          f"{cte.resonancia_f0_gamma1():.5f}")

    # 1c. IdentidadEspectral: autofunciones y autovalores
    ide = IdentidadEspectral()

    psi_0_at_1 = ide.autoestado(1.0, 0)
    check("ψ₀(1) = 1 + 0i  (x=1 en la autofunción)",
          abs(psi_0_at_1 - complex(1.0, 0.0)) < 1e-10,
          f"{psi_0_at_1:.3f}")

    psi_0_at_e = ide.autoestado(math.e, 0)
    check("|ψ₀(e)| = e^{-1/2} ≈ 0.6065",
          abs(abs(psi_0_at_e) - math.exp(-0.5)) < 1e-6,
          f"|ψ₀| = {abs(psi_0_at_e):.6f}")

    # 1d. Ecuación de autovalores Ĥ_π ψₙ = γₙ ψₙ
    for i in range(5):
        h_psi = ide.aplicar_hamiltoniano(1.0, i)
        gamma_i = _ZEROS_20[i]
        check(f"Ĥ_π ψ_{i}(1) = γ_{i} · 1  (autovalor exacto)",
              abs(h_psi - gamma_i) < 1e-10,
              f"γ_{i} = {gamma_i:.6f}")

    # 1e. Coherencia Ψ_identidad
    psi_id = ide.psi_identidad()
    check(f"Ψ_identidad ≥ 0.99  (coherencia muy alta: F₀/γ₁ ≈ 10.024)",
          psi_id >= 0.99, f"{psi_id:.6f}")

    # 1f. Espectro completo
    espectro = ide.espectro_completo()
    check("Espectro completo tiene 20 autovalores",
          len(espectro) == 20, str(len(espectro)))
    check("Primer autovalor = γ₁",
          abs(espectro[0] - _ZEROS_20[0]) < 1e-10)

    print(f"\n  → Ψ_identidad = {psi_id:.6f}")
    print("  FASE 1: PASS")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 2: Toro Adélico — Colapso de Órbita
# ─────────────────────────────────────────────────────────────────────────────

def validacion_fase2_toro_adelico() -> None:
    separador("FASE 2: Toro Adélico — Colapso de Órbita del Flujo x ↦ e^t x")

    toro = ToroAdelico(n_primos=10)

    # 2a. Flujo de dilatación
    x0 = 2.5
    flujo_t0 = toro.flujo_dilatacion(x0, 0.0)
    check(f"Flujo(x={x0}, t=0) = {x0}  (identidad)",
          abs(flujo_t0 - x0) < 1e-10, f"{flujo_t0:.6f}")

    flujo_ln2 = toro.flujo_dilatacion(x0, math.log(2))
    check(f"Flujo(x={x0}, t=ln 2) = 2·{x0} = {2*x0}  (cierre órbita p=2)",
          abs(flujo_ln2 - 2 * x0) < 1e-10, f"{flujo_ln2:.6f}")

    # 2b. Tiempos de cierre de órbita
    t_p2_k1 = toro.tiempo_orbita_prima(2, 1)
    check("t_closure(p=2, k=1) = ln 2 ≈ 0.6931",
          abs(t_p2_k1 - math.log(2)) < 1e-10, f"{t_p2_k1:.6f}")

    t_p3_k2 = toro.tiempo_orbita_prima(3, 2)
    check("t_closure(p=3, k=2) = 2·ln 3 ≈ 2.1972",
          abs(t_p3_k2 - 2 * math.log(3)) < 1e-10, f"{t_p3_k2:.6f}")

    # 2c. Tiempos de órbita para los 10 primeros primos
    tiempos = toro.tiempos_orbita()
    check("tiempos_orbita() retorna 10 pares (primo, t_closure)",
          len(tiempos) == 10, str(len(tiempos)))
    check("Primer par es (2, ln 2)",
          tiempos[0][0] == 2 and abs(tiempos[0][1] - math.log(2)) < 1e-10,
          f"({tiempos[0][0]}, {tiempos[0][1]:.6f})")

    # 2d. Conteo de Weyl vs empírico
    n_weyl_g20 = toro.conteo_weyl(_ZEROS_20[-1])
    check(f"N_weyl(γ₂₀) ∈ [18, 21]  (aprox. empírico 20)",
          18.0 < n_weyl_g20 < 21.0, f"{n_weyl_g20:.4f}")

    n_emp = toro.conteo_empirico(_ZEROS_20[-1] + 1.0)
    check("conteo_empirico(γ₂₀ + 1) = 20",
          n_emp == 20, str(n_emp))

    # 2e. Coherencia Ψ_toro
    psi_to = toro.psi_toro()
    check(f"Ψ_toro ≥ 0.888  (umbral noético)",
          psi_to >= 0.888, f"{psi_to:.6f}")

    # 2f. MatrizDensidad
    md = MatrizDensidad()
    eps = md.tasa_decoherencia()
    check(f"ε_dec = Σ(1/γₙ)/(N·F₀) > 0",
          eps > 0, f"{eps:.2e}")
    check("ε_dec < 0.001  (tasa de decoherencia muy pequeña)",
          eps < 0.001, f"{eps:.2e}")

    pureza = md.pureza()
    check(f"Tr(ρ²) ≥ 0.999  (estado casi puro)",
          pureza >= 0.999, f"{pureza:.6f}")

    c_off = md.coherencia_offdiagonal()
    check(f"C_off = 1 − 1/N = {1 - 1/20:.4f}  (dominio off-diagonal)",
          abs(c_off - (1 - 1 / 20)) < 1e-10, f"{c_off:.4f}")

    psi_de = md.psi_densidad()
    check(f"Ψ_densidad ≥ 0.888",
          psi_de >= 0.888, f"{psi_de:.6f}")

    print(f"\n  → Ψ_toro     = {psi_to:.6f}")
    print(f"  → Ψ_densidad = {psi_de:.6f}")
    print(f"  → ε_dec      = {eps:.2e}")
    print("  FASE 2: PASS")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 3: Invariante de Fase — Ψ(t) ≥ 0.999
# ─────────────────────────────────────────────────────────────────────────────

def validacion_fase3_invariante_fase() -> None:
    separador("FASE 3: Invariante de Fase — Ψ(t) ≥ 0.999 (Umbral Diamantino)")

    inv = InvarianteFase()

    # 3a. Tasa de decaimiento espectral
    eps = inv.tasa_decaimiento_espectral()
    check("ε_dec > 0  (no trivialmente nulo)",
          eps > 0, f"{eps:.2e}")
    check("ε_dec < 0.001  (sistema altamente coherente)",
          eps < 0.001, f"{eps:.2e}")

    # 3b. Función de coherencia en distintos instantes
    T0 = 1.0 / _F0  # período fundamental
    for t_label, t_val in [("t=0", 0.0), ("t=T₀", T0), ("t=10T₀", 10 * T0)]:
        psi_t = inv.psi_en_t(t_val)
        check(f"Ψ({t_label}) ≥ 0.999  (coherencia constante)",
              psi_t >= 0.999, f"{psi_t:.6f}")

    # 3c. Umbral diamantino
    check("umbral_diamante() = 0.999",
          abs(inv.umbral_diamante() - 0.999) < 1e-10,
          str(inv.umbral_diamante()))

    # 3d. supera_umbral_diamante
    check("supera_umbral_diamante() = True",
          inv.supera_umbral_diamante())

    # 3e. Coherencia Ψ_fase
    psi_fa = inv.psi_fase()
    check(f"Ψ_fase ≥ 0.999  (umbral diamantino alcanzado)",
          psi_fa >= 0.999, f"{psi_fa:.8f}")
    check(f"Ψ_fase ≥ 0.888  (umbral noético)",
          psi_fa >= 0.888, f"{psi_fa:.8f}")

    # 3f. Criba de Eratóstenes (usada por ToroAdelico)
    primos_100 = _criba_eratostenes(100)
    check("25 primos ≤ 100",
          len(primos_100) == 25, str(len(primos_100)))
    check("Último primo ≤ 100 es 97",
          primos_100[-1] == 97)

    print(f"\n  → Ψ_fase     = {psi_fa:.8f}  (umbral diamante = 0.999)")
    print(f"  → ε_dec      = {eps:.2e}  (decoherencia espectral)")
    print("  FASE 3: PASS")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 4: Punto Fijo Soberano + Sistema Integrado
# ─────────────────────────────────────────────────────────────────────────────

def validacion_fase4_punto_fijo_sistema() -> None:
    separador("FASE 4: Punto Fijo Soberano + Sistema Integrado ∴BNP∞³")

    pfs = PuntoFijoSoberano()

    # 4a. Coherencia espectral del punto fijo
    psi_esp = pfs.coherencia_espectral()
    check(f"Ψ_espectral ≥ 0.99  (coherencia alta: F₀/γ₁ ≈ 10.024)",
          psi_esp >= 0.99, f"{psi_esp:.6f}")

    # 4b. Contracción de Banach
    psi_g0 = pfs.contraccion(0.0)
    psi_g1 = pfs.contraccion(1.0)
    check("g(0) > 0  (la contracción avanza desde el origen)",
          psi_g0 > 0, f"{psi_g0:.6f}")
    check("g(Ψ_esp) ≈ Ψ_esp  (punto fijo exacto de la contracción)",
          abs(pfs.contraccion(psi_esp) - psi_esp) < 1e-10,
          f"|g(Ψ_esp) − Ψ_esp| = {abs(pfs.contraccion(psi_esp) - psi_esp):.2e}")

    # 4c. Iteración del punto fijo
    psi_iter = pfs.iterar_punto_fijo()
    psi_exacto = pfs.punto_fijo_exacto()
    check(f"Ψ_N ≈ Ψ* = {psi_exacto:.6f}  (convergencia tras 20 iter.)",
          abs(psi_iter - psi_exacto) < 0.001,
          f"Ψ_N = {psi_iter:.6f}")

    # 4d. Firma QCAL (Blake2b-16)
    datos_test = b"bio_nodo_qcal_signature"
    firma = pfs.firma_qcal(datos_test)
    check("Firma QCAL tiene 32 caracteres hexadecimales",
          len(firma) == 32 and all(c in "0123456789abcdef" for c in firma),
          firma)
    check("Firma QCAL es determinista",
          pfs.firma_qcal(datos_test) == firma)
    check("verificar_firma() válida para datos originales",
          pfs.verificar_firma(firma, datos_test))
    check("verificar_firma() inválida para datos distintos",
          not pfs.verificar_firma(firma, b"datos_alterados"))

    # 4e. Coherencia Ψ_soberania
    psi_so = pfs.psi_soberania()
    check(f"Ψ_soberania ≥ 0.999  (convergencia al punto fijo)",
          psi_so >= 0.999, f"{psi_so:.6f}")

    # 4f. CoherenciaBioNodo — agregador
    coh = CoherenciaBioNodo()
    desglose = coh.desglose()
    for nombre, psi_val in desglose.items():
        if nombre != "psi_global":
            check(f"Ψ_{nombre} ≥ 0.888",
                  psi_val >= 0.888, f"{psi_val:.6f}")
    psi_g_coh = coh.psi_global()
    check(f"Ψ_global (CoherenciaBioNodo) ≥ 0.888",
          psi_g_coh >= 0.888, f"{psi_g_coh:.6f}")

    # 4g. SistemaBioNodo — certificación completa
    sis = SistemaBioNodo()
    cert = sis.certificar()
    psi_g = cert["psi_global"]
    activo = cert["sello_activo"]

    check(f"Ψ_global (SistemaBioNodo) ≥ 0.888",
          psi_g >= 0.888, f"{psi_g:.6f}")
    check("sello_activo = True",
          activo is True)
    check(f"Sello = '∴BNP∞³'",
          cert["sello"] == "∴BNP∞³", cert["sello"])
    check("cert_mark = 'BNP-BIONODO-VERIFIED'",
          cert["cert_mark"] == "BNP-BIONODO-VERIFIED")
    check("supera_umbral_diamante = True",
          cert["supera_umbral_diamante"] is True)
    check("firma_qcal tiene 32 caracteres",
          len(cert["firma_qcal"]) == 32, cert["firma_qcal"])

    # 4h. API pública
    resultado = bio_nodo_percepcion_activar()
    check("API: sello_activo = True",
          resultado["sello_activo"] is True)
    check("API: psi_global ≥ 0.888",
          resultado["psi_global"] >= 0.888, f"{resultado['psi_global']:.6f}")
    check("API: cert_mark = 'BNP-BIONODO-VERIFIED'",
          resultado["cert_mark"] == "BNP-BIONODO-VERIFIED")
    check("API: supera_umbral_diamante = True",
          resultado["supera_umbral_diamante"] is True)

    # 4i. ResultadoBioNodo dataclass
    resultado_dc = ResultadoBioNodo(
        psi_global=psi_g,
        sello_activo=activo,
        sello=_SELLO,
        cert_mark=_CERT_MARK,
        n_zeros=20,
        firma_qcal=cert["firma_qcal"],
    )
    check("ResultadoBioNodo.psi_global ≥ 0.888",
          resultado_dc.psi_global >= 0.888)
    check("ResultadoBioNodo.sello_activo = True",
          resultado_dc.sello_activo is True)

    # 4j. Resumen completo
    print(f"\n  ┌─ RESUMEN DE COHERENCIA ─────────────────────────────────────┐")
    print(f"  │  Ψ_identidad  = {cert['psi_identidad']:.6f}")
    print(f"  │  Ψ_toro       = {cert['psi_toro']:.6f}")
    print(f"  │  Ψ_densidad   = {cert['psi_densidad']:.6f}")
    print(f"  │  Ψ_fase       = {cert['psi_fase']:.6f}  (umbral diamante ≥ 0.999)")
    print(f"  │  Ψ_soberania  = {cert['psi_soberania']:.6f}")
    print(f"  │  ──────────────────────────────────────────────────────────── │")
    print(f"  │  Ψ_global     = {psi_g:.6f}  (umbral: 0.888)")
    print(f"  │  F₀/γ₁        = {cert['resonancia_f0_gamma1']:.6f}  ≈ 10.024")
    print(f"  │  Sello        = {cert['sello']}")
    print(f"  │  Firma QCAL   = {cert['firma_qcal'][:16]}...")
    print(f"  └──────────────────────────────────────────────────────────────┘")
    print("  FASE 4: PASS")


# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  VALIDACIÓN: Bio-Nodo y Percepción como Invariante Geométrico ∴BNP∞³    ║")
    print("║  F0 = 141.7001 Hz  |  Ĥ_π|Ψ⟩ = γₙ|Ψ⟩  |  Ψ_diamante ≥ 0.999         ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝")

    fases = [
        ("FASE 1", validacion_fase1_identidad_espectral),
        ("FASE 2", validacion_fase2_toro_adelico),
        ("FASE 3", validacion_fase3_invariante_fase),
        ("FASE 4", validacion_fase4_punto_fijo_sistema),
    ]

    errores = []
    for nombre, fase_fn in fases:
        try:
            fase_fn()
        except AssertionError as e:
            errores.append(f"{nombre}: {e}")
            print(f"\n  ✗ {nombre}: FALLO — {e}")

    separador("RESULTADO FINAL")
    if errores:
        print(f"\n  ✗ VALIDACIÓN FALLIDA ({len(errores)} errores):")
        for err in errores:
            print(f"    - {err}")
        sys.exit(1)
    else:
        print("\n  ✓ TODAS LAS FASES PASARON")
        print("  ✓ Ψ_global ≥ 0.888 (umbral noético)")
        print("  ✓ Ψ_fase ≥ 0.999 (umbral diamantino)")
        print("  ✓ BNP-BIONODO-VERIFIED")
        print(f"  ✓ Sello: {_SELLO}")
        print("\n  La percepción no es posterior al cálculo:")
        print("  el Bio-Nodo reconoce su propia firma en el espectro del universo.")


if __name__ == "__main__":
    main()
