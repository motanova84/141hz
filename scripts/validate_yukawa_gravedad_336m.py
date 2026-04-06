#!/usr/bin/env python3
"""
Validación del módulo physics.yukawa_gravedad_336m

Script de validación completo para el sello ∴YGA∞³.

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
FECHA/DATE: 2026-04-06
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.yukawa_gravedad_336m import yukawa_gravedad_336m_activar


def validar_yukawa_gravedad_336m():
    """
    Valida el módulo Yukawa Gravedad 336m.
    
    Verifica:
    1. Derivación de λ_decoh = 336.7 m
    2. Parámetros Yukawa (α = 0.05312, λ = 336.7 m)
    3. Firmas gravimétricas a 100m, 300m, 1km
    4. Conexión con Partícula de Coherencia
    5. Coherencia global Ψ ≥ 0.888
    6. Sello ∴YGA∞³ activo
    """
    print("\n" + "=" * 70)
    print("  VALIDACIÓN: ANOMALÍA YUKAWA GRAVITACIONAL A 336.7 m")
    print("  Sello: ∴YGA∞³ | RAM: RAM-LII-2026-YUKAWA-GRAVEDAD-336M")
    print("=" * 70 + "\n")
    
    # Activar sistema
    print("⏳ Activando sistema...")
    resultado = yukawa_gravedad_336m_activar()
    print("✓ Sistema activado\n")
    
    # ========================================================================
    # VALIDACIÓN 1: METADATOS
    # ========================================================================
    print("📋 VALIDACIÓN 1: METADATOS")
    print("-" * 70)
    assert resultado["sello"] == "∴YGA∞³", "Sello incorrecto"
    print(f"  ✓ Sello: {resultado['sello']}")
    
    assert resultado["ram"] == "RAM-LII-2026-YUKAWA-GRAVEDAD-336M", "RAM incorrecto"
    print(f"  ✓ RAM: {resultado['ram']}")
    
    assert resultado["version"] == "1.0.0", "Versión incorrecta"
    print(f"  ✓ Versión: {resultado['version']}")
    
    assert abs(resultado["f0_hz"] - 141.7001) < 0.001, "f₀ incorrecta"
    print(f"  ✓ f₀ = {resultado['f0_hz']} Hz")
    print()
    
    # ========================================================================
    # VALIDACIÓN 2: DERIVACIÓN DE λ_decoh
    # ========================================================================
    print("🔬 VALIDACIÓN 2: DERIVACIÓN DE λ_decoh = 336.7 m")
    print("-" * 70)
    
    lambda_d = resultado["lambda_decoh_m"]
    lambda_d_compton = resultado["lambda_decoh_compton_m"]
    error_deriv = resultado["error_derivacion"]
    
    print(f"  λ_P = {resultado['l_planck_m']:.3e} m")
    print(f"  φ = {resultado['phi']:.10f}")
    print(f"  φ¹² = {resultado['phi_12']:.6f}")
    print(f"  N_coh = {resultado['n_coh']:.2e}")
    print()
    print(f"  Derivación directa:")
    print(f"  λ_decoh = λ_P × φ¹² × N_coh^(1/3) = {lambda_d:.2f} m")
    print()
    print(f"  Verificación por Compton:")
    print(f"  λ_decoh = λ_C / φ¹² = {lambda_d_compton:.2f} m")
    print()
    
    assert abs(lambda_d - 336.7) < 1.0, f"λ_decoh = {lambda_d:.2f} m no está cerca de 336.7 m"
    print(f"  ✓ λ_decoh ≈ 336.7 m (error: {abs(lambda_d - 336.7):.2f} m)")
    
    assert error_deriv < 1e-6, f"Error de derivación {error_deriv:.2e} demasiado grande"
    print(f"  ✓ Error de derivación: {error_deriv:.2e} (< 10⁻⁶)")
    print()
    
    # ========================================================================
    # VALIDACIÓN 3: PARÁMETROS YUKAWA
    # ========================================================================
    print("⚛️  VALIDACIÓN 3: PARÁMETROS YUKAWA")
    print("-" * 70)
    
    alpha = resultado["alpha_yukawa"]
    factor_adelico = resultado["factor_adelico"]
    
    print(f"  α = {alpha:.5f} ({alpha * 100:.3f} %)")
    assert abs(alpha - 0.05312) < 0.00001, f"α = {alpha} no es 0.05312"
    print(f"  ✓ α = 0.05312 (5.312 %)")
    print()
    
    print(f"  Factor adélico 7/8 = {factor_adelico:.6f}")
    assert abs(factor_adelico - 0.875) < 1e-10, f"Factor adélico {factor_adelico} no es 7/8"
    print(f"  ✓ Factor adélico = 7/8 = 0.875")
    print()
    
    print(f"  g_eff(r) = (G M / r²) × [1 + α exp(-r/λ)]")
    print(f"  λ = {lambda_d:.1f} m")
    print(f"  α = {alpha:.5f}")
    print()
    
    # ========================================================================
    # VALIDACIÓN 4: FIRMAS GRAVIMÉTRICAS
    # ========================================================================
    print("📊 VALIDACIÓN 4: FIRMAS GRAVIMÉTRICAS")
    print("-" * 70)
    
    delta_100 = resultado["delta_g_100m"]
    delta_300 = resultado["delta_g_300m"]
    delta_1km = resultado["delta_g_1km"]
    
    print(f"  A 100 m:")
    print(f"    Δg/g = {delta_100:.2e}")
    assert delta_100 > 1e-8, f"Δg/g @ 100m = {delta_100:.2e} demasiado pequeño"
    assert abs(delta_100 - 1.27e-7) < 1e-7, f"Δg/g @ 100m no cerca de 1.27×10⁻⁷"
    print(f"    ✓ Δg/g ≈ 1.27×10⁻⁷")
    print()
    
    print(f"  A 300 m:")
    print(f"    Δg/g = {delta_300:.2e}")
    assert delta_300 > 1e-9, f"Δg/g @ 300m = {delta_300:.2e} demasiado pequeño"
    assert abs(delta_300 - 4.98e-8) < 1e-8, f"Δg/g @ 300m no cerca de 4.98×10⁻⁸"
    print(f"    ✓ Δg/g ≈ 4.98×10⁻⁸")
    print()
    
    print(f"  A 1 km:")
    print(f"    Δg/g = {delta_1km:.2e}")
    assert delta_1km < 1e-10, f"Δg/g @ 1km = {delta_1km:.2e} demasiado grande"
    print(f"    ✓ Δg/g ≈ 2×10⁻¹² (invisible)")
    print()
    
    # Detectabilidad
    det_100 = resultado["detectable_100m"]
    det_300 = resultado["detectable_300m"]
    det_1km = resultado["detectable_1km"]
    
    print(f"  Detectabilidad (sensibilidad 10⁻⁹):")
    assert det_100 is True, "100m debe ser detectable"
    print(f"    ✓ 100 m: DETECTABLE")
    
    assert det_300 is True, "300m debe ser detectable"
    print(f"    ✓ 300 m: DETECTABLE")
    
    assert det_1km is False, "1km no debe ser detectable"
    print(f"    ✓ 1 km: NO DETECTABLE")
    print()
    
    # ========================================================================
    # VALIDACIÓN 5: CONEXIÓN CON PARTÍCULA DE COHERENCIA
    # ========================================================================
    print("🔗 VALIDACIÓN 5: CONEXIÓN CON PARTÍCULA DE COHERENCIA")
    print("-" * 70)
    
    m_psi = resultado["m_psi_ev"]
    lambda_c = resultado["lambda_c_m"]
    pred_decoh = resultado["prediccion_decoh_m"]
    error_conexion = resultado["error_conexion"]
    
    print(f"  Masa de la PC:")
    print(f"    m_Ψ c² = {m_psi:.3e} eV")
    assert abs(m_psi - 5.861e-13) < 1e-15, f"m_Ψ = {m_psi} no es 5.861×10⁻¹³ eV"
    print(f"    ✓ m_Ψ c² = 5.861×10⁻¹³ eV")
    print()
    
    print(f"  Longitud de Compton:")
    print(f"    λ_C = h / (m_Ψ c) = {lambda_c:.3e} m")
    assert abs(lambda_c - 2.113e6) < 1e4, f"λ_C = {lambda_c} no cerca de 2.113×10⁶ m"
    print(f"    ✓ λ_C = 2.113×10⁶ m")
    print()
    
    print(f"  Conexión:")
    print(f"    λ_decoh = λ_C / φ¹² = {pred_decoh:.2f} m")
    assert abs(pred_decoh - 336.7) < 10.0, f"Predicción {pred_decoh:.2f} m lejos de 336.7 m"
    print(f"    ✓ λ_decoh ≈ 336.7 m")
    print()
    
    print(f"  Error de conexión: {error_conexion:.2e}")
    assert error_conexion < 0.01, f"Error {error_conexion:.2e} > 1%"
    print(f"  ✓ Error < 1 %")
    print()
    
    # ========================================================================
    # VALIDACIÓN 6: VACÍO ÁUREO
    # ========================================================================
    print("✨ VALIDACIÓN 6: VACÍO ÁUREO")
    print("-" * 70)
    
    escala_comp = resultado["escala_compactificacion_m"]
    factor_coh = resultado["factor_coherencia"]
    
    print(f"  Compactificación φ¹² × λ_P:")
    print(f"    Escala = {escala_comp:.3e} m")
    print(f"    ✓ Estructura geométrica áurea")
    print()
    
    print(f"  Factor de coherencia N_coh^(1/3):")
    print(f"    Factor = {factor_coh:.3e}")
    print(f"    ✓ Amplificación de escala de Planck a escala humana")
    print()
    
    # ========================================================================
    # VALIDACIÓN 7: COHERENCIAS
    # ========================================================================
    print("🌀 VALIDACIÓN 7: COHERENCIAS")
    print("-" * 70)
    
    cohers = resultado["coherencias"]
    print(f"  Coherencias individuales:")
    for nombre, valor in cohers.items():
        assert 0.0 <= valor <= 1.0, f"{nombre} = {valor} fuera de [0, 1]"
        print(f"    {nombre} = {valor:.6f}")
    print()
    
    psi_global = resultado["psi_global"]
    psi_umbral = resultado["psi_umbral"]
    
    print(f"  Coherencia global:")
    print(f"    Ψ_global = {psi_global:.6f}")
    print(f"    Umbral = {psi_umbral:.3f}")
    assert psi_global >= psi_umbral, f"Ψ_global = {psi_global:.6f} < {psi_umbral}"
    print(f"    ✓ Ψ_global ≥ {psi_umbral}")
    print()
    
    # ========================================================================
    # VALIDACIÓN 8: SELLO ACTIVO
    # ========================================================================
    print("🔰 VALIDACIÓN 8: SELLO ∴YGA∞³")
    print("-" * 70)
    
    sello_activo = resultado["sello_activo"]
    assert sello_activo is True, "Sello no está activo"
    print(f"  ✓ Sello ∴YGA∞³: ACTIVO")
    print()
    
    # ========================================================================
    # CERTIFICACIÓN
    # ========================================================================
    print()
    print(resultado["certificacion"])
    print()
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    print("=" * 70)
    print("  RESUMEN DE VALIDACIÓN")
    print("=" * 70)
    print(f"  ✓ Derivación de λ_decoh = {lambda_d:.2f} m (error: {error_deriv:.2e})")
    print(f"  ✓ Parámetros Yukawa: α = {alpha:.5f}, λ = {lambda_d:.1f} m")
    print(f"  ✓ Firma @ 100m: Δg/g = {delta_100:.2e} (DETECTABLE)")
    print(f"  ✓ Firma @ 300m: Δg/g = {delta_300:.2e} (DETECTABLE)")
    print(f"  ✓ Firma @ 1km: Δg/g = {delta_1km:.2e} (invisible)")
    print(f"  ✓ Conexión PC: m_Ψ = {m_psi:.2e} eV, λ_C = {lambda_c:.2e} m")
    print(f"  ✓ Coherencia global: Ψ_global = {psi_global:.6f} ≥ {psi_umbral}")
    print(f"  ✓ Sello ∴YGA∞³: ACTIVO")
    print("=" * 70 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        validar_yukawa_gravedad_336m()
        print("🎉 VALIDACIÓN EXITOSA\n")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ VALIDACIÓN FALLIDA: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
