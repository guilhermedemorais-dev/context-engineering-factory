# Runtime

## Objective
Provide a minimal, executable runtime for Factory bots using LangChain.

## What this does
- Loads bot contracts from `factory-workflow/bots/<bot>.md`
- Loads context from `factory-workflow/context/INDEX.md` and referenced files
- Runs a task with an LLM
- Writes outputs to files (never stdout-only)
- Records gaps in `factory-workflow/context/core/gaps.md` when context is missing

## Requirements
- Python 3.10+
- API access for the configured LLM provider

## Setup
1) Create a virtual environment and install deps:
```
python -m venv .venv
. .venv/bin/activate
pip install -r factory-workflow/bots/runtime/requirements.txt
```

2) Configure env vars:
```
cp factory-workflow/bots/runtime/.env.example .env
# edit .env
```

3) Review runtime config:
- `factory-workflow/bots/runtime/config.yaml`

## Run
```
python factory-workflow/bots/runtime/cli.py run orchestrator --task "Summarize current plan" --workspace "/path/to/workspace"
```

For dev bot (requires a project path under /apps):
```
python factory-workflow/bots/runtime/cli.py run dev --task "Implement feature X" --workspace "/path/to/workspace" --project "/apps/my-project"
```

For browser audit bot (requires chrome_devtools in mcp.toml):
```
python factory-workflow/bots/runtime/cli.py run qa-e2e-browser-audit --task "Browser audit baseUrl=https://app.exemplo.com" --workspace "/path/to/workspace"
```

## Outputs
- Execution outputs: `factory-workflow/bots/runtime/out/<timestamp>/<bot>/`
- Deliverables:
  - Documentation/plan bots: only inside `/factory-workflow`
  - Dev bot: only inside `/apps/<project>` (required)

## Notes
- If context is missing, the bot will append gaps to `factory-workflow/context/core/gaps.md` and stop.
- Paths are validated; path traversal is blocked.
- Browser audit requer `factory-workflow/config/mcp.toml` com `[chrome_devtools]` habilitado (ou `FACTORY_MCP_CONFIG`).
- LLM token limit can be set via `FACTORY_LLM_MAX_COMPLETION_TOKENS` or `llm.max_completion_tokens` in `factory-workflow/bots/runtime/config.yaml`.
