from typer.testing import CliRunner

from buildr_cli.main import app


runner = CliRunner()


def test_hello_preserves_original_behavior():
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Buildr is working!" in result.stdout


def test_ask_has_a_no_cost_offline_mode(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = runner.invoke(app, ["ask", "What is Python?"])
    assert result.exit_code == 0
    assert "You asked: What is Python?" in result.stdout
    assert "no API request" in result.stdout


def test_create_and_list_project(tmp_path):
    output = tmp_path / "projects"
    created = runner.invoke(app, ["create", "calculator app", "--output", str(output)])
    assert created.exit_code == 0
    assert "Created project: calculator_app" in created.stdout

    listed = runner.invoke(app, ["list", "--output", str(output)])
    assert listed.exit_code == 0
    assert "calculator_app" in listed.stdout
    assert "calculator" in listed.stdout


def test_create_never_overwrites_existing_project(tmp_path):
    output = tmp_path / "projects"
    assert runner.invoke(app, ["create", "calculator app", "--output", str(output)]).exit_code == 0
    second = runner.invoke(app, ["create", "calculator app", "--output", str(output)])
    assert second.exit_code == 1
    assert "already exists" in second.stdout

