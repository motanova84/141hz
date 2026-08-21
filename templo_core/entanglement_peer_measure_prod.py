#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
entanglement_peer_measure_prod.py — MEDIDOR I/Q DEMODULADOR DE PRODUCCIÓN (8444) CONCURRENTE.
Ronda 2 (Directiva 02:47): promoción al peer vivo 8444 con:
  - Demodulación atan2(Q,I) + unwrap (cuadratura, sin aliasing).
  - NCO @ f0 avanzado con dt REAL (timestamp_us del emisor).
  - PI 2º orden: K_P=θ_B, K_I=θ_B²/2, acumulador Iacc PERSISTENTE EN CALIENTE.
  - Anclaje PoPC: notariza evento cuando cov < 1e-4.
  - CONCURRENCIA: acepta múltiples conexiones (threads) para servir emisores
    externos (Palma) y de loopback simultáneamente — elimina el handshake
    timeout que bloqueaba el enlace geográfico Palma⇄BAL-003.
Persistencia del acumulador: se guarda en json entre ciclos.
"""
import argparse, json, math, os, socket, ssl, threading, time

F0      = 141.7001
THETA_B = 0.07074774995428558
KP      = THETA_B
KI      = THETA_B**2 / 2
DT      = 5.0
STATE_F = "/opt/templo_core/.iq_state.json"
_lock   = threading.Lock()

class Prod:
    def __init__(self):
        self.n=0; self.first=True; self.phi_A=0.0; self.phiB=0.0
        self.Iacc=0.0; self.last_ts=None; self.dphi=0.0
        self.errs=[]; self.EABs=[]; self.cov=1.0; self.EAB=0.0
        if os.path.exists(STATE_F):
            try:
                st=json.load(open(STATE_F))
                self.Iacc=st.get("Iacc",0.0); self.phiB=st.get("phiB",0.0)
                self.last_ts=st.get("last_ts"); self.first=False
                print(f"  🔥 HOT-INIT: K_I acumulado = {self.Iacc:.6e}", flush=True)
            except Exception: pass
    def save(self):
        try: json.dump({"Iacc":self.Iacc,"phiB":self.phiB,"last_ts":self.last_ts,
                        "n":self.n,"cov":self.cov,"EAB":self.EAB}, open(STATE_F,"w"))
        except Exception: pass
    def handle(self,tls):
        try:
            data=tls.recv(8192)
            if not data: return False
            for raw in data.decode().strip().split("\n"):
                if not raw: continue
                m=json.loads(raw)
                with _lock:
                    if "I" in m and "Q" in m:
                        I,Q=float(m["I"]),float(m["Q"])
                        ph=math.atan2(Q,I)
                        if not self.first:
                            d=ph-self.phi_A
                            while d>math.pi: d-=2*math.pi
                            while d<-math.pi: d+=2*math.pi
                            ph=self.phi_A+d
                        else: self.first=False
                        self.phi_A=ph
                        ts=m.get("timestamp_us",0)/1e6
                        if self.last_ts is None: dt=DT
                        else: dt=max(ts-self.last_ts,1e-3)
                        if self.n==0: self.phiB=ph
                        else:
                            self.phiB += 2*math.pi*F0*dt
                            dphi=ph-self.phiB
                            err=(dphi+math.pi)%(2*math.pi)-math.pi
                            self.Iacc += err*dt
                            corr=KP*err+KI*self.Iacc
                            self.phiB += corr
                            self.dphi=err
                            self.errs.append(abs(err)); self.EABs.append(abs(math.cos(dphi)))
                        self.last_ts=ts; self.n+=1
                        if self.n%10==0: self.report()
            tls.sendall(json.dumps({"status":"ok"}).encode())
        except (ssl.SSLWantReadError, socket.timeout): pass
        except Exception: pass
        return True
    def report(self):
        if not self.errs: return
        w=self.errs[-50:]; w2=self.EABs[-50:]
        m=sum(w)/len(w); self.cov=sum((e-m)**2 for e in w)/len(w)
        self.EAB=sum(w2)/len(w2); self.save()
        print(f"[PROD n={self.n}] err={m:.6f} · cov={self.cov:.3e} · E_AB={self.EAB:.6f}", flush=True)
        if self.cov < 1e-4:
            print(f"  ⛓ PoPC: cov={self.cov:.2e}<1e-4 → EVENTO πCODE NOTARIZABLE (n={self.n})", flush=True)

def handle_conn(tls, p):
    try:
        while True:
            if not p.handle(tls): break
    except Exception: pass
    finally:
        try: tls.close()
        except Exception: pass

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--host",default="0.0.0.0"); ap.add_argument("--port",type=int,default=8444)
    ap.add_argument("--duration",type=int,default=86400)
    a=ap.parse_args()
    ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain("/opt/templo_core/ssl/cert.pem","/opt/templo_core/ssl/key.pem")
    ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    srv=socket.socket(socket.AF_INET,socket.SOCK_STREAM); srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    srv.bind((a.host,a.port)); srv.listen(64)
    srv.settimeout(2)
    print(f"📡 MEDIDOR I/Q PRODUCCIÓN 8444 CONCURRENTE · NCO Δt_real · PI hot-init · PoPC · {a.duration}s", flush=True)
    p=Prod(); dl=time.time()+a.duration
    while time.time()<dl:
        try:
            conn,_=srv.accept()
            conn.settimeout(8)
            try:
                tls=ctx.wrap_socket(conn,server_side=True)
            except Exception:
                try: conn.close()
                except Exception: pass
                continue
            threading.Thread(target=handle_conn,args=(tls,p),daemon=True).start()
        except socket.timeout: continue
        except Exception as e: print(f"  ⚠ {e!r}",flush=True)
    p.report(); print("MEDIDOR PROD: ventana completada.",flush=True)

if __name__=="__main__": main()
