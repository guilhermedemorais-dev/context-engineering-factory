# Runtime Policy (Local Execution)

## Objetivo
Definir o contrato do runtime local (bots/CLI) e suas restricoes operacionais para garantir seguranca, auditabilidade e previsibilidade.

## Modelo de execucao
- O runtime executa bots locais (context-sync, planner, dev, qa, review) via fila (jobs) ou execucao direta.
- O runtime gera logs e evidencias em um output_root configuravel (padrao: `factory-workflow/bots/runtime/out/`).
- O runtime deve respeitar o policy-engine e gates antes de qualquer escrita/acao de risco.

## Paths e limites
- Workspace: raiz do projeto atual (informada via `--workspace`).
- Factory root: `factory-workflow/` dentro do workspace (padrao).
- Restricao de escrita:
  - Implementacao (dev) deve escrever apenas dentro do projeto permitido (ex.: `/apps/<project>` quando aplicavel).
  - Artefatos de fabricacao (research/plan/release) devem ir para os paths canonicos definidos pelo workflow.

## Configuracao canonica
- Runtime config: `factory-workflow/bots/runtime/config.yaml`
- MCP config (local, gitignored): `factory-workflow/config/mcp.toml`
- Env vars: `.env` (gitignored) no workspace.

## Logging e audit trail
- Cada execucao deve gerar:
  - log (append) com timestamp e status
  - lista de deliverables (paths)
  - gaps abertos (quando houver)
- Evidencias de QA devem ser gravadas em `factory-workflow/tests/reports/**` quando aplicavel.

## Rede e ferramentas
- Rede deve ser tratada como restrita: apenas endpoints configurados (MCPs) e conforme politica.
- Operacoes destrutivas e deploy exigem aprovacao humana registrada.

## Enforcement (policy-engine)
O runtime/CLI deve validar antes de executar:
1) Context compliance (`factory-workflow/context/INDEX.md`).
2) Sem gaps bloqueantes OPEN (`factory-workflow/context/core/gaps.md`).
3) Plan aprovado para implementacao.
4) Confirmacao humana para operacoes de risco.

## Relacoes
- Workflow: `factory-workflow/docs.fabrication/workflow.md`
- Gates: `factory-workflow/cicd/gates.md`
- Policy engine: `factory-workflow/policies/policy-engine.md`

