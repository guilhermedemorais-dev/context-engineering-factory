# Gaps

## O que sao gaps
Gaps sao faltas, ambiguidades ou conflitos no contexto que bloqueiam decisao ou execucao.

## Template de gap (canonico)
- ID:
- Data: YYYY-MM-DD
- Descricao:
- Impacto:
- Owner:
- Status: OPEN | DECIDED | DEFERRED
- **Sugestao de Solucao:** (obrigatório - o agente DEVE propor uma solução para o dev aprovar)

## Regra
- Qualquer duvida bloqueante deve ser registrada aqui.
- **Todo gap DEVE incluir uma Sugestao de Solucao.** O desenvolvedor pode aprovar, rejeitar ou discutir.
- O desenvolvedor responde: "Aplique a sugestão do GAP-XXX" ou discute alternativas.


## Gaps Abertos

(sem gaps abertos no momento)

## Gaps Resolvidos

### GAP-CORE-008
- ID: GAP-CORE-008
- Data: 2026-01-13
- Descricao: Canonico definido para qualidade: factory-workflow/context/quality/.
- Impacto: DOCUMENTACAO_INCONSISTENTE
- Owner: TBD
- Status: DECIDED

### GAP-TOOLING-001
- ID: GAP-TOOLING-001
- Data: 2026-01-17
- Descricao: Nao existia .gitignore para proteger `factory-workflow/config/mcp.toml` (arquivo real de configuracao MCP).
- Impacto: RISCO_DE_SECRET
- Owner: TBD
- Status: DECIDED

### GAP-CORE-001
- ID: GAP-CORE-001
- Data: 2026-01-13
- Descricao: Definir visao do sistema (por que existe, problema, publico-alvo, objetivos e nao objetivos).
- Impacto: BLOQUEIA
- Owner: guimp
- Status: DECIDED
- Decisao: Aprovado em 2026-02-17.
- **Sugestao de Solucao:** Adotar como visao do SecureContextFactory: "Framework Python-first para desenvolvimento com IA rapido e seguro, com governanca inegociavel (gates/policies/audit/human approval) e contexto persistente para eliminar amnesia, drift de especificacao e mudancas nao auditaveis". Publico-alvo: devs solo, squads pequenas e tech leads/enterprises com compliance. Nao-objetivos: SaaS, auto-deploy para producao sem humano, e bypass de gates.

### GAP-CORE-002
- ID: GAP-CORE-002
- Data: 2026-01-13
- Descricao: Definir escopo dentro/fora, suposicoes, restricoes e dependencias externas.
- Impacto: BLOQUEIA
- Owner: guimp
- Status: DECIDED
- Decisao: Aprovado em 2026-02-17.
- **Sugestao de Solucao:** Escopo dentro: CLI wizard (init/install), RPI+gates executaveis, gap tracking forcado, integracoes opcionais (LangGraph/CrewAI), runtime/bots + skills, MCP policy e audit trail. Fora: plataforma hospedada, "autonomia irrestrita", e features sem evidencias/QA. Restricoes: sem Node obrigatorio; operacoes de risco exigem aprovacao humana. Dependencias externas (opcionais): LangGraph/CrewAI, providers MCP (Context7/GitHub/HF/Playwright).

### GAP-CORE-003
- ID: GAP-CORE-003
- Data: 2026-01-13
- Descricao: Definir requisitos funcionais, nao funcionais e criterios de aceite.
- Impacto: BLOQUEIA
- Owner: guimp
- Status: DECIDED
- Decisao: Aprovado em 2026-02-17.
- **Sugestao de Solucao:** RF: comandos `securecontextfactory init/install/audit/gap/run-squad/autopilot-graph`, enforce de policy-engine antes de escrita/deploy/destrutivo, checkpoints e execucao stateful (opcional), squads com roles/backstories (opcional), contexto por projeto. RNF: auditabilidade por default, reproducibilidade, seguranca (redaction/allowlists), UX "one-command", compatibilidade Linux/macOS/WSL. Criterios: sem plan APPROVED => BLOCKED; sem gaps bloqueantes => executa; evidencias geradas em bundle.

### GAP-CORE-004
- ID: GAP-CORE-004
- Data: 2026-01-13
- Descricao: Definir regras de negocio, excecoes e validacoes.
- Impacto: BLOQUEIA
- Owner: guimp
- Status: DECIDED
- Decisao: Aprovado em 2026-02-17.
- **Sugestao de Solucao:** Regras canonicas: (1) sem plan aprovado: proibido escrever codigo/config sensivel (excecao: docs de Research/Plan) (2) sem QA evidence: proibido release/deploy (3) qualquer duvida relevante => GAP com sugestao e STOP (4) acao destrutiva => confirmacao humana registrada (5) reuso antes de criar (MCP/registry/design-system). Excecoes: allowlist explicita (ex.: gerar plan/research).

### GAP-CORE-005
- ID: GAP-CORE-005
- Data: 2026-01-13
- Descricao: Definir entidades, campos, relacionamentos e dados sensiveis.
- Impacto: BLOQUEIA
- Owner: guimp
- Status: DECIDED
- Decisao: Aprovado em 2026-02-17.
- **Sugestao de Solucao:** Definir entidades minimas: ContextPack (INDEX + core/quality/ui/tooling), GAP (id/status/impact/sugestao), Plan (status/aprovador/data/escopo/testes), ApprovalRecord (acao/aprovador/data), AuditEvent (jsonl), EvidenceBundle (paths), GraphRun (run_id/checkpoints), SquadRun (crew_id). Dados sensiveis: tokens, segredos, PII. Regra: nunca persistir segredos no repo; usar `.env`/vault e aplicar redaction em logs.

### GAP-CORE-006
- ID: GAP-CORE-006
- Data: 2026-01-13
- Descricao: Definir glossario com termos de negocio e tecnicos.
- Impacto: BLOQUEIA
- Owner: guimp
- Status: DECIDED
- Decisao: Aprovado em 2026-02-17.
- **Sugestao de Solucao:** Criar/atualizar glossario canonico em `factory-workflow/docs.fabrication/glossary.md` (ou criar alias em `factory-workflow/docs/glossary.md` se necessario) contendo termos: GAP, Gate, Policy-engine, Plan APPROVED, Evidence, RPI, MCP, Registry, Squad/Crew, Graph, Checkpoint, Human approval, BLOCKED/GO/NO-GO.

### GAP-CORE-007
- ID: GAP-CORE-007
- Data: 2026-01-13
- Descricao: Definir principios, prioridades e trade-offs.
- Impacto: BLOQUEIA
- Owner: guimp
- Status: DECIDED
- Decisao: Aprovado em 2026-02-17.
- **Sugestao de Solucao:** Principios: seguranca/auditabilidade > autonomia; explicito > implicito; stop-and-suggest > suposicao; reuso > reinvencao; RPI obrigatorio; contexto por projeto; human approval para risco. Trade-offs: mais friccao inicial em troca de menos retrabalho/incidentes; dependencias opcionais para tracao vs engines nativas como backlog.

### GAP-TOOLING-002
- ID: GAP-TOOLING-002
- Data: 2026-01-19
- Descricao: Chrome DevTools MCP nao possui cliente/tooling implementado no runtime (bot existe, mas depende de MCP externo).
- Impacto: BLOQUEIA auditoria automatizada via CLI sem MCP externo.
- Owner: guimp
- Status: DEFERRED
- Decisao: Aprovado em 2026-02-17 (nao implementado em fusion-v1).
- Next step: implementar cliente MCP (CDP) no runtime ou integrar executor externo.
- **Sugestao de Solucao:** Implementar um executor local minimo (CDP via websocket) no runtime para o bot `qa-e2e-browser-audit`, com allowlist de comandos e output em `factory-workflow/bots/runtime/out/`. Alternativa: integrar Playwright para coletar metricas essenciais quando CDP nao estiver disponivel, mantendo audit trail.

### GAP-TOOLING-003
- ID: GAP-TOOLING-003
- Data: 2026-02-17
- Descricao: `factory-workflow/context/tooling/mcp-policy.md` foi referenciado como leitura obrigatoria em `factory-workflow/context/INDEX.md`, mas o arquivo nao existe.
- Impacto: BLOQUEIA (politica MCP indefinida / referencia quebrada).
- Owner: guimp
- Status: DECIDED
- Decisao: Aprovado em 2026-02-17.
- **Sugestao de Solucao:** Criar `factory-workflow/context/tooling/mcp-policy.md` com politica canonica (tipos de MCP permitidos, requisitos de audit trail/logging, regras de secrets, allow/deny de ferramentas, e exigencias de "human approval" para operacoes de risco). Alternativamente, remover o item do `INDEX.md` e ajustar `factory-workflow/context/codex/implementation-rules.md` para tratar a politica MCP como opcional, mas isso enfraquece a governanca.

### GAP-TOOLING-004
- ID: GAP-TOOLING-004
- Data: 2026-02-17
- Descricao: `factory-workflow/context/tooling/runtime.md` e referenciado em multiplos pontos (gates, governanca, quickstart), mas o arquivo nao existe (a pasta `factory-workflow/context/tooling/` tambem nao existe).
- Impacto: BLOQUEIA (politica/contrato do runtime indefinidos; referencias quebradas).
- Owner: guimp
- Status: DECIDED
- Decisao: Aprovado em 2026-02-17.
- **Sugestao de Solucao:** Criar `factory-workflow/context/tooling/runtime.md` (e a pasta `factory-workflow/context/tooling/`) definindo: modelo de execucao local, limites do runtime (paths permitidos, IO, rede), configuracao canonica (config.yaml, queue_dir, output_root), regras de auditoria/logs, e como o policy-engine deve ser aplicado antes de qualquer escrita/deploy.
