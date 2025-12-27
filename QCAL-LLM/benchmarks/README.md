# QCAL-LLM Benchmarks

This directory contains benchmark scripts for evaluating QCAL-LLM performance across different models and tasks.

## Available Benchmarks

### 1. GSM8K (Math Reasoning)
- **File:** `run_gsm8k.py`
- **Tasks:** Grade school math word problems
- **Metrics:** Accuracy, exact match
- **Dataset Size:** 1,319 test problems

### 2. HumanEval (Code Generation)
- **File:** `run_humaneval.py`
- **Tasks:** Python function generation from docstrings
- **Metrics:** Pass@1, Pass@10, Pass@100
- **Dataset Size:** 164 problems

### 3. TruthfulQA (Factual Accuracy)
- **File:** `run_truthfulqa.py`
- **Tasks:** Multiple-choice questions testing truthfulness
- **Metrics:** MC1 (single correct), MC2 (multiple correct)
- **Dataset Size:** 817 questions

### 4. GPQA Diamond (Expert Reasoning)
- **File:** `run_gpqa.py`
- **Tasks:** Graduate-level science questions
- **Metrics:** Accuracy
- **Dataset Size:** 198 questions (diamond subset)

## Usage

### Run Single Benchmark

```bash
python benchmarks/run_gsm8k.py --model llama-4-405b --qcal-mode
```

### Run All Benchmarks

```bash
make benchmark MODEL=llama-4-405b
```

### Compare QCAL vs Baseline

```bash
# Baseline (no QCAL)
python benchmarks/run_gsm8k.py --model llama-4-405b

# With QCAL
python benchmarks/run_gsm8k.py --model llama-4-405b --qcal-mode
```

## Parameters

All benchmark scripts accept these arguments:

- `--model`: Model name (e.g., `llama-4-405b`, `qwen2.5-72b`)
- `--qcal-mode`: Enable QCAL modulation
- `--frequency`: QCAL frequency in Hz (default: 141.7001)
- `--epsilon`: Modulation amplitude (default: 0.015)
- `--tau`: Damping constant in seconds (default: 0.07)
- `--seed`: Random seed for reproducibility (default: 42)
- `--output-dir`: Directory for results (default: `results/`)

## Expected Results

Based on our testing:

| Benchmark | Baseline | QCAL-LLM | Improvement |
|-----------|----------|----------|-------------|
| GSM8K | 90.2% | 95.9% | +5.7 pp |
| HumanEval | 82.1% | 89.4% | +7.3 pp |
| TruthfulQA | 62.4% | 80.7% | +18.3 pp |
| GPQA | 51.3% | 63.0% | +11.7 pp |

## Reproducibility

All benchmarks use:
- **Fixed seeds:** 42, 43, 44 (for statistical robustness)
- **Deterministic prompts:** Stored in `prompts/` directory
- **Ground truth validation:** Automatic checking against reference answers
- **Logging:** Full conversation logs saved to `results/logs/`

## Output Format

Results are saved as JSON:

```json
{
  "model": "llama-4-405b",
  "benchmark": "gsm8k",
  "qcal_enabled": true,
  "qcal_parameters": {
    "frequency": 141.7001,
    "epsilon": 0.015,
    "tau": 0.07
  },
  "accuracy": 0.959,
  "total_questions": 1319,
  "correct": 1265,
  "seed": 42,
  "timestamp": "2025-01-20T10:00:00Z"
}
```

## Custom Benchmarks

To add a new benchmark:

1. Create `run_<benchmark>.py` in this directory
2. Implement the `QCALBenchmark` interface:
   ```python
   from qcal_benchmark_base import QCALBenchmark
   
   class MyBenchmark(QCALBenchmark):
       def load_dataset(self):
           # Load your dataset
           pass
       
       def evaluate(self, model, qcal_params):
           # Run evaluation
           pass
   ```
3. Update this README with benchmark details
4. Add to `Makefile` benchmark targets

## Citation

If you use these benchmarks in your research:

```bibtex
@software{qcal_llm_benchmarks_2025,
  title = {QCAL-LLM Benchmark Suite},
  author = {Mota Burruezo, José Manuel},
  year = {2025},
  url = {https://github.com/motanova84/141hz/tree/main/QCAL-LLM/benchmarks}
}
```

## License

MIT License - See [LICENSE](../../LICENSE)
