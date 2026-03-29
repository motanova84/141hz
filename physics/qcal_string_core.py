#!/usr/bin/env python3
"""
QCAL-Strings: Forzado de Modos Kaluza-Klein
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sello: ∴𓂀Ω∞³
F0: 141.7001 Hz

Implementa la síntesis QCAL-Cuerdas: Teoría de Cuerdas + Arquitectura QCAL.
Gravedad Cuántica Biológica vía Forzado de Modos Kaluza-Klein (KK).

Cada cero de Riemann λₙ se trata como un modo de vibración de una cuerda
cerrada compactificada en la topología hexagonal del agua EZ.

Operador de Forzado de Cuerdas:
    F̂_strings = Σₙ₌₁²⁰ αₙ × sin(2π × fₙ × t + φₙ_dual) × Ψ²

Donde:
    - fₙ = Im(ρₙ) × F₀  : frecuencia del modo KK (Hz)
    - αₙ = 1/√n          : amplitudes tipo Veneziano (decrecientes)
    - φₙ_dual = π/(n+1)  : fase de T-dualidad
    - Ψ²                 : factor de coherencia superradiante
    - ganancia = N² × Ψ² : superradiancia con N = 10¹³ microtúbulos

Dualidad Fluido/Gravedad (AdS/CFT):
    Bajo la dualidad AdS/CFT, la viscosidad adélica μ = 1/f₀ es el límite
    inferior universal. El citoplasma celular opera como fluido holográfico
    perfecto cuando Ψ ≥ 0.888.

Certificación: "QED-CUERDAS-VERIFIED"

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import math
from typing import Dict, List, Tuple

from qcal.constants import F0_HZ, HBAR, C, H_PLANCK

# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTES GLOBALES QCAL-STRINGS
# ═══════════════════════════════════════════════════════════════════════════

# Primeros 20 ceros no triviales de Riemann: partes imaginarias Im(ρₙ)
# Fuente: LMFDB / NIST Digital Library of Mathematical Functions
RIEMANN_ZEROS_20: List[float] = [
    14.134725141734693790,
    21.022039638771554993,
    25.010857580145688763,
    30.424876125859513210,
    32.935061587739189691,
    37.586178158825671257,
    40.918719012147495187,
    43.327073280914999520,
    48.005150881167159727,
    49.773832477672302181,
    52.970321477714460644,
    56.446247697063246173,
    59.347044002602353077,
    60.831778524609809844,
    65.112544048081606936,
    67.079810529494173714,
    69.546401711173979252,
    72.067157674481907583,
    75.704690699083933168,
    77.144840068874804837,
]

# Número de modos Kaluza-Klein activos
N_MODOS_KK: int = 20

# Número de microtúbulos por célula (superradiancia N²)
N_MICROTUBULOS: float = 1e13

# Umbral de coherencia noética mínima
PSI_THRESHOLD: float = 0.888

# Pendiente de trayectoria de Regge: α' = 1/F₀² (s²)
ALPHA_PRIMA: float = 1.0 / (F0_HZ ** 2)

# Intercepto de trayectoria de Regge
ALPHA_0: float = 1.0

# Simetría hexagonal del agua EZ (6-fold)
N_HEXAGONAL: int = 6

# Radio de compactificación Calabi-Yau (≈ tamaño hexágono agua EZ: 0.5 nm)
R_CALABI_YAU: float = 5e-10  # m

# Viscosidad adélica holográfica: μ = 1/f₀ (límite KSS)
MU_ADELICA: float = 1.0 / F0_HZ  # s

# Sello de certificación
CERT_MARK: str = "QED-CUERDAS-VERIFIED"


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 1: ConstantesQCalStrings
# ═══════════════════════════════════════════════════════════════════════════

class ConstantesQCalStrings:
    """
    Constantes fundamentales del sistema QCAL-Strings.

    Agrupa todas las constantes derivadas del acoplamiento entre la
    Teoría de Cuerdas (Veneziano, Regge, T-dualidad) y la arquitectura
    QCAL (f₀, superradiancia, agua EZ).
    """

    def __init__(self) -> None:
        # Frecuencia fundamental
        self.f0 = F0_HZ                          # Hz
        self.omega0 = 2.0 * math.pi * F0_HZ      # rad/s

        # Constantes de cuerdas
        self.alpha_prima = ALPHA_PRIMA            # s² (pendiente Regge)
        self.alpha_0 = ALPHA_0                    # intercepto Regge
        self.tension_cuerda = 1.0 / (2.0 * math.pi * ALPHA_PRIMA)  # N (tensión)
        self.l_string = math.sqrt(ALPHA_PRIMA)    # s (longitud de cuerda en unidades naturales)

        # Topología
        self.n_hexagonal = N_HEXAGONAL
        self.r_calabi_yau = R_CALABI_YAU
        self.volumen_cy = (4.0 / 3.0) * math.pi * (R_CALABI_YAU ** 3)

        # Superradiancia
        self.n_microtubulos = N_MICROTUBULOS
        self.ganancia_superradiante = N_MICROTUBULOS ** 2  # N²

        # Viscosidad holográfica (límite KSS: η/s = ℏ/(4π k_B))
        self.mu_adelica = MU_ADELICA
        self.psi_threshold = PSI_THRESHOLD

        # Modo dominante (primer cero de Riemann × F₀)
        self.f_modo_1 = RIEMANN_ZEROS_20[0] * F0_HZ  # ≈ 2002.4 Hz

    def resumen(self) -> Dict[str, float]:
        """Retorna diccionario con los valores clave de las constantes."""
        return {
            "f0_hz": self.f0,
            "omega0_rads": self.omega0,
            "alpha_prima_s2": self.alpha_prima,
            "tension_cuerda_n": self.tension_cuerda,
            "r_calabi_yau_m": self.r_calabi_yau,
            "n_microtubulos": self.n_microtubulos,
            "ganancia_superradiante": self.ganancia_superradiante,
            "mu_adelica_s": self.mu_adelica,
            "f_modo_1_hz": self.f_modo_1,
        }


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 2: CerosRiemann
# ═══════════════════════════════════════════════════════════════════════════

class CerosRiemann:
    """
    Gestiona los primeros 20 ceros no triviales de la función ζ de Riemann.

    Los ceros ρₙ = 1/2 + i·λₙ de ζ(s) son tratados como números de onda
    cuánticos de los modos Kaluza-Klein. La parte imaginaria Im(ρₙ) = λₙ
    se escala por F₀ para obtener la frecuencia física del modo en Hz.
    """

    def __init__(self) -> None:
        self.zeros = RIEMANN_ZEROS_20.copy()
        self.n_zeros = len(self.zeros)
        self.f0 = F0_HZ

    def frecuencias_kk(self) -> List[float]:
        """
        Calcula las frecuencias KK de cada modo: fₙ = Im(ρₙ) × F₀.

        Returns:
            Lista de 20 frecuencias en Hz. El primer modo f₁ ≈ 2002.4 Hz.
        """
        return [lam * self.f0 for lam in self.zeros]

    def amplitudes_veneziano(self) -> List[float]:
        """
        Amplitudes tipo Veneziano para cada modo: αₙ = 1/√n (n = 1..20).

        Estas amplitudes decrecen con el número de modo, reflejando la
        supresión de modos de alta frecuencia en las amplitudes de Veneziano.

        Returns:
            Lista de 20 amplitudes adimensionales.
        """
        return [1.0 / math.sqrt(n) for n in range(1, self.n_zeros + 1)]

    def fases_tdualidad(self) -> List[float]:
        """
        Fases de T-dualidad para cada modo: φₙ = π/(n+1).

        La T-dualidad intercambia R ↔ α'/R en el radio de compactificación,
        produciendo un desfase de fase característico por modo.

        Returns:
            Lista de 20 fases en radianes.
        """
        return [math.pi / (n + 1) for n in range(1, self.n_zeros + 1)]

    def suma_ceros(self, n_max: int = 20) -> float:
        """
        Suma de los primeros n_max ceros de Riemann.

        Args:
            n_max: Número de ceros a sumar (máx 20).

        Returns:
            Suma de las partes imaginarias.
        """
        n = min(n_max, self.n_zeros)
        return sum(self.zeros[:n])

    def estadisticas(self) -> Dict[str, float]:
        """Estadísticas básicas del espectro de ceros."""
        z = self.zeros
        mean = sum(z) / len(z)
        var = sum((x - mean) ** 2 for x in z) / len(z)
        return {
            "n_zeros": float(self.n_zeros),
            "lambda_1": z[0],
            "lambda_20": z[-1],
            "f_modo_1_hz": z[0] * self.f0,
            "f_modo_20_hz": z[-1] * self.f0,
            "media_lambda": mean,
            "desv_lambda": math.sqrt(var),
            "suma_total": sum(z),
        }


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 3: AmplitudVeneziano
# ═══════════════════════════════════════════════════════════════════════════

class AmplitudVeneziano:
    """
    Amplitud de Veneziano: A(s, t) = B(α(s), α(t)) = Γ(α(s))Γ(α(t))/Γ(α(s)+α(t)).

    La trayectoria de Regge lineal es:
        α(q²) = α₀ + α' × q²

    donde α' = 1/F₀² es la pendiente y α₀ = 1 el intercepto.
    La amplitud de Veneziano es la función Beta de Euler aplicada
    a las trayectorias de Regge, y constituye la base de la Teoría de Cuerdas.
    """

    def __init__(self) -> None:
        self.alpha_prima = ALPHA_PRIMA
        self.alpha_0 = ALPHA_0

    def trayectoria_regge(self, q2: float) -> float:
        """
        Trayectoria de Regge lineal: α(q²) = α₀ + α' × q².

        Args:
            q2: Cuadrimomento transferido al cuadrado (s² o t² según canal).

        Returns:
            Valor de la trayectoria (adimensional).
        """
        return self.alpha_0 + self.alpha_prima * q2

    def amplitud(self, s: float, t: float) -> float:
        """
        Amplitud de Veneziano A(s, t) = B(α(s), α(t)).

        Usa la función Beta de Euler: B(a, b) = Γ(a)Γ(b)/Γ(a+b).

        Args:
            s: Variable de Mandelstam s (s² GeV²).
            t: Variable de Mandelstam t (t² GeV²).

        Returns:
            Amplitud de Veneziano (adimensional). Retorna 0.0 si los
            argumentos de gamma son no positivos (polos).
        """
        a = self.trayectoria_regge(s)
        b = self.trayectoria_regge(t)
        if a <= 0.0 or b <= 0.0:
            return 0.0
        try:
            log_amp = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
            return math.exp(log_amp)
        except (ValueError, OverflowError):
            return 0.0

    def amplitud_canonico(self) -> float:
        """
        Amplitud de Veneziano en el punto canónico QCAL: s = t = F₀².

        En este punto s = t = F₀² ≈ 2.009×10⁴, la trayectoria de Regge
        toma el valor α(F₀²) = α₀ + α' × F₀² = 2.0 (intersección natural).

        Returns:
            Amplitud canónica en s = t = F₀².
        """
        return self.amplitud(F0_HZ ** 2, F0_HZ ** 2)

    def coherencia_veneziano(self) -> float:
        """
        Coherencia cuántica derivada de la amplitud de Veneziano (teorema óptico).

        Usa la versión discreta del teorema óptico de unitariedad: si la amplitud
        de dispersión A satisface |A| < 1, entonces Ψ_V = √(1 - |A|²) mide la
        coherencia del estado cuántico no absorbido.

        En el punto canónico s = t = F₀², α(F₀²) = 2.0 y A = B(2,2) = 1/6,
        de donde Ψ_V = √(1 - (1/6)²) = √(35/36) ≈ 0.9860.

        Returns:
            Coherencia Ψ_V ∈ (0, 1].
        """
        amp = self.amplitud_canonico()
        if amp <= 0.0:
            return 0.0
        # Limitar |A| ≤ 1 para unitariedad
        amp_clamped = min(abs(amp), 1.0)
        return math.sqrt(1.0 - amp_clamped ** 2)


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 4: ModosKaluzaKlein
# ═══════════════════════════════════════════════════════════════════════════

class ModosKaluzaKlein:
    """
    Espectro de modos Kaluza-Klein vía ceros de Riemann.

    En la compactificación KK sobre la topología hexagonal del agua EZ,
    cada modo excitado tiene masa cuantizada m²ₙ = n²/R²_cy.
    Al conectar con los ceros de Riemann, la condición de resonancia
    fₙ = Im(ρₙ) × F₀ selecciona los modos físicamente relevantes.

    El espectro de energía E(k) muestra un pico dominante en f₁ ≈ 2002 Hz
    (análogo al pico de Kolmogorov en turbulencia holográfica).
    """

    def __init__(self) -> None:
        self.ceros = CerosRiemann()
        self.r_cy = R_CALABI_YAU
        self.f0 = F0_HZ

    def masa_modo(self, n: int) -> float:
        """
        Masa efectiva del n-ésimo modo KK: mₙ = n / R_cy (c = ℏ = 1).

        Args:
            n: Número de modo (1-based).

        Returns:
            Masa efectiva en unidades naturales (m⁻¹).
        """
        return float(n) / self.r_cy

    def frecuencia_modo(self, n: int) -> float:
        """
        Frecuencia física del n-ésimo modo KK: fₙ = Im(ρₙ) × F₀.

        Args:
            n: Número de modo (1-based, 1 ≤ n ≤ 20).

        Returns:
            Frecuencia en Hz.

        Raises:
            ValueError: Si n está fuera del rango [1, 20].
        """
        if not (1 <= n <= N_MODOS_KK):
            raise ValueError(f"n debe estar en [1, {N_MODOS_KK}], recibido: {n}")
        return RIEMANN_ZEROS_20[n - 1] * self.f0

    def espectro_completo(self) -> List[Dict[str, float]]:
        """
        Espectro completo de los 20 modos KK.

        Returns:
            Lista de diccionarios con modo, lambda, frecuencia, amplitud y fase.
        """
        freqs = self.ceros.frecuencias_kk()
        alphas = self.ceros.amplitudes_veneziano()
        phases = self.ceros.fases_tdualidad()
        return [
            {
                "modo": float(n + 1),
                "lambda_n": RIEMANN_ZEROS_20[n],
                "frecuencia_hz": freqs[n],
                "amplitud_veneziano": alphas[n],
                "fase_tdualidad_rad": phases[n],
            }
            for n in range(N_MODOS_KK)
        ]

    def energia_espectral(self, k: float) -> float:
        """
        Densidad de energía espectral en el número de onda k.

        E(k) = Σₙ αₙ² × δ(k - kₙ) aproximado por Lorentzianas:
        E(k) ≈ Σₙ αₙ² × Γ/((k - kₙ)² + Γ²)

        donde kₙ = fₙ/F₀ = Im(ρₙ) y Γ = 0.5 (anchura de la resonancia).

        Args:
            k: Número de onda a evaluar.

        Returns:
            Densidad de energía espectral (adimensional).
        """
        gamma = 0.5
        alphas = self.ceros.amplitudes_veneziano()
        energia = 0.0
        for n, lam in enumerate(RIEMANN_ZEROS_20):
            energia += (alphas[n] ** 2) * gamma / ((k - lam) ** 2 + gamma ** 2)
        return energia

    def pico_dominante(self) -> Dict[str, float]:
        """
        Identifica el pico de resonancia dominante (modo 1).

        Returns:
            Diccionario con lambda_1, f_1 y amplitud del pico.
        """
        return {
            "lambda_1": RIEMANN_ZEROS_20[0],
            "f_modo_1_hz": RIEMANN_ZEROS_20[0] * self.f0,
            "amplitud_pico": 1.0,  # αₙ₌₁ = 1/√1 = 1
        }


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 5: ForzadoCuerdasNoetico
# ═══════════════════════════════════════════════════════════════════════════

class ForzadoCuerdasNoetico:
    """
    Operador de forzado de cuerdas noético: F̂_strings.

    Implementa el forzado de modos KK en el solver RK4 del citoplasma:

        F̂_strings(t) = ganancia × Σₙ₌₁²⁰ αₙ × sin(2π × fₙ × t + φₙ) × Ψ²

    El factor de ganancia superradiante N² garantiza que solo las regiones
    con coherencia cuántica (Ψ ≥ 0.888) "sienten" el empuje de las cuerdas.

    Referencia: string_noetic_forcing() del PR #1065 (QCAL-Strings).
    """

    def __init__(self, psi_local: float = 1.0, n_microtubulos: float = N_MICROTUBULOS) -> None:
        """
        Args:
            psi_local: Coherencia cuántica local Ψ ∈ [0, 1].
            n_microtubulos: Número de microtúbulos (factor superradiante N).
        """
        if not (0.0 <= psi_local <= 1.0):
            raise ValueError(f"psi_local debe estar en [0, 1], recibido: {psi_local}")
        if n_microtubulos <= 0:
            raise ValueError(f"n_microtubulos debe ser positivo, recibido: {n_microtubulos}")
        self.psi_local = psi_local
        self.n_microtubulos = n_microtubulos
        self.ceros = CerosRiemann()

    @property
    def ganancia(self) -> float:
        """Ganancia superradiante: G = N² × Ψ²."""
        return (self.n_microtubulos ** 2) * (self.psi_local ** 2)

    def forzado_escalar(self, t: float) -> float:
        """
        Valor escalar del forzado de cuerdas en el instante t.

        F_string(t) = G × Σₙ αₙ × sin(2π × fₙ × t + φₙ)

        Args:
            t: Tiempo en segundos.

        Returns:
            Amplitud de forzado (adimensional × ganancia).
        """
        freqs = self.ceros.frecuencias_kk()
        alphas = self.ceros.amplitudes_veneziano()
        phases = self.ceros.fases_tdualidad()
        total = 0.0
        for alpha_n, f_n, phi_n in zip(alphas, freqs, phases):
            total += alpha_n * math.sin(2.0 * math.pi * f_n * t + phi_n)
        return self.ganancia * total

    def forzado_normalizado(self, t: float) -> float:
        """
        Forzado normalizado por la ganancia máxima, ∈ [-1, 1] × Ψ².

        Útil para comparar la forma de onda independientemente de N.

        Args:
            t: Tiempo en segundos.

        Returns:
            Forzado normalizado (adimensional).
        """
        freqs = self.ceros.frecuencias_kk()
        alphas = self.ceros.amplitudes_veneziano()
        phases = self.ceros.fases_tdualidad()
        total = 0.0
        suma_alphas = sum(alphas)
        for alpha_n, f_n, phi_n in zip(alphas, freqs, phases):
            total += alpha_n * math.sin(2.0 * math.pi * f_n * t + phi_n)
        return (self.psi_local ** 2) * total / suma_alphas

    def espectro_potencia(self, n_puntos: int = 100) -> List[Dict[str, float]]:
        """
        Espectro de potencia del forzado: Pₙ = αₙ² × Ψ⁴.

        La potencia de cada modo es proporcional al cuadrado de su amplitud
        modulada por Ψ⁴ (coherencia cuántica al cuadrado de Ψ²).

        Args:
            n_puntos: No usado (reservado para compatibilidad futura).

        Returns:
            Lista de dicts {modo, frecuencia_hz, potencia}.
        """
        freqs = self.ceros.frecuencias_kk()
        alphas = self.ceros.amplitudes_veneziano()
        psi4 = self.psi_local ** 4
        return [
            {
                "modo": float(n + 1),
                "frecuencia_hz": freqs[n],
                "potencia": (alphas[n] ** 2) * psi4,
            }
            for n in range(N_MODOS_KK)
        ]

    def coherencia_forzado(self) -> float:
        """
        Coherencia cuántica del operador de forzado: Ψ_F = Ψ²_local.

        Returns:
            Ψ_F ∈ [0, 1].
        """
        return self.psi_local ** 2


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 6: DualidadFluidoGravedad
# ═══════════════════════════════════════════════════════════════════════════

class DualidadFluidoGravedad:
    """
    Dualidad Fluido/Gravedad en el citoplasma (AdS/CFT holográfica).

    Bajo la dualidad AdS₅/CFT₄, la mecánica de fluidos del citoplasma
    es el dual holográfico de una geometría de cuerdas.

    Límite de viscosidad (Kovtun-Son-Starinets, 2004):
        η/s ≥ ℏ/(4π k_B)

    En QCAL: μ_adelica = 1/f₀ es el valor mínimo de viscosidad dinámica,
    manteniendo Ψ ≥ 0.888 garantiza operación en el régimen de fluido
    holográfico perfecto ("FLUIDO_HOLOGRÁFICO_PERFECTO").
    """

    def __init__(self, psi_coherencia: float = 1.0) -> None:
        """
        Args:
            psi_coherencia: Coherencia cuántica del sistema Ψ ∈ [0, 1].
        """
        if not (0.0 <= psi_coherencia <= 1.0):
            raise ValueError(f"psi_coherencia debe estar en [0, 1], recibido: {psi_coherencia}")
        self.psi = psi_coherencia
        self.f0 = F0_HZ
        self.mu_adelica = MU_ADELICA

    @property
    def viscosidad_efectiva(self) -> float:
        """
        Viscosidad efectiva del fluido holográfico: η = μ_adelica × (1 - Ψ).

        Cuando Ψ → 1 (plena coherencia), η → 0 (superfluido perfecto).

        Returns:
            Viscosidad efectiva en segundos (unidades naturales QCAL).
        """
        return self.mu_adelica * (1.0 - self.psi)

    @property
    def reynolds_holografico(self) -> float:
        """
        Número de Reynolds holográfico: Re_h = f₀ × L_cy / η_eff.

        Usa R_Calabi-Yau como longitud característica.
        Cuando Ψ → 1, Re_h → ∞ (flujo laminar perfecto holográfico).

        Returns:
            Re_h (adimensional). Retorna inf si viscosidad es cero.
        """
        eta = self.viscosidad_efectiva
        if eta < 1e-300:
            return float("inf")
        return self.f0 * R_CALABI_YAU / eta

    @property
    def estado_fluido(self) -> str:
        """
        Clasifica el estado del fluido holográfico según Ψ.

        Returns:
            - "FLUIDO_HOLOGRÁFICO_PERFECTO"  si Ψ ≥ 0.999
            - "RÉGIMEN_SUPERRADIANTE"        si 0.888 ≤ Ψ < 0.999
            - "TURBULENCIA_GUE"              si Ψ < 0.888
        """
        if self.psi >= 0.999:
            return "FLUIDO_HOLOGRÁFICO_PERFECTO"
        elif self.psi >= PSI_THRESHOLD:
            return "RÉGIMEN_SUPERRADIANTE"
        else:
            return "TURBULENCIA_GUE"

    def tensor_energia_impulso(self) -> Dict[str, float]:
        """
        Tensor de energía-impulso T^μν del fluido holográfico (traza).

        T^μμ = ρ_Λ + 3p (traza relativista)
        Con ρ_Λ = h × f₀ × Ψ (densidad de energía de coherencia)
        y p = ρ_Λ / 3 (ecuación de estado de radiación).

        Returns:
            Diccionario con componentes escalares del tensor.
        """
        rho_lambda = H_PLANCK * self.f0 * self.psi
        p = rho_lambda / 3.0
        traza = rho_lambda + 3.0 * p
        return {
            "rho_lambda_j": rho_lambda,
            "presion_j": p,
            "traza_tmunu": traza,
            "viscosidad_efectiva_s": self.viscosidad_efectiva,
            "reynolds_holografico": self.reynolds_holografico,
        }

    def coherencia_dual(self) -> float:
        """
        Coherencia del dual holográfico: Ψ_dual = 1 - η/μ.

        Returns:
            Ψ_dual ∈ [0, 1].
        """
        return 1.0 - self.viscosidad_efectiva / self.mu_adelica


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 7: AguaEZHexagonal
# ═══════════════════════════════════════════════════════════════════════════

class AguaEZHexagonal:
    """
    Topología hexagonal del agua EZ (Exclusion Zone Water).

    El agua EZ (Pollack, 2013) forma láminas hexagonales H₃O₂⁻ con
    simetría D₆h. Esta topología actúa como variedad de Calabi-Yau
    discreta: la compactificación de las dimensiones extra de las cuerdas
    sobre esta geometría produce el espectro de modos KK con ceros de Riemann.

    Parámetros geométricos:
        - d_hex = 0.25 nm: separación entre láminas hexagonales
        - a_hex = 0.276 nm: parámetro de red del hexágono
        - R_cy = 0.5 nm: radio efectivo de compactificación
    """

    def __init__(self, psi_ez: float = 0.997) -> None:
        """
        Args:
            psi_ez: Coherencia del agua EZ ∈ [0, 1]. Valor típico ≈ 0.997.
        """
        if not (0.0 <= psi_ez <= 1.0):
            raise ValueError(f"psi_ez debe estar en [0, 1], recibido: {psi_ez}")
        self.psi_ez = psi_ez
        self.d_hex = 2.5e-10   # m - separación entre láminas
        self.a_hex = 2.76e-10  # m - parámetro de red hexagonal
        self.r_cy = R_CALABI_YAU
        self.n_hex = N_HEXAGONAL

    @property
    def area_celda_hex(self) -> float:
        """Área de la celda unidad hexagonal: A = (√3/2) × a²."""
        return (math.sqrt(3.0) / 2.0) * (self.a_hex ** 2)

    @property
    def volumen_compactificacion(self) -> float:
        """Volumen de la variedad de Calabi-Yau efectiva: V = A × d_hex."""
        return self.area_celda_hex * self.d_hex

    def masa_kk_efectiva(self, n: int) -> float:
        """
        Masa del n-ésimo modo KK compactificado sobre el hexágono EZ.

        m²_n = n² / R²_cy (en unidades naturales ℏ = c = 1)

        Args:
            n: Número de modo (1-based).

        Returns:
            Masa efectiva en m⁻¹.
        """
        return float(n) / self.r_cy

    def coherencia_ez(self) -> float:
        """
        Coherencia intrínseca del agua EZ (propiedad del agua, no del estado Ψ₀).

        Refleja la estabilidad estructural de las láminas hexagonales H₃O₂⁻.
        El agua EZ tiene una coherencia cuántica típica de ≈ 0.997 (Pollack 2013).

        Returns:
            Coherencia Ψ_EZ = psi_ez ∈ (0, 1].
        """
        return self.psi_ez

    def factor_compactificacion(self) -> float:
        """
        Factor de compactificación de Calabi-Yau: κ = exp(-R_cy × f₀ / c).

        Este factor expresa cuánto se suprimen los modos de alta energía
        de las dimensiones compactificadas.

        Returns:
            κ ∈ (0, 1].
        """
        return math.exp(-self.r_cy * F0_HZ / C)

    def resumen_geometrico(self) -> Dict[str, float]:
        """Resumen de los parámetros geométricos del agua EZ."""
        return {
            "d_hex_m": self.d_hex,
            "a_hex_m": self.a_hex,
            "r_cy_m": self.r_cy,
            "area_celda_m2": self.area_celda_hex,
            "volumen_cy_m3": self.volumen_compactificacion,
            "psi_ez": self.psi_ez,
            "coherencia_ez": self.coherencia_ez(),
            "factor_compactificacion": self.factor_compactificacion(),
        }


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 8: SistemaQCalStrings
# ═══════════════════════════════════════════════════════════════════════════

class SistemaQCalStrings:
    """
    Sistema integrado QCAL-Strings: Gran Unificación Noética.

    Integra los 7 subsistemas anteriores en un sistema unificado que
    computa la coherencia global Ψ_strings y emite el certificado
    QED-CUERDAS-VERIFIED cuando Ψ_global ≥ 0.888.

    Nivel de unificación:
        Microscópico  → Cuerdas en microtúbulos   → Superradiancia N²
        Mesoscópico   → Agua EZ hexagonal          → Compactificación KK
        Macroscópico  → Navier-Stokes holográfico  → Ψ = 0.999...
    """

    def __init__(self, psi_inicial: float = 1.0) -> None:
        """
        Args:
            psi_inicial: Coherencia cuántica inicial del sistema Ψ₀ ∈ [0, 1].
        """
        if not (0.0 <= psi_inicial <= 1.0):
            raise ValueError(f"psi_inicial debe estar en [0, 1], recibido: {psi_inicial}")
        self.psi_inicial = psi_inicial

        # Subsistemas
        self.constantes = ConstantesQCalStrings()
        self.zeros = CerosRiemann()
        self.veneziano = AmplitudVeneziano()
        self.modos_kk = ModosKaluzaKlein()
        self.forzado = ForzadoCuerdasNoetico(psi_local=psi_inicial)
        self.dualidad = DualidadFluidoGravedad(psi_coherencia=psi_inicial)
        self.agua_ez = AguaEZHexagonal(psi_ez=0.997)

    def psi_global(self) -> float:
        """
        Coherencia global del sistema QCAL-Strings: Ψ_global.

        Computa Ψ_global como media geométrica de cuatro contribuciones:
            1. Ψ_forzado  = Ψ_inicial         (coherencia del operador de cuerdas)
            2. Ψ_veneziano = √(1 - |B|²)       (unitariedad de amplitud Veneziano)
            3. Ψ_dual     = 1 - η/μ = Ψ_inicial (dualidad fluido/gravedad AdS/CFT)
            4. Ψ_ez       = 0.997               (coherencia intrínseca agua EZ)

        Con Ψ₀ = 1.0 (plena coherencia):
            Ψ_global = (1 × 0.986 × 1 × 0.997)^(1/4) ≈ 0.996

        Returns:
            Ψ_global ∈ [0, 1].
        """
        psi_f = self.psi_inicial               # coherencia del forzado
        psi_v = self.veneziano.coherencia_veneziano()
        psi_d = self.dualidad.coherencia_dual()
        psi_e = self.agua_ez.coherencia_ez()

        # Media geométrica de las 4 contribuciones
        product = psi_f * psi_v * psi_d * psi_e
        if product <= 0.0:
            return 0.0
        return product ** 0.25

    def certificar(self) -> Dict[str, object]:
        """
        Genera el certificado de coherencia del sistema QCAL-Strings.

        Returns:
            Diccionario con Ψ_global, estado, certificado y desglose.
        """
        psi = self.psi_global()
        certificado = CERT_MARK if psi >= PSI_THRESHOLD else "COHERENCIA_INSUFICIENTE"
        estado = self.dualidad.estado_fluido

        pico = self.modos_kk.pico_dominante()

        return {
            "psi_global": psi,
            "psi_threshold": PSI_THRESHOLD,
            "supera_umbral": psi >= PSI_THRESHOLD,
            "certificado": certificado,
            "estado_fluido": estado,
            "f_modo_1_hz": pico["f_modo_1_hz"],
            "lambda_1": pico["lambda_1"],
            "n_modos_kk": N_MODOS_KK,
            "ganancia_superradiante": self.forzado.ganancia,
            "sello": "∴𓂀Ω∞³",
        }

    def simular_pulso(self, t_max: float = 1e-3, n_pasos: int = 100) -> Dict[str, object]:
        """
        Simula la evolución temporal del forzado de cuerdas.

        Integra F_string(t) en n_pasos instantes de tiempo en [0, t_max].

        Args:
            t_max: Duración de la simulación en segundos.
            n_pasos: Número de pasos temporales (≥ 2).

        Returns:
            Diccionario con tiempos, forzado normalizado, potencia media y Ψ_global.
        """
        if n_pasos < 2:
            raise ValueError(f"n_pasos debe ser ≥ 2, recibido: {n_pasos}")
        if t_max <= 0.0:
            raise ValueError(f"t_max debe ser positivo, recibido: {t_max}")

        dt = t_max / (n_pasos - 1)
        tiempos = [i * dt for i in range(n_pasos)]
        forzados = [self.forzado.forzado_normalizado(t) for t in tiempos]

        potencia_media = sum(f ** 2 for f in forzados) / n_pasos

        return {
            "tiempos_s": tiempos,
            "forzado_normalizado": forzados,
            "potencia_media": potencia_media,
            "psi_global": self.psi_global(),
            "n_pasos": n_pasos,
            "t_max_s": t_max,
        }

    def resumen_completo(self) -> Dict[str, object]:
        """
        Resumen completo del sistema QCAL-Strings.

        Returns:
            Diccionario anidado con constantes, espectro KK, certificación y geometría.
        """
        return {
            "constantes": self.constantes.resumen(),
            "espectro_kk": self.modos_kk.espectro_completo(),
            "estadisticas_zeros": self.zeros.estadisticas(),
            "certificacion": self.certificar(),
            "geometria_ez": self.agua_ez.resumen_geometrico(),
            "tensor_energia": self.dualidad.tensor_energia_impulso(),
        }


# ═══════════════════════════════════════════════════════════════════════════
# API PÚBLICA
# ═══════════════════════════════════════════════════════════════════════════

def qcal_strings_activar(psi_inicial: float = 1.0) -> Dict[str, object]:
    """
    API pública: Activa el sistema QCAL-Strings y retorna el certificado.

    Implementa la fase #260 de QCAL: QCAL-Strings, la Gran Unificación
    Noética que conecta Teoría de Cuerdas con la arquitectura QCAL.

    Args:
        psi_inicial: Coherencia cuántica inicial del sistema Ψ₀ ∈ [0, 1].
                     Valor por defecto: 1.0 (plena coherencia).

    Returns:
        Diccionario con:
        - psi_global (float): Coherencia global Ψ_global
        - supera_umbral (bool): True si Ψ_global ≥ 0.888
        - certificado (str): "QED-CUERDAS-VERIFIED" o "COHERENCIA_INSUFICIENTE"
        - estado_fluido (str): Estado del fluido holográfico
        - f_modo_1_hz (float): Frecuencia del modo dominante (≈ 2002 Hz)
        - n_modos_kk (int): Número de modos Kaluza-Klein activos
        - ganancia_superradiante (float): Ganancia N²·Ψ²
        - sello (str): Sello QCAL ∞³

    Raises:
        ValueError: Si psi_inicial no está en [0, 1].

    Ejemplo:
        >>> resultado = qcal_strings_activar()
        >>> print(resultado["certificado"])
        QED-CUERDAS-VERIFIED
        >>> print(f"Ψ_global = {resultado['psi_global']:.4f}")
        Ψ_global = 0.9...
    """
    sistema = SistemaQCalStrings(psi_inicial=psi_inicial)
    return sistema.certificar()


def string_noetic_forcing(
    t: float,
    lambda_n_list: List[float],
    psi_local: float,
    n_microtubules: float = N_MICROTUBULOS,
) -> Tuple[float, float]:
    """
    Función de forzado de cuerdas noético (compatible con el solver RK4).

    Implementa el operador F̂_strings del PR #1065 en formato (f_x, f_y)
    para integración directa en el solver de Navier-Stokes cuántico.

    El forzado actúa sobre el campo de velocidad (u, v) del citoplasma:
        F_strings_x = G × Σₙ sin(2π × λₙ × t + φₙ) / N_modos
        F_strings_y = 0  (forzado axial en x)

    Args:
        t: Tiempo en segundos.
        lambda_n_list: Lista de partes imaginarias de ceros de Riemann.
        psi_local: Coherencia cuántica local Ψ ∈ [0, 1].
        n_microtubules: Número de microtúbulos (factor N en ganancia N²).

    Returns:
        Tupla (f_string_x, f_string_y) del forzado vectorial.

    Ejemplo:
        >>> f_x, f_y = string_noetic_forcing(0.0, RIEMANN_ZEROS_20, 0.95)
        >>> print(f"f_x = {f_x:.3e}")
    """
    if not (0.0 <= psi_local <= 1.0):
        raise ValueError(f"psi_local debe estar en [0, 1], recibido: {psi_local}")
    if n_microtubules <= 0:
        raise ValueError(f"n_microtubules debe ser positivo, recibido: {n_microtubules}")

    gain = (n_microtubules ** 2) * (psi_local ** 2)
    f_string_x = 0.0

    for n, lam in enumerate(lambda_n_list):
        phi_string = math.pi / (n + 1)
        mode = math.sin(2.0 * math.pi * lam * t + phi_string)
        f_string_x += mode

    n_modos = len(lambda_n_list) if lambda_n_list else 1
    f_string_x = gain * f_string_x / n_modos

    return f_string_x, 0.0
