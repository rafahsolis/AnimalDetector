"""HTML template loading and rendering."""

from pathlib import Path
from typing import Dict


class TemplateLoader:
    def __init__(self, templates_dir: Path) -> None:
        self._templates_dir = templates_dir

    def load_template(self, template_name: str) -> str:
        template_path = self._get_template_path(template_name)
        return self._read_template_file(template_path)

    def render_template(self, template_name: str, context: Dict[str, str]) -> str:
        template_content = self.load_template(template_name)
        return self._replace_placeholders(template_content, context)

    def _get_template_path(self, template_name: str) -> Path:
        return self._templates_dir / template_name

    @staticmethod
    def _read_template_file(template_path: Path) -> str:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def _replace_placeholders(template: str, context: Dict[str, str]) -> str:
        result = template
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, value)
        return result

