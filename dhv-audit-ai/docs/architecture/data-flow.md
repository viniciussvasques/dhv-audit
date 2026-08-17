# Fluxo de Dados — Pipeline Ponta a Ponta

## 1. Fluxo Principal: Documento → Ação

```mermaid
flowchart TD
    A[Entrada de Dados] --> B{Canal}
    B -->|Upload| C1[Ingestion Service]
    B -->|Email| C1
    B -->|API/ERP| C1
    B -->|Open Banking| C1
    B -->|SPED/eSocial| C1

    C1 --> D[Validação & Deduplicação]
    D --> E[Storage S3 - Original Imutável]
    D --> F[Extraction Pipeline]

    F --> G{Tipo Documento}
    G -->|PDF/Imagem| H1[OCR + LLM Vision]
    G -->|XML NF-e/CT-e| H2[Parser XML]
    G -->|XLSX/CSV| H3[Parser Tabular]
    G -->|OFX/Banco| H4[Parser Financeiro]
    G -->|SPED| H5[Parser SPED]

    H1 & H2 & H3 & H4 & H5 --> I[Dados Estruturados + Confidence Score]
    I --> J{Confiança < 90%?}
    J -->|Sim| K[Fila Revisão Humana]
    J -->|Não| L[Classification & Taxonomia DHV]
    K --> L

    L --> M[Analysis Engine]
    M --> N[Regras Determinísticas]
    M --> O[Agentes IA por Domínio]
    M --> P[Benchmark DHV]
    M --> Q[Cruzamento Cross-Domain]

    N & O & P & Q --> R[Achados com Evidência]
    R --> S[Scoring: Severidade + Impacto + Confiança]
    S --> T[Human-in-the-Loop Validation]
    T --> U[Action Plan Generator]
    U --> V[Entrega: Dashboard + Relatório + Plano de Ação]
    V --> W[Follow-up & Captura de Valor]
```

---

## 2. Fluxo Comercial: Cliente → Contrato → Auditoria

```mermaid
sequenceDiagram
    participant SA as Super Admin
    participant AD as Admin DHV
    participant CRM as Commercial Module
    participant CL as Cliente
    participant ENG as Engagement Module
    participant WF as Workflow

    SA->>CRM: Cadastra tenant + chaves provedores
    AD->>CRM: Cadastra empresa cliente (CNPJ, filiais)
    AD->>CRM: Cria proposta comercial (escopo, módulos, pricing)
    CRM->>CL: Envia proposta para aprovação
    CL->>CRM: Aprova proposta
    CRM->>CRM: Gera contrato de auditoria (PDF)
    CRM->>CRM: Gera NDA / confidencialidade (PDF)
    CL->>CRM: Assina contratos (e-sign)
    AD->>ENG: Inicia engagement (ciclo de auditoria)
    ENG->>WF: Cria workflow com checklist documentos
    ENG->>CL: Notifica: documentos pendentes
    CL->>ENG: Upload documentos + conecta contas bancárias
    ENG->>ENG: Dispara pipeline de análise
```

---

## 3. Fluxo de Cruzamento de Dados (Cross-Domain)

```mermaid
flowchart LR
    subgraph fontes [Fontes de Dados]
        LOG[Logística<br/>CT-e, Faturas Frete]
        FIN[Financeiro<br/>Extratos, AP/AR]
        RH[RH<br/>Folha, eSocial]
        COMP[Compras<br/>NF-e, Cotações]
        FISC[Fiscal<br/>SPED, NF-e XML]
        BANK[Contas Bancárias<br/>OFX, Open Banking]
    end

    subgraph grafo [Grafo de Relacionamentos]
        CNPJ[Entidade: CNPJ]
        DOC[Entidade: Documento]
        PAY[Entidade: Pagamento]
        EMP[Entidade: Funcionário]
    end

    LOG & FIN & RH & COMP & FISC & BANK --> grafo

    grafo --> CRUZ[Cruzamento Engine]

    CRUZ --> R1[NF-e Compra × Pagamento Bancário<br/>→ Pagamento sem NF]
    CRUZ --> R2[CT-e × NF-e × Contrato Frete<br/>→ Frete acima tabela]
    CRUZ --> R3[Folha × eSocial × FGTS<br/>→ Encargos incorretos]
    CRUZ --> R4[Fornecedor × Múltiplos CNPJs<br/>→ Possível fraude]
    CRUZ --> R5[Centro Custo × Despesa × Budget<br/>→ Estouro orçamentário]
    CRUZ --> R6[Funcionário × Nota × Reembolso<br/>→ Reembolso indevido]
```

---

## 4. Fluxo Admin: Gestão da Plataforma

```mermaid
flowchart TD
    ADMIN[Painel Admin DHV] --> TEN[Tenants & Empresas]
    ADMIN --> USR[Usuários & RBAC]
    ADMIN --> KEY[Chaves de Provedores]
    ADMIN --> MOD[Módulos Ativos por Tenant]
    ADMIN --> BIL[Billing & Faturamento]
    ADMIN --> AUD[Audit Trail Global]
    ADMIN --> CFG[Configurações Globais]

    KEY --> KEY1[OpenAI API Key]
    KEY --> KEY2[Anthropic API Key]
    KEY --> KEY3[AWS Textract]
    KEY --> KEY4[SEFAZ Webhook]
    KEY --> KEY5[Open Banking]

    TEN --> TEN1[Empresa Matriz]
    TEN1 --> TEN2[Filiais / CNPJs]
    TEN2 --> TEN3[Centros de Custo]
    TEN3 --> TEN4[Contas Bancárias]
```

---

## 5. Eventos de Domínio (Event-Driven)

| Evento | Produtor | Consumidores |
|---|---|---|
| `DocumentUploaded` | Ingestion | Extraction, Workflow |
| `DocumentExtracted` | Extraction | Classification, Review Queue |
| `DocumentClassified` | Classification | Analysis |
| `FindingDetected` | Analysis | Review Queue, Dashboard, Chat |
| `FindingValidated` | Governance | Action Plan, Follow-up |
| `ActionPlanGenerated` | Delivery | Client Portal, Workflow |
| `EngagementStarted` | Engagement | Ingestion, Workflow, Contracts |
| `ContractSigned` | Commercial | Engagement, Governance |
| `CrossReferenceDetected` | Analysis | Consultant Workspace |
| `ValueCaptured` | Follow-up | Dashboard, Billing |

---

## 6. Filas Assíncronas

| Fila | Prioridade | SLA |
|---|---|---|
| `extraction.ocr` | Normal | < 5 min/documento |
| `extraction.xml` | Alta | < 30 seg/documento |
| `analysis.rules` | Alta | < 2 min/lote |
| `analysis.ai` | Normal | < 10 min/lote |
| `analysis.cross_domain` | Normal | < 15 min/engagement |
| `reports.generate` | Baixa | < 30 min/relatório |
| `contracts.generate` | Alta | < 1 min/documento |
| `notifications.email` | Normal | < 1 min |
| `review.human` | Crítica | SLA definido por engagement |
