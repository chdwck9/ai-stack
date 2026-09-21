#!/usr/bin/env bash
set -euo pipefail

AI_ROOT="/Volumes/Live/@Edge/.ai"
HERMES_HOME="${HOME}/.hermes"

echo "==> Installing Hermes Agent"

if ! command -v hermes >/dev/null 2>&1; then
    curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
else
    echo "Hermes already installed: $(hermes --version)"
fi

export PATH="${HOME}/.local/bin:${HOME}/bin:${PATH}"

echo "==> Creating AI directories"

mkdir -p \
    "${AI_ROOT}/config/hermes-webui" \
    "${AI_ROOT}/data/openwebui" \
    "${AI_ROOT}/data/anythingllm" \
    "${AI_ROOT}/data/searxng" \
    "${AI_ROOT}/scripts"

mkdir -p "${HERMES_HOME}"

echo "==> Configuring Hermes"

hermes config set skills.external_dirs "${AI_ROOT}/skills"

echo "==> Configuring API gateway"

hermes config set API_SERVER_ENABLED true

if [ ! -f "${HERMES_HOME}/.env" ]; then
    touch "${HERMES_HOME}/.env"
    chmod 600 "${HERMES_HOME}/.env"
fi

if ! grep -q '^API_SERVER_KEY=' "${HERMES_HOME}/.env"; then
    API_KEY="$(openssl rand -hex 32)"
    printf 'API_SERVER_KEY=%s\n' "${API_KEY}" >> "${HERMES_HOME}/.env"
fi

if ! grep -q '^API_SERVER_HOST=' "${HERMES_HOME}/.env"; then
    printf 'API_SERVER_HOST=0.0.0.0\n' >> "${HERMES_HOME}/.env"
fi

if ! grep -q '^API_SERVER_PORT=' "${HERMES_HOME}/.env"; then
    printf 'API_SERVER_PORT=8642\n' >> "${HERMES_HOME}/.env"
fi

echo
echo "==> Hermes installation complete"
echo
echo "Hermes:"
hermes --version
echo
echo "Config:"
echo "  ${HERMES_HOME}/config.yaml"
echo
echo "Secrets:"
echo "  ${HERMES_HOME}/.env"
echo
echo "Skills:"
echo "  ${AI_ROOT}/skills"