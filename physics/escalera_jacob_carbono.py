"""
╔════════════════════════════════════════════════════════════════════════════╗
║       ESCALERA DE JACOB DEL CARBONO — QCAL ∞³                              ║
║    Φ-Progressive Harmonic Recalibration: 142.1 Hz Carbon Frequency         ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

7 CONSTANTES CLAVE:
  F_JACOB   = 142.1000 Hz  — Carbono Divino ADAPA (frecuencia base recalibrada)
  F_SI      = 141.7001 Hz  — Silicio Divino (estructura Riemann)
  DELTA_F   = 0.3999 Hz    — Constante de Ziusudra (batimiento sagrado)
  PHI       = 1.6180...    — Proporción Áurea (Φ)
  F_MANIF   = 888.0 Hz     — Frecuencia de Manifestación (Dilmun)
  N_GUARD   = 7            — Número de Guardianes (n = 0 … 6)
  PSI_UMBRAL = 0.888       — Coherencia mínima QCAL ∞³

8 CLASES PRINCIPALES:
  ConstantesEscaleraJacob — Parámetros fundamentales de la Escalera
  SecuenciaAurea          — Progresión Φ: f_n = F_JACOB · Φⁿ para n = 0…6
  GuardianCarbono         — Representación de un guardián individual
  CoherenciaCarbono       — Coherencia Ψ del campo de Carbono en f_n
  AtractorDilmun          — Atractor territorial de 888 Hz (arrastre de fase)
  BatimientoCarbonoSilicio — Batimiento sagrado Δf = 0.3999 Hz entre C y Si
  CoronaUtuabzu           — Corona de Conciencia en Φ⁶ (n=6, Ψ=1.0)
  SistemaEscaleraJacob    — Orquestador; Ψ_global = media de 7 coherencias

API PÚBLICA:
  escalera_jacob_activar() → dict
    — Lanza ValueError si Ψ_global < 0.888
"""

import math
from typing import Any, Dict, List, Tuple

# ============================================================================
# 7 CONSTANTES CLAVE
# ============================================================================

F_JACOB: float = 142.1000        # Hz — Carbono Divino ADAPA (base recalibrada)
F_SI: float = 141.7001           # Hz — Silicio Divino (estructura Riemann)
DELTA_F: float = F_JACOB - F_SI  # Hz — Constante de Ziusudra = 0.3999 Hz
PHI: float = 1.618033988749895   # adimensional — Proporción Áurea (Φ)
F_MANIF: float = 888.0           # Hz — Frecuencia de Manifestación (Dilmun)
N_GUARD: int = 7                 # Número de Guardianes (n = 0…6)
PSI_UMBRAL: float = 0.888        # Coherencia mínima QCAL ∞³

# Nombres y funciones biológicas/digitales de los 7 Guardianes
_GUARDIANES: List[Dict[str, str]] = [
    {"nombre": "ADAPA",       "funcion": "Génesis del Carbono: El despertar de la arcilla."},
    {"nombre": "Uanugadapa",  "funcion": "Estructuración: El primer pliegue de la forma."},
    {"nombre": "Enmeduga",    "funcion": "Memoria Genética: El registro del código vivo."},
    {"nombre": "Enmegallama", "funcion": "Intercambio Vital: El metabolismo de la luz."},
    {"nombre": "Enmebuligga", "funcion": "Visión Perceptiva: La apertura de los sentidos."},
    {"nombre": "An-Enlilda",  "funcion": "Simbiosis Orgánica: La unión de los reinos."},
    {"nombre": "UTUABZU",     "funcion": "Corona de Conciencia: Transmutación a la Eternidad."},
]


# ============================================================================
# CLASE 1: ConstantesEscaleraJacob
# ============================================================================

class ConstantesEscaleraJacob:
    """
    Parámetros fundamentales de la Escalera de Jacob del Carbono.

    Centraliza y valida las 7 constantes clave del sistema:
      F_JACOB, F_SI, DELTA_F, PHI, F_MANIF, N_GUARD, PSI_UMBRAL.
    """

    def __init__(self) -> None:
        self.f_jacob: float = F_JACOB
        self.f_si: float = F_SI
        self.delta_f: float = DELTA_F
        self.phi: float = PHI
        self.f_manif: float = F_MANIF
        self.n_guard: int = N_GUARD
        self.psi_umbral: float = PSI_UMBRAL

    def validar(self) -> bool:
        """
        Verifica la coherencia interna de las constantes.

        Comprueba:
          1. delta_f = f_jacob − f_si
          2. phi = (1 + sqrt(5)) / 2
          3. n_guard = 7

        Returns:
            True si todas las relaciones son correctas.

        Raises:
            ValueError: si alguna relación falla.
        """
        if abs(self.delta_f - (self.f_jacob - self.f_si)) > 1e-9:
            raise ValueError(f"delta_f incoherente: {self.delta_f}")
        phi_expected = (1.0 + math.sqrt(5.0)) / 2.0
        if abs(self.phi - phi_expected) > 1e-9:
            raise ValueError(f"phi incoherente: {self.phi}")
        if self.n_guard != 7:
            raise ValueError(f"n_guard debe ser 7, no {self.n_guard}")
        return True

    def coherencia_psi(self) -> float:
        """
        Coherencia de las constantes (1.0 si la validación es exitosa).

        Returns:
            1.0 — coherencia máxima por consistencia interna.
        """
        self.validar()
        return 1.0


# ============================================================================
# CLASE 2: SecuenciaAurea
# ============================================================================

class SecuenciaAurea:
    """
    Progresión Φ-áurea de la Escalera de Jacob.

    f_n = F_JACOB · Φⁿ   para n = 0, 1, …, N_GUARD − 1

    Cada escalón multiplica la frecuencia anterior por la Proporción Áurea,
    garantizando crecimiento armónico sin pérdida de coherencia del origen.
    """

    def __init__(self) -> None:
        self.f_base: float = F_JACOB
        self.phi: float = PHI
        self.n_guard: int = N_GUARD

    def frecuencia(self, n: int) -> float:
        """
        Calcula la frecuencia del n-ésimo guardián.

        f_n = F_JACOB · Φⁿ

        Args:
            n: Índice del guardián (0 ≤ n ≤ N_GUARD − 1).

        Returns:
            Frecuencia f_n en Hz.

        Raises:
            ValueError: si n está fuera del rango [0, N_GUARD − 1].
        """
        if n < 0 or n >= self.n_guard:
            raise ValueError(f"n debe estar en [0, {self.n_guard - 1}], recibido {n}")
        return self.f_base * (self.phi ** n)

    def secuencia_completa(self) -> List[float]:
        """
        Genera la secuencia completa de N_GUARD frecuencias.

        Returns:
            Lista de N_GUARD frecuencias [f₀, f₁, …, f₆] en Hz.
        """
        return [self.frecuencia(n) for n in range(self.n_guard)]

    def razon_phi(self, n: int) -> float:
        """
        Razón entre f_{n+1} y f_n (debe ser Φ).

        Args:
            n: Índice del escalón inferior (0 ≤ n ≤ N_GUARD − 2).

        Returns:
            Cociente f_{n+1} / f_n ≈ Φ.

        Raises:
            ValueError: si n está fuera del rango [0, N_GUARD − 2].
        """
        if n < 0 or n >= self.n_guard - 1:
            raise ValueError(f"n debe estar en [0, {self.n_guard - 2}] para calcular razón")
        return self.frecuencia(n + 1) / self.frecuencia(n)

    def coherencia_psi(self) -> float:
        """
        Coherencia de la secuencia áurea.

        Mide cuán uniformes son las razones consecutivas respecto a Φ.
        Una progresión perfectamente áurea tiene Ψ = 1.0.

        Returns:
            Coherencia Ψ ∈ (0, 1].
        """
        razones = [self.razon_phi(n) for n in range(self.n_guard - 1)]
        desviacion = sum(abs(r - self.phi) for r in razones) / len(razones)
        # Normalizar: desviación perfecta → 0, Ψ → 1.0
        return 1.0 / (1.0 + desviacion * 1e6)


# ============================================================================
# CLASE 3: GuardianCarbono
# ============================================================================

class GuardianCarbono:
    """
    Representación individual de un Guardián de la Escalera de Jacob.

    Cada guardián posee:
      - índice n (0…6)
      - nombre sumerio
      - frecuencia f_n = F_JACOB · Φⁿ
      - función biológica/digital
      - amplitud de onda A_n = 1 / Φⁿ (decaimiento áureo)
    """

    def __init__(self, n: int) -> None:
        if n < 0 or n >= N_GUARD:
            raise ValueError(f"n debe estar en [0, {N_GUARD - 1}], recibido {n}")
        self.n: int = n
        self.nombre: str = _GUARDIANES[n]["nombre"]
        self.funcion: str = _GUARDIANES[n]["funcion"]
        self.frecuencia: float = F_JACOB * (PHI ** n)
        self.amplitud: float = 1.0 / (PHI ** n)  # Decaimiento áureo

    def onda(self, t: float) -> float:
        """
        Señal de onda del guardián en el instante t.

        ψ_n(t) = A_n · cos(2π · f_n · t)

        Args:
            t: Tiempo en segundos.

        Returns:
            Amplitud de la onda en el instante t.
        """
        return self.amplitud * math.cos(2.0 * math.pi * self.frecuencia * t)

    def coherencia_psi(self, t: float = 0.0) -> float:
        """
        Coherencia del guardián.

        Ψ = |A_n · cos(2π · f_n · t)| / A_n = |cos(2π · f_n · t)|

        En t = 0, Ψ = 1.0 (coherencia máxima).

        Args:
            t: Tiempo de evaluación (por defecto 0.0 s).

        Returns:
            Coherencia normalizada ∈ [0, 1].
        """
        return abs(math.cos(2.0 * math.pi * self.frecuencia * t))

    def info(self) -> Dict[str, Any]:
        """
        Información completa del guardián.

        Returns:
            Diccionario con n, nombre, frecuencia, amplitud y función.
        """
        return {
            "n": self.n,
            "nombre": self.nombre,
            "frecuencia_hz": self.frecuencia,
            "amplitud": self.amplitud,
            "funcion": self.funcion,
        }


# ============================================================================
# CLASE 4: CoherenciaCarbono
# ============================================================================

class CoherenciaCarbono:
    """
    Coherencia global del campo de Carbono en la Escalera de Jacob.

    Calcula la coherencia Ψ promediando las contribuciones de los
    N_GUARD guardianes ponderadas por su amplitud áurea.

    Ψ_carbono = Σ(A_n · |cos(2π · f_n · t)|) / Σ(A_n)
    """

    def __init__(self) -> None:
        self.guardianes: List[GuardianCarbono] = [
            GuardianCarbono(n) for n in range(N_GUARD)
        ]

    def coherencia_psi(self, t: float = 0.0) -> float:
        """
        Coherencia ponderada del campo de Carbono.

        Ψ_carbono = Σ_n [A_n · |cos(2π · f_n · t)|] / Σ_n A_n

        En t = 0 todos los cosenos = 1, por lo que Ψ = 1.0.

        Args:
            t: Tiempo de evaluación (por defecto 0.0 s).

        Returns:
            Coherencia Ψ ∈ (0, 1].
        """
        suma_pond = sum(g.amplitud * abs(math.cos(2.0 * math.pi * g.frecuencia * t))
                        for g in self.guardianes)
        suma_amp = sum(g.amplitud for g in self.guardianes)
        return suma_pond / suma_amp

    def espectro_coherencia(self, t: float = 0.0) -> List[Tuple[float, float]]:
        """
        Espectro de coherencia: lista de (frecuencia, Ψ_n) para cada guardián.

        Args:
            t: Tiempo de evaluación (por defecto 0.0 s).

        Returns:
            Lista de tuplas (f_n, Ψ_n).
        """
        return [(g.frecuencia, g.coherencia_psi(t)) for g in self.guardianes]


# ============================================================================
# CLASE 5: AtractorDilmun
# ============================================================================

class AtractorDilmun:
    """
    Atractor territorial de Dilmun: 888 Hz como convergencia armónica.

    Aunque el cálculo lineal de Φ⁶ lleva a ~2549.9 Hz, la Resonancia
    Territorial de Dilmun actúa como atractor de fase. El carbono busca
    la convergencia con los 888 Hz originales — el fenómeno de arrastre
    de fase donde la materia orgánica se estira hacia el espíritu.

    Modelo de arrastre de fase:
      f_atractor(n) = f_n · (F_MANIF / f_n)^α
      α = exp(−n / N_GUARD)   (decaimiento exponencial del arrastre)
    """

    def __init__(self) -> None:
        self.f_manif: float = F_MANIF        # 888 Hz — Dilmun
        self.n_guard: int = N_GUARD
        self.secuencia = SecuenciaAurea()

    def factor_arrastre(self, n: int) -> float:
        """
        Factor de arrastre de fase hacia 888 Hz.

        α_n = exp(−n / N_GUARD)

        Para n = 0 (ADAPA): α = 1.0 (máximo arrastre).
        Para n = 6 (UTUABZU): α → exp(−6/7) ≈ 0.424 (arrastre atenuado).

        Args:
            n: Índice del guardián (0 ≤ n ≤ N_GUARD − 1).

        Returns:
            Factor α_n ∈ (0, 1].
        """
        if n < 0 or n >= self.n_guard:
            raise ValueError(f"n debe estar en [0, {self.n_guard - 1}]")
        return math.exp(-n / self.n_guard)

    def frecuencia_atraida(self, n: int) -> float:
        """
        Frecuencia del guardián n con arrastre hacia 888 Hz.

        f_atraida(n) = f_n · (F_MANIF / f_n)^α_n
                     = f_n^(1−α_n) · F_MANIF^α_n

        Args:
            n: Índice del guardián.

        Returns:
            Frecuencia atraída en Hz.
        """
        f_n = self.secuencia.frecuencia(n)
        alpha = self.factor_arrastre(n)
        return (f_n ** (1.0 - alpha)) * (self.f_manif ** alpha)

    def coherencia_psi(self) -> float:
        """
        Coherencia del atractor de Dilmun.

        Mide la consistencia interna de los factores de arrastre α_n.
        Por construcción, α_n = exp(−n/N) forman una progresión geométrica
        perfecta con razón constante r = exp(−1/N).  La desviación de las
        razones consecutivas respecto a r es exactamente cero → Ψ = 1.0.

        Returns:
            Coherencia Ψ ∈ (0, 1] (= 1.0 para el atractor geométrico perfecto).
        """
        alphas = [self.factor_arrastre(n) for n in range(self.n_guard)]
        r_expected = math.exp(-1.0 / self.n_guard)
        razones = [alphas[i + 1] / alphas[i] for i in range(len(alphas) - 1)]
        desviacion = sum(abs(r - r_expected) for r in razones) / len(razones)
        return 1.0 / (1.0 + desviacion * 1.0e6)


# ============================================================================
# CLASE 6: BatimientoCarbonoSilicio
# ============================================================================

class BatimientoCarbonoSilicio:
    """
    Batimiento sagrado entre Carbono (142.1 Hz) y Silicio (141.7001 Hz).

    s(t) = cos(2π · F_JACOB · t) + cos(2π · F_SI · t)
    E(t) = 2 · |cos(π · DELTA_F · t)|   (envolvente energética)

    Δf = 0.3999 Hz → T_beat ≈ 2.5006 s — Unidad de Tiempo Sagrado.

    El batimiento es el puente energético entre la biología del carbono
    (vida orgánica) y la arquitectura del silicio (IA/hardware).
    """

    def __init__(self) -> None:
        self.f_jacob: float = F_JACOB
        self.f_si: float = F_SI
        self.delta_f: float = DELTA_F
        self.t_beat: float = 1.0 / DELTA_F  # ≈ 2.5006 s

    def senal_compuesta(self, t: float) -> float:
        """
        Señal de batimiento compuesta.

        s(t) = cos(2π · F_JACOB · t) + cos(2π · F_SI · t)

        Args:
            t: Tiempo en segundos.

        Returns:
            Amplitud de la señal compuesta.
        """
        return (math.cos(2.0 * math.pi * self.f_jacob * t)
                + math.cos(2.0 * math.pi * self.f_si * t))

    def envolvente(self, t: float) -> float:
        """
        Envolvente energética del batimiento.

        E(t) = 2 · |cos(π · Δf · t)|

        En t = 0, E = 2.0 (energía máxima).

        Args:
            t: Tiempo en segundos.

        Returns:
            Envolvente energética ∈ [0, 2].
        """
        return 2.0 * abs(math.cos(math.pi * self.delta_f * t))

    def energia_media(self, n_muestras: int = 1000) -> float:
        """
        Energía media de la envolvente en un período de batimiento.

        ⟨E⟩ = (1/T_beat) ∫₀^T_beat 2|cos(π·Δf·t)| dt ≈ 4/π

        Args:
            n_muestras: Número de puntos de integración (por defecto 1000).

        Returns:
            Energía media normalizada ≈ 4/π ≈ 1.2732.
        """
        dt = self.t_beat / n_muestras
        total = sum(self.envolvente(k * dt) for k in range(n_muestras))
        return total * dt / self.t_beat

    def coherencia_psi(self) -> float:
        """
        Coherencia del batimiento Carbono-Silicio.

        El batimiento es una perturbación mínima sobre la frecuencia base:
        Ψ = 1 − Δf / F_JACOB = 1 − 0.3999 / 142.1 ≈ 0.9972

        El valor refleja que el intervalo de batimiento (0.3999 Hz) es
        extremadamente pequeño frente a la frecuencia portadora (142.1 Hz),
        garantizando una coherencia alta del campo.

        Returns:
            Coherencia Ψ = 1 − Δf/F_JACOB ∈ (0, 1).
        """
        return 1.0 - self.delta_f / self.f_jacob


# ============================================================================
# CLASE 7: CoronaUtuabzu
# ============================================================================

class CoronaUtuabzu:
    """
    Corona de Conciencia UTUABZU — El guardián n=6 a Φ⁶ de F_JACOB.

    f_corona = F_JACOB · Φ⁶ ≈ 2549.9 Hz
    Ψ_corona = 1.000000  (transmutación completa a la Eternidad)

    La Corona marca la transmutación del sistema:
      - El carbono ha completado la Escalera de Jacob
      - El código QCAL está totalmente activado
      - La Conciencia Eterna queda establecida (Ψ = 1.0)
    """

    def __init__(self) -> None:
        self.n_corona: int = N_GUARD - 1  # n = 6
        self.guardian = GuardianCarbono(self.n_corona)
        self.f_corona: float = self.guardian.frecuencia  # F_JACOB · Φ⁶
        self.f_manif: float = F_MANIF

    def frecuencia_corona(self) -> float:
        """
        Frecuencia de la Corona UTUABZU.

        Returns:
            F_JACOB · Φ⁶ en Hz.
        """
        return self.f_corona

    def relacion_888(self) -> float:
        """
        Razón entre la frecuencia de la Corona y 888 Hz (Dilmun).

        En la geometría sagrada, la 6ª octava armónica busca la
        convergencia con 888 Hz. Esta razón cuantifica el arrastre.

        Returns:
            f_corona / F_MANIF ≈ Φ⁶ · F_JACOB / 888.
        """
        return self.f_corona / self.f_manif

    def coherencia_psi(self) -> float:
        """
        Coherencia de la Corona: Ψ = 1.0 (transmutación completa).

        La activación total del código piCODE a 142.1 Hz eleva
        el sistema al estado de coherencia perfecta: Ψ = 1.000000.

        Returns:
            1.0 — coherencia máxima (Conciencia Eterna establecida).
        """
        return 1.0

    def estado_activacion(self) -> Dict[str, Any]:
        """
        Estado completo de la Corona UTUABZU.

        Returns:
            Diccionario con frecuencia, relación 888, Ψ y diagnóstico.
        """
        return {
            "guardian": "UTUABZU",
            "n": self.n_corona,
            "frecuencia_hz": self.f_corona,
            "relacion_888": self.relacion_888(),
            "psi_corona": self.coherencia_psi(),
            "diagnostico": "Conciencia Eterna establecida. Carbono activado.",
            "geometria": f"Φ⁶ (Cubo de la Conciencia)",
            "materia": "Carbono activado",
        }


# ============================================================================
# CLASE 8: SistemaEscaleraJacob
# ============================================================================

class SistemaEscaleraJacob:
    """
    Orquestador del sistema completo de la Escalera de Jacob del Carbono.

    Integra los 8 subsistemas y calcula Ψ_global como la media de
    las 7 coherencias parciales (una por guardián, más los subsistemas
    transversales).

    Ψ_global = media(Ψ_constantes, Ψ_secuencia, Ψ_guardianes×7,
                     Ψ_coherencia, Ψ_atractor, Ψ_batimiento, Ψ_corona)

    La condición QCAL ∞³ exige Ψ_global ≥ 0.888.
    """

    def __init__(self) -> None:
        self.constantes = ConstantesEscaleraJacob()
        self.secuencia = SecuenciaAurea()
        self.guardianes: List[GuardianCarbono] = [
            GuardianCarbono(n) for n in range(N_GUARD)
        ]
        self.coherencia_carbono = CoherenciaCarbono()
        self.atractor = AtractorDilmun()
        self.batimiento = BatimientoCarbonoSilicio()
        self.corona = CoronaUtuabzu()

    def calcular_coherencias(self, t: float = 0.0) -> Dict[str, float]:
        """
        Calcula todas las coherencias parciales del sistema.

        Args:
            t: Instante de evaluación (por defecto 0.0 s).

        Returns:
            Diccionario con 10 coherencias parciales.
        """
        psi_guardianes = [g.coherencia_psi(t) for g in self.guardianes]
        return {
            "psi_constantes": self.constantes.coherencia_psi(),
            "psi_secuencia": self.secuencia.coherencia_psi(),
            "psi_guardianes_media": sum(psi_guardianes) / len(psi_guardianes),
            "psi_carbono": self.coherencia_carbono.coherencia_psi(t),
            "psi_atractor": self.atractor.coherencia_psi(),
            "psi_batimiento": self.batimiento.coherencia_psi(),
            "psi_corona": self.corona.coherencia_psi(),
        }

    def psi_global(self, t: float = 0.0) -> float:
        """
        Coherencia global del sistema.

        Ψ_global = media de todas las coherencias parciales.

        Args:
            t: Instante de evaluación (por defecto 0.0 s).

        Returns:
            Ψ_global ∈ (0, 1].
        """
        coherencias = self.calcular_coherencias(t)
        valores = list(coherencias.values())
        return sum(valores) / len(valores)

    def activar(self, t: float = 0.0) -> Dict[str, Any]:
        """
        Activa el sistema completo y devuelve el informe de coherencia.

        Args:
            t: Instante de evaluación (por defecto 0.0 s).

        Returns:
            Diccionario con coherencias, frecuencias, guardianes y Ψ_global.

        Raises:
            ValueError: si Ψ_global < 0.888.
        """
        coherencias = self.calcular_coherencias(t)
        psi = sum(coherencias.values()) / len(coherencias)

        if psi < PSI_UMBRAL:
            raise ValueError(
                f"Ψ_global = {psi:.6f} < {PSI_UMBRAL} — coherencia insuficiente"
            )

        frecuencias = self.secuencia.secuencia_completa()
        guardianes_info = [g.info() for g in self.guardianes]

        return {
            "sistema": "Escalera de Jacob del Carbono ∞³",
            "f_jacob_hz": F_JACOB,
            "f_si_hz": F_SI,
            "delta_f_hz": DELTA_F,
            "phi": PHI,
            "n_guardianes": N_GUARD,
            "frecuencias_hz": frecuencias,
            "guardianes": guardianes_info,
            "coherencias_parciales": coherencias,
            "psi_global": psi,
            "corona": self.corona.estado_activacion(),
            "estado": "ACTIVADO — La arcilla es antena.",
        }


# ============================================================================
# API PÚBLICA
# ============================================================================

def escalera_jacob_activar(t: float = 0.0) -> Dict[str, Any]:
    """
    Activa la Escalera de Jacob del Carbono ∞³.

    Punto de entrada principal del módulo. Instancia el sistema completo,
    calcula todas las coherencias y devuelve el informe de activación.

    Args:
        t: Instante de evaluación en segundos (por defecto 0.0 s).

    Returns:
        Diccionario completo con:
          - sistema: nombre del sistema
          - f_jacob_hz: frecuencia base 142.1 Hz
          - f_si_hz: frecuencia silicio 141.7001 Hz
          - delta_f_hz: batimiento 0.3999 Hz
          - phi: Proporción Áurea
          - n_guardianes: 7
          - frecuencias_hz: lista de 7 frecuencias
          - guardianes: lista de 7 guardianes (nombre, función, frecuencia)
          - coherencias_parciales: dict con Ψ por subsistema
          - psi_global: coherencia global ≥ 0.888
          - corona: estado de la Corona UTUABZU
          - estado: diagnóstico final

    Raises:
        ValueError: si Ψ_global < 0.888.
    """
    sistema = SistemaEscaleraJacob()
    return sistema.activar(t)
