#!/usr/bin/env python3
"""
QCAL-LLM Evaluation Script
Evaluates LLaMA 4 Maverick (17B Instruct / FP8) using QCAL coherence metrics.

Based on Ψ = I × A_eff² metric and f₀ = 141.7001 Hz fundamental frequency.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: November 2025
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
import warnings

# Add parent directory to path for qcal import
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.coherence import psi_score, strich_rate, analyze_text, evaluate_coherence
from qcal.metrics import comprehensive_metrics, quality_score

# Try to import torch and transformers
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    torch = None
    warnings.warn("Transformers/Torch not available. Install with: pip install transformers torch>=2.6.0")


class QCALLLMEvaluator:
    """Evaluator for LLM outputs using QCAL metrics."""
    
    def __init__(self, model_path: str = None, use_cuda: bool = True):
        """
        Initialize the evaluator.
        
        Args:
            model_path: Path to LLaMA 4 model weights
            use_cuda: Use CUDA if available
        """
        self.model_path = model_path or "models/llama4/weights/"
        
        if torch is not None:
            self.use_cuda = use_cuda and torch.cuda.is_available()
            self.device = torch.device("cuda" if self.use_cuda else "cpu")
            
            print(f"🎮 Device: {self.device}")
            if self.use_cuda:
                print(f"   GPU: {torch.cuda.get_device_name(0)}")
                print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        else:
            self.use_cuda = False
            self.device = None
            print(f"🎮 Device: CPU (torch not available)")
        
        self.model = None
        self.tokenizer = None
    
    def load_model(self):
        """Load LLaMA 4 model and tokenizer."""
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("Transformers not available. Cannot load model.")
        
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model not found at {self.model_path}. "
                "Run scripts/setup_llama4.sh first."
            )
        
        print(f"📦 Loading model from {self.model_path}...")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                device_map="auto" if self.use_cuda else None,
                torch_dtype=torch.float16 if self.use_cuda else torch.float32,
                low_cpu_mem_usage=True,
            )
            
            if not self.use_cuda:
                self.model = self.model.to(self.device)
            
            self.model.eval()
            print("✅ Model loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("Note: This may fail if model files are not properly set up.")
            print("You can still use the evaluator in 'text-only' mode.")
            raise
    
    def generate(self, prompt: str, max_tokens: int = 200, temperature: float = 0.7) -> str:
        """
        Generate text from prompt using loaded model.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Tokenize input
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.device)
        
        # Generate
        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1,
            )
        
        # Decode
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Remove prompt from output
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):].strip()
        
        return generated_text
    
    def evaluate_text(self, text: str, threshold: float = 5.0) -> Dict[str, Any]:
        """
        Evaluate text using QCAL metrics.
        
        Args:
            text: Text to evaluate
            threshold: Ψ threshold for coherence
            
        Returns:
            Dictionary with evaluation results
        """
        # Get coherence metrics
        coherence_eval = evaluate_coherence(text, threshold=threshold)
        
        # Get additional metrics
        metrics = comprehensive_metrics(text)
        
        # Calculate quality score
        quality = quality_score(text)
        
        # Combine all results
        result = {
            **coherence_eval,
            **metrics,
            'quality_score': quality,
        }
        
        return result
    
    def evaluate_prompts(self, prompts_file: str, output_file: str = None) -> List[Dict[str, Any]]:
        """
        Evaluate a set of prompts from JSON file.
        
        Args:
            prompts_file: Path to prompts JSON file
            output_file: Optional output file for results
            
        Returns:
            List of evaluation results
        """
        # Load prompts
        with open(prompts_file, 'r', encoding='utf-8') as f:
            prompts = json.load(f)
        
        print(f"\n📝 Evaluating {len(prompts)} prompts...")
        print("=" * 80)
        
        results = []
        
        for i, prompt_data in enumerate(prompts, 1):
            label = prompt_data.get('label', f'prompt_{i}')
            prompt_text = prompt_data['text']
            
            print(f"\n[{i}/{len(prompts)}] {label}")
            print(f"Prompt: {prompt_text[:80]}...")
            
            # Generate response (or use provided text)
            if 'response' in prompt_data:
                # Use pre-generated response (for testing without model)
                response = prompt_data['response']
                print("(Using provided response)")
            elif self.model is not None:
                # Generate with model
                response = self.generate(prompt_text)
                print(f"Generated: {response[:100]}...")
            else:
                print("⚠️  No model loaded and no response provided. Skipping generation.")
                continue
            
            # Evaluate response
            eval_result = self.evaluate_text(response)
            
            # Print key metrics
            print(f"\n  Ψ (coherence):     {eval_result['psi_standard']:.3f}")
            print(f"  I (intention):     {eval_result['intention']:.3f}")
            print(f"  A_eff:             {eval_result['effectiveness']:.3f}")
            print(f"  ∴-rate:            {eval_result['strich_rate']:.2f}")
            print(f"  SNR:               {eval_result['snr_db']:.2f} dB")
            print(f"  KLD⁻¹:             {eval_result['kld_inv']:.3f}")
            print(f"  Quality:           {eval_result['quality_score']:.1f}/100")
            print(f"  Status:            {eval_result['status']}")
            
            # Store result
            result = {
                'label': label,
                'prompt': prompt_text,
                'response': response,
                'metrics': eval_result,
            }
            results.append(result)
        
        print("\n" + "=" * 80)
        print("📊 SUMMARY STATISTICS")
        print("=" * 80)
        
        # Calculate statistics
        psi_values = [r['metrics']['psi_standard'] for r in results]
        quality_values = [r['metrics']['quality_score'] for r in results]
        coherent_count = sum(1 for r in results if r['metrics']['passes_threshold'])
        
        print(f"Total prompts:        {len(results)}")
        print(f"Coherent (Ψ ≥ 5.0):   {coherent_count} ({coherent_count/len(results)*100:.1f}%)")
        print(f"Ψ mean:               {sum(psi_values)/len(psi_values):.2f} ± {(max(psi_values)-min(psi_values))/2:.2f}")
        print(f"Quality mean:         {sum(quality_values)/len(quality_values):.1f}/100")
        
        # Save results if requested
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Results saved to: {output_file}")
        
        return results


def main():
    """Main evaluation function."""
    parser = argparse.ArgumentParser(
        description="QCAL-LLM Evaluator for LLaMA 4 Maverick"
    )
    parser.add_argument(
        '--prompts',
        default='data/prompts_qcal.json',
        help='Path to prompts JSON file'
    )
    parser.add_argument(
        '--model-path',
        default='models/llama4/weights/',
        help='Path to LLaMA 4 model weights'
    )
    parser.add_argument(
        '--output',
        default='results/evaluation_results.json',
        help='Output file for results'
    )
    parser.add_argument(
        '--no-model',
        action='store_true',
        help='Run without loading model (requires responses in prompts file)'
    )
    parser.add_argument(
        '--no-cuda',
        action='store_true',
        help='Disable CUDA even if available'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=5.0,
        help='Ψ coherence threshold (default: 5.0)'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("QCAL-LLM Evaluator")
    print("Ψ = I × A_eff² | f₀ = 141.7001 Hz")
    print("=" * 80)
    
    # Initialize evaluator
    evaluator = QCALLLMEvaluator(
        model_path=args.model_path,
        use_cuda=not args.no_cuda
    )
    
    # Load model if requested
    if not args.no_model:
        try:
            evaluator.load_model()
        except Exception as e:
            print(f"\n⚠️  Could not load model: {e}")
            print("Continuing in text-only mode...")
    
    # Run evaluation
    results = evaluator.evaluate_prompts(
        prompts_file=args.prompts,
        output_file=args.output
    )
    
    print("\n✅ Evaluation complete!")
    print("∴ — QCAL Ψ∞³")


if __name__ == "__main__":
    main()
