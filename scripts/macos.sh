#!/usr/bin/env bash
set -euo pipefail

SCRIPT_NAME="$(basename "$0")"
PYTHON_BIN=${PYTHON_BIN:-python}

# Detect whether the script is being sourced
run_mode="executed"
if [[ -n "${BASH_SOURCE:-}" && "${BASH_SOURCE[0]}" != "$0" ]]; then
  run_mode="sourced"
elif [[ -n "${ZSH_EVAL_CONTEXT:-}" && "$ZSH_EVAL_CONTEXT" == *":file"* ]]; then
  run_mode="sourced"
fi

log() { printf '[LiveNeuron macOS] %s\n' "$*"; }

die() {
  log "$*"
  if [[ "$run_mode" == "sourced" ]]; then
    return 1 2>/dev/null || exit 1
  else
    exit 1
  fi
}

usage() {
  cat <<'EOF'
Usage:
  scripts/macos.sh setup              Install libomp (if needed) and run import check
  scripts/macos.sh env                Export env vars (source this to persist)
  scripts/macos.sh run <cmd> [args]   Run a command with env set
  scripts/macos.sh check              Quick import check with env set
  scripts/macos.sh help               Show this help

Env overrides:
  PYTHON_BIN           Python executable to use for checks (default: python)
  LIVENEURON_BASE      Base dir for caches/config (default: ${VIRTUAL_ENV:-$HOME}/.liveneuron)
  _MNE_FAKE_HOME_DIR   Override MNE fake home
  MPLCONFIGDIR         Override Matplotlib config dir
  XDG_CACHE_HOME       Override cache dir
  DYLD_INSERT_LIBRARIES Override libomp injection path
EOF
  if [[ "$run_mode" == "sourced" ]]; then
    return 0
  else
    exit 0
  fi
}

ensure_brew() {
  if ! command -v brew >/dev/null 2>&1; then
    die "Homebrew not found. Install Homebrew first: https://brew.sh/"
  fi
}

ensure_libomp() {
  local mode="${1:-require}"
  if brew ls --versions libomp >/dev/null 2>&1; then
    return 0
  fi
  if [[ "$mode" == "install" ]]; then
    log "Installing libomp via Homebrew..."
    brew install libomp
  else
    die "libomp not installed. Run scripts/macos.sh setup first."
  fi
}

set_env() {
  ensure_brew
  ensure_libomp require

  local libomp_prefix
  libomp_prefix=$(brew --prefix libomp)
  local libomp_dylib="${libomp_prefix}/lib/libomp.dylib"

  local base_dir="${LIVENEURON_BASE:-${VIRTUAL_ENV:-$HOME}/.liveneuron}"
  export _MNE_FAKE_HOME_DIR="${_MNE_FAKE_HOME_DIR:-$base_dir/.mne-home}"
  export MPLCONFIGDIR="${MPLCONFIGDIR:-$base_dir/.matplotlib-config}"
  export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$base_dir/.cache}"
  export DYLD_INSERT_LIBRARIES="${DYLD_INSERT_LIBRARIES:-$libomp_dylib}"

  mkdir -p "$_MNE_FAKE_HOME_DIR" "$MPLCONFIGDIR" "$XDG_CACHE_HOME"
}

cmd_setup() {
  ensure_brew
  ensure_libomp install
  set_env

  log "Using PYTHON_BIN=${PYTHON_BIN}"
  log "DYLD_INSERT_LIBRARIES=${DYLD_INSERT_LIBRARIES}"
  log "Running import check..."

  "$PYTHON_BIN" - <<'PY'
from eelbrain_plotly_viz import EelbrainPlotly2DViz, create_sample_brain_data, __version__
print("LiveNeuron OK, version:", __version__)
PY

  log "Setup complete."
}

cmd_env() {
  set_env
  if [[ "$run_mode" == "sourced" ]]; then
    log "Env exported to current shell."
  else
    log "Env set for this process. To persist, run: source scripts/macos.sh env"
  fi
  log "DYLD_INSERT_LIBRARIES=${DYLD_INSERT_LIBRARIES}"
}

cmd_run() {
  if [[ $# -eq 0 ]]; then
    die "Usage: scripts/macos.sh run <command> [args]"
  fi
  set_env
  log "DYLD_INSERT_LIBRARIES=${DYLD_INSERT_LIBRARIES}"
  exec "$@"
}

cmd_check() {
  set_env
  log "Using PYTHON_BIN=${PYTHON_BIN}"
  log "DYLD_INSERT_LIBRARIES=${DYLD_INSERT_LIBRARIES}"
  "$PYTHON_BIN" - <<'PY'
from eelbrain_plotly_viz import __version__
print("LiveNeuron OK, version:", __version__)
PY
}

main() {
  local cmd="${1:-help}"
  shift || true
  case "$cmd" in
    setup) cmd_setup "$@" ;;
    env) cmd_env "$@" ;;
    run) cmd_run "$@" ;;
    check) cmd_check "$@" ;;
    help|--help|-h) usage ;;
    *) die "Unknown command: $cmd. Run '${SCRIPT_NAME} help' for usage." ;;
  esac
}

main "$@"
