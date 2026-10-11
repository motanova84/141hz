import QCAL.LiberXIV

namespace QCAL.LiberXI

open QCAL.LiberXIV

-- The LIBER XIV constants are reused as exact rationals.
def R_as : ℚ := R_dS
def T_H_calc : ℚ := R_as / c
def H₀_calc : ℚ := (1 - 11 * Λ_G) * c / R_as
def T_mas_uno_calc : ℚ := (1 / H₀_calc) * (1 - 11 * Λ_G)
def segundos_por_año : ℚ := 31557600
def T_H_Gyr_calc : ℚ := T_H_calc / (segundos_por_año * 10 ^ 9)

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

-- LIBER XIV instead defines local time as 1/(ε f₀); with those values
-- it is about 6822 seconds, not the 7057 seconds stated in the LIBER XI text.
-- The separate expression 1/(E-f₀) cannot be evaluated until E is specified.
def I_propio_LiberXIV : ℚ := T_propio_calc

theorem I_propio_LiberXIV_rango :
    I_propio_LiberXIV > 6800 ∧ I_propio_LiberXIV < 6850 := by
  unfold I_propio_LiberXIV T_propio_calc ε Λ_G pi_aprox f₀
  norm_num

theorem I_propio_LiberXIV_no_es_7057 :
    I_propio_LiberXIV ≠ 7057 := by
  unfold I_propio_LiberXIV T_propio_calc ε Λ_G pi_aprox f₀
  norm_num

theorem tiempo_local_menor_que_hubble :
    I_propio_LiberXIV < T_H_calc := by
  unfold I_propio_LiberXIV T_propio_calc ε Λ_G pi_aprox f₀ T_H_calc R_as R_dS c
  norm_num

end QCAL.LiberXI
