# QCAL-LLM Makefile
# Automated benchmarking and testing suite

.PHONY: help benchmark test docker-build docker-run clean

MODEL ?= llama-4-405b
QCAL_FREQUENCY ?= 141.7001
QCAL_EPSILON ?= 0.015
QCAL_TAU ?= 0.07

help:
	@echo "QCAL-LLM Makefile Commands:"
	@echo ""
	@echo "  make benchmark MODEL=<model-name>  - Run full benchmark suite"
	@echo "  make test                           - Run test suite"
	@echo "  make docker-build                   - Build Docker image"
	@echo "  make docker-run                     - Run Docker container"
	@echo "  make clean                          - Clean generated files"
	@echo ""
	@echo "Environment variables:"
	@echo "  MODEL=$(MODEL)"
	@echo "  QCAL_FREQUENCY=$(QCAL_FREQUENCY)"
	@echo "  QCAL_EPSILON=$(QCAL_EPSILON)"
	@echo "  QCAL_TAU=$(QCAL_TAU)"

benchmark:
	@echo "Running benchmark suite for $(MODEL)..."
	@echo "QCAL Parameters: f0=$(QCAL_FREQUENCY), ε=$(QCAL_EPSILON), τ=$(QCAL_TAU)"
	@mkdir -p results
	@if [ -f benchmarks/run_gsm8k.py ]; then \
		python benchmarks/run_gsm8k.py --model $(MODEL) --qcal-mode \
			--frequency $(QCAL_FREQUENCY) --epsilon $(QCAL_EPSILON) --tau $(QCAL_TAU); \
	else \
		echo "Note: GSM8K benchmark not yet implemented. Creating stub..."; \
		mkdir -p benchmarks; \
		echo "# GSM8K benchmark stub - implement with your model" > benchmarks/run_gsm8k.py; \
	fi
	@if [ -f benchmarks/run_humaneval.py ]; then \
		python benchmarks/run_humaneval.py --model $(MODEL) --qcal-mode \
			--frequency $(QCAL_FREQUENCY) --epsilon $(QCAL_EPSILON) --tau $(QCAL_TAU); \
	fi
	@if [ -f benchmarks/run_truthfulqa.py ]; then \
		python benchmarks/run_truthfulqa.py --model $(MODEL) --qcal-mode \
			--frequency $(QCAL_FREQUENCY) --epsilon $(QCAL_EPSILON) --tau $(QCAL_TAU); \
	fi
	@if [ -f benchmarks/run_gpqa.py ]; then \
		python benchmarks/run_gpqa.py --model $(MODEL) --qcal-mode \
			--frequency $(QCAL_FREQUENCY) --epsilon $(QCAL_EPSILON) --tau $(QCAL_TAU); \
	fi
	@echo "Benchmark complete! Results saved to results/"

test:
	@echo "Running QCAL-LLM test suite..."
	@if [ -f ../test_qcal_llm.py ]; then \
		python ../test_qcal_llm.py; \
	elif [ -f ../noesis-qcal-llm/test_psi_metric_core.py ]; then \
		python ../noesis-qcal-llm/test_psi_metric_core.py; \
	else \
		echo "Warning: No test files found. Please check repository structure."; \
	fi

docker-build:
	@echo "Building QCAL-LLM Docker image..."
	docker build -f Dockerfile -t motanova/qcal-llm:latest-gpu .
	@echo "Build complete! Image: motanova/qcal-llm:latest-gpu"

docker-run:
	@echo "Starting QCAL-LLM container..."
	docker run --gpus all -p 8000:8000 \
		-e MODEL=$(MODEL) \
		-e QCAL_FREQUENCY=$(QCAL_FREQUENCY) \
		-e QCAL_EPSILON=$(QCAL_EPSILON) \
		-e QCAL_TAU=$(QCAL_TAU) \
		motanova/qcal-llm:latest-gpu

clean:
	@echo "Cleaning generated files..."
	rm -rf results/*.json results/*.png results/*.log
	rm -rf benchmarks/__pycache__
	rm -rf __pycache__
	@echo "Clean complete!"

# Quick tests for different models
test-llama4-405b:
	@$(MAKE) benchmark MODEL=llama-4-405b

test-llama4-70b:
	@$(MAKE) benchmark MODEL=llama-4-70b

test-qwen25-72b:
	@$(MAKE) benchmark MODEL=qwen2.5-72b-instruct

test-deepseek-r1:
	@$(MAKE) benchmark MODEL=deepseek-r1-671b

# Ablation study
ablation:
	@echo "Running ablation study (frequency variation)..."
	@mkdir -p results/ablation
	@for freq in 140.6 141.0 141.7 142.0 142.8; do \
		echo "Testing frequency: $$freq Hz"; \
		QCAL_FREQUENCY=$$freq $(MAKE) benchmark MODEL=$(MODEL) > results/ablation/freq_$$freq.log 2>&1; \
	done
	@echo "Ablation study complete! Results in results/ablation/"
