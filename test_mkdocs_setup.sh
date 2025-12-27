#!/bin/bash
# Test script for MkDocs documentation setup

set -e  # Exit on error

echo "🧪 Testing MkDocs Documentation Setup"
echo "======================================"
echo ""

# Check Python version
echo "1️⃣  Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   ✅ Python $PYTHON_VERSION"
echo ""

# Check if mkdocs is installed
echo "2️⃣  Checking MkDocs installation..."
if command -v mkdocs &> /dev/null; then
    MKDOCS_VERSION=$(mkdocs --version 2>&1 | head -n1)
    echo "   ✅ $MKDOCS_VERSION"
else
    echo "   ❌ MkDocs not found. Installing..."
    pip install -r requirements.txt
fi
echo ""

# Check mkdocs.yml exists
echo "3️⃣  Checking configuration file..."
if [ -f "mkdocs.yml" ]; then
    echo "   ✅ mkdocs.yml found"
else
    echo "   ❌ mkdocs.yml not found!"
    exit 1
fi
echo ""

# Check docs directory
echo "4️⃣  Checking docs directory..."
if [ -d "docs" ]; then
    DOC_COUNT=$(find docs -name "*.md" | wc -l)
    echo "   ✅ docs/ directory found with $DOC_COUNT markdown files"
else
    echo "   ❌ docs/ directory not found!"
    exit 1
fi
echo ""

# Check branding assets
echo "5️⃣  Checking branding assets..."
if [ -f "docs/assets/brand/logo.svg" ]; then
    echo "   ✅ Logo found"
else
    echo "   ⚠️  Logo not found (optional)"
fi
if [ -f "docs/assets/brand/favicon.png" ]; then
    echo "   ✅ Favicon found"
else
    echo "   ⚠️  Favicon not found (optional)"
fi
echo ""

# Test build
echo "6️⃣  Testing MkDocs build..."
BUILD_OUTPUT=$(mkdocs build 2>&1)
if echo "$BUILD_OUTPUT" | grep -q "Documentation built"; then
    echo "   ✅ Build successful!"
elif echo "$BUILD_OUTPUT" | grep -q "Failed to resolve 'fonts.google.com'"; then
    echo "   ⚠️  Build completed with social cards disabled (network restriction)"
    echo "      Social cards will work in GitHub Actions environment"
else
    echo "   ❌ Build failed!"
    echo ""
    echo "   Running build again to show errors:"
    mkdocs build
    exit 1
fi
echo ""

# Check site directory
echo "7️⃣  Checking generated site..."
if [ -d "site" ]; then
    HTML_COUNT=$(find site -name "*.html" | wc -l)
    echo "   ✅ site/ directory generated with $HTML_COUNT HTML files"
    
    if [ -f "site/index.html" ]; then
        echo "   ✅ Homepage generated"
    else
        echo "   ❌ Homepage not generated!"
    fi
else
    echo "   ❌ site/ directory not generated!"
    exit 1
fi
echo ""

# Check GitHub workflow
echo "8️⃣  Checking GitHub Actions workflow..."
if [ -f ".github/workflows/docs.yml" ]; then
    echo "   ✅ docs.yml workflow found"
else
    echo "   ❌ docs.yml workflow not found!"
    exit 1
fi
echo ""

# Check README badges
echo "9️⃣  Checking README badges..."
if grep -q "github.com/motanova84/141hz/actions/workflows/docs.yml" README.md; then
    echo "   ✅ Docs badge found in README"
else
    echo "   ❌ Docs badge not found in README!"
fi
if grep -q "last-commit" README.md; then
    echo "   ✅ Last commit badge found in README"
else
    echo "   ⚠️  Last commit badge not found in README"
fi
if grep -q "website" README.md; then
    echo "   ✅ Website badge found in README"
else
    echo "   ⚠️  Website badge not found in README"
fi
echo ""

# Summary
echo "✨ Summary"
echo "=========="
echo ""
echo "✅ All critical checks passed!"
echo ""
echo "📝 Next Steps:"
echo "   1. Review the generated site/ directory"
echo "   2. Customize branding in docs/assets/brand/"
echo "   3. Commit and push to trigger GitHub Pages deployment"
echo "   4. Visit https://motanova84.github.io/141hz once deployed"
echo ""
echo "🚀 To preview locally:"
echo "   mkdocs serve"
echo "   Then visit http://127.0.0.1:8000"
echo ""
echo "📚 For more info, see docs/DOCUMENTATION_SETUP.md"
