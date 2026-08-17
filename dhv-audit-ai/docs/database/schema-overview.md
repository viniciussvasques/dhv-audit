# Vis?o Geral do Banco de Dados (Schema Overview)

## 1. Estrat?gia de Multi-tenancy e Isolamento
A plataforma utiliza uma abordagem de banco de dados ?nico com isolamento l?gico baseado em **Row-Level Security (RLS)** do PostgreSQL. 
*   Cada tabela de neg?cio possui obrigatoriamente a coluna `tenant_id`.
*   As pol?ticas de RLS garantem que consultas efetuadas por um usu?rio autenticado acessem estritamente os dados associados ao seu pr?prio `tenant_id`.
*   O bypass de RLS ? permitido apenas para perfis de suporte global (*SuperAdmin/Consultores DHV*) mediante autoriza??o espec?fica e chave de criptografia dedicada.

---

## 2. Tabelas Principais do Sistema

### A. Tabela: `tenants`
Armazena as informa??es das organiza??es que assinam a plataforma (clientes corporativos da DHV ou filiais administrativas).
```sql
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'active', -- active, suspended, canceled
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
```

### B. Tabela: `users`
Controle de usu?rios com controle de acesso baseado em pap?is (RBAC).
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'viewer', -- super_admin, admin, consultant, client_manager, viewer
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
CREATE INDEX idx_users_tenant ON users(tenant_id);
```

### C. Tabela: `companies`
Representa as pessoas jur?dicas (CNPJs) associadas a um tenant. Um grupo econ?mico (tenant) pode conter m?ltiplas empresas.
```sql
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    cnpj VARCHAR(14) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    trade_name VARCHAR(255),
    state_registration VARCHAR(20),
    city_registration VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
CREATE INDEX idx_companies_tenant ON companies(tenant_id);
```

### D. Tabela: `audit_cycles` (Ciclos de Auditoria)
Fases espec?ficas de auditoria executadas em uma janela de tempo.
```sql
CREATE TABLE audit_cycles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    company_id UUID REFERENCES companies(id) ON DELETE RESTRICT,
    title VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, processing, analyzed, validated, completed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
CREATE INDEX idx_audit_cycles_tenant ON audit_cycles(tenant_id);
```

### E. Tabela: `documents`
Guarda registros e refer?ncias aos arquivos originais ingestados e armazenados no Object Storage (S3).
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    audit_cycle_id UUID REFERENCES audit_cycles(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(512) NOT NULL, -- URI no bucket S3 (ex: s3://bucket/tenant/file.pdf)
    file_hash VARCHAR(64) NOT NULL, -- SHA-256 para evitar duplicidade de ingest?o
    document_type VARCHAR(50) NOT NULL, -- cte, nfe, nfse, ofx, e_social, manual
    status VARCHAR(50) DEFAULT 'queued', -- queued, parsing, processed, failed
    ocr_confidence_score NUMERIC(5,2),
    raw_extracted_json JSONB, -- Dados JSON estruturados pelo parser
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
CREATE INDEX idx_documents_hash ON documents(file_hash);
CREATE INDEX idx_documents_cycle ON documents(audit_cycle_id);
```

### F. Tabela: `findings` (Achados e Desvios Identificados)
Cont?m as diverg?ncias encontradas pelo motor de regras e agentes de IA que representam oportunidades de economia de custos ou riscos tribut?rios.
```sql
CREATE TABLE findings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    audit_cycle_id UUID REFERENCES audit_cycles(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    severity VARCHAR(50) NOT NULL, -- low, medium, high, critical
    financial_impact NUMERIC(15,2) NOT NULL DEFAULT 0.00,
    confidence_score NUMERIC(5,2) NOT NULL,
    is_validated BOOLEAN DEFAULT FALSE NOT NULL,
    validated_by UUID REFERENCES users(id),
    validated_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
CREATE INDEX idx_findings_cycle ON findings(audit_cycle_id);
CREATE INDEX idx_findings_severity ON findings(severity);
```

### G. Tabela: `audit_logs` (Trilha de Auditoria Geral)
Registo imut?vel de todas as a??es sens?veis realizadas na plataforma para conformidade com a LGPD e SOC 2.
```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL, -- login, user_create, document_delete, finding_validate
    target_table VARCHAR(100) NOT NULL,
    target_id UUID NOT NULL,
    before_state JSONB,
    after_state JSONB,
    ip_address VARCHAR(45) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
CREATE INDEX idx_audit_logs_tenant ON audit_logs(tenant_id);
```
