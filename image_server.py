#!/usr/bin/env python3
"""
Simple Image Browser HTTP server
- Serves a directory of images (like `python -m http.server`)
- Image view page with Prev / Next navigation
- Delete button (POST) to remove current image

Usage:
  python image_server.py --dir /path/to/images --port 8000

Security notes:
- Designed for local use. It prevents path traversal by resolving paths and
  ensuring they stay within the configured root directory.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote, unquote
from pathlib import Path
from typing import Optional, List
import argparse
import mimetypes
import html
import sys

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

def list_images(root: Path) -> List[str]:
    image_files = [p.name for p in root.iterdir() if is_image_file(p)]
    return sorted(image_files, key=str.lower)

def is_image_file(path: Path) -> bool:
    is_file = path.is_file()
    has_image_extension = path.suffix.lower() in IMAGE_EXTS
    return is_file and has_image_extension

def is_safe_child(parent: Path, child: Path) -> bool:
    resolved_parent = parent.resolve()
    resolved_child = child.resolve()
    return is_child_of_parent(resolved_parent, resolved_child)

def is_child_of_parent(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False

def get_server_ip(ip: Optional[str]) -> str:
    if ip is not None:
        return ip
    return '127.0.0.1'

def get_server_port(port: Optional[int]) -> int:
    if port is not None:
        return port
    return 8000

def create_server_address(ip: str, port: int) -> tuple:
    return (ip, port)

class ImageRequestHandler(BaseHTTPRequestHandler):
    server_version = "ImageHTTP/0.2"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index"):
            return self.page_index()
        elif parsed.path == "/view":
            return self.page_view()
        elif parsed.path == "/raw":
            return self.serve_raw()
        elif parsed.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/delete":
            return self.handle_delete()
        else:
            self.send_error(404, "Not Found")

    def get_query(self):
        parsed = urlparse(self.path)
        return parse_qs(parsed.query)

    def send_html(self, html_text: str, *, status: int = 200):
        data = html_text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def redirect(self, location: str, status: int = 303):
        self.send_response(status)
        self.send_header("Location", location)
        self.end_headers()

    def page_index(self):
        server_root = self.get_server_root()
        imgs = list_images(server_root)
        rows = []
        if not imgs:
            rows.append('<div class="empty">No images in this folder.</div>')
        for name in imgs:
            esc = html.escape(name)
            url = f"/view?name={quote(name)}"
            thumb = f"/raw?name={quote(name)}"
            rows.append(f'<a class="card" href="{url}"><img loading="lazy" src="{thumb}" alt="{esc}"><div class="meta">{esc}</div></a>')
        content = "\n".join(rows)
        self.send_html(self.wrap_html(f"""
        <header><h1>Image Browser</h1><div class='muted'>Root: {html.escape(str(server_root))}</div></header>
        <main class='grid'>{content}</main>
        <footer>Tip: Use ← / → or D to delete image.</footer>
        """))

    def page_view(self):
        q = self.get_query()
        name = q.get("name", [None])[0]
        if not name:
            return self.redirect("/")
        file = (self.get_server_root() / name)
        if not is_safe_child(self.get_server_root(), file) or not file.exists():
            return self.send_error(404, "Image not found")

        imgs = list_images(self.get_server_root())
        if name not in imgs:
            return self.redirect("/")

        idx = imgs.index(name)
        prev_name = imgs[idx - 1] if idx > 0 else imgs[-1]
        next_name = imgs[idx + 1] if idx < len(imgs) - 1 else imgs[0]

        def view_url(n):
            return f"/view?name={quote(n)}"

        img_url = f"/raw?name={quote(name)}"
        self.send_html(self.wrap_html(f"""
        <header><a class='btn' href='/'>⟵ Back</a><div class='spacer'></div><div class='crumb'>{html.escape(name)}</div></header>
        <main class='viewer'>
          <a class='nav prev' href='{view_url(prev_name)}' title='Previous (←)'>◀</a>
          <img src='{img_url}' alt='{html.escape(name)}'>
          <a class='nav next' href='{view_url(next_name)}' title='Next (→)'>▶</a>
        </main>
        <form class='toolbar' method='POST' action='/delete'>
          <input type='hidden' name='name' value='{html.escape(name)}'>
          <button class='btn danger' type='submit' title='Delete (D)'>🗑 Delete</button>
          <a class='btn' href='{view_url(prev_name)}'>⬅ Prev</a>
          <a class='btn' href='{view_url(next_name)}'>Next ➡</a>
          <div class='muted'>{idx+1} / {len(imgs)}</div>
        </form>
        <script>
          document.addEventListener('keydown', function(e){{
            if(e.key==='ArrowLeft'){{ e.preventDefault(); window.location='{view_url(prev_name)}'; }}
            else if(e.key==='ArrowRight'){{ e.preventDefault(); window.location='{view_url(next_name)}'; }}
            else if(e.key==='d' || e.key==='D' || e.key==='Delete'){{ e.preventDefault(); document.forms[0].submit(); }}
          }});
        </script>
        """))

    def serve_raw(self):
        q = self.get_query()
        name = q.get("name", [None])[0]
        if not name:
            return self.send_error(400, "Missing 'name'")
        file = (self.get_server_root() / name)
        if not is_safe_child(self.get_server_root(), file) or not file.exists():
            return self.send_error(404, "Not Found")
        ctype, _ = mimetypes.guess_type(str(file))
        ctype = ctype or "application/octet-stream"
        with open(file, 'rb') as f:
            data = f.read()
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def handle_delete(self):
        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length).decode('utf-8') if length else ''
        params = parse_qs(body)
        name = params.get('name', [None])[0]
        if not name:
            return self.send_error(400, "Missing 'name'")
        file = (self.get_server_root() / unquote(name))
        if not is_safe_child(self.get_server_root(), file) or not file.exists():
            return self.send_error(404, "Not Found")

        imgs_before = list_images(self.get_server_root())
        try:
            idx = imgs_before.index(unquote(name))
        except ValueError:
            idx = 0

        try:
            file.unlink()
        except Exception as e:
            return self.send_error(500, f"Failed to delete: {e}")

        imgs_after = list_images(self.get_server_root())
        if not imgs_after:
            return self.redirect("/")
        next_idx = idx if idx < len(imgs_after) else len(imgs_after) - 1
        target = imgs_after[next_idx]
        return self.redirect(f"/view?name={quote(target)}")

    def wrap_html(self, body: str) -> str:
        return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Image Browser</title>
<style>
  :root{{--bg:#0b1020;--muted:#9aa0aa;--text:#e5e7eb;}}
  body{{margin:0;background:#0b1020;color:var(--text);font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif}}
  header{{display:flex;align-items:center;gap:12px;padding:12px 14px;border-bottom:1px solid #1f2937;background:rgba(0,0,0,.25)}}
  h1{{font-size:16px;margin:0;color:#cbd5e1}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;padding:14px}}
  .card{{display:flex;flex-direction:column;gap:8px;text-decoration:none;color:inherit;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:10px;transition:transform .06s,background .2s}}
  .card:hover{{background:rgba(255,255,255,.06);transform:translateY(-1px)}}
  .card img{{width:100%;height:150px;object-fit:cover;border-radius:8px}}
  .viewer{{position:relative;min-height:70vh;display:grid;place-items:center;padding:10px}}
  .viewer img{{max-width:95vw;max-height:75vh;border-radius:12px;box-shadow:0 8px 28px rgba(0,0,0,.35)}}
  .nav{{position:absolute;top:50%;transform:translateY(-50%);font-size:26px;text-decoration:none;color:#e5e7eb;background:rgba(0,0,0,.35);padding:10px 12px;border-radius:10px;border:1px solid rgba(255,255,255,.1)}}
  .nav.prev{{left:12px}}.nav.next{{right:12px}}
  .toolbar{{display:flex;gap:8px;align-items:center;justify-content:center;padding:12px;border-top:1px solid #1f2937}}
  .btn{{appearance:none;border:1px solid rgba(255,255,255,.12);background:#0b1220;color:#e7e7eb;padding:8px 12px;border-radius:10px;text-decoration:none;cursor:pointer}}
  .btn.danger{{background:linear-gradient(180deg,#ef4444,#b91c1c);border-color:rgba(0,0,0,.25)}}
  footer{{padding:10px 14px;color:#9aa0aa;border-top:1px solid #1f2937;text-align:center}}
  .muted{{color:#9aa0aa;font-size:12px}}
  .spacer{{flex:1}}
  .crumb{{font-size:13px;color:#cbd5e1;max-width:60ch;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
  .empty{{padding:24px;color:#9aa0aa}}
</style></head><body>{body}</body></html>"""

    def get_server_root(self) -> Path:
        return self.server.root  # type: ignore[attr-defined]

def create_http_server(ip: str, port: int, root: Path) -> HTTPServer:
    server_address = create_server_address(ip, port)
    httpd = HTTPServer(server_address, ImageRequestHandler)
    assign_root_to_server(httpd, root)
    return httpd

def assign_root_to_server(httpd: HTTPServer, root: Path) -> None:
    httpd.root = root  # type: ignore[attr-defined]

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Image Server")
    add_arguments_to_parser(parser)
    return parser.parse_args()

def add_arguments_to_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--dir', required=True, help='Directory to serve')
    parser.add_argument('--ip', default=None, help='IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='Port (default: 8000)')

def print_startup_message(ip: str, port: int) -> None:
    print(f"Server running at http://{ip}:{port}/")
    print("Press Ctrl+C to exit.")

def start_server(httpd: HTTPServer) -> None:
    httpd.serve_forever()

def main() -> None:
    args = parse_arguments()
    root_path = Path(args.dir)
    ip = get_server_ip(args.ip)
    port = get_server_port(args.port)
    print_startup_message(ip, port)
    httpd = create_http_server(ip, port, root_path)
    start_server(httpd)

if __name__ == "__main__":
    main()
