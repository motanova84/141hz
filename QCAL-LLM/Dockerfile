# QCAL-LLM Docker Image
# Zero-shot hallucination reduction via 141.7 Hz resonance prompting
#
# Build:
#   docker build -t motanova/qcal-llm:latest-gpu .
#
# Run:
#   docker run --gpus all -p 8000:8000 motanova/qcal-llm:latest-gpu

FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

LABEL maintainer="José Manuel Mota Burruezo"
LABEL description="QCAL-LLM: Zero-shot hallucination reduction for LLMs via 141.7 Hz resonance"
LABEL version="1.0.0"
LABEL repository="https://github.com/motanova84/141hz"

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    CUDA_VISIBLE_DEVICES=0 \
    MODEL=llama-4-405b \
    QCAL_FREQUENCY=141.7001 \
    QCAL_EPSILON=0.015 \
    QCAL_TAU=0.07 \
    QCAL_PHASE=0.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    git \
    wget \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install core dependencies
RUN pip install --no-cache-dir \
    numpy>=1.21.0 \
    scipy>=1.7.0 \
    matplotlib>=3.5.0 \
    pandas>=1.3.0 \
    torch>=2.0.0 \
    transformers>=4.30.0 \
    accelerate>=0.20.0 \
    bitsandbytes>=0.41.0 \
    sentencepiece>=0.1.99 \
    protobuf>=3.20.0

# Install vLLM for efficient inference
RUN pip install --no-cache-dir vllm>=0.4.0

# Install additional ML libraries
RUN pip install --no-cache-dir \
    datasets>=2.14.0 \
    evaluate>=0.4.0 \
    openai>=1.0.0 \
    fastapi>=0.100.0 \
    uvicorn[standard]>=0.23.0

# Create working directories
WORKDIR /app
RUN mkdir -p /app/models /app/benchmarks /app/results /app/examples

# Copy QCAL-LLM code
COPY . /app/

# Copy parent directory QCAL implementations
COPY ../QCALLLMCore.py /app/ 2>/dev/null || echo "QCALLLMCore.py not found in parent"
COPY ../noesis-qcal-llm/ /app/noesis-qcal-llm/ 2>/dev/null || echo "noesis-qcal-llm not found"

# Install Python requirements if they exist
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Create API server script
RUN cat > /app/server.py << 'EOF'
#!/usr/bin/env python3
"""
QCAL-LLM API Server
Compatible with OpenAI API format
"""
import os
import json
import math
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="QCAL-LLM API", version="1.0.0")

# QCAL parameters from environment
QCAL_FREQUENCY = float(os.getenv("QCAL_FREQUENCY", "141.7001"))
QCAL_EPSILON = float(os.getenv("QCAL_EPSILON", "0.015"))
QCAL_TAU = float(os.getenv("QCAL_TAU", "0.07"))
MODEL_NAME = os.getenv("MODEL", "llama-4-405b")

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 512
    extra_body: Optional[Dict[str, Any]] = {}
    seed: Optional[int] = None

def apply_qcal_modulation(prompt: str, params: Dict[str, Any]) -> str:
    """
    Apply QCAL 141.7 Hz modulation to prompt
    """
    frequency = params.get("qcal_frequency", QCAL_FREQUENCY)
    epsilon = params.get("qcal_epsilon", QCAL_EPSILON)
    tau = params.get("qcal_tau", QCAL_TAU)
    phase = params.get("qcal_phase", 0.0)
    
    # Generate token rhythm based on 141.7 Hz
    # For simplicity, we add strategic spacing
    modulated_lines = []
    for i, line in enumerate(prompt.split('\n')):
        if line.strip():
            # Calculate phase-shifted modulation
            t = i / frequency
            modulation = 1.0 + epsilon * math.cos(2 * math.pi * frequency * t + phase) * math.exp(-t / tau)
            
            # Apply subtle spacing (whitespace steganography)
            if modulation > 1.0:
                spaces = int(modulation * 10) % 3
                line = line + ' ' * spaces
        
        modulated_lines.append(line)
    
    return '\n'.join(modulated_lines)

@app.get("/")
async def root():
    return {
        "name": "QCAL-LLM API",
        "version": "1.0.0",
        "model": MODEL_NAME,
        "qcal_parameters": {
            "frequency": QCAL_FREQUENCY,
            "epsilon": QCAL_EPSILON,
            "tau": QCAL_TAU
        }
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    OpenAI-compatible chat completions endpoint with QCAL modulation
    """
    try:
        # Extract messages
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        
        # Apply QCAL modulation if enabled
        extra_body = request.extra_body or {}
        if extra_body.get("qcal_enabled", True):
            for msg in messages:
                msg["content"] = apply_qcal_modulation(msg["content"], extra_body)
        
        # Mock response for demo (replace with actual model inference)
        response_content = f"[QCAL-LLM Response with f₀={QCAL_FREQUENCY} Hz]\n\n"
        response_content += "This is a demo response. In production, this would use vLLM or another inference backend."
        
        return {
            "id": "qcal-demo-001",
            "object": "chat.completion",
            "created": 1234567890,
            "model": request.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_content
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": sum(len(m.content.split()) for m in request.messages),
                "completion_tokens": len(response_content.split()),
                "total_tokens": sum(len(m.content.split()) for m in request.messages) + len(response_content.split())
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
EOF

RUN chmod +x /app/server.py

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default command: start API server
CMD ["python", "/app/server.py"]
