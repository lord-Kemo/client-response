#!/usr/bin/env python3
"""Local server for Valor AI client confirmation form.

Serves files from current directory and stores form submissions under ./responses.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


RESPONSES_DIR = Path("responses")


class FormHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/submit":
            self.send_error(HTTPStatus.NOT_FOUND, "Route not found")
            return

        content_length = self.headers.get("Content-Length")
        if not content_length:
            self.send_error(HTTPStatus.BAD_REQUEST, "Missing Content-Length")
            return

        try:
            length = int(content_length)
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON body")
            return

        RESPONSES_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        output_name = f"response_{timestamp}.json"
        output_path = RESPONSES_DIR / output_name

        envelope = {
            "savedAt": datetime.now().isoformat(),
            "clientIp": self.client_address[0] if self.client_address else "unknown",
            "data": payload,
        }

        output_path.write_text(json.dumps(envelope, indent=2, ensure_ascii=True), encoding="utf-8")

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

        response = {"ok": True, "fileName": output_name}
        self.wfile.write(json.dumps(response).encode("utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local Valor AI form server")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), FormHandler)

    print(f"Serving on http://{args.host}:{args.port}")
    print("Open: http://localhost:{port}/client.html".format(port=args.port))
    print("Submissions are saved under ./responses")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
