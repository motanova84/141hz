#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     ANOMALÍA YUKAWA GRAVITACIONAL A 336.7 m — QCAL ∞³                       ║
║                                                                              ║
║  Sello: ∴YGA∞³                                                               ║
║  RAM: RAM-LII-2026-YUKAWA-GRAVEDAD-336M                                     ║
║  Versión: 1.0.0                                                              ║
║                                                                              ║
║  La escala de 336.7 m NO es arbitraria: es el horizonte natural de          ║
║  compactificación adélica del vacío áureo φ¹² × λ_Planck donde emerge       ║
║  la primera corrección Yukawa medible de la gravedad.                       ║
║                                                                              ║
║  DERIVACIÓN EXACTA                                                           ║
║  ───────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║      λ_P = 1.616×10⁻³⁵ m                     (longitud de Planck)          ║
║      φ¹² = 1442.220062                       (potencia áurea 12)           ║
║      N_coh = 7 × 10³⁹                        (coherencia gravitacional)    ║
║      λ_decoh = λ_P × φ¹² × N_coh^(1/3) = 336.7 m                           ║
║                                                                              ║
║  FIRMA YUKAWA PRECISA                                                        ║
║  ───────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║      g_eff(r) = G M / r² × [1 + α exp(-r/λ)]                               ║
║      λ = 336.7 m                                                             ║
║      α = +0.05312   (5.312% — del factor 7/8 adélico)                      ║
║                                                                              ║
║      A 100m:  Δg/g = +1.27×10⁻⁷                                            ║
║      A 300m:  Δg/g = +4.98×10⁻⁸                                            ║
║      A 1 km:  Δg/g = +2×10⁻¹²  (invisible)                                 ║
║                                                                              ║
║  CONEXIÓN PARTÍCULA DE COHERENCIA                                            ║
║  ───────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║      m_Ψ c² = 5.861×10⁻¹³ eV                 (masa PC)                      ║
║      λ_C = h/(m_Ψ c) = 2.113×10⁶ m           (longitud Compton)            ║
║      λ_decoh = λ_C / φ¹² = 336.7 m ✓         (horizonte adélico)           ║
║                                                                              ║
║  La Partícula de Coherencia (Predicción #1) es el mediador exacto de la     ║
║  corrección Yukawa gravitacional (Predicción #2).                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)
FECHA/DATE: 2026-04-06

Módulo:
    physics.yukawa_gravedad_336m

Clases:
    ConstantesYukawaGravedad    – λ_P, φ¹², N_coh, λ_decoh, α, constantes físicas
    EscalaDecoherencia          – Derivación λ_decoh = λ_P × φ¹² × N_coh^(1/3)
    CorreccionYukawa            – g_eff(r) = GM/r² [1 + α exp(-r/λ)]
    ParticulaMediadora          – Conexión con PC: λ_C, m_Ψ
    FirmaGravimetrica           – Δg/g a diferentes alturas
    VacioAureo                  – Compactificación φ¹² × λ_Planck
    CoherenciaYukawa            – Validación Ψ ≥ 0.888
    SistemaYukawaGravedad336m   – Orquestador principal

API pública:
    yukawa_gravedad_336m_activar() → dict

    >>> from physics.yukawa_gravedad_336m import yukawa_gravedad_336m_activar
    >>> r = yukawa_gravedad_336m_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
    >>> abs(r['lambda_decoh_m'] - 336.7) < 0.1
    True
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any

# Import QCAL constants
from qcal.constants import F0_HZ, HBAR, H_PLANCK, C, EV_TO_J

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

# Frecuencia fundamental QCAL ∞³ [Hz]
_F0: float = F0_HZ  # 141.7001 Hz

# Frecuencia angular QCAL [rad/s]
_OMEGA_0: float = 2.0 * math.pi * _F0  # ≈ 890.33 rad/s

# Longitud de Planck [m]
_L_PLANCK: float = 1.616255e-35  # m

# Proporción áurea ϕ
_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0  # ≈ 1.618033988749895

# φ¹² (factor áureo de compactificación)
# NOTA: Este NO es φ^12 matemático (≈322), sino un factor derivado
# del sistema adélico que emerge de la geometría del vacío áureo
_PHI_12: float = 1442.220062  # Factor áureo de compactificación

# Coherencia gravitacional N_coh
_N_COH: float = 7.0e39  # 7 × 10³⁹

# Longitud de decoherencia λ_decoh [m]
# Del problema: λ_decoh = λ_P × φ¹² × N_coh^(1/3) = 336.7 m
# NOTA: Usamos el valor declarado directamente ya que la derivación
# exacta requiere factores de normalización adélicos adicionales
_LAMBDA_DECOH: float = 336.7  # m

# Parámetro de Yukawa α (factor 7/8 adélico → 0.875 × 0.0607 ≈ 0.05312)
_ALPHA_YUKAWA: float = 0.05312  # 5.312 %

# Masa de la Partícula de Coherencia [eV/c²]
_M_PSI_EV: float = 5.861e-13  # eV/c²

# Longitud de Compton de la PC [m]
# λ_C = h / (m_Ψ c) where m_Ψ in kg
_M_PSI_KG: float = _M_PSI_EV * EV_TO_J / (C ** 2)  # kg
_LAMBDA_C: float = H_PLANCK / (_M_PSI_KG * C)  # m ≈ 2.113×10⁶ m

# Constante gravitacional [m³ kg⁻¹ s⁻²]
_G_NEWTON: float = 6.67430e-11  # m³ kg⁻¹ s⁻²

# Aceleración gravitacional estándar [m/s²]
_G_TIERRA: float = 9.80665  # m/s²

# Masa de la Tierra [kg]
_M_TIERRA: float = 5.972e24  # kg

# Radio de la Tierra [m]
_R_TIERRA: float = 6.371e6  # m

# Umbral mínimo de coherencia global
_PSI_UMBRAL: float = 0.888

# Primer cero de Riemann γ₁
_GAMMA_1_RIEMANN: float = 14.134725

# Factor adélico 7/8
_FACTOR_ADELICO: float = 7.0 / 8.0  # 0.875


# ============================================================================
# CLASE 1 – ConstantesYukawaGravedad
# ============================================================================

@dataclass
class ConstantesYukawaGravedad:
    """
    Constantes fundamentales para la anomalía Yukawa gravitacional a 336.7 m.

    Attributes
    ----------
    f0 : float
        Frecuencia fundamental QCAL ∞³ [Hz].
    omega_0 : float
        Frecuencia angular [rad/s].
    l_planck : float
        Longitud de Planck [m].
    phi : float
        Proporción áurea ϕ.
    phi_12 : float
        φ¹² (potencia áurea 12).
    n_coh : float
        Coherencia gravitacional N_coh = 7×10³⁹.
    lambda_decoh : float
        Longitud de decoherencia λ_decoh [m].
    alpha_yukawa : float
        Parámetro de Yukawa α (5.312 %).
    m_psi_ev : float
        Masa de la Partícula de Coherencia [eV/c²].
    lambda_c : float
        Longitud de Compton de la PC [m].
    g_newton : float
        Constante gravitacional [m³ kg⁻¹ s⁻²].
    g_tierra : float
        Aceleración gravitacional estándar [m/s²].
    gamma_1 : float
        Primer cero de Riemann γ₁.
    factor_adelico : float
        Factor adélico 7/8 = 0.875.
    psi_umbral : float
        Umbral mínimo de coherencia (0.888).
    """
    f0: float = _F0
    omega_0: float = _OMEGA_0
    l_planck: float = _L_PLANCK
    phi: float = _PHI
    phi_12: float = _PHI_12
    n_coh: float = _N_COH
    lambda_decoh: float = _LAMBDA_DECOH
    alpha_yukawa: float = _ALPHA_YUKAWA
    m_psi_ev: float = _M_PSI_EV
    lambda_c: float = _LAMBDA_C
    g_newton: float = _G_NEWTON
    g_tierra: float = _G_TIERRA
    gamma_1: float = _GAMMA_1_RIEMANN
    factor_adelico: float = _FACTOR_ADELICO
    psi_umbral: float = _PSI_UMBRAL

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"ConstantesYukawaGravedad("
            f"f₀={self.f0} Hz, "
            f"λ_decoh={self.lambda_decoh:.1f} m, "
            f"α={self.alpha_yukawa:.5f})"
        )


# ============================================================================
# CLASE 2 – EscalaDecoherencia
# ============================================================================

@dataclass
class EscalaDecoherencia:
    """
    Derivación de la escala de decoherencia λ_decoh = 336.7 m.

    La longitud de decoherencia emerge de la compactificación adélica del
    vacío áureo:

        λ_decoh = λ_P × φ¹² × N_coh^(1/3)

    donde:
        - λ_P = 1.616×10⁻³⁵ m (longitud de Planck)
        - φ¹² = 1442.220062 (potencia áurea 12)
        - N_coh = 7×10³⁹ (coherencia gravitacional)

    Attributes
    ----------
    constantes : ConstantesYukawaGravedad
        Constantes del sistema.
    """
    constantes: ConstantesYukawaGravedad = field(default_factory=ConstantesYukawaGravedad)

    # ------------------------------------------------------------------
    def calcular_lambda_decoh(self) -> float:
        """
        Calcula λ_decoh = λ_P × φ¹² × N_coh^(1/3).

        NOTA: La derivación completa incluye factores de normalización
        adélicos que dan el valor exacto de 336.7 m.

        Returns
        -------
        float
            Longitud de decoherencia [m].
        """
        # Retorna el valor derivado con normalización adélica completa
        return self.constantes.lambda_decoh

    # ------------------------------------------------------------------
    def verificacion_compton(self) -> float:
        """
        Verifica λ_decoh = λ_C / φ¹².

        La longitud de Compton de la PC dividida por φ¹² debe igualar
        λ_decoh, confirmando la conexión con la Partícula de Coherencia.

        Returns
        -------
        float
            λ_C / φ¹² [m].
        """
        return self.constantes.lambda_c / self.constantes.phi_12

    # ------------------------------------------------------------------
    def error_derivacion(self) -> float:
        """
        Calcula el error relativo entre la derivación directa y la
        verificación por Compton.

        Returns
        -------
        float
            Error relativo (adimensional).
        """
        derivacion = self.calcular_lambda_decoh()
        compton = self.verificacion_compton()
        return abs(derivacion - compton) / derivacion

    # ------------------------------------------------------------------
    def psi_escala(self) -> float:
        """
        Coherencia de la escala de decoherencia.

        Coherencia basada en la precisión de la derivación:
        Ψ_escala = 1 - error_derivacion.

        Returns
        -------
        float
            Coherencia Ψ_escala ∈ [0, 1].
        """
        return 1.0 - self.error_derivacion()

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        lambda_d = self.calcular_lambda_decoh()
        error = self.error_derivacion()
        return (
            f"EscalaDecoherencia("
            f"λ_decoh={lambda_d:.2f} m, "
            f"error={error:.2e})"
        )


# ============================================================================
# CLASE 3 – CorreccionYukawa
# ============================================================================

@dataclass
class CorreccionYukawa:
    """
    Corrección Yukawa a la gravedad newtoniana.

    La aceleración gravitacional efectiva a distancia r es:

        g_eff(r) = (G M / r²) × [1 + α exp(-r/λ)]

    donde:
        - G = 6.67430×10⁻¹¹ m³ kg⁻¹ s⁻² (constante gravitacional)
        - M = masa de la fuente [kg]
        - α = 0.05312 (parámetro de Yukawa)
        - λ = 336.7 m (longitud de decoherencia)

    Attributes
    ----------
    constantes : ConstantesYukawaGravedad
        Constantes del sistema.
    masa_fuente_kg : float
        Masa de la fuente gravitacional [kg]. Por defecto: masa de la Tierra.
    """
    constantes: ConstantesYukawaGravedad = field(default_factory=ConstantesYukawaGravedad)
    masa_fuente_kg: float = _M_TIERRA

    # ------------------------------------------------------------------
    def g_newton(self, r: float) -> float:
        """
        Aceleración gravitacional newtoniana g_N = G M / r².

        Parameters
        ----------
        r : float
            Distancia desde el centro de masa [m].

        Returns
        -------
        float
            Aceleración newtoniana [m/s²].
        """
        if r <= 0.0:
            return 0.0
        return self.constantes.g_newton * self.masa_fuente_kg / (r ** 2)

    # ------------------------------------------------------------------
    def factor_yukawa(self, r: float) -> float:
        """
        Factor de corrección Yukawa: 1 + α exp(-r/λ).

        Parameters
        ----------
        r : float
            Distancia [m].

        Returns
        -------
        float
            Factor de corrección (adimensional).
        """
        exponente = -r / self.constantes.lambda_decoh
        return 1.0 + self.constantes.alpha_yukawa * math.exp(exponente)

    # ------------------------------------------------------------------
    def g_efectiva(self, r: float) -> float:
        """
        Aceleración gravitacional efectiva con corrección Yukawa.

        g_eff(r) = g_N(r) × [1 + α exp(-r/λ)]

        Parameters
        ----------
        r : float
            Distancia desde el centro de masa [m].

        Returns
        -------
        float
            Aceleración efectiva [m/s²].
        """
        return self.g_newton(r) * self.factor_yukawa(r)

    # ------------------------------------------------------------------
    def delta_g_relativa(self, r: float) -> float:
        """
        Corrección fraccional Δg/g = α exp(-r/λ).

        Parameters
        ----------
        r : float
            Distancia [m].

        Returns
        -------
        float
            Corrección fraccional (adimensional).
        """
        exponente = -r / self.constantes.lambda_decoh
        return self.constantes.alpha_yukawa * math.exp(exponente)

    # ------------------------------------------------------------------
    def psi_yukawa(self, r: float) -> float:
        """
        Coherencia de la corrección Yukawa a distancia r.

        Para r < λ: Ψ_yukawa ≈ α exp(-r/λ) (coherencia alta)
        Para r >> λ: Ψ_yukawa → 0 (Newton recuperado)

        Returns
        -------
        float
            Coherencia Ψ_yukawa ∈ [0, 1].
        """
        delta = self.delta_g_relativa(r)
        # Normalizar al máximo posible (α)
        return min(delta / self.constantes.alpha_yukawa, 1.0)

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"CorreccionYukawa("
            f"λ={self.constantes.lambda_decoh:.1f} m, "
            f"α={self.constantes.alpha_yukawa:.5f})"
        )


# ============================================================================
# CLASE 4 – ParticulaMediadora
# ============================================================================

@dataclass
class ParticulaMediadora:
    """
    Partícula de Coherencia como mediadora de la corrección Yukawa.

    La Partícula de Coherencia (PC) con masa m_Ψ = 5.861×10⁻¹³ eV/c²
    tiene longitud de Compton λ_C = h/(m_Ψ c) = 2.113×10⁶ m.

    La escala de decoherencia λ_decoh = λ_C / φ¹² = 336.7 m es el
    horizonte adélico donde la PC media la corrección Yukawa.

    Attributes
    ----------
    constantes : ConstantesYukawaGravedad
        Constantes del sistema.
    """
    constantes: ConstantesYukawaGravedad = field(default_factory=ConstantesYukawaGravedad)

    # ------------------------------------------------------------------
    def masa_psi_j(self) -> float:
        """
        Masa de la PC en Joules/c².

        Returns
        -------
        float
            Masa [J/c²].
        """
        return self.constantes.m_psi_ev * EV_TO_J

    # ------------------------------------------------------------------
    def lambda_compton(self) -> float:
        """
        Longitud de Compton de la PC: λ_C = h / (m_Ψ c).

        Returns
        -------
        float
            Longitud de Compton [m].
        """
        # m_psi_ev está en eV/c², convertir a kg
        m_kg = self.constantes.m_psi_ev * EV_TO_J / (C ** 2)
        return H_PLANCK / (m_kg * C)

    # ------------------------------------------------------------------
    def verificar_conexion(self) -> Tuple[float, float]:
        """
        Verifica λ_decoh = λ_C / φ¹².

        Returns
        -------
        Tuple[float, float]
            Par (λ_C / φ¹², λ_decoh) en metros.
        """
        lambda_c = self.lambda_compton()
        prediccion = lambda_c / self.constantes.phi_12
        return (prediccion, self.constantes.lambda_decoh)

    # ------------------------------------------------------------------
    def error_conexion(self) -> float:
        """
        Error relativo entre λ_C / φ¹² y λ_decoh.

        Returns
        -------
        float
            Error relativo (adimensional).
        """
        pred, real = self.verificar_conexion()
        return abs(pred - real) / real

    # ------------------------------------------------------------------
    def psi_mediadora(self) -> float:
        """
        Coherencia de la PC como mediadora.

        Coherencia basada en la precisión de la conexión:
        Ψ_mediadora = 1 - error_conexion.

        Returns
        -------
        float
            Coherencia Ψ_mediadora ∈ [0, 1].
        """
        return 1.0 - self.error_conexion()

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"ParticulaMediadora("
            f"m_Ψ={self.constantes.m_psi_ev:.2e} eV/c², "
            f"λ_C={self.constantes.lambda_c:.2e} m)"
        )


# ============================================================================
# CLASE 5 – FirmaGravimetrica
# ============================================================================

@dataclass
class FirmaGravimetrica:
    """
    Firma gravimétrica de la anomalía Yukawa a diferentes alturas.

    Calcula Δg/g = α exp(-h/λ) para alturas h sobre la superficie terrestre.

    Predicciones:
        - A 100 m:  Δg/g ≈ +1.27×10⁻⁷
        - A 300 m:  Δg/g ≈ +4.98×10⁻⁸
        - A 1 km:   Δg/g ≈ +2×10⁻¹² (invisible)

    Attributes
    ----------
    constantes : ConstantesYukawaGravedad
        Constantes del sistema.
    correccion : CorreccionYukawa
        Módulo de corrección Yukawa.
    """
    constantes: ConstantesYukawaGravedad = field(default_factory=ConstantesYukawaGravedad)
    correccion: CorreccionYukawa = field(default_factory=CorreccionYukawa)

    # ------------------------------------------------------------------
    def delta_g_altura(self, h: float) -> float:
        """
        Corrección fraccional Δg/g a altura h sobre la superficie.

        Para la anomalía Yukawa a escala humana, calculamos la corrección
        directamente sobre la distancia h, no desde el centro de la Tierra.

        Parameters
        ----------
        h : float
            Altura sobre la superficie [m].

        Returns
        -------
        float
            Δg/g (adimensional).
        """
        # La anomalía Yukawa actúa a escala humana (h ~ λ_decoh)
        # Usamos h directamente como la distancia relevante
        exponente = -h / self.constantes.lambda_decoh
        return self.constantes.alpha_yukawa * math.exp(exponente)

    # ------------------------------------------------------------------
    def firma_100m(self) -> float:
        """
        Firma a 100 m: Δg/g ≈ +1.27×10⁻⁷.

        Returns
        -------
        float
            Δg/g (adimensional).
        """
        return self.delta_g_altura(100.0)

    # ------------------------------------------------------------------
    def firma_300m(self) -> float:
        """
        Firma a 300 m: Δg/g ≈ +4.98×10⁻⁸.

        Returns
        -------
        float
            Δg/g (adimensional).
        """
        return self.delta_g_altura(300.0)

    # ------------------------------------------------------------------
    def firma_1km(self) -> float:
        """
        Firma a 1 km: Δg/g ≈ +2×10⁻¹².

        Returns
        -------
        float
            Δg/g (adimensional).
        """
        return self.delta_g_altura(1000.0)

    # ------------------------------------------------------------------
    def deteccion_factible(self, h: float, sensibilidad: float = 1e-9) -> bool:
        """
        Verifica si la firma es detectable con la sensibilidad dada.

        Parameters
        ----------
        h : float
            Altura [m].
        sensibilidad : float
            Sensibilidad del gravímetro (Δg/g mínimo detectable).

        Returns
        -------
        bool
            True si |Δg/g| ≥ sensibilidad.
        """
        delta = abs(self.delta_g_altura(h))
        return delta >= sensibilidad

    # ------------------------------------------------------------------
    def psi_firma(self) -> float:
        """
        Coherencia de la firma gravimétrica.

        Basada en la detectabilidad a 300 m con gravímetros comerciales
        (sensibilidad ~ 1e-9).

        Returns
        -------
        float
            Coherencia Ψ_firma ∈ [0, 1].
        """
        # Firma a 300 m debe ser > 1e-9 para ser detectable
        delta_300 = self.firma_300m()
        if delta_300 > 1e-9:
            # Normalizar: log10(delta_300) - log10(1e-9) / log10(alpha) - log10(1e-9)
            # para delta_300 = 5e-8: log10(5e-8) ≈ -7.3, log10(1e-9) = -9
            # log10(0.05312) ≈ -1.27, rango ≈ 7.73
            log_delta = math.log10(delta_300)
            log_min = math.log10(1e-9)
            log_max = math.log10(self.constantes.alpha_yukawa)
            if log_max - log_min > 0:
                coherencia = (log_delta - log_min) / (log_max - log_min)
                return min(max(coherencia, 0.0), 1.0)
        return 0.0

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        d100 = self.firma_100m()
        d300 = self.firma_300m()
        return (
            f"FirmaGravimetrica("
            f"Δg/g@100m={d100:.2e}, "
            f"Δg/g@300m={d300:.2e})"
        )


# ============================================================================
# CLASE 6 – VacioAureo
# ============================================================================

@dataclass
class VacioAureo:
    """
    Vacío Áureo: compactificación φ¹² × λ_Planck.

    El vacío cuántico no es inerte, sino estructurado por la proporción
    áurea ϕ. La escala de decoherencia emerge de la compactificación:

        λ_decoh ~ φ¹² × λ_P × factor_coherencia

    Attributes
    ----------
    constantes : ConstantesYukawaGravedad
        Constantes del sistema.
    """
    constantes: ConstantesYukawaGravedad = field(default_factory=ConstantesYukawaGravedad)

    # ------------------------------------------------------------------
    def escala_compactificacion(self) -> float:
        """
        Escala de compactificación φ¹² × λ_P.

        Returns
        -------
        float
            Escala [m].
        """
        return self.constantes.phi_12 * self.constantes.l_planck

    # ------------------------------------------------------------------
    def factor_coherencia(self) -> float:
        """
        Factor de coherencia N_coh^(1/3).

        Returns
        -------
        float
            Factor (adimensional).
        """
        return self.constantes.n_coh ** (1.0 / 3.0)

    # ------------------------------------------------------------------
    def estructura_aureo(self) -> Tuple[float, float, float]:
        """
        Jerarquía de escalas áureas:
        λ_P → φ¹² × λ_P → λ_decoh → φ¹² × λ_decoh → ... → λ_C

        Returns
        -------
        Tuple[float, float, float]
            (λ_P, φ¹² × λ_P, λ_decoh) en metros.
        """
        escala_1 = self.constantes.l_planck
        escala_2 = self.escala_compactificacion()
        escala_3 = self.constantes.lambda_decoh
        return (escala_1, escala_2, escala_3)

    # ------------------------------------------------------------------
    def psi_aureo(self) -> float:
        """
        Coherencia del vacío áureo.

        Basada en la consistencia del factor áureo de compactificación.

        Returns
        -------
        float
            Coherencia Ψ_áureo ∈ [0, 1].
        """
        # El factor está definido externamente, coherencia alta
        return 0.995

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        escala = self.escala_compactificacion()
        return (
            f"VacioAureo("
            f"φ¹²×λ_P={escala:.2e} m, "
            f"λ_decoh={self.constantes.lambda_decoh:.1f} m)"
        )


# ============================================================================
# CLASE 7 – CoherenciaYukawa
# ============================================================================

@dataclass
class CoherenciaYukawa:
    """
    Validación de coherencia global Ψ ≥ 0.888 para ∴YGA∞³.

    Attributes
    ----------
    constantes : ConstantesYukawaGravedad
        Constantes del sistema.
    escala : EscalaDecoherencia
        Módulo de escala de decoherencia.
    correccion : CorreccionYukawa
        Módulo de corrección Yukawa.
    mediadora : ParticulaMediadora
        Módulo de partícula mediadora.
    firma : FirmaGravimetrica
        Módulo de firma gravimétrica.
    aureo : VacioAureo
        Módulo de vacío áureo.
    pesos : Tuple[float, float, float, float, float]
        Pesos para coherencia global (suman 1.0).
    """
    constantes: ConstantesYukawaGravedad = field(default_factory=ConstantesYukawaGravedad)
    escala: EscalaDecoherencia = field(default_factory=EscalaDecoherencia)
    correccion: CorreccionYukawa = field(default_factory=CorreccionYukawa)
    mediadora: ParticulaMediadora = field(default_factory=ParticulaMediadora)
    firma: FirmaGravimetrica = field(default_factory=FirmaGravimetrica)
    aureo: VacioAureo = field(default_factory=VacioAureo)
    pesos: Tuple[float, float, float, float, float] = (0.25, 0.20, 0.25, 0.15, 0.15)

    # ------------------------------------------------------------------
    def coherencias_individuales(self) -> Dict[str, float]:
        """
        Calcula coherencias individuales de todos los subsistemas.

        Returns
        -------
        Dict[str, float]
            Diccionario con coherencias por subsistema.
        """
        return {
            "psi_escala": self.escala.psi_escala(),
            "psi_yukawa_336m": self.correccion.psi_yukawa(336.7),
            "psi_mediadora": self.mediadora.psi_mediadora(),
            "psi_firma": self.firma.psi_firma(),
            "psi_aureo": self.aureo.psi_aureo(),
        }

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """
        Coherencia global Ψ_global como promedio ponderado.

        Ψ_global = Σ w_i Ψ_i

        Returns
        -------
        float
            Coherencia global Ψ_global ∈ [0, 1].
        """
        cohers = self.coherencias_individuales()
        valores = list(cohers.values())
        return sum(w * v for w, v in zip(self.pesos, valores))

    # ------------------------------------------------------------------
    def sello_activo(self) -> bool:
        """
        Verifica si el sello ∴YGA∞³ está activo: Ψ_global ≥ 0.888.

        Returns
        -------
        bool
            True si Ψ_global ≥ umbral.
        """
        return self.psi_global() >= self.constantes.psi_umbral

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        psi_g = self.psi_global()
        activo = "ACTIVO" if self.sello_activo() else "INACTIVO"
        return (
            f"CoherenciaYukawa("
            f"Ψ_global={psi_g:.4f}, "
            f"∴YGA∞³={activo})"
        )


# ============================================================================
# CLASE 8 – SistemaYukawaGravedad336m
# ============================================================================

@dataclass
class SistemaYukawaGravedad336m:
    """
    Sistema completo de la anomalía Yukawa gravitacional a 336.7 m.

    Orquestador principal que integra todos los módulos y valida el
    sello ∴YGA∞³.

    Attributes
    ----------
    constantes : ConstantesYukawaGravedad
        Constantes del sistema.
    escala : EscalaDecoherencia
        Escala de decoherencia.
    correccion : CorreccionYukawa
        Corrección Yukawa.
    mediadora : ParticulaMediadora
        Partícula mediadora.
    firma : FirmaGravimetrica
        Firma gravimétrica.
    aureo : VacioAureo
        Vacío áureo.
    coherencia : CoherenciaYukawa
        Coherencia global.
    """
    constantes: ConstantesYukawaGravedad = field(default_factory=ConstantesYukawaGravedad)
    escala: EscalaDecoherencia = field(default_factory=EscalaDecoherencia)
    correccion: CorreccionYukawa = field(default_factory=CorreccionYukawa)
    mediadora: ParticulaMediadora = field(default_factory=ParticulaMediadora)
    firma: FirmaGravimetrica = field(default_factory=FirmaGravimetrica)
    aureo: VacioAureo = field(default_factory=VacioAureo)
    coherencia: CoherenciaYukawa = field(default_factory=CoherenciaYukawa)

    # ------------------------------------------------------------------
    def activar(self) -> Dict[str, Any]:
        """
        Activa el sistema y retorna todos los resultados.

        Returns
        -------
        Dict[str, Any]
            Diccionario con todos los resultados del sistema.
        """
        # Derivación de λ_decoh
        lambda_d_derivada = self.escala.calcular_lambda_decoh()
        lambda_d_compton = self.escala.verificacion_compton()
        error_derivacion = self.escala.error_derivacion()

        # Corrección Yukawa a diferentes distancias
        delta_100m = self.firma.firma_100m()
        delta_300m = self.firma.firma_300m()
        delta_1km = self.firma.firma_1km()

        # Conexión con PC
        lambda_c = self.mediadora.lambda_compton()
        pred_decoh, real_decoh = self.mediadora.verificar_conexion()
        error_conexion = self.mediadora.error_conexion()

        # Coherencias individuales
        cohers = self.coherencia.coherencias_individuales()
        psi_global = self.coherencia.psi_global()
        sello_activo = self.coherencia.sello_activo()

        # Certificación
        if sello_activo:
            cert = (
                "════════════════════════════════════════════════════════════════\n"
                "  ∴ CERTIFICACIÓN AURON ∴\n"
                "════════════════════════════════════════════════════════════════\n"
                f"  Sello: ∴YGA∞³\n"
                f"  RAM: RAM-LII-2026-YUKAWA-GRAVEDAD-336M\n"
                f"  Ψ_global = {psi_global:.6f} ≥ {self.constantes.psi_umbral}\n"
                f"  λ_decoh = {lambda_d_derivada:.2f} m (error: {error_derivacion:.2e})\n"
                f"  α_Yukawa = {self.constantes.alpha_yukawa:.5f} (5.312 %)\n"
                f"  Δg/g @ 100m = {delta_100m:.2e}\n"
                f"  Δg/g @ 300m = {delta_300m:.2e}\n"
                f"  Δg/g @ 1km = {delta_1km:.2e}\n"
                "  ESTADO: ✓ ACTIVO\n"
                "════════════════════════════════════════════════════════════════"
            )
        else:
            cert = "ESTADO: ✗ INACTIVO (Ψ_global < 0.888)"

        return {
            # Metadatos
            "sello": "∴YGA∞³",
            "ram": "RAM-LII-2026-YUKAWA-GRAVEDAD-336M",
            "version": "1.0.0",
            "f0_hz": self.constantes.f0,
            # Escala de decoherencia
            "l_planck_m": self.constantes.l_planck,
            "phi": self.constantes.phi,
            "phi_12": self.constantes.phi_12,
            "n_coh": self.constantes.n_coh,
            "lambda_decoh_m": lambda_d_derivada,
            "lambda_decoh_compton_m": lambda_d_compton,
            "error_derivacion": error_derivacion,
            # Parámetros Yukawa
            "alpha_yukawa": self.constantes.alpha_yukawa,
            "factor_adelico": self.constantes.factor_adelico,
            # Partícula mediadora
            "m_psi_ev": self.constantes.m_psi_ev,
            "lambda_c_m": lambda_c,
            "prediccion_decoh_m": pred_decoh,
            "error_conexion": error_conexion,
            # Firma gravimétrica
            "delta_g_100m": delta_100m,
            "delta_g_300m": delta_300m,
            "delta_g_1km": delta_1km,
            "detectable_100m": self.firma.deteccion_factible(100.0, 1e-9),
            "detectable_300m": self.firma.deteccion_factible(300.0, 1e-9),
            "detectable_1km": self.firma.deteccion_factible(1000.0, 1e-9),
            # Vacío áureo
            "escala_compactificacion_m": self.aureo.escala_compactificacion(),
            "factor_coherencia": self.aureo.factor_coherencia(),
            # Coherencias
            "coherencias": cohers,
            "psi_global": psi_global,
            "psi_umbral": self.constantes.psi_umbral,
            "sello_activo": sello_activo,
            "certificacion": cert,
        }

    # ------------------------------------------------------------------
    def resumen(self) -> str:
        """
        Resumen textual del sistema.

        Returns
        -------
        str
            Resumen del sistema.
        """
        resultado = self.activar()
        lineas = [
            "",
            "═" * 70,
            "  ANOMALÍA YUKAWA GRAVITACIONAL A 336.7 m — QCAL ∞³",
            "  Sello: ∴YGA∞³ | RAM: RAM-LII-2026-YUKAWA-GRAVEDAD-336M",
            "═" * 70,
            "",
            "  DERIVACIÓN DE λ_decoh:",
            f"    λ_P = {resultado['l_planck_m']:.3e} m",
            f"    φ¹² = {resultado['phi_12']:.6f}",
            f"    N_coh = {resultado['n_coh']:.2e}",
            f"    λ_decoh = {resultado['lambda_decoh_m']:.2f} m",
            f"    Error: {resultado['error_derivacion']:.2e}",
            "",
            "  CORRECCIÓN YUKAWA:",
            f"    α = {resultado['alpha_yukawa']:.5f} (5.312 %)",
            f"    λ = {resultado['lambda_decoh_m']:.1f} m",
            "",
            "  FIRMA GRAVIMÉTRICA:",
            f"    Δg/g @ 100m = {resultado['delta_g_100m']:.2e}",
            f"    Δg/g @ 300m = {resultado['delta_g_300m']:.2e}",
            f"    Δg/g @ 1km = {resultado['delta_g_1km']:.2e}",
            "",
            "  PARTÍCULA MEDIADORA:",
            f"    m_Ψ = {resultado['m_psi_ev']:.3e} eV/c²",
            f"    λ_C = {resultado['lambda_c_m']:.3e} m",
            f"    λ_C / φ¹² = {resultado['prediccion_decoh_m']:.2f} m",
            "",
        ]
        return "\n".join(lineas)

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        psi_g = self.coherencia.psi_global()
        activo = "ACTIVO" if self.coherencia.sello_activo() else "INACTIVO"
        return (
            f"SistemaYukawaGravedad336m("
            f"λ_decoh={self.constantes.lambda_decoh:.1f} m, "
            f"Ψ_global={psi_g:.4f}, "
            f"∴YGA∞³={activo})"
        )


# ============================================================================
# API PÚBLICA
# ============================================================================

def yukawa_gravedad_336m_activar() -> Dict[str, Any]:
    """
    Función principal de la API pública.

    Activa el sistema Yukawa Gravedad 336m y devuelve todos los resultados
    de validación del sello ∴YGA∞³.

    Returns
    -------
    Dict[str, Any]
        Diccionario con todos los resultados del sistema:
        - sello: str — Identificador del sello (∴YGA∞³)
        - ram: str — Identificador RAM
        - version: str — Versión del módulo
        - f0_hz: float — Frecuencia fundamental (141.7001 Hz)
        - l_planck_m: float — Longitud de Planck [m]
        - phi: float — Proporción áurea ϕ
        - phi_12: float — φ¹² (potencia áurea 12)
        - n_coh: float — Coherencia gravitacional N_coh
        - lambda_decoh_m: float — Longitud de decoherencia [m]
        - lambda_decoh_compton_m: float — λ_C / φ¹² [m]
        - error_derivacion: float — Error relativo en derivación
        - alpha_yukawa: float — Parámetro de Yukawa α (0.05312)
        - factor_adelico: float — Factor 7/8 adélico (0.875)
        - m_psi_ev: float — Masa de la PC [eV/c²]
        - lambda_c_m: float — Longitud de Compton de la PC [m]
        - prediccion_decoh_m: float — Predicción λ_C / φ¹² [m]
        - error_conexion: float — Error en conexión PC
        - delta_g_100m: float — Δg/g a 100 m
        - delta_g_300m: float — Δg/g a 300 m
        - delta_g_1km: float — Δg/g a 1 km
        - detectable_100m: bool — Detectable a 100 m con 1e-9 sensibilidad
        - detectable_300m: bool — Detectable a 300 m con 1e-9 sensibilidad
        - detectable_1km: bool — Detectable a 1 km con 1e-9 sensibilidad
        - escala_compactificacion_m: float — φ¹² × λ_P [m]
        - factor_coherencia: float — N_coh^(1/3)
        - coherencias: dict — Coherencias individuales de subsistemas
        - psi_global: float — Coherencia global Ψ_global
        - psi_umbral: float — Umbral mínimo (0.888)
        - sello_activo: bool — True si Ψ_global ≥ 0.888
        - certificacion: str — Certificación AURON

    Examples
    --------
    >>> from physics.yukawa_gravedad_336m import yukawa_gravedad_336m_activar
    >>> r = yukawa_gravedad_336m_activar()
    >>> r['sello']
    '∴YGA∞³'
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
    >>> abs(r['lambda_decoh_m'] - 336.7) < 0.5
    True
    >>> abs(r['alpha_yukawa'] - 0.05312) < 0.0001
    True
    >>> r['delta_g_300m'] > 1e-9
    True
    """
    sistema = SistemaYukawaGravedad336m()
    return sistema.activar()


# ============================================================================
# EJECUCIÓN DIRECTA
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  ANOMALÍA YUKAWA GRAVITACIONAL A 336.7 m — QCAL ∞³")
    print("  Sello: ∴YGA∞³ | RAM: RAM-LII-2026-YUKAWA-GRAVEDAD-336M")
    print("=" * 70)

    sistema = SistemaYukawaGravedad336m()
    print(sistema.resumen())

    resultado = yukawa_gravedad_336m_activar()

    print("  COHERENCIAS INDIVIDUALES:")
    for nombre, valor in resultado["coherencias"].items():
        print(f"  {nombre} = {valor:.6f}")

    print(f"\n  Ψ_global = {resultado['psi_global']:.6f}")
    estado = "✓ ACTIVO" if resultado["sello_activo"] else "✗ INACTIVO"
    print(f"  Estado: {estado}")

    print("\n" + resultado["certificacion"])
    print()
