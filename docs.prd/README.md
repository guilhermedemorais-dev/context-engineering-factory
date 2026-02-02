# Docs.example (PRDs para iniciar um projeto)

Copie esta pasta para a **raiz do seu projeto** e renomeie para `docs/`:

```bash
cp -R Docs.example docs
```

Depois, preencha os arquivos:
- `docs/prd.md`
- `docs/ui-ux.md`
- `docs/tech.md`

## Como a Factory usa isso
O bot `context-sync` lê `./docs/*.md` e distribui o conteúdo para a base de contexto em:
- `factory-workflow/context/core/*`
- `factory-workflow/context/ui/*`
- `factory-workflow/context/quality/*`
- `factory-workflow/context/tooling/*`

Regra: se faltar informação, ele registra GAP em `factory-workflow/context/core/gaps.md` e **para**.
