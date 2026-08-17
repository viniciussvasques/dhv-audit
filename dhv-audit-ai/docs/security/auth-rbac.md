# Autentica??o & Controle de Acesso Baseado em Pap?is (Auth & RBAC)

Este documento especifica a estrat?gia de seguran?a, autentica??o e matriz de permiss?es (RBAC) do sistema **DHV Audit AI**.

---

## 1. Fluxo de Autentica??o
O sistema adota autentica??o sem estado (*stateless*) baseada em tokens **JWT (JSON Web Tokens)** assinados com o algoritmo `HS256` ou `RS256`.

1. **Credenciais:** O usu?rio envia `email` e `password` para a rota `/api/v1/auth/login`.
2. **Emiss?o de Token:** O servidor valida o hash da senha (computado via `bcrypt` ou `argon2`) e emite um par de tokens:
   - `access_token` (vida ?til: 15 minutos).
   - `refresh_token` (vida ?til: 7 dias, armazenado em cookie seguro `HttpOnly`, `Secure` e `SameSite=Strict`).
3. **Sess?o:** Para cada requisi??o subsequente, o cliente anexa o `access_token` no header `Authorization: Bearer <token>`.

---

## 2. Hierarquia de Pap?is e Permiss?es (RBAC Matrix)

O sistema possui cinco pap?is predefinidos, divididos em escopos globais (DHV Log) e locais (Cliente).

| Permiss?o | SuperAdmin (DHV) | Consultant (DHV) | TenantAdmin (Cliente) | ClientManager (Cliente) | Viewer (Cliente) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Criar Tenants** | ? | ? | ? | ? | ? |
| **Alterar Configura??es do Sistema** | ? | ? | ? | ? | ? |
| **Criar Ciclos de Auditoria** | ? | ? | ? | ? | ? |
| **Deletar Ciclos de Auditoria** | ? | ? | ? | ? | ? |
| **Fazer Upload de Documentos** | ? | ? | ? | ? | ? |
| **Visualizar Findings (Achados)** | ? | ? | ? | ? | ? |
| **Validar Findings (Human-in-the-Loop)**| ? | ? | ? | ? | ? |
| **Editar Regras de Neg?cio (IA)** | ? | ? | ? | ? | ? |
| **Gerenciar Usu?rios do Tenant** | ? | ? | ? | ? | ? |

- **Escopo de Dados (Tenancy):**
  - Usu?rios com pap?is do Cliente (`TenantAdmin`, `ClientManager`, `Viewer`) s?o restritos pelo RLS do PostgreSQL ao seu respectivo `tenant_id`.
  - Usu?rios globais da DHV (`SuperAdmin`, `Consultant`) possuem privil?gios de acesso multi-tenant para cruzar e validar achados de m?ltiplos clientes do portf?lio.

---

## 3. Pol?ticas de Seguran?a de Senhas e MFA
- **Complexidade de Senhas:** M?nimo de 10 caracteres, exigindo pelo menos uma letra mai?scula, uma min?scula, um n?mero e um caractere especial.
- **Autentica??o de Dois Fatores (MFA):** Obrigat?ria para todos os usu?rios com papel `SuperAdmin` e `Consultant`. Opcional para os demais pap?is. Implementa??o via padr?o TOTP (Google Authenticator, Microsoft Authenticator).
- **Bloqueio de Contas (Brute-force protection):** Ap?s 5 tentativas de login incorretas consecutivas dentro de 10 minutos, a conta ? suspensa temporariamente por 30 minutos.
