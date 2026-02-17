# Research — SecureContextFactory (fusion-v1)

## Objetivo
Definir uma estrategia de fusao que evolui o core do repo atual (Factory) para o projeto final **SecureContextFactory**, integrando:
- UX/arquitetura inspiradas no SynkraAI/aios-core (wizard, squads, "ADE-like pipeline") **reimplementadas em Python**
- Orquestracao stateful via LangGraph (branching/cycles/retries/checkpoints) como camada opcional
- Squads/crews via CrewAI (roles/goals/delegacao) como camada opcional

## Regras inegociaveis (core)
- Governanca hardcore: gates obrigatorios, policy-engine, audit trail, aprovacao humana para operacoes de risco.
- RPI obrigatorio: Research -> Plan -> Implement.
- Gap detection forcado + `gaps.md` com sugestao de solucao.
- Persistencia de contexto por projeto.
- Defesa contra vazamentos/hallucinacoes/bugs: allowlists, redaction e limites operacionais.

## Evidencias / referencias externas (para consultar durante implementacao)
- SynkraAI/aios-core (repo): https://github.com/SynkraAI/aios-core
- LangGraph (repo): https://github.com/langchain-ai/langgraph
- CrewAI (repo): https://github.com/crewAIInc/crewAI

> Nota: esta feature nao fara "vendoring escondido" de codigo. Integracao preferencial:
> - dependencias opcionais (LangGraph/CrewAI)
> - reimplementacao (aios-core)
> - se houver vendoring pontual (MIT), manter `THIRD_PARTY_NOTICES.md` e LICENSEs em `third_party/`.

## Estado atual do repo (gaps que bloqueiam implementacao)
- `factory-workflow/context/core/vision.md` etc estao pendentes e apontam para GAP-CORE-001..007.
- Referencias obrigatorias quebradas em tooling:
  - `factory-workflow/context/tooling/mcp-policy.md` nao existe (GAP-TOOLING-003)
  - `factory-workflow/context/tooling/runtime.md` nao existe (GAP-TOOLING-004)

## Decisoes-chave (propostas)
1) Python-first como linguagem primaria; Node nao obrigatorio.
2) Camadas opcionais: `securecontextfactory[langgraph]` e `securecontextfactory[crewai]`.
3) CLI oficial: `securecontextfactory` (Typer + Rich), com wizard e comandos de execucao governada.
4) Orquestracao: gates como nodes condicionais (LangGraph) e/ou wrappers de tasks (Crew).
5) Audit trail: JSONL + bundles de evidencias, sempre gerados por comando/execucao.

## Artefatos planejados
- `pyproject.toml` + pacote `src/securecontextfactory/` com CLI.
- `docs/pt-BR` e `docs/en` (estrutura espelhada).
- `examples/` com 3 flows: feature delivery, security audit, UI change (reuse/MCP).
- CI basico (lint/test) e estrategia de release semantico.

