# Factory Docs

## Objetivo
Esta pasta publica a documentacao de uso do framework, com guias, templates oficiais e exemplos preenchidos.

## Onde comecar
- Guia rapido: `factory-workflow/docs/quickstart.md`
- Workflow completo: `factory-workflow/docs/workflow.md`

## Templates e exemplos
- Templates oficiais: `factory-workflow/docs/templates/README.md`
- Exemplos preenchidos: `factory-workflow/docs/examples/README.md`

## Relacao entre docs.md e context/*
- `docs.md` e o documento mestre humano.
- O conteudo do `docs.md` deve ser distribuido para os arquivos operacionais em `factory-workflow/context/*`.
- Bots operam sempre sobre `factory-workflow/context/*`, nao sobre o `docs.md`.

## Convencoes e regras
- Nao inventar requisitos.
- Se faltar decisao, registrar em `factory-workflow/context/core/gaps.md`.
- Templates sao canonicos e devem ser reutilizados.
