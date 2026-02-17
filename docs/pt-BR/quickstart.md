# SecureContextFactory Quickstart (pt-BR)

## 1) Instalar
No repo:
```bash
pip install -e .
```

## 2) Bootstrap (env + MCP)
```bash
securecontextfactory init
securecontextfactory install --kickconfig
```

Opcional (hooks no workspace):
```bash
securecontextfactory hook install all
```

Diagnostico:
```bash
securecontextfactory doctor
```

## 3) PRD
Coloque seus arquivos em `docs.prd/`:
- `docs.prd/prd.md`
- `docs.prd/tech.md`
- `docs.prd/ui-ux.md`

## 4) Autopilot (RPI)
1) Distribuir PRDs e gerar Plan (DRAFT):
```bash
securecontextfactory autopilot-start --feature "current"
```
Por default, o comando sincroniza `docs.prd/*.md` para `docs/*.md` antes de rodar o runtime.

2) Rodar o daemon para executar a fila (em outro terminal):
```bash
python factory-workflow/bots/runtime/cli.py daemon --workspace "."
```

3) Aprovar o plan:
- Edite `factory-workflow/docs/autopilot/current/plan.md`
- Troque para `Status: APPROVED` e preencha aprovador/data.

4) Enfileirar implementacao + QA:
```bash
securecontextfactory autopilot-build --feature "current" --project "/apps/<projeto>" --with-e2e
```

## 5) Auditar
```bash
securecontextfactory audit --feature "current"
```

Evidencias:
- Runtime out: `factory-workflow/bots/runtime/out/`
- QA reports: `factory-workflow/tests/reports/**`
