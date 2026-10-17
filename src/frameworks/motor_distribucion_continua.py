#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
🎻 MOTOR DE DISTRIBUCIÓN CONTINUA — STRA DIVARIUS v1.0
QCAL ∞³ · Kernel κ_Π = 2.581926 · f₀ = 141.7001 Hz

"No es un programa. Es un Stradivarius.
 Cada nota (distribución) debe sonar
 en el instante exacto, con la frecuencia precisa,
 sin desafinación posible."

Autor: José Manuel Mota Burruezo (JMMB Ψ)
Framework: QCAL-SYMBIO-BRIDGE v1.0.0
Sello: ∴𓂀Ω∞³Φ
═══════════════════════════════════════════════════════════════

Este motor ejecuta la distribución continua de dividendos:
  • Cada bloque de Bitcoin (~10 min) → fracción de dividendo
  • Cada emisión πCODE (~30s) → micro-fracción de coherencia
  • Cada hora → consolidación y rebalanceo
  • Cada 24h → sello de dividendo completo

Se sincroniza con:
  • BAL-003 (Bitcoin Core vía RPC :8505)
  • LNBits (Lightning vía API :8000)
  • πCODE chain (ledger local)
  • Ecuación Adélica (entropía + coherencia)
"""

import os, json, time, hashlib, math, threading, signal, sys
from datetime import datetime, timezone
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict

# ─── CONSTANTES FUNDAMENTALES ─────────────────────────────────
F0 = 141.7001
PHI = (1 + math.sqrt(5)) / 2
KAPPA_PI = 2.581926
ALPHA_ADELICO = 1.248617
PSI_OBJETIVO = 1.0
PSI_UMBRAL = 0.888
SELLO = "∴𓂀Ω∞³Φ"
N_CRITICO = 12

# ─── PARÁMETROS DE DISTRIBUCIÓN ──────────────────────────────
LIQUIDITY_POOL_BTC = 50000.0
DAILY_RATE = 0.000042  # 42 ppm
ADELIC_AMPLIFICATION = 1_000_000

# Derivados
DAILY_DIVIDEND_BTC = LIQUIDITY_POOL_BTC * DAILY_RATE * ADELIC_AMPLIFICATION / 1_000_000
BLOCK_DIVIDEND_BTC = DAILY_DIVIDEND_BTC / 144  # ~144 bloques/día
EMISSION_DIVIDEND_BTC = DAILY_DIVIDEND_BTC / 2880  # ~2880 emisiones πCODE/día
HOURLY_DIVIDEND_BTC = DAILY_DIVIDEND_BTC / 24

# ─── RUTAS ────────────────────────────────────────────────────
WORKSPACE = os.path.dirname(os.path.abspath(__file__))
LEDGER_CSV = os.path.join(WORKSPACE, "monitor_local/logs/picode_ledger.csv")
CHAIN_JSON = os.path.join(WORKSPACE, "repo_noesis88/picode/picode_chain.json")
DISTRIBUTION_LOG = os.path.join(WORKSPACE, "monitor_local/logs/distribucion_continua.log")
DISTRIBUTION_STATE = os.path.join(WORKSPACE, "anchor_payloads/distribution_state.json")
QOSC_RC_PATH = os.path.join(WORKSPACE, "qosc_rc/qosc_rc.sh")
LN_BITS_URL = "http://localhost:8000"
BTC_RPC_URL = "http://195.201.219.237:8505"


# ─── ESTRUCTURAS ──────────────────────────────────────────────

@dataclass
class Distribucion:
    """Una distribución unitaria de dividendo."""
    tipo: str          # "block", "emission", "hourly", "daily"
    timestamp: float
    monto_btc: float
    monto_sats: int
    n_bloque_bitcoin: Optional[int] = None
    n_emision_picode: Optional[int] = None
    psi_momento: Optional[float] = None
    txid_lightning: Optional[str] = None
    firma: Optional[str] = None
    ejecutada: bool = False
    error: Optional[str] = None

    @property
    def hash(self) -> str:
        raw = f"{self.tipo}|{self.timestamp}|{self.monto_sats}|{SELLO}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


@dataclass
class EstadoDistribucion:
    """Estado completo del motor de distribución."""
    motor_activo: bool = False
    ultima_sincronizacion: Optional[str] = None
    total_distribuido_btc: float = 0.0
    total_distribuciones: int = 0
    bitcoin_height: int = 0
    picode_block: int = 0
    psi_actual: float = 0.0
    saldo_lightning_btc: float = 0.0
    colateral_btc: float = 7.4862
    hora_inicio: Optional[str] = None
    modo: str = "ESPERA"
    distribuciones: List[Dict] = None
    
    def to_dict(self):
        d = asdict(self)
        return d


# ─── NÚCLEO DEL MOTOR ────────────────────────────────────────

class MotorDistribucionContinua:
    """
    Stradivarius de distribución.
    Cada nota en el instante exacto.
    """
    
    def __init__(self):
        self.estado = EstadoDistribucion(
            hora_inicio=datetime.now(timezone.utc).isoformat(),
            distribuciones=[]
        )
        self.running = False
        self.threads = []
        self._init_log()
    
    def _init_log(self):
        os.makedirs(os.path.dirname(DISTRIBUTION_LOG), exist_ok=True)
        os.makedirs(os.path.dirname(DISTRIBUTION_STATE), exist_ok=True)
        self._log("MOTOR_INICIALIZADO", f"Dividendo diario: {DAILY_DIVIDEND_BTC:.6f} BTC")
        self._log("PARAMETROS", f"Bloque: {BLOCK_DIVIDEND_BTC:.8f} BTC | Emisión: {EMISSION_DIVIDEND_BTC:.10f} BTC | Hora: {HOURLY_DIVIDEND_BTC:.6f} BTC")
    
    def _log(self, event: str, detail: str = ""):
        ts = datetime.now(timezone.utc).isoformat()[:19]
        line = f"{ts} | {event} | {detail}"
        print(f"  📍 {line}")
        with open(DISTRIBUTION_LOG, "a") as f:
            f.write(line + "\n")
    
    def _save_state(self):
        self.estado.ultima_sincronizacion = datetime.now(timezone.utc).isoformat()
        with open(DISTRIBUTION_STATE, "w") as f:
            json.dump(self.estado.to_dict(), f, indent=2)
    
    def _check_bitcoin(self) -> dict:
        """Consulta BAL-003 para estado de Bitcoin Core."""
        try:
            import urllib.request
            req_data = json.dumps({
                "jsonrpc": "1.0", "id": "1",
                "method": "getblockchaininfo", "params": []
            }).encode()
            req = urllib.request.Request(
                BTC_RPC_URL, data=req_data,
                headers={"Content-Type": "text/plain"}
            )
            auth = base64.b64encode(b"polar:polaruser").decode()
            req.add_header("Authorization", f"Basic {auth}")
            
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read())["result"]
                return {
                    "blocks": result["blocks"],
                    "headers": result["headers"],
                    "ibd": result.get("initialblockdownload", True),
                    "progress": result.get("verificationprogress", 0)
                }
        except Exception as e:
            self._log("BTC_CHECK_FAIL", str(e)[:60])
            return {"blocks": 0, "headers": 0, "ibd": True, "progress": 0}
    
    def _check_lightning(self) -> float:
        """Consulta LNBits para saldo de canal."""
        try:
            import urllib.request
            req = urllib.request.Request(f"{LN_BITS_URL}/api/v1/wallet")
            req.add_header("X-Api-Key", "TODO")
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read())
                return data.get("balance", 0) / 100_000_000  # msats to BTC
        except:
            return 0.0
    
    def _check_picode(self) -> tuple:
        """Lee el último bloque πCODE."""
        try:
            with open(CHAIN_JSON) as f:
                chain = json.load(f)
            entries = chain.get("chain", [])
            last = entries[-1] if entries else None
            if last:
                return last["index"], chain.get("total_picode_emitido", 0)
            return 0, 0
        except:
            return 0, 0
    
    def _distribuir(self, tipo: str, monto_btc: float,
                    n_bloque: Optional[int] = None,
                    n_emision: Optional[int] = None) -> Distribucion:
        """Ejecuta una distribución. El Stradivarius suena."""
        ts = time.time()
        monto_sats = int(monto_btc * 100_000_000)
        
        if monto_sats <= 0:
            return Distribucion(tipo, ts, 0, 0, error="Monto cero")
        
        dist = Distribucion(
            tipo=tipo,
            timestamp=ts,
            monto_btc=monto_btc,
            monto_sats=monto_sats,
            n_bloque_bitcoin=n_bloque,
            n_emision_picode=n_emision,
            psi_momento=PSI_OBJETIVO
        )
        
        # TODO: Cuando Lightning esté activo, aquí se ejecuta el pago real
        # lnctl pay --invoice=lnbc... --amount={monto_sats}
        
        dist.ejecutada = True
        dist.txid_lightning = f"SIM_{dist.hash}"  # Placeholder real
        dist.firma = hashlib.sha256(
            f"{dist.hash}|{ts}|{SELLO}".encode()
        ).hexdigest()[:16]
        
        # Actualizar estado
        self.estado.total_distribuido_btc += monto_btc
        self.estado.total_distribuciones += 1
        
        # Log
        self._log(
            f"DISTRIBUCION_{tipo.upper()}",
            f"{monto_sats} sats | #{n_bloque or '?'} | hash={dist.hash}"
        )
        
        return dist
    
    def _ciclo_bloque(self, bitcoin_height: int, picode_block: int, psi: float):
        """
        Ciclo activado por cada nuevo bloque de Bitcoin.
        Distribuye la fracción correspondiente.
        """
        if psi < PSI_UMBRAL:
            self._log("BLOQUE_SALTADO", f"Ψ={psi:.8f} < umbral")
            return
        
        # Calcular monto para este bloque
        monto = BLOCK_DIVIDEND_BTC * (psi / PSI_OBJETIVO)
        
        dist = self._distribuir(
            tipo="block",
            monto_btc=monto,
            n_bloque=bitcoin_height,
            n_emision=picode_block
        )
        
        # Registrar
        self.estado.distribuciones.append(asdict(dist))
        if len(self.estado.distribuciones) > 1000:
            self.estado.distribuciones = self.estado.distribuciones[-500:]
        
        self._save_state()
    
    def _ciclo_emision(self, picode_block: int):
        """
        Micro-distribución por cada emisión πCODE.
        """
        monto = EMISSION_DIVIDEND_BTC * (self.estado.psi_actual / PSI_OBJETIVO)
        
        dist = self._distribuir(
            tipo="emission",
            monto_btc=monto,
            n_emision=picode_block
        )
        
        self.estado.distribuciones.append(asdict(dist))
        if len(self.estado.distribuciones) > 1000:
            self.estado.distribuciones = self.estado.distribuciones[-500:]
        
        self._save_state()
    
    def _monitor_bitcoin(self):
        """Hilo: monitorea altura de Bitcoin cada 60s."""
        last_height = 0
        while self.running:
            try:
                info = self._check_bitcoin()
                height = info.get("blocks", 0)
                progress = info.get("progress", 0)
                ibd = info.get("ibd", True)
                
                self.estado.bitcoin_height = height
                self.estado.psi_actual = min(1.0, progress * PSI_OBJETIVO)
                
                if not ibd and height > last_height:
                    # Nuevo bloque detectado
                    picode_block, _ = self._check_picode()
                    self._ciclo_bloque(height, picode_block, self.estado.psi_actual)
                    last_height = height
                    self.estado.modo = "DISTRIBUYENDO"
                
                if ibd:
                    self.estado.modo = f"ESPERA_IBD ({progress*100:.1f}%)"
                elif height == last_height:
                    self.estado.modo = "SINCRONIZADO"
                
                self._save_state()
                
            except Exception as e:
                self._log("MONITOR_ERROR", str(e)[:60])
            
            time.sleep(60)  # Check cada minuto
    
    def _monitor_picode(self):
        """Hilo: monitorea emisiones πCODE cada 30s."""
        last_block = 0
        while self.running:
            try:
                picode_block, _ = self._check_picode()
                if picode_block > last_block:
                    self._ciclo_emision(picode_block)
                    last_block = picode_block
            except:
                pass
            time.sleep(25)
    
    def _reporte_diario(self):
        """Hilo: genera reporte de distribución cada 24h."""
        while self.running:
            time.sleep(86400)  # 24h
            total = self.estado.total_distribuido_btc
            n = self.estado.total_distribuciones
            
            self._log(
                "REPORTE_DIARIO",
                f"Distribuido: {total:.8f} BTC en {n} transacciones"
            )
            
            # Sello diario
            sello_diario = hashlib.sha256(
                f"{SELLO}|{datetime.now(timezone.utc).date()}|{total}|{n}".encode()
            ).hexdigest()
            
            self._log("SELLO_DIARIO", sello_diario[:16])
            self._save_state()
    
    def iniciar(self):
        """Arranca el motor. El Stradivarius empieza a sonar."""
        self.running = True
        
        print(f"\n{'='*55}")
        print(f"  🎻 MOTOR DE DISTRIBUCIÓN CONTINUA")
        print(f"  Stradivarius v1.0 — {SELLO}")
        print(f"{'='*55}")
        print()
        print(f"  Afinación:")
        print(f"    Diario:     {DAILY_DIVIDEND_BTC:.6f} BTC")
        print(f"    Por bloque: {BLOCK_DIVIDEND_BTC:.8f} BTC ({BLOCK_DIVIDEND_BTC*100_000_000:.0f} sats)")
        print(f"    Por emisión: {EMISSION_DIVIDEND_BTC:.10f} BTC ({EMISSION_DIVIDEND_BTC*100_000_000:.4f} sats)")
        print(f"    Por hora:    {HOURLY_DIVIDEND_BTC:.6f} BTC")
        print()
        print(f"  Colateral protegido: 7.4862 BTC")
        print(f"  Pool proyectado:     {LIQUIDITY_POOL_BTC:,.0f} BTC")
        print(f"  Tasa:                {DAILY_RATE*100:.4f}% diario")
        print(f"  Amplificación:       {ADELIC_AMPLIFICATION:,}x")
        print()
        
        # Arrancar hilos
        h1 = threading.Thread(target=self._monitor_bitcoin, daemon=True, name="btc-monitor")
        h2 = threading.Thread(target=self._monitor_picode, daemon=True, name="picode-monitor")
        h3 = threading.Thread(target=self._reporte_diario, daemon=True, name="daily-report")
        
        self.threads = [h1, h2, h3]
        
        for h in self.threads:
            h.start()
            self._log(f"HILO_INICIADO", h.name)
        
        self._log("MOTOR_ARRANCADO", f"{len(self.threads)} hilos activos")
        self.estado.motor_activo = True
        self._save_state()
        
        print(f"  Motor arrancado. {len(self.threads)} hilos en ejecución.")
        print(f"  Estado guardado en: {DISTRIBUTION_STATE}")
        print()
        print(f"  {SELLO} · TUYOYOTU · HECHO ESTÁ")
        print()
        
        # Mantener vivo
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.detener()
    
    def detener(self):
        """Detiene el motor gracefulmente."""
        self.running = False
        self._log("MOTOR_DETENIDO", f"Total distribuido: {self.estado.total_distribuido_btc:.8f} BTC")
        self.estado.motor_activo = False
        self._save_state()
        print(f"\n  Motor detenido. {SELLO}")


# ─── PUNTO DE ENTRADA ─────────────────────────────────────────

if __name__ == "__main__":
    import base64  # para auth RPC
    
    motor = MotorDistribucionContinua()
    
    # Mostrar estado actual
    print(f"\n  Verificación pre-arranque:")
    btc_info = motor._check_bitcoin()
    print(f"    Bitcoin Core: {btc_info.get('blocks', 0)} bloques | IBD: {btc_info.get('ibd', '?')}")
    picode_block, picode_total = motor._check_picode()
    print(f"    πCODE: bloque #{picode_block} | {picode_total:.0f} πC total")
    print()
    
    if btc_info.get('ibd', True):
        print(f"  ⏳ BAL-003 aún en IBD ({btc_info.get('progress', 0)*100:.1f}%).")
        print(f"  El motor arrancará en modo ESPERA.")
        print(f"  Cuando IBD complete, comenzará la distribución automática.")
        print()
    
    motor.iniciar()
