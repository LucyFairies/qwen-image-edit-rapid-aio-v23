# AGENTS.md — qwen-image-edit-rapid-aio-v23

Follow the rules in the parent files:

- `workdir/AGENTS.md`
- `C:\Users\h4sch\AGENTS.md`
- `C:\Users\h4sch\CLAUDE.md`

## GitHub

- Inside Grok sessions: prefer the MCP integration (`grok_com_github`) for repository operations, file changes, issues, etc.
- For local development workflow: use the provided `setup-gh.ps1` + native `git` and `gh` CLI.

## Conventions in this project

- PowerShell (pwsh) examples with full paths where the Python env is referenced.
- Keep the Gradio / CLI usage instructions up-to-date.
- New setup helpers belong in the project folder as `.ps1` (see `setup-gh.ps1` and the pattern from `json-translator/install-shortcut.ps1`).

When making changes, run the verification steps described in the main README (especially the gh script + existing Python flows).
