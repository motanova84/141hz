#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
real_phase_emitter_perpetuo.py — EMISOR I/Q PERPETUO (Palma → BAL-003:8444).
Ronda 2 · Directiva del Director (02:47 GMT+2): activación perpetua.
  - Oscilador Noesis f₀=141.7001 Hz en cuadratura: I=cos(2πf₀t+Φ_pleroma), Q=sin(...).
  - Φ_pleroma(t) = θ_B·sin(ω_drift·t), diferenciable, sin pliego mod 2π.
  - Bucle infinito while True con auto-reconnect ante SSLEOFError / ventana del daemon
    (espera 1s) SIN perder el histórico del NCO (acumulador de fase remoto vive en el medidor).
  - Muestreo holgado dt (por defecto 5.0s, configurable >5s) para eliminar saturación TCP.
  - Persistencia: el estado local se guarda en json entre arranques del daemon.
"""
import argparse, json, math, os, socket, ssl, time

F0     = 141.7001
THETA_B = 0.07074774995428558
SEED_W = 2.0 * math.pi * 0.0001
STATE_F = "/opt/templo_core/.iq_emitter_state.json"

def save_state(t0, cycle, total):
    try: json.dump({"t0":t0,"cycle":cycle,"total":total}, open(STATE_F,"w"))
    except Exception: pass

def fresh_connect(host, port, ctx):
    c = ctx.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=host)
    c.connect((host, port))
    c.settimeout(9)
    return c

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8444)
    ap.add_argument("--dt", type=float, default=5.0)     # holgado: >5s si se pide
    ap.add_argument("--max", type=int, default=0)        # 0 = perpetuo
    a = ap.parse_args()

    ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE

    # hot-init: retomar t0 si existe (continúa la fase, no reinicia la coherencia temporal)
    t0 = time.time(); cycle = 0
    if os.path.exists(STATE_F):
        try:
            st = json.load(open(STATE_F))
            if st.get("t0"): t0 = st["t0"]; cycle = st.get("cycle",0)
        except Exception: pass

    print(f"🔮 EMISOR I/Q PERPETUO → {a.host}:{a.port} · f₀={F0} Hz · dt={a.dt}s · perpetuo={a.max==0}", flush=True)
    print(f"   oscilador Noesis real · Φ_pleroma=θ_B·sin(ω_drift·t) · NO sonda", flush=True)
    print("-"*72, flush=True)

    last = time.time(); total = cycle
    while True:
        try:
            conn = fresh_connect(a.host, a.port, ctx)
            print(f"── conectado (latido {total+1})", flush=True)
            while True:
                try:
                    if a.max and total >= a.max: conn.close(); print("límite alcanzado",flush=True); return
                    tout = time.time() >= last + a.dt
                    if tout:
                        ts = time.time(); elapsed = ts - t0
                        carrier = 2.0*math.pi*F0*elapsed
                        pleroma = THETA_B*math.sin(SEED_W*elapsed)
                        phi_c = carrier + pleroma
                        msg = {"cycle":total+1,"timestamp_us":int(ts*1e6),"f0":F0,
                               "I":math.cos(phi_c),"Q":math.sin(phi_c),"phi_cont":phi_c,
                               "probe":False}
                        conn.sendall(json.dumps(msg).encode())
                        try: conn.recv(4096)
                        except Exception: pass
                        total += 1
                        if total % 10 == 0:
                            print(f"  [{total}] I={msg['I']:+.6f} Q={msg['Q']:+.6f} rev={phi_c/(2*math.pi):.1f}", flush=True)
                            save_state(t0, total, total)
                        last = time.time()
                    time.sleep(0.2)
                except (ssl.SSLEOFError, ConnectionError, BrokenPipeError, socket.timeout):
                    raise
        except (ssl.SSLEOFError, ConnectionError, BrokenPipeError, socket.timeout, OSError) as e:
            print(f"  socket cerrado ({e!r}) — reconexión en 1s, coherencia preservada", flush=True)
            try: conn.close()
            except Exception: pass
            time.sleep(1)

if __name__ == "__main__":
    main()
