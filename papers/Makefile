# Makefile for LaTeX paper compilation
# Paper: Coherencia Universal - 141.7001 Hz

PAPER = paper_definitivo
TEX = $(PAPER).tex
PDF = $(PAPER).pdf

# LaTeX compiler
LATEX = pdflatex
BIBTEX = bibtex
LATEXMK = latexmk

# Compilation flags
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error

.PHONY: all clean distclean view help

# Default target
all: $(PDF)

# Compile the paper (runs twice for references)
$(PDF): $(TEX)
	@echo "Compiling $(TEX)..."
	$(LATEX) $(LATEX_FLAGS) $(TEX)
	@echo "Running second pass for references..."
	$(LATEX) $(LATEX_FLAGS) $(TEX)
	@echo "PDF generated: $(PDF)"

# Compile with bibliography (full pipeline)
full: $(TEX)
	@echo "Full compilation with bibliography..."
	$(LATEX) $(LATEX_FLAGS) $(TEX)
	$(BIBTEX) $(PAPER)
	$(LATEX) $(LATEX_FLAGS) $(TEX)
	$(LATEX) $(LATEX_FLAGS) $(TEX)
	@echo "PDF generated: $(PDF)"

# Use latexmk for automated compilation
auto: $(TEX)
	@echo "Automated compilation with latexmk..."
	$(LATEXMK) -pdf $(TEX)

# Clean auxiliary files
clean:
	@echo "Cleaning auxiliary files..."
	rm -f *.aux *.log *.out *.toc *.bbl *.blg *.fdb_latexmk *.fls *.synctex.gz

# Clean everything including PDF
distclean: clean
	@echo "Removing PDF..."
	rm -f $(PDF)

# View the PDF (requires PDF viewer)
view: $(PDF)
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(PDF); \
	elif command -v open > /dev/null; then \
		open $(PDF); \
	else \
		echo "No PDF viewer found. Please open $(PDF) manually."; \
	fi

# Check if LaTeX is installed
check:
	@echo "Checking LaTeX installation..."
	@command -v $(LATEX) >/dev/null 2>&1 || { echo "pdflatex not found. Please install a LaTeX distribution."; exit 1; }
	@echo "pdflatex found: $$(which $(LATEX))"
	@command -v $(BIBTEX) >/dev/null 2>&1 && echo "bibtex found: $$(which $(BIBTEX))" || echo "bibtex not found (optional)"
	@command -v $(LATEXMK) >/dev/null 2>&1 && echo "latexmk found: $$(which $(LATEXMK))" || echo "latexmk not found (optional)"

# Show help
help:
	@echo "Makefile for Coherencia Universal LaTeX Paper"
	@echo ""
	@echo "Available targets:"
	@echo "  all        - Compile the paper (default)"
	@echo "  full       - Compile with bibliography"
	@echo "  auto       - Use latexmk for automated compilation"
	@echo "  clean      - Remove auxiliary files"
	@echo "  distclean  - Remove all generated files including PDF"
	@echo "  view       - Open the PDF with default viewer"
	@echo "  check      - Check LaTeX installation"
	@echo "  help       - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make              # Compile the paper"
	@echo "  make full         # Compile with bibliography"
	@echo "  make clean        # Clean auxiliary files"
	@echo "  make view         # View the PDF"
