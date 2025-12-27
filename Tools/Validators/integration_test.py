#!/usr/bin/env python3
"""
Comprehensive Integration Test for QC-LLM

Tests all major components of the modular architecture
"""

import sys
from pathlib import Path

# Add paths
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root / "API" / "Python"))
sys.path.insert(0, str(root / "Applications" / "LLM"))

print("=" * 70)
print("QC-LLM Comprehensive Integration Test")
print("=" * 70)
print()

# Test 1: Core API
print("Test 1: Core API (Python)")
print("-" * 70)
try:
    from qc_llm import QC_LLM, F0
    
    validator = QC_LLM()
    result = validator.validate("Quantum coherence in language models")
    
    assert "coherence" in result
    assert result["coherence"] > 0
    assert F0 == 141.7001
    
    print(f"✅ Core API works")
    print(f"   Coherence: {result['coherence']:.2%}")
    print(f"   Frequency: {F0} Hz")
except Exception as e:
    print(f"❌ Core API failed: {e}")
    sys.exit(1)

print()

# Test 2: Coherence Metric
print("Test 2: Coherence Metric Application")
print("-" * 70)
try:
    from CoherenceMetric import CoherenceMetric
    
    metric = CoherenceMetric()
    score = metric.measure("Test quantum coherence measurement")
    
    assert 0 <= score <= 1
    
    print(f"✅ Coherence Metric works")
    print(f"   Score: {score:.2%}")
except Exception as e:
    print(f"❌ Coherence Metric failed: {e}")
    sys.exit(1)

print()

# Test 3: Quantum Alignment
print("Test 3: Quantum Alignment Application")
print("-" * 70)
try:
    from QuantumAlignment import QuantumAlignment
    
    aligner = QuantumAlignment(threshold=0.80)
    result = aligner.align_text("Original text to align")
    
    assert "coherence" in result
    assert "aligned" in result
    assert "iterations" in result
    
    print(f"✅ Quantum Alignment works")
    print(f"   Aligned: {result['aligned']}")
    print(f"   Coherence: {result['coherence']:.2%}")
except Exception as e:
    print(f"❌ Quantum Alignment failed: {e}")
    sys.exit(1)

print()

# Test 4: Real-Time Monitor
print("Test 4: Real-Time Monitor Application")
print("-" * 70)
try:
    from RealTimeMonitor import RealTimeMonitor
    
    monitor = RealTimeMonitor(window_size=10)
    
    # Simulate stream
    chunks = ["First chunk", "Second chunk", "Third chunk"]
    for chunk in chunks:
        coherence = monitor.update(chunk)
    
    stats = monitor.get_statistics()
    
    assert "mean" in stats
    assert stats["samples"] == len(chunks)
    
    print(f"✅ Real-Time Monitor works")
    print(f"   Mean coherence: {stats['mean']:.2%}")
    print(f"   Trend: {stats['trend']}")
except Exception as e:
    print(f"❌ Real-Time Monitor failed: {e}")
    sys.exit(1)

print()

# Test 5: Benchmark Infrastructure
print("Test 5: Benchmark Infrastructure")
print("-" * 70)
try:
    sys.path.insert(0, str(root / "Benchmarks" / "LLMComparison"))
    from benchmark import LLMBenchmark
    
    benchmark = LLMBenchmark()
    
    # Mock responses
    responses = [
        "Response to prompt 1",
        "Response to prompt 2",
        "Response to prompt 3",
        "Response to prompt 4",
        "Response to prompt 5"
    ]
    
    result = benchmark.benchmark_model("TestModel", responses)
    
    assert "avg_coherence" in result
    assert "model" in result
    assert result["model"] == "TestModel"
    
    print(f"✅ Benchmark Infrastructure works")
    print(f"   Avg coherence: {result['avg_coherence']:.2%}")
except Exception as e:
    print(f"❌ Benchmark Infrastructure failed: {e}")
    sys.exit(1)

print()

# Test 6: Batch Processing
print("Test 6: Batch Processing")
print("-" * 70)
try:
    texts = [
        "First document to validate",
        "Second document to validate",
        "Third document to validate"
    ]
    
    results = validator.batch_validate(texts)
    
    assert len(results) == len(texts)
    for result in results:
        assert "coherence" in result
    
    avg_coherence = sum(r["coherence"] for r in results) / len(results)
    
    print(f"✅ Batch Processing works")
    print(f"   Texts processed: {len(texts)}")
    print(f"   Avg coherence: {avg_coherence:.2%}")
except Exception as e:
    print(f"❌ Batch Processing failed: {e}")
    sys.exit(1)

print()

# Test 7: Model Comparison
print("Test 7: Model Comparison")
print("-" * 70)
try:
    outputs = {
        "Model A": "High quality coherent text with good structure",
        "Model B": "Lower quality text structure",
        "Model C": "Very coherent and well-structured output"
    }
    
    rankings = metric.rank_outputs(outputs)
    
    assert len(rankings) == len(outputs)
    assert all(isinstance(r[1], float) for r in rankings)
    
    print(f"✅ Model Comparison works")
    print(f"   Rankings:")
    for i, (model, score) in enumerate(rankings, 1):
        print(f"      {i}. {model}: {score:.2%}")
except Exception as e:
    print(f"❌ Model Comparison failed: {e}")
    sys.exit(1)

print()

# Test 8: Detailed Analysis
print("Test 8: Detailed Analysis")
print("-" * 70)
try:
    analysis = metric.detailed_analysis(
        "Comprehensive test of quantum coherence analysis"
    )
    
    assert "coherence" in analysis
    assert "frequency_alignment" in analysis
    assert "quantum_entropy" in analysis
    assert "recommendation" in analysis
    
    print(f"✅ Detailed Analysis works")
    print(f"   Coherence: {analysis['coherence']:.2%}")
    print(f"   Freq Alignment: {analysis['frequency_alignment']:.2%}")
    print(f"   Quantum Entropy: {analysis['quantum_entropy']:.2%}")
except Exception as e:
    print(f"❌ Detailed Analysis failed: {e}")
    sys.exit(1)

print()

# Summary
print("=" * 70)
print("✅ ALL INTEGRATION TESTS PASSED!")
print("=" * 70)
print()
print("Summary:")
print("  ✓ Core API (Python)")
print("  ✓ Coherence Metric Application")
print("  ✓ Quantum Alignment Application")
print("  ✓ Real-Time Monitor Application")
print("  ✓ Benchmark Infrastructure")
print("  ✓ Batch Processing")
print("  ✓ Model Comparison")
print("  ✓ Detailed Analysis")
print()
print(f"Fundamental Frequency: f₀ = {F0} Hz")
print("=" * 70)
