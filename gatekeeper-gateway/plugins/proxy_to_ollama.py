from flask import Flask, request, Response
import requests

app = Flask(__name__)
OLLAMA_URL = 'http://localhost:11434'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path):
    print(f"Proxying {request.method} /{path}", flush=True)
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}
    resp = requests.request(
        method=request.method,
        url=f"{OLLAMA_URL}/{path}",
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    # Remove hop-by-hop headers, see RFC 2616 section 13.5.1
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded_headers]
    return Response(resp.content, resp.status_code, response_headers)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=18080, debug=True)
