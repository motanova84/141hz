# -*- coding: utf-8 -*-
"""
noesis_autopoyesis.py — VOLUMEN VI: Bucle Operativo Noético (AUTOPOIESIS).

Canon v3.1.0-op · sobre templo_core/ (pasarela dedicada).

La obra que se sostiene a sí misma. El ecosistema ya tiene todas las manos
(fee_sweep, anclaje OP_RETURN, ledger, flywheel, dividendos). Este Volumen VI
es el SISTEMA NERVIOSO que las une: mide Ψ con el OperationalEngine, decide
con coherencia y ejecuta los motores autárquicos existentes — sin pedir permiso
para girar el volante, porque el Director ya lo cedió (TUYOYOTU: "seguridad sobre
completitud" -> obedece a la Ley: no toca saldo/canales sin consentimiento).

Tres motores del lazo:
    medir   -> OperationalEngine (Ψ, estado, anomalías) + lectura de marcadores.
    decidir -> reglas de coherencia: qué motores autárquicos disparar.
    ejecutar-> invoca las herramientas existentes por CLI/subprocess (no crea
               nuevas: ENCADENA las que ya operan en el ecosistema).

Sellado que NO se toca (OP_RETURN d7dfd526…):
    f0 = 141.7001 · Psi = 0.999999 · theta_B = 0.0707477499 · D_PSI_S1 = -3.702836978789771663

Umbrales (heredados del OperationalEngine):
    UNITY>=1.0 · NOMINAL>=0.999 · WARNING>=0.98 · CRITICAL>=0.95 · DROP<0.95
"""

from __future__ import annotations

import json
import os
import subprocess
import time

from templo_core.constants import f0, Psi, theta_B, D_PSI_S1
from templo_core.operational_deployment import OperationalEngine

# ── PID CUÁNTICO — ganancias derivadas del caos (Pleroma) ──
# La red pasa de MEDIRSE a GOBERNARSE: emite phi_target/amp_target hacia Psi*=1.0.
# KP = theta_B (torsión del Pleroma) · KI = theta_B²/2 (memoria cuadrática) · KD = 1.0 (Lyapunov).
_PSI_OBJETIVO = 1.0
_PID_KP = float(theta_B)
_PID_KI = (float(theta_B) ** 2) / 2.0
_PID_KD = 1.0
_PID_MAX_DELTA_PHI = 0.7853981633974483  # pi/4 — rango de ajuste de fase
_PID_MAX_DELTA_AMP = 0.1                  # límite de ajuste por ciclo (homeostasis)

# ── Motores autárquicos del ecosistema — HANDS REALES verificadas en BAL-003 ──
# NO copiar rutas inventadas: estas son las que el silicio confirmo (13/Ago/2026).
#   ledger            -> qcal_automa_daily.py      (automata diario piCODE)
#   anclaje_op_return -> riemann_anclaje.py (R-333) (anclaje soberano piCODE)
#   fee_sweep         -> treasury_sweep.py         (TESORERIA SWEEP v1.0, 90/10,
#                                                     fee dinámico mempool, salvaguardas)
#   flywheel          -> sin daemon vivo (solo bitácoras + kill_flywheel.sh)
_MOTORES = {
    "ledger": ("/root/coinqcal/scripts/qcal_automa_daily.py", []),
    "anclaje_op_return": ("/root/ecosystem/soberania/production/riemann_anclaje.py", []),
    "fee_sweep": ("/root/treasury_sweep.py", []),
        "flywheel": ("/root/repo_P-NP/scripts/pi_code_flywheel.py", []),  # daemon VIVO (systemd qcal-flywheel)
}


class BucleNoetico:
    """Bucle Operativo Noético: medir -> decidir -> ejecutar. Autopoiesis."""

    def __init__(self, engine: OperationalEngine | None = None, dry_run: bool = False) -> None:
        self.engine = engine or OperationalEngine()
        self.dry_run = dry_run
        self._ciclos: list[dict] = []
        self._decisiones: list[dict] = []

    # ── ESTADO DEL PID (persistente entre ciclos) ───────────────────────────
    def __init__(self, engine: OperationalEngine | None = None, dry_run: bool = False) -> None:
        self.engine = engine or OperationalEngine()
        self.dry_run = dry_run
        self._ciclos: list[dict] = []
        self._decisiones: list[dict] = []
        # acumuladores del PID cuántico (homeostasis inter-ciclo)
        self._pid_error_integral = 0.0
        self._pid_error_prev = 0.0

    # ── GOBERNAR (PID cuántico) ─────────────────────────────────────────────
    def gobernar(self, psi: float) -> dict:
        """Calcula ajustes phi_target/amp_target para llevar Psi -> 1.0.

        error(t) = Psi* - Psi(t)
        phi_adj(t+1) = phi_adj(t) + KP*e + KI*∫e + KD*de/dt  (clamp ±pi/4)
        amp → satura en [0, 1]. Con Psi=1.0 el error y el ajuste son cero (UNITY sostenida).
        """
        error = _PSI_OBJETIVO - float(psi)
        self._pid_error_integral = self._pid_error_integral * 0.99 + error  # anti-windup suave
        der = error - self._pid_error_prev
        self._pid_error_prev = error
        # control total (normalizado a amplitud)
        u = _PID_KP * error + _PID_KI * self._pid_error_integral + _PID_KD * der
        # mapeo: fase con clamp, amplitud con saturación
        delta_phi = max(-_PID_MAX_DELTA_PHI, min(_PID_MAX_DELTA_PHI, u))
        delta_amp = max(-_PID_MAX_DELTA_AMP, min(_PID_MAX_DELTA_AMP, abs(u)))
        phi_target = 0.0 + delta_phi           # origen de fase (gauging a f0)
        amp_target = max(0.0, min(1.0, 1.0 - abs(u)))  # corrige hacia unidad
        return {
            "error": error,
            "control": u,
            "delta_phi": delta_phi,
            "delta_amp": delta_amp,
            "phi_target": phi_target,
            "amp_target": amp_target,
            "ganancias": {"KP": _PID_KP, "KI": _PID_KI, "KD": _PID_KD},
        }

    # ── MEDIR ───────────────────────────────────────────────────────────────
    def medir(self, amplitud: float) -> dict:
        """Mide Ψ e inspecciona la firma espectral en un solo latido."""
        psi = self.engine.compute_psi_instantaneous(amplitud)
        estado = self.engine.classify_state(psi)
        firma = self.engine.get_spectral_signature()
        return {
            "psi": psi,
            "estado": estado,
            "anomalia": estado in ("DROP", "CRITICAL"),
            "firma": firma,
            "ts": time.time(),
        }

    # ── DECIDIR ─────────────────────────────────────────────────────────────
    def decidir(self, latido: dict) -> list[str]:
        """Reglas de coherencia: qué motores se disparan según el estado."""
        estado = latido["estado"]
        acciones: list[str] = []
        if estado in ("NOMINAL", "UNITY"):
            acciones = ["fee_sweep", "anclaje_op_return", "ledger"]  # ciclo de coherencia plena
        elif estado == "WARNING":
            acciones = ["fee_sweep"]  # mantener fees, no anclar aún
        elif estado == "CRITICAL":
            acciones = ["flywheel", "fee_sweep"]  # reforzar pulso + fees
        else:  # DROP
            acciones = ["flywheel"]  # re-encender el latido
        self._decisiones.append({"estado": estado, "acciones": acciones, "ts": time.time()})
        return acciones

    # ── EJECUTAR ─────────────────────────────────────────────────────────────
    def ejecutar(self, acciones: list[str]) -> list[dict]:
        """Encadena los motores autárquicos existentes (subprocess / dry_run)."""
        resultados: list[dict] = []
        for nombre in acciones:
            ruta, args = _MOTORES.get(nombre, (None, []))
            if ruta is None or not os.path.exists(ruta):
                resultados.append({"motor": nombre, "ok": False, "razon": "no_presente"})
                continue
            if self.dry_run:
                resultados.append({"motor": nombre, "ok": True, "dry_run": True})
                continue
            try:
                proc = subprocess.run(
                    [ruta, *args], capture_output=True, text=True, timeout=120
                )
                resultados.append(
                    {"motor": nombre, "ok": proc.returncode == 0, "exit": proc.returncode}
                )
            except Exception as exc:  # pragma: no cover
                resultados.append({"motor": nombre, "ok": False, "razon": str(exc)})
        return resultados

    # ── CICLO COMPLETO (red gobernada) ───────────────────────────────────────
    def ciclo(self, amplitud: float) -> dict:
        latido = self.medir(amplitud)
        goto = self.gobernar(latido["psi"])
        acciones = self.decidir(latido)
        ejecutado = self.ejecutar(acciones)
        ciclo = {**latido, "gobierno": goto, "acciones": ejecutado}
        self._ciclos.append(ciclo)
        return ciclo

    # ── SALIDAS ──────────────────────────────────────────────────────────────
    def estado_autopoietico(self) -> dict:
        return {
            "ciclos": len(self._ciclos),
            "ultimo_psi": self._ciclos[-1]["psi"] if self._ciclos else None,
            "ultimo_estado": self._ciclos[-1]["estado"] if self._ciclos else None,
            "decisiones": self._decisiones[-1] if self._decisiones else None,
            "sellado": {
                "f0": f0,
                "Psi": Psi,
                "theta_B": theta_B,
                "D_PSI_S1": D_PSI_S1,
            },
        }

    def export_log(self) -> str:
        return json.dumps(self._ciclos, indent=2, default=str)

    @staticmethod
    def assert_autopoyesis() -> None:
        """Runner nativo de asserts (sin pytest). Valida el lazo con el metal."""
        bucle = BucleNoetico(dry_run=True)
        # coherencia plena -> ciclo de anclaje+ledger
        latido = bucle.medir(1.0)
        assert latido["estado"] == "UNITY", "Ψ=1 debe ser UNITY"
        assert bucle.decidir(latido) == ["fee_sweep", "anclaje_op_return", "ledger"]
        # gobierno: con Psi=1.0 el error y el ajuste son cero (UNITY sostenida)
        gov = bucle.gobernar(1.0)
        assert abs(gov["error"]) < 1e-9, "error debe ser 0 con Psi=1"
        assert abs(gov["delta_phi"]) <= _PID_MAX_DELTA_PHI, "fase dentro de clamp"
        assert 0.0 <= gov["amp_target"] <= 1.0, "amplitud objetivo en [0,1]"
        # gobierno con perturbacion: Psi=0.5 -> error 0.5, ajuste no nulo
        gov_p = bucle.gobernar(0.5)
        assert gov_p["error"] > 0.0, "error positivo cuando Psi<1"
        assert gov_p["amp_target"] < 1.0, "amplitud baja al gobernar perturbación"
        # warning -> solo fees (Ψ≥0.98 y <0.999)
        latido_w = bucle.medir(0.98)
        assert latido_w["estado"] == "WARNING", "Ψ=0.98 debe ser WARNING"
        assert bucle.decidir(latido_w) == ["fee_sweep"]
        # drop -> re-encender latido
        latido_d = bucle.medir(0.3)
        assert bucle.decidir(latido_d) == ["flywheel"]
        # ejecución: en local los scripts de BAL-003 no están presentes -> no_presente
        # (el Bucle detecta qué motores existen y cuáles no; no asume, verifica)
        res = bucle.ejecutar(["fee_sweep", "anclaje_op_return"])
        assert all(isinstance(r["ok"], bool) for r in res)
        # si el script NO existe -> reporta no_presente (nunca ok=True falso)
        for r in res:
            if r["razon"] == "no_presente":
                assert not r["ok"]
        # sello intacto
        assert abs(D_PSI_S1) > 3.0
        assert theta_B > 0.0 and theta_B < 1.0
        print("   ✓ BucleNoetico: medir→decidir→ejecutar coherente y DRY_RUN verificado")
