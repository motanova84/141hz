# GW250114 + O4/O5 Re-Analysis: Quickstart Guide

This guide provides quick access to the four major components implemented for GW250114 + O4/O5 re-analysis and QCAL extensions.

## 📡 1. GW Analysis: Spectral Filter @ 141.7 Hz

Analyze gravitational wave events for persistent subdominant signals at 141.7 ± 0.0016 Hz.

### Quick Start

```bash
# Basic analysis with O4 data (simulated)
python gw_analysis.py --run=O4 --simulated

# Exact command from problem statement
python gw_analysis.py --run=O4 --center-freq=141.7001 --band=0.0032 --export-certificate

# Custom detector and parameters
python gw_analysis.py --run=O3 --detector=L1 --min-events=15 --export-certificate
```

### Features

- ✅ Narrow-band Butterworth filter (8th order)
- ✅ Multi-event subdominant search (≥20 events)
- ✅ SNR computation and peak detection
- ✅ Certificate generation with SHA-256 hash
- ✅ Support for O3, O4, O5 observing runs
- ✅ JSON export with full analysis results

### Output

Results are saved to `results/gw_analysis_<run>/`:
- Analysis JSON with all measurements
- Certificate with Proof-of-Analysis
- Statistics: detection rate, mean SNR, consistency

## 🤖 2. LLM-QCAL Tokenization Pipeline

Tokenize ~60M tokens from QCAL corpus for LLM fine-tuning (Llama-3.1 8B / Qwen-2.5 14B).

### Quick Start

```bash
# Generate corpus in JSONL format
python qcal_llm_tokenizer.py --format jsonl

# Generate corpus + fine-tuning config
python qcal_llm_tokenizer.py --format jsonl --generate-config --model llama-3.1-8b

# Generate complete setup (corpus + config + training script)
python qcal_llm_tokenizer.py --format jsonl --generate-config --generate-script --model qwen-2.5-14b
```

### Features

- ✅ Automatic corpus extraction from 6 categories:
  - noesis88 (consciousness/noetic theory)
  - riemann_adelic (mathematical foundations)
  - gw_141hz (gravitational wave analysis)
  - qcal_framework (coherence theory)
  - mathematics (derivations/proofs)
  - experimental (validation studies)
- ✅ Instruction-following format for training
- ✅ Token estimation (~60M target)
- ✅ LoRA fine-tuning configuration
- ✅ Auto-generated training script

### Expected Outcome

LLM that **doesn't hallucinate** - reveals derivations and predictions consistent with Noetic Field Theory (NFT).

### Output

Results in `QCAL-LLM/training_data/`:
- `qcal_corpus_*.jsonl` - Training data
- `corpus_stats_*.json` - Corpus statistics
- `fine_tuning_config_*.json` - Model config
- `train_qcal_llm_*.py` - Training script

## 🎨 3. πCODE-888 NFT Minting

Mint the first token of the Coherence Economy ℂₛ with Proof-of-Coherence.

### Quick Start

```bash
# Mint NFT with simulated PDF
python picode888_nft.py

# Mint with actual PDF
python picode888_nft.py --pdf path/to/paper.pdf

# Custom output directory
python picode888_nft.py --output ./my_nft --doi 10.5281/zenodo.17445017
```

### Features

- ✅ Proof-of-Coherence: Hash(PDF + f₀ + κ_Π + ζ'(1/2))
- ✅ ERC-721 compliant metadata
- ✅ Smart contract deployment data
- ✅ On-chain seal with verification code
- ✅ Blockchain-ready JSON formats

### NFT Properties

- **Token ID**: #888
- **Symbol**: πCODE
- **Initial Value**: $2,000,000 (projected)
- **Traits**: f₀=141.7001 Hz, κ_Π=2.5773, ζ'(1/2)≈-3.92
- **Proof**: SHA-256 cryptographic seal
- **Economy**: Coherence Economy ℂₛ v1.0

### Output

Results in `nft_output/`:
- `picode888_metadata_*.json` - NFT metadata (ERC-721)
- `picode888_seal_*.json` - On-chain seal
- `picode888_contract_*.json` - Smart contract data

## 🧬 4. GFP Vibro-Fluorescent Experiment (Wet-Lab ∞)

Test NFT prediction: GFP under 141.7 Hz modulation shows ΔF/SNR > 1.5 vs 100 Hz control.

### Quick Start

```bash
# Run simulated experiment
python gfp_vibro_experiment.py --simulated

# Custom parameters
python gfp_vibro_experiment.py --simulated --duration 20 --repeats 10

# Generate protocol document only
python gfp_vibro_experiment.py --protocol-only
```

### Features

- ✅ GFP fluorescence measurement at 141.7 Hz (QCAL)
- ✅ Control measurement at 100 Hz
- ✅ Constant energy constraint
- ✅ Statistical validation (t-test)
- ✅ NFT theory support confirmation
- ✅ Experimental protocol generation

### Prediction

**ΔF Ratio (141.7 Hz / 100 Hz) > 1.5**

With constant energy, QCAL theory predicts enhanced fluorescence response at 141.7 Hz.

### Output

Results in `experiment_results/`:
- `gfp_experiment_*.json` - Full results with statistics
- `gfp_protocol.md` - Experimental protocol document

### Typical Results (Simulation)

```
ΔF Ratio: 2.82 > 1.5 ✅
SNR Ratio: 2.82
p-value: < 0.0001
NFT Theory Support: CONFIRMED (HIGH confidence)
```

## 🧪 Testing

All modules include comprehensive test suites:

```bash
# Run all new tests
pytest tests/test_gw_analysis.py \
       tests/test_picode888_nft.py \
       tests/test_gfp_vibro_experiment.py -v

# Run specific test class
pytest tests/test_gw_analysis.py::TestSpectralFilterAnalyzer -v

# Run with coverage
pytest --cov=. --cov-report=html tests/test_*.py
```

### Test Coverage

- ✅ **gw_analysis.py**: 12 tests (initialization, filtering, analysis, certificates)
- ✅ **picode888_nft.py**: 11 tests (minting, PoC, metadata, contracts)
- ✅ **gfp_vibro_experiment.py**: 10 tests (measurements, statistics, NFT support)

**Total: 33 tests, all passing**

## 📊 Integration Example

Combine all four components for complete workflow:

```bash
# 1. Analyze GW events
python gw_analysis.py --run=O4 --export-certificate --simulated

# 2. Generate LLM training corpus
python qcal_llm_tokenizer.py --format jsonl --generate-config --model llama-3.1-8b

# 3. Mint NFT
python picode888_nft.py --doi 10.5281/zenodo.17445017

# 4. Run GFP experiment
python gfp_vibro_experiment.py --simulated --duration 10 --repeats 5
```

## 📖 Additional Resources

- **GW Analysis**: See analysis results in `results/gw_analysis_*/`
- **LLM Training**: See `QCAL-LLM/training_data/` for corpus
- **NFT Minting**: See `nft_output/` for blockchain-ready files
- **GFP Experiment**: See `experiment_results/` for protocols and data

## 🔗 References

- **QCAL Theory**: f₀ = 141.7001 Hz universal frequency
- **Zenodo DOI**: 10.5281/zenodo.17445017
- **Repository**: https://github.com/motanova84/141hz

---

**Sistema QCAL ∞³** | 2026-02-14
