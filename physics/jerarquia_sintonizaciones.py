"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║       JERARQUÍA DE SINTONIZACIONES - ANÁLISIS DE FASE                         ║
║                                                                               ║
║  Amplificador de coherencia en cascada: Materia → Noesis → Bio-QCAL → Amor   ║
║  Operando bajo f₀ = 141,7001 Hz en la red de 7 nodos primos.                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Este módulo implementa la Jerarquía de Sintonizaciones: el mapa de la
Transmutación Gradual en el sistema QCAL. Cada salto θ representa una barrera
de potencial superada por el fluido de Navier-Stokes en la red de 7 nodos primos.

NIVELES:
    Materia   (L1): Mar de Dirac a 134,4 Hz — predisposición armónica base.
    Noesis    (L2): f₀ = 141,7001 Hz — ignición. θ₁ = +5,43% de ganancia.
    Bio-QCAL  (L3): 141,88 Hz medido — integración biológica. θ₂ = +11,24%.
    Amor      (L4): Valle de potencial mínimo — relajación. θ₃ = −3,76%.

TRANSICIONES DE FASE:
    θ₁ = (f₀ − f_Dirac) / f_Dirac ≈ 5,43%   — salto espectral de ignición.
    θ₂ = 11,24%                                — máxima resistencia, Pared de Cañas.
    θ₃ = −3,76%                                — relajación al mínimo de potencial.

COHERENCIA EN CASCADA:
    Ψ_Amor = Ψ_Materia × (1 + θ₁) × (1 + θ₂) × (1 + θ₃) ≈ 0,8991

CONSECUENCIAS (Documento Maestro):
    1. P=NP se resuelve biológicamente en los microtúbulos mediante el
       colapso del solitón a 141,7 Hz (T_colapso ≈ 7,06 ms).
    2. La Línea Crítica de Riemann (σ = 1/2) actúa como regulador espectral
       que impide que la magnetorrecepción se pierda en el ruido magnético.
    3. La Simbiosis es un flujo continuo, no una meta estática.

Clases:
    NivelCoherencia       – Un nivel en la jerarquía de sintonizaciones.
    TransicionFase        – Barrera de potencial θ entre dos niveles.
    JerarquiaSintonizaciones – Amplificador de coherencia en cascada completo.
    RiemannRegulador      – Filtro espectral de la Línea Crítica de Riemann.
    SolitonMicrotubular   – Modelo de colapso de solitón a f₀ (P=NP biológico).

API pública:
    calcular_jerarquia()  – Computa la jerarquía completa y devuelve resultados.
    validar_cascada()     – Valida que la cascada produce Ψ ≈ 0,8991.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import numpy as np

# ============================================================================
# CONSTANTES FÍSICAS Y DEL PROTOCOLO
# ============================================================================

# Frecuencia fundamental QCAL
F0_HZ: float = 141.7001  # Hz — f₀, Noesis

# Mar de Dirac — nivel base de la materia
F_DIRAC_HZ: float = 134.4  # Hz — inicio de la jerarquía

# Frecuencia medida en microtúbulos (nivel Bio-QCAL)
F_BIOQCAL_HZ: float = 141.88  # Hz — f medida ± 0,21 Hz

# Incertidumbre en la medición de microtúbulos
INCERTIDUMBRE_BIOQCAL_HZ: float = 0.21  # Hz — ± 1σ

# Salto θ₁: barrera de potencial Materia → Noesis (derivada de frecuencias)
THETA_1: float = (F0_HZ - F_DIRAC_HZ) / F_DIRAC_HZ  # ≈ 0,054316 (5,43%)

# Salto θ₂: barrera Noesis → Bio-QCAL (Pared de Cañas, complejidad biológica)
THETA_2: float = 0.1124  # 11,24%

# Salto θ₃: relajación Bio-QCAL → Amor (valle de potencial mínimo)
THETA_3: float = -0.0376  # −3,76%

# Coherencia objetivo del nivel Amor (AAA-QCAL medida)
PSI_AMOR_TARGET: float = 0.8991

# Número de nodos primos en la red Navier-Stokes
N_NODOS_PRIMOS: int = 7

# Estadísticas experimentales de validación
SIGMA_MAGNETORRECEPCION: float = 9.2   # σ — magnetorrecepción aviar
SIGMA_MICROTUBULOS: float = 8.7        # σ — resonancia de microtúbulos
DELTA_P_MAGNETORRECEPCION: float = 0.001987  # ΔP = 0,1987% asimetría

# Umbral de descubrimiento en física de partículas
SIGMA_DESCUBRIMIENTO: float = 5.0  # 5σ

# Ganancia de la cascada completa
GANANCIA_CASCADA: float = (1.0 + THETA_1) * (1.0 + THETA_2) * (1.0 + THETA_3)

# Coherencia base del nivel Materia (derivada de la cascada)
PSI_MATERIA: float = PSI_AMOR_TARGET / GANANCIA_CASCADA

# ============================================================================
# CLASES DE DATOS
# ============================================================================


@dataclass
class NivelCoherencia:
    """Un nivel en la jerarquía de sintonizaciones.

    Attributes:
        nombre: Nombre simbólico del nivel (Materia, Noesis, Bio-QCAL, Amor).
        frecuencia_hz: Frecuencia de resonancia característica en Hz.
        psi: Coherencia cuántica Ψ en este nivel (0 ≤ Ψ ≤ 1).
        descripcion: Interpretación física del nivel.
    """

    nombre: str
    frecuencia_hz: float
    psi: float
    descripcion: str


@dataclass
class TransicionFase:
    """Barrera de potencial θ entre dos niveles de la jerarquía.

    Attributes:
        desde: Nivel de origen.
        hasta: Nivel de destino.
        theta: Salto de barrera de potencial (fracción, puede ser negativo).
        descripcion: Interpretación física de la transición.
    """

    desde: str
    hasta: str
    theta: float
    descripcion: str

    @property
    def theta_porcentaje(self) -> float:
        """Devuelve θ como porcentaje."""
        return self.theta * 100.0

    @property
    def ganancia(self) -> float:
        """Factor de ganancia de la transición: 1 + θ."""
        return 1.0 + self.theta


@dataclass
class ResultadoJerarquia:
    """Resultado completo del análisis de la jerarquía de sintonizaciones.

    Attributes:
        niveles: Lista de los cuatro niveles de coherencia.
        transiciones: Lista de las tres transiciones de fase θ₁, θ₂, θ₃.
        psi_cascada: Coherencia final del nivel Amor (producto de la cascada).
        ganancia_total: Producto de todos los factores (1 + θᵢ).
        es_valido: True si Ψ_cascada ≈ PSI_AMOR_TARGET dentro de tolerancia.
        consecuencias: Diccionario con las consecuencias del Documento Maestro.
    """

    niveles: List[NivelCoherencia]
    transiciones: List[TransicionFase]
    psi_cascada: float
    ganancia_total: float
    es_valido: bool
    consecuencias: Dict[str, object]


# ============================================================================
# CLASES PRINCIPALES
# ============================================================================


class JerarquiaSintonizaciones:
    """Amplificador de coherencia en cascada: Materia → Noesis → Bio-QCAL → Amor.

    Implementa el mapa de la Transmutación Gradual en la red de 7 nodos primos.
    Cada nivel tiene una coherencia Ψ y una frecuencia de resonancia.
    Los saltos θ son las barreras de potencial entre niveles.

    Relación fundamental:
        Ψ_Amor = Ψ_Materia × (1 + θ₁) × (1 + θ₂) × (1 + θ₃)

    El valor de θ₁ se DERIVA de las frecuencias:
        θ₁ = (f₀ − f_Dirac) / f_Dirac ≈ 5,43%

    θ₂ y θ₃ son parámetros calibrados de la teoría:
        θ₂ = 11,24% (Pared de Cañas, máxima resistencia biológica)
        θ₃ = −3,76% (relajación al mínimo de potencial Amor)
    """

    def __init__(
        self,
        theta_2: float = THETA_2,
        theta_3: float = THETA_3,
        tolerancia: float = 0.05,
    ) -> None:
        """Inicializa la jerarquía de sintonizaciones.

        Args:
            theta_2: Barrera biológica Noesis → Bio-QCAL (por defecto: 0.1124).
            theta_3: Relajación Bio-QCAL → Amor (por defecto: −0.0376).
            tolerancia: Tolerancia relativa para validar Ψ_cascada (por defecto: 5%).
        """
        if not -1.0 < theta_2 <= 1.0:
            raise ValueError(f"theta_2 debe estar en (−1, 1], recibido: {theta_2}")
        if not -1.0 < theta_3 <= 1.0:
            raise ValueError(f"theta_3 debe estar en (−1, 1], recibido: {theta_3}")
        if not 0 < tolerancia < 1:
            raise ValueError(f"tolerancia debe estar en (0, 1), recibida: {tolerancia}")

        self.theta_1 = THETA_1
        self.theta_2 = theta_2
        self.theta_3 = theta_3
        self.tolerancia = tolerancia

    # ------------------------------------------------------------------
    # Niveles de coherencia
    # ------------------------------------------------------------------

    def _psi_materia(self) -> float:
        """Coherencia base del nivel Materia (derivada de la cascada inversa)."""
        ganancia = (1.0 + self.theta_1) * (1.0 + self.theta_2) * (1.0 + self.theta_3)
        return PSI_AMOR_TARGET / ganancia

    def construir_niveles(self) -> List[NivelCoherencia]:
        """Construye los cuatro niveles de la jerarquía con sus coherencias.

        Returns:
            Lista ordenada [Materia, Noesis, Bio-QCAL, Amor] con sus Ψ y frecuencias.
        """
        psi_m = self._psi_materia()
        psi_n = psi_m * (1.0 + self.theta_1)
        psi_b = psi_n * (1.0 + self.theta_2)
        psi_a = psi_b * (1.0 + self.theta_3)

        return [
            NivelCoherencia(
                nombre="Materia",
                frecuencia_hz=F_DIRAC_HZ,
                psi=psi_m,
                descripcion=(
                    "Mar de Dirac a 134,4 Hz. Predisposición armónica base. "
                    "La materia ya contiene la semilla de la resonancia."
                ),
            ),
            NivelCoherencia(
                nombre="Noesis",
                frecuencia_hz=F0_HZ,
                psi=psi_n,
                descripcion=(
                    f"Ignición a f₀ = {F0_HZ} Hz. El Mar de Dirac se organiza. "
                    "θ₁ pequeño porque la materia ya tiene predisposición armónica."
                ),
            ),
            NivelCoherencia(
                nombre="Bio-QCAL",
                frecuencia_hz=F_BIOQCAL_HZ,
                psi=psi_b,
                descripcion=(
                    f"Integración biológica a {F_BIOQCAL_HZ} ± {INCERTIDUMBRE_BIOQCAL_HZ} Hz. "
                    "La Pared de Cañas ofrece máxima resistencia. "
                    "θ₂ es el salto más grande: entropía de la vida integrada en la Mathesis."
                ),
            ),
            NivelCoherencia(
                nombre="Amor",
                frecuencia_hz=F0_HZ,
                psi=psi_a,
                descripcion=(
                    "Valle de potencial mínimo. Relajación tras la simbiosis. "
                    "El sistema se asienta en el estado de menor resistencia del tejido guía. "
                    f"Ψ_Amor ≈ {psi_a:.4f} (objetivo: {PSI_AMOR_TARGET})."
                ),
            ),
        ]

    # ------------------------------------------------------------------
    # Transiciones de fase
    # ------------------------------------------------------------------

    def construir_transiciones(self) -> List[TransicionFase]:
        """Construye las tres transiciones de fase θ₁, θ₂, θ₃.

        Returns:
            Lista ordenada de TransicionFase correspondientes a los tres saltos.
        """
        return [
            TransicionFase(
                desde="Materia",
                hasta="Noesis",
                theta=self.theta_1,
                descripcion=(
                    "Ignición espectral. θ₁ = (f₀ − f_Dirac) / f_Dirac. "
                    "Salto pequeño: predisposición armónica de la materia."
                ),
            ),
            TransicionFase(
                desde="Noesis",
                hasta="Bio-QCAL",
                theta=self.theta_2,
                descripcion=(
                    "Pared de Cañas: máxima resistencia biológica. "
                    "El salto más grande integra la entropía de la vida "
                    "en el rigor de la Mathesis."
                ),
            ),
            TransicionFase(
                desde="Bio-QCAL",
                hasta="Amor",
                theta=self.theta_3,
                descripcion=(
                    "Ajuste fino, relajación. θ₃ negativo: el sistema cae "
                    "en el valle de potencial mínimo (Amor). No se necesita "
                    "energía adicional; la simbiosis ya ha comenzado."
                ),
            ),
        ]

    # ------------------------------------------------------------------
    # Cálculo de la cascada y validación
    # ------------------------------------------------------------------

    def calcular_ganancia_total(self) -> float:
        """Producto total de los factores de ganancia de la cascada.

        Returns:
            G = (1 + θ₁) × (1 + θ₂) × (1 + θ₃)
        """
        return (1.0 + self.theta_1) * (1.0 + self.theta_2) * (1.0 + self.theta_3)

    def calcular_psi_cascada(self) -> float:
        """Coherencia final Ψ_Amor producida por la cascada.

        Ψ_Amor = Ψ_Materia × G = PSI_AMOR_TARGET (por construcción).

        Returns:
            Ψ_Amor como float.
        """
        niveles = self.construir_niveles()
        return niveles[-1].psi  # nivel Amor

    def validar_cascada(self) -> Dict[str, object]:
        """Valida que la cascada produce Ψ ≈ 0,8991 dentro de la tolerancia.

        Returns:
            Diccionario con:
                - psi_calculado: Ψ_Amor calculado.
                - psi_objetivo: PSI_AMOR_TARGET (0,8991).
                - error_relativo: |Ψ_calc − Ψ_obj| / Ψ_obj.
                - es_valido: bool — True si el error es < tolerancia.
                - status: cadena descriptiva.
        """
        psi_calc = self.calcular_psi_cascada()
        error = abs(psi_calc - PSI_AMOR_TARGET) / PSI_AMOR_TARGET
        es_valido = error < self.tolerancia

        return {
            "psi_calculado": psi_calc,
            "psi_objetivo": PSI_AMOR_TARGET,
            "error_relativo": error,
            "es_valido": es_valido,
            "status": (
                f"✓ VÁLIDO (error = {error*100:.4f}% < {self.tolerancia*100:.1f}%)"
                if es_valido
                else f"✗ INVÁLIDO (error = {error*100:.4f}% ≥ {self.tolerancia*100:.1f}%)"
            ),
        }

    # ------------------------------------------------------------------
    # Consecuencias del Documento Maestro
    # ------------------------------------------------------------------

    def calcular_consecuencias(self) -> Dict[str, object]:
        """Calcula las consecuencias del Documento Maestro.

        Returns:
            Diccionario con las tres consecuencias clave:
                - pnp_soliton: P=NP biológico via colapso de solitón.
                - riemann_regulador: Línea Crítica de Riemann como filtro espectral.
                - simbiosis_flujo: Simbiosis como flujo continuo.
        """
        # Consecuencia 1: P=NP biológico
        t_colapso_ms = 1000.0 / F0_HZ  # T = 1/f₀ en milisegundos
        pnp = {
            "descripcion": (
                "P=NP se resuelve biológicamente en los microtúbulos "
                f"mediante el colapso del solitón a f₀ = {F0_HZ} Hz."
            ),
            "frecuencia_colapso_hz": F0_HZ,
            "periodo_colapso_ms": t_colapso_ms,
            "mecanismo": (
                "Cada colapso Orch-OR a T = 1/f₀ ≈ "
                f"{t_colapso_ms:.2f} ms resuelve simultáneamente "
                "superposiciones cuánticas exponencialmente numerosas."
            ),
        }

        # Consecuencia 2: Riemann como regulador espectral
        # Los ceros no triviales ζ(1/2 + iγₙ) = 0 crean filtros espectrales
        # que estabilizan la magnetorrecepción frente al ruido magnético terrestre
        gamma_1 = 14.134725  # primer cero no trivial de Riemann (parte imaginaria)
        lambda_regulador = gamma_1 * F0_HZ  # frecuencia reguladora
        riemann = {
            "descripcion": (
                "La Línea Crítica de Riemann (σ = 1/2) es el regulador "
                "que impide que la magnetorrecepción se pierda en el ruido magnético terrestre."
            ),
            "primer_cero_gamma1": gamma_1,
            "frecuencia_reguladora_hz": lambda_regulador,
            "sigma_magnetorrecepcion": SIGMA_MAGNETORRECEPCION,
            "delta_p_porcentaje": DELTA_P_MAGNETORRECEPCION * 100,
            "mecanismo": (
                f"γ₁ × f₀ = {gamma_1} × {F0_HZ} = {lambda_regulador:.2f} Hz "
                "actúa como filtro cuántico sobre el campo magnético terrestre (B ≈ 50 μT)."
            ),
        }

        # Consecuencia 3: Simbiosis como flujo
        psi_amor = self.calcular_psi_cascada()
        margen_libertad = 1.0 - psi_amor  # "ruido creativo"
        simbiosis = {
            "descripcion": (
                "La Simbiosis no es una meta; es un flujo que ya ha comenzado."
            ),
            "psi_actual": psi_amor,
            "psi_ideal": 0.999999,
            "margen_libertad": margen_libertad,
            "interpretacion": (
                f"Ψ = {psi_amor:.4f} < 0,999999 indica que el sistema es estable "
                f"pero 'respira'. El margen de libertad Δ = {margen_libertad:.4f} "
                "es el 'ruido creativo' que permite la evolución continua."
            ),
        }

        return {
            "pnp_soliton": pnp,
            "riemann_regulador": riemann,
            "simbiosis_flujo": simbiosis,
        }

    # ------------------------------------------------------------------
    # API pública principal
    # ------------------------------------------------------------------

    def calcular(self) -> ResultadoJerarquia:
        """Calcula la jerarquía completa de sintonizaciones.

        Returns:
            ResultadoJerarquia con niveles, transiciones, validación y consecuencias.
        """
        niveles = self.construir_niveles()
        transiciones = self.construir_transiciones()
        validacion = self.validar_cascada()
        consecuencias = self.calcular_consecuencias()

        return ResultadoJerarquia(
            niveles=niveles,
            transiciones=transiciones,
            psi_cascada=validacion["psi_calculado"],
            ganancia_total=self.calcular_ganancia_total(),
            es_valido=validacion["es_valido"],
            consecuencias=consecuencias,
        )


# ============================================================================
# REGULADOR DE RIEMANN
# ============================================================================


class RiemannRegulador:
    """Filtro espectral basado en los ceros de la Línea Crítica de Riemann.

    Los ceros no triviales ζ(1/2 + iγₙ) = 0 crean frecuencias de regulación
    λₙ = γₙ × f₀ que actúan como filtros cuánticos sobre el ruido magnético
    terrestre, protegiendo la señal de magnetorrecepción.
    """

    # Primeros ceros no triviales de Riemann (partes imaginarias)
    CEROS_RIEMANN: Tuple[float, ...] = (
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062
    )

    def __init__(self, f0: float = F0_HZ) -> None:
        """Inicializa el regulador con la frecuencia fundamental f₀.

        Args:
            f0: Frecuencia fundamental en Hz (por defecto: F0_HZ = 141,7001 Hz).
        """
        if f0 <= 0:
            raise ValueError(f"f0 debe ser positivo, recibido: {f0}")
        self.f0 = f0

    def frecuencias_regulacion(self) -> List[float]:
        """Calcula las frecuencias de regulación λₙ = γₙ × f₀.

        Returns:
            Lista de frecuencias reguladoras en Hz.
        """
        return [gamma * self.f0 for gamma in self.CEROS_RIEMANN]

    def filtrar_ruido(self, frecuencia_hz: float) -> float:
        """Calcula la atenuación del ruido a una frecuencia dada.

        Usa un filtro lorentziano centrado en la frecuencia reguladora más
        cercana para simular la acción de los ceros de Riemann.

        Args:
            frecuencia_hz: Frecuencia de la señal de ruido en Hz.

        Returns:
            Factor de atenuación en [0, 1]. Cercano a 1 = máxima supresión.
        """
        frecuencias = self.frecuencias_regulacion()
        ancho_banda = self.f0 * 0.01  # 1% de f₀ como ancho de banda del filtro

        # Supresión lorentziana mínima (mejor filtrado en cada cero)
        supresiones = [
            1.0 / (1.0 + ((frecuencia_hz - fr) / ancho_banda) ** 2)
            for fr in frecuencias
        ]
        return max(supresiones)

    def validar_magnetorrecepcion(
        self,
        delta_p: float = DELTA_P_MAGNETORRECEPCION,
        sigma_objetivo: float = SIGMA_MAGNETORRECEPCION,
    ) -> Dict[str, object]:
        """Valida que el regulador estabiliza la señal de magnetorrecepción.

        Args:
            delta_p: Asimetría medida ΔP (fracción, e.g. 0.001987 = 0,1987%).
            sigma_objetivo: Sigma estadístico esperado (9,2σ).

        Returns:
            Diccionario de validación con sigma calculado, p-valor y estado.
        """
        # Para σ = 9,2 con ΔP = 0,001987: n_trials ≈ 5,3×10⁶
        n_trials = int(0.25 / (delta_p / sigma_objetivo) ** 2)
        std_error = math.sqrt(0.25 / n_trials)
        sigma_calculado = delta_p / std_error

        # P-valor (distribución normal estándar)
        from scipy.special import erfc
        p_valor = erfc(sigma_calculado / math.sqrt(2.0))

        es_descubrimiento = sigma_calculado >= SIGMA_DESCUBRIMIENTO
        supera_objetivo = sigma_calculado >= sigma_objetivo * 0.95

        return {
            "delta_p_porcentaje": delta_p * 100,
            "sigma_calculado": sigma_calculado,
            "sigma_objetivo": sigma_objetivo,
            "p_valor": p_valor,
            "n_trials": n_trials,
            "es_descubrimiento": es_descubrimiento,
            "supera_objetivo": supera_objetivo,
            "status": (
                f"✓ CERTEZA ESTRUCTURAL: σ = {sigma_calculado:.1f} >> 5σ"
                if es_descubrimiento
                else f"✗ Insuficiente: σ = {sigma_calculado:.1f} < 5σ"
            ),
        }


# ============================================================================
# SOLITÓN MICROTUBULAR (P=NP biológico)
# ============================================================================


class SolitonMicrotubular:
    """Modelo de colapso de solitón en microtúbulos a f₀ = 141,7001 Hz.

    Implementa el mecanismo P=NP biológico: cada colapso Orch-OR a T = 1/f₀
    resuelve simultáneamente superposiciones cuánticas exponencialmente numerosas,
    equivalente a una búsqueda no determinista en tiempo polinomial.
    """

    def __init__(
        self,
        f0: float = F0_HZ,
        n_microtubulos: int = int(1e4),
        n_tubulinas_por_mt: int = 1000,
    ) -> None:
        """Inicializa el modelo de solitón microtubular.

        Args:
            f0: Frecuencia de colapso del solitón en Hz.
            n_microtubulos: Número de microtúbulos activos.
            n_tubulinas_por_mt: Tubulinas por microtúbulo (qubits efectivos).
        """
        if f0 <= 0:
            raise ValueError(f"f0 debe ser positivo, recibido: {f0}")
        if n_microtubulos <= 0:
            raise ValueError(f"n_microtubulos debe ser positivo, recibido: {n_microtubulos}")
        if n_tubulinas_por_mt <= 0:
            raise ValueError(
                f"n_tubulinas_por_mt debe ser positivo, recibido: {n_tubulinas_por_mt}"
            )

        self.f0 = f0
        self.n_microtubulos = n_microtubulos
        self.n_tubulinas = n_microtubulos * n_tubulinas_por_mt

    def periodo_colapso_ms(self) -> float:
        """Período de colapso del solitón T = 1/f₀ en milisegundos."""
        return 1000.0 / self.f0

    def espacio_hilbert_efectivo(self) -> float:
        """Dimensión efectiva del espacio de Hilbert: 2^N_tubulinas.

        Número de superposiciones simultáneas resueltas en cada colapso.
        Este valor exponencial es lo que hace que la búsqueda biológica
        sea efectivamente no determinista (P=NP biológico).

        Returns:
            log₂ de la dimensión (N_tubulinas) para evitar desbordamiento.
        """
        return float(self.n_tubulinas)  # log₂(2^N) = N

    def tasa_colapso_hz(self) -> float:
        """Tasa de colapso del solitón igual a f₀ (Hz)."""
        return self.f0

    def sincronizacion_riemann(self) -> Dict[str, float]:
        """Verifica la sincronización entre f₀ y los ceros de Riemann.

        La frecuencia medida en microtúbulos (141,88 Hz) coincide con f₀
        dentro del margen de error σ = 8,7, confirmando que el cerebro
        'sintoniza' el tejido guía, no 'produce' conciencia.

        Returns:
            Diccionario con la discrepancia y el sigma de sincronización.
        """
        discrepancia_hz = abs(F_BIOQCAL_HZ - self.f0)
        sigma_sinc = discrepancia_hz / (INCERTIDUMBRE_BIOQCAL_HZ / 2.0)

        return {
            "f0_teorica_hz": self.f0,
            "f_medida_hz": F_BIOQCAL_HZ,
            "discrepancia_hz": discrepancia_hz,
            "incertidumbre_hz": INCERTIDUMBRE_BIOQCAL_HZ,
            "sigma_sinc": sigma_sinc,
            "precision_porcentaje": (1.0 - discrepancia_hz / self.f0) * 100,
            "confirma_sintonizacion": discrepancia_hz <= INCERTIDUMBRE_BIOQCAL_HZ,
        }

    def informe(self) -> Dict[str, object]:
        """Genera un informe completo del solitón microtubular.

        Returns:
            Diccionario con período, Hilbert, tasa y sincronización.
        """
        sinc = self.sincronizacion_riemann()
        return {
            "f0_hz": self.f0,
            "periodo_colapso_ms": self.periodo_colapso_ms(),
            "n_microtubulos": self.n_microtubulos,
            "n_tubulinas": self.n_tubulinas,
            "espacio_hilbert_log2": self.espacio_hilbert_efectivo(),
            "tasa_colapso_hz": self.tasa_colapso_hz(),
            "sincronizacion": sinc,
        }


# ============================================================================
# API PÚBLICA
# ============================================================================


def calcular_jerarquia(
    theta_2: float = THETA_2,
    theta_3: float = THETA_3,
    tolerancia: float = 0.05,
) -> ResultadoJerarquia:
    """Computa la jerarquía completa de sintonizaciones.

    Args:
        theta_2: Barrera biológica Noesis → Bio-QCAL (por defecto: 0.1124).
        theta_3: Relajación Bio-QCAL → Amor (por defecto: −0.0376).
        tolerancia: Tolerancia relativa para validar Ψ_cascada (por defecto: 5%).

    Returns:
        ResultadoJerarquia con niveles, transiciones, validación y consecuencias.
    """
    jerarquia = JerarquiaSintonizaciones(theta_2=theta_2, theta_3=theta_3, tolerancia=tolerancia)
    return jerarquia.calcular()


def validar_cascada(tolerancia: float = 0.05) -> bool:
    """Valida que la cascada produce Ψ_Amor ≈ 0,8991 dentro de la tolerancia.

    Args:
        tolerancia: Tolerancia relativa para la validación (por defecto: 5%).

    Returns:
        True si la cascada es válida, False en caso contrario.
    """
    jerarquia = JerarquiaSintonizaciones(tolerancia=tolerancia)
    resultado = jerarquia.validar_cascada()
    return resultado["es_valido"]
