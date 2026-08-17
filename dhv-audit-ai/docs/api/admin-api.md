# API de Administra??o (Admin & Core API)

Esta especifica??o t?cnica descreve as rotas de API fundamentais para o funcionamento da plataforma **DHV Audit AI**, englobando o gerenciamento de ciclos de auditoria, documentos e achados (*findings*).

---

## 1. Ciclos de Auditoria (`/api/v1/audits`)

### A. Criar Ciclo de Auditoria
- **M?todo:** `POST`
- **Path:** `/api/v1/audits`
- **Cabe?alhos:**
  - `X-Tenant-ID`: `UUID-do-Tenant`
- **Corpo da Requisi??o (JSON):**
```json
{
  "id": "c1a23b4c-1234-5678-90ab-cdef12345678",
  "company_id": "99b88c77-abcd-ef01-2345-6789abcdef01",
  "title": "Auditoria de Fretes - Q2/2026",
  "start_date": "2026-04-01",
  "end_date": "2026-06-30"
}
```
- **Resposta (201 Created):**
```json
{
  "id": "c1a23b4c-1234-5678-90ab-cdef12345678",
  "tenant_id": "33b44c55-1111-2222-3333-444455556666",
  "company_id": "99b88c77-abcd-ef01-2345-6789abcdef01",
  "title": "Auditoria de Fretes - Q2/2026",
  "start_date": "2026-04-01",
  "end_date": "2026-06-30",
  "status": "pending",
  "created_at": "2026-08-17T15:00:00Z"
}
```

### B. Obter Ciclo de Auditoria por ID
- **M?todo:** `GET`
- **Path:** `/api/v1/audits/{id}`
- **Resposta (200 OK):**
```json
{
  "id": "c1a23b4c-1234-5678-90ab-cdef12345678",
  "tenant_id": "33b44c55-1111-2222-3333-444455556666",
  "company_id": "99b88c77-abcd-ef01-2345-6789abcdef01",
  "title": "Auditoria de Fretes - Q2/2026",
  "start_date": "2026-04-01",
  "end_date": "2026-06-30",
  "status": "processing",
  "total_findings": 14,
  "total_financial_impact": 125430.22,
  "created_at": "2026-08-17T15:00:00Z"
}
```

---

## 2. Documentos e Ingest?o (`/api/v1/documents`)

### A. Fazer Upload de Documento para o Ciclo
- **M?todo:** `POST`
- **Path:** `/api/v1/documents/upload`
- **Content-Type:** `multipart/form-data`
- **Par?metros de Formul?rio (Form-data):**
  - `audit_cycle_id`: `c1a23b4c-1234-5678-90ab-cdef12345678` (UUID)
  - `document_type`: `cte` -- nfe, nfse, ofx, e_social, manual
  - `file`: `arquivo_fatura.pdf` (Bin?rio)
- **Resposta (201 Created):**
```json
{
  "id": "d9876c54-3210-fedc-ba98-76543210fedc",
  "audit_cycle_id": "c1a23b4c-1234-5678-90ab-cdef12345678",
  "filename": "arquivo_fatura.pdf",
  "file_path": "s3://dhv-audit-storage/tenant-33b4/arquivo_fatura.pdf",
  "file_hash": "a45f9...55b28",
  "document_type": "cte",
  "status": "queued",
  "created_at": "2026-08-17T15:05:00Z"
}
```

---

## 3. Achados e Revis?o Humana (`/api/v1/findings`)

### A. Adicionar Achado de Auditoria (Gerado pela IA / Parser)
- **M?todo:** `POST`
- **Path:** `/api/v1/audits/{cycle_id}/findings`
- **Corpo da Requisi??o (JSON):**
```json
{
  "id": "f5556667-7777-8888-9999-000011112222",
  "document_id": "d9876c54-3210-fedc-ba98-76543210fedc",
  "title": "Cobran?a de Frete Superior ? Tabela",
  "description": "O CT-e 10293 apresentou cobran?a de Frete Peso R$ 1.200,00, enquanto a tabela contratada estabelece R$ 950,00.",
  "severity": "high",
  "financial_impact": 250.00,
  "confidence_score": 0.96
}
```
- **Resposta (201 Created):**
```json
{
  "id": "f5556667-7777-8888-9999-000011112222",
  "audit_cycle_id": "c1a23b4c-1234-5678-90ab-cdef12345678",
  "document_id": "d9876c54-3210-fedc-ba98-76543210fedc",
  "title": "Cobran?a de Frete Superior ? Tabela",
  "description": "O CT-e 10293 apresentou cobran?a de Frete Peso R$ 1.200,00, enquanto a tabela contratada estabelece R$ 950,00.",
  "severity": "high",
  "financial_impact": 250.00,
  "confidence_score": 0.96,
  "is_validated": false,
  "created_at": "2026-08-17T15:10:00Z"
}
```

### B. Validar Achado (A??o Humana do Consultor / Human-in-the-Loop)
- **M?todo:** `PATCH`
- **Path:** `/api/v1/findings/{id}/validate`
- **Corpo da Requisi??o (JSON):**
```json
{
  "is_validated": true,
  "adjusted_impact": 250.00, -- Consultor pode revisar e ajustar o impacto final detectado pela IA
  "comment": "Auditado e confirmado em duplicidade de tabela."
}
```
- **Resposta (200 OK):**
```json
{
  "id": "f5556667-7777-8888-9999-000011112222",
  "is_validated": true,
  "financial_impact": 250.00,
  "validated_by": "u1112223-4444-5555-6666-777788889999", -- UUID do usu?rio consultor que validou
  "validated_at": "2026-08-17T15:15:00Z",
  "comment": "Auditado e confirmado em duplicidade de tabela."
}
```
