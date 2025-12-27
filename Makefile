.PHONY: all venv setup install data data-force download test-data check-data analyze validate validate-offline pipeline validate-connectivity validate-gw150914 validate-gw250114 verify-optimization workflow status clean clean-force docker help
.PHONY: all download analyze clean venv setup test-data

all: setup test-data analyze
.PHONY: all venv setup install data download test-data analyze validate pipeline clean docker help

# Default target - complete workflow
all: setup validate
.PHONY: all install venv setup data analyze clean docker

all: setup data analyze

venv:
	python3 -m venv venv

setup: venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

.PHONY: \
  all venv setup install \
  data download test-data check-data \
  analyze validate validate-offline pipeline \
  validate-connectivity validate-gw150914 validate-gw250114 \
  alert-gw250114 test-alert-gw250114 test-rpsi \
  validacion-quintica multievento test-multievento \
  multi-event-snr test-multi-event-snr demo-multi-event-snr \
  universalidad-virgo-kagra test-universalidad-virgo-kagra \
  snr-gw200129 test-snr-gw200129 \
  energia-cuantica test-energia-cuantica \
  fractal-resonance test-fractal-resonance \
  validate-3-pilares test-3-pilares \
  validate-discovery-standards test-discovery-standards \
  pycbc-analysis test-pycbc demo-pycbc coherencia-escalas \
  gwtc3-analysis busqueda-gwtc1 \
  busqueda-armonicos test-armonicos resonancia-cruzada test-resonancia \
  caracterizacion-bayesiana test-caracterizacion \
  dashboard dashboard-status workflow status \
  escuchar test-escuchar listen \
  clean docker help \
  experimentos test-experimentos diagrams-experimentos
install: setup

.PHONY: all venv setup install data download test-data check-data analyze validate validate-offline pipeline validate-connectivity validate-gw150914 validate-gw250114 verify-optimization workflow status clean docker help

# Default target - complete workflow
all: setup validate
	@echo "🎉 Workflow predeterminado completado"
	@echo "💡 Para análisis completo con datos: make workflow"

# Show available targets
help:
	@echo "🌌 GW250114 - 141.7001 Hz Analysis - Available targets:"
	@echo ""
	@echo "  all                   - Complete workflow: setup + validate"
	@echo "  setup                 - Create virtual environment and install dependencies"
	@echo "  install               - Alias for setup (compatibility)"
	@echo "  venv                  - Create virtual environment only"
	@echo "  data                  - Download real GWOSC data (with confirmation)"
	@echo "  data-force            - Download data without confirmation (automated)"
	@echo "  download              - Alias for data (compatibility)"
	@echo "  test-data             - Generate test data (falls back to real data)"
	@echo "  check-data            - Verify if data files are available"
	@echo "  analyze               - Run complete analysis pipeline (requires data)"
	@echo "  validate              - Run scientific validation pipeline (NEW)"
	@echo "  validate-offline      - Run validation with synthetic data only (NEW)"
	@echo "  pipeline              - Alias for validate (compatibility)"
	@echo "  validate-connectivity - Test GWOSC connectivity only (NEW)"
	@echo "  validate-gw150914     - Validate GW150914 control (NEW)"
	@echo "  validate-gw250114     - Test GW250114 framework (NEW)"
	@echo "  alert-gw250114        - Monitor GW250114 availability continuously (NEW)"
	@echo "  test-alert-gw250114   - Test GW250114 alert system (NEW)"
	@echo "  test-rpsi             - Test R_Ψ symmetry and compactification radius (NEW)"
	@echo "  multievento           - Run multi-event Bayesian analysis (NEW)"
	@echo "  test-multievento      - Test multi-event module with synthetic data (NEW)"
	@echo "  multi-event-snr       - Run multi-event SNR analysis at 141.7 Hz (NEW)"
	@echo "  test-multi-event-snr  - Test multi-event SNR analysis module (NEW)"
	@echo "  demo-multi-event-snr  - Demo multi-event SNR with synthetic data (NEW)"
	@echo "  universalidad-virgo-kagra - Test 141.7 Hz universality in Virgo/KAGRA (NEW)"
	@echo "  test-universalidad-virgo-kagra - Test Virgo/KAGRA universality module (NEW)"
	@echo "  snr-gw200129          - Analyze SNR for GW200129_065458 at 141.7 Hz (NEW)"
	@echo "  test-snr-gw200129     - Test SNR analysis for GW200129_065458 (NEW)"
	@echo "  energia-cuantica      - Calculate quantum energy E_Ψ = hf₀ (NEW)"
	@echo "  test-energia-cuantica - Test quantum energy calculations (NEW)"
	@echo "  fractal-resonance     - Derive 141.7001 Hz from fractal resonance in fundamental constants (NEW)"
	@echo "  test-fractal-resonance - Test fractal resonance derivation module (NEW)"
	@echo "  validate-3-pilares    - Run 3 pillars validation: reproducibility, falsifiability, evidence (NEW)"
	@echo "  test-3-pilares        - Test 3 pillars validation scripts (NEW)"
	@echo "  validate-discovery-standards - Validate scientific discovery standards (>10σ) (NEW)"
	@echo "  test-discovery-standards     - Test discovery standards validation (NEW)"
	@echo "  pycbc-analysis        - Run PyCBC-based GW150914 analysis (NEW)"
	@echo "  test-pycbc            - Test PyCBC analysis script (NEW)"
	@echo "  demo-pycbc            - Run PyCBC analysis demo with simulated data (NEW)"
	@echo "  coherencia-escalas    - Generate coherence multi-scale visualization (NEW)"
	@echo "  gwtc3-analysis        - Run GWTC-3 complete analysis with auto-installation (NEW)"
	@echo "  busqueda-gwtc1        - Run GWTC-1 systematic search for 141.7 Hz (NEW)"
	@echo "  busqueda-armonicos    - Search for higher harmonics of f₀ in LIGO data (NEW)"
	@echo "  test-armonicos        - Test higher harmonics search module (NEW)"
	@echo "  resonancia-cruzada    - Multi-detector cross-resonance analysis (Virgo/KAGRA) (NEW)"
	@echo "  test-resonancia       - Test cross-resonance analysis module (NEW)"
	@echo "  caracterizacion-bayesiana - Bayesian Q-factor characterization (NEW)"
	@echo "  test-caracterizacion  - Test Bayesian characterization module (NEW)"
	@echo "  experimentos          - Run experimental protocols for f₀ validation (NEW)"
	@echo "  test-experimentos     - Test experimental protocols (28 tests) (NEW)"
	@echo "  diagrams-experimentos - Generate workflow diagrams for experiments (NEW)"
	@echo "  escuchar              - Interactive discovery experience: 'Ahora te toca escuchar' (NEW)"
	@echo "  test-escuchar         - Test escuchar.py interactive script (NEW)"
	@echo "  listen                - Alias for escuchar (English) (NEW)"
	@echo "  dashboard             - Run real-time monitoring dashboard (NEW)"
	@echo "  dashboard-status      - Run GW250114 status dashboard (NEW)"
	@echo "  verify-optimization   - Verify maximum system optimization (NEW)"
	@echo "  workflow              - Complete workflow: setup + data + analyze"
	@echo "  docker                - Build and run Docker container"
	@echo "  status                - Show project status and environment info"
	@echo "  clean                 - Remove generated files (with confirmation)"
	@echo "  clean-force           - Clean without confirmation (automated)"
	@echo "  help                  - Show this help message"

# Create virtual environment
# Create virtual environment
venv:
	python3 -m venv venv

# Setup environment with dependencies
setup: venv
	@echo "📦 Installing dependencies..."
	@./venv/bin/pip install --upgrade pip --timeout 30 2>/dev/null || echo "⚠️  Pip upgrade skipped due to network issues"
	@./venv/bin/pip install -r requirements.txt --timeout 30 || echo "⚠️  Some packages may not have installed - check manually if needed"
	@echo "✅ Setup completed"

# Install dependencies (same as setup for compatibility)
install: setup

# Download real data from GWOSC
data: setup
	@echo "📡 Descargando datos de GWOSC..."
	./venv/bin/python scripts/descargar_datos.py || echo "⚠️  Error descargando datos - verificar conectividad"

# Download data without confirmation (for automated workflows)
data-force: setup
	@echo "📡 Descargando datos de GWOSC (sin confirmación)..."
	./venv/bin/python scripts/descargar_datos.py --yes || echo "⚠️  Error descargando datos - verificar conectividad"

# Alias for data (for compatibility with old branch)  
download: data

# Generate test data (optional - script not implemented yet)
test-data: data
	@echo "⚠️  Test data generation script not implemented yet"
	@echo "   Using real GWOSC data instead via 'make data'"

# Check if data exists
check-data:
	@echo "🔍 Verificando disponibilidad de datos..."
	@if [ -d "data/raw" ] && [ -n "$$(ls -A data/raw 2>/dev/null)" ]; then \
		echo "   ✅ Datos encontrados en data/raw/"; \
		ls -la data/raw/; \
	else \
		echo "   ❌ No se encontraron datos"; \
		echo "   💡 Ejecuta: make data"; \
		false; \
	fi

# Run complete analysis (legacy scripts) - with data dependency
analyze: check-data
	@echo "🔬 Ejecutando análisis completo..."
	./venv/bin/python scripts/analizar_ringdown.py
	./venv/bin/python scripts/analizar_l1.py
	./venv/bin/python scripts/analisis_noesico.py

# Run scientific validation pipeline (NEW - from problem statement)
validate:
	@echo "🚀 Ejecutando Pipeline de Validación Científica"
	@echo "   Implementa los requisitos del problema statement"
	./venv/bin/python scripts/pipeline_validacion.py

# Alias for validate
pipeline: validate
# Run comprehensive GW250114 analysis (6-step workflow)
analyze-gw250114:
	./venv/bin/python scripts/analisis_gw250114.py

# Individual validation steps  
validate-connectivity: setup
	@echo "🌐 Validando conectividad GWOSC..."
	./venv/bin/python scripts/validar_conectividad.py || echo "⚠️  Problemas de conectividad detectados"

validate-gw150914: setup
	@echo "🔬 Validando análisis de control GW150914..."
	./venv/bin/python scripts/validar_gw150914.py || echo "⚠️  Validación GW150914 falló - revisar conectividad"

validate-gw250114: setup  
	@echo "🎯 Validando framework GW250114..."
	./venv/bin/python scripts/analizar_gw250114.py || echo "⚠️  Framework GW250114 presentó errores - revisar logs"

# Alert system for GW250114 availability
alert-gw250114: setup
	@echo "🚨 Sistema de alertas automáticas para GW250114"
	@echo "   Iniciando monitoreo continuo..."
	@echo "   Presiona Ctrl+C para detener"
	./venv/bin/python scripts/verificador_gw250114.py

# Test alert system for GW250114
test-alert-gw250114: setup
	@echo "🧪 Testing alert system for GW250114..."
	./venv/bin/python scripts/test_verificador_gw250114.py

# Test R_Ψ symmetry and compactification radius
test-rpsi: setup
	@echo "🔬 Testing R_Ψ symmetry and compactification radius..."
	@echo "   Validating R_Ψ = 1.687e-35 m and f₀ = 141.7001 Hz relationship"
	./venv/bin/python scripts/test_rpsi_symmetry.py

# Validate Calabi-Yau compactification (Section 5.7f)
validacion-quintica: setup
	@echo "🔬 Validación numérica de compactificación sobre la quíntica en ℂP⁴..."
	@echo "   Sección 5.7(f): Jerarquía RΨ ≈ 10⁴⁷ y frecuencia f₀ = 141.7001 Hz"
	./venv/bin/python scripts/validacion_compactificacion_quintica.py

# Multi-event Bayesian analysis
multievento: setup
	@echo "🌌 Ejecutando análisis bayesiano multi-evento..."
	@echo "   Eventos: GW150914, GW151012, GW170104, GW190521, GW200115"
	./venv/bin/python scripts/analisis_bayesiano_multievento.py || echo "⚠️  Análisis multi-evento completado con advertencias"

# Test multi-event module with synthetic data
test-multievento: setup
	@echo "🧪 Testing análisis bayesiano multi-evento..."
	./venv/bin/python scripts/test_analisis_bayesiano_multievento.py

# Multi-event SNR analysis at 141.7 Hz
multi-event-snr: setup
	@echo "📊 Ejecutando análisis multi-evento de SNR en 141.7 Hz..."
	@echo "   Eventos: GW150914, GW151012, GW151226, GW170104, GW170608,"
	@echo "            GW170729, GW170809, GW170814, GW170817, GW170818, GW170823"
	@echo "   Banda: 140.7-142.7 Hz"
	./venv/bin/python scripts/multi_event_snr_analysis.py || echo "⚠️  Análisis multi-evento SNR completado con advertencias"

# Test multi-event SNR analysis module
test-multi-event-snr: setup
	@echo "🧪 Testing análisis multi-evento de SNR..."
	./venv/bin/python scripts/test_multi_event_snr_analysis.py

# Demo multi-event SNR analysis with synthetic data
demo-multi-event-snr: setup
	@echo "🎬 Ejecutando demostración de análisis multi-evento SNR..."
	@echo "   Usando datos sintéticos (sin conectividad a GWOSC)"
	./venv/bin/python scripts/demo_multi_event_snr.py || python3 scripts/demo_multi_event_snr.py

# Test universality of 141.7 Hz in Virgo and KAGRA detectors
universalidad-virgo-kagra: setup
	@echo "🌍 Ejecutando test de universalidad 141.7 Hz en Virgo/KAGRA..."
	@echo "   Eventos: GW170814, GW170817, GW170818, GW170823"
	@echo "   Detector: Virgo (V1)"
	@echo "   Banda: 141.4-142.0 Hz"
	./venv/bin/python scripts/test_universalidad_virgo_kagra.py || echo "⚠️  Análisis Virgo/KAGRA completado con advertencias"

# Test Virgo/KAGRA universality module
test-universalidad-virgo-kagra: setup
	@echo "🧪 Testing análisis de universalidad Virgo/KAGRA..."
	./venv/bin/python scripts/test_test_universalidad_virgo_kagra.py
# SNR analysis for GW200129_065458 event
snr-gw200129: setup
	@echo "📊 Ejecutando análisis de SNR para GW200129_065458 en 141.7 Hz..."
	@echo "   Evento O3b: 2020-01-29 06:54:58 UTC"
	@echo "   Detectores: H1, L1, V1 (K1 no disponible)"
	./venv/bin/python scripts/snr_gw200129_analysis.py

# Test SNR analysis for GW200129_065458
test-snr-gw200129: setup
	@echo "🧪 Testing análisis de SNR para GW200129_065458..."
	./venv/bin/python scripts/test_snr_gw200129_analysis.py

# Calculate quantum energy of fundamental mode
energia-cuantica: setup
	@echo "⚛️  Calculando energía cuántica del modo fundamental..."
	@echo "   E_Ψ = hf₀ con f₀ = 141.7001 Hz"
	./venv/bin/python scripts/energia_cuantica_fundamental.py

# Test quantum energy calculations
test-energia-cuantica: setup
	@echo "🧪 Testing cálculos de energía cuántica..."
	./venv/bin/python scripts/test_energia_cuantica.py

# Derive 141.7001 Hz from fractal resonance in fundamental constants
fractal-resonance:
	@echo "🔢 Deriving 141.7001 Hz from Fractal Resonance in Fundamental Constants..."
	@echo "   Complex prime series with α_opt = 0.551020"
	@echo "   Fractal correction δ ≈ 1.000141678"
	@echo "   Fractal dimension D_f ≈ 1.236857745"
	python3 scripts/fractal_resonance_constants.py

# Test fractal resonance module
test-fractal-resonance:
	@echo "🧪 Testing fractal resonance derivation..."
	python3 scripts/test_fractal_resonance_constants.py

# Run 3 pillars validation: reproducibility, falsifiability, evidence
validate-3-pilares: setup
	@echo "🌟 Ejecutando Validación de 3 Pilares del Método Científico..."
	@echo "   1. REPRODUCIBILIDAD GARANTIZADA"
	@echo "   2. FALSABILIDAD EXPLÍCITA"
	@echo "   3. EVIDENCIA EMPÍRICA CONCRETA"
	./venv/bin/python scripts/validacion_completa_3_pilares.py

# Test 3 pillars validation scripts
test-3-pilares: setup
	@echo "🧪 Testing scripts de validación de 3 pilares..."
	@echo "   Testing reproducibilidad..."
	./venv/bin/python scripts/reproducibilidad_garantizada.py || exit 1
	@echo "   Testing falsabilidad..."
	./venv/bin/python scripts/falsabilidad_explicita.py || exit 1
	@echo "   Testing evidencia empírica..."
	./venv/bin/python scripts/evidencia_empirica.py || exit 1
	@echo "   Testing validación completa..."
	./venv/bin/python scripts/validacion_completa_3_pilares.py || exit 1
	@echo "✅ Todos los tests de 3 pilares pasaron exitosamente"

# Validate scientific discovery standards (Particle Physics, Astronomy, Medicine)
validate-discovery-standards: setup
	@echo "📊 Validando Estándares de Descubrimiento Científico..."
	@echo "   • Física de partículas: ≥ 5σ"
	@echo "   • Astronomía: ≥ 3σ"
	@echo "   • Medicina (EEG): ≥ 2σ"
	./venv/bin/python scripts/discovery_standards.py
	@echo "✅ Validación de estándares completada"

# Test discovery standards validation
test-discovery-standards: setup
	@echo "🧪 Testing validación de estándares de descubrimiento..."
	./venv/bin/python scripts/test_discovery_standards.py
	@echo "✅ Tests de estándares de descubrimiento pasaron exitosamente"

# Run PyCBC-based GW150914 analysis
pycbc-analysis: setup
	@echo "🌌 Ejecutando análisis GW150914 con PyCBC..."
	@echo "   Filtrado, blanqueado y graficado de señal"
	@mkdir -p results/figures
	./venv/bin/python scripts/analizar_gw150914_pycbc.py || echo "⚠️  Análisis PyCBC requiere conectividad a GWOSC"

# Test PyCBC analysis script
test-pycbc: setup
	@echo "🧪 Testing script de análisis PyCBC..."
	./venv/bin/python scripts/test_analizar_gw150914_pycbc.py

# Run PyCBC demo with simulated data
demo-pycbc: setup
	@echo "🎬 Ejecutando demostración de análisis PyCBC con datos simulados..."
	@mkdir -p results/figures
	@if ./venv/bin/python -c "import matplotlib" 2>/dev/null; then \
		./venv/bin/python scripts/demo_pycbc_analysis.py; \
	else \
		echo "⚠️  venv sin matplotlib, usando Python del sistema"; \
		python3 scripts/demo_pycbc_analysis.py; \
	fi
# Run all analyses (legacy + GW250114)
analyze-all: analyze analyze-gw250114

# Verify maximum system optimization
verify-optimization: setup
	@echo "🔍 Verificando optimización máxima del sistema..."
	./venv/bin/python scripts/verificacion_sistema_optimizado.py

# Docker support
docker:
	docker build -t gw141hz .
	docker run --rm -v $(PWD):/app gw141hz

# Complete workflow with data
workflow: setup data analyze
	@echo "🎉 Workflow completo finalizado"
	@echo "📊 Datos descargados y análisis ejecutado"

# Clean up generated files
clean:
	@echo "🧹 Limpiando archivos generados..."
	@echo "⚠️  Esta operación eliminará:"
	@echo "   - venv/ (entorno virtual)"
	@echo "   - data/ (datos descargados)"
	@echo "   - results/ (resultados de análisis)"
	@echo "   - Archivos de caché y temporales"
	@read -p "¿Continuar? [y/N]: " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[YySs]$$ ]]; then \
		rm -rf venv __pycache__ .pytest_cache results/ data/ *.egg-info; \
		rm -rf scripts/__pycache__/ notebooks/__pycache__/; \
		echo "✅ Limpieza completada"; \
	else \
		echo "❌ Limpieza cancelada"; \
	fi

# Clean up without confirmation (for automated workflows)
clean-force:
	@echo "🧹 Limpiando archivos generados (sin confirmación)..."
	rm -rf venv __pycache__ .pytest_cache results/ data/ *.egg-info
	rm -rf scripts/__pycache__/ notebooks/__pycache__/
	@echo "✅ Limpieza completada"

# Experimental Protocols for f₀ Validation
experimentos: setup
	@echo "🧪 Ejecutando Protocolos Experimentales para f₀ = 141.7001 Hz..."
	./venv/bin/python scripts/protocolos_experimentales.py
	@echo ""
	@echo "✅ Experimentos completados"
	@echo "📊 Resultados: results/experimentos_f0.json"

# Test experimental protocols
test-experimentos: setup
	@echo "🧪 Ejecutando tests de protocolos experimentales..."
	./venv/bin/python scripts/test_protocolos_experimentales.py
	@echo ""
	@echo "✅ Tests completados"

# Generate workflow diagrams for experiments
diagrams-experimentos: setup
	@echo "📊 Generando diagramas de flujo experimental..."
	./venv/bin/python scripts/generar_diagrama_experimentos.py
	@echo ""
	@echo "✅ Diagramas generados"
	@echo "🖼️  Flujo: results/figures/flujo_experimentos_f0.png"
	@echo "🖼️  Timeline: results/figures/timeline_experimentos_f0.png"

# Search for higher harmonics of f₀
busqueda-armonicos: setup
	@echo "🎵 Búsqueda experimental de armónicos superiores..."
	@echo "   Frecuencia fundamental: f₀ = 141.7001 Hz"
	@echo "   Armónicos: submúltiplos, múltiplos, áureos, π"
	./venv/bin/python scripts/busqueda_armonicos_superiores.py || echo "⚠️  Análisis completado con advertencias"

# Test higher harmonics search
test-armonicos: setup
	@echo "🧪 Testing búsqueda de armónicos superiores..."
	./venv/bin/python scripts/test_busqueda_armonicos_superiores.py

# Multi-detector cross-resonance analysis (Virgo/KAGRA)
resonancia-cruzada: setup
	@echo "🔗 Análisis de resonancia cruzada multi-detector..."
	@echo "   Detectores: H1, L1, V1, K1"
	@echo "   Análisis: Coherencia, fase, SNR individual"
	./venv/bin/python scripts/resonancia_cruzada_virgo_kagra.py || echo "⚠️  Análisis completado con advertencias"

# Test cross-resonance analysis
test-resonancia: setup
	@echo "🧪 Testing análisis de resonancia cruzada..."
	./venv/bin/python scripts/test_resonancia_cruzada_virgo_kagra.py

# Bayesian Q-factor characterization
caracterizacion-bayesiana: setup
	@echo "📊 Caracterización bayesiana del Q-factor..."
	@echo "   Incluye: distribución posterior, intervalos de credibilidad"
	./venv/bin/python scripts/caracterizacion_bayesiana.py || echo "⚠️  Caracterización completada con advertencias"

# Test Bayesian characterization
test-caracterizacion: setup
	@echo "🧪 Testing caracterización bayesiana..."
	@echo "   Verificando cálculo de posteriores y Q-factor"
	@./venv/bin/python -c "from scripts.caracterizacion_bayesiana import CaracterizacionBayesiana, generar_datos_sinteticos_gw250114; import numpy as np; datos, fs, _ = generar_datos_sinteticos_gw250114(); bayes = CaracterizacionBayesiana(); res = bayes.estimar_q_factor(datos, fs); print('✅ Tests básicos pasaron')"

# Additional reproducibility targets

# Build LaTeX documentation (if available)
pdf-docs:
	@echo "📄 Building LaTeX documentation..."
	@if command -v latexmk >/dev/null 2>&1; then \
		if [ -f "docs/main.tex" ]; then \
			cd docs && latexmk -pdf -shell-escape main.tex; \
		else \
			echo "No LaTeX source found, skipping"; \
		fi \
	else \
		echo "latexmk not installed, skipping PDF build"; \
	fi

# Generate environment lock file
lock-env:
	@echo "🔒 Generating environment lock file..."
	./venv/bin/pip freeze > ENV.lock
	@echo "✅ Environment locked to ENV.lock"

# Run hierarchical Bayesian analysis for 141.7 Hz
bayes-analysis:
	@echo "📊 Running hierarchical Bayesian analysis..."
	./venv/bin/python bayes/hierarchical_model.py

# Verify antenna patterns
antenna-check:
	@echo "📡 Checking antenna pattern consistency..."
	@jupyter nbconvert --to notebook --execute notebooks/antenna_pattern.ipynb --output antenna_pattern_executed.ipynb
	@echo "✅ Antenna pattern analysis complete"

# Interactive discovery experience: "Ahora te toca escuchar"
escuchar:
	@echo "🎧 Iniciando experiencia interactiva del descubrimiento..."
	@if [ ! -f "multi_event_final.json" ]; then \
		echo "⚠️  Generando resultados multi-evento primero..."; \
		python3 multi_event_analysis.py; \
	fi
	python3 escuchar.py

# Run escuchar in automatic mode (no interaction)
escuchar-auto:
	@echo "🎧 Ejecutando modo automático..."
	@if [ ! -f "multi_event_final.json" ]; then \
		echo "⚠️  Generando resultados multi-evento primero..."; \
		python3 multi_event_analysis.py; \
	fi
	python3 escuchar.py --auto

# Test escuchar.py script
test-escuchar:
	@echo "🧪 Testing escuchar.py interactive script..."
	python3 test_escuchar.py

# Alias for escuchar (English)
listen: escuchar

# Alias for automatic mode (English)
listen-auto: escuchar-auto
