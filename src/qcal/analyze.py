from __future__ import annotations
import pathlib, json, math
from dataclasses import dataclass
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class Result:
    catalog: str
    detector: str
    band: float
    mean_snr: float
    n_events: int
    table_path: str
    figure_path: str

def _mock_gwtc1_band_stats(band: float) -> tuple[np.ndarray, float]:
    rng = np.random.default_rng(1417)
    snr = rng.normal(loc=21.38, scale=6.38, size=11)
    return snr, snr.mean()

def analyze_catalog(catalog: str, band: float, detector: str, outdir: str) -> dict:
    outdir = pathlib.Path(outdir)
    (outdir / "tables").mkdir(parents=True, exist_ok=True)
    (outdir / "figures").mkdir(parents=True, exist_ok=True)

    if catalog == "GWTC-1":
        snr, mean_snr = _mock_gwtc1_band_stats(band)
        events = [f"GWTC1-{i+1:02d}" for i in range(len(snr))]
    else:
        snr = np.array([10.0, 12.0, 25.0, 18.0])  # placeholder
        mean_snr = snr.mean()
        events = [f"O4-{i+1:02d}" for i in range(len(snr))]

    df = pd.DataFrame({"event": events, "snr_141hz": snr})
    table_path = outdir / "tables" / f"{catalog}_band_{band:.1f}.csv"
    df.to_csv(table_path, index=False)

    plt.figure()
    plt.bar(df["event"], df["snr_141hz"])
    plt.axhline(5.0, linestyle="--")
    plt.title(f"SNR en banda {band:.1f} Hz — {catalog} ({detector})")
    plt.xticks(rotation=75, ha="right")
    fig_path = outdir / "figures" / f"{catalog}_band_{band:.1f}.png"
    plt.tight_layout()
    plt.savefig(fig_path, dpi=160)
    plt.close()

    res = Result(catalog, detector, band, float(mean_snr), len(events),
                 str(table_path), str(fig_path))
    return json.loads(json.dumps(res.__dict__))
