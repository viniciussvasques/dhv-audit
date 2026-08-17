# Estrutura de Pastas — Monorepo Profissional

## Visão Geral

O projeto adota um **monorepo** com backend Python (FastAPI) e frontend TypeScript (Next.js), organizado por bounded contexts modulares.

```
dhv-audit-ai/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Lint, typecheck, testes
│       ├── cd-staging.yml            # Deploy staging
│       └── cd-production.yml         # Deploy produção
│
├── docs/                             # Documentação técnica (este diretório)
│   ├── README.md
│   ├── master-plan.md
│   ├── architecture/
│   ├── adr/
│   ├── modules/
│   ├── api/
│   ├── ui/
│   ├── database/
│   ├── contracts/
│   └── security/
│
├── backend/                          # API Python (FastAPI)
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── alembic/                      # Migrações de banco
│   │   ├── versions/
│   │   └── env.py
│   ├── src/
│   │   ├── main.py                   # Entry point FastAPI
│   │   ├── config/                   # Settings (Pydantic Settings)
│   │   │   ├── settings.py
│   │   │   └── dependencies.py       # DI container
│   │   │
│   │   ├── shared/                   # Kernel compartilhado
│   │   │   ├── domain/
│   │   │   │   ├── base_entity.py
│   │   │   │   ├── value_objects.py  # Money, CNPJ, Email, Period
│   │   │   │   └── events.py
│   │   │   ├── application/
│   │   │   │   ├── unit_of_work.py
│   │   │   │   └── event_bus.py
│   │   │   └── infrastructure/
│   │   │       ├── database/
│   │   │       │   ├── session.py
│   │   │       │   └── base_model.py
│   │   │       ├── queue/
│   │   │       ├── storage/
│   │   │       └── logging/
│   │   │
│   │   ├── modules/                  # Módulos de negócio (bounded contexts)
│   │   │   │
│   │   │   ├── platform/             # M10 — Tenants, users, RBAC
│   │   │   │   ├── domain/
│   │   │   │   ├── application/
│   │   │   │   ├── infrastructure/
│   │   │   │   └── interfaces/
│   │   │   │       └── routes.py
│   │   │   │
│   │   │   ├── commercial/           # M12, M13 — CRM, billing
│   │   │   ├── engagement/           # Ciclos, escopo, cronograma
│   │   │   ├── ingestion/            # M1 — Upload, conectores
│   │   │   ├── extraction/           # M2 — OCR, parsing
│   │   │   ├── classification/       # M3 — Taxonomia, dedup
│   │   │   ├── analysis/             # M4, M5, M18-M23 — Motor IA
│   │   │   ├── delivery/             # M6-M9 — Dashboard, reports, chat
│   │   │   ├── governance/           # M11, M15, M16 — Workpapers, EQCR
│   │   │   ├── workflow/             # M14 — Tarefas, filas
│   │   │   ├── followup/             # M17 — Remediação, captura valor
│   │   │   ├── contracts/            # Contratos, NDAs, propostas
│   │   │   ├── integrations/         # M25 — ERP, bancos, SEFAZ
│   │   │   │
│   │   │   └── audit_domains/        # Domínios verticais de auditoria
│   │   │       ├── logistics/
│   │   │       ├── hr/
│   │   │       ├── procurement/
│   │   │       ├── financial/
│   │   │       ├── fiscal/
│   │   │       └── fleet/
│   │   │
│   │   └── interfaces/               # Adaptadores HTTP globais
│   │       ├── api/
│   │       │   ├── v1/
│   │       │   │   ├── router.py     # Agregador de rotas
│   │       │   │   ├── admin/        # Rotas admin
│   │       │   │   ├── client/       # Rotas portal cliente
│   │       │   │   └── consultant/   # Rotas workspace consultor
│   │       │   └── middleware/
│   │       │       ├── auth.py
│   │       │       ├── tenant.py
│   │       │       └── audit_trail.py
│   │       └── webhooks/
│   │
│   └── tests/
│       ├── unit/
│       ├── integration/
│       ├── e2e/
│       └── fixtures/
│
├── frontend/                         # Next.js 14+ (App Router)
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.ts
│   ├── public/
│   └── src/
│       ├── app/                      # App Router (Next.js)
│       │   ├── (admin)/              # Painel Admin DHV
│       │   │   ├── layout.tsx
│       │   │   ├── dashboard/
│       │   │   ├── tenants/
│       │   │   ├── companies/
│       │   │   ├── users/
│       │   │   ├── providers/        # Chaves LLM/OCR
│       │   │   ├── engagements/
│       │   │   ├── contracts/
│       │   │   ├── billing/
│       │   │   └── settings/
│       │   │
│       │   ├── (client)/             # Portal do Cliente
│       │   │   ├── layout.tsx
│       │   │   ├── dashboard/
│       │   │   ├── documents/
│       │   │   ├── findings/
│       │   │   ├── action-plans/
│       │   │   ├── uploads/
│       │   │   └── reports/
│       │   │
│       │   ├── (consultant)/           # Workspace Consultor
│       │   │   ├── layout.tsx
│       │   │   ├── inbox/              # Fila de trabalho
│       │   │   ├── audits/
│       │   │   ├── review-queue/       # Human-in-the-loop
│       │   │   ├── workpapers/
│       │   │   ├── eqcr/
│       │   │   └── cross-analysis/
│       │   │
│       │   ├── (auth)/
│       │   │   ├── login/
│       │   │   └── forgot-password/
│       │   │
│       │   └── layout.tsx
│       │
│       ├── components/
│       │   ├── ui/                     # Design system (shadcn/ui)
│       │   ├── forms/
│       │   ├── charts/
│       │   ├── documents/
│       │   └── audit/
│       │
│       ├── lib/
│       │   ├── api/                    # Client HTTP (fetch/axios)
│       │   ├── auth/
│       │   ├── hooks/
│       │   └── utils/
│       │
│       └── types/                      # TypeScript types (sync com API)
│
├── infra/                              # Infraestrutura como código
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   ├── Dockerfile.frontend
│   │   └── docker-compose.yml
│   ├── terraform/                      # (futuro) AWS/GCP
│   └── k8s/                            # (futuro) Kubernetes
│
├── scripts/
│   ├── setup-dev.sh
│   ├── seed-db.py
│   └── generate-openapi.sh
│
├── templates/                          # Templates de documentos legais
│   ├── contracts/
│   │   ├── audit_engagement.docx
│   │   ├── nda_mutual.docx
│   │   └── proposal_commercial.docx
│   └── reports/
│       ├── executive_summary.pptx
│       └── technical_audit.xlsx
│
├── .env.example
├── Makefile
├── ARCHITECTURE.md
├── CHANGELOG.md
└── README.md
```

---

## Convenções por Módulo Backend

Cada módulo em `backend/src/modules/{nome}/` segue a estrutura:

```
modules/{nome}/
├── domain/
│   ├── entities.py          # Entidades de domínio
│   ├── value_objects.py     # VOs específicos do módulo
│   ├── repositories.py      # Interfaces (ports)
│   ├── services.py          # Domain services
│   └── events.py            # Domain events
├── application/
│   ├── use_cases/           # Um arquivo por use case
│   ├── dto.py                 # Input/Output DTOs
│   └── handlers.py            # Event handlers
├── infrastructure/
│   ├── repositories.py        # Implementações SQLAlchemy
│   ├── models.py              # ORM models
│   └── adapters/              # Integrações externas
└── interfaces/
    └── routes.py              # FastAPI router do módulo
```

---

## Regras de Dependência

```
interfaces → application → domain ← infrastructure
                ↓
              shared
```

- **domain/** não importa nada de fora do domínio
- **application/** importa apenas domain e shared
- **infrastructure/** implementa ports definidos em domain
- **interfaces/** orquestra use cases via DI
- Módulos se comunicam via **domain events**, nunca importação direta de infra

---

## Migração do Código Atual

O código existente em `src/` na raiz será migrado para `backend/src/` seguindo esta estrutura. Durante a transição, ambos coexistem com alias no `pyproject.toml`.
