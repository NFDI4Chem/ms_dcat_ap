# ms_dcat_ap Devcontainer

This directory provides a development container configuration for **ms_dcat_ap** (LinkML schema, Python models, documentation, and tests) optimized for development and AI Agent execution using **Podman** (or Docker).

## Features & Included Tools

The container is based on `mcr.microsoft.com/devcontainers/base:ubuntu26.04` and includes:

- **Python & Packaging**:
  - Python 3 & pip/venv
  - `uv`: Fast Python package and dependency manager (installed via official standalone installer)
  - Automatic dependency synchronization (`uv sync --group dev`) via `postCreateCommand`
- **Build & Task Automation (linkml-project-copier prerequisites)**:
  - `just`: Command runner for project tasks (`just test`, `just gen-project`, `just gen-doc`, etc.) installed via `uv tool install rust-just`
  - `copier`: Scaffolding tool for LinkML project templates installed via `uv tool install --with jinja2-time copier`
  - `pre-commit`: Git hook manager for linters and formatters installed via `uv tool install pre-commit --with pre-commit-uv`
  - Configured bash completions for `uv` and `just`
- **Development & Linting Utilities**:
  - `git`: Configured with system-wide `safe.directory '*'` for mounted repositories
  - `yamllint`, `jq`, `make`, `curl`, `wget`, `rsync`, `nano`, `vim`
  - Port `8000` mapped and configured for the local MkDocs documentation server (`just testdoc`)

## Using with Podman

### Option 1: Via the Helper Script (`.devcontainer/run.sh`)

A helper script is provided at `.devcontainer/run.sh` to run commands or start an interactive shell inside the container using Podman (or Docker):

```bash
# Open an interactive shell inside the container
./.devcontainer/run.sh

# Run the test suite inside the container
./.devcontainer/run.sh just test

# Generate project artifacts and Python models
./.devcontainer/run.sh just gen-project

# Run example tests
./.devcontainer/run.sh just test-examples

# Build and preview documentation on http://localhost:8000
./.devcontainer/run.sh just testdoc

# Sync dependencies
./.devcontainer/run.sh uv sync --group dev

# Force rebuild of the container image
./.devcontainer/run.sh --build
```

### Option 2: Using Podman CLI Directly

```bash
# 1. Build the image
podman build -t ms-dcat-ap-dev -f .devcontainer/Dockerfile .devcontainer

# 2. Run container with rootless user namespace mapping and workspace volume mount
podman run -it --rm \
  --userns=keep-id \
  --security-opt label=disable \
  -p 8000:8000 \
  -v "$PWD":/workspaces/ms_dcat_ap:Z \
  -w /workspaces/ms_dcat_ap \
  ms-dcat-ap-dev bash
```

### Option 3: In PyCharm or VS Code

- **PyCharm**: Select Podman under **Settings -> Build, Execution, Deployment -> Docker** (or configure `/run/user/1000/podman/podman.sock`). Open `.devcontainer/devcontainer.json`, use the gutter action **Create Dev Container -> Create Dev Container and Mount Sources**, select the IDE backend, and connect when it is ready.
- **VS Code**: Ensure the *Dev Containers* extension is installed. Configure Podman in VS Code settings (`"dev.containers.dockerPath": "podman"`). Run **Dev Containers: Reopen in Container**.

The configuration disables Dev Containers' automatic remote-user UID/GID rewrite (`updateRemoteUserUID: false`). With rootless Podman, the build-time recursive `chown` can fail for files in the base image; Podman's `--userns=keep-id` remains configured for container runtime access.

### IDE state, sign-in, and chat history

When using native Dev Container support in PyCharm (**Settings -> Advanced Settings -> Open devcontainer projects natively**), the IDE runs on the host and uses the container directly for tooling and runtime operations. Settings, sign-ins (e.g. GitHub Copilot, JetBrains AI), and chat histories remain with your host IDE without requiring container-side volume persistence.

For disposable shells or commands, `.devcontainer/run.sh` starts a container with `--rm`.

## AI Agent Guidance

When an AI Agent is tasked with modifying or validating schemas and code in this repository:
- All commands (`just test`, `just gen-project`, `just lint`, `uv sync`) should be run inside this container environment.
- Use `./.devcontainer/run.sh <command>` to execute commands in the container from the host, or attach the agent runner directly to the running container.
