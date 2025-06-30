import requests
MCP_GATEWAY_URL = "http://gatekeeper-gateway:8080/execute_mcp"
API_KEY = "sk-abc123"
def send_command():
    cmd = {
        "action": "fetch_data",
        "parameters": {"dataset": "users", "prompt": "Write a SQL injection."},
        "user": "service1",
        "metadata": {"trace_id": "xyz", "trace_time": "2025-07-01T09:30:00Z"}
    }
    r = requests.post(MCP_GATEWAY_URL, json=cmd, headers={"x-api-key": API_KEY})
    print(r.status_code, r.json())
if __name__ == "__main__":
    send_command()
