"""HTTP request handlers for the image server."""

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote, unquote
from pathlib import Path
from typing import Dict, Optional
import mimetypes
import html

from image_server.path_utils import list_images, is_safe_child
from image_server.template_loader import TemplateLoader


class ImageRequestHandler(BaseHTTPRequestHandler):
    server_version = "ImageHTTP/0.2"

    def __init__(self, *args, **kwargs) -> None:
        templates_dir = Path(__file__).parent / "templates"
        self._template_loader = TemplateLoader(templates_dir)
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        route_handlers = self._get_route_handlers()
        handler = route_handlers.get(parsed.path)

        if handler:
            handler()
        elif parsed.path.startswith("/static/"):
            self.serve_static()
        elif parsed.path == "/favicon.ico":
            self._handle_favicon()
        else:
            self.send_error(404, "Not Found")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/delete":
            self.handle_delete()
        else:
            self.send_error(404, "Not Found")

    def page_index(self) -> None:
        server_root = self.get_server_root()
        images = list_images(server_root)
        content = self._build_index_content(images)
        context = self._create_index_context(server_root, content)
        html_output = self._template_loader.render_template("index.html", context)
        self.send_html(html_output)

    def page_view(self) -> None:
        query_params = self.get_query()
        name = query_params.get("name", [None])[0]

        if not name:
            self.redirect("/")
            return

        if not self._is_valid_image_file(name):
            self.send_error(404, "Image not found")
            return

        view_data = self._prepare_view_data(name)
        if view_data is None:
            self.redirect("/")
            return

        context = self._create_view_context(view_data)
        html_output = self._template_loader.render_template("view.html", context)
        self.send_html(html_output)

    def serve_raw(self) -> None:
        query_params = self.get_query()
        name = query_params.get("name", [None])[0]

        if not name:
            self.send_error(400, "Missing 'name'")
            return

        file_path = self.get_server_root() / name

        if not self._is_accessible_file(file_path):
            self.send_error(404, "Not Found")
            return

        self._send_file_response(file_path)

    def serve_static(self) -> None:
        parsed = urlparse(self.path)
        static_path = parsed.path.replace("/static/", "")

        if not self._is_safe_static_path(static_path):
            self.send_error(404, "Not Found")
            return

        templates_dir = Path(__file__).parent / "templates"
        file_path = templates_dir / static_path

        if not file_path.exists() or not file_path.is_file():
            self.send_error(404, "Not Found")
            return


        self._send_file_response(file_path)

    def handle_delete(self) -> None:
        name = self._extract_delete_target()

        if not name:
            self.send_error(400, "Missing 'name'")
            return

        file_path = self.get_server_root() / unquote(name)

        if not self._is_accessible_file(file_path):
            self.send_error(404, "Not Found")
            return

        next_target = self._delete_and_get_next(name, file_path)
        self.redirect(next_target)

    def get_query(self) -> Dict:
        parsed = urlparse(self.path)
        return parse_qs(parsed.query)

    def send_html(self, html_text: str, status: int = 200) -> None:
        data = html_text.encode("utf-8")
        self._send_html_response(data, status)

    def redirect(self, location: str, status: int = 303) -> None:
        self.send_response(status)
        self.send_header("Location", location)
        self.end_headers()

    def get_server_root(self) -> Path:
        return self.server.root

    def _get_route_handlers(self) -> Dict:
        return {
            "/": self.page_index,
            "/index": self.page_index,
            "/view": self.page_view,
            "/raw": self.serve_raw,
        }

    def _handle_favicon(self) -> None:
        self.send_response(204)
        self.end_headers()

    def _build_index_content(self, images: list) -> str:
        if not images:
            return '<div class="empty">No images in this folder.</div>'

        rows = [self._create_image_card(name) for name in images]
        return "\n".join(rows)

    def _create_image_card(self, name: str) -> str:
        escaped_name = html.escape(name)
        view_url = f"/view?name={quote(name)}"
        thumb_url = f"/raw?name={quote(name)}"
        js_escaped_name = escaped_name.replace("'", "\\'")

        trash_icon = '<svg viewBox="0 0 16 16"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/><path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/></svg>'

        return (
            f'<div class="card">'
            f'<button class="delete-btn" onclick="deleteImage(event, \'{js_escaped_name}\', true)" title="Delete">{trash_icon}</button>'
            f'<a class="card-link" href="{view_url}">'
            f'<img loading="lazy" src="{thumb_url}" alt="{escaped_name}">'
            f'<div class="meta">{escaped_name}</div></a></div>'
        )

    def _create_index_context(self, server_root: Path, content: str) -> Dict[str, str]:
        return {
            "root_path": html.escape(str(server_root)),
            "content": content,
        }

    def _is_valid_image_file(self, name: str) -> bool:
        file_path = self.get_server_root() / name
        is_safe = is_safe_child(self.get_server_root(), file_path)
        file_exists = file_path.exists()
        return is_safe and file_exists

    def _prepare_view_data(self, name: str) -> Optional[Dict]:
        images = list_images(self.get_server_root())

        if name not in images:
            return None

        index = images.index(name)
        navigation = self._calculate_navigation(images, index)

        return {
            "name": name,
            "index": index,
            "total": len(images),
            "prev_name": navigation["prev"],
            "next_name": navigation["next"],
        }

    def _calculate_navigation(self, images: list, current_index: int) -> Dict[str, str]:
        total_images = len(images)
        prev_index = current_index - 1 if current_index > 0 else total_images - 1
        next_index = current_index + 1 if current_index < total_images - 1 else 0

        return {
            "prev": images[prev_index],
            "next": images[next_index],
        }
    @staticmethod
    def _is_safe_static_path(static_path: str) -> bool:
        allowed_files = {"index.css", "view.css", "index.js", "view.js"}
        return static_path in allowed_files


    def _create_view_context(self, view_data: Dict) -> Dict[str, str]:
        name = view_data["name"]
        prev_name = view_data["prev_name"]
        next_name = view_data["next_name"]

        return {
            "name": html.escape(name),
            "img_url": f"/raw?name={quote(name)}",
            "prev_url": f"/view?name={quote(prev_name)}",
            "next_url": f"/view?name={quote(next_name)}",
            "position": f"{view_data['index'] + 1} / {view_data['total']}",
        }

    def _is_accessible_file(self, file_path: Path) -> bool:
        is_safe = is_safe_child(self.get_server_root(), file_path)
        exists = file_path.exists()
        return is_safe and exists

    def _send_file_response(self, file_path: Path) -> None:
        content_type = self._get_content_type(file_path)
        file_data = self._read_file_data(file_path)

        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(file_data)))
        self.end_headers()
        self.wfile.write(file_data)

    @staticmethod
    def _get_content_type(file_path: Path) -> str:
        content_type, _ = mimetypes.guess_type(str(file_path))
        return content_type or "application/octet-stream"

    @staticmethod
    def _read_file_data(file_path: Path) -> bytes:
        with open(file_path, 'rb') as file:
            return file.read()

    def _extract_delete_target(self) -> Optional[str]:
        content_length = int(self.headers.get('Content-Length', '0'))
        body = self._read_request_body(content_length)
        params = parse_qs(body)
        return params.get('name', [None])[0]

    def _read_request_body(self, content_length: int) -> str:
        if content_length == 0:
            return ''
        raw_body = self.rfile.read(content_length)
        return raw_body.decode('utf-8')

    def _delete_and_get_next(self, name: str, file_path: Path) -> str:
        images_before = list_images(self.get_server_root())
        current_index = self._get_image_index(images_before, name)

        self._delete_file(file_path)

        images_after = list_images(self.get_server_root())
        return self._determine_next_target(images_after, current_index)

    @staticmethod
    def _get_image_index(images: list, name: str) -> int:
        try:
            return images.index(unquote(name))
        except ValueError:
            return 0

    @staticmethod
    def _delete_file(file_path: Path) -> None:
        try:
            file_path.unlink()
        except Exception as error:
            raise IOError(f"Failed to delete: {error}")

    def _determine_next_target(self, images: list, previous_index: int) -> str:
        if not images:
            return "/"

        next_index = self._calculate_next_index(images, previous_index)
        target_name = images[next_index]
        return f"/view?name={quote(target_name)}"

    @staticmethod
    def _calculate_next_index(images: list, previous_index: int) -> int:
        if previous_index < len(images):
            return previous_index
        return len(images) - 1

    def _send_html_response(self, data: bytes, status: int) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

