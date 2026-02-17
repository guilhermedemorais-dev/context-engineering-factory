# Principles (Prioridades e Trade-offs)

## Prioridades
1) **Seguranca e auditabilidade > autonomia**
2) **Explicito > implicito** (nada de suposicoes silenciosas)
3) **Stop-and-suggest > seguir com duvida**
4) **Reuso > reinvencao** (MCP/registry/design-system antes de criar)
5) **Reprodutibilidade > improviso**

## Trade-offs aceitos
- Mais friccao inicial (gates/aprovacao) para reduzir retrabalho, incidentes e drift.
- Dependencias opcionais (LangGraph/CrewAI) para tracao rapida; engines nativas podem ser backlog.
- Preferir "falhar com motivo" (BLOCKED) a "continuar errado".

## Anti-principios (proibidos)
- "Burlar gates para ganhar tempo"
- "Editar contexto para passar"
- "Evidencia falsa"
- "Persistir secrets/PII no repo"

