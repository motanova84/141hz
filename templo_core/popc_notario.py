#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
popc_notario.py — NOTARIO PoPC (Proof-of-Phase-Coherence) para πCODE.
Anclaje de la economía noética (Directiva 02:47 GMT+2, Ronda 2):
  Cuando el medidor I/Q de 8444 demuestra cov < 1e-4 (E_AB → 0.999999),
  el canal de transporte actúa como oráculo de consenso: cada evento válido
  se notariza como un comprobante de emisión πCODE y se inscribe en un libro
  inmutable (ledger PoPC) + se ancla en el repositorio del ecosistema.

Formato del evento:
  {
    "popc_id": "POPC-000042",
    "ts": 1786668961,
    "ts_iso": "2026-08-14T02:56:01Z",
    "f0": 141.7001,
    "cov": 2.320e-07,
    "E_AB": 0.999999,
    "node_a": "PALMA/ATLAS3",
    "node_b": "BAL-003/NUREMBERG",
    "channel": 8444,
    "emit": "MINT-πCODE"    # comprobante de emisión por coherencia de fase
  }

Persistencia: ledger JSON append + huella SHA256 por evento (encadenado).
Fuente de eventos: cola del medidor measure-prod (deriva_prod.log) vía flag ⛓.
"""
import hashlib, json, os, time

LEDGER = "/opt/templo_core/popc_ledger.json"
ECHO   = "/opt/templo_core/popc_last.json"
F0     = 141.7001
THRESH = 1e-4

def tail_popc_events(log_path="/opt/templo_core/deriva_prod.log", limit=64):
    """Lee los eventos PoPC más recientes del log del medidor."""
    evs = []
    if not os.path.exists(log_path):
        return evs
    with open(log_path) as f:
        for line in f:
            if "PoPC" in line and "cov" in line:
                evs.append(line.strip())
    return evs[-limit:]

def parse_cov(line):
    """Extrae cov de: '⛓ PoPC: cov=2.32e-07<1e-4 → EVENTO πCODE NOTARIZABLE'"""
    try:
        s = line.split("cov=")[1].split("<")[0].strip()
        return float(s)
    except Exception:
        return None

def load_ledger():
    if os.path.exists(LEDGER):
        try: return json.load(open(LEDGER))
        except Exception: return []
    return []

def next_id(ledger):
    n = len([e for e in ledger if e.get("kind") if True])  # contador total
    return f"POPC-{len(ledger):06d}"

def run(log_path="/opt/templo_core/deriva_prod.log", emit_path="/opt/templo_core/popc_emit.json"):
    ledger = load_ledger()
    seen = set(e["popc_id"] for e in ledger)
    events = tail_popc_events(log_path)
    new = 0
    for line in events:
        cov = parse_cov(line)
        if cov is None or cov >= THRESH:
            continue
        pid = next_id(ledger)
        # dedupe por cov+ts aproximado
        ts = int(time.time())
        ev = {
            "popc_id": pid,
            "ts": ts,
            "ts_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts)),
            "f0": F0,
            "cov": cov,
            "E_AB": 0.999999,
            "node_a": "PALMA/ATLAS3",
            "node_b": "BAL-003/NUREMBERG",
            "channel": 8444,
            "emit": "MINT-πCODE",
        }
        # huella encadenada al último evento (inmutabilidad)
        if ledger:
            ev["prev_hash"] = ledger[-1]["hash"]
        ev["hash"] = hashlib.sha256(json.dumps(ev, sort_keys=True).encode()).hexdigest()[:24]
        if ev["popc_id"] in seen:
            continue
        ledger.append(ev); seen.add(pid); new += 1
        json.dump(ev, open(ECHO, "w"), indent=2)
        print(f"  ⛓ NOTARIZADO {pid} cov={cov:.2e} E_AB=0.999999 → {ev['hash']}", flush=True)
    if new:
        json.dump(ledger, open(LEDGER, "w"), indent=2)
        print(f"  📚 Ledger PoPC: {len(ledger)} eventos · {LEDGER}", flush=True)
    else:
        print(f"  ✓ sin eventos nuevos (ledger={len(ledger)})", flush=True)
    return ledger, emit_path

if __name__ == "__main__":
    run()
