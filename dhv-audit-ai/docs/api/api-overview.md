# Vis?o Geral da API (API Overview)

## 1. Diretrizes de Design RESTful
A API do **DHV Audit AI** ? projetada seguindo padr?es r?gidos REST e orientada pelo protocolo HTTPS para todas as comunica??es.

- **Formato de Dados:** Todas as requisi??es e respostas utilizam `application/json` codificado em UTF-8.
- **Autentica??o:** Baseada em Tokens JWT transmitidos no cabe?alho `Authorization: Bearer <token>`.
- **Cabe?alho Multi-tenant:** Toda requisi??o ? API deve incluir o header `X-Tenant-ID` para controle de contexto, exceto nas rotas de autentica??o e no portal global.
- **Versionamento:** O controle de vers?o ? inclu?do diretamente no path da URL (ex: `/api/v1/...`).

---

## 2. Padr?o de Respostas HTTP

### C?digos de Status Comuns
| C?digo | Significado | Descri??o |
|---|---|---|
| `200 OK` | Sucesso | Requisi??o processada com ?xito. Retorna os dados solicitados. |
| `201 Created` | Criado | Novo recurso criado com sucesso (ex: novo Ciclo de Auditoria). |
| `204 No Content` | Sem Conte?do | Opera??o realizada com sucesso, sem conte?do de retorno (ex: dele??o). |
| `400 Bad Request` | Requisi??o Inv?lida | Erro de valida??o de dados no corpo da requisi??o ou formato incorreto. |
| `401 Unauthorized` | N?o Autorizado | Token de autentica??o ausente, expirado ou inv?lido. |
| `403 Forbidden` | Proibido | O usu?rio possui token v?lido, mas n?o tem permiss?o para o recurso solicitado. |
| `404 Not Found` | N?o Encontrado | O recurso especificado n?o existe no banco de dados. |
| `422 Unprocessable` | Erro Sem?ntico | O corpo da mensagem est? em formato correto, mas cont?m erros l?gicos de valida??o. |
| `500 Server Error` | Erro Interno | Falha inesperada no processamento do servidor. |

---

## 3. Formato de Erro Padronizado (JSON)
Em caso de erro (4xx ou 5xx), a API retorna um payload JSON contendo os seguintes campos:
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "O campo 'financial_impact' deve ser um valor num?rico positivo.",
    "details": [
      {
        "field": "financial_impact",
        "issue": "must_be_positive_float"
      }
    ],
    "timestamp": "2026-08-17T14:32:00Z"
  }
}
```

---

## 4. Pagina??o, Filtros e Ordena??o
Para rotas que retornam listas (cole??es de recursos como achados ou documentos), adotam-se os seguintes par?metros de query:

- **Pagina??o:**
  - `page`: N?mero da p?gina (indexada em 1). Ex: `?page=2`
  - `limit`: Quantidade de registros por p?gina. Ex: `?limit=50` (padr?o ? 20, m?ximo de 100).
- **Ordena??o:**
  - `sort_by`: Campo para ordena??o (ex: `?sort_by=created_at`).
  - `order`: Dire??o da ordena??o (`asc` ou `desc`). Ex: `?order=desc`.
- **Filtros Din?micos:**
  - Filtros espec?ficos do recurso (ex: `/api/v1/findings?severity=high&is_validated=false`).
