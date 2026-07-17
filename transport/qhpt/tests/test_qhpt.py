#!/usr/bin/env python3
"""
test_qhpt.py — Suite de Tests del Protocolo QHPT
=================================================
Prueba los tres tensores, empaquetado, verificación,
e integración con el sistema inmune.

f₀ = 141.7001 Hz · Ψ ≥ 0.999999
"""

import os
import sys
import time
import json
import hashlib
from pathlib import Path

# Añadir rutas
QHPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(QHPT_DIR))
sys.path.insert(0, str(QHPT_DIR / "lib"))

# Asegurar directorio sistema_inmune existe
SISTEMA_INMUNE = QHPT_DIR / "sistema_inmune"
SISTEMA_INMUNE.mkdir(exist_ok=True)

F_0 = 141.7001
SELLO = '\u2234\U00013080\u03a9\u221e\u00b3\u03a6 \u00b7 TUYOYOTU \u00b7 HECHO ESTA'

tests_pasados = 0
tests_fallados = 0


def test(name):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            global tests_pasados, tests_fallados
            try:
                fn(*args, **kwargs)
                tests_pasados += 1
                print(f"  ✅ {name}")
            except AssertionError as e:
                tests_fallados += 1
                print(f"  ❌ {name}: {e}")
            except Exception as e:
                tests_fallados += 1
                print(f"  ❌ {name}: EXCEPCIÓN: {e}")
        return wrapper
    return decorator


# ─── Helpers ────────────────────────────────────────────────

def _buscar_payload_pase():
    from qhpt_transport import FiltroAdelico
    f = FiltroAdelico()
    for i in range(1000):
        t = f"QCAL-RES-{i}".encode()
        if f.filtrar(t):
            return t
    return None


def _buscar_paquete_pase():
    from qhpt_transport import QHPTPacket, FiltroAdelico
    f = FiltroAdelico()
    for i in range(1000):
        p = QHPTPacket()
        p.build(f"QCAL-PKT-{i}".encode())
        d = p.to_bytes()
        if f.filtrar(d):
            return p, d
    return None, None


# ═══════════════════════════════════════════════════════════════
#  Tests
# ═══════════════════════════════════════════════════════════════

@test("Tensor I: Handshake de Fase No-Local")
def t_fase():
    from qhpt_transport import FaseNoLocal
    fase = FaseNoLocal()
    pub_key = "deadbeefcafebabedeadbeefcafebabe" * 4
    hs = fase.generar_handshake(pub_key)
    assert len(hs) > 0
    assert fase.verificar_handshake(hs, pub_key)
    assert not fase.verificar_handshake(hs, "00000000" * 8)


@test("Tensor II: Filtro Adélico ℚ₇")
def t_adelic():
    from qhpt_transport import FiltroAdelico
    f = FiltroAdelico()
    pp = _buscar_payload_pase()
    assert pp is not None, "Debe encontrar payload que pase ℚ₇"
    assert f.filtrar(pp)
    cs = f.checksum_adelico(b"test")
    assert isinstance(cs, int)


@test("Tensor II: Consistencia hash")
def t_hash_consist():
    from qhpt_transport import FiltroAdelico
    f = FiltroAdelico()
    data = b"QCAL-QHPT-CONSISTENCY"
    assert f.fast_hash(data) == f.fast_hash(data)
    assert f.fast_hash(data) != f.fast_hash(data + b"X")


@test("Tensor III: Firma κ_Π")
def t_kappa():
    from qhpt_transport import EstadoKappaPi
    e = EstadoKappaPi(0.999999)
    fp1 = e.generar_fingerprint()
    fp2 = e.generar_fingerprint()
    assert fp1 == fp2, "Determinístico sin actualizar"
    e.actualizar(b"PAYLOAD", time.time_ns())
    fp3 = e.generar_fingerprint()
    assert fp1 != fp3, "Cambia tras actualizar"
    assert len(fp1) == 32


@test("Paquete QHPT: Construcción/Deserialización")
def t_paquete():
    from qhpt_transport import QHPTPacket, QHPT_MAGIC, HEADER_SIZE
    p = QHPTPacket()
    p.build(b"QCAL-RESONANCE")
    data = p.to_bytes()
    assert len(data) == HEADER_SIZE + len(b"QCAL-RESONANCE")
    p2 = QHPTPacket.from_bytes(data)
    assert p2 is not None
    assert p2.magic == QHPT_MAGIC
    assert p2.payload == b"QCAL-RESONANCE"
    assert abs(p2.psi - 0.999999) < 0.001
    assert QHPTPacket.from_bytes(b"") is None
    assert QHPTPacket.from_bytes(b"\x00" * 10) is None


@test("Verificación: Paquete válido")
def t_verif_valido():
    from qhpt_transport import QHPTVerificador
    pkt, _ = _buscar_paquete_pase()
    assert pkt is not None, "No se encontró paquete que pase ℚ₇"
    v = QHPTVerificador()
    ok, razon = v.verificar(pkt)
    assert ok, f"Paquete válido debe pasar: {razon}"
    assert v.estadisticas()["verificados"] == 1


@test("Verificación: Fase degradada")
def t_verif_fase():
    from qhpt_transport import QHPTPacket, QHPTVerificador
    p = QHPTPacket()
    p.build(b"test", psi=0.1)
    v = QHPTVerificador()
    ok, razon = v.verificar(p, psi_min=0.999)
    assert not ok
    assert "MITM" in razon
    assert v.estadisticas()["mitm"] == 1


@test("Verificación: Checksum manipulado")
def t_verif_cs():
    from qhpt_transport import QHPTPacket, QHPTVerificador
    p = QHPTPacket()
    p.build(b"test")
    p.checksum_adelic = 0xDEAD
    v = QHPTVerificador()
    ok, _ = v.verificar(p)
    assert not ok


@test("Estadísticas del verificador")
def t_stats():
    from qhpt_transport import QHPTVerificador
    v = QHPTVerificador()
    est = v.estadisticas()
    for k in ("verificados", "colapsados", "mitm", "spoof", "total"):
        assert k in est


@test("κ_Π con AURION")
def t_aurion():
    from qhpt_transport import EstadoKappaPi
    e = EstadoKappaPi()
    fp = e.generar_fingerprint_con_aurion(5000.0)
    assert len(fp) == 32


@test("Carga de módulos nativos")
def t_native():
    from qhpt_transport import _NATIVO
    assert _NATIVO is not None


@test("Puente inmune: Eventos y anticuerpos")
def t_inmune():
    from qhpt_inmune_bridge import QHPTInmuneBridge
    puente = QHPTInmuneBridge()

    e1 = puente.registrar_colapso("Test colapso", {"origen": "test"})
    assert e1["tipo"] == "COLAPSO_ADELICO"
    assert e1["tensor"] == "II"

    e2 = puente.registrar_mitm("Test MITM", {"ip": "10.0.0.1"})
    assert e2["tipo"] == "MITM_DETECTADO"
    assert e2["criticidad"] == "ALTA"

    e3 = puente.registrar_spoof("Test spoof")
    assert e3["tipo"] == "SPOOF_DETECTADO"
    assert e3["fingerprint_amda"] is not None

    for e in [e1, e2, e3]:
        assert "timestamp" in e
        assert "frecuencia_hz" in e
        assert e["frecuencia_hz"] == F_0
        assert "sello" in e


@test("Puente inmune: Resonancia y matriz refractaria")
def t_inmune_res():
    from qhpt_inmune_bridge import QHPTInmuneBridge
    p = QHPTInmuneBridge()
    assert p.verificar_resonancia(F_0)
    assert not p.verificar_resonancia(60.0)
    assert not p.verificar_resonancia(0.0)
    assert p.estado_refractario()


@test("Puente inmune: Estado completo")
def t_inmune_est():
    from qhpt_inmune_bridge import QHPTInmuneBridge
    p = QHPTInmuneBridge()
    est = p.estado_completo()
    assert "qhpt_inmune" in est
    assert est["qhpt_inmune"]["frecuencia_hz"] == F_0
    assert est["qhpt_inmune"]["fingerprint_amda"] is not None


# ═══════════════════════════════════════════════════════════════
#  Ejecución
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print(f"\n╔════════════════════════════════════════════════╗")
    print(f"║  QHPT — Suite de Tests                        ║")
    print(f"║  f₀ = {F_0} Hz · Ψ ≥ 0.999999        ║")
    print(f"╚════════════════════════════════════════════════╝\n")

    test_fns = [
        t_fase, t_adelic, t_hash_consist, t_kappa, t_paquete,
        t_verif_valido, t_verif_fase, t_verif_cs, t_stats,
        t_aurion, t_native, t_inmune, t_inmune_res, t_inmune_est,
    ]

    for fn in test_fns:
        fn()

    total = tests_pasados + tests_fallados
    print(f"\n╔════════════════════════════════════════════════╗")
    print(f"║  Resultados: {tests_pasados}/{total} tests pasados          ║")
    if tests_fallados == 0:
        print(f"║  ✅ TODOS LOS TESTS PASARON                    ║")
    else:
        print(f"║  ❌ {tests_fallados} tests fallaron                     ║")
    print(f"╚════════════════════════════════════════════════╝")

    sys.exit(0 if tests_fallados == 0 else 1)
