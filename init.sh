#!/usr/bin/env bash
# init.sh — project-executive-dashboard-data (Python, BI/Data)
set -euo pipefail

PASS=0; FAIL=0
green() { echo -e "\033[32m✓ $1\033[0m"; }
red()   { echo -e "\033[31m✗ $1\033[0m"; }
warn()  { echo -e "\033[33m⚠ $1\033[0m"; }
info()  { echo -e "\033[36m→ $1\033[0m"; }
check() { local l="$1"; shift; if "$@" &>/dev/null; then green "$l"; PASS=$((PASS + 1)); else red "$l"; FAIL=$((FAIL + 1)); fi; }

echo ""; info "project-executive-dashboard-data — verificación pre-sesión"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""; info "Estructura"
check "generate_data.py existe"  test -f "generate_data.py"
check "README.md existe"         test -f "README.md"
check "CLAUDE.md en .gitignore"  grep -q "CLAUDE.md" ".gitignore"

[ ! -d ".claude/progress" ] && mkdir -p ".claude/progress" && warn ".claude/progress creado" || { green ".claude/progress existe"; PASS=$((PASS + 1)); }

echo ""; info "Python — librerías"
check "pandas disponible"  python3 -c "import pandas"
check "numpy disponible"   python3 -c "import numpy"

echo ""; info "Sintaxis"
find . -name "*.py" -not -path "./.git/*" -not -path "./node_modules/*" | while read f; do
  python3 -m py_compile "$f" 2>/dev/null || { red "Sintaxis: $f"; FAIL=$((FAIL + 1)); }
done
[ "$FAIL" -eq 0 ] && { green "Todos los .py compilan OK"; PASS=$((PASS + 1)); }

echo ""; info "Git"
UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
[ "$UNCOMMITTED" -gt 0 ] && warn "$UNCOMMITTED archivo(s) sin commit" || { green "Working tree limpio"; PASS=$((PASS + 1)); }

echo ""; echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Resultado: $PASS ✓  $FAIL ✗"
[ "$FAIL" -gt 0 ] && { red "PROYECTO EN MAL ESTADO — Resuelve los errores antes de continuar"; exit 1; } || { green "Proyecto verificado — puedes empezar"; exit 0; }
