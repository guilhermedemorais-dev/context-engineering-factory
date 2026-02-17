# Glossary

## Objetivo
Definir termos canonicos usados pelo SecureContextFactory para reduzir ambiguidade.

## Termos
- **RPI**: Research -> Plan -> Implement. Sequencia obrigatoria.
- **ContextPack**: conjunto de arquivos de contexto por projeto em `factory-workflow/context/**`.
- **GAP**: falta/ambiguo/conflito no contexto que bloqueia decisao/execucao. Sempre inclui sugestao.
- **Gate**: verificador (manual ou executavel) que valida conformidade (contexto, reuse, QA, release).
- **Policy-engine**: regras inegociaveis (ex.: sem plan aprovado, sem deploy sem QA, sem destrutivo sem humano).
- **Plan APPROVED**: status que autoriza implementacao; deve registrar aprovador e data no `plan.md`.
- **Evidence**: evidencias objetivas (paths, logs, relatorios) que sustentam decisoes e QA.
- **Audit trail**: trilha append-only de eventos/decisoes/execucoes (ex.: JSONL).
- **MCP**: providers de contexto/conhecimento/ferramentas (Context7, GitHub, HF, Playwright etc).
- **Registry**: catalogo de reuso (UI/components/docs) consultado antes de criar.
- **Squad/Crew**: conjunto de agentes com roles/goals/backstory e delegacao (camada colaborativa).
- **Graph**: orquestracao stateful (nodes/edges) com branching/cycles/retries e checkpoints.
- **Checkpoint**: persistencia de estado da execucao para pause/resume e durabilidade.
- **Human approval**: aprovacao humana registrada, exigida para operacoes de risco (policy-engine).
- **BLOCKED**: status que indica execucao parada por gate/policy/gap; deve trazer proximo passo.
- **GO/NO-GO**: decisao de release baseada em evidencias, gates e riscos.

