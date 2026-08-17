# 0004: Estratégia de Monólito Modular

**Status**: Aceito  
**Data**: 2026-08-16

---

## Contexto

A plataforma possui 28+ módulos funcionais que precisam ser desenvolvidos incrementalmente por uma equipe pequena inicial. Precisamos de uma arquitetura que permita modularidade sem a complexidade operacional de microserviços prematura.

---

## Decisão

Adotar **Modular Monolith** com comunicação inter-módulos via **Domain Events** (in-process initially, message broker later).

### Princípios

1. **Cada módulo é um bounded context** com domain/application/infrastructure/interfaces próprios
2. **Módulos NÃO importam infraestrutura de outros módulos** — apenas domain events
3. **Deploy único** (um processo API + um processo Worker) na Fase 1
4. **Extração para microserviço** é possível quando um módulo justificar (volume, escala, time)

### Comunicação Inter-Módulos

```
Fase 1 (Monólito):
  Module A → EventBus (in-process) → Module B

Fase 2 (Escala):
  Module A → Redis Pub/Sub → Module B

Fase 3 (Microserviços):
  Module A → RabbitMQ/SQS → Module B (serviço separado)
```

### Mapa de Módulos e Dependências

```
Platform (base — todos dependem)
  ├── Commercial
  ├── Engagement
  │     ├── Ingestion
  │     │     └── Extraction
  │     │           └── Classification
  │     │                 └── Analysis ← Audit Domains
  │     │                       └── Delivery
  │     ├── Workflow
  │     ├── Governance
  │     └── Follow-up
  ├── Contracts
  └── Integrations
```

### Regras de Acoplamento

| Permitido | Proibido |
|---|---|
| Módulo A publica evento, Módulo B escuta | Módulo A importa repository de Módulo B |
| Shared kernel (value objects comuns) | Módulo A chama use case de Módulo B diretamente |
| API Gateway agrega rotas de todos módulos | Módulo A acessa tabela de Módulo B via SQL |
| Domain events tipados em shared/events | Lógica de negócio de B dentro de A |

### Plugin Architecture (Audit Domains)

Domínios de auditoria (Logistics, HR, Procurement, etc.) são **plugins** registrados no Analysis Engine:

```python
class AuditDomainPlugin(Protocol):
    domain_id: str
    def get_rules(self) -> list[Rule]: ...
    def get_ai_agent(self) -> AIAgent: ...
    def get_cross_references(self) -> list[CrossReferenceRule]: ...
    def get_benchmarks(self) -> list[BenchmarkMetric]: ...
```

Novos domínios são adicionados sem modificar o core.

---

## Consequências

### Positivas
- Desenvolvimento rápido com deploy simples
- Refactoring seguro (testes abrangem tudo)
- Transações ACID entre módulos (sem saga complexity)
- Extração gradual para microserviços quando necessário

### Negativas
- Disciplina necessária para não acoplar módulos
- Um bug pode afetar toda a aplicação
- Scaling horizontal requer replicar tudo

### Mitigação
- Lint rules para detectar imports cross-module proibidos
- Testes de integração por módulo
- Feature flags para ativar/desativar módulos por tenant
