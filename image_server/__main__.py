#!/usr/bin/env python3
"""
Image Server module entry point.

Usage:
  python -m image_server --dir /path/to/images --port 8000
"""

from pathlib import Path
import argparse

from image_server.server import (
    create_http_server,
    start_server,
    get_server_ip,
    get_server_port,
)


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

