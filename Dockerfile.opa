FROM alpine:latest

# Install curl and ca-certificates
RUN apk add --no-cache curl ca-certificates

# Try multiple download sources for OPA ARM64
RUN set -ex; \
    urls=" \
        https://github.com/open-policy-agent/opa/releases/download/v0.60.0/opa_linux_arm64_static \
        https://github.com/open-policy-agent/opa/releases/download/v0.59.0/opa_linux_arm64_static \
        https://github.com/open-policy-agent/opa/releases/download/v0.58.0/opa_linux_arm64_static \
    "; \
    for url in $urls; do \
        echo "Trying $url"; \
        if curl -L -f -o /usr/local/bin/opa "$url"; then \
            chmod +x /usr/local/bin/opa; \
            break; \
        fi; \
    done; \
    test -x /usr/local/bin/opa

# Verify it works
RUN /usr/local/bin/opa version

# Create app directory
RUN mkdir -p /app/opa

EXPOSE 8181 8282
ENTRYPOINT ["/usr/local/bin/opa"]