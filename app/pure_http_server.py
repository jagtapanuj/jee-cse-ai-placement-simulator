from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .simulator_core import compare, list_programs, simulate, source_drawer

ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"


def _bool(value: str | None) -> bool:
    return str(value or "").lower() in {"1", "true", "yes", "y"}


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path):
        if not path.exists() or not path.is_file():
            self.send_error(404)
            return
        suffix = path.suffix.lower()
        content_type = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
        }.get(suffix, "text/plain; charset=utf-8")
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        path = parsed.path
        try:
            if path == "/api/health":
                return self._send_json({"status": "ok", "data_version": "maharashtra-v6-localapp-v7"})
            if path == "/api/programs":
                return self._send_json({"programs": list_programs(_bool(params.get("include_partial", [""])[0]))})
            if path == "/api/simulate":
                rank_raw = params.get("rank", [None])[0]
                rank = int(rank_raw) if rank_raw else None
                return self._send_json(simulate(
                    rank=rank,
                    rank_type=params.get("rank_type", ["UNKNOWN"])[0],
                    include_partial=_bool(params.get("include_partial", [""])[0]),
                    branch_query=params.get("branch", [None])[0],
                    max_results=int(params.get("max_results", ["25"])[0]),
                ))
            if path.startswith("/api/sources/"):
                return self._send_json(source_drawer(path.rsplit("/", 1)[-1]))
            if path == "/" or path == "/index.html":
                return self._send_file(FRONTEND_DIR / "index.html")
            frontend_path = (FRONTEND_DIR / path.lstrip("/")).resolve()
            if str(frontend_path).startswith(str(FRONTEND_DIR.resolve())):
                return self._send_file(frontend_path)
            self.send_error(404)
        except Exception as exc:
            self._send_json({"error": str(exc)}, status=400)


def run(host="127.0.0.1", port=8000):
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Serving local simulator at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
