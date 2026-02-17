# Glossário (SecureContextFactory)

Este glossário existe para reduzir ambiguidade de termos.

## Termos

### Contexto (sources of truth)
Conjunto de documentos em `factory-workflow/context/*` que define regras, requisitos, políticas e padrões.

### Gap
Qualquer informação necessária para executar (plan/implement/QA) que está **indefinida**, **conflitante** ou **não coberta**. Deve ser registrado em `factory-workflow/context/core/gaps.md`.

### Research
Etapa de levantamento com **evidências**. Saída típica: `research.md` com links e conclusões.

### Plan
Documento executável (por humanos e agentes) com escopo, passos e testes. A Implementação só começa com plan aprovado.

### Plan aprovado
Gate humano explícito registrado no `plan.md` (ver `factory-workflow/docs/workflow.md`).

### Policy-engine
Regras inegociaveis aplicadas antes de qualquer escrita, deploy ou acao destrutiva. Ver `factory-workflow/policies/policy-engine.md`.

### Audit trail
Trilha append-only de eventos/decisoes/execucoes, com timestamps e evidencias (paths).

### Evidence
Evidencias objetivas (logs, relatorios, links, paths) que sustentam decisoes, QA e release.

### MCP
Providers de contexto/conhecimento/ferramentas (ex.: Context7, GitHub, HuggingFace, Playwright). Ver `factory-workflow/libs/mcp/*`.

### Registry
Catalogo de reuso consultado antes de criar (ex.: registries de UI/componentes).

### Squad/Crew
Conjunto de agentes com roles/goals/backstory e delegacao para executar tasks sob governanca.

### Graph
Orquestracao stateful via nodes/edges com branching/cycles/retries e checkpoints.

### Checkpoint
Persistencia de estado para pause/resume e execucao duravel.

### Human approval
Aprovacao humana registrada, exigida para operacoes de risco (policy-engine).

### BLOCKED
Status de execucao que indica parada por gap/gate/policy, com motivo e proximo passo.

### Bot
Agente executável (normalmente Python via CLI local) com contrato de entrada/saída.

### Engine
Componente lógico de responsabilidade (planner, execution, quality, security, doc, distribution). Pode orquestrar bots.

### Gate
Critério de bloqueio em pipeline (CI/CD) ou em processo. Ver `factory-workflow/cicd/gates.md`.
