"""HTTP server setup and configuration."""

from http.server import HTTPServer
from pathlib import Path
from typing import Optional

from image_server.handlers import ImageRequestHandler


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


def create_http_server(ip: str, port: int, root: Path) -> HTTPServer:
    server_address = create_server_address(ip, port)
    httpd = HTTPServer(server_address, ImageRequestHandler)
    assign_root_to_server(httpd, root)
    return httpd


def assign_root_to_server(httpd: HTTPServer, root: Path) -> None:
    httpd.root = root


def start_server(httpd: HTTPServer) -> None:
    httpd.serve_forever()

