"""
QC-LLM Frequency Validator API
Public endpoint for coherence validation

This module implements the REST API described in PHASE 2 of the problem statement.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import sys
from pathlib import Path

# Add Python package to path
sys.path.insert(0, str(Path(__file__).parent.parent / "Python"))

from qc_llm import QC_LLM, F0

app = FastAPI(
    title="QC-LLM API",
    description="Quantum Coherence Validator for LLM Outputs",
    version="1.0.0"
)

class TextInput(BaseModel):
    text: str
    model: str = "unknown"

class CoherenceScore(BaseModel):
    coherence: float
    frequency_alignment: float
    quantum_metric: float
    recommendation: str

# Initialize validator
validator = QC_LLM()

def compute_coherence(text: str) -> dict:
    """
    Compute quantum coherence of text
    
    Algorithm:
    1. Tokenize and embed text
    2. Compute spectral density
    3. Measure alignment with f₀ = 141.7001 Hz
    4. Return multi-dimensional coherence score
    """
    result = validator.validate(text)
    
    # Add quantum metric (from entropy)
    quantum_metric = result.get("quantum_entropy", 0.5)
    
    return {
        "coherence": result["coherence"],
        "frequency_alignment": result["frequency_alignment"],
        "quantum_metric": quantum_metric,
        "recommendation": result["recommendation"]
    }

@app.post("/validate", response_model=CoherenceScore)
async def validate_coherence(input: TextInput):
    """
    Validate quantum coherence of text input
    
    Returns:
        CoherenceScore with detailed metrics
    """
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")
    
    result = compute_coherence(input.text)
    
    return CoherenceScore(**result)

@app.get("/frequency")
async def get_fundamental_frequency():
    """Get the fundamental coherence frequency"""
    return {
        "f0": F0,
        "unit": "Hz",
        "derivation": "sqrt(2) × f_ref where f_ref = |ζ'(1/2)| × φ³",
        "reference": "DOI: 10.5281/zenodo.17379721"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
