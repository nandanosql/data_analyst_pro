#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# data-init.sh — Initialize Data Analysis Workspace
# Creates directories, checks Python, installs dependencies, validates setup.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${CYAN}${BOLD}"
echo "╔═══════════════════════════════════════════════╗"
echo "║   📊 Data Analyst Pro — Workspace Setup       ║"
echo "╚═══════════════════════════════════════════════╝"
echo -e "${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# ─── Step 1: Check Python ──────────────────────────────────────────────────────

echo -e "${BLUE}[1/5]${NC} Checking Python installation..."

PYTHON_CMD=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        version=$("$cmd" --version 2>&1 | awk '{print $2}')
        major=$(echo "$version" | cut -d. -f1)
        minor=$(echo "$version" | cut -d. -f2)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 9 ]; then
            PYTHON_CMD="$cmd"
            echo -e "  ${GREEN}✓${NC} Found $cmd $version"
            break
        else
            echo -e "  ${YELLOW}⚠${NC} $cmd $version found but need ≥ 3.9"
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo -e "  ${RED}✗ Python 3.9+ not found${NC}"
    echo "  Please install Python 3.9 or later: https://www.python.org/downloads/"
    exit 1
fi

# ─── Step 2: Create Directories ────────────────────────────────────────────────

echo -e "${BLUE}[2/5]${NC} Creating directory structure..."

DIRS=(
    "data"
    "output/charts"
    "output/cleaned"
    "reports"
    "queries"
)

for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "  ${GREEN}✓${NC} Created $dir/"
    else
        echo -e "  ${YELLOW}○${NC} $dir/ already exists"
    fi
done

# ─── Step 3: Install Python Dependencies ───────────────────────────────────────

echo -e "${BLUE}[3/5]${NC} Installing Python dependencies..."

if [ -f "requirements.txt" ]; then
    $PYTHON_CMD -m pip install -r requirements.txt --quiet 2>&1 | tail -5
    echo -e "  ${GREEN}✓${NC} Dependencies installed"
else
    echo -e "  ${RED}✗ requirements.txt not found${NC}"
    exit 1
fi

# ─── Step 4: Validate Scripts ──────────────────────────────────────────────────

echo -e "${BLUE}[4/5]${NC} Validating scripts..."

SCRIPTS=(
    "scripts/analyze.py"
    "scripts/visualize.py"
    "scripts/clean.py"
    "scripts/report.py"
)

all_valid=true
for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        if $PYTHON_CMD -c "import py_compile; py_compile.compile('$script', doraise=True)" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} $script"
        else
            echo -e "  ${RED}✗${NC} $script — syntax error"
            all_valid=false
        fi
    else
        echo -e "  ${RED}✗${NC} $script — not found"
        all_valid=false
    fi
done

if [ "$all_valid" = false ]; then
    echo -e "\n  ${YELLOW}⚠ Some scripts have issues. Check above for details.${NC}"
fi

# ─── Step 5: Verify Dependencies ──────────────────────────────────────────────

echo -e "${BLUE}[5/5]${NC} Verifying Python packages..."

PACKAGES=("pandas" "matplotlib" "seaborn" "scipy" "numpy" "openpyxl" "tabulate" "jinja2")

for pkg in "${PACKAGES[@]}"; do
    if $PYTHON_CMD -c "import $pkg" 2>/dev/null; then
        version=$($PYTHON_CMD -c "import $pkg; print($pkg.__version__)" 2>/dev/null || echo "?")
        echo -e "  ${GREEN}✓${NC} $pkg ($version)"
    else
        echo -e "  ${RED}✗${NC} $pkg — not installed"
    fi
done

# ─── Summary ───────────────────────────────────────────────────────────────────

echo ""
echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}${BOLD}  ✓ Workspace ready!${NC}"
echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${BOLD}Quick Start:${NC}"
echo -e "  ${YELLOW}$PYTHON_CMD scripts/analyze.py --input examples/sample_data.csv${NC}"
echo -e "  ${YELLOW}$PYTHON_CMD scripts/clean.py --input examples/sample_data.csv --audit${NC}"
echo -e "  ${YELLOW}$PYTHON_CMD scripts/visualize.py --input examples/sample_data.csv --auto${NC}"
echo -e "  ${YELLOW}$PYTHON_CMD scripts/report.py --input examples/sample_data.csv --charts${NC}"
echo ""
