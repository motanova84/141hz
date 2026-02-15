#!/usr/bin/env python3
"""
QCAL-LLM Tokenization Pipeline
================================

Tokenization and corpus preparation pipeline for fine-tuning LLMs on QCAL knowledge.
Generates ~60M token corpus from:
- noesis88 documentation and theory
- Riemann-adelic mathematics
- 141hz gravitational wave analysis
- QCAL coherence framework

Target models:
- Llama-3.1 8B
- Qwen-2.5 14B

Expected outcome: LLM that doesn't hallucinate - reveals derivations and 
predictions consistent with Noetic Field Theory (NFT).

Author: Sistema QCAL ∞³
Date: 2026-02-14
"""

import json
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timezone
import re


class QCALCorpusGenerator:
    """
    Generate training corpus from QCAL repository for LLM fine-tuning.
    
    This class extracts and tokenizes documentation, code, and mathematical
    derivations to create a coherent corpus for training LLMs on QCAL theory.
    """
    
    def __init__(self, repo_path: Path, output_dir: Optional[Path] = None):
        """
        Initialize the corpus generator.
        
        Args:
            repo_path: Path to the 141hz repository
            output_dir: Directory for output files (default: repo_path/QCAL-LLM/training_data)
        """
        self.repo_path = Path(repo_path)
        self.output_dir = output_dir or (self.repo_path / "QCAL-LLM" / "training_data")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # QCAL constants
        self.f0 = 141.7001  # Hz
        self.kappa_pi = 2.5773
        self.zeta_half = 0.0  # ζ'(1/2) - would need mpmath for exact value
        
        # Corpus statistics
        self.stats = {
            "total_tokens": 0,
            "total_documents": 0,
            "sources": {
                "noesis88": 0,
                "riemann_adelic": 0,
                "gw_141hz": 0,
                "qcal_framework": 0,
                "mathematics": 0,
                "experimental": 0
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Document categories
        self.categories = {
            "noesis88": [
                "*noesis*", "*noetica*", "*noetic*", "*consciencia*",
                "*consciousness*", "*campo_psi*", "*psi_*"
            ],
            "riemann_adelic": [
                "*riemann*", "*zeta*", "*adelic*", "*prime*", "*primos*",
                "*numero*"
            ],
            "gw_141hz": [
                "*gw*", "*gravitational*", "*ligo*", "*virgo*", "*ondas*",
                "*141hz*", "*141.7*"
            ],
            "qcal_framework": [
                "*qcal*", "*coherence*", "*coherencia*", "*campo*",
                "*framework*", "*atlas*"
            ],
            "mathematics": [
                "*matematica*", "*derivacion*", "*demostracion*",
                "*theorem*", "*proof*", "*validacion*"
            ],
            "experimental": [
                "*experiment*", "*validacion*", "*verificacion*",
                "*wet_lab*", "*fluorescence*"
            ]
        }
    
    def find_documents(self, category: str) -> List[Path]:
        """
        Find all documents matching a category.
        
        Args:
            category: Document category name
            
        Returns:
            List of file paths
        """
        patterns = self.categories.get(category, [])
        files = []
        
        for pattern in patterns:
            # Search markdown files
            files.extend(self.repo_path.glob(f"**/{pattern}.md"))
            # Search Python files
            files.extend(self.repo_path.glob(f"**/{pattern}.py"))
        
        # Remove duplicates and sort
        files = sorted(list(set(files)))
        
        # Filter out hidden directories and common excludes
        filtered_files = []
        for f in files:
            if not any(part.startswith('.') for part in f.parts):
                if 'node_modules' not in f.parts and '__pycache__' not in f.parts:
                    filtered_files.append(f)
        
        return filtered_files
    
    def extract_text(self, file_path: Path) -> str:
        """
        Extract text content from a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Extracted text content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"⚠️  Could not read {file_path}: {e}")
            return ""
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text (rough approximation).
        
        Args:
            text: Input text
            
        Returns:
            Estimated token count
        """
        # Rough estimate: ~1.3 tokens per word for English/Spanish
        words = len(text.split())
        return int(words * 1.3)
    
    def create_instruction_format(self, content: str, metadata: Dict) -> Dict:
        """
        Create instruction-following format for LLM training.
        
        Args:
            content: Document content
            metadata: Document metadata
            
        Returns:
            Formatted instruction dictionary
        """
        # Extract title/topic if available
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else metadata.get('filename', 'Unknown')
        
        # Create instruction-response pairs
        instruction = f"Explain the QCAL theory concept: {title}"
        
        # Clean content (remove excessive whitespace, etc.)
        clean_content = re.sub(r'\n{3,}', '\n\n', content)
        clean_content = clean_content.strip()
        
        return {
            "instruction": instruction,
            "input": "",
            "output": clean_content,
            "metadata": metadata
        }
    
    def generate_corpus(self, format: str = "jsonl") -> Path:
        """
        Generate the complete training corpus.
        
        Args:
            format: Output format ('jsonl', 'json', or 'txt')
            
        Returns:
            Path to generated corpus file
        """
        print("🔬 QCAL-LLM Tokenization Pipeline")
        print("=" * 70)
        print(f"Repository: {self.repo_path}")
        print(f"Output: {self.output_dir}")
        print(f"Target: ~60M tokens")
        print("=" * 70)
        
        corpus_data = []
        
        # Process each category
        for category, patterns in self.categories.items():
            print(f"\n📁 Processing category: {category}")
            files = self.find_documents(category)
            print(f"   Found {len(files)} files")
            
            category_tokens = 0
            for file_path in files:
                content = self.extract_text(file_path)
                if not content:
                    continue
                
                tokens = self.estimate_tokens(content)
                category_tokens += tokens
                
                # Create training example
                metadata = {
                    "source_file": str(file_path.relative_to(self.repo_path)),
                    "category": category,
                    "tokens": tokens,
                    "qcal_constants": {
                        "f0": self.f0,
                        "kappa_pi": self.kappa_pi
                    }
                }
                
                example = self.create_instruction_format(content, metadata)
                corpus_data.append(example)
            
            self.stats["sources"][category] = category_tokens
            print(f"   Tokens: {category_tokens:,}")
        
        # Update total statistics
        self.stats["total_documents"] = len(corpus_data)
        self.stats["total_tokens"] = sum(self.stats["sources"].values())
        
        # Save corpus
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "jsonl":
            output_file = self.output_dir / f"qcal_corpus_{timestamp}.jsonl"
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in corpus_data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
        elif format == "json":
            output_file = self.output_dir / f"qcal_corpus_{timestamp}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(corpus_data, f, ensure_ascii=False, indent=2)
        else:  # txt
            output_file = self.output_dir / f"qcal_corpus_{timestamp}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in corpus_data:
                    f.write(f"### {item['instruction']}\n\n")
                    f.write(f"{item['output']}\n\n")
                    f.write("-" * 70 + "\n\n")
        
        # Save statistics
        stats_file = self.output_dir / f"corpus_stats_{timestamp}.json"
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print("\n" + "=" * 70)
        print("✅ Corpus Generation Complete!")
        print("=" * 70)
        print(f"Total documents: {self.stats['total_documents']:,}")
        print(f"Total tokens: {self.stats['total_tokens']:,}")
        print(f"Corpus file: {output_file}")
        print(f"Statistics: {stats_file}")
        print("=" * 70)
        
        return output_file
    
    def generate_fine_tuning_config(self, model_type: str = "llama-3.1-8b") -> Path:
        """
        Generate fine-tuning configuration file.
        
        Args:
            model_type: Target model type ('llama-3.1-8b' or 'qwen-2.5-14b')
            
        Returns:
            Path to config file
        """
        print(f"\n📋 Generating fine-tuning config for {model_type}...")
        
        config = {
            "model": {
                "type": model_type,
                "base_model": self._get_base_model_id(model_type),
                "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
            },
            "training": {
                "method": "lora",
                "lora_r": 8,
                "lora_alpha": 16,
                "lora_dropout": 0.05,
                "learning_rate": 2e-4,
                "num_epochs": 3,
                "batch_size": 4,
                "gradient_accumulation_steps": 4,
                "warmup_steps": 100,
                "save_steps": 500,
                "logging_steps": 10,
            },
            "data": {
                "format": "instruction",
                "max_length": 2048,
                "train_split": 0.95,
                "validation_split": 0.05,
            },
            "optimization": {
                "optimizer": "adamw",
                "scheduler": "cosine",
                "weight_decay": 0.01,
                "max_grad_norm": 1.0,
            },
            "qcal_constants": {
                "f0": self.f0,
                "kappa_pi": self.kappa_pi,
                "target": "NFT-consistent derivations without hallucination"
            }
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        config_file = self.output_dir / f"fine_tuning_config_{model_type}_{timestamp}.json"
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"   ✓ Config saved to: {config_file}")
        
        return config_file
    
    def _get_base_model_id(self, model_type: str) -> str:
        """
        Get Hugging Face model ID for a model type.
        
        Args:
            model_type: Model type identifier
            
        Returns:
            HuggingFace model ID
        """
        model_ids = {
            "llama-3.1-8b": "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "qwen-2.5-14b": "Qwen/Qwen2.5-14B-Instruct",
        }
        return model_ids.get(model_type, "meta-llama/Meta-Llama-3.1-8B-Instruct")
    
    def generate_training_script(self, model_type: str = "llama-3.1-8b") -> Path:
        """
        Generate training script for fine-tuning.
        
        Args:
            model_type: Target model type
            
        Returns:
            Path to training script
        """
        script_content = f"""#!/usr/bin/env python3
\"\"\"
Fine-tuning script for QCAL-LLM on {model_type}
Generated: {datetime.now(timezone.utc).isoformat()}
\"\"\"

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import json

# Load configuration
with open("fine_tuning_config_{model_type}_*.json", "r") as f:
    config = json.load(f)

# Load model and tokenizer
model_name = config["model"]["base_model"]
print(f"Loading model: {{model_name}}")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
)

# Configure LoRA
lora_config = LoraConfig(
    r=config["training"]["lora_r"],
    lora_alpha=config["training"]["lora_alpha"],
    target_modules=config["model"]["target_modules"],
    lora_dropout=config["training"]["lora_dropout"],
    bias="none",
    task_type="CAUSAL_LM"
)

# Prepare model for training
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)

print(f"Trainable parameters: {{model.print_trainable_parameters()}}")

# Load dataset
dataset = load_dataset("json", data_files="qcal_corpus_*.jsonl")

# Tokenization function
def tokenize_function(examples):
    texts = [
        f"### Instruction: {{inst}}\\n### Response: {{resp}}"
        for inst, resp in zip(examples["instruction"], examples["output"])
    ]
    return tokenizer(texts, truncation=True, max_length=config["data"]["max_length"])

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./qcal_llm_checkpoint",
    num_train_epochs=config["training"]["num_epochs"],
    per_device_train_batch_size=config["training"]["batch_size"],
    gradient_accumulation_steps=config["training"]["gradient_accumulation_steps"],
    learning_rate=config["training"]["learning_rate"],
    warmup_steps=config["training"]["warmup_steps"],
    logging_steps=config["training"]["logging_steps"],
    save_steps=config["training"]["save_steps"],
    save_total_limit=3,
    fp16=True,
    optim="adamw_torch",
    report_to="none",
)

# Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    data_collator=data_collator,
)

# Train
print("Starting training...")
trainer.train()

# Save model
model.save_pretrained("./qcal_llm_final")
tokenizer.save_pretrained("./qcal_llm_final")

print("Training complete! Model saved to ./qcal_llm_final")
"""
        
        script_file = self.output_dir / f"train_qcal_llm_{model_type}.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # Make executable
        script_file.chmod(0o755)
        
        print(f"\n📝 Training script generated: {script_file}")
        
        return script_file


def main():
    """Main entry point for tokenization pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="QCAL-LLM Tokenization Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--repo-path", type=str, default=".",
                       help="Path to 141hz repository")
    parser.add_argument("--output-dir", type=str, default=None,
                       help="Output directory for corpus")
    parser.add_argument("--format", type=str, default="jsonl",
                       choices=["jsonl", "json", "txt"],
                       help="Output format")
    parser.add_argument("--model", type=str, default="llama-3.1-8b",
                       choices=["llama-3.1-8b", "qwen-2.5-14b"],
                       help="Target model for fine-tuning config")
    parser.add_argument("--generate-config", action="store_true",
                       help="Generate fine-tuning configuration")
    parser.add_argument("--generate-script", action="store_true",
                       help="Generate training script")
    
    args = parser.parse_args()
    
    # Create generator
    generator = QCALCorpusGenerator(
        repo_path=Path(args.repo_path),
        output_dir=Path(args.output_dir) if args.output_dir else None
    )
    
    # Generate corpus
    corpus_file = generator.generate_corpus(format=args.format)
    
    # Generate config if requested
    if args.generate_config:
        config_file = generator.generate_fine_tuning_config(args.model)
    
    # Generate training script if requested
    if args.generate_script:
        script_file = generator.generate_training_script(args.model)
    
    print("\n✅ Pipeline complete!")
    print(f"   Corpus: {corpus_file}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
