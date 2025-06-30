![status: alpha](https://img.shields.io/badge/status-alpha-red)

# GateKeeperMCP

> **Alpha Software**
> This project is in its early ALPHA stage and under active development.  
> APIs, features, and security controls are subject to change.  
> **Do not use in production. Use at your own risk.**

---

GateKeeperMCP is an experimental, plugin-based gateway and protocol handler for Model Context Protocol (MCP) systems, designed to provide enterprise-grade security, policy enforcement, and observability between AI/LLM agents, services, or automation clients.

---

## Architecture Overview

GateKeeperMCP consists of three main components:

- **Gateway**: Receives MCP requests, enforces security plugins (auth, OPA policy, RBAC, PII detection, rate limiting, etc.), and proxies to the backend.
- **Server**: Dummy backend that executes MCP commands and returns a response.
- **Client**: Example script that sends MCP commands to the gateway.

---

## Features

- Plugin-based middleware (easy extension with new plugins)
- Enterprise policy-as-code support via OPA (Open Policy Agent)
- Authentication (API key, OIDC)
- Role-Based Access Control (RBAC) and WAF hooks
- PII and prompt safety plugins
- Rate limiting, logging, metrics, and tracing observability
- Registry and signature verification for MCP tools

---

## Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourname/GateKeeperMCP.git
   cd GateKeeperMCP
   ```

2. **(Optional) Start with Docker Compose**

   ```bash
   docker-compose up
   ```

3. **Gateway**
   - Runs on FastAPI (`gatekeeper-gateway/main.py`)
   - Loads plugins from `/plugins`
   - Main endpoint: `POST /execute_mcp` (proxies to server after security checks)

4. **Server**
   - Runs on FastAPI (`gatekeeper-server/main.py`)
   - Accepts `POST /execute` and responds with echo payload

5. **Client**
   - Example script (`gatekeeper-client/main.py`) to send MCP commands to the gateway

---

## Security Disclaimer

- This project is in **alpha** and should **not** be used for production or sensitive environments.
- No guarantee of completeness or security is provided.
- Use at your own risk.

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

## Authors

- Yu M Cheuk (David)

---

## Acknowledgments

- Inspired by enterprise policy-as-code and secure AI gateway design patterns.