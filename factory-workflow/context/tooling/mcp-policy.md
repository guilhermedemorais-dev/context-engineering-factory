# Politica MCP (Model/Context/Component Providers)

## Objetivo
Garantir reuso, evidencias e governanca no uso de MCPs.

## Regras principais
- **Reuso antes de criar.**
- Prioridade de consulta:
  1) Docs oficiais
  2) MCP de docs oficiais (ex.: Context7)
  3) StackOverflow (auxiliar, nunca autoridade final)
- **Nao inventar:** se nao cobrir, registrar GAP e parar.

## Regras de evidencia
- Sempre guardar links/fontes no `research.md` e/ou `plan.md`.
- Evidencia deve incluir **o trecho relevante** ou sumario do achado.

## Mapeamento canonico (recomendado)
- **Context7**: documentacao oficial e API
- **shadcn**: UI registry/components
- **Playwright**: QA automation
- **GitHub**: issues/PRs/operacoes
- **Security audit**: auditoria de dependencias
- **HuggingFace (futuro)**: IA multimodal/artefatos
- **StackOverflow**: auxiliar, com validacao cruzada

## Politica de MCP blob
- Outputs grandes **vao para arquivo** dedicado.
- O contexto ativo recebe apenas **sumario curto**.

## Relacoes
- Servidores MCP: `factory-workflow/libs/mcp/servers/README.md`
- Registries MCP: `factory-workflow/libs/mcp/registries/README.md`
- Quality bars: `factory-workflow/context/quality/quality-bars.md`
- Gates: `factory-workflow/cicd/gates.md`
