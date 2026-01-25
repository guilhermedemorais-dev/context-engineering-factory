# Policy Engine Rules

Mandatory rules:
1) No write actions without an approved plan.
2) No deploy actions without QA engine evidence.
3) No decisions without recorded justification.
4) No destructive actions without human confirmation.

Enforcement points:
- Before any agent write operation.
- Before execution-engine applies changes.
- Before distribution-engine publishes artifacts.
- Before any delete or reset operation.

Artifacts:
- Decision records: factory-workflow/governance/adr/**
- QA evidence: factory-workflow/tests/reports/**
- Plan approvals: factory-workflow/docs/projects/**/work/**/plan.md
