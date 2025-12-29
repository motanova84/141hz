"""
QC-LLM REST API
Public endpoint for coherence validation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import sys
sys.path.append('../Python')

from qc_llm import QC_LLM, F0

app = FastAPI(
    title="QC-LLM API",
    description="Quantum Coherence Validator for Language Models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class TextInput(BaseModel):
    text: str = Field(..., min_length=1, description="Text to validate")
    model: Optional[str] = Field("unknown", description="Source model name")

class CoherenceResult(BaseModel):
    coherence: float = Field(..., ge=0, le=1)
    frequency_alignment: float = Field(..., ge=0, le=1)
    quantum_entropy: float = Field(..., ge=0, le=1)
    recommendation: str
    frequency: float
    version: str

# Initialize validator
validator = QC_LLM()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "QC-LLM API",
        "version": "1.0.0",
        "frequency": F0,
        "endpoints": {
            "validate": "/validate",
            "frequency": "/frequency",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.post("/validate", response_model=CoherenceResult)
async def validate_coherence(input: TextInput):
    """
    Validate quantum coherence of text
    
    Returns detailed metrics including:
    - Overall coherence score
    - Frequency alignment with f₀
    - Quantum entropy
    - Recommendation
    """
    try:
        result = validator.validate(input.text)
        return CoherenceResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/frequency")
async def get_frequency():
    """Get fundamental frequency f₀"""
    return {
        "f0": F0,
        "unit": "Hz",
        "derivation": {
            "formula": "f₀ = √2 × f_ref",
            "f_ref": "55100/550 Hz",
            "zeta_connection": "|ζ'(1/2)| × φ³",
            "scale_factor": "k ≈ 16.195"
        },
        "references": {
            "doi": "10.5281/zenodo.17379721",
            "github": "https://github.com/motanova84/141hz"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "frequency": F0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
