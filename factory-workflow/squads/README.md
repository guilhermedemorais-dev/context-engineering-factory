# Squads (templates)

Esta pasta define squads versionados para execucao colaborativa (CrewAI opcional), sempre sob governanca do SecureContextFactory.

Formato (YAML):
```yaml
name: default
description: ...
manager:
  role: "..."
  goal: "..."
  backstory: "..."
expected_output: "..."
process: sequential   # ou hierarchical (se suportado)
```

Comandos:
```bash
securecontextfactory squad list
securecontextfactory squad init default
securecontextfactory run-squad default --task "..."
```

