# Scope

## Dentro do escopo
- CLI wizard Python-first para iniciar/instalar/rodar pipelines e squads.
- Metodologia RPI obrigatoria (Research -> Plan -> Implement) com aprovacao humana do plan.
- Governanca hardcore: policy-engine, gates, audit trail, gaps forcados com sugestao.
- Persistencia de contexto por projeto (em `factory-workflow/context/**`).
- Integracoes opcionais para acelerar:
  - LangGraph (orquestracao stateful com branching/retries/checkpoints).
  - CrewAI (squads/crews com roles/goals/delegacao).
  - UX/arquitetura inspiradas no aios-core (wizard, squads, pipeline ADE-like) reimplementadas em Python.
- Runtime/bots locais para context-sync/planner/dev/qa/review.
- MCPs e registries para reuso antes de criar (docs/knowledge, UI registry, audits).

## Fora do escopo
- Plataforma hospedada (SaaS).
- "Agente root" com permissao irrestrita por padrao.
- Deploy para producao automatizado sem aprovacao humana registrada.
- Vendoring amplo de codigo de terceiros sem compliance de licencas/avisos.

## Suposicoes explicitas
- Projeto roda em ambiente com Python 3.11+ e Git.
- O usuario fornece PRDs em `docs.prd/` (ou aceita que o sistema converta input em arquivos).
- Tokens/segredos sao fornecidos via `.env`/vault (nunca commitados).
- O usuario aceita gates como parte do processo (sem "bypass").

## Restricoes conhecidas
- Node.js nao e requisito obrigatorio (Python-first).
- Operacoes de risco exigem confirmacao humana (policy-engine).
- Escrita de codigo deve seguir escopo aprovado no plan e respeitar paths permitidos do runtime.

## Dependencias externas
- Opcionais (via extras): LangGraph, CrewAI.
- MCP providers (dependendo do uso): Context7, GitHub, HuggingFace, Playwright, Chrome DevTools.
