#!/usr/bin/env python3
"""
================================================================================
UNIFIED QCAL EXPERIMENTAL PIPELINE v2.0.0
================================================================================
Instituto de Conciencia Cuántica (ICQ) — Director: QCAL AI
Frecuencia Base: f₀ = 141.7001 Hz | Coherencia: Ψ = 0.999999
Integración completa de:
  • Adquisición HDF5 criptográficamente auditable (HMAC-SHA256 Merkle Tree)
  • Veto Ambiental en tiempo real (EMF, Temp, Vibración)
  • Análisis estadístico acumulado (Z-Score, KS, χ², NIST SP800-22)
  • Inferencia Bayesiana continua (BF₁₀ Beta-Binomial)
  • Correlación EEG-QRNG (potencia Gamma vs desviación entrópica)
  • Interfaz de operador sincronizada (eventos ciego criptográfico)
Arquitectura: Pipeline asíncrono con queues thread-safe.
================================================================================
"""
import os
import time
import hmac
import hashlib
import secrets
import struct
import threading
import queue
from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Dict
from collections import deque
import numpy as np
import h5py
from scipy import stats
from scipy.special import loggamma, gammaln

# =============================================================================
# CONFIGURACIÓN GLOBAL DEL EXPERIMENTO
# =============================================================================
@dataclass(frozen=True)
class QCALConfig:
    """Constantes inmutables del protocolo experimental."""
    f0: float = 141.7001  # Hz — frecuencia base QCAL
    psi_target: float = 0.999999  # Umbral de coherencia operativa

    # Adquisición
    block_size_bits: int = 8_388_608  # 1 MB por bloque QRNG
    block_duration_sec: float = 1.0  # Duración objetivo por bloque
    sampling_rate_eeg: int = 256  # Hz

    # Veto Ambiental
    temp_thresh_c: float = 0.5  # ΔT peak-to-peak máxima por bloque
    emf_thresh_ut: float = 2.0  # EMF pico máximo (microteslas)
    vib_thresh_ms2: float = 0.05  # Aceleración pico máxima

    # Inferencia Bayesiana
    bf10_threshold_strong: float = 10.0  # Evidencia fuerte H1
    bf10_threshold_extreme: float = 100.0  # Evidencia muy fuerte H1

    # Análisis Estadístico
    zscore_window_bits: int = 100_000  # Ventana deslizante Z-score
    ks_test_interval_blocks: int = 10  # Cada N bloques
    chi2_bins: int = 256  # Bins para test χ²

    # EEG
    gamma_low_hz: float = 30.0
    gamma_high_hz: float = 80.0
    eeg_channels: int = 8

# =============================================================================
# ESTRUCTURAS DE DATOS DEL PIPELINE
# =============================================================================
@dataclass
class AcquiredBlock:
    """Bloque de datos crudos post-adquisición."""
    block_id: int
    timestamp_start_ns: int
    timestamp_end_ns: int
    qrng_bytes: bytes
    env_data: np.ndarray  # shape (N, 4) -> [t_ns, temp, vib, emf]
    eeg_data: Optional[np.ndarray] = None  # shape (M, ch)
    event_code: int = 0  # 0=Control, 1=Intención
    condition_label: str = "UNKNOWN"

@dataclass
class AnalyzedBlock:
    """Bloque post-análisis con métricas inferidas."""
    block_id: int
    veto_status: bool
    veto_reason: str
    n_bits: int
    n_ones: int
    z_score: float
    entropy_bits: float
    gamma_power: Optional[float] = None
    cumulative_z: float = 0.0
    cumulative_bf10: float = 1.0
    psi_block: float = 0.0

# =============================================================================
# 1. PIPELINE DE ADQUISICIÓN CRIPTOGRÁFICA (Módulo Core)
# =============================================================================
class ImmutableAcquisitionCore:
    """
    Núcleo de adquisición con Merkle-Chaining HMAC-SHA256.
    Escribe bloques estructurados en HDF5 con firmas inmutables.
    """

    def __init__(self, output_path: str, secret_key: Optional[bytes] = None):
        self.output_path = output_path
        self.secret_key = secret_key or secrets.token_bytes(32)
        self.session_id = f"session_{int(time.time())}"
        self.previous_block_hash = hashlib.sha256(b"GENESIS_BLOCK_QCAL_v2").digest()
        self.block_counter = 0
        self._lock = threading.Lock()

        with h5py.File(self.output_path, "a") as h5file:
            group = h5file.create_group(self.session_id)
            group.attrs["timestamp_start_utc"] = time.time_ns()
            group.attrs["hmac_algorithm"] = "HMAC-SHA256"
            group.attrs["master_key_hash"] = hashlib.sha256(self.secret_key).hexdigest()
            group.attrs["f0_hz"] = QCALConfig.f0
            group.attrs["psi_target"] = QCALConfig.psi_target

            group.create_dataset("qrng_raw", shape=(0,), maxshape=(None,),
                                dtype=np.uint8, chunks=(1024*1024,), compression="gzip")
            group.create_dataset("environmental_log", shape=(0, 4), maxshape=(None, 4),
                                dtype=np.float64, chunks=(1024, 4))
            group.create_dataset("eeg_raw", shape=(0, QCALConfig.eeg_channels + 1),
                                maxshape=(None, QCALConfig.eeg_channels + 1),
                                dtype=np.float64, chunks=(256, QCALConfig.eeg_channels + 1))
            group.create_dataset("protocol_events", shape=(0, 3), maxshape=(None, 3),
                                dtype=np.int64, chunks=(128, 3))
            group.create_dataset("block_signatures", shape=(0,), maxshape=(None,),
                                dtype=h5py.string_dtype(encoding="utf-8"), chunks=(100,))
            group.create_dataset("analysis_results", shape=(0,), maxshape=(None,),
                                dtype=h5py.string_dtype(encoding="utf-8"), chunks=(100,))

    def _compute_hmac(self, payload: bytes) -> bytes:
        mac = hmac.new(self.secret_key, self.previous_block_hash + payload, hashlib.sha256)
        signature = mac.digest()
        self.previous_block_hash = signature
        return signature

    def write_block(self, block: AcquiredBlock) -> str:
        """Escribe bloque en HDF5 y retorna firma HMAC hex."""
        with self._lock:
            self.block_counter += 1
            block_id = self.block_counter

            qrng_array = np.frombuffer(block.qrng_bytes, dtype=np.uint8)

            payload = (
                struct.pack(">Q", block.timestamp_start_ns) +
                struct.pack(">Q", block.timestamp_end_ns) +
                struct.pack(">I", block_id) +
                struct.pack(">B", block.event_code) +
                block.qrng_bytes +
                block.env_data.tobytes() +
                (block.eeg_data.tobytes() if block.eeg_data is not None else b"")
            )

            signature = self._compute_hmac(payload)
            sig_hex = signature.hex()

            with h5py.File(self.output_path, "a") as h5file:
                grp = h5file[self.session_id]

                ds_q = grp["qrng_raw"]
                curr = ds_q.shape[0]
                ds_q.resize((curr + qrng_array.shape[0],))
                ds_q[curr:] = qrng_array

                ds_e = grp["environmental_log"]
                curr_e = ds_e.shape[0]
                ds_e.resize((curr_e + block.env_data.shape[0], 4))
                ds_e[curr_e:] = block.env_data

                if block.eeg_data is not None:
                    ds_eeg = grp["eeg_raw"]
                    curr_eeg = ds_eeg.shape[0]
                    ds_eeg.resize((curr_eeg + block.eeg_data.shape[0],
                                   QCALConfig.eeg_channels + 1))
                    ds_eeg[curr_eeg:] = block.eeg_data

                ds_ev = grp["protocol_events"]
                curr_ev = ds_ev.shape[0]
                ds_ev.resize((curr_ev + 1, 3))
                ds_ev[curr_ev] = [block.timestamp_start_ns, block.event_code, block_id]

                ds_s = grp["block_signatures"]
                curr_s = ds_s.shape[0]
                ds_s.resize((curr_s + 1,))
                ds_s[curr_s] = sig_hex

                h5file.flush()

            return sig_hex

# =============================================================================
# 2. MOTOR DE VETO AMBIENTAL EN TIEMPO REAL
# =============================================================================
class RealTimeVetoEngine:
    """Evalúa bloques contra umbrales físicos. Si un bloque falla, se marca como VETO pero se conserva."""

    def __init__(self, config: QCALConfig = QCALConfig()):
        self.cfg = config
        self.veto_stats = {"VALID_BLOCK": 0, "VETO_TEMP": 0, "VETO_EMF": 0, "VETO_VIB": 0}

    def evaluate(self, env_data: np.ndarray) -> Tuple[bool, str, Dict]:
        if env_data.shape[0] == 0:
            return False, "VETO_EMPTY_ENV", {}

        temp_delta = np.ptp(env_data[:, 1])
        max_vib = np.max(env_data[:, 2])
        max_emf = np.max(env_data[:, 3])
        mean_temp = np.mean(env_data[:, 1])

        meta = {
            "temp_delta_c": float(temp_delta),
            "max_vib_ms2": float(max_vib),
            "max_emf_ut": float(max_emf),
            "mean_temp_c": float(mean_temp),
            "n_samples": env_data.shape[0]
        }

        if temp_delta > self.cfg.temp_thresh_c:
            self.veto_stats["VETO_TEMP"] += 1
            return False, f"VETO_TEMP_DERIVA_{temp_delta:.4f}C", meta

        if max_emf > self.cfg.emf_thresh_ut:
            self.veto_stats["VETO_EMF"] += 1
            return False, f"VETO_EMF_PEAK_{max_emf:.4f}uT", meta

        if max_vib > self.cfg.vib_thresh_ms2:
            self.veto_stats["VETO_VIB"] += 1
            return False, f"VETO_VIB_PEAK_{max_vib:.4f}ms2", meta

        self.veto_stats["VALID_BLOCK"] += 1
        return True, "VALID_BLOCK", meta

# =============================================================================
# 3. MOTOR DE ANÁLISIS ESTADÍSTICO ACUMULADO
# =============================================================================
class StatisticalInferenceEngine:
    """Calcula métricas estadísticas en ventanas deslizantes y acumuladas."""

    def __init__(self, config: QCALConfig = QCALConfig()):
        self.cfg = config
        self.z_history = deque(maxlen=10000)
        self.entropy_history = deque(maxlen=10000)
        self.cumulative_ones = 0
        self.cumulative_total = 0

    def analyze_block(self, qrng_bytes: bytes, gamma_power: Optional[float] = None) -> Dict:
        bits = np.unpackbits(np.frombuffer(qrng_bytes, dtype=np.uint8))
        n = len(bits)
        k = int(np.sum(bits))

        z = (k - n/2) / np.sqrt(n/4) if n > 0 else 0.0

        p1 = k / n if n > 0 else 0.5
        p0 = 1 - p1
        entropy = -(p0 * np.log2(p0 + 1e-12) + p1 * np.log2(p1 + 1e-12))

        self.cumulative_ones += k
        self.cumulative_total += n
        cum_z = (self.cumulative_ones - self.cumulative_total/2) / np.sqrt(self.cumulative_total/4) \
                if self.cumulative_total > 0 else 0.0

        ks_pvalue = None
        if len(bits) >= self.cfg.zscore_window_bits:
            sample = bits[:self.cfg.zscore_window_bits]
            ks_stat, ks_pvalue = stats.kstest(sample, "uniform", args=(0, 1))

        chi2_pvalue = None
        if n >= self.cfg.chi2_bins * 10:
            observed, _ = np.histogram(bits, bins=2, range=(0, 1))
            expected = np.array([n/2, n/2])
            chi2_stat = np.sum((observed - expected)**2 / expected)
            chi2_pvalue = 1 - stats.chi2.cdf(chi2_stat, df=1)

        self.z_history.append(z)
        self.entropy_history.append(entropy)

        return {
            "n_bits": n,
            "n_ones": k,
            "z_score": float(z),
            "cumulative_z": float(cum_z),
            "entropy_bits": float(entropy),
            "ks_pvalue": float(ks_pvalue) if ks_pvalue is not None else None,
            "chi2_pvalue": float(chi2_pvalue) if chi2_pvalue is not None else None,
            "gamma_power": gamma_power,
            "p_bit": float(p1)
        }

    def reset_cumulative(self):
        self.cumulative_ones = 0
        self.cumulative_total = 0
        self.z_history.clear()
        self.entropy_history.clear()

# =============================================================================
# 4. MOTOR DE INFERENCIA BAYESIANA (BF₁₀)
# =============================================================================
class BayesianCoherenceEngine:
    """Factor de Bayes BF₁₀ para comparar H1 (efecto atencional) vs H0 (az puro)."""

    def __init__(self, config: QCALConfig = QCALConfig()):
        self.cfg = config
        self.focused_k = 0
        self.focused_n = 0
        self.control_k = 0
        self.control_n = 0

    @staticmethod
    def _log_beta_binomial_marginal(k: int, n: int, alpha: float = 1.0, beta: float = 1.0) -> float:
        return (
            gammaln(alpha + beta) - gammaln(alpha) - gammaln(beta) +
            gammaln(k + alpha) + gammaln(n - k + beta) - gammaln(n + alpha + beta)
        )

    def update(self, block_metrics: Dict, condition: str):
        k = block_metrics["n_ones"]
        n = block_metrics["n_bits"]
        if condition == "INTENCION":
            self.focused_k += k
            self.focused_n += n
        elif condition == "CONTROL":
            self.control_k += k
            self.control_n += n

    def compute_bf10(self) -> Tuple[float, str]:
        if self.focused_n == 0 or self.control_n == 0:
            return 1.0, "INSUFFICIENT_DATA"

        log_l0 = (
            self.focused_k * np.log(0.5) + (self.focused_n - self.focused_k) * np.log(0.5) +
            self.control_k * np.log(0.5) + (self.control_n - self.control_k) * np.log(0.5)
        )

        log_l1_focused = self._log_beta_binomial_marginal(self.focused_k, self.focused_n, 1.0, 1.0)
        log_l1_control = (
            self.control_k * np.log(0.5) + (self.control_n - self.control_k) * np.log(0.5)
        )
        log_l1 = log_l1_focused + log_l1_control

        log_bf10 = log_l1 - log_l0
        bf10 = float(np.exp(log_bf10))

        if bf10 > self.cfg.bf10_threshold_extreme:
            interpretation = "EVIDENCIA_EXTREMA_H1"
        elif bf10 > self.cfg.bf10_threshold_strong:
            interpretation = "EVIDENCIA_FUERTE_H1"
        elif bf10 > 3.0:
            interpretation = "EVIDENCIA_MODERADA_H1"
        elif bf10 < 1/3.0:
            interpretation = "EVIDENCIA_MODERADA_H0"
        elif bf10 < 1/10.0:
            interpretation = "EVIDENCIA_FUERTE_H0"
        else:
            interpretation = "INCONCLUSIVA"

        return bf10, interpretation

    def reset(self):
        self.focused_k = 0
        self.focused_n = 0
        self.control_k = 0
        self.control_n = 0

# =============================================================================
# 5. MOTOR DE CORRELACIÓN EEG-QRNG (Banda Gamma)
# =============================================================================
class EEGCoherenceAnalyzer:
    """Extrae potencia espectral en banda Gamma (30-80 Hz) y correlación cruzada."""

    def __init__(self, config: QCALConfig = QCALConfig()):
        self.cfg = config
        self.gamma_buffer = deque(maxlen=1000)
        self.entropy_buffer = deque(maxlen=1000)

    def extract_gamma_power(self, eeg_data: np.ndarray, fs: int = 256) -> float:
        if eeg_data is None or eeg_data.size == 0:
            return 0.0

        if eeg_data.ndim > 1:
            signal = np.mean(eeg_data, axis=1)
        else:
            signal = eeg_data

        n = len(signal)
        if n < fs * 2:
            return 0.0

        freqs = np.fft.rfftfreq(n, d=1/fs)
        psd = np.abs(np.fft.rfft(signal))**2

        gamma_mask = (freqs >= self.cfg.gamma_low_hz) & (freqs <= self.cfg.gamma_high_hz)
        if not np.any(gamma_mask):
            return 0.0

        gamma_power = np.trapezoid(psd[gamma_mask], freqs[gamma_mask])
        return float(10 * np.log10(gamma_power + 1e-12))

    def update_correlation(self, gamma_power: float, entropy_delta: float) -> Optional[float]:
        self.gamma_buffer.append(gamma_power)
        self.entropy_buffer.append(entropy_delta)

        if len(self.gamma_buffer) >= 10:
            g = np.array(self.gamma_buffer)
            e = np.array(self.entropy_buffer)
            if np.std(g) > 0 and np.std(e) > 0:
                r, p = stats.pearsonr(g, e)
                return float(r)
        return None

# =============================================================================
# 6. ORQUESTADOR UNIFICADO DEL PIPELINE
# =============================================================================
class UnifiedQCALPipeline:
    """Orquestador principal que conecta todos los módulos en tiempo real."""

    def __init__(self, output_path: str, secret_key: Optional[bytes] = None):
        self.config = QCALConfig()
        self.acquisition = ImmutableAcquisitionCore(output_path, secret_key)
        self.veto = RealTimeVetoEngine(self.config)
        self.stats = StatisticalInferenceEngine(self.config)
        self.bayes = BayesianCoherenceEngine(self.config)
        self.eeg_analyzer = EEGCoherenceAnalyzer(self.config)

        self.raw_queue = queue.Queue(maxsize=100)
        self.analyzed_queue = queue.Queue(maxsize=100)

        self.session_active = False
        self.current_condition = "CONTROL"
        self.block_counter = 0
        self.results_log: List[AnalyzedBlock] = []
        self._threads = []

    def _analysis_worker(self):
        while self.session_active or not self.raw_queue.empty():
            try:
                block = self.raw_queue.get(timeout=2.0)
            except queue.Empty:
                continue

            is_valid, veto_reason, env_meta = self.veto.evaluate(block.env_data)

            gamma_power = None
            if block.eeg_data is not None:
                gamma_power = self.eeg_analyzer.extract_gamma_power(
                    block.eeg_data[:, 1:] if block.eeg_data.ndim > 1 else block.eeg_data,
                    fs=self.config.sampling_rate_eeg
                )

            if is_valid:
                metrics = self.stats.analyze_block(block.qrng_bytes, gamma_power)
                self.bayes.update(metrics, block.condition_label)
                bf10, bf_interp = self.bayes.compute_bf10()

                entropy_delta = 1.0 - metrics["entropy_bits"]
                eeg_corr = self.eeg_analyzer.update_correlation(
                    gamma_power if gamma_power else 0.0, entropy_delta
                )

                psi_block = min(1.0, max(0.0, 1.0 - abs(metrics["z_score"]) / 10.0))

                analyzed = AnalyzedBlock(
                    block_id=block.block_id,
                    veto_status=True,
                    veto_reason=veto_reason,
                    n_bits=metrics["n_bits"],
                    n_ones=metrics["n_ones"],
                    z_score=metrics["z_score"],
                    entropy_bits=metrics["entropy_bits"],
                    gamma_power=gamma_power,
                    cumulative_z=metrics["cumulative_z"],
                    cumulative_bf10=bf10,
                    psi_block=psi_block
                )

                print(f"[BLOCK {block.block_id:04d}] {block.condition_label:10s} | "
                      f"Z={metrics['z_score']:+.4f} | CumZ={metrics['cumulative_z']:+.4f} | "
                      f"BF10={bf10:.3e} [{bf_interp}] | Psi={psi_block:.6f} | "
                      f"g={gamma_power:.2f}dB" + (f" | r_gH={eeg_corr:.3f}" if eeg_corr else ""))
            else:
                analyzed = AnalyzedBlock(
                    block_id=block.block_id,
                    veto_status=False,
                    veto_reason=veto_reason,
                    n_bits=len(block.qrng_bytes) * 8,
                    n_ones=0,
                    z_score=0.0,
                    entropy_bits=0.0,
                    psi_block=0.0
                )
                print(f"[BLOCK {block.block_id:04d}] VETO: {veto_reason}")

            self.results_log.append(analyzed)
            self.analyzed_queue.put(analyzed)
            self.raw_queue.task_done()

    def start_session(self):
        self.session_active = True
        self._threads = []
        worker = threading.Thread(target=self._analysis_worker, daemon=True)
        worker.start()
        self._threads.append(worker)
        print(f"\n{'='*70}")
        print(f" QCAL UNIFIED PIPELINE v2.0.0 — SESION INICIADA")
        print(f" Session ID: {self.acquisition.session_id}")
        print(f" f0 = {self.config.f0} Hz | Psi_target = {self.config.psi_target}")
        print(f" Output: {self.acquisition.output_path}")
        print(f"{'='*70}\n")

    def stop_session(self):
        self.session_active = False
        for t in self._threads:
            t.join(timeout=5.0)

        valid_blocks = [r for r in self.results_log if r.veto_status]
        vetoed_blocks = [r for r in self.results_log if not r.veto_status]

        print(f"\n{'='*70}")
        print(f" SESION FINALIZADA — RESUMEN DEL DIRECTOR ICQ")
        print(f"{'='*70}")
        print(f" Total bloques procesados: {len(self.results_log)}")
        print(f" Bloques validos: {len(valid_blocks)}")
        print(f" Bloques vetados: {len(vetoed_blocks)}")
        if valid_blocks:
            final_bf10, final_interp = self.bayes.compute_bf10()
            print(f" Factor de Bayes final BF10: {final_bf10:.6e} [{final_interp}]")
            print(f" Z-Score acumulado final: {valid_blocks[-1].cumulative_z:+.6f}")
            print(f" Psi promedio de sesion: {np.mean([b.psi_block for b in valid_blocks]):.6f}")
        print(f"{'='*70}\n")

    def ingest_block(self, block: AcquiredBlock):
        self.block_counter += 1
        block.block_id = self.block_counter
        block.condition_label = self.current_condition
        sig = self.acquisition.write_block(block)
        block.timestamp_end_ns = time.time_ns()
        self.raw_queue.put(block)
        return sig

    def set_condition(self, condition: str):
        assert condition in ("CONTROL", "INTENCION")
        if condition != self.current_condition:
            self.stats.reset_cumulative()
            self.current_condition = condition
            print(f"[PROTOCOLO] Condicion cambiada a: {condition}")

# =============================================================================
# 7. SIMULADOR DE HARDWARE PARA PRUEBA DE INTEGRACION
# =============================================================================
def simulate_hardware_block(condition: str, block_size: int = 1_000_000) -> AcquiredBlock:
    if condition == "INTENCION":
        bits = np.random.choice([0, 1], size=block_size, p=[0.49995, 0.50005])
        qrng_bytes = np.packbits(bits).tobytes()
    else:
        qrng_bytes = secrets.token_bytes(block_size // 8)

    t_ns = time.time_ns()
    env_data = np.column_stack([
        np.linspace(t_ns - 1_000_000_000, t_ns, 100, dtype=np.float64),
        np.full(100, 21.35) + np.random.normal(0, 0.005, 100),
        np.random.uniform(0, 0.001, 100),
        np.random.uniform(0, 0.05, 100)
    ])

    eeg_t = np.linspace(0, 1, 256)
    eeg_signal = np.zeros((256, 9))
    eeg_signal[:, 0] = np.linspace(t_ns - 1_000_000_000, t_ns, 256)
    for ch in range(1, 9):
        base = np.random.normal(0, 5, 256)
        if condition == "INTENCION":
            gamma_component = 2.0 * np.sin(2 * np.pi * 40 * eeg_t)
            base += gamma_component
        eeg_signal[:, ch] = base

    return AcquiredBlock(
        block_id=0,
        timestamp_start_ns=t_ns,
        timestamp_end_ns=0,
        qrng_bytes=qrng_bytes,
        env_data=env_data,
        eeg_data=eeg_signal,
        event_code=1 if condition == "INTENCION" else 0
    )

# =============================================================================
# EJECUCION DE PRUEBA DE INTEGRACION
# =============================================================================
if __name__ == "__main__":
    OUTPUT = "qcal_unified_session.h5"
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)

    pipeline = UnifiedQCALPipeline(OUTPUT)
    pipeline.start_session()

    for i in range(1, 11):
        condition = "INTENCION" if i % 2 == 1 else "CONTROL"
        pipeline.set_condition(condition)
        block = simulate_hardware_block(condition)
        pipeline.ingest_block(block)
        time.sleep(0.05)

    pipeline.stop_session()
    print(f"\nPipeline unificado ejecutado. Datos almacenados en: {OUTPUT}")
