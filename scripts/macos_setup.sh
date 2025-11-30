#!/usr/bin/env bash
set -euo pipefail

log() { printf '[LiveNeuron setup] %s\n' "$*"; }

PYTHON_BIN=${PYTHON_BIN:-python}

if ! command -v brew >/dev/null 2>&1; then
  log "Homebrew not found. Please install Homebrew first: https://brew.sh/"
  exit 1
fi

if ! brew ls --versions libomp >/dev/null 2>&1; then
  log "Installing libomp via Homebrew..."
  brew install libomp
else
  log "libomp already installed."
fi

libomp_prefix=$(brew --prefix libomp)
libomp_dylib="${libomp_prefix}/lib/libomp.dylib"

export _MNE_FAKE_HOME_DIR="${_MNE_FAKE_HOME_DIR:-$PWD/.mne-home}"
export MPLCONFIGDIR="${MPLCONFIGDIR:-$PWD/.matplotlib-config}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$PWD/.cache}"
export DYLD_INSERT_LIBRARIES="${DYLD_INSERT_LIBRARIES:-$libomp_dylib}"

mkdir -p "$_MNE_FAKE_HOME_DIR" "$MPLCONFIGDIR" "$XDG_CACHE_HOME"

log "Using PYTHON_BIN=${PYTHON_BIN}"
log "DYLD_INSERT_LIBRARIES=${DYLD_INSERT_LIBRARIES}"
log "Running import check..."

"$PYTHON_BIN" - <<'PY'
from eelbrain_plotly_viz import EelbrainPlotly2DViz, create_sample_brain_data, __version__

print("LiveNeuron OK, version:", __version__)
PY

log "Done. Keep this shell (or these env vars) when launching LiveNeuron."
