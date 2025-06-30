![status: beta](https://img.shields.io/badge/status-beta-orange)

# GateKeeperMCP

> **Beta Software**
> This project is in active development and considered **ALPHA/BETA**.  
> APIs, features, and behavior may change at any time. Use in production is not recommended.

---

GateKeeperMCP is a modular, API-first security gateway framework with policy-as-code controls and support for automated triage, designed for modern enterprise environments. It aims to standardize security guardrails for Model Context Protocol (MCP) applications, providing plugin support and OPA (Open Policy Agent) integration for policy enforcement.

---

## Features

- **API Gateway for MCP**: Proxy and standardize MCP server endpoints
- **Plugin-based Architecture**: Drop-in plugin system for custom security and business logic
- **Open Policy Agent (OPA) Integration**: Enterprise-ready policy-as-code support
- **API Key Security**: Protects endpoints with key-based authentication
- **Automated Triage**: Run triage scripts and serve merged decision outputs via API
- **JSON and File APIs**: Fetch triage results and metadata
- **Engineer-centric Filtering**: Query approval records by engineer, status, and date
- **Status and Health Checks**: Built-in endpoints for monitoring
- **Extensible**: Easy to add new endpoints and plugins

---

## Disclaimer

This software is provided **as-is**, **without warranty** of any kind.  
**Use at your own risk**.  
Features and APIs may change at any time.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourname/GateKeeperMCP.git
cd GateKeeperMCP
```

### 2. (Recommended) Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

1. **Set up your API key**  
   Create a `~/creds.env` file with:

   ```bash
   export TRIAGE_API_KEY=your_api_key_here
   ```

2. **Run the FastAPI app**  
   (You can use `uvicorn` for local development)

   ```bash
   uvicorn triage_api02:app --reload
   ```

3. **Access API docs**  
   Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Key Endpoints

- `POST /triage/run`: Trigger triage run and merge outputs
- `GET /triage/latest`: Download latest merged triage result (file)
- `GET /triage/latest/json`: Get latest triage result as JSON
- `GET /triage/engineer/{engineer}`: Get records for an engineer
- `GET /triage/status`: View last triage job status
- `GET /health`: Health check

**API calls require the `x-api-key` header.**

---

## Development Notes

- **OPA policy files**: Place custom OPA policies in the appropriate plugin/policy directory (see `/plugins`).
- **Plugins**: Drop your custom Python modules or security plugins in `/plugins`.

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

## Contributing

Pull requests and issues are welcome.  
Please open an issue to discuss major changes first.

---

## Authors

- Yu Ming Cheuk, David

---

## Acknowledgments

- Inspired by best practices in API security, modern policy-as-code frameworks, and MCP standardization efforts.
