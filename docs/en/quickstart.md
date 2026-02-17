# SecureContextFactory Quickstart (en)

## 1) Install
From the repo:
```bash
pip install -e .
```

## 2) Bootstrap (env + MCP)
```bash
securecontextfactory init
securecontextfactory install --kickconfig
```

Optional (workspace hooks):
```bash
securecontextfactory hook install all
```

Diagnostics:
```bash
securecontextfactory doctor
```

## 3) PRD
Put your PRDs in `docs.prd/`:
- `docs.prd/prd.md`
- `docs.prd/tech.md`
- `docs.prd/ui-ux.md`

## 4) Autopilot (RPI)
1) Distribute PRDs and generate a DRAFT plan:
```bash
securecontextfactory autopilot-start --feature "current"
```
By default, this command syncs `docs.prd/*.md` into `docs/*.md` before running the runtime.

2) Run the daemon to process the queue (in another terminal):
```bash
python factory-workflow/bots/runtime/cli.py daemon --workspace "."
```

3) Approve the plan:
- Edit `factory-workflow/docs/autopilot/current/plan.md`
- Set `Status: APPROVED` and fill approver/date.

4) Queue implementation + QA:
```bash
securecontextfactory autopilot-build --feature "current" --project "/apps/<project>" --with-e2e
```

## 5) Audit
```bash
securecontextfactory audit --feature "current"
```

Evidence paths:
- Runtime out: `factory-workflow/bots/runtime/out/`
- QA reports: `factory-workflow/tests/reports/**`
