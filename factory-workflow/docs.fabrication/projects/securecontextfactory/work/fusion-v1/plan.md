# Plan — SecureContextFactory (fusion-v1)

> Objetivo: transformar Research em execucao segura e previsivel.

## Aprovação do Plan
- Status: APPROVED
- Aprovador: guimp
- Data: 2026-02-17
- Observações: Fusão "SecureContextFactory" (core + CLI Python + camadas opcionais LangGraph/CrewAI + UX inspirada no aios-core).

---

## Contexto e referências
- Docs internas relevantes:
  - `factory-workflow/context/INDEX.md`
  - `factory-workflow/policies/policy-engine.md`
  - `factory-workflow/cicd/gates.md`
  - `factory-workflow/docs.fabrication/workflow.md`
- Research:
  - `factory-workflow/docs.fabrication/projects/securecontextfactory/work/fusion-v1/research.md`

## Escopo
### Inclui
- Definir SecureContextFactory como produto (vision/scope/requirements) e fechar gaps bloqueantes no contexto core.
- Criar a camada de CLI Python (Typer + Rich) como fachada oficial do framework:
  - `securecontextfactory init`
  - `securecontextfactory install` (wizard/env/MCP/skills)
  - `securecontextfactory autopilot-graph` (LangGraph opcional)
  - `securecontextfactory run-squad` (CrewAI opcional)
  - `securecontextfactory audit` / `securecontextfactory gap` (governanca)
- Implementar governanca como componente central:
  - policy-engine executavel (checks) antes de qualquer escrita/deploy/destrutivo
  - gates como checks e como nodes condicionais no graph
  - `gaps.md` como mecanismo de "stop-and-suggest"
- Corrigir referencias obrigatorias quebradas:
  - criar `factory-workflow/context/tooling/mcp-policy.md`
  - criar `factory-workflow/context/tooling/runtime.md`
  - atualizar `factory-workflow/context/INDEX.md` (incluir tooling) e `factory-workflow/context/codex/implementation-rules.md` conforme necessario
- Documentacao minima:
  - README rebrand para SecureContextFactory
  - `docs/pt-BR` + `docs/en` quickstart
  - 1 exemplo executavel (hello-factory + gated pipeline)

### Não inclui
- Vendoring amplo de repos externos.
- SaaS/hosted platform.
- Auto-deploy para producao sem aprovacao humana.
- Reimplementacao completa de LangGraph/CrewAI (fica como backlog; inicialmente integracao via dependencias opcionais).

## Requisitos / critérios de aceite
- [ ] Nome do projeto/documentacao/CLI: **SecureContextFactory** (exato) em locais relevantes.
- [ ] Contexto core preenchido (vision/scope/requirements/business-rules/data/glossario/principios) sem gaps bloqueantes OPEN.
- [ ] `securecontextfactory init` cria layout de contexto por projeto + audit trail local.
- [ ] `securecontextfactory install` configura `.env` placeholders + instala skills globais (opcional).
- [ ] Governanca enforced:
  - [ ] sem plan APPROVED: comandos que executam implementacao retornam BLOCKED
  - [ ] gaps bloqueantes: pipeline para e registra audit event
  - [ ] operacoes de risco exigem confirmacao humana
- [ ] Integração opcional:
  - [ ] sem LangGraph instalado: `autopilot-graph` falha com mensagem clara de instalacao
  - [ ] sem CrewAI instalado: `run-squad` falha com mensagem clara de instalacao
- [ ] Docs + exemplo minimo rodando localmente.

## Arquivos alvo (intenção)
- `pyproject.toml`
- `src/securecontextfactory/**`
- `README.md`
- `docs/pt-BR/**`, `docs/en/**`
- `examples/**`
- `factory-workflow/context/**` (fechamento de gaps + tooling)
- `factory-workflow/cicd/gates.md` (ajustes de fontes de verdade, se necessario)

## Plano de execução (passo a passo)
1. Fechar gaps bloqueantes do core:
   - preencher `factory-workflow/context/core/*.md` com definicoes do SecureContextFactory
   - atualizar `factory-workflow/context/core/gaps.md` (Status DECIDED para GAP-CORE-001..007, GAP-TOOLING-003/004)
2. Criar `factory-workflow/context/tooling/mcp-policy.md` e `factory-workflow/context/tooling/runtime.md`.
3. Criar pacote Python `securecontextfactory` (Typer + Rich) com comandos:
   - init/install/audit/gap
   - adapters opcionais: LangGraph (graphs) e CrewAI (squads)
4. Implementar policy-engine executavel (checks reutilizaveis):
   - `require_plan_approved()`
   - `require_no_blocking_gaps()`
   - `require_human_approval(action=...)`
5. Integrar com o runtime atual:
   - comando para acionar `factory-workflow/bots/runtime/cli.py autopilot-start/build` ou equivalente via import
6. Documentacao e exemplos:
   - README SecureContextFactory
   - quickstart PT/EN
   - `examples/hello-securecontextfactory/`
7. CI basico:
   - `pytest` para gates/policy checks
   - lint (ruff/black) via pre-commit (opcional)

## Roadmap (para "quero tudo" sem travar a entrega)
- v0.1 (fusion-v1): governanca + CLI + integracoes opcionais + 1 exemplo + CI basico.
- v0.2: wizard "aios-core-like" completo (doctor, env detect, templates), hooks multi-IDE (instalador), squads registry + templates.
- v0.3: LangGraph pipelines completos (branching/retries + checkpoints duraveis) mapeando gates como nodes; resume/pause oficial.
- v0.4: Crew engine avancado (delegacao, hierarquia, paralelismo, manager policies) + observabilidade.
- v0.5+: engines nativas (sem LangGraph/CrewAI) como opcao "no deps", mantendo compatibilidade.

## Plano de testes
### Unit
- policy-engine: plan approved check, gaps scan, approvals flow.
- CLI: parse + retorno de exit codes BLOCKED.

### Integration
- `securecontextfactory init` + `audit` gerando JSONL.
- `install` copiando skills para XDG path (com dry-run opcional).

### E2E (se aplicável)
- smoke test: `securecontextfactory init` -> `autopilot-graph` (quando extra langgraph instalado) -> bloqueia/continua conforme gates.

### QA evidências esperadas
- logs/relatorios em paths definidos (audit JSONL + outputs do runtime quando acionado).

## Riscos e mitigação
- Risco: escopo grande e friccao de governanca.
  - Mitigação: entregar v0.1 com CLI + governanca + integracoes opcionais; backlog para engines nativas.
- Risco: divergencia entre "gates docs" e "gates executaveis".
  - Mitigação: testes unitarios dos checks + mapeamento claro docs->codigo.

## Rollback / estratégia de deploy (se aplicável)
- N/A (framework local). Releases somente apos QA + changelog + tag.
