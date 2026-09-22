import json

import pytest

from buildr_cli.generator import BuildrGenerationError, create_project, slugify


def test_slugify_creates_safe_python_style_name():
    assert slugify("Make a Calculator App!") == "make_a_calculator_app"
    assert slugify("2026 dashboard") == "project_2026_dashboard"


def test_slugify_rejects_punctuation_only():
    with pytest.raises(BuildrGenerationError):
        slugify("!!!")


def test_calculator_template_contains_code_tests_and_manifest(tmp_path):
    project = create_project("calculator app", output_dir=tmp_path)
    assert project.template == "calculator"
    assert (project.path / "main.py").exists()
    assert (project.path / "test_main.py").exists()
    manifest = json.loads((project.path / "buildr.json").read_text())
    assert manifest["generated_by"] == "buildr-cli 0.2.0"


def test_generic_description_gets_minimal_starter(tmp_path):
    project = create_project("campus task organizer", output_dir=tmp_path)
    assert project.template == "python-starter"
    assert "campus task organizer" in (project.path / "README.md").read_text()

