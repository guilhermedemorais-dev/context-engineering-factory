---
name: factory-dev-workflow
description: Apply the SecureContextFactory (Context Engineering + Spec-driven Delivery) workflow for software development in this repo. Use when planning, researching, or implementing features with RPI (Research to Plan to Implement), when creating or using PRDs in `docs.prd/`, when enforcing context loading from `factory-workflow/context/INDEX.md`, or when policy/gate compliance (plan approval, QA evidence, gap tracking) is required.
---

# SecureContextFactory Dev Workflow

## Overview
Enforce the SecureContextFactory RPI workflow (Research → Plan → Implement), governance, and QA gates. Prefer the runtime/autopilot for automated delivery and the skill-resolver for routing and gap detection.
Deliver production-ready software only after QA evidence and gates are satisfied. Avoid mockups unless explicitly requested.

## Workflow (RPI + Gates)

### 1. Load context (mandatory)
- Read `factory-workflow/context/INDEX.md` and then each file listed there in order.
- If any requirement is missing or conflicting, record a GAP in `factory-workflow/context/core/gaps.md` and stop.

### 2. PRD intake (docs.prd)
- Use `docs.prd/prd.md`, `docs.prd/tech.md`, and `docs.prd/ui-ux.md` as the human PRD source.
- If running the runtime, copy `docs.prd/` to `docs/` because `context-sync` reads `docs/*.md` at repo root.
- Prefer PRD files over chat input. Only use chat input when the user explicitly cannot provide files.
- If these docs are missing or incomplete, request input and/or record a GAP before planning.
- Summarize relevant parts into the Research/Plan artifacts.

### 3. Research
- Collect evidence and references; do not assume.
- Store evidence and links in `research.md` under the feature work folder.

### 4. Plan
- Create `plan.md` using `factory-workflow/docs.fabrication/templates/plan.template.md`.
- Include scope, steps, test plan, acceptance criteria, risks, and evidence.
- Require explicit plan approval before any write.

### 5. Implement
- Only after plan approval (policy engine).
- Keep changes within the approved scope and target files.
- Update docs and decisions when needed.

### 6. QA + Gates
- Run tests listed in the plan; capture evidence where applicable.
- Do not deploy or perform destructive actions without required evidence and human approval.
- Do not claim “production-ready” without QA evidence and gates satisfied.

### 7. Handoff / context control (as needed)
- If the context is large or a session ends, write `progress.md` in the work folder.

## Runtime (CLI autopilot)

Prefer the runtime when you need the full automated pipeline.

1. Run `context-sync` to distribute `docs/*.md` into `factory-workflow/context/*`.
2. Run `autopilot-start` to generate a DRAFT plan and review it.
3. Approve the plan in `plan.md`.
4. Run `autopilot-build` to enqueue dev and QA bots.
5. Respect the dev bot path constraint: write only under `/apps/<project>`.

### Autopilot commands (examples)
```bash
python factory-workflow/bots/runtime/cli.py autopilot-start \
  --workspace "." \
  --feature "current"
```

```bash
python factory-workflow/bots/runtime/cli.py autopilot-build \
  --workspace "." \
  --feature "current" \
  --project "/apps/<project>" \
  --with-e2e
```

SecureContextFactory CLI wrappers:
```bash
securecontextfactory autopilot-start --workspace "." --feature "current"
securecontextfactory autopilot-build --workspace "." --feature "current" --project "/apps/<project>" --with-e2e
```

### Context-sync and planner (manual runtime)
```bash
cp -R docs.prd docs
python factory-workflow/bots/runtime/cli.py run context-sync \
  --task "Distribuir PRDs de ./docs para factory-workflow/context" \
  --workspace "."
```

```bash
python factory-workflow/bots/runtime/cli.py run planner \
  --task "Research + Plan + Queue para feature atual" \
  --workspace "."
```

## Manual vs Autopilot

- Use **Autopilot** for standard feature delivery with strict RPI and QA sequencing.
- Use **Manual** when the task is exploratory, non-standard, or requires custom sequencing.
- Autopilot example: feature delivery with plan approval and QA sequence enforced.
- Manual example: spike/POC, migration prep, or when you must adjust the bot order.

## Quick Checks (before implement)

- Confirm `factory-workflow/context/core/gaps.md` has no blocking GAPs.
- Confirm `plan.md` has `Status: APPROVED` and reviewer/date filled.
- Confirm target paths match the plan (dev bot writes only under `/apps/<project>`).
- Confirm QA evidence path is known: `factory-workflow/tests/reports/**`.
- Optional: run `securecontextfactory doctor` to validate environment and governance quickly.

## Recommended Standard Flow (Factory)

1. Prepare PRDs in `docs.prd/` and copy to `docs/` if using runtime.
2. Run `context-sync`.
3. Run `autopilot-start` to generate the DRAFT plan.
4. Approve the plan at the top of `plan.md`.
5. Run `autopilot-build` to enqueue dev and QA bots.
6. Review QA evidence in `factory-workflow/tests/reports/**`.
7. Use `review` output for release readiness.

Autopilot outputs:
- Plan: `factory-workflow/docs/autopilot/<feature>/plan.md`
- Release checklist: `factory-workflow/docs/autopilot/<feature>/release.md`

### Autopilot (concrete example)
```bash
python factory-workflow/bots/runtime/cli.py autopilot-start \
  --workspace "." \
  --feature "payments-v1"
```

```bash
python factory-workflow/bots/runtime/cli.py autopilot-build \
  --workspace "." \
  --feature "payments-v1" \
  --project "/apps/buypeer" \
  --with-e2e
```

## Bots involved (runtime pipeline)

- `orchestrator`, `planner`, `dev`
- `qa-unit`, `qa-integration`, `qa-e2e`, `qa-security`
- `review`

## Skill resolver + agents

Use the skill-resolver when you need automated routing or gap detection.

1. Ensure context and work artifacts exist.
2. Let the resolver build the queue based on policies and categories.
3. Follow the agent registry for stage ownership.

Outputs:
- `factory-workflow/skill-resolver/queue.yaml`
- `factory-workflow/skill-resolver/resolver.yaml`

## Artifact locations

- Feature work folder: `factory-workflow/docs.fabrication/projects/<project>/work/<feature>/`
- Canonical files: `research.md`, `plan.md`, `progress.md`, `decisions.md`
- Gaps: `factory-workflow/context/core/gaps.md`
- Autopilot outputs: `factory-workflow/docs/autopilot/<feature>/` (when using runtime)

## Context locality (important)

The skill can be global, but the context is always **per project**.
`context-sync` writes to `factory-workflow/context/*` inside the current project workspace.

## Path notes

Some docs in this repo still reference `factory-workflow/docs/*`. The actual folder here is `factory-workflow/docs.fabrication/`. If a referenced path does not exist, map it to `docs.fabrication` and record a GAP if ambiguity remains.

## References

Read `references/factory-sources.md` for the canonical docs to consult and when to use them.
