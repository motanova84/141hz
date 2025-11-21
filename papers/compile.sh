#!/bin/bash
# Compilation script for Coherencia Universal LaTeX paper
# Author: José Manuel Mota Burruezo (JMMB Ψϖ)
# Paper: paper_definitivo.tex

set -e  # Exit on error

PAPER="paper_definitivo"
TEX_FILE="${PAPER}.tex"
PDF_FILE="${PAPER}.pdf"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if pdflatex is installed
check_latex() {
    if ! command -v pdflatex &> /dev/null; then
        print_error "pdflatex not found. Please install a LaTeX distribution:"
        echo "  - Ubuntu/Debian: sudo apt-get install texlive-full"
        echo "  - macOS: brew install --cask mactex"
        echo "  - Windows: Install MiKTeX or TeX Live"
        exit 1
    fi
    print_success "pdflatex found: $(which pdflatex)"
}

# Compile the paper
compile_paper() {
    print_info "Compiling ${TEX_FILE}..."
    
    # First pass
    print_info "Running first LaTeX pass..."
    pdflatex -interaction=nonstopmode -halt-on-error "${TEX_FILE}" > /dev/null 2>&1
    
    # Second pass for references
    print_info "Running second LaTeX pass for references..."
    pdflatex -interaction=nonstopmode -halt-on-error "${TEX_FILE}" > /dev/null 2>&1
    
    if [ -f "${PDF_FILE}" ]; then
        print_success "PDF generated successfully: ${PDF_FILE}"
        print_info "File size: $(du -h "${PDF_FILE}" | cut -f1)"
    else
        print_error "PDF generation failed"
        exit 1
    fi
}

# Compile with bibliography
compile_full() {
    print_info "Full compilation with bibliography..."
    
    print_info "Running first LaTeX pass..."
    pdflatex -interaction=nonstopmode -halt-on-error "${TEX_FILE}" > /dev/null 2>&1
    
    if command -v bibtex &> /dev/null; then
        print_info "Running BibTeX..."
        bibtex "${PAPER}" > /dev/null 2>&1 || print_warning "BibTeX encountered warnings"
    else
        print_warning "bibtex not found, skipping bibliography generation"
    fi
    
    print_info "Running second LaTeX pass..."
    pdflatex -interaction=nonstopmode -halt-on-error "${TEX_FILE}" > /dev/null 2>&1
    
    print_info "Running third LaTeX pass..."
    pdflatex -interaction=nonstopmode -halt-on-error "${TEX_FILE}" > /dev/null 2>&1
    
    if [ -f "${PDF_FILE}" ]; then
        print_success "PDF generated successfully: ${PDF_FILE}"
        print_info "File size: $(du -h "${PDF_FILE}" | cut -f1)"
    else
        print_error "PDF generation failed"
        exit 1
    fi
}

# Clean auxiliary files
clean() {
    print_info "Cleaning auxiliary files..."
    rm -f *.aux *.log *.out *.toc *.bbl *.blg *.fdb_latexmk *.fls *.synctex.gz
    print_success "Auxiliary files removed"
}

# Clean everything
distclean() {
    clean
    print_info "Removing PDF..."
    rm -f "${PDF_FILE}"
    print_success "All generated files removed"
}

# Show usage
usage() {
    cat << EOF
Usage: $0 [COMMAND]

Commands:
  compile    - Compile the paper (default)
  full       - Compile with bibliography
  clean      - Remove auxiliary files
  distclean  - Remove all generated files
  help       - Show this help message

Examples:
  $0              # Compile the paper
  $0 full         # Compile with bibliography
  $0 clean        # Clean auxiliary files

Paper: ${TEX_FILE}
Output: ${PDF_FILE}
EOF
}

# Main logic
main() {
    # Check if we're in the right directory
    if [ ! -f "${TEX_FILE}" ]; then
        print_error "${TEX_FILE} not found in current directory"
        print_info "Please run this script from the papers/ directory"
        exit 1
    fi
    
    # Parse command
    COMMAND="${1:-compile}"
    
    case "$COMMAND" in
        compile)
            check_latex
            compile_paper
            ;;
        full)
            check_latex
            compile_full
            ;;
        clean)
            clean
            ;;
        distclean)
            distclean
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            print_error "Unknown command: $COMMAND"
            usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
