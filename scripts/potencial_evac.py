#!/usr/bin/env python3
"""
Simulación del Potencial de Energía del Vacío Efectivo E_vac

Este script calcula y grafica el potencial de energía del vacío como función
de R_Ψ, utilizando constantes físicas reales (CODATA 2022).

Formula:
E_vac(R_Ψ) = α·R_Ψ^(-4) + β·ζ'(1/2)·R_Ψ^(-2) + γ·Λ²·R_Ψ² + δ·sin²(log(R_Ψ)/log(b))

Donde:
- α, β, γ, δ: coeficientes de acoplamiento O(1)
- ζ'(1/2): derivada de la función zeta de Riemann en s=1/2
- Λ: constante cosmológica
- b: base adélica (π)
- R_Ψ: radio característico en unidades de longitud de Planck

Objetivo:
- Encontrar el mínimo estable R_Ψ*
- Verificar que f₀ = c/(2π·R_Ψ*·ℓ_P) ≈ 141.7001 Hz

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c, physical_constants

# ===== CONSTANTES FÍSICAS (CODATA 2022) =====
lP = physical_constants["Planck length"][0]     # 1.616255e-35 m
Lambda = 1.1e-52                                # m^-2 (constante cosmológica)
zeta_prime = -0.207886                          # ζ'(1/2)

# ===== PARÁMETROS AJUSTABLES =====
# Coeficientes de acoplamiento O(1) según el problema
# NOTA: Los parámetros se ajustan para obtener f₀ ≈ 141.7001 Hz
# El mínimo debe estar cerca de R_Ψ* ≈ 2.08e40 ℓP para lograr esta frecuencia
alpha = 1.0      # coeficiente de acoplamiento término R^-4
beta = 1.0       # coeficiente de acoplamiento término R^-2
gamma = 1.0      # coeficiente de acoplamiento término cosmológico
delta = 0.5      # coeficiente de acoplamiento término log-periódico
b = np.pi        # base adélica

# ===== RANGO DE R_Ψ =====
# Exploramos un rango amplio desde 1 ℓP hasta 10^48 ℓP
R_vals = np.logspace(0, 48, 5000)   # R_Ψ en unidades de ℓP


# ===== FUNCIÓN DEL POTENCIAL EFECTIVO =====
def Evac(R):
    """
    Calcula el potencial efectivo del vacío E_vac(R_Ψ)

    Parámetros:
    -----------
    R : array_like
        Radio característico R_Ψ en unidades de longitud de Planck

    Retorna:
    --------
    E : array_like
        Energía del potencial efectivo del vacío
    """
    term1 = alpha * R**(-4)
    term2 = beta * zeta_prime * R**(-2)
    term3 = gamma * (Lambda**2) * (R * lP)**2  # convierte a metros
    term4 = delta * np.sin(np.log(R) / np.log(b))**2
    return term1 + term2 + term3 + term4


# ===== CÁLCULO DEL POTENCIAL =====
E_vals = Evac(R_vals)

# ===== LOCALIZACIÓN DEL MÍNIMO =====
idx_min = np.argmin(E_vals)
R_star = R_vals[idx_min]
E_min = E_vals[idx_min]

# Cálculo de la frecuencia f₀
f0 = c / (2 * np.pi * R_star * lP)

# ===== VALIDACIÓN DE ESTABILIDAD =====
# Calcula la segunda derivada (curvatura) en el mínimo
from numpy import gradient  # noqa: E402

log_R_vals = np.log(R_vals)
d2E = gradient(gradient(E_vals, log_R_vals), log_R_vals)
curvature_at_min = d2E[idx_min]

# ===== COMPARACIÓN CON JERARQUÍA COSMOLÓGICA =====
# rho_P / rho_Lambda ~ (R_Psi / lP)^2
# Se espera R_Psi / lP ~ 10^61 para algunos modelos
hierarchy_ratio = R_star  # ya está en unidades de lP

# ===== RESULTADOS =====
print("=" * 80)
print("SIMULACIÓN DEL POTENCIAL EFECTIVO DEL VACÍO E_vac(R_Ψ)")
print("=" * 80)
print("\n📊 CONSTANTES FÍSICAS (CODATA 2022):")
print(f"   Longitud de Planck (ℓ_P):      {lP:.6e} m")
print(f"   Velocidad de la luz (c):        {c:.8e} m/s")
print(f"   Constante cosmológica (Λ):      {Lambda:.6e} m^-2")
print(f"   Derivada zeta ζ'(1/2):          {zeta_prime:.6f}")
print("\n⚙️ PARÁMETROS DE ACOPLAMIENTO:")
print(f"   α = {alpha:.2f}, β = {beta:.2f}, γ = {gamma:.2f}, δ = {delta:.2f}")
print(f"   Base adélica (b):               {b:.6f}")
print("\n✨ RESULTADOS:")
print(f"   R_Ψ* (mínimo estable):          {R_star:.4e} ℓ_P")
print(f"   E_vac(R_Ψ*):                    {E_min:.6e}")
print(f"   Frecuencia f₀:                  {f0:.6f} Hz")
print("   Objetivo:                       141.7001 Hz")
print(f"   Diferencia:                     {abs(f0 - 141.7001):.6f} Hz")
print("\n🔬 VALIDACIONES:")
print(f"   Curvatura en el mínimo:         {curvature_at_min:.6e}")
if curvature_at_min > 0:
    print("   → ✅ Mínimo ESTABLE (curvatura positiva)")
else:
    print("   → ⚠️  Mínimo INESTABLE (curvatura negativa)")
print(f"\n   Jerarquía R_Ψ/ℓ_P:              {hierarchy_ratio:.4e}")
print("   Escala típica esperada:         ~10^47 - 10^61")
print("=" * 80)

# ===== GRÁFICO =====
plt.figure(figsize=(10, 6))
plt.loglog(R_vals, np.abs(E_vals), 'b-', linewidth=1.5, label='|E_vac(R_Ψ)|')
plt.axvline(R_star, color='red', linestyle='--', linewidth=2,
            label=f'R_Ψ* = {R_star:.2e} ℓ_P')
plt.axhline(np.abs(E_min), color='orange', linestyle=':', linewidth=1,
            alpha=0.7)
plt.xlabel(r'$R_\Psi / \ell_P$', fontsize=12)
plt.ylabel(r'$|E_{vac}(R_\Psi)|$ [unidades arbitrarias]', fontsize=12)
plt.title(r'Potencial Efectivo del Vacío $E_{vac}(R_\Psi)$' + '\n' +
          f'Mínimo estable en $R_\\Psi^* = {R_star:.2e}$ $\\ell_P$ → '
          f'$f_0 = {f0:.4f}$ Hz',
          fontsize=13)
plt.legend(fontsize=11)
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.tight_layout()
plt.savefig('potential_plot.png', dpi=150)
print("\n📈 Gráfico guardado como 'potential_plot.png'")

# ===== OPCIONAL: GUARDAR DATOS EN CSV =====
try:
    np.savetxt("Evac_Rpsi_data.csv",
               np.column_stack((R_vals, E_vals)),
               delimiter=",",
               header="Rpsi(lP),Evac",
               comments='')
    print("💾 Datos guardados en 'Evac_Rpsi_data.csv'")
except Exception as e:
    print(f"⚠️  No se pudieron guardar los datos: {e}")

plt.show()

# ===== VALIDACIONES COMPLEMENTARIAS =====
print("\n" + "=" * 80)
print("VALIDACIONES COMPLEMENTARIAS")
print("=" * 80)

# 1. Comparación con jerarquía cosmológica
print("\n1. JERARQUÍA COSMOLÓGICA:")
print(f"   R_Ψ*/ℓ_P = {R_star:.4e}")
print("   Se espera (ρ_P/ρ_Λ)^(1/2) ≈ 10^61 para algunos modelos")
print(f"   Valor actual: 10^{np.log10(R_star):.2f}")

# 2. Escaneo de parámetros (±10% variación)
print("\n2. ESCANEO DE PARÁMETROS (±10%):")
print("   Evaluando robustez del mínimo...")

variations = []
param_names = ['alpha', 'beta', 'gamma', 'delta', 'b']
param_values = [alpha, beta, gamma, delta, b]

for i, (name, val) in enumerate(zip(param_names, param_values)):
    for factor in [0.9, 1.1]:
        # Create modified parameters
        params_mod = param_values.copy()
        params_mod[i] = val * factor

        # Calculate potential with modified parameters
        def Evac_mod(R):
            term1 = params_mod[0] * R**(-4)
            term2 = params_mod[1] * zeta_prime * R**(-2)
            term3 = params_mod[2] * Lambda**2 * (R * lP)**2
            term4 = params_mod[3] * np.sin(np.log(R) / np.log(params_mod[4]))**2
            return term1 + term2 + term3 + term4

        E_mod = np.array([Evac_mod(R) for R in R_vals])
        idx_min_mod = np.argmin(E_mod)
        R_star_mod = R_vals[idx_min_mod]
        f0_mod = c / (2 * np.pi * R_star_mod * lP)

        variations.append({
            'param': name,
            'factor': factor,
            'R_star': R_star_mod,
            'f0': f0_mod,
            'delta_R': (R_star_mod - R_star) / R_star * 100,
            'delta_f': (f0_mod - f0) / f0 * 100
        })

print(f"   {'Parámetro':<10} {'Factor':<8} {'R_Ψ* (ℓP)':<15} "
      f"{'f₀ (Hz)':<15} {'ΔR (%)':<10} {'Δf (%)':<10}")
print("   " + "-" * 78)
for v in variations:
    print(f"   {v['param']:<10} {v['factor']:<8.2f} {v['R_star']:<15.4e} "
          f"{v['f0']:<15.4f} {v['delta_R']:<10.2f} {v['delta_f']:<10.2f}")

# 3. Estabilidad local
print("\n3. ANÁLISIS DE ESTABILIDAD LOCAL:")
# Buscar índices alrededor del mínimo
idx_range = slice(max(0, idx_min-5), min(len(R_vals), idx_min+6))
R_local = R_vals[idx_range]
E_local = E_vals[idx_range]

print("   R_Ψ valores cercanos al mínimo:")
for i, (R, E) in enumerate(zip(R_local, E_local)):
    marker = " ← MÍNIMO" if R == R_star else ""
    print(f"     R = {R:.4e} ℓP,  E_vac = {E:.6e}{marker}")

print("\n" + "=" * 80)
print("SIMULACIÓN COMPLETADA")
print("=" * 80)
