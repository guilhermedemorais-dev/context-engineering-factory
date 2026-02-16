# Factory Sources (read as needed)

## Context and policy
- `factory-workflow/context/INDEX.md` — mandatory reading order and GAP rule.
- `factory-workflow/policies/policy-engine.md` — no write without approved plan, no deploy without QA, no destructive action without confirmation.

## Workflow and templates
- `factory-workflow/docs.fabrication/workflow.md` — RPI workflow, plan approval block, DoR/DoD.
- `factory-workflow/docs.fabrication/quickstart.md` — runtime setup and work folder conventions.
- `factory-workflow/docs.fabrication/templates/plan.template.md` — plan template.

## Runtime and bots
- `factory-workflow/bots/runtime/README.md` — CLI runtime, autopilot, outputs.
- `factory-workflow/bots/context-sync.md` — PRD ingestion rules and mapping to context.
- `factory-workflow/bots/README.md` — bot rules and context order.

## Skill resolver and agents
- `factory-workflow/skill-resolver/README.md` — gap detection and queue generation.
- `factory-workflow/docs.fabrication/architecture/skill-resolution.md` — category mapping rules.
- `factory-workflow/agents/registry.yaml` — agent stages and triggers.

## PRD intake (docs.prd)
- `docs.prd/README.md` — how PRDs flow into context.
- `docs.prd/prd.md`, `docs.prd/tech.md`, `docs.prd/ui-ux.md` — human PRD inputs.

## QA and gates (if needed)
- `factory-workflow/cicd/gates.md` — gate requirements.
- `factory-workflow/tests/reports/**` — QA evidence location.
