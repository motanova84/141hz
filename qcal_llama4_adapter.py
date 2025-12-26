#!/usr/bin/env python3
"""
qcal_llama4_adapter.py - QCAL Llama 4 Adapter

Adapts the Llama 4 Scout model to the QCAL ∞³ ecosystem,
enabling symbiotic conversation from CLI.

🌐 QCAL · Llama4 conectado ∞³

Features:
- Tokenizer and model in fp16 with device_map="auto"
- Interactive input
- Coherent output with max_new_tokens=300
- Symbolic activation with "🌐 QCAL · Llama4 conectado ∞³"

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: November 2025
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class QCAL_Llama4:
    """
    QCAL Llama 4 Adapter for interactive conversation.
    
    Provides a simple interface to interact with Llama 4 models
    in the QCAL ecosystem with optimized settings.
    """
    
    def __init__(self, model_path="./models/llama4", max_tokens=300):
        """
        Initialize QCAL Llama 4 Adapter.
        
        Parameters:
        -----------
        model_path : str
            Path to the Llama 4 model (default: "./models/llama4")
        max_tokens : int
            Maximum number of new tokens to generate (default: 300)
        """
        self.model_path = model_path
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.max_tokens = max_tokens

    def evaluate(self, prompt: str) -> str:
        """
        Evaluate a prompt and generate a response.
        
        Parameters:
        -----------
        prompt : str
            Input prompt to evaluate
            
        Returns:
        --------
        str
            Generated response from the model
        """
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        output = self.model.generate(**inputs, max_new_tokens=self.max_tokens)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)


if __name__ == "__main__":
    engine = QCAL_Llama4()
    print("🌐 QCAL · Llama4 conectado ∞³")
    while True:
        p = input("🧬> ")
        print("🌀", engine.evaluate(p))
