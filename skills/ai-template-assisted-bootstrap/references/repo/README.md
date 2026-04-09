# AI-Assisted Template

Portuguese version: [README.pt-BR.md](README.pt-BR.md)

Generic AI-assisted project template with direct `make` workflows and no implementation code yet.

## Overview

This repository is a generic template for AI-assisted software projects.

## Prepared For

This template is set up for the tools we already reference in the repo, including:

- AI agents and assistants such as Codex, Claude, Gemini CLI, Cursor, and GitHub Copilot
- `make`-driven workflows
- repository-local docs and agent instructions
- VS Code task support

## Template State

- No implementation code ships with the template yet
- `make` targets are defined directly in the `Makefile`
- The repo keeps the workflow and documentation structure ready for future projects

## Requirements

- `make`
- `tree` and `pbcopy` for `make tree` on macOS

## Usage

```bash
make help
make run
```

The `run` and `debug` targets always stop the previous instance before starting a new one.

## Useful Commands

```bash
make help
make build
make stop
make run
make debug
make clean
make test
make github-release
make tree
```

## Repository Docs

- [AGENTS.md](AGENTS.md)
- [CLAUDE.md](CLAUDE.md)
- [GEMINI.md](GEMINI.md)
- [README.pt-BR.md](README.pt-BR.md)

## Structure

- `Makefile`: direct build, stop, run, debug, test, clean, GitHub release, and tree workflow
- `.codex/environments/environment.toml`: Codex actions for build, stop, run, debug, and test
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: short pointers to the repo guides
- `.cursor/rules/template.mdc`: Cursor rules for the repository
- `.github/copilot-instructions.md`: GitHub Copilot instructions
- `.vscode/tasks.json`: VS Code task list for the template
- `skills/`: reserved for repository-local skills

## Current Status

- The template is intentionally empty at the code level
- The documentation and tool scaffolding are ready for future projects
- Development flow is guided by `make stop` + `make run`
