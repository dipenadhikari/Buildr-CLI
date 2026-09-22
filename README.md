# Buildr CLI

**Status: reconstructed prototype · v0.2.0**

Buildr is a small Python terminal assistant for students and early builders. It can answer a coding question through an optional OpenAI connection and generate safe starter projects without executing or overwriting them.

This repository reconstructs the Buildr prototype originally created in April 2026. The original commands worked, but generated folders caused setuptools to fail with “Multiple top-level packages discovered in a flat-layout.” Version 0.2 fixes that design problem with an explicit `src/` package layout.

Buildr is intentionally separate from **OpenMind**, the later AI-agent project.

## What works

```bash
buildr hello
buildr ask "What is Python?"
buildr ask "Explain this SQL join" --offline
buildr create "calculator app"
buildr create "stock dashboard"
buildr create "campus task organizer" --name campus_tasks
buildr list
```

### `hello`

Confirms that the installed command works.

### `ask`

- Uses the OpenAI Responses API when `OPENAI_API_KEY` is configured.
- Uses `gpt-4.1-mini` by default to preserve the original Buildr decision.
- Uses a transparent offline response when no key is available.
- Never claims that code was executed.

### `create`

- Recognizes calculator and stock-dashboard requests.
- Uses a generic Python starter for other descriptions.
- Writes projects under `projects/` by default.
- Creates a `buildr.json` manifest.
- Never overwrites an existing directory.
- Never executes generated code.

### `list`

Lists valid generated projects by reading their manifests.

## Install for development

Requirements: Python 3.12–3.14 and [`uv`](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/dipenadhikari/buildr-cli.git
cd buildr-cli
uv sync --all-groups
uv run buildr hello
```

You can also verify the editable command after activating the environment:

```bash
source .venv/bin/activate
buildr --version
buildr hello
```

## Optional OpenAI setup

Buildr does not need an API key for project generation or offline questions.

```bash
cp .env.example .env
```

Then add your key locally:

```text
OPENAI_API_KEY=your-key-here
BUILDR_MODEL=gpt-4.1-mini
```

Never commit `.env` or paste an API key into source code, screenshots, issues, or terminal logs.

The OpenAI integration uses the Python SDK’s Responses API pattern:

```python
from openai import OpenAI

client = OpenAI()
response = client.responses.create(
    model="gpt-4.1-mini",
    input="Explain a Python list comprehension.",
)
print(response.output_text)
```

API usage may cost money. Availability and limits depend on the connected OpenAI account.

## Generate projects safely

```bash
uv run buildr create "calculator app"
uv run buildr create "stock dashboard"
uv run buildr list
```

To write somewhere else:

```bash
uv run buildr create "study tracker" --output ~/Developer/generated-projects
```

Review generated files before running them.

## Test and build

```bash
uv run pytest
uv build
```

The test suite covers:

- the original `hello` and offline `ask` behavior;
- OpenAI integration through a mocked client;
- safe naming and path handling;
- calculator and generic templates;
- no-overwrite behavior;
- project discovery.

GitHub Actions repeats the tests, builds the wheel and source distribution, and runs the installed CLI from the wheel.

## Why the packaging bug is fixed

Only `src/buildr_cli/` is eligible for package discovery:

```toml
[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
include = ["buildr_cli*"]
```

Generated projects live outside `src`, so `calculator_app`, `stock_dashboard`, or `projects` cannot be mistaken for Buildr packages.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the complete explanation and [`docs/ROADMAP.md`](docs/ROADMAP.md) for evidence required before expanding the tool.

## Honest limitations

Buildr v0.2 is not a Cursor replacement, autonomous agent, or production code generator. It does not inspect arbitrary repositories, edit existing code, execute shell commands, or push to GitHub. Those capabilities need explicit permissions, sandboxing, validation, and audit history.

## Portfolio explanation

> I rebuilt an early CLI prototype after generated folders broke Python package discovery. I changed it to a `src` layout, separated generation from execution, added atomic writes and overwrite protection, mocked external AI calls in tests, and verified the built wheel in CI.

