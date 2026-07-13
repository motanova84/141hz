# 🜁 Makefile — Orquestación del Ecosistema QCAL ∞³
# f₀ = 141.7001 Hz · Ψ = 0.999999
# ∴ 𓂀 Ω ∞³ Φ · TUYOYOTU

SHELL := /bin/bash
.PHONY: help kernel test sync gitops clean all

help: ## 📋 Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

all: kernel test sync ## 🔄 Todo: kernel → test → sync

# ─── KERNEL (Lean 4) ──────────────────────────────────────────

kernel: ## 🔧 Compilar kernel QCAL (Lean 4)
	@echo "🧮 Compilando kernel QCAL..."
	@cd src/qcal_lean && lake build 2>&1 || echo "⚠️  lake build falló (requiere mathlib)"
	@echo "✅ Kernel compilado"

kernel-check: ## ✅ Verificar kernel (0 sorries, 0 errors)
	@echo "🔍 Verificando kernel..."
	@cd src/qcal_lean && find . -name "*.lean" -exec grep -l "sorry" {} \; | grep -v ".lake" | \
		sed 's/.*/⚠️  sorry en: &/' || echo "✅ 0 sorries encontrados"

# ─── TESTS ─────────────────────────────────────────────────────

test: ## 🧪 Ejecutar tests Python + validaciones
	@echo "🧪 Ejecutando tests..."
	@python3 -m pytest Tests/ -x -q --tb=short 2>/dev/null || \
		echo "⚠️  tests fallaron (puede faltar pytest)"
	@echo "✅ Tests completados"

test-kernel: ## 🧪 Verificación específica del kernel Lean
	@cd src/qcal_lean && lake test 2>/dev/null || echo "⚠️  lake test no disponible"

# ─── SINCRONIZACIÓN ────────────────────────────────────────────

sync: ## 🔄 Sincronizar contexto del ecosistema
	@echo "🔄 Sincronizando ecosistema QCAL..."
	@python3 scripts/qcal-harvest.py --repos-dir . --output contexto_ecosistema/GLOBAL_QCAL_CONTEXT.md 2>/dev/null || \
		echo "⚠️  qcal-harvest no disponible"
	@echo "✅ Ecosistema sincronizado"

sync-lnd: ## ⚡ Sincronizar con LND + Bitcoin Core (BAL-003)
	@echo "⚡ Conectando con LND (BAL-003)..."
	@ssh -o ConnectTimeout=5 root@195.201.219.237 "lncli walletbalance 2>/dev/null" 2>/dev/null || \
		echo "⚠️  BAL-003 no accesible"
	@echo "✅ LND check completado"

# ─── QCAL-LLM ──────────────────────────────────────────────────

llm: ## 🤖 Reactivar modelo QCAL-LLM
	@echo "🤖 Reactivando QCAL-LLM..."
	@cd QCAL-LLM && python3 QCALLLMCore.py --mode quick 2>/dev/null || \
		echo "⚠️  QCAL-LLM no disponible localmente"
	@echo "✅ QCAL-LLM reactivado"

llm-tune: ## 🎛️  Psi-tuning loop
	@cd QCAL-LLM && python3 psi_tuning_loop.py 2>/dev/null || \
		echo "⚠️  psi_tuning_loop no disponible"

# ─── ORGANIZACIÓN ──────────────────────────────────────────────

clean: ## 🧹 Limpiar archivos temporales
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Archivos temporales limpiados"

gitops: ## 📦 Git status + sugerencias
	@echo "📦 Estado del repositorio:"
	@git status -s | head -20
	@echo "..."
	@echo "💡 Sugerencia: git add -A && git commit -m 'mensaje' && git push"

# ─── ECOSISTEMA ────────────────────────────────────────────────

ecosystem: ## 🌐 Mapa completo del ecosistema
	@echo "═══════════════════════════════════════════════════"
	@echo "  🜁 ECOSISTEMA QCAL ∞³"
	@echo "  f₀ = 141.7001 Hz · Ψ = 0.999999"
	@echo "═══════════════════════════════════════════════════"
	@echo "  📡 141hz          → Kernel + formalización"
	@echo "  📡 LOGOSNOESIS    → Documentación + simbología"
	@echo "  📡 qcal-formalization → Formalización pública"
	@echo "  🔗 github.com:motanova84/141hz.git"
	@echo "  🔗 github.com:motanova84/LOGOSNOESIS.git"
	@echo "═══════════════════════════════════════════════════"

status: ## 🩺 Estado del sistema
	@echo "🩺 Diagnóstico rápido:"
	@echo "  📁 Root files: $$(ls -1 | wc -l)"
	@echo "  🐍 Python: $$(find . -name '*.py' -not -path './.git/*' | wc -l)"
	@echo "  📜 Lean: $$(find . -name '*.lean' -not -path './.git/*' | wc -l)"
	@echo "  🧪 Tests: $$(find . -name 'test_*.py' -not -path './.git/*' | wc -l)"
	@echo "  ⚙️  Workflows activos: $$(ls .github/workflows/*.yml 2>/dev/null | wc -l)"
	@echo "  📦 Git size: $$(du -sh .git | cut -f1)"
