FROM python:3.11

# System deps: bash, git, curl, nodejs 20.x, clean up after install
RUN apt-get update \
    && apt-get install -y bash git curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# App user (for safety)
RUN useradd -m appuser

# Python deps (incl. flask for proxying)
RUN pip install --upgrade pip
RUN pip install fastapi[all] requests python-jose[cryptography] presidio-analyzer presidio-anonymizer flask
RUN python -m spacy download en_core_web_lg
# Install promptfoo as root
RUN npm install -g promptfoo@latest
# Set OLLAMA_BASE_URL so promptfoo always finds the host's Ollama (Mac/Win)
ENV OLLAMA_BASE_URL="http://host.docker.internal:11434"
ENV PATH="/usr/local/bin:${PATH}"

WORKDIR /app

COPY --chown=appuser:appuser main.py .
COPY --chown=appuser:appuser config.yaml .
COPY --chown=appuser:appuser plugins ./plugins
COPY --chown=appuser:appuser schemas ./schemas
COPY --chown=appuser:appuser opa ./opa
COPY --chown=appuser:appuser entrypoint.sh .

USER appuser

ENTRYPOINT ["./entrypoint.sh"]
