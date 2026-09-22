# Roadmap

## v0.2 — reconstructed prototype

- Repair Python packaging with a `src` layout
- Preserve `hello`, `ask`, and `create`
- Add offline behavior and optional OpenAI Responses API support
- Prevent overwrites and path escape
- Add project manifests, listing, tests, examples, and CI

## Evidence required before v0.3

Use Buildr to create at least ten small personal or class projects. Record:

- which requested templates repeat;
- which files are changed immediately after generation;
- whether offline mode is useful;
- whether AI answers need access to local project files;
- where users misunderstand what Buildr has executed.

## Possible v0.3

- Configurable template registry
- `buildr inspect` for a read-only project summary
- Preview planned file changes before creation
- Structured AI output with schema validation
- Per-project conversation history with explicit storage controls

## Explicitly deferred

- Shell-command execution
- Autonomous file editing
- Git commits and pushes
- Background agents
- OpenMind features

Those capabilities require a separate permission, sandboxing, and audit design. They should not be smuggled into a simple scaffolding tool.

