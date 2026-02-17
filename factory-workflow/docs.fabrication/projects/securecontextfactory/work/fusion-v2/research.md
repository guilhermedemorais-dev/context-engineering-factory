# Research — SecureContextFactory (fusion-v2)

## Objetivo
Evoluir o SecureContextFactory para o v0.2 (fusion-v2) focando em:
- Wizard "aios-core-like" (doctor/env detect/templates)
- Hooks multi-IDE (instalador de configuracoes no workspace)
- Registry + templates de squads (base para execucao colaborativa)

## Contexto (fonte de verdade)
- `factory-workflow/context/INDEX.md` (ordem obrigatoria)
- `factory-workflow/policies/policy-engine.md`
- `factory-workflow/cicd/gates.md`
- `factory-workflow/context/tooling/*`

## Estado atual
Ja existe:
- CLI `securecontextfactory` com init/install/autopilot wrappers/audit/gap.
- Runtime/bots com autopilot e fila.
- Contexto core e tooling policies preenchidos.

## Falhas/limites atuais (v0.1)
- Falta comando de "doctor" para validar ambiente/config e orientar correcoes.
- Falta "hook installer" para VSCode/Cursor/agent files no workspace (config como codigo).
- Falta registry de squads com templates versionados e comandos para criar/listar.

## Diretrizes de design (v0.2)
- Python-first, sem Node obrigatorio.
- Hooks devem ser idempotentes (nao quebrar config existente).
- Doctor deve ser acionavel: reportar OK/WARN/ERROR e sugerir proximo passo, sem vazar secrets.
- Squad registry deve ser simples (YAML) e versionavel.

