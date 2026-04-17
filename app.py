# -*- coding: utf-8 -*-
"""Streamlit dashboard for QCAL MCP resonance checks."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, Optional

import pandas as pd
import requests
import streamlit as st

import mcp_network.resonance as qcal_resonance

MCP_URL = "http://127.0.0.1:8506/jsonrpc"
NODES = ["auron-governor", "141-hz", "interferometro-noesico", "biologia-cuantica-noesica"]

st.set_page_config(page_title="QCAL ∞³ Dashboard", layout="wide")
st.title("🌀 QCAL-SYMBIO-BRIDGE v1.0.1 — MCP Network Resonance")

with st.sidebar:
    st.header("Controles Globales")
    real_mode = st.checkbox("🔬 Activar Modo Real (datos físicos)", value=False)

    if real_mode:
        os.environ["QCAL_REAL_TESTS"] = "1"
        st.success("✅ Modo Real activado — Observadores físicos cargados")
    else:
        os.environ.pop("QCAL_REAL_TESTS", None)

    refresh = st.button("Actualizar Resonancia")


def get_resonance(node: str) -> Optional[Dict]:
    try:
        response = requests.post(
            MCP_URL,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "network.checkResonance",
                "params": {"node": node},
            },
            timeout=5,
        )
        if response.status_code == 200:
            payload = response.json()
            if "result" in payload:
                return payload["result"]
    except Exception:
        return qcal_resonance.check_node_resonance(node)

    return qcal_resonance.check_node_resonance(node)


if "psi_history" not in st.session_state:
    st.session_state.psi_history = {node: [] for node in NODES}
if "timeline" not in st.session_state:
    st.session_state.timeline = []

st.subheader("Estado de Resonancia de los 4 Nodos")
cols = st.columns(4)
current_results = {}

for idx, node in enumerate(NODES):
    with cols[idx]:
        data = get_resonance(node)
        current_results[node] = data
        if data:
            status_emoji = "🟢" if data["status"] == "pass" else "🟡" if data["status"] == "warn" else "🔴"
            st.markdown(f"### {status_emoji} **{node}**")
            st.metric("Ψ Coherencia", f"{data['psi']:.6f}")
            st.metric("Resonancia", data["resonance"])
            st.metric("Frecuencia", f"{data['frequency_hz']} Hz")
            st.metric("Latencia", f"{data['latency_ms']} ms")

            with st.expander("Detalles QCAL", expanded=False):
                st.json(data["qcal"], expanded=False)

            if data["qcal"].get("modo_real"):
                st.caption("📡 Fuente: Datos físicos reales")
            else:
                st.caption("🔬 Modo simulación")
        else:
            st.error(f"No se pudo obtener datos de {node}")

if refresh or not st.session_state.timeline:
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.timeline.append(timestamp)
    st.session_state.timeline = st.session_state.timeline[-120:]
    for node in NODES:
        psi = current_results.get(node, {}).get("psi") if current_results.get(node) else None
        if psi is not None:
            st.session_state.psi_history[node].append(psi)
            st.session_state.psi_history[node] = st.session_state.psi_history[node][-120:]

st.subheader("Evolución temporal de Ψ")
if st.session_state.timeline:
    psi_df = pd.DataFrame(
        {node: st.session_state.psi_history[node] for node in NODES},
        index=st.session_state.timeline[-len(st.session_state.psi_history[NODES[0]]):],
    )
    st.line_chart(psi_df)
else:
    st.info("Pulsa 'Actualizar Resonancia' para iniciar la serie temporal de Ψ.")

st.caption(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | ∴𓂀Ω∞³")
