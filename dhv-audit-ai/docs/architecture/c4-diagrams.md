# Diagramas C4 — DHV Audit AI Platform

## Nível 1 — Contexto do Sistema

```mermaid
C4Context
    title Contexto do Sistema — DHV Audit AI

    Person(admin, "Super Admin DHV", "Gerencia plataforma, chaves, tenants")
    Person(consultant, "Consultor DHV", "Executa e valida auditorias")
    Person(client, "Gestor Cliente", "Upload docs, aprova achados")
    Person(reviewer, "Revisor Qualidade", "EQCR antes da entrega")

    System(dhv, "DHV Audit AI Platform", "Auditoria inteligente com IA, cruzamento de dados e prescrição de ações")

    System_Ext(sefaz, "SEFAZ / Receita", "NF-e, CT-e, SPED")
    System_Ext(erp, "ERPs", "SAP, TOTVS, Sankhya, Omie")
    System_Ext(bank, "Open Banking", "Extratos, transações")
    System_Ext(llm, "Provedores IA", "OpenAI, Anthropic, AWS")
    System_Ext(ocr, "Motores OCR", "AWS Textract, Tesseract")
    System_Ext(esign, "Assinatura Digital", "DocuSign, Clicksign")
    System_Ext(email, "Email (SMTP)", "Recepção automática de docs")

    Rel(admin, dhv, "Gerencia plataforma")
    Rel(consultant, dhv, "Executa auditorias")
    Rel(client, dhv, "Envia docs, aprova achados")
    Rel(reviewer, dhv, "Revisa qualidade")
    Rel(dhv, sefaz, "Consulta XMLs fiscais")
    Rel(dhv, erp, "Importa dados operacionais")
    Rel(dhv, bank, "Importa extratos")
    Rel(dhv, llm, "Análise com IA")
    Rel(dhv, ocr, "Extração de documentos")
    Rel(dhv, esign, "Contratos e NDAs")
    Rel(email, dhv, "Recebe documentos por email")
```

---

## Nível 2 — Contêineres

```mermaid
C4Container
    title Contêineres — DHV Audit AI

    Person(user, "Usuário", "Admin, Consultor ou Cliente")

    Container_Boundary(frontend, "Frontend") {
        Container(admin_ui, "Admin Panel", "Next.js", "Gestão plataforma")
        Container(client_ui, "Client Portal", "Next.js", "Self-service cliente")
        Container(consultant_ui, "Consultant Workspace", "Next.js", "Operação auditoria")
    }

    Container_Boundary(backend, "Backend") {
        Container(api, "API Gateway", "FastAPI", "REST API v1")
        Container(worker, "Worker", "Celery/ARQ", "Processamento assíncrono")
        Container(analyzer, "Analysis Engine", "Python", "Regras + IA + Cruzamento")
    }

    ContainerDb(db, "PostgreSQL", "Dados estruturados multi-tenant")
    ContainerDb(redis, "Redis", "Cache, filas, sessions")
    ContainerDb(s3, "S3 / MinIO", "Documentos originais")
    ContainerDb(graph, "Entity Graph", "PostgreSQL + JSONB", "Grafo de relacionamentos")

    Rel(user, admin_ui, "HTTPS")
    Rel(user, client_ui, "HTTPS")
    Rel(user, consultant_ui, "HTTPS")
    Rel(admin_ui, api, "REST/JSON")
    Rel(client_ui, api, "REST/JSON")
    Rel(consultant_ui, api, "REST/JSON")
    Rel(api, db, "SQLAlchemy")
    Rel(api, redis, "Cache/Sessions")
    Rel(api, worker, "Enqueue jobs")
    Rel(worker, analyzer, "Process")
    Rel(worker, s3, "Read/Write docs")
    Rel(analyzer, db, "Store findings")
    Rel(analyzer, graph, "Cross-reference")
```

---

## Nível 3 — Componentes do Backend (Módulos)

```mermaid
graph TB
    subgraph interfaces [Interfaces Layer]
        API[FastAPI Router]
        WH[Webhooks]
        MW[Middleware: Auth, Tenant, Audit]
    end

    subgraph application [Application Layer]
        UC[Use Cases]
        EH[Event Handlers]
        SCH[Schedulers]
    end

    subgraph modules [Business Modules]
        PLAT[Platform<br/>Users, RBAC]
        COMM[Commercial<br/>CRM, Contracts]
        ENG[Engagement<br/>Audit Cycles]
        ING[Ingestion<br/>Upload, Connectors]
        EXT[Extraction<br/>OCR, Parsers]
        CLS[Classification<br/>Taxonomy]
        ANA[Analysis<br/>Rules, AI, Cross]
        DEL[Delivery<br/>Reports, Actions]
        GOV[Governance<br/>Workpapers, EQCR]
        WF[Workflow<br/>Tasks, Queues]
        FUP[Follow-up<br/>Remediation]
        INT[Integrations<br/>ERP, Bank, SEFAZ]
    end

    subgraph domains [Audit Domains]
        LOG[Logistics]
        HR[HR]
        PROC[Procurement]
        FIN[Financial]
        FISC[Fiscal]
        FLEET[Fleet]
    end

    subgraph infrastructure [Infrastructure]
        PG[(PostgreSQL)]
        RD[(Redis)]
        S3[(S3)]
        LLM[LLM Client]
        OCR[OCR Client]
    end

    API --> UC
    UC --> modules
    ANA --> domains
    modules --> infrastructure
    domains --> infrastructure
```

---

## Nível 4 — Componentes do Analysis Engine

```mermaid
graph LR
    INPUT[Dados Estruturados] --> ER[Entity Resolution]
    ER --> GB[Graph Builder]
    GB --> RE[Rule Engine]
    GB --> PM[Pattern Matcher ML]
    RE --> IC[Impact Calculator]
    PM --> IC
    IC --> AR[Action Recommender]
    AR --> OUT[Actionable Findings]

    RE --> RL[(Rule Library<br/>M18)]
    PM --> BM[(Benchmark DHV<br/>M5)]
    AR --> KB[(Knowledge Base<br/>M26)]
```
