# Visão Geral do Sistema — DHV Audit AI

## 1. Propósito

Construir a **melhor plataforma de auditoria inteligente** do mercado brasileiro — um sistema que não apenas detecta problemas, mas **prescreve ações concretas** para:

- **Reduzir custos** (frete, folha, compras, tributos, financeiro)
- **Padronizar processos** (checklists, políticas, workflows)
- **Capturar valor** (economia identificada → economia realizada)
- **Operar uma firma de auditoria** de ponta a ponta

---

## 2. Princípios de Engenharia

| Princípio | Aplicação |
|---|---|
| **Clean Architecture** | Domínio isolado; dependências apontam para o centro |
| **Domain-Driven Design** | Bounded contexts por domínio de auditoria |
| **Modular Monolith** | Módulos independentes, deploy único inicialmente |
| **Event-Driven** | Comunicação assíncrona entre módulos via eventos |
| **Multi-Tenant First** | Isolamento rigoroso desde o dia 1 |
| **Evidence-Based AI** | Toda conclusão da IA exige evidência rastreável |
| **Human-in-the-Loop** | Consultor valida achados críticos antes da entrega |
| **API-First** | Backend expõe API REST; frontends são consumidores |

---

## 3. Camadas do Sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CAMADA DE APRESENTAÇÃO                      │
│  Admin Panel │ Client Portal │ Consultant Workspace │ Mobile (PWA)  │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ HTTPS / REST / WebSocket
┌───────────────────────────────▼─────────────────────────────────────┐
│                         CAMADA DE INTERFACES                        │
│  FastAPI Routers │ Webhooks │ GraphQL (futuro) │ SSE / WS           │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│                         CAMADA DE APLICAÇÃO                         │
│  Use Cases │ Orquestradores │ DTOs │ Event Handlers │ Schedulers    │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│                           CAMADA DE DOMÍNIO                         │
│  Entidades │ Value Objects │ Domain Services │ Repository Ports     │
│  ┌─────────┬─────────┬──────────┬───────────┬──────────┐          │
│  │ Audit   │ Company │ Contract │ Finding   │ Document  │          │
│  │ Cycle   │ Tenant  │ Engagement│ Action    │ Evidence  │          │
│  └─────────┴─────────┴──────────┴───────────┴──────────┘          │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│                        CAMADA DE INFRAESTRUTURA                     │
│  PostgreSQL │ Redis │ S3 │ LLM/OCR │ Email │ Queue │ PDF Engine    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Bounded Contexts (Domínios)

| Contexto | Responsabilidade |
|---|---|
| **Platform** | Tenants, usuários, RBAC, configurações globais |
| **Commercial** | CRM, propostas, contratos, faturamento |
| **Engagement** | Ciclos de auditoria, escopo, cronograma, equipe |
| **Ingestion** | Upload, conectores, e-mail, webhooks |
| **Extraction** | OCR, parsing XML/SPED, normalização |
| **Analysis** | Regras, IA, benchmark, cruzamento de dados |
| **Delivery** | Dashboard, relatórios, plano de ação, follow-up |
| **Governance** | Workpapers, EQCR, trilha de auditoria, LGPD |

---

## 5. Output Final do Sistema (Entregável ao Cliente)

Para cada achado, a plataforma entrega um **Actionable Finding**:

```json
{
  "finding_id": "f-2026-00142",
  "title": "Cobrança de frete acima da tabela contratada",
  "severity": "high",
  "domain": "logistics",
  "financial_impact": 47850.00,
  "confidence_score": 0.96,
  "evidence": [
    { "type": "invoice", "document_id": "doc-8821", "page": 2, "field": "valor_frete" },
    { "type": "contract", "document_id": "doc-1103", "clause": "4.2", "rate_table": "tabela_2025" }
  ],
  "root_cause": "Transportadora XYZ aplicou tabela 2024 em faturas de jan/2026",
  "recommended_actions": [
    {
      "action": "Contestar faturas 8821, 8822, 8823 junto à transportadora XYZ",
      "owner": "Gestor de Logística",
      "effort": "low",
      "deadline_days": 15,
      "expected_recovery": 47850.00,
      "template": "contestacao_frete_v2.docx"
    },
    {
      "action": "Implementar validação automática tabela × fatura no processo de conferência",
      "owner": "Controller",
      "effort": "medium",
      "deadline_days": 30,
      "process_standard": "PROC-LOG-012"
    }
  ],
  "cross_references": [
    { "domain": "financial", "finding_id": "f-2026-00098", "relation": "pagamento_duplicado_mesmo_frete" }
  ],
  "status": "pending_validation",
  "validated_by": null
}
```

---

## 6. Personas e Interfaces

| Persona | Interface | Principais Ações |
|---|---|---|
| **Super Admin DHV** | Admin Panel | Chaves de provedores, tenants, billing, config global |
| **Admin DHV** | Admin Panel + Workspace | Empresas, contratos, equipes, relatórios globais |
| **Consultor DHV** | Consultant Workspace | Executar auditoria, validar achados, workpapers |
| **Revisor de Qualidade** | Consultant Workspace | EQCR, aprovar entregas |
| **Gestor Cliente** | Client Portal | Upload docs, ver achados, aprovar plano de ação |
| **Operacional Cliente** | Client Portal | Responder pendências, anexar evidências |
| **Financeiro Cliente** | Client Portal | Ver impacto financeiro, acompanhar recuperação |

---

## 7. Métricas de Sucesso da Plataforma

| Métrica | Meta |
|---|---|
| Cobertura documental por ciclo | ≥ 95% dos documentos do escopo |
| Precisão de achados (pós-validação) | ≥ 90% confirmados pelo consultor |
| Tempo ciclo auditoria (vs manual) | Redução ≥ 70% |
| Economia identificada / faturamento cliente | Ratio documentado por engagement |
| Economia capturada / identificada | ≥ 60% em 90 dias pós-entrega |
| NPS clientes | ≥ 50 |
| Uptime API | ≥ 99.9% |
