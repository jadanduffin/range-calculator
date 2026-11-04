# Project template: spec-first agentic development

A starting point for any project built with an AI agent. Every project runs
the same loop, and every file here supports one stage of it:

    SPEC  ->  PLAN  ->  TESTS  ->  BUILD  ->  REVIEW  ->  RELEASE

## Starting a project

| Situation | Do this |
|---|---|
| Brand-new project | `gh repo create my-project --template jadanduffin/project-template --private --clone` |
| Existing project | Open it in Claude Code and run `/adopt-workflow` |

Then fill in the top of `CLAUDE.md` and write `docs/SPEC.md` before any code.
First time on a new machine? See SETUP.md.

## What's in here

| File | What it's for | Fill it in |
|---|---|---|
| `CLAUDE.md` | Standing instructions for your AI agent | First |
| `docs/SPEC.md` | What you're building and why | Before any code |
| `docs/ARCHITECTURE.md` | Modules, interfaces, invariants | After the spec |
| `docs/PLAN.md` | The approved build plan | After the architecture |
| `tests/` | One test per acceptance criterion | Before building each step |
| `BACKLOG.md` | Parking lot for ideas meant for later releases | Whenever an idea pops up |
| `DEVLOG.md` | YOUR journal: decisions and lessons | End of every session |
| `AGENT_LOG.md` | The AGENT's journal: what it did and why | After every task |
| `docs/FUNDAMENTALS.md` | Principles, vocabulary, stack choices | Any time |
| `SETUP.md` | Install the tools on a new machine | Once per machine |
| `.github/workflows/tests.yml` | Runs your tests on GitHub on every push (CI) | Already on |

## Not a Python project?

The workflow files above work for anything. The Python starter is optional.
Delete these, then set the test and run commands in `CLAUDE.md` and `tests.yml`:

`pyproject.toml`, `.python-version`, `src/`, `tests/test_setup.py`

## Everyday commands (Python starter)

| Command | What it does |
|---|---|
| `uv run pytest` | Run all tests |
| `uv run python -m app` | Run your project (once it exists) |
| `uv add <package>` | Add a library (ask yourself first: do I need it?) |
| `uv run smoke_test.py` | Check this machine is set up |
