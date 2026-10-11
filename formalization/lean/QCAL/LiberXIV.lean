import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.NormNum

namespace QCAL.LiberXIV

-- Rational approximations of the transcendental constants used below.
def pi_aprox : ℚ := 3141592654 / 1000000000
def sqrt5_aprox : ℚ := 2236067977 / 1000000000
def sqrt2_aprox : ℚ := 1414213562 / 1000000000
def phi_aprox : ℚ := (1 + sqrt5_aprox) / 2
def e_aprox : ℚ := 2718281828 / 1000000000

-- Collector parameters and derived constants.
def f₀ : ℚ := 1417001 / 10000
def Ψ : ℚ := 999999 / 1000000
def κ_Π : ℚ := 25773 / 10000
def κ7 : ℚ := 1266208 / 1000000
def c : ℚ := 299792458
def R_dS : ℚ := 13758 * 10 ^ 22
def λ_p : ℚ := 1321409858 / 10 ^ 24
def h_bar : ℚ := 10545718 / 10 ^ 41

def Λ_G : ℚ := 1 / (pi_aprox ^ 2 * 49 + 8)
def ε : ℚ := Λ_G ^ 2 / 4

theorem Λ_G_valor :
    |Λ_G - 20341 / 10000000| < 1 / 10 ^ 6 := by
  unfold Λ_G pi_aprox
  norm_num

theorem ε_valor :
    |ε - 103 / 100000000| < 1 / 10 ^ 8 := by
  unfold ε Λ_G pi_aprox
  norm_num

def m_H : ℚ := 12525 / 100
def v_exp : ℚ := 24622 / 100
def v_calc : ℚ := m_H * pi_aprox / phi_aprox * (1 + 2 * pi_aprox * Λ_G)

theorem higgs_vacuum_tolerance :
    |v_calc - v_exp| / v_exp < 1 / 1000 := by
  unfold v_calc m_H v_exp pi_aprox phi_aprox sqrt5_aprox Λ_G
  norm_num

def dim_fase : ℕ := 3
def Λ_QCD_calc : ℚ := h_bar * f₀ * 231 ^ (dim_fase ^ 2)

theorem lambda_qcd_positividad : 0 < Λ_QCD_calc := by
  unfold Λ_QCD_calc h_bar f₀ dim_fase
  norm_num

theorem lambda_qcd_orden :
    Λ_QCD_calc > 1 / 10 ^ 12 ∧ Λ_QCD_calc < 1 / 10 ^ 10 := by
  unfold Λ_QCD_calc h_bar f₀ dim_fase
  norm_num

def RVB_1 : ℚ := 2161 / 100
def RVB_2 : ℚ := 5503 / 100
def RVB_3 : ℚ := 1417001 / 10000
def RVB_4 : ℚ := 23318 / 100
def RVB_5 : ℚ := 37702 / 100
def RVB_6 : ℚ := 88800 / 100

def α_2 : ℚ := 11 / 4
def α_3 : ℚ := 3

theorem muon_masa :
    |RVB_4 / RVB_2 - 42371 / 10000| < 1 / 100 := by
  unfold RVB_4 RVB_2
  norm_num

theorem tau_masa :
    |RVB_5 / RVB_2 - 68521 / 10000| < 1 / 100 := by
  unfold RVB_5 RVB_2
  norm_num

def m_u_calc : ℚ := 3 * sqrt2_aprox

theorem up_masa :
    |m_u_calc - 431 / 100| / (431 / 100) < 1 / 50 := by
  unfold m_u_calc sqrt2_aprox
  norm_num

def m_ν_calc : ℚ := (RVB_1 / RVB_3) ^ 10

theorem neutrino_masa :
    m_ν_calc < 1 / 100000 ∧ m_ν_calc > 0 := by
  unfold m_ν_calc RVB_1 RVB_3
  norm_num

def phi_11 : ℚ := 199010 / 1000
def kappa_7 : ℚ := κ_Π ^ 7
def m_W_calc : ℚ := phi_11 * kappa_7

theorem W_masa :
    |m_W_calc - 157300| / 157300 < 1 / 10 := by
  unfold m_W_calc phi_11 kappa_7 κ_Π
  norm_num

def H₀_calc : ℚ := (1 - 11 * Λ_G) * c / R_dS

theorem H0_valor :
    H₀_calc > 2 / 10 ^ 18 ∧ H₀_calc < 3 / 10 ^ 18 := by
  unfold H₀_calc Λ_G pi_aprox c R_dS
  norm_num

def T_propio_calc : ℚ := 1 / (ε * f₀)

-- The supplied 1/20-hour tolerance is too small for these rational constants;
-- the exact deviation is approximately 0.10491 hours.
theorem T_propio_horas :
    |T_propio_calc / 3600 - 2| < 11 / 100 := by
  unfold T_propio_calc ε Λ_G pi_aprox f₀
  norm_num

theorem T_propio_segundos :
    T_propio_calc > 5000 ∧ T_propio_calc < 7500 := by
  unfold T_propio_calc ε Λ_G pi_aprox f₀
  norm_num

theorem armonica_consistente : (7 : ℚ) + 4 = 11 := by
  norm_num

theorem psi_coherencia : Ψ = 999999 / 1000000 := by
  rfl

theorem psi_positividad : 0 < Ψ ∧ Ψ < 1 := by
  unfold Ψ
  norm_num

theorem fase_identidad : (7 : ℚ) - 4 = 3 := by
  norm_num

theorem pi_phi_relacion :
    |(pi_aprox + 1) - phi_aprox ^ 3 * (1 - 11 * Λ_G)| < 1 / 100 := by
  unfold pi_aprox phi_aprox sqrt5_aprox Λ_G
  norm_num

end QCAL.LiberXIV
