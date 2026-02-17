# MCP Policy

## Objetivo
Definir regras obrigatorias para uso de MCPs (Model/Context/Component Providers) durante Research/Plan/Implement/QA.

## Principios
- Reuso antes de criar (consultar servidores/registries).
- Evidencia antes de implementar (referencias e outputs resumidos).
- Seguranca por default (secrets/PII nunca em texto plano no repo).
- Auditabilidade: chamadas e resultados relevantes devem deixar trilha (links/paths).

## Allowed / Denied
### Allowed (padrao)
- MCPs de documentacao/conhecimento (ex.: Context7, StackOverflow) durante Research.
- MCPs de repositorio (ex.: GitHub) para evidencias (issues/PRs/tags/commits).
- MCPs de modelos/datasets (ex.: HuggingFace) para pesquisa e validacao.
- MCPs locais de automacao (ex.: Playwright/Chrome DevTools) para QA e evidencias.

### Denied (por default)
- Ferramentas que executam acao destrutiva sem confirmacao humana (delete/reset/wipe).
- Qualquer integracao que exfiltra segredos/PII.
- "Web browsing" sem registrar evidencias (links) em Research/Plan.

## Regras de secrets e PII
- Tokens e credenciais: somente via `.env`/vault (nunca commit).
- Logs e arquivos de evidencias devem aplicar **redaction** quando houver risco de secret.
- Se um output de MCP contiver secret/PII: parar, registrar GAP e exigir acao humana.

## Regras de evidencia
- Outputs grandes: salvar em arquivo e colocar no contexto ativo apenas **sumario objetivo**.
- Research/Plan devem conter links e paths para qualquer evidencia usada para decisao.
- Nao "inventar" resultados de MCP: se nao foi consultado/nao ha link, trate como desconhecido.

## Human approval (operacoes de risco)
Obrigatorio solicitar aprovacao humana registrada para:
- deploy/release para producao
- mudancas destrutivas (delete/reset)
- mudancas de seguranca/credenciais/politicas
- escrita fora do path permitido do projeto (quando aplicavel)

## Relacoes
- Gates: `factory-workflow/cicd/gates.md`
- Policy engine: `factory-workflow/policies/policy-engine.md`
- Registries: `factory-workflow/libs/mcp/registries/*`
- Servers: `factory-workflow/libs/mcp/servers/*`

