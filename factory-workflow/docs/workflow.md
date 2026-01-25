# Workflow oficial: RPI (Research → Plan → Implement)

## Objetivo
Reduzir retrabalho, evitar overengineering e impedir reinvencao da roda.

## Definicao do fluxo
1) **Research**
   - Buscar evidencias (docs oficiais, MCP, referencias)
   - Mapear riscos e alternativas
   - Registrar gaps se nao houver cobertura
2) **Plan**
   - Definir escopo, arquivos e passos
   - Especificar testes e criterios de aceite
   - Consolidar evidencias
3) **Implement**
   - Executar somente apos Plan aprovado
   - Atualizar codigo + docs + testes
4) **QA**
   - Executar testes e auditorias apos Implement
   - Para UI navegavel, rodar `qa-e2e-browser-audit` (Chrome DevTools MCP)
   - Registrar relatorios e evidencias

## Autonomia (skill resolver + engines)
1) Orchestrator recebe intent
2) Skill resolver detecta gaps e monta fila de agentes
3) Planner engine gera research + plan
4) Execution engine aplica mudancas aprovadas
5) Quality + Security engines validam e registram evidencias
6) Doc engine atualiza docs e arquitetura
7) Distribution engine prepara release apos QA

## Policy engine (nao opcional)
- Nenhuma escrita sem plan aprovado
- Nenhum deploy sem QA engine
- Nenhuma decisao sem justificativa registrada
- Nenhuma acao destrutiva sem confirmacao humana

## Regras de contexto
- **Keep context utilization < 40%** (guideline).
- **Intentional compaction**: ao trocar de sessao, gerar `progress.md`.
- Contexto grande = sumarizar, anexar arquivo e reduzir contexto ativo.

## Artefatos canonicos por feature/ticket
Caminho sugerido:
- `factory-workflow/docs/projects/<projeto>/work/<feature>/`

Arquivos:
- `research.md` (evidencias e links)
- `plan.md` (escopo, passos, testes)
- `progress.md` (compaction e handoff)
- `decisions.md` (decisoes e trade-offs)

## Gates humanos
- **Research review** (rapido, validar evidencias)
- **Plan review** (obrigatorio)
- **Implement** so inicia apos Plan aprovado

## Politica de MCP durante Research
- MCP outputs grandes **vao para arquivo**.
- O contexto ativo recebe apenas **sumario objetivo**.
- Evidencias (links) ficam no `research.md` e/ou `plan.md`.

## Definition of Ready (para iniciar Implement)
- `plan.md` completo com:
  - arquivos alvo
  - passos de execucao
  - passos de teste
  - evidencias (links)
- Nenhum gap aberto bloqueante em `factory-workflow/context/core/gaps.md`.
- Plan aprovado (gate humano).

## Conexoes obrigatorias
- Qualidade: `factory-workflow/context/quality/*`
- Gates CI/CD: `factory-workflow/cicd/gates.md` e `factory-workflow/cicd/checklist.md`
- Governanca: `factory-workflow/governance/*` (ADRs, risks)
- Arquitetura autonoma: `factory-workflow/docs/architecture/autonomous-factory.md`
