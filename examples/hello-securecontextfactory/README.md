# hello-securecontextfactory

Minimal example showing the governed flow (RPI + gaps + plan approval).

## Steps
1) From repo root:
```bash
pip install -e .
securecontextfactory init
securecontextfactory install --kickconfig
```

2) Fill `docs.prd/` (use templates):
- `docs.prd/prd.md`
- `docs.prd/tech.md`
- `docs.prd/ui-ux.md`

3) Start autopilot:
```bash
securecontextfactory autopilot-start --feature "hello"
python factory-workflow/bots/runtime/cli.py daemon --workspace "."
```

4) Approve plan:
Edit `factory-workflow/docs/autopilot/hello/plan.md` and set `Status: APPROVED`.

5) Queue implementation + QA:
```bash
securecontextfactory autopilot-build --feature "hello" --project "/apps/<project>"
```

