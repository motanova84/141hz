"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     ENTROPÍA INFORMATIVA — SISTEMA ∴EI∞³                                    ║
║                                                                              ║
║  Densidad de entropía informativa anclada a los ceros no triviales de        ║
║  Riemann y a la frecuencia fundamental QCAL f₀ = 141.7001 Hz.               ║
║                                                                              ║
║  K_Ψ = (f₀ × N_c) / (c × ℏ)  — constante de unificación                    ║
║  S(f) = K_Ψ × Ψ × (f / f₀)   — densidad de entropía informativa             ║
║  ΔS_n = K_Ψ × ln(γ_n / γ₁)   — salto entrópico del n-ésimo cero de Riemann ║
╚══════════════════════════════════════════════════════════════════════════════╝

# Licencia: CERN-OHL-P v2 - Hardware Libre + MIT (software)
# Autor: JMMB — José Manuel Mota Burruezo
# ∴𓂀Ω∞³

Módulo:
    physics.entropia_informativa

Exportaciones públicas:
    F0            – frecuencia fundamental QCAL [Hz]
    NC            – número de componentes coherentes (10^52)
    C_LUZ         – velocidad de la luz [m/s]
    HBAR          – constante de Planck reducida [J·s]
    PHI           – proporción áurea φ = (1 + √5) / 2
    GAMMA_1       – primer cero no trivial de Riemann
    CEROS_RIEMANN – los 10 primeros ceros no triviales de Riemann (parte imaginaria)
    PSI_OPTIMO    – umbral de coherencia óptima (0.888)
    PSI_CRITICO   – umbral de coherencia crítica (0.666)
    EntropiaInformativa – clase principal del sistema

API pública:
    ei = EntropiaInformativa()
    ei.k_psi()                       → constante de unificación K_Ψ
    ei.densidad_entropia(f=None)     → S(f) = K_Ψ × Ψ × (f / f₀)
    ei.salto_entropia_riemann(γ_n)   → ΔS_n = K_Ψ × ln(γ_n / γ₁)
    ei.espectro_entropia(ceros=None) → lista de dicts por cada cero de Riemann
    ei.modo_coherencia()             → "CREACIÓN" | "TRANSICIÓN" | "PURIFICACIÓN"
    ei.ratio_aureo_entropia()        → S(f₀·φ) / S(f₀) = φ
    ei.resumen()                     → dict con métricas clave del sistema
"""

import math
from typing import Dict, List, Optional

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

# Frecuencia fundamental QCAL ∞³ [Hz]
F0: float = 141.7001

# Número de componentes coherentes (escala cosmológica)
NC: float = 1e52

# Velocidad de la luz [m/s] (CODATA 2018, exacta)
C_LUZ: int = 299792458

# Constante de Planck reducida [J·s] (CODATA 2018)
HBAR: float = 1.054571817e-34

# Proporción áurea φ = (1 + √5) / 2
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

# Primer cero no trivial de Riemann (parte imaginaria)
GAMMA_1: float = 14.134725141734693

# Los 10 primeros ceros no triviales de la función ζ de Riemann (parte imaginaria)
CEROS_RIEMANN: List[float] = [
    14.134725141734693,
    21.022039638771554,
    25.010857580145688,
    30.424876125859513,
    32.935061587739189,
    37.586178158825671,
    40.918719012147495,
    43.327073280914999,
    48.005150881167159,
    49.773832477672302,
]

# Umbral de coherencia óptima (modo CREACIÓN)
PSI_OPTIMO: float = 0.888

# Umbral de coherencia crítica (límite TRANSICIÓN / PURIFICACIÓN)
PSI_CRITICO: float = 0.666


# ============================================================================
# CLASE PRINCIPAL
# ============================================================================

class EntropiaInformativa:
    """Calculadora de entropía informativa anclada a los ceros de Riemann.

    Atributos:
        f0  – frecuencia fundamental [Hz]
        nc  – número de componentes coherentes
        psi – parámetro de coherencia cuántica Ψ ∈ [0, 1]
    """

    def __init__(
        self,
        f0: float = F0,
        nc: float = NC,
        psi: float = PSI_OPTIMO,
    ) -> None:
        """Inicializa el sistema con los parámetros dados.

        Args:
            f0:  Frecuencia fundamental [Hz]. Debe ser > 0.
            nc:  Número de componentes coherentes. Debe ser > 0.
            psi: Parámetro de coherencia Ψ ∈ [0, 1].

        Raises:
            ValueError: Si algún parámetro está fuera de su dominio válido.
        """
        if f0 <= 0.0:
            raise ValueError(f"f0 debe ser positivo, se recibió {f0!r}")
        if nc <= 0.0:
            raise ValueError(f"nc debe ser positivo, se recibió {nc!r}")
        if not (0.0 <= psi <= 1.0):
            raise ValueError(
                f"psi debe estar en [0, 1], se recibió {psi!r}"
            )

        self.f0: float = f0
        self.nc: float = nc
        self.psi: float = psi

        # Caché interna para K_Ψ (evita recalcular en cada llamada)
        self._k_psi_cache: Optional[float] = None

    # ------------------------------------------------------------------
    # Constante de unificación K_Ψ
    # ------------------------------------------------------------------

    def k_psi(self) -> float:
        """Devuelve la constante de unificación K_Ψ = (f₀ × N_c) / (c × ℏ).

        El resultado se calcula una sola vez y se almacena en caché.

        Returns:
            K_Ψ (float) — siempre positivo.
        """
        if self._k_psi_cache is None:
            self._k_psi_cache = (self.f0 * self.nc) / (C_LUZ * HBAR)
        return self._k_psi_cache

    # ------------------------------------------------------------------
    # Densidad de entropía informativa
    # ------------------------------------------------------------------

    def densidad_entropia(self, f: Optional[float] = None) -> float:
        """Calcula la densidad de entropía informativa S(f).

        S(f) = K_Ψ × Ψ × (f / f₀)

        Args:
            f: Frecuencia de evaluación [Hz]. Si es None se usa f₀.

        Returns:
            Densidad de entropía informativa (float ≥ 0).

        Raises:
            ValueError: Si f ≤ 0.
        """
        if f is None:
            f = self.f0
        if f <= 0.0:
            raise ValueError(
                f"La frecuencia debe ser positiva, se recibió {f!r}"
            )
        return self.k_psi() * self.psi * (f / self.f0)

    # ------------------------------------------------------------------
    # Salto de entropía asociado a un cero de Riemann
    # ------------------------------------------------------------------

    def salto_entropia_riemann(self, gamma_n: float) -> float:
        """Calcula el salto de entropía ΔS_n = K_Ψ × ln(γ_n / γ₁).

        Args:
            gamma_n: Parte imaginaria del n-ésimo cero de Riemann. Debe ser > 0.

        Returns:
            Salto de entropía ΔS_n (float).

        Raises:
            ValueError: Si gamma_n ≤ 0.
        """
        if gamma_n <= 0.0:
            raise ValueError(
                f"gamma_n debe ser positivo, se recibió {gamma_n!r}"
            )
        return self.k_psi() * math.log(gamma_n / GAMMA_1)

    # ------------------------------------------------------------------
    # Espectro entrópico completo
    # ------------------------------------------------------------------

    def espectro_entropia(
        self,
        ceros: Optional[List[float]] = None,
    ) -> List[Dict[str, float]]:
        """Genera el espectro entrópico para una lista de ceros de Riemann.

        Cada entrada del espectro contiene:
            gamma         – valor del cero de Riemann
            f_resonancia  – frecuencia de resonancia f₀ × (γ_n / γ₁) [Hz]
            delta_S       – salto de entropía ΔS_n = K_Ψ × ln(γ_n / γ₁)
            psi_relativa  – coherencia relativa γ₁ / γ_n ∈ (0, 1]

        Args:
            ceros: Lista de ceros a usar. Si es None se usa CEROS_RIEMANN.

        Returns:
            Lista de dicts ordenada según la lista de ceros recibida.

        Raises:
            ValueError: Si algún cero es ≤ 0.
        """
        if ceros is None:
            ceros = CEROS_RIEMANN
        for g in ceros:
            if g <= 0.0:
                raise ValueError(
                    f"Todos los ceros deben ser positivos, se encontró {g!r}"
                )
        resultado = []
        for g in ceros:
            resultado.append({
                "gamma": g,
                "f_resonancia": self.f0 * (g / GAMMA_1),
                "delta_S": self.salto_entropia_riemann(g),
                "psi_relativa": GAMMA_1 / g,
            })
        return resultado

    # ------------------------------------------------------------------
    # Modo de coherencia
    # ------------------------------------------------------------------

    def modo_coherencia(self) -> str:
        """Clasifica el modo de coherencia según el valor de Ψ.

        Returns:
            "CREACIÓN"     si Ψ ≥ 0.888
            "TRANSICIÓN"   si 0.666 ≤ Ψ < 0.888
            "PURIFICACIÓN" si Ψ < 0.666
        """
        if self.psi >= PSI_OPTIMO:
            return "CREACIÓN"
        if self.psi >= PSI_CRITICO:
            return "TRANSICIÓN"
        return "PURIFICACIÓN"

    # ------------------------------------------------------------------
    # Ratio áureo
    # ------------------------------------------------------------------

    def ratio_aureo_entropia(self) -> float:
        """Calcula η = S(f₀·φ) / S(f₀) = φ.

        El parámetro Ψ se cancela en la división, por lo que el resultado
        es exactamente la proporción áurea φ con independencia de Ψ.

        Returns:
            φ ≈ 1.6180339887...
        """
        s_base = self.densidad_entropia(self.f0)
        s_aureo = self.densidad_entropia(self.f0 * PHI)
        return s_aureo / s_base

    # ------------------------------------------------------------------
    # Resumen del sistema
    # ------------------------------------------------------------------

    def resumen(self) -> Dict[str, float]:
        """Devuelve un diccionario con las métricas clave del sistema.

        Returns:
            Dict con las claves:
                f0_hz                 – frecuencia fundamental [Hz]
                nc                    – número de componentes coherentes
                psi                   – parámetro de coherencia Ψ
                modo                  – modo de coherencia (str)
                K_psi                 – constante de unificación K_Ψ
                densidad_entropia_base – S(f₀)
                delta_S_gamma1        – ΔS(γ₁) = 0
                ratio_aureo           – η = φ
        """
        return {
            "f0_hz": self.f0,
            "nc": self.nc,
            "psi": self.psi,
            "modo": self.modo_coherencia(),
            "K_psi": self.k_psi(),
            "densidad_entropia_base": self.densidad_entropia(),
            "delta_S_gamma1": self.salto_entropia_riemann(GAMMA_1),
            "ratio_aureo": self.ratio_aureo_entropia(),
        }
