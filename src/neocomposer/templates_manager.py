import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from . import paths
from .exceptions import TemplateError


SUPPORTED_TEMPLATE_EXTENSIONS = (".html", ".txt", ".md")
VARIABLE_PATTERN = re.compile(r"{{\s*([A-Za-z_][A-Za-z0-9_]*)\s*}}")


@dataclass(frozen=True)
class EmailTemplate:
    """Parsed reusable email template."""

    name: str
    path: str
    subject: Optional[str]
    body: str

    @property
    def variables(self) -> List[str]:
        """Variable names required by the subject and body."""
        content = f"{self.subject or ''}\n{self.body}"
        return sorted(set(VARIABLE_PATTERN.findall(content)))


class TemplatesManager:
    """Loads, lists, and renders reusable email templates."""

    def __init__(self, templates_dir: Optional[str] = None):
        self.templates_dir = templates_dir or paths.get_templates_dir()

    def list_templates(self) -> List[EmailTemplate]:
        """Returns all templates found in the templates directory."""
        if not os.path.isdir(self.templates_dir):
            return []

        templates = []
        for filename in sorted(os.listdir(self.templates_dir)):
            template_path = os.path.join(self.templates_dir, filename)
            if not os.path.isfile(template_path):
                continue
            if not filename.endswith(SUPPORTED_TEMPLATE_EXTENSIONS):
                continue
            templates.append(self.load(filename))

        return templates

    def load(self, identifier: str) -> EmailTemplate:
        """Loads a template by name, stem, relative name, or direct file path."""
        template_path = self._resolve_template_path(identifier)

        try:
            with open(template_path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as e:
            raise TemplateError(f"Could not read template {template_path}: {e}") from e

        metadata, body = self._parse_frontmatter(content, template_path)
        subject = metadata.get("subject")

        return EmailTemplate(
            name=os.path.splitext(os.path.basename(template_path))[0],
            path=template_path,
            subject=subject,
            body=body,
        )

    def render(self, identifier: str, variables: Dict[str, str]) -> Tuple[Optional[str], str]:
        """Renders a template and returns (subject, body)."""
        template = self.load(identifier)
        missing = [name for name in template.variables if name not in variables]
        if missing:
            raise TemplateError(
                "Missing template variables: " + ", ".join(sorted(missing))
            )

        return (
            self._render_text(template.subject, variables) if template.subject else None,
            self._render_text(template.body, variables),
        )

    def _resolve_template_path(self, identifier: str) -> str:
        if not identifier:
            raise TemplateError("Template name cannot be empty")

        if os.path.isfile(identifier):
            return os.path.abspath(identifier)

        candidate = os.path.join(self.templates_dir, identifier)
        if os.path.isfile(candidate):
            return candidate

        matches = []
        stem, ext = os.path.splitext(identifier)
        if ext:
            candidate = os.path.join(self.templates_dir, identifier)
            if os.path.isfile(candidate):
                matches.append(candidate)
        else:
            for supported_ext in SUPPORTED_TEMPLATE_EXTENSIONS:
                candidate = os.path.join(self.templates_dir, identifier + supported_ext)
                if os.path.isfile(candidate):
                    matches.append(candidate)

            if os.path.isdir(self.templates_dir):
                for filename in os.listdir(self.templates_dir):
                    file_stem, file_ext = os.path.splitext(filename)
                    if file_ext in SUPPORTED_TEMPLATE_EXTENSIONS and file_stem == identifier:
                        candidate = os.path.join(self.templates_dir, filename)
                        if candidate not in matches:
                            matches.append(candidate)

        if len(matches) == 1:
            return matches[0]

        if len(matches) > 1:
            names = ", ".join(os.path.basename(path) for path in sorted(matches))
            raise TemplateError(f"Ambiguous template '{identifier}': {names}")

        raise TemplateError(
            f"Template '{identifier}' not found in {self.templates_dir}"
        )

    def _parse_frontmatter(self, content: str, template_path: str) -> Tuple[Dict[str, str], str]:
        lines = content.splitlines(keepends=True)
        if not lines or lines[0].strip() != "---":
            return {}, content

        closing_index = None
        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                closing_index = index
                break

        if closing_index is None:
            raise TemplateError(f"Template frontmatter is not closed: {template_path}")

        metadata = self._parse_metadata("".join(lines[1:closing_index]), template_path)
        body = "".join(lines[closing_index + 1 :])
        return metadata, body

    def _parse_metadata(self, raw_metadata: str, template_path: str) -> Dict[str, str]:
        metadata = {}
        for line_number, line in enumerate(raw_metadata.splitlines(), start=2):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if ":" not in stripped:
                raise TemplateError(
                    f"Invalid frontmatter line {line_number} in {template_path}: {line}"
                )
            key, value = stripped.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"').strip("'")
        return metadata

    def _render_text(self, text: Optional[str], variables: Dict[str, str]) -> str:
        if text is None:
            return ""

        return VARIABLE_PATTERN.sub(
            lambda match: str(variables[match.group(1)]),
            text,
        )
