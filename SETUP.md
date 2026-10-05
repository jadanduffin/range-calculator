# Machine setup

Do this once per computer. Open a new terminal window after each install.
If Claude Desktop is already open, quit and reopen it once the installs finish,
or it won't see the new tools.

## Accounts

| Account | Where | Note |
|---|---|---|
| GitHub (free) | https://github.com/signup | Verify your email |
| Claude (paid plan: Pro or Max) | https://claude.ai | Claude Code won't sign in without a paid plan |

Git is the tool on your computer that saves versions of your work.
GitHub is the website where your copy of the project lives online.

## Mac

| Tool | Command |
|---|---|
| Git | `git --version` (if it offers to install developer tools, click Install) |
| uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| GitHub CLI | Download the Mac installer from https://cli.github.com and run it |
| Claude Desktop | Download from https://claude.ai/download, install, and sign in |

## Windows

Install Git FIRST. Then open PowerShell:

| Tool | Command |
|---|---|
| Git | Download and run the installer from https://git-scm.com (accept all defaults) |
| uv | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| GitHub CLI | `winget install --id GitHub.cli` (no winget? Download the installer from https://cli.github.com) |
| Claude Desktop | Download from https://claude.ai/download, install, and sign in |

## Optional: Claude Code in the terminal (CLI)

| System | Command |
|---|---|
| Mac | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Windows (PowerShell) | `irm https://claude.ai/install.ps1 \| iex` |

Then type `claude` inside your project folder to start it.

## Sign in and configure (once)

    gh auth login
    gh auth setup-git
    git config --global user.name "Your Name"
    git config --global user.email "you@example.com"

`gh auth login` asks you questions and opens your browser, so run it yourself.
`gh auth setup-git` lets Git use that sign-in when it pushes to GitHub.

## Start a project from this template

    gh repo create my-project --template jadanduffin/project-template --private --clone
    cd my-project
    uv run smoke_test.py

When the smoke test says "All checks passed", open `my-project` in Claude Code.

## Laptop won't cooperate? Plan B

Open your repo on github.com, click the green Code button, then the
Codespaces tab, then "Create codespace". You get the whole setup in your
browser. Type `claude` in the codespace terminal to start Claude Code.
