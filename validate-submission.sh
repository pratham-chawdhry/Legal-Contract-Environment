#!/usr/bin/env bash

set -uo pipefail

# --- Auto-activate virtual environment (robust cross-platform) ---
if [ -d "venv" ]; then
  # Try Windows Git Bash style
  if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
  fi

  # Try Linux/WSL style
  if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
  fi
fi

DOCKER_BUILD_TIMEOUT=600
if [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  BOLD='\033[1m'
  NC='\033[0m'
else
  RED='' GREEN='' YELLOW='' BOLD='' NC=''
fi

run_with_timeout() {
  local secs="$1"; shift
  if command -v timeout &>/dev/null; then
    timeout "$secs" "$@"
  elif command -v gtimeout &>/dev/null; then
    gtimeout "$secs" "$@"
  else
    "$@" &
    local pid=$!
    ( sleep "$secs" && kill "$pid" 2>/dev/null ) &
    local watcher=$!
    wait "$pid" 2>/dev/null
    local rc=$?
    kill "$watcher" 2>/dev/null
    wait "$watcher" 2>/dev/null
    return $rc
  fi
}

portable_mktemp() {
  local prefix="${1:-validate}"
  mktemp "${TMPDIR:-/tmp}/${prefix}-XXXXXX" 2>/dev/null || mktemp
}

CLEANUP_FILES=()
cleanup() { rm -f "${CLEANUP_FILES[@]+"${CLEANUP_FILES[@]}"}"; }
trap cleanup EXIT

PING_URL="${1:-}"
REPO_DIR="${2:-.}"

if [ -z "$PING_URL" ]; then
  printf "Usage: %s <ping_url> [repo_dir]\n" "$0"
  exit 1
fi

if ! REPO_DIR="$(cd "$REPO_DIR" 2>/dev/null && pwd)"; then
  printf "Error: directory '%s' not found\n" "${2:-.}"
  exit 1
fi

PING_URL="${PING_URL%/}"
export PING_URL
PASS=0

log()  { printf "[%s] %b\n" "$(date -u +%H:%M:%S)" "$*"; }
pass() { log "${GREEN}PASSED${NC} -- $1"; PASS=$((PASS + 1)); }
fail() { log "${RED}FAILED${NC} -- $1"; }
hint() { printf "  ${YELLOW}Hint:${NC} %b\n" "$1"; }
stop_at() {
  printf "\n"
  printf "${RED}${BOLD}Validation stopped at %s.${NC}\n" "$1"
  exit 1
}

printf "\n========================================\n"
printf "  OpenEnv Submission Validator\n"
printf "========================================\n"

log "Repo:     $REPO_DIR"
log "Ping URL: $PING_URL"

# ---------------- STEP 1 ----------------
log "Step 1/3: Pinging HF Space ($PING_URL/reset)..."

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Content-Type: application/json" -d '{}' \
  "$PING_URL/reset" --max-time 30 || printf "000")

if [ "$HTTP_CODE" = "200" ]; then
  pass "HF Space is live"
else
  fail "HF Space not reachable"
  stop_at "Step 1"
fi

# ---------------- STEP 2 ----------------
log "Step 2/3: Docker build..."

docker build "$REPO_DIR" -t temp-test >/dev/null 2>&1 && pass "Docker build succeeded" || {
  fail "Docker build failed"
  stop_at "Step 2"
}

# ---------------- STEP 3 ----------------
log "Step 3/3: openenv validate..."

# Use python module instead of relying on PATH
VALIDATE_OK=false
VALIDATE_OUTPUT=$(cd "$REPO_DIR" && python -m openenv validate 2>&1) && VALIDATE_OK=true

if [ "$VALIDATE_OK" = true ]; then
  pass "openenv validate passed"
  echo "$VALIDATE_OUTPUT"
else
  fail "openenv validate failed"
  echo "$VALIDATE_OUTPUT"
  stop_at "Step 3"
fi

printf "\n========================================\n"
printf "  All checks passed! 🚀\n"
printf "========================================\n"