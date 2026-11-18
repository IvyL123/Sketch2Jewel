"""Sketch2Jewel 本地服务器：静态文件 + Aholo API 代理（绕开浏览器 CORS）。

用法: py serve.py [port]   （仅绑定 127.0.0.1）
代理: /proxy?url=<urlencoded>  转发任意方法到目标 https 地址，
      回传状态码/头(裁剪)/响应体。仅本机可用。
"""
import sys
import urllib.parse
import urllib.request
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
MAX_BODY = 64 * 1024 * 1024          # 草图/GLB 上传体积上限
BLOCKED_HOST_SUFFIX = ("localhost", "127.0.0.1", "0.0.0.0", "::1", "192.168.", "10.", "172.")

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "S2J/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("[s2j] " + (fmt % args) + "\n")

    # ---- 静态文件 ----
    def _serve_static(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", ""):
            path = "/index.html"
        f = (APP_DIR / path.lstrip("/")).resolve()
        if not str(f).startswith(str(APP_DIR)) or not f.is_file():
            self.send_error(404, "Not Found")
            return
        ctype = {
            ".html": "text/html; charset=utf-8", ".js": "application/javascript",
            ".css": "text/css", ".png": "image/png", ".jpg": "image/jpeg",
            ".webp": "image/webp", ".glb": "model/gltf-binary", ".svg": "image/svg+xml",
        }.get(f.suffix.lower(), "application/octet-stream")
        data = f.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    # ---- 代理 ----
    def _proxy(self):
        qs = urllib.parse.urlparse(self.path).query
        target = urllib.parse.parse_qs(qs).get("url", [""])[0]
        u = urllib.parse.urlparse(target)
        if u.scheme != "https" or not u.hostname:
            self._json(400, '{"error":"proxy requires https URL"}')
            return
        host = u.hostname.lower()
        if any(host.endswith(b) or host == b for b in BLOCKED_HOST_SUFFIX):
            self._json(400, '{"error":"blocked host"}')
            return
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            self._json(413, '{"error":"body too large"}')
            return
        body = self.rfile.read(length) if length else None
        req = urllib.request.Request(target, data=body, method=self.command)
        for h in ("Authorization", "Content-Type", "ous-token-v2", "Accept"):
            v = self.headers.get(h)
            if v:
                req.add_header(h, v)
        req.add_header("User-Agent", "Sketch2Jewel/1.0")
        ctx = ssl.create_default_context()
        try:
            with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
                data = resp.read(MAX_BODY)
                self.send_response(resp.status)
                ct = resp.headers.get("Content-Type", "application/octet-stream")
                self.send_header("Content-Type", ct)
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            data = e.read(MAX_BODY)
            self.send_response(e.code)
            self.send_header("Content-Type", e.headers.get("Content-Type", "application/json"))
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:                                   # noqa: BLE001
            self._json(502, '{"error":"proxy failed: %s"}' % str(e).replace('"', "'"))

    def _json(self, code, s):
        b = s.encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _route(self):
        if self.path.startswith("/proxy?"):
            self._proxy()
        elif self.command in ("GET", "HEAD"):
            self._serve_static()
        else:
            self.send_error(405)

    do_GET = _route
    do_HEAD = _route
    do_POST = _route

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Sketch2Jewel server on http://127.0.0.1:{port}  (proxy ready)")
    srv.serve_forever()
