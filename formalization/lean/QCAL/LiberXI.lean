import QCAL.LiberXIV

/-!
# LIBER XI: time-scale closure

The source values are transcribed from PI Coherencia del universo,
DOI 10.5281/zenodo.23288642, XI.1–XI.5.
-/
namespace QCAL.LiberXI

open QCAL.LiberXIV

-- The LIBER XIV constants are reused as exact rationals.
def R_as : ℚ := R_dS
def T_H_calc : ℚ := R_as / c
def H₀_calc : ℚ := (1 - 11 * Λ_G) * c / R_as
def H₀_inverse_calc : ℚ := 1 / H₀_calc
def T_mas_uno_calc : ℚ := (1 / H₀_calc) * (1 - 11 * Λ_G)
def segundos_por_año : ℚ := 31557600
def T_H_Gyr_calc : ℚ := T_H_calc / (segundos_por_año * 10 ^ 9)
def H₀_inverse_Gyr_calc : ℚ := H₀_inverse_calc / (segundos_por_año * 10 ^ 9)

theorem H0_rango :
    H₀_calc > 21 / 10 ^ 19 ∧ H₀_calc < 22 / 10 ^ 19 := by
  unfold H₀_calc R_as R_dS Λ_G pi_aprox c
  norm_num

theorem T_H_segundos :
    T_H_calc > 45 * 10 ^ 16 ∧ T_H_calc < 47 * 10 ^ 16 := by
  unfold T_H_calc R_as R_dS c
  norm_num

theorem T_H_edad_universo :
    T_H_Gyr_calc > 145 / 10 ∧ T_H_Gyr_calc < 146 / 10 := by
  unfold T_H_Gyr_calc T_H_calc R_as R_dS c segundos_por_año
  norm_num

theorem H₀_inverse_edad_universo :
    H₀_inverse_Gyr_calc > 148 / 10 ∧ H₀_inverse_Gyr_calc < 149 / 10 := by
  unfold H₀_inverse_Gyr_calc H₀_inverse_calc H₀_calc R_as R_dS
  unfold Λ_G pi_aprox c segundos_por_año
  norm_num

theorem H₀_inverse_vs_T_H :
    H₀_inverse_calc / T_H_calc > 102 / 100 ∧
      H₀_inverse_calc / T_H_calc < 103 / 100 := by
  unfold H₀_inverse_calc H₀_calc T_H_calc R_as R_dS Λ_G pi_aprox c
  norm_num

theorem factor_correccion_no_cero :
    1 - 11 * Λ_G ≠ 0 := by
  unfold Λ_G pi_aprox
  norm_num

theorem corrected_reciprocal_identity
    (δ speed radius : ℚ)
    (hδ : 1 - 11 * δ ≠ 0) (hspeed : speed ≠ 0) (hradius : radius ≠ 0) :
    (1 / ((1 - 11 * δ) * speed / radius)) * (1 - 11 * δ) =
      radius / speed := by
  field_simp [hδ, hspeed, hradius]
  ring

-- With the stated definition of T+1, the correction gives exact equality
-- with T_H; it does not yield a nonzero 0.007% residual.
theorem T_mas_uno_igual_T_H :
    T_mas_uno_calc = T_H_calc := by
  unfold T_mas_uno_calc H₀_calc T_H_calc R_as
  exact corrected_reciprocal_identity Λ_G c R_dS
    factor_correccion_no_cero (by norm_num [c]) (by norm_num [R_dS])

-- LIBER XI uses ε = 10⁻⁶; LIBER XIV separately gives the refined
-- ε = Λ_G²/4, so these are intentionally distinct local-time values.
def ε_LiberXI : ℚ := 1 / 10 ^ 6
def I_propio_LiberXI : ℚ := 1 / (ε_LiberXI * f₀)

theorem I_propio_LiberXI_rango :
    I_propio_LiberXI > 7057 ∧ I_propio_LiberXI < 7058 := by
  unfold I_propio_LiberXI ε_LiberXI f₀
  norm_num

def factor_conversion_LiberXI : ℚ := 6501 * 10 ^ 10

theorem factor_conversion_error :
    |T_H_calc / I_propio_LiberXI - factor_conversion_LiberXI| /
      factor_conversion_LiberXI < 1 / 1000 := by
  unfold T_H_calc R_as R_dS c I_propio_LiberXI ε_LiberXI f₀
  unfold factor_conversion_LiberXI
  norm_num

-- LIBER XIV's refined epsilon yields a distinct time of about 6822 seconds.
def I_propio_LiberXIV : ℚ := T_propio_calc

theorem I_propio_LiberXIV_rango :
    I_propio_LiberXIV > 6800 ∧ I_propio_LiberXIV < 6850 := by
  unfold I_propio_LiberXIV T_propio_calc ε Λ_G pi_aprox f₀
  norm_num

theorem I_propio_LiberXIV_no_es_7057 :
    I_propio_LiberXIV ≠ 7057 := by
  unfold I_propio_LiberXIV T_propio_calc ε Λ_G pi_aprox f₀
  norm_num

def pi_phi_error_relativo : ℚ :=
  |(pi_aprox + 1) - phi_aprox ^ 3 * (1 - 11 * Λ_G)| / (pi_aprox + 1)

-- The exact rational approximation is between 0.007% and 0.0075%;
-- the source's 0.007% is its rounded presentation.
theorem pi_phi_error_relativo_rango :
    7 / 100000 < pi_phi_error_relativo ∧
      pi_phi_error_relativo < 3 / 40000 := by
  unfold pi_phi_error_relativo pi_aprox phi_aprox sqrt5_aprox Λ_G
  norm_num

theorem tiempo_local_menor_que_hubble :
    I_propio_LiberXI < T_H_calc := by
  unfold I_propio_LiberXI ε_LiberXI f₀ T_H_calc R_as R_dS c
  norm_num

end QCAL.LiberXI
