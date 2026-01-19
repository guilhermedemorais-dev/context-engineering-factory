# Context Index

## Objective
Define the mandatory read order and sources of truth for context.

## Mandatory read order
1. factory-workflow/context/core/vision.md
2. factory-workflow/context/core/scope.md
3. factory-workflow/context/core/requirements.md
4. factory-workflow/context/core/business-rules.md
5. factory-workflow/context/core/data.md
6. factory-workflow/context/quality/definition-of-done.md
7. factory-workflow/context/tooling/mcp-policy.md
8. factory-workflow/context/ui/component-policy.md
9. factory-workflow/context/codex/implementation-rules.md

## Rules
- Nothing may be assumed outside this context.
- If anything is undefined or conflicting, log it in `factory-workflow/context/core/gaps.md` and stop implementation.
- Context overrides code and runtime behavior.

## How to use
- Read in order before planning or implementation.
- Re-read after any change to the context sources.
