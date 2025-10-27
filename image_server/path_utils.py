"""Path safety and image file detection utilities."""

from pathlib import Path
from typing import List

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}


def list_images(root: Path) -> List[str]:
    image_files = [p.name for p in root.iterdir() if is_image_file(p)]
    return sorted(image_files, key=str.lower)


def is_image_file(path: Path) -> bool:
    is_file = path.is_file()
    has_image_extension = has_valid_image_extension(path)
    return is_file and has_image_extension


def has_valid_image_extension(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTENSIONS


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

