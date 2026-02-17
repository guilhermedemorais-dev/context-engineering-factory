# Requirements

## Requisitos funcionais (RF)
- RF-001: Manter governanca inegociavel (policy-engine + gates + audit trail).
- RF-002: Workflow RPI obrigatorio com aprovacao humana do plan antes de qualquer implementacao.
- RF-003: Detectar gaps bloqueantes e registrar em `factory-workflow/context/core/gaps.md` com sugestao de solucao; parar execucao.
- RF-004: CLI oficial `securecontextfactory` com comandos:
  - `init` (bootstrap do projeto + scaffolds minimos)
  - `install` (wizard de ambiente/MCP e instalacao de skills)
  - `doctor` (diagnostico de ambiente/governanca/config sem vazamento de secrets)
  - `hook install` (instalador de hooks no workspace para IDEs/agentes)
  - `squad` (registry/templates: list/init/show)
  - `project init` (scaffold minimo em `apps/<name>/`)
  - `autopilot-start` / `autopilot-build` (pipeline do runtime atual com gates)
  - `autopilot-graph` (pipeline stateful com checkpoints, opcional)
  - `run-squad` (execucao colaborativa via squads/crews, opcional)
  - `audit` (verificar gates e evidencias)
  - `gap` (criar/listar/fechar gaps)
- RF-005: Integrar com runtime/bots existentes (context-sync/planner/dev/qa/review) sem quebrar compatibilidade.

## Requisitos nao funcionais (RNF)
- RNF-001: Auditabilidade por default (eventos e evidencias devem ser gravados em paths definidos).
- RNF-002: Reprodutibilidade (mesmo input/contexto => mesma sequencia de gates/acoes).
- RNF-003: Segurança: redaction de secrets em logs, allowlists e confirmacao humana para risco.
- RNF-004: UX "one-command" com mensagens de erro acionaveis (BLOCKED com motivo e proximo passo).
- RNF-005: Compatibilidade Linux/macOS/WSL (quando aplicavel).
- Ver tambem:
  - `factory-workflow/context/quality/quality-bars.md`
  - `factory-workflow/context/quality/test-strategy.md`

## Criterios de aceite (alto nivel)
- Sem `plan.md` com `Status: APPROVED`: comandos que executam implementacao retornam BLOCKED.
- Com gaps bloqueantes OPEN: pipeline retorna BLOCKED e registra evidencias/audit.
- Comandos opcionais (LangGraph/CrewAI) falham de forma clara quando deps nao estao instaladas.
- Evidencias de QA sao registradas nos paths esperados antes de release/deploy.

## Requisito vs decisao futura
- Requisito: deve estar explicitamente definido no contexto.
- Decisao futura: item sem definicao atual, registrar em factory-workflow/context/core/gaps.md.
