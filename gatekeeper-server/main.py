from fastapi import FastAPI, Request
app = FastAPI(title="GateKeeperMCP Server")
@app.post("/execute")
async def execute(request: Request):
    body = await request.json()
    return {"status": "executed", "echo": body}
@app.get("/health")
def health():
    return {"status": "ok"}