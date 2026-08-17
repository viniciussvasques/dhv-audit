# Módulos M12–M17 — Operação da Firma de Auditoria

---

## M12 — CRM & Gestão de Engajamentos

### Objetivo
Gerenciar o ciclo comercial e operacional completo: desde o cadastro da empresa cliente até a execução do engagement de auditoria.

### Entidades de Domínio

```python
@dataclass
class Company:
    id: str
    tenant_id: str
    cnpj: str
    razao_social: str
    nome_fantasia: str
    type: CompanyType  # matriz | filial
    parent_id: Optional[str]
    sector: str  # varejo, farma, industria, ecommerce
    branches: List["Company"]
    cost_centers: List[CostCenter]
    bank_accounts: List[BankAccount]

@dataclass
class Engagement:
    id: str
    tenant_id: str
    company_id: str
    title: str
    status: EngagementStatus  # draft, active, in_review, delivered, closed
    scope: EngagementScope
    team: List[TeamMember]
    schedule: Schedule
    modules_active: List[str]  # logistics, hr, procurement, ...
    created_at: datetime

@dataclass
class EngagementScope:
    domains: List[str]           # módulos de auditoria ativos
    period_start: date
    period_end: date
    companies: List[str]         # CNPJs no escopo
    document_checklist: List[DocumentRequirement]
    estimated_documents: int
```

### Funcionalidades

| Feature | Descrição |
|---|---|
| Cadastro de empresas | CNPJ, filiais, centros de custo, contas bancárias |
| Proposta comercial | Escopo, módulos, pricing, prazo |
| Iniciar auditoria | Cria engagement + workflow + checklist |
| Equipe alocada | Consultores, revisor, gestor cliente |
| Cronograma | Milestones: ingestão → análise → revisão → entrega |
| Status tracking | Progresso por fase (% docs, % achados validados) |

### API Endpoints

```
POST   /api/v1/admin/companies
GET    /api/v1/admin/companies
GET    /api/v1/admin/companies/{id}
PUT    /api/v1/admin/companies/{id}
POST   /api/v1/admin/companies/{id}/branches
POST   /api/v1/admin/companies/{id}/bank-accounts
POST   /api/v1/admin/engagements
GET    /api/v1/admin/engagements
GET    /api/v1/admin/engagements/{id}
PUT    /api/v1/admin/engagements/{id}/status
POST   /api/v1/admin/engagements/{id}/team
```

---

## M13 — Precificação & Faturamento

### Objetivo
Gerenciar pricing, faturamento e margem por cliente/engagement.

### Funcionalidades

| Feature | Descrição |
|---|---|
| Tabela de preços | Por módulo, volume de documentos, complexidade |
| Proposta com pricing | Cálculo automático baseado em escopo |
| Faturamento | Mensal/recorrente (continuous audit) ou por projeto |
| Margem por engagement | Custo (horas consultor + LLM) vs receita |
| Tracking de receita | Dashboard financeiro DHV |

### Modelo de Pricing

```yaml
pricing_model:
  base_fee: 5000.00  # taxa base por engagement
  modules:
    logistics: 2000.00
    hr: 1500.00
    procurement: 1500.00
    financial: 2000.00
    fiscal: 2500.00
    fleet: 1000.00
  per_document: 0.50  # acima de 10.000 docs
  continuous_audit_monthly: 3000.00
```

---

## M14 — Workflow de Auditoria

### Objetivo
Orquestrar tarefas, filas e atribuições entre consultores durante o engagement.

### Funcionalidades

| Feature | Descrição |
|---|---|
| Kanban board | Colunas: Pendente → Em Análise → Revisão → Validado → Entregue |
| Filas por consultor | Inbox personalizado com priorização |
| Atribuição automática | Round-robin ou por especialidade |
| Prazos e SLA | Alertas de atraso, escalonamento |
| Checklist de documentos | Docs pendentes vs recebidos vs processados |
| Dependências | Tarefa B só inicia após tarefa A |

### Estados do Workflow

```
[Documento Pendente] → [Em Processamento] → [Extraído]
    → [Em Análise] → [Achado Detectado] → [Fila Revisão Humana]
    → [Validado] → [Plano de Ação Gerado] → [EQCR] → [Entregue ao Cliente]
    → [Follow-up Ativo] → [Valor Capturado] → [Encerrado]
```

---

## M15 — Workpapers & Evidências

### Objetivo
Pasta de trabalho digital que vincula cada achado à sua cadeia completa de evidências — requisito para credibilidade jurídica e profissional.

### Funcionalidades

| Feature | Descrição |
|---|---|
| Cadeia de evidências | Achado → Regra → Documento → Campo → Valor |
| Indexação automática | Workpaper gerado automaticamente por achado |
| Anotações do consultor | Comentários, flags, observações |
| Referência cruzada | Links entre achados relacionados |
| Export | Workpaper completo em PDF para arquivo |
| Imutabilidade | Evidências originais nunca alteradas (hash SHA-256) |

### Estrutura do Workpaper

```
Workpaper WP-2026-00142
├── Achado: Cobrança de frete acima da tabela
├── Severidade: HIGH | Impacto: R$ 47.850,00
├── Regra aplicada: LOG-003 (frete vs tabela contratada)
├── Evidências:
│   ├── [Doc] Fatura frete #8821 (p.2, campo valor_frete = R$ 12.500)
│   ├── [Doc] Contrato transp. XYZ (cláusula 4.2, tabela 2025)
│   └── [Calc] Diferença: R$ 12.500 - R$ 8.200 = R$ 4.300 × 11 faturas
├── Validação:
│   ├── Consultor: João Silva (2026-02-15)
│   └── Revisor EQCR: Maria Santos (2026-02-18)
└── Status: VALIDATED
```

---

## M16 — Revisão de Qualidade (EQCR)

### Objetivo
Garantir qualidade da entrega com segunda revisão independente antes de publicar achados ao cliente.

### Funcionalidades

| Feature | Descrição |
|---|---|
| Fila EQCR | Achados críticos e alto impacto vão obrigatoriamente |
| Checklist de qualidade | Metodologia, evidência suficiente, cálculo correto |
| Aprovação / Rejeição | Revisor aprova ou devolve com comentários |
| 4 olhos | Nenhum achado publicado sem 2 validações |
| Métricas de qualidade | Taxa de rejeição, tempo médio de revisão |

---

## M17 — Follow-up & Remediação

### Objetivo
Acompanhar se o cliente implementou cada ação recomendada e medir economia **capturada** vs **identificada**.

### Funcionalidades

| Feature | Descrição |
|---|---|
| Tracking de ações | Status: pendente → em andamento → concluída → verificada |
| Verificação automática | Re-ingestão de docs para confirmar correção |
| Economia capturada | R$ efetivamente recuperado/economizado |
| Alertas de atraso | Cliente não implementou ação no prazo |
| Relatório de valor | ROI do engagement para o cliente |
| Renovação | Sugestão de novo ciclo baseado em follow-up |

### Métricas de Valor

```
Economia Identificada:    R$ 250.000  (achados validados)
Economia em Andamento:    R$  80.000  (ações em execução)
Economia Capturada:       R$ 120.000  (ações concluídas e verificadas)
Taxa de Captura:          48%         (capturada / identificada)
ROI do Engagement:        12x         (capturada / custo auditoria)
```
