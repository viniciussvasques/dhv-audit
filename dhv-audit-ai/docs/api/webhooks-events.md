# Webhooks & Mensageria Asqu?ncrona (Webhooks & Async Events)

Esta especifica??o descreve os t?picos de mensageria ass?ncrona, filas e callbacks por webhook suportados pela arquitetura do **DHV Audit AI** para integra??es com ERPs de clientes, sistemas fiscais e atualiza??es de status em tempo real.

---

## 1. Arquitetura Base de Webhooks
Sempre que um evento de longa dura??o (como OCR de documentos, an?lise de agentes de IA ou processamento de relat?rios em lote) ? conclu?do, o sistema dispara uma notifica??o HTTP POST (*Webhook*) para a URL registrada no Tenant Profile do cliente.

- **Assinatura de Seguran?a:** Todos os payloads de webhooks incluem o cabe?alho `X-DHV-Signature` contendo o hash HMAC-SHA256 do corpo do payload, computado com a chave secreta compartilhada do cliente.
- **Pol?ticas de Retentativa:** Se o servidor do cliente retornar c?digos de status diferentes de 2xx, o sistema adota retentativas exponenciais com jitter (m?ximo de 5 tentativas em 24h).

---

## 2. Eventos de Processamento de Documentos (`document.parsed`)
Disparado imediatamente ap?s o motor de OCR e LLM Vision concluir a leitura estruturada do documento e calcular o Score de Confian?a.

```json
{
  "event": "document.parsed",
  "timestamp": "2026-08-17T15:20:00Z",
  "tenant_id": "33b44c55-1111-2222-3333-444455556666",
  "data": {
    "document_id": "d9876c54-3210-fedc-ba98-76543210fedc",
    "audit_cycle_id": "c1a23b4c-1234-5678-90ab-cdef12345678",
    "filename": "cte-001923.xml",
    "document_type": "cte",
    "ocr_confidence_score": 98.40,
    "status": "processed",
    "fields_extracted": {
      "cnpj_emitter": "12345678000199",
      "cnpj_receiver": "98765432000100",
      "total_value": 4500.00,
      "tax_value": 540.00
    }
  }
}
```

---

## 3. Eventos de An?lise e Detec??o de Achados (`finding.detected`)
Disparado quando a IA de auditoria (Logistics, Fiscal, HR, etc.) detecta uma anomalia em um documento ou lote de transa??es.

```json
{
  "event": "finding.detected",
  "timestamp": "2026-08-17T15:22:00Z",
  "tenant_id": "33b44c55-1111-2222-3333-444455556666",
  "data": {
    "finding_id": "f5556667-7777-8888-9999-000011112222",
    "audit_cycle_id": "c1a23b4c-1234-5678-90ab-cdef12345678",
    "document_id": "d9876c54-3210-fedc-ba98-76543210fedc",
    "title": "Cobran?a de Frete Superior ? Tabela",
    "severity": "high",
    "financial_impact": 250.00,
    "confidence_score": 0.96,
    "needs_human_review": false
  }
}
```

---

## 4. Eventos de Fluxo Humano (`finding.validated`)
Disparado quando o auditor/consultor da DHV Log aprova ou rejeita o achado sinalizado pela IA na fila de valida??o (*Human-in-the-Loop*).

```json
{
  "event": "finding.validated",
  "timestamp": "2026-08-17T15:30:00Z",
  "tenant_id": "33b44c55-1111-2222-3333-444455556666",
  "data": {
    "finding_id": "f5556667-7777-8888-9999-000011112222",
    "is_validated": true,
    "adjusted_financial_impact": 250.00,
    "validator_name": "Pedro Alvares Cabral",
    "validation_comment": "Confirmado pela equipe de log?stica."
  }
}
```
