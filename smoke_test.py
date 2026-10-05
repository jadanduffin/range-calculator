"""Machine setup check. Run: uv run smoke_test.py

uv creates the project's virtual environment (and downloads Python if
needed) before this script runs, so you never install Python yourself.
"""
import os
import shutil
import subprocess
import sys

results = []


def check(name, ok, fix, required=True):
    results.append((ok, required))
    mark = "PASS" if ok else ("FAIL" if required else "SKIP")
    print(f"[{mark}] {name}")
    if not ok:
        print(f"       Fix: {fix}")


def run(cmd, env=None):
    try:
        out = subprocess.run(
            cmd, capture_output=True, text=True, timeout=20, env=env
        )
        return out.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


print("\nSetup check\n")

in_venv = sys.prefix != sys.base_prefix
check(
    "Running inside the project's virtual environment",
    in_venv,
    "Run this with:  uv run smoke_test.py  (not plain python).",
)

check(
    f"Python 3.11 or newer (you have {sys.version.split()[0]})",
    sys.version_info >= (3, 11),
    "Run:  uv python install 3.12  then rerun.",
)

check(
    "Git is installed",
    shutil.which("git") is not None,
    "Install Git from git-scm.com, then open a NEW terminal window.",
)

check(
    "Git knows who you are",
    run(["git", "config", "--global", "user.name"])
    and run(["git", "config", "--global", "user.email"]),
    'Run:  git config --global user.name "Your Name"  and  '
    'git config --global user.email "you@example.com"',
)

check(
    "You are inside a Git repo",
    run(["git", "rev-parse", "--is-inside-work-tree"]),
    "cd into your project folder, then rerun.",
)

check(
    "Claude Code CLI (optional)",
    shutil.which("claude") is not None,
    "Optional. See SETUP.md if you want the terminal version.",
    required=False,
)

check(
    "GitHub CLI is installed and signed in",
    run(["gh", "auth", "status"]),
    "Install GitHub CLI (see SETUP.md), then run:  gh auth login",
)

# Never stop to ask for a password: a missing sign-in should fail, not hang.
no_prompt = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"}
check(
    "Git can reach your repo on GitHub",
    run(["git", "ls-remote", "origin"], env=no_prompt),
    "Check your internet, then run:  gh auth setup-git  and rerun.",
)

check(
    "pytest is available",
    run([sys.executable, "-m", "pytest", "--version"]),
    "Run:  uv sync  then rerun.",
)

check(
    "VS Code command (optional)",
    shutil.which("code") is not None,
    "Optional. Install VS Code from code.visualstudio.com.",
    required=False,
)

failed = [r for r in results if r[1] and not r[0]]
print()
if failed:
    print(f"{len(failed)} required check(s) failed. Fix them above and rerun.")
    sys.exit(1)
print("All checks passed. You are ready.")
