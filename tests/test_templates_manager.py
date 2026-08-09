import pytest

from neocomposer.exceptions import TemplateError
from neocomposer.templates_manager import TemplatesManager


@pytest.fixture
def templates_dir(tmp_path):
    return tmp_path


def write_template(directory, filename, content):
    path = directory / filename
    path.write_text(content)
    return path


def test_list_templates_missing_dir(tmp_path):
    manager = TemplatesManager(str(tmp_path / "missing"))
    assert manager.list_templates() == []


def test_list_templates_returns_supported_extensions(templates_dir):
    write_template(templates_dir, "welcome.txt", "Hello {{ name }}")
    write_template(templates_dir, "notes.md", "# Notes")
    write_template(templates_dir, "ignored.py", "print('hi')")

    manager = TemplatesManager(str(templates_dir))
    templates = manager.list_templates()

    names = sorted(t.name for t in templates)
    assert names == ["notes", "welcome"]


def test_load_template_without_frontmatter(templates_dir):
    write_template(templates_dir, "plain.txt", "Hello {{ name }}")

    manager = TemplatesManager(str(templates_dir))
    template = manager.load("plain.txt")

    assert template.subject is None
    assert template.body == "Hello {{ name }}"
    assert template.variables == ["name"]


def test_load_template_with_frontmatter(templates_dir):
    write_template(
        templates_dir,
        "greeting.txt",
        '---\nsubject: "Hi {{ name }}"\n---\nHello {{ name }}, welcome {{ place }}',
    )

    manager = TemplatesManager(str(templates_dir))
    template = manager.load("greeting.txt")

    assert template.subject == "Hi {{ name }}"
    assert template.body == "Hello {{ name }}, welcome {{ place }}"
    assert template.variables == ["name", "place"]


def test_load_template_unclosed_frontmatter_raises(templates_dir):
    write_template(templates_dir, "broken.txt", "---\nsubject: Hi\nHello")

    manager = TemplatesManager(str(templates_dir))
    with pytest.raises(TemplateError, match="frontmatter is not closed"):
        manager.load("broken.txt")


def test_load_template_invalid_frontmatter_line_raises(templates_dir):
    write_template(templates_dir, "broken.txt", "---\nno-colon-here\n---\nBody")

    manager = TemplatesManager(str(templates_dir))
    with pytest.raises(TemplateError, match="Invalid frontmatter line"):
        manager.load("broken.txt")


def test_load_template_by_stem_without_extension(templates_dir):
    write_template(templates_dir, "welcome.txt", "Hello")

    manager = TemplatesManager(str(templates_dir))
    template = manager.load("welcome")

    assert template.name == "welcome"


def test_load_template_ambiguous_stem_raises(templates_dir):
    write_template(templates_dir, "welcome.txt", "Hello")
    write_template(templates_dir, "welcome.md", "# Hello")

    manager = TemplatesManager(str(templates_dir))
    with pytest.raises(TemplateError, match="Ambiguous template"):
        manager.load("welcome")


def test_load_template_not_found_raises(templates_dir):
    manager = TemplatesManager(str(templates_dir))
    with pytest.raises(TemplateError, match="not found"):
        manager.load("missing")


def test_load_template_empty_identifier_raises(templates_dir):
    manager = TemplatesManager(str(templates_dir))
    with pytest.raises(TemplateError, match="cannot be empty"):
        manager.load("")


def test_load_template_by_absolute_path(templates_dir):
    path = write_template(templates_dir, "welcome.txt", "Hello")

    manager = TemplatesManager(str(templates_dir / "other"))
    template = manager.load(str(path))

    assert template.name == "welcome"


def test_render_substitutes_variables(templates_dir):
    write_template(
        templates_dir,
        "greeting.txt",
        '---\nsubject: "Hi {{ name }}"\n---\nHello {{ name }}',
    )

    manager = TemplatesManager(str(templates_dir))
    subject, body = manager.render("greeting.txt", {"name": "Ada"})

    assert subject == "Hi Ada"
    assert body == "Hello Ada"


def test_render_missing_variables_raises(templates_dir):
    write_template(templates_dir, "greeting.txt", "Hello {{ name }}")

    manager = TemplatesManager(str(templates_dir))
    with pytest.raises(TemplateError, match="Missing template variables"):
        manager.render("greeting.txt", {})


def test_render_template_without_subject_returns_none(templates_dir):
    write_template(templates_dir, "plain.txt", "Hello {{ name }}")

    manager = TemplatesManager(str(templates_dir))
    subject, body = manager.render("plain.txt", {"name": "Ada"})

    assert subject is None
    assert body == "Hello Ada"
