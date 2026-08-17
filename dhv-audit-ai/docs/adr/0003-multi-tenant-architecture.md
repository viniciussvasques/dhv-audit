# 0003: Arquitetura Multi-Tenant

**Status**: Aceito  
**Data**: 2026-08-16

---

## Contexto

A plataforma atende múltiplas empresas clientes da DHV, cada uma com filiais, CNPJs, centros de custo e contas bancárias. Dados fiscais e financeiros exigem isolamento rigoroso. Precisamos de uma estratégia multi-tenant que balance segurança, performance e simplicidade operacional.

---

## Decisão

Adotar **multi-tenant com isolamento lógico via `tenant_id` + Row-Level Security (RLS)** no PostgreSQL.

### Modelo de Tenancy

```
┌─────────────────────────────────────────────┐
│              DHV Platform (Root)             │
│  Super Admin gerencia tudo                   │
├─────────────────────────────────────────────┤
│  Tenant: Empresa Cliente A (Grupo X)        │
│  ├── Company: Matriz (CNPJ 01)              │
│  │   ├── Branch: Filial SP (CNPJ 02)        │
│  │   ├── Branch: Filial RJ (CNPJ 03)        │
│  │   ├── CostCenter: Logística               │
│  │   ├── CostCenter: RH                      │
│  │   └── BankAccount: Itaú 12345-6           │
│  ├── Engagement: Auditoria Q1 2026           │
│  └── Users: gestor@empresaA.com, ...         │
├─────────────────────────────────────────────┤
│  Tenant: Empresa Cliente B (Grupo Y)        │
│  └── ...                                     │
└─────────────────────────────────────────────┘
```

### Estratégia de Isolamento

| Camada | Mecanismo |
|---|---|
| **Banco de dados** | Coluna `tenant_id` em TODAS as tabelas + RLS policy |
| **API** | Middleware extrai `tenant_id` do JWT → set `app.current_tenant` |
| **Storage S3** | Prefixo `/{tenant_id}/documents/...` |
| **Cache Redis** | Prefixo de key `tenant:{id}:...` |
| **Filas** | Payload inclui `tenant_id`; worker valida |
| **Logs** | Campo `tenant_id` em structured logging |

### Hierarquia Organizacional

```sql
-- Entidades de organização
tenants          (id, name, plan, settings)
companies        (id, tenant_id, cnpj, razao_social, type: matriz|filial)
cost_centers     (id, company_id, code, name, department)
bank_accounts    (id, company_id, bank, agency, account, type)
departments      (id, company_id, name)
employees        (id, company_id, cpf, name, cost_center_id)
```

### RLS Policy (exemplo)

```sql
ALTER TABLE audit_cycles ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON audit_cycles
    USING (tenant_id = current_setting('app.current_tenant')::uuid);
```

### JWT Claims

```json
{
  "sub": "user-uuid",
  "tenant_id": "tenant-uuid",
  "role": "consultant",
  "permissions": ["audit:read", "audit:write", "finding:validate"],
  "company_scope": ["company-uuid-1", "company-uuid-2"]
}
```

---

## Alternativas Consideradas

| Opção | Prós | Contras | Decisão |
|---|---|---|---|
| Schema por tenant | Isolamento forte | Complexidade migração N schemas | Rejeitada |
| Database por tenant | Máximo isolamento | Custo operacional alto | Rejeitada |
| tenant_id + RLS | Simples, performático, seguro | Requer disciplina no código | **Aceita** |
| Tenant_id sem RLS | Mais simples | Risco de data leak por bug | Rejeitada |

---

## Consequências

- Toda query DEVE incluir filtro de tenant (enforced by RLS)
- Testes DEVEM validar isolamento cross-tenant
- Super Admin bypassa RLS via role especial
- Migração de dados entre tenants não é trivial (by design)
