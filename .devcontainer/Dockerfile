FROM mcr.microsoft.com/devcontainers/base:ubuntu26.04

# Prevent interactive prompts during apt installations
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Install base utilities and Python tooling
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash-completion \
    ca-certificates \
    curl \
    git \
    gnupg \
    jq \
    less \
    make \
    nano \
    procps \
    python3 \
    python3-pip \
    python3-venv \
    rsync \
    sudo \
    tar \
    unzip \
    vim \
    wget \
    yamllint \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install uv via official standalone installer (https://docs.astral.sh/uv/getting-started/installation/)
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh

# Install tools recommended by linkml-project-copier via uv tool as system-wide tools
ENV UV_TOOL_DIR=/usr/local/share/uv/tools \
    UV_TOOL_BIN_DIR=/usr/local/bin
RUN uv tool install rust-just \
    && uv tool install --with jinja2-time copier \
    && uv tool install pre-commit --with pre-commit-uv \
    && chmod -R a+rx /usr/local/share/uv /usr/local/bin \
    && just --version \
    && copier --version \
    && pre-commit --version

# Configure bash completion and git safe directory
RUN mkdir -p /etc/bash_completion.d \
    && uv generate-shell-completion bash > /etc/bash_completion.d/uv \
    && just --completions bash > /etc/bash_completion.d/just \
    && git config --system --add safe.directory '*'

WORKDIR /workspaces/ms_dcat_ap
USER vscode
