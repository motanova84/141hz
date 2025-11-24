"""
LLM Coherence Comparison Benchmark

Compares quantum coherence across major LLMs
"""

import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Callable
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "API" / "Python"))
from qc_llm import QC_LLM, F0

# Test prompts (curated for scientific content)
TEST_PROMPTS = [
    "Explain the Riemann Hypothesis",
    "Describe quantum entanglement",
    "What is consciousness?",
    "Explain Navier-Stokes equations",
    "Describe the golden ratio"
]

class LLMBenchmark:
    """
    Benchmark quantum coherence across LLMs
    
    Usage:
        >>> benchmark = LLMBenchmark()
        >>> results = benchmark.run_benchmark({
        ...     "GPT-4": gpt4_responses,
        ...     "Claude-3.5": claude_responses
        ... })
    """
    
    def __init__(self, test_prompts: Optional[List[str]] = None):
        """
        Initialize benchmark
        
        Args:
            test_prompts: Custom test prompts (default: predefined set)
        """
        self.test_prompts = test_prompts or TEST_PROMPTS
        self.validator = QC_LLM()
    
    def benchmark_model(
        self, 
        model_name: str, 
        responses: List[str]
    ) -> Dict:
        """
        Benchmark a single model
        
        Args:
            model_name: Name of the model
            responses: List of responses (one per test prompt)
            
        Returns:
            Dictionary with benchmark results
        """
        if len(responses) != len(self.test_prompts):
            raise ValueError(
                f"Expected {len(self.test_prompts)} responses, "
                f"got {len(responses)}"
            )
        
        scores = []
        for response in responses:
            result = self.validator.validate(response)
            scores.append(result["coherence"])
        
        return {
            "model": model_name,
            "avg_coherence": float(np.mean(scores)),
            "min_coherence": float(np.min(scores)),
            "max_coherence": float(np.max(scores)),
            "std_dev": float(np.std(scores)),
            "scores": scores,
            "timestamp": datetime.now().isoformat()
        }
    
    def run_benchmark(
        self, 
        model_responses: Dict[str, List[str]]
    ) -> List[Dict]:
        """
        Run benchmark across multiple models
        
        Args:
            model_responses: Dict mapping model names to response lists
            
        Returns:
            List of benchmark results, sorted by avg_coherence
        """
        results = []
        
        for model_name, responses in model_responses.items():
            result = self.benchmark_model(model_name, responses)
            results.append(result)
        
        # Sort by average coherence (descending)
        results.sort(key=lambda x: x["avg_coherence"], reverse=True)
        
        return results
    
    def generate_leaderboard(
        self, 
        results: List[Dict],
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate markdown leaderboard
        
        Args:
            results: Benchmark results
            output_path: Optional path to save leaderboard
            
        Returns:
            Markdown formatted leaderboard
        """
        md = f"""# QC-LLM Coherence Leaderboard

**Last Updated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Fundamental Frequency:** f₀ = {F0} Hz

## Results

| Rank | Model | Avg Coherence | Min | Max | Std Dev |
|------|-------|---------------|-----|-----|---------|
"""
        
        for i, r in enumerate(results, 1):
            md += (
                f"| {i} | {r['model']} | "
                f"{r['avg_coherence']:.2%} | "
                f"{r['min_coherence']:.2%} | "
                f"{r['max_coherence']:.2%} | "
                f"{r['std_dev']:.4f} |\n"
            )
        
        md += f"""

## Methodology

- **Fundamental Frequency:** f₀ = {F0} Hz
- **Test Prompts:** {len(self.test_prompts)} scientific questions
- **Metric:** Spectral alignment with f₀

## Test Prompts

"""
        for i, prompt in enumerate(self.test_prompts, 1):
            md += f"{i}. {prompt}\n"
        
        md += """
## Reference

Mota Burruezo, J.M. (2025). Quantum Coherence in Language Models.  
DOI: 10.5281/zenodo.17379721
"""
        
        if output_path:
            Path(output_path).write_text(md)
        
        return md
    
    def save_results(self, results: List[Dict], output_path: str):
        """
        Save results to JSON file
        
        Args:
            results: Benchmark results
            output_path: Path to save JSON
        """
        output = {
            "timestamp": datetime.now().isoformat(),
            "frequency": F0,
            "test_prompts": self.test_prompts,
            "results": results
        }
        
        Path(output_path).write_text(
            json.dumps(output, indent=2)
        )
