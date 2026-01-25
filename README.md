# 🏭 Factory

> **Framework publico para Context Engineering, Spec-driven Delivery e governanca de entrega de software.**

Factory existe para resolver um problema simples e ignorado:

🚨 **IA nao falha por codigo.**  
**IA falha por CONTEXTO mal definido.**

---

## 🎯 O que e a Factory

Factory e o **sistema operacional do desenvolvimento de software**.

Ela nao gera codigo sozinha.  
Ela define **como pesquisar, decidir, planejar, validar e automatizar** a construcao de software — **antes**, **durante** e **depois** da implementacao.

---

## 🧭 Workflow canonico: RPI (Research → Plan → Implement)

### Fluxo (Mermaid)

```mermaid
flowchart TD
    A[💡 Ideia] --> B[🔎 Research]
    B --> C[🧭 Plan]
    C --> D[🧱 Implement]
    D --> E[🧪 Testes]
    E --> F[🚦 Gates]
    F --> G[🚀 Deploy]
```

### Fluxo (fallback)

```
IDEIA
  ↓
RESEARCH (evidencias + gaps)
  ↓
PLAN (escopo + passos + testes)
  ↓
IMPLEMENT (codigo + docs)
  ↓
TESTES
  ↓
GATES
  ↓
DEPLOY
```

---

## 🤖 Execucao e bots

- **Executor de IA** (IDE assistant / LLM executor) edita arquivos.
- **Bots Python** executam **apenas via CLI local** (ou CI configurado).
- Nada executa sem contexto fechado; gaps devem ser registrados.

👉 **Como executar bots:** veja `factory-workflow/docs/quickstart.md`.

---

## 🧠 Contexto e governanca

- **Contexto e fonte de verdade:** `factory-workflow/context/*`.
- **Reuso antes de criar:** politica MCP em `factory-workflow/context/tooling/mcp-policy.md`.
- **Seguranca e gates:** `factory-workflow/cicd/*`.
- **Governanca e auditoria:** `factory-workflow/governance/*`.

---

## 📁 Estrutura essencial

- `factory-workflow/docs/` → onboarding, workflow, templates
- `factory-workflow/context/` → core, quality, tooling, UI, codex
- `factory-workflow/bots/` → contratos de bots (Markdown)
- `factory-workflow/bots/runtime/` → runtime local (CLI)
- `factory-workflow/libs/mcp/` → servers e registries MCP
- `factory-workflow/cicd/` → gates, checklist, deploy

---

## 🚀 Por onde comecar

1) `factory-workflow/docs/quickstart.md`  
2) `factory-workflow/docs/workflow.md`  
3) `factory-workflow/docs/templates/README.md`  
4) `factory-workflow/docs/examples/README.md`

---

## 🧩 Tutorial rapido (setup + uso)

### Setup na maquina (uma vez)
1) Python 3.10+ e Git instalados
2) Criar venv e instalar deps do runtime:
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r factory-workflow/bots/runtime/requirements.txt
```
3) Criar `.env` local:
```bash
cp factory-workflow/bots/runtime/.env.example .env
```
4) Configurar MCPs locais:
```bash
cp factory-workflow/config/mcp.example.toml factory-workflow/config/mcp.toml
```

### Setup no projeto (kickoff)
1) Criar docs do projeto:
`factory-workflow/docs/projects/<projeto>/`
2) Preencher documentos base:
`docs.md`, `stack.md`, `design-system.md`, `mcp.md`
3) Criar referencia detalhada:
`docs/projects/<projeto>/reference/` (modulos, paginas, regras, fluxos, data-contracts)
4) Gerar diagramas (Mermaid):
`docs/projects/<projeto>/architecture/frontend-flow.md`
`docs/projects/<projeto>/architecture/backend-flow.md`
5) Rodar o checklist completo:
`factory-workflow/docs/templates/project-kickoff.checklist.md`

### Setup em projeto existente (takeover)
1) Preencher checklist completo:
`factory-workflow/docs/templates/project-takeover.checklist.md`
2) Registrar gaps em `factory-workflow/context/core/gaps.md`
3) Criar/atualizar referencia em `docs/projects/<projeto>/reference/`

### Quando tudo estiver pronto
Peça ao Factory: **Research + Plan + Queue** (nenhuma implementacao sem plan aprovado).
Use o guia: `factory-workflow/docs/modelo factory.md`.

---

## 🔐 Regras inegociaveis

- Contexto fechado antes de executar.
- Plan aprovado antes de implementar.
- Evidencias e links em Research/Plan.
- Producao exige aprovacao humana.

---

## 🔗 Referencias rapidas

- Workflow RPI: `factory-workflow/docs/workflow.md`
- Politica MCP: `factory-workflow/context/tooling/mcp-policy.md`
- Runtime local (CLI): `factory-workflow/context/tooling/runtime.md`
- Quickstart: `factory-workflow/docs/quickstart.md`
- Modelo de uso (prompt mestre): `factory-workflow/docs/modelo factory.md`
- Templates completos: `factory-workflow/docs/templates/README.md`
- Exemplos: `factory-workflow/docs/examples/README.md`

---

## Ultimas atualizacoes (main)

- 2026-01-25 — docs: add tutorial de uso, templates de referencia, checklists e diagramas
- 2026-01-25 — Add GitHub Actions workflow for Python package publishing (commit `9414abf`)
- 2026-01-19 — feat(factory): enable qa-e2e-browser-audit runtime bot (commit `d6c0c0a`)
- 2026-01-19 — feat(factory): add chrome devtools mcp + browser audit qa bot (commit `97c1bd2`)
