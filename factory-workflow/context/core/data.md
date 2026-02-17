# Data

## Entidades principais
- ContextPack: conjunto de arquivos de contexto (INDEX + core/quality/ui/tooling/codex).
- Gap: registro de falta/ambiguo/conflito com sugestao de solucao.
- Research: evidencias (links, resultados) que justificam o plan.
- Plan: escopo, passos, testes, criterios e aprovacao humana.
- AuditEvent: evento append-only (JSONL) de execucao/decisao.
- EvidenceBundle: conjunto de paths/artefatos gerados (logs, relatorios, outputs).
- GraphRun: execucao stateful (run_id, checkpoints).
- SquadRun: execucao colaborativa (squad/crew id, tasks, outputs).

## Campos importantes e significados
- Gap:
  - ID, Data, Descricao, Impacto, Status, Owner, Sugestao de Solucao
- Plan:
  - Status (DRAFT/APPROVED/CHANGES_REQUESTED), Aprovador, Data, Observacoes
- AuditEvent:
  - ts, actor, action, inputs (redacted), outputs (paths), status (OK/BLOCKED/FAILED)

## Relacionamentos conceituais
- ContextPack orienta Research/Plan.
- Gaps bloqueiam execucao ate decisao/mitigacao.
- Plan aprovado autoriza Implement + QA.
- AuditEvent referencia EvidenceBundle (paths) para rastreabilidade.

## Dados sensiveis
- Tokens (GitHub/Context7/HF), chaves, credenciais, cookies.
- PII/segredos do negocio (dados de clientes, contratos, segredos comerciais).
- Regra: secrets via `.env`/vault; logs devem aplicar redaction.

## O que NAO deve ser persistido
- Secrets em texto plano dentro do repo.
- Dumps completos de outputs grandes de MCP no contexto ativo (gerar arquivo e resumir).
- Chaves/identificadores de producao sem necessidade (minimizacao).
