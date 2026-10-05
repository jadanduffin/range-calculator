# CLAUDE.md

Standing instructions for the AI agent working in this repo.
Keep this file SHORT. Every line here costs context on every request.

## About this project
<!-- Fill these in when you start. Who you are lives in ~/.claude/CLAUDE.md. -->
- What I'm building (one sentence):
- Spec: docs/SPEC.md. Plan: docs/PLAN.md. Architecture: docs/ARCHITECTURE.md.
- Test command: `uv run pytest`  <!-- change if this isn't a Python project -->
- Run command: `uv run python -m app`  <!-- change to however this project runs -->

## How to work with me
- Before writing code, restate what you think I'm asking and wait for a yes.
- Critique my ideas. If a plan, requirement, or instruction is weak, say so
  directly and explain why, then suggest a better option.
- Teach as you go. When you make an architectural choice, explain it in
  two or three plain sentences a beginner can follow.
- Prefer the simplest thing that works. No new dependencies without asking.

## Project rules
- Do not build anything that isn't in docs/PLAN.md without asking.
- New idea that isn't in PLAN.md (mine or yours)? Add a row to BACKLOG.md,
  tell me in one line, and carry on with the current task.
- Every acceptance criterion in the spec gets a test in tests/.
- Run the test command after every change. Never report a task as done
  while tests are failing.
- Keep modules small with clear interfaces (see docs/ARCHITECTURE.md).
- Commit after each working step with a clear message.

## Journaling
- After each task, append an entry to AGENT_LOG.md: what you did, what you
  decided and why, and anything you were unsure about.
