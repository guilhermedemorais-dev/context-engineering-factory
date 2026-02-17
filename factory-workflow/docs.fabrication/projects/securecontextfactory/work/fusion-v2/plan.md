# Plan — SecureContextFactory (fusion-v2)

> Objetivo: entregar v0.2 com wizard/doctor + hooks multi-IDE + squads registry/templates, mantendo governanca inegociavel.

## Aprovação do Plan
- Status: APPROVED
- Aprovador: guimp
- Data: 2026-02-17
- Observações: Aprovado via chat: "segue pra versão dois".

---

## Contexto e referências
- Research:
  - `factory-workflow/docs.fabrication/projects/securecontextfactory/work/fusion-v2/research.md`
- Fontes de verdade:
  - `factory-workflow/context/INDEX.md`
  - `factory-workflow/policies/policy-engine.md`
  - `factory-workflow/cicd/gates.md`

## Escopo
### Inclui
- Adicionar `securecontextfactory doctor` (env detect + checks de governanca/config).
- Adicionar `securecontextfactory hook install ...` (workspace hooks):
  - VSCode/Cursor tasks (autopilot/daemon/audit)
  - AGENTS.md / .cursorrules (instrucoes de governanca)
- Adicionar `securecontextfactory squad ...`:
  - registry + templates versionados em `factory-workflow/squads/`
  - comandos: list/init/show
  - `run-squad` passa a carregar definicao do squad quando existir.
- Templates/scaffold minimo para projeto local:
  - `securecontextfactory project init <name>` (cria `apps/<name>/` + work artifacts base)
- Hardening: gaps do runtime devem respeitar formato canonico e incluir sugestao (sem corromper arquivo).

### Não inclui
- Hooks que escrevem fora do workspace (ex.: alterar ~/.config) por default.
- Implementacao completa de ADE/memory engine.

## Criterios de aceite
- [ ] `securecontextfactory doctor` identifica problemas comuns (mcp/env/plan/gaps/deps) e nao vaza secrets.
- [ ] `securecontextfactory hook install vscode` cria/atualiza `.vscode/tasks.json` sem apagar tasks existentes.
- [ ] `securecontextfactory hook install agents` cria/atualiza `AGENTS.md` com regras principais.
- [ ] `securecontextfactory squad init <name>` cria template YAML.
- [ ] `securecontextfactory squad list` lista squads instalados.
- [ ] `securecontextfactory run-squad <name>` usa definicao quando existir (fallback seguro se nao existir).
- [ ] Runtime continua registrando gaps com sugestao e sem quebrar `gaps.md`.

## Plano de execucao
1. Criar pasta `factory-workflow/squads/` + templates.
2. Implementar comandos `doctor`, `hook`, `squad` na CLI.
3. Atualizar `run-squad` para usar definicoes.
4. Hardening no runtime gaps (sanitize/truncate).
5. Ajustar docs (quickstart + README) para novos comandos.
6. Garantir compilacao e testes unitarios basicos (onde aplicavel).
