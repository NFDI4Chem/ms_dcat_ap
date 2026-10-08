#!/usr/bin/env bash
set -euo pipefail

# Script to build and run the ms_dcat_ap devcontainer with Podman or Docker
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
IMAGE_NAME="ms-dcat-ap-dev"

CONTAINER_TOOL=""
if command -v podman >/dev/null 2>&1; then
  CONTAINER_TOOL="podman"
elif command -v docker >/dev/null 2>&1; then
  CONTAINER_TOOL="docker"
else
  echo "Error: Neither podman nor docker was found in PATH." >&2
  exit 1
fi

build_image() {
  echo "Building devcontainer image '${IMAGE_NAME}' with ${CONTAINER_TOOL}..."
  "${CONTAINER_TOOL}" build \
    -t "${IMAGE_NAME}" \
    -f "${SCRIPT_DIR}/Dockerfile" \
    "${SCRIPT_DIR}"
}

print_help() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS] [COMMAND...]

Run commands or an interactive shell inside the ms_dcat_ap devcontainer using Podman or Docker.

Options:
  --build       Force rebuild of the devcontainer image
  -h, --help    Show this help message

Examples:
  $(basename "$0")                        # Open interactive bash shell in container
  $(basename "$0") just test              # Run all tests inside the container
  $(basename "$0") just gen-project       # Generate project artifacts
  $(basename "$0") just testdoc           # Build and serve docs locally
  $(basename "$0") uv sync --group dev    # Sync dependencies
  $(basename "$0") --build                # Rebuild image before running
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  print_help
  exit 0
fi

if [[ "${1:-}" == "--build" ]]; then
  build_image
  shift
fi

# Build image if it doesn't exist yet
if ! "${CONTAINER_TOOL}" image exists "${IMAGE_NAME}" 2>/dev/null; then
  build_image
fi

EXTRA_ARGS=()
if [[ "${CONTAINER_TOOL}" == "podman" ]]; then
  EXTRA_ARGS+=(
    "--userns=keep-id"
    "--security-opt" "label=disable"
  )
fi

# Interactive TTY allocation if stdin is a terminal
INTERACTIVE_FLAGS=()
if [ -t 0 ]; then
  INTERACTIVE_FLAGS+=("-it")
else
  INTERACTIVE_FLAGS+=("-i")
fi

if [ $# -eq 0 ]; then
  # Default: open bash shell
  exec "${CONTAINER_TOOL}" run "${INTERACTIVE_FLAGS[@]}" --rm \
    "${EXTRA_ARGS[@]}" \
    -p 8000:8000 \
    -v "${WORKSPACE_ROOT}:/workspaces/ms_dcat_ap:Z" \
    -w /workspaces/ms_dcat_ap \
    "${IMAGE_NAME}" \
    bash
else
  # Execute provided command
  exec "${CONTAINER_TOOL}" run "${INTERACTIVE_FLAGS[@]}" --rm \
    "${EXTRA_ARGS[@]}" \
    -p 8000:8000 \
    -v "${WORKSPACE_ROOT}:/workspaces/ms_dcat_ap:Z" \
    -w /workspaces/ms_dcat_ap \
    "${IMAGE_NAME}" \
    "$@"
fi
