# Índice de Módulos — DHV Audit AI Platform

**Total:** 28 módulos funcionais organizados em 4 camadas + 6 domínios de auditoria.

---

## Camada 1 — Pipeline Core (M1–M6)

| # | Módulo | Descrição | Doc |
|---|---|---|---|
| M1 | Ingestão de Documentos | Upload, email, conectores, Open Banking | [module-01-to-06.md](./module-01-to-06.md) |
| M2 | OCR & Extração | OCR + LLM Vision, parsers XML/SPED/OFX | [module-01-to-06.md](./module-01-to-06.md) |
| M3 | Classificação & Padronização | Taxonomia DHV, dedup, entity resolution | [module-01-to-06.md](./module-01-to-06.md) |
| M4 | Motor de Análise & Anomalias | Regras + IA, severidade, impacto financeiro | [module-01-to-06.md](./module-01-to-06.md) |
| M5 | Benchmarking Setorial | Índice DHV, comparação por setor/região | [module-01-to-06.md](./module-01-to-06.md) |
| M6 | Recomendações & Plano de Ação | Prescrição de ações, templates, ROI | [module-01-to-06.md](./module-01-to-06.md) |

## Camada 2 — Entrega & Governança (M7–M11)

| # | Módulo | Descrição | Doc |
|---|---|---|---|
| M7 | Dashboard Executivo & KPIs | KPIs, economia identificada vs capturada | [module-07-to-11.md](./module-07-to-11.md) |
| M8 | Relatórios Automáticos | PDF, PPTX, XLSX, agendamento | [module-07-to-11.md](./module-07-to-11.md) |
| M9 | Assistente IA (Chat/RAG) | Chat contextual com evidências | [module-07-to-11.md](./module-07-to-11.md) |
| M10 | Usuários & Multi-tenant | RBAC, perfis, isolamento | [module-07-to-11.md](./module-07-to-11.md) |
| M11 | Segurança & LGPD | Criptografia, audit trail, retenção | [module-07-to-11.md](./module-07-to-11.md) |

## Camada 3 — Operação da Firma (M12–M17)

| # | Módulo | Descrição | Doc |
|---|---|---|---|
| M12 | CRM & Gestão de Engajamentos | Clientes, propostas, escopo, cronograma | [module-12-to-17-operacao-firma.md](./module-12-to-17-operacao-firma.md) |
| M13 | Precificação & Faturamento | Pricing, faturas, margem por cliente | [module-12-to-17-operacao-firma.md](./module-12-to-17-operacao-firma.md) |
| M14 | Workflow de Auditoria | Kanban, filas, atribuições, prazos | [module-12-to-17-operacao-firma.md](./module-12-to-17-operacao-firma.md) |
| M15 | Workpapers & Evidências | Pasta de trabalho digital, cadeia de evidências | [module-12-to-17-operacao-firma.md](./module-12-to-17-operacao-firma.md) |
| M16 | Revisão de Qualidade (EQCR) | Segunda revisão, aprovação 4 olhos | [module-12-to-17-operacao-firma.md](./module-12-to-17-operacao-firma.md) |
| M17 | Follow-up & Remediação | Acompanhamento de ações, captura de valor | [module-12-to-17-operacao-firma.md](./module-12-to-17-operacao-firma.md) |

## Camada 4 — Inteligência Avançada (M18–M23)

| # | Módulo | Descrição | Doc |
|---|---|---|---|
| M18 | Motor de Regras & Compliance | Biblioteca de regras versionadas (SPED, ICMS, ANTT) | [module-18-to-23-inteligencia.md](./module-18-to-23-inteligencia.md) |
| M19 | Amostragem & Materialidade | Seleção estatística, extrapolação de erro | [module-18-to-23-inteligencia.md](./module-18-to-23-inteligencia.md) |
| M20 | Continuous Auditing | Monitoramento contínuo, alertas em tempo real | [module-18-to-23-inteligencia.md](./module-18-to-23-inteligencia.md) |
| M21 | Fraud Detection & Forensics | Benford, grafos, padrões de fraude | [module-18-to-23-inteligencia.md](./module-18-to-23-inteligencia.md) |
| M22 | Data Analytics Engine | Scripts analíticos, joins, pivots, outliers | [module-18-to-23-inteligencia.md](./module-18-to-23-inteligencia.md) |
| M23 | AI Governance & Feedback Loop | Consultor valida → IA aprende, versionamento | [module-18-to-23-inteligencia.md](./module-18-to-23-inteligencia.md) |

## Camada 5 — Plataforma & Escala (M24–M28)

| # | Módulo | Descrição | Doc |
|---|---|---|---|
| M24 | Portal do Cliente (Self-Service) | Upload, achados, plano de ação, aprovações | [module-24-to-28-plataforma.md](./module-24-to-28-plataforma.md) |
| M25 | Integration Hub (iPaaS) | Conectores ERP, bancos, SEFAZ, eSocial | [module-24-to-28-plataforma.md](./module-24-to-28-plataforma.md) |
| M26 | Knowledge Base & Metodologia | Playbooks, onboarding consultores | [module-24-to-28-plataforma.md](./module-24-to-28-plataforma.md) |
| M27 | Marketplace de Regras & Plugins | Regras por vertical, extensões de terceiros | [module-24-to-28-plataforma.md](./module-24-to-28-plataforma.md) |
| M28 | White-label & Multi-marca | Revenda para outras consultorias | [module-24-to-28-plataforma.md](./module-24-to-28-plataforma.md) |

---

## Domínios de Auditoria (Plugins)

Cada domínio é um **plugin** registrado no Analysis Engine (M4) com regras, agente IA, benchmarks e cruzamentos próprios.

| Domínio | Escopo | Doc |
|---|---|---|
| **Logistics** | Frete, CT-e, rotas, peso cubado, SLAs | [domain-logistics.md](./domains/domain-logistics.md) |
| **HR** | Folha, eSocial, encargos, ponto, rescisões | [domain-hr.md](./domains/domain-hr.md) |
| **Procurement** | Compras, cotações, contratos, split NF | [domain-procurement.md](./domains/domain-procurement.md) |
| **Financial** | AP/AR, extratos, conciliação, fluxo de caixa | [domain-financial.md](./domains/domain-financial.md) |
| **Fiscal/Tax** | SPED, NF-e, créditos ICMS/PIS/COFINS, retenções | [domain-fiscal-tax.md](./domains/domain-fiscal-tax.md) |
| **Fleet** | Combustível, manutenção, telemetria, multas | [domain-fleet.md](./domains/domain-fleet.md) |

---

## Módulo Transversal: Contratos & Documentos Legais

| Escopo | Doc |
|---|---|
| Contratos de auditoria, NDAs, propostas, termos de contestação | [legal-documents.md](../contracts/legal-documents.md) |

---

## Mapa de Dependências

```
M10 Platform ──────────────────────────────────────────────┐
    │                                                       │
    ├── M12 CRM ── M13 Billing                              │
    │       │                                               │
    │       └── M14 Workflow ── M15 Workpapers ── M16 EQCR  │
    │               │                                       │
    │               └── Engagement (Audit Cycle)             │
    │                       │                               │
    │                       ├── M1 Ingestion                │
    │                       │     └── M2 Extraction         │
    │                       │           └── M3 Classification│
    │                       │                 └── M4 Analysis ◄── Domains
    │                       │                       ├── M5 Benchmark
    │                       │                       ├── M18 Rules
    │                       │                       ├── M21 Fraud
    │                       │                       └── M22 Analytics
    │                       │                             │
    │                       └── M6 Action Plan ── M17 Follow-up
    │                               │
    │                               ├── M7 Dashboard
    │                               ├── M8 Reports
    │                               └── M9 Chat AI
    │                                                       │
    ├── M24 Client Portal                                   │
    ├── M25 Integrations                                    │
    └── M11 Security ◄────────────────────────────────────┘
```
