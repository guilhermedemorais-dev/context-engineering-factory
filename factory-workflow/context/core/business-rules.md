# Business Rules

## Regras de negocio explicitas
- BR-001: Nenhuma escrita de codigo/config sensivel sem plan aprovado.
- BR-002: Nenhum deploy/release sem evidencias de QA.
- BR-003: Nenhuma acao destrutiva sem confirmacao humana registrada.
- BR-004: Se existir duvida relevante (requisito/escopo/risco/impacto), abrir GAP com sugestao e parar.
- BR-005: Reuso antes de criar (MCP/registry/design-system).

## Condicoes, excecoes e validacoes
- Excecao permitida sem plan aprovado: escrever/atualizar artefatos de Research/Plan e registrar gaps.
- Validacoes minimas antes de execucao:
  - contexto carregado conforme `factory-workflow/context/INDEX.md`
  - sem gaps bloqueantes OPEN
  - plan aprovado para implementacao
  - paths permitidos (restricoes do runtime)

## Regras que NAO podem ser violadas
- Nao inventar requisitos.
- Nao "editar contexto para passar gate" (contexto e fonte de verdade).
- Nao registrar evidencias falsas.
- Nao persistir secrets/PII em texto plano no repo.

## O que acontece em caso de erro
- Se regra/gate falhar: retornar `BLOCKED`, registrar audit event e (quando aplicavel) abrir GAP com sugestao.
- Se operacao for de risco e nao houver aprovacao humana: abortar com instrucao clara de como aprovar.
