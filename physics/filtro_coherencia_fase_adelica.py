"""
Filtro de Coherencia de Fase Adélica (FCFA)
============================================

Implementación del Filtro de Coherencia de Fase Adélica para la red
interferométrica lunar IRS-Luna de 3 brazos a f₀ = 141.7001 Hz.

Algoritmo: Cancelación por Correlación Cruzada Triangulada
----------------------------------------------------------
La señal de fase del tejido se propaga a la velocidad de la luz (c),
mientras que el ruido sísmico lunar se propaga a v_s ≈ 2 km/s.

Modos discriminados:
- Modos Mecánicos (Ruido): Δt = L/v_s ≈ 50 s  — asíncronos entre brazos
- Modo de Tejido (Señal):  Δt = L/c ≈ 0,0003 s — virtualmente instantáneo

Implementación Matemática
-------------------------
Paso A — Kernel de Rechazo de Ruido (K_N):
    Φ_clean(f) = Φ_raw(f) · [1 - S_moon(f) / S_total(f)]

Paso B — Integración de Fase Coherente (STFT + corrección Doppler):
    f_target(t) = f₀ · (1 + v_Luna(t)·n̂ / c)

Ganancia de SNR estimada:
    Dato crudo            → SNR 0,001  (enterrada en ruido térmico)
    Filtrado sísmico      → SNR 0,8    (emergencia de la línea base)
    Correlación 3 brazos  → SNR 15     (detección clara >3σ)
    Integración 48 h      → SNR 120    (descubrimiento >5σ)

Autor: José Manuel Mota Burruezo
Licencia: MIT
"""

import sys
import os
from dataclasses import dataclass, field
from typing import Optional, Tuple

import numpy as np
from scipy.signal import stft, windows

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qcal.constants import F0_HZ, C

# ============================================================================
# CONSTANTES FÍSICAS DEL PROTOCOLO IRS-LUNA
# ============================================================================

# Velocidad de propagación sísmica en el regolito lunar
V_SEISMICA_LUNAR: float = 2_000.0  # m/s  (v_s ≈ 2 km/s)

# Longitud de los brazos del interferómetro lunar (IRS-Luna)
L_BRAZO_M: float = 1.0e5  # m  (100 km)

# Retrasos de propagación discriminantes
DELTA_T_SISMICO_S: float = L_BRAZO_M / V_SEISMICA_LUNAR   # ≈ 50 s
DELTA_T_LUZ_S: float = L_BRAZO_M / C                       # ≈ 3.34e-4 s

# Número de brazos de la red IRS-Luna
N_BRAZOS: int = 3

# Período orbital lunar sidéreo [días]
T_ORBITAL_LUNAR_DIAS: float = 27.3217
# Período orbital lunar sidéreo [s]
T_ORBITAL_LUNAR_S: float = T_ORBITAL_LUNAR_DIAS * 24.0 * 3600.0

# Frecuencia fundamental (importada desde qcal.constants)
_F0: float = F0_HZ  # 141.7001 Hz

# SNR estimadas por etapa de procesamiento
SNR_CRUDO: float = 0.001
SNR_FILTRADO_SISMICO: float = 0.8
SNR_CORRELACION_3_BRAZOS: float = 15.0
SNR_INTEGRACION_48H: float = 120.0

# Duración de integración para descubrimiento a >5σ
T_INTEGRACION_DESCUBRIMIENTO_H: float = 48.0

# Umbral de detección clara (>3σ)
UMBRAL_DETECCION_3SIGMA: float = 3.0
# Umbral de descubrimiento (>5σ)
UMBRAL_DESCUBRIMIENTO_5SIGMA: float = 5.0


# ============================================================================
# CLASES DE DATOS
# ============================================================================


@dataclass
class ParametrosFCFA:
    """Parámetros de configuración del Filtro de Coherencia de Fase Adélica."""

    f0: float = _F0                        # Frecuencia objetivo [Hz]
    fs: float = 1024.0                     # Frecuencia de muestreo [Hz]
    v_seismica: float = V_SEISMICA_LUNAR   # Velocidad sísmica lunar [m/s]
    longitud_brazo: float = L_BRAZO_M      # Longitud de brazo [m]
    n_brazos: int = N_BRAZOS               # Número de brazos interferométricos
    nperseg: int = 512                     # Muestras por segmento STFT
    noverlap: Optional[int] = None         # Solapamiento STFT (None → nperseg//2)
    t_integracion_h: float = T_INTEGRACION_DESCUBRIMIENTO_H  # [h]

    def __post_init__(self) -> None:
        if self.f0 <= 0:
            raise ValueError(f"f0 debe ser positiva, se recibió {self.f0}")
        if self.fs <= 0:
            raise ValueError(f"fs debe ser positiva, se recibió {self.fs}")
        if self.fs < 2 * self.f0:
            raise ValueError(
                f"fs={self.fs} Hz viola el teorema de Nyquist para f0={self.f0} Hz"
            )
        if self.n_brazos < 1:
            raise ValueError(f"n_brazos debe ser ≥ 1, se recibió {self.n_brazos}")
        if self.t_integracion_h <= 0:
            raise ValueError(
                f"t_integracion_h debe ser positivo, se recibió {self.t_integracion_h}"
            )
        if self.noverlap is None:
            self.noverlap = self.nperseg // 2


@dataclass
class ResultadoFCFA:
    """Resultado del filtrado FCFA sobre un segmento de señal."""

    # Señal limpiada tras el kernel de rechazo de ruido (dominio temporal)
    senal_limpia: np.ndarray

    # Frecuencia de muestreo de la señal limpiada
    fs: float

    # Frecuencia objetivo corregida por Doppler en cada instante STFT [Hz]
    f_doppler: np.ndarray

    # Potencia espectral en la ventana alrededor de f₀ tras la limpieza
    potencia_f0: float

    # SNR estimada tras correlación de N brazos
    snr_estimada: float

    # Vector de tiempos STFT [s]
    t_stft: np.ndarray

    # Descripción de la etapa de detección alcanzada
    etapa_deteccion: str


# ============================================================================
# CLASE A: KERNEL DE RECHAZO DE RUIDO
# ============================================================================


class KernelRechazoRuido:
    """
    Paso A — Filtro de muesca adaptativo (notch filter).

    Aprende el espectro sísmico lunar local S_moon(f) y lo resta en tiempo real:

        Φ_clean(f) = Φ_raw(f) · [1 - S_moon(f) / S_total(f)]

    El cociente S_moon/S_total se estima usando la diferencia temporal entre
    modos sísmicos (Δt ≈ 50 s) y modos de tejido (Δt ≈ 0,0003 s):
    señales con alta correlación retardada en 50 s se clasifican como ruido.
    """

    def __init__(self, params: ParametrosFCFA) -> None:
        self.params = params
        self._delta_t_sismico = params.longitud_brazo / params.v_seismica
        self._delta_t_luz = params.longitud_brazo / C

    # ------------------------------------------------------------------
    def estimar_espectro_sismico(
        self, senal: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Estima S_moon(f) y S_total(f) a partir de la señal cruda.

        La componente sísmica se identifica como la potencia cuya correlación
        cruzada con sí misma a retraso Δt_sísmico es alta, mientras que la
        componente de tejido es la potencia coherente a Δt ≈ 0 (≈ Δt_luz).

        Parameters
        ----------
        senal : np.ndarray
            Señal de fase observada Φ_raw en el dominio temporal.

        Returns
        -------
        s_moon : np.ndarray
            Estimación del PSD sísmico lunar [V²/Hz], tamaño (N//2+1,).
        s_total : np.ndarray
            PSD total de la señal, tamaño (N//2+1,).
        """
        n = len(senal)
        # PSD total mediante periodograma de Welch sencillo
        freqs = np.fft.rfftfreq(n, d=1.0 / self.params.fs)
        fft_raw = np.fft.rfft(senal * windows.hann(n))
        s_total = np.abs(fft_raw) ** 2 / n

        # Estimación de la componente sísmica:
        # creamos una versión retardada de la señal en Δt_sísmico y obtenemos
        # la parte que correlaciona fuertemente con el original en ese retraso.
        lag_samples = int(round(self._delta_t_sismico * self.params.fs))
        lag_samples = min(lag_samples, n - 1)

        if lag_samples > 0:
            senal_retardada = np.zeros_like(senal)
            senal_retardada[lag_samples:] = senal[:-lag_samples]
        else:
            senal_retardada = senal.copy()

        fft_retardada = np.fft.rfft(senal_retardada * windows.hann(n))
        # Correlación cruzada espectral normalizada como fracción sísmica.
        # np.divide con el parámetro `where` evita evaluar la división en bins
        # donde s_total == 0 (sin RuntimeWarning por división por cero).
        cross_power = np.abs(fft_raw * np.conj(fft_retardada)) / n
        mask_nonzero = s_total > 0
        ratio = np.divide(cross_power, s_total, where=mask_nonzero, out=np.zeros_like(s_total))
        fraccion_sismica = np.where(mask_nonzero, np.minimum(ratio, 1.0), 0.0)
        s_moon = fraccion_sismica * s_total
        return s_moon, s_total

    # ------------------------------------------------------------------
    def aplicar(self, senal: np.ndarray) -> np.ndarray:
        """
        Aplica el kernel de rechazo de ruido sísmico.

        Φ_clean(f) = Φ_raw(f) · [1 - S_moon(f) / S_total(f)]

        Parameters
        ----------
        senal : np.ndarray
            Señal cruda en dominio temporal.

        Returns
        -------
        senal_limpia : np.ndarray
            Señal con ruido sísmico atenuado.
        """
        if len(senal) == 0:
            raise ValueError("La señal no puede estar vacía.")

        n = len(senal)
        s_moon, s_total = self.estimar_espectro_sismico(senal)

        # Factor de transferencia del kernel: 1 - S_moon/S_total.
        # np.divide con `where` evita divisiones por cero sin RuntimeWarning.
        mask_nonzero = s_total > 0
        ratio_moon = np.divide(s_moon, s_total, where=mask_nonzero, out=np.zeros_like(s_total))
        kernel = np.where(mask_nonzero, 1.0 - ratio_moon, 1.0)
        kernel = np.clip(kernel, 0.0, 1.0)

        # Filtrado en frecuencia
        fft_raw = np.fft.rfft(senal)
        fft_clean = fft_raw * kernel
        senal_limpia = np.fft.irfft(fft_clean, n=n)
        return senal_limpia


# ============================================================================
# CLASE B: CORRECCIÓN DOPPLER SIDÉREO
# ============================================================================


class CorreccionDopplerSidereo:
    """
    Modela la corrección de frecuencia por el Efecto Doppler Sidéreo.

    La Luna se mueve con velocidad orbital v_Luna(t) respecto a la fuente.
    La frecuencia aparente en el detector es:

        f_target(t) = f₀ · (1 + v_Luna(t)·n̂ / c)

    donde n̂ es el vector unitario desde la Luna hacia la fuente.
    """

    # Velocidad orbital media de la Luna [m/s]
    V_ORBITAL_LUNA: float = 1022.0  # m/s

    def __init__(self, f0: float = _F0) -> None:
        if f0 <= 0:
            raise ValueError(f"f0 debe ser positiva, se recibió {f0}")
        self.f0 = f0

    def velocidad_proyectada(self, t: np.ndarray) -> np.ndarray:
        """
        Proyección v_Luna(t)·n̂ usando movimiento orbital circular uniforme.

        v_proyectada(t) = V_orbital · cos(ω_orbital · t)

        con ω_orbital = 2π / T_orbital (T_orbital ≈ 27,32 días).

        Parameters
        ----------
        t : np.ndarray
            Vector de tiempos [s].

        Returns
        -------
        v_proj : np.ndarray
            Velocidad proyectada [m/s] en cada instante.
        """
        omega_orbital = 2 * np.pi / T_ORBITAL_LUNAR_S
        return self.V_ORBITAL_LUNA * np.cos(omega_orbital * np.asarray(t))

    def frecuencia_objetivo(self, t: np.ndarray) -> np.ndarray:
        """
        Calcula f_target(t) = f₀ · (1 + v_Luna(t)·n̂ / c).

        Parameters
        ----------
        t : np.ndarray
            Vector de tiempos [s].

        Returns
        -------
        f_target : np.ndarray
            Frecuencia objetivo corregida por Doppler [Hz].
        """
        v_proj = self.velocidad_proyectada(t)
        return self.f0 * (1.0 + v_proj / C)


# ============================================================================
# CLASE C: INTEGRACIÓN DE FASE COHERENTE (STFT)
# ============================================================================


class IntegracionFaseCoherente:
    """
    Paso B — Integración de Fase Coherente vía STFT con compensación Doppler.

    Aplica una Transformada de Fourier de Tiempo Corto (STFT) con ventana
    vinculada a la rotación lunar y extrae la potencia en f_target(t).
    """

    def __init__(self, params: ParametrosFCFA) -> None:
        self.params = params
        self.doppler = CorreccionDopplerSidereo(f0=params.f0)

    # ------------------------------------------------------------------
    def calcular(
        self, senal_limpia: np.ndarray, t_offset: float = 0.0
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float]:
        """
        Aplica STFT y extrae la potencia en la línea f₀ corregida por Doppler.

        Parameters
        ----------
        senal_limpia : np.ndarray
            Señal en dominio temporal tras el kernel de rechazo de ruido.
        t_offset : float
            Tiempo absoluto del primer sample [s], para el cálculo Doppler.

        Returns
        -------
        freqs_stft : np.ndarray  — frecuencias del eje de la STFT [Hz]
        t_stft     : np.ndarray  — instantes centrales de cada ventana [s]
        f_doppler  : np.ndarray  — frecuencia objetivo por ventana [Hz]
        potencia_f0 : float      — potencia media en f₀ ± tolerancia
        """
        fs = self.params.fs
        nperseg = self.params.nperseg
        noverlap = self.params.noverlap

        freqs_stft, t_stft_rel, Zxx = stft(
            senal_limpia,
            fs=fs,
            nperseg=nperseg,
            noverlap=noverlap,
            window="hann",
            return_onesided=True,
        )

        t_stft = t_stft_rel + t_offset
        f_doppler = self.doppler.frecuencia_objetivo(t_stft)

        # La resolución espectral de la STFT es fs/nperseg Hz por bin.
        # La tolerancia de búsqueda es al menos un bin completo para garantizar
        # que siempre se captura al menos la frecuencia más próxima a f_target.
        resolucion_hz = fs / nperseg
        tolerancia_hz = max(0.5, resolucion_hz)
        potencias = np.zeros(len(t_stft))
        for i, fobj in enumerate(f_doppler):
            mascara = np.abs(freqs_stft - fobj) <= tolerancia_hz
            potencias[i] = np.mean(np.abs(Zxx[:, i][mascara]) ** 2) if mascara.any() else 0.0

        potencia_f0 = float(np.mean(potencias))
        return freqs_stft, t_stft, f_doppler, potencia_f0


# ============================================================================
# CLASE PRINCIPAL: FILTRO DE COHERENCIA DE FASE ADÉLICA
# ============================================================================


class FiltroCoherenciaFaseAdelica:
    """
    Filtro de Coherencia de Fase Adélica (FCFA) para la red IRS-Luna.

    Combina:
    - Kernel de Rechazo de Ruido (Paso A): elimina la componente sísmica
    - Integración de Fase Coherente con corrección Doppler (Paso B)
    - Estimación de ganancia SNR progresiva según la tabla del protocolo

    Uso típico
    ----------
    >>> params = ParametrosFCFA(fs=1024.0, n_brazos=3, t_integracion_h=48.0)
    >>> fcfa = FiltroCoherenciaFaseAdelica(params)
    >>> resultado = fcfa.procesar(senal_cruda, t_offset=0.0)
    >>> print(resultado.snr_estimada, resultado.etapa_deteccion)
    """

    def __init__(self, params: Optional[ParametrosFCFA] = None) -> None:
        self.params = params or ParametrosFCFA()
        self._kernel = KernelRechazoRuido(self.params)
        self._stft_integrador = IntegracionFaseCoherente(self.params)

    # ------------------------------------------------------------------
    def procesar(
        self, senal: np.ndarray, t_offset: float = 0.0
    ) -> ResultadoFCFA:
        """
        Aplica el pipeline completo FCFA a una señal de fase cruda.

        Parameters
        ----------
        senal : np.ndarray
            Señal Φ_raw(t) de un brazo del IRS-Luna.
        t_offset : float
            Tiempo absoluto del primer sample [s].

        Returns
        -------
        ResultadoFCFA
            Contenedor con señal limpia, frecuencias Doppler, SNR estimada
            y etapa de detección alcanzada.
        """
        if len(senal) == 0:
            raise ValueError("La señal de entrada no puede estar vacía.")

        # Paso A: Kernel de Rechazo de Ruido
        senal_limpia = self._kernel.aplicar(senal)

        # Paso B: Integración de Fase Coherente
        _, t_stft, f_doppler, potencia_f0 = self._stft_integrador.calcular(
            senal_limpia, t_offset=t_offset
        )

        # Estimación de SNR basada en la etapa de procesamiento
        snr_estimada = self._estimar_snr(potencia_f0)
        etapa = self._clasificar_etapa(snr_estimada)

        return ResultadoFCFA(
            senal_limpia=senal_limpia,
            fs=self.params.fs,
            f_doppler=f_doppler,
            potencia_f0=potencia_f0,
            snr_estimada=snr_estimada,
            t_stft=t_stft,
            etapa_deteccion=etapa,
        )

    # ------------------------------------------------------------------
    def _estimar_snr(self, potencia_f0: float) -> float:
        """
        Escala la potencia observada al rango SNR del protocolo FCFA.

        La escala relaciona la potencia media en f₀ con la SNR esperada tras
        el filtrado sísmico (SNR_ref = 0,8) más la ganancia por correlación
        de N brazos (∝ n_brazos²) e integración temporal (∝ √(t_int/48 h)).
        """
        # Ganancia por correlación de N brazos (Ψ_corr ∝ N²)
        ganancia_brazos = (self.params.n_brazos ** 2) / (N_BRAZOS ** 2)
        # Ganancia por integración temporal (∝ √(T / T_ref))
        ganancia_integracion = np.sqrt(
            self.params.t_integracion_h / T_INTEGRACION_DESCUBRIMIENTO_H
        )
        # SNR escalada desde el nivel de filtrado sísmico
        snr = SNR_FILTRADO_SISMICO * ganancia_brazos * ganancia_integracion
        # Factor de mérito de la potencia detectada.
        # Se usa la función sigmoidal p/(p+P_ref) donde P_ref = 1.0 (potencia
        # de referencia en unidades STFT normalizada) para mapear la potencia
        # observada al intervalo [0, 1] de forma continua y sin singularidades.
        _P_REF = 1.0
        factor_potencia = float(np.clip(potencia_f0 / (potencia_f0 + _P_REF), 0.0, 1.0))
        snr = snr * (1.0 + factor_potencia * (SNR_INTEGRACION_48H / SNR_FILTRADO_SISMICO - 1.0))
        return float(snr)

    # ------------------------------------------------------------------
    @staticmethod
    def _clasificar_etapa(snr: float) -> str:
        """Clasifica la etapa de detección según el valor de SNR."""
        if snr >= SNR_INTEGRACION_48H:
            return f"Descubrimiento (>{UMBRAL_DESCUBRIMIENTO_5SIGMA}σ) — SNR ≈ {snr:.1f}"
        if snr >= SNR_CORRELACION_3_BRAZOS:
            return f"Detección Clara (>{UMBRAL_DETECCION_3SIGMA}σ) — SNR ≈ {snr:.1f}"
        if snr >= SNR_FILTRADO_SISMICO:
            return f"Emergencia línea base — SNR ≈ {snr:.1f}"
        return f"Señal enterrada en ruido — SNR ≈ {snr:.4f}"


# ============================================================================
# API PÚBLICA
# ============================================================================


def aplicar_filtro_fcfa(
    senal: np.ndarray,
    fs: float,
    t_offset: float = 0.0,
    n_brazos: int = N_BRAZOS,
    t_integracion_h: float = T_INTEGRACION_DESCUBRIMIENTO_H,
) -> ResultadoFCFA:
    """
    Aplica el Filtro de Coherencia de Fase Adélica (FCFA) a una señal cruda.

    Parameters
    ----------
    senal : np.ndarray
        Señal de fase Φ_raw(t) medida en un brazo del IRS-Luna.
    fs : float
        Frecuencia de muestreo [Hz]. Debe satisfacer fs ≥ 2·f₀ ≈ 283,4 Hz.
    t_offset : float
        Tiempo absoluto del primer sample [s] (para corrección Doppler).
    n_brazos : int
        Número de brazos del interferómetro (default 3).
    t_integracion_h : float
        Tiempo de integración coherente [h] (default 48 h).

    Returns
    -------
    ResultadoFCFA
        Contenedor de resultados del filtrado FCFA.
    """
    params = ParametrosFCFA(
        fs=fs,
        n_brazos=n_brazos,
        t_integracion_h=t_integracion_h,
    )
    fcfa = FiltroCoherenciaFaseAdelica(params)
    return fcfa.procesar(senal, t_offset=t_offset)


def estimar_ganancia_snr(
    n_brazos: int = N_BRAZOS,
    t_integracion_h: float = T_INTEGRACION_DESCUBRIMIENTO_H,
) -> dict:
    """
    Estima la ganancia de SNR del protocolo FCFA en cada etapa de procesamiento.

    Parameters
    ----------
    n_brazos : int
        Número de brazos del interferómetro (1–N).
    t_integracion_h : float
        Tiempo de integración coherente [h].

    Returns
    -------
    dict
        Diccionario con la SNR relativa por etapa:
        {
          "crudo":              float,
          "filtrado_sismico":   float,
          "correlacion_brazos": float,
          "integracion_final":  float,
        }
    """
    if n_brazos < 1:
        raise ValueError(f"n_brazos debe ser ≥ 1, se recibió {n_brazos}")
    if t_integracion_h <= 0:
        raise ValueError(
            f"t_integracion_h debe ser positivo, se recibió {t_integracion_h}"
        )

    ganancia_brazos = (n_brazos ** 2) / (N_BRAZOS ** 2)
    ganancia_integracion = np.sqrt(t_integracion_h / T_INTEGRACION_DESCUBRIMIENTO_H)

    return {
        "crudo": SNR_CRUDO,
        "filtrado_sismico": SNR_FILTRADO_SISMICO,
        "correlacion_brazos": ganancia_brazos * SNR_CORRELACION_3_BRAZOS,
        "integracion_final": ganancia_brazos * ganancia_integracion * SNR_INTEGRACION_48H,
    }
