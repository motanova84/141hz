from qcal.analyze import analyze_catalog
def test_gwtc1_band_stats_mean_over_threshold(tmp_path):
    out = analyze_catalog("GWTC-1", 141.7, "H1", tmp_path.as_posix())
    assert out["n_events"] >= 10
    assert out["mean_snr"] > 5.0
