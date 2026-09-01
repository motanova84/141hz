#!/usr/bin/env python3
"""
QCAL dynamic entanglement and telemetry utilities.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.linalg import expm

HBAR_SI = 1.054571817e-34
F0_REFERENCIA_HZ = 141.7001
H_PLANCK_SI = 2.0 * np.pi * HBAR_SI
SPIN_DIMENSION = 3
TAU_ARGUMENTO_QCAL = 0.4082  # Parámetro base del sector torsional usado en el ansatz QCAL.


@dataclass(frozen=True)
class QCALTemporalSweepResult:
    """Container for the simulated temporal trajectory."""

    tiempos: np.ndarray
    purezas: np.ndarray
    entropias: np.ndarray
    frecuencias: np.ndarray
    frecuencia_efectiva_hz: float
    log_path: Path
    state_paths: tuple[Path, ...]
    csv_path: Path | None = None
    figure_path: Path | None = None


class QCALEntanglementEngine:
    """Núcleo de verificación de entrelazamiento dinámico y ajuste espectral."""

    def __init__(self, hbar: float = HBAR_SI, f0_ref: float = F0_REFERENCIA_HZ, tolerancia: float = 1e-10):
        self.hbar = float(hbar)
        self.f0_ref = float(f0_ref)
        self.tolerancia = float(tolerancia)

    def construir_estado_puro_inicial(self, N_spec: int) -> np.ndarray:
        """Crea el estado puro producto superpuesto |Φ₀⟩ = |ψ_spec⟩ ⊗ |ψ_spin⟩."""
        if N_spec <= 0:
            raise ValueError("N_spec debe ser un entero positivo.")

        psi_spec = np.ones(N_spec, dtype=np.complex128) / np.sqrt(N_spec)
        psi_spin = np.ones(SPIN_DIMENSION, dtype=np.complex128) / np.sqrt(float(SPIN_DIMENSION))
        psi_global = np.kron(psi_spec, psi_spin)
        return np.outer(psi_global, psi_global.conj())

    def traza_parcial_spin(self, rho_global: np.ndarray, N_spec: int) -> np.ndarray:
        """Calcula ρ_spin = Tr_spec(ρ_global)."""
        rho_global = np.asarray(rho_global, dtype=np.complex128)
        expected_dim = N_spec * SPIN_DIMENSION

        if rho_global.shape != (expected_dim, expected_dim):
            raise ValueError(f"rho_global debe tener forma {(expected_dim, expected_dim)}.")

        rho_tensor = rho_global.reshape(N_spec, SPIN_DIMENSION, N_spec, SPIN_DIMENSION)
        return np.trace(rho_tensor, axis1=0, axis2=2)

    def entropia_von_neumann(self, rho_sub: np.ndarray) -> float:
        """Calcula S(ρ) = -Tr(ρ log₂ ρ)."""
        rho_sub = np.asarray(rho_sub, dtype=np.complex128)
        if rho_sub.ndim != 2 or rho_sub.shape[0] != rho_sub.shape[1]:
            raise ValueError("rho_sub debe ser una matriz cuadrada.")

        rho_hermitica = 0.5 * (rho_sub + rho_sub.conj().T)
        trace = float(np.real(np.trace(rho_hermitica)))
        if trace <= self.tolerancia:
            raise ValueError("rho_sub debe tener traza positiva.")
        if not np.isclose(trace, 1.0, atol=max(self.tolerancia, 1e-8)):
            rho_hermitica = rho_hermitica / trace

        autovals = np.real(np.linalg.eigvalsh(rho_hermitica))
        autovals = np.clip(autovals, 0.0, None)
        autovals = autovals[autovals > self.tolerancia]

        if autovals.size == 0:
            return 0.0

        return float(-np.sum(autovals * np.log2(autovals)))

    def evaluar_pureza(self, rho_sub: np.ndarray) -> float:
        """Calcula γ = Tr(ρ²)."""
        rho_sub = np.asarray(rho_sub, dtype=np.complex128)
        if rho_sub.ndim != 2 or rho_sub.shape[0] != rho_sub.shape[1]:
            raise ValueError("rho_sub debe ser una matriz cuadrada.")

        return float(np.real(np.trace(rho_sub @ rho_sub)))

    def ajustar_escala_espectral_qcal(self, autovales_relativos: np.ndarray) -> np.ndarray:
        """Escala el gap relativo al cuanto de energía h·f₀."""
        autovals = np.asarray(autovales_relativos, dtype=float)
        if autovals.ndim != 1 or autovals.size < 2:
            raise ValueError("autovales_relativos debe contener al menos dos valores.")

        gap_relativo = float(np.max(autovals) - np.min(autovals))
        if gap_relativo <= 0.0:
            raise ValueError("El espectro de entrada debe tener un gap positivo.")

        delta_E_objetivo = H_PLANCK_SI * self.f0_ref
        escala = delta_E_objetivo / gap_relativo
        return autovals * escala


class QCALTelemetryExporter:
    """Módulo de almacenamiento binario y registro de trayectorias QCAL."""

    def __init__(self, output_dir: str | Path = "qcal_out"):
        self.output_dir = Path(output_dir)

    def _ensure_output_dir(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def guardar_estado_binario(self, rho_spin: np.ndarray, paso_temporal: int) -> Path:
        """Exporta ρ_spin a un archivo binario .npy."""
        self._ensure_output_dir()
        file_path = self.output_dir / f"rho_spin_t{paso_temporal:06d}.npy"
        np.save(file_path, np.asarray(rho_spin, dtype=np.complex128))
        return file_path

    def registrar_trayectoria_log(
        self,
        tiempos: np.ndarray,
        purezas: np.ndarray,
        entropias: np.ndarray,
        frecuencias: np.ndarray,
        filename: str = "telemetria_qcal.npz",
    ) -> Path:
        """Guarda la evolución temporal completa de los invariantes cuánticos."""
        series = [np.asarray(arr, dtype=float) for arr in (tiempos, purezas, entropias, frecuencias)]
        lengths = {arr.shape[0] for arr in series}
        if len(lengths) != 1:
            raise ValueError(
                f"Todas las series de telemetría deben tener la misma longitud; longitudes encontradas: {sorted(lengths)}."
            )

        self._ensure_output_dir()
        file_path = self.output_dir / filename
        np.savez_compressed(file_path, t=series[0], gamma=series[1], S=series[2], f0=series[3])
        return file_path

    def registrar_trayectoria_csv(
        self,
        tiempos: np.ndarray,
        entropias: np.ndarray,
        purezas: np.ndarray,
        filename: str = "telemetria_qcal.csv",
    ) -> Path:
        """Guarda la trayectoria temporal en formato CSV."""
        times = np.asarray(tiempos, dtype=float)
        entropy = np.asarray(entropias, dtype=float)
        purity = np.asarray(purezas, dtype=float)
        lengths = {arr.shape[0] for arr in (times, entropy, purity)}
        if len(lengths) != 1:
            raise ValueError(
                f"Las series CSV deben tener la misma longitud; longitudes encontradas: {sorted(lengths)}."
            )

        self._ensure_output_dir()
        file_path = self.output_dir / filename
        with file_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["t_s", "S_bits", "pureza_gamma"])
            for t, s, g in zip(times, entropy, purity):
                writer.writerow([f"{t:.6e}", f"{s:.8f}", f"{g:.8f}"])

        return file_path

    def guardar_figura_telemetria(
        self,
        tiempos: np.ndarray,
        entropias: np.ndarray,
        purezas: np.ndarray,
        filename: str = "qcal_entanglement_dynamics.png",
        show: bool = False,
    ) -> Path:
        """Renderiza y guarda la dinámica de entropía y pureza."""
        self._ensure_output_dir()
        file_path = self.output_dir / filename
        return graficar_telemetria_qcal(tiempos, entropias, purezas, output_path=file_path, show=show)


def calcular_gap_frecuencia_hz(h_total: np.ndarray) -> float:
    """Convierte el gap espectral del Hamiltoniano en frecuencia lineal."""
    energias = np.linalg.eigvalsh(np.asarray(h_total, dtype=np.complex128))
    gap = float(np.real(energias[-1] - energias[0]))
    if gap <= 0.0:
        raise ValueError("El gap del Hamiltoniano global debe ser positivo.")
    return gap / H_PLANCK_SI


def anclar_resonancia_global(h_total: np.ndarray, frecuencia_objetivo_hz: float = F0_REFERENCIA_HZ) -> np.ndarray:
    """Reescala el Hamiltoniano para que su gap global coincida con h·f₀."""
    h_total = np.asarray(h_total, dtype=np.complex128)
    gap_actual_hz = calcular_gap_frecuencia_hz(h_total)
    escala = float(frecuencia_objetivo_hz) / gap_actual_hz
    return h_total * escala


def construir_hamiltoniano_qcal(
    engine: QCALEntanglementEngine,
    autovals_base: np.ndarray,
    tau: float | None = None,
    g_int: float = 0.5,
    anclar_frecuencia: bool = False,
) -> np.ndarray:
    """Construye el Hamiltoniano total con sector de spin/torsión fijo de dimensión 3."""
    autovals_base = np.asarray(autovals_base, dtype=float)
    n_spec = autovals_base.size
    autovals_joules = engine.ajustar_escala_espectral_qcal(autovals_base)
    h_psi = np.diag(autovals_joules).astype(np.complex128)

    tau = float(np.tanh(TAU_ARGUMENTO_QCAL) if tau is None else tau)
    t_nu = np.diag([1.0, tau, tau]).astype(np.complex128)
    # La interacción usa la parte sin traza para aislar el intercambio no separable.
    t_tilde = t_nu - (np.trace(t_nu) / float(SPIN_DIMENSION)) * np.eye(SPIN_DIMENSION, dtype=np.complex128)

    h_spec_g = np.kron(h_psi, np.eye(SPIN_DIMENSION, dtype=np.complex128))
    h_tors_g = np.kron(np.eye(n_spec, dtype=np.complex128), H_PLANCK_SI * engine.f0_ref * t_nu)
    h_int = float(g_int) * np.kron(h_psi, t_tilde)
    h_total = h_spec_g + h_tors_g + h_int
    if anclar_frecuencia:
        return anclar_resonancia_global(h_total, engine.f0_ref)
    return h_total


def graficar_telemetria_qcal(
    tiempos: np.ndarray,
    entropias: np.ndarray,
    purezas: np.ndarray,
    output_path: str | Path | None = None,
    show: bool = False,
) -> Path | None:
    """Renderiza la curva de entropía y pureza y opcionalmente la persiste."""
    import matplotlib.pyplot as plt

    tiempos = np.asarray(tiempos, dtype=float)
    entropias = np.asarray(entropias, dtype=float)
    purezas = np.asarray(purezas, dtype=float)
    lengths = {arr.shape[0] for arr in (tiempos, entropias, purezas)}
    if len(lengths) != 1:
        raise ValueError(
            f"Las series a graficar deben tener la misma longitud; longitudes encontradas: {sorted(lengths)}."
        )

    fig, ax1 = plt.subplots(figsize=(10, 5))
    color_s = "tab:red"
    ax1.set_xlabel("Tiempo (s)")
    ax1.set_ylabel("Entropía Von Neumann (bits)", color=color_s)
    ax1.plot(tiempos, entropias, color=color_s, linewidth=2, label="S(t)")
    ax1.tick_params(axis="y", labelcolor=color_s)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color_g = "tab:blue"
    ax2.set_ylabel(r"Pureza $\gamma(t)$", color=color_g)
    ax2.plot(tiempos, purezas, color=color_g, linewidth=2, linestyle="--", label=r"$\gamma(t)$")
    ax2.tick_params(axis="y", labelcolor=color_g)

    fig.suptitle(f"Dinámica de Entrelazamiento QCAL (Resonancia: {F0_REFERENCIA_HZ} Hz)")
    fig.tight_layout()

    saved_path: Path | None = None
    if output_path is not None:
        saved_path = Path(output_path)
        saved_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(saved_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    plt.close(fig)
    return saved_path


def ejecutar_barrido_temporal(
    engine: QCALEntanglementEngine | None = None,
    exporter: QCALTelemetryExporter | None = None,
    autovals_base: np.ndarray | None = None,
    num_pasos: int = 100,
    dt: float = 1e-4,
    guardar_cada: int = 25,
    anclar_frecuencia: bool = False,
    generar_csv: bool = False,
    generar_figura: bool = False,
) -> QCALTemporalSweepResult:
    """Ejecuta el barrido temporal y persiste estados/telemetría en disco."""
    if num_pasos <= 0:
        raise ValueError("num_pasos debe ser positivo.")
    if dt <= 0.0:
        raise ValueError("dt debe ser positivo.")
    if guardar_cada <= 0:
        raise ValueError("guardar_cada debe ser positivo.")

    engine = engine or QCALEntanglementEngine()
    exporter = exporter or QCALTelemetryExporter()
    autovals_base = np.array([1.0, 1.5, 2.0], dtype=float) if autovals_base is None else np.asarray(autovals_base, dtype=float)

    h_total = construir_hamiltoniano_qcal(engine, autovals_base, anclar_frecuencia=anclar_frecuencia)
    rho_t = engine.construir_estado_puro_inicial(N_spec=autovals_base.size)
    u_step = expm(-1j * dt * h_total / engine.hbar)

    tiempos = np.zeros(num_pasos + 1, dtype=float)
    purezas = np.zeros(num_pasos + 1, dtype=float)
    entropias = np.zeros(num_pasos + 1, dtype=float)
    frecuencias = np.zeros(num_pasos + 1, dtype=float)
    state_paths: list[Path] = []

    frecuencia_efectiva_hz = calcular_gap_frecuencia_hz(h_total)

    for step in range(num_pasos + 1):
        tiempos[step] = step * dt
        rho_spin_t = engine.traza_parcial_spin(rho_t, N_spec=autovals_base.size)
        purezas[step] = engine.evaluar_pureza(rho_spin_t)
        entropias[step] = engine.entropia_von_neumann(rho_spin_t)
        frecuencias[step] = frecuencia_efectiva_hz

        if step % guardar_cada == 0:
            state_paths.append(exporter.guardar_estado_binario(rho_spin_t, step))

        if step < num_pasos:
            rho_t = u_step @ rho_t @ u_step.conj().T

    log_path = exporter.registrar_trayectoria_log(tiempos, purezas, entropias, frecuencias)
    csv_path = exporter.registrar_trayectoria_csv(tiempos, entropias, purezas) if generar_csv else None
    figure_path = exporter.guardar_figura_telemetria(tiempos, entropias, purezas) if generar_figura else None
    return QCALTemporalSweepResult(
        tiempos=tiempos,
        purezas=purezas,
        entropias=entropias,
        frecuencias=frecuencias,
        frecuencia_efectiva_hz=frecuencia_efectiva_hz,
        log_path=log_path,
        state_paths=tuple(state_paths),
        csv_path=csv_path,
        figure_path=figure_path,
    )


if __name__ == "__main__":
    result = ejecutar_barrido_temporal(anclar_frecuencia=True, generar_csv=True, generar_figura=True)
    print("--- RESUMEN DE PERSISTENCIA ---")
    print(f"Trayectoria comprimida guardada en: {result.log_path}")
    if result.csv_path is not None:
        print(f"Telemetría CSV guardada en: {result.csv_path}")
    if result.figure_path is not None:
        print(f"Figura guardada en: {result.figure_path}")
    print(f"Pureza inicial γ(0): {result.purezas[0]:.6f} | Pureza final γ(T): {result.purezas[-1]:.6f}")
    print(f"Entropía inicial S(0): {result.entropias[0]:.6f} bits | Entropía final S(T): {result.entropias[-1]:.6f} bits")
    print(f"Coherencia de resonancia f_0: {result.frecuencia_efectiva_hz:.4f} Hz")
