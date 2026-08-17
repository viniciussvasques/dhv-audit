# Painel de Administra??o da Plataforma (Admin Panel)

O **Painel de Administra??o** ? a ferramenta de governan?a global utilizada pelos administradores de TI da DHV Log para gerenciar o ecossistema de cont?ineres e schemas isolados do modelo de boutique de elite, cadastrar novos clientes da fila, monitorar a integridade das inst?ncias Docker e do PostgreSQL h?brido, e auditar as atividades dos consultores.

---

## 1. Tela: Gest?o de Clientes, Cont?ineres & Schemas (Client & Infrastructure Node Management)

Esta tela centraliza a cria??o, ativa??o e monitoramento dos n?s dedicados para as holdings parceiras.

### Componentes de Intera??o e M?tricas
- **Tabela Geral de N?s de Clientes (Client Nodes):**
  - **Nome/Grupo Econ?mico:** Raz?o social ou holding controladora.
  - **Subdom?nio/IP Privado:** URL ou endpoint privado de isolamento do n?.
  - **Status do Cont?iner:** `Rodando` (verde), `Parado` (cinza), `Iniciando` (azul) ou `Sobrecarga` (vermelho).
  - **Uso de Recursos por Cont?iner:** CPU, Mem?ria RAM e espa?o em disco no S3 dedicado.
  - **Status do Schema PostgreSQL:** Indica??o clara do schema isolado ativo (ex: `schema_cliente_alfa`).
- **Formul?rio de Cria??o de N? (Wizard de Provisionamento):**
  - **Passo 1:** Dados B?sicos (Raz?o Social, CNPJ Principal, Endere?o).
  - **Passo 2:** Provisionamento do Cont?iner (Gera automaticamente um novo n? Docker dedicado em porta isolada).
  - **Passo 3:** Cria??o do Schema Isolado (Inicia o schema isolado no PostgreSQL executando as migrations via Alembic).
  - **Passo 4:** Configura??es de Integra??o sob Demanda (Configura??o das credenciais personalizadas de VPN ou t?nel seguro para leitura de ERP legados como SAP e TOTVS/Protheus).

---

## 2. Tela: Monitor de Desempenho e Lat?ncia dos Agentes de IA (AI Orchestrator Monitor)

Esta tela fornece m?tricas t?cnicas em tempo real sobre a sa?de dos processamentos ass?ncronos e custos de provedores de IA.

### M?tricas em Tempo Real
- **Fila de Ingest?o e OCR:**
  - Quantidade de documentos na fila de espera para OCR (`Pendente na Fila: 4`).
  - Tempo m?dio de processamento por p?gina (`3.2 segundos`).
- **Uso e Custo de Tokens de IA (LLM Costs):**
  - Consumo acumulado de tokens de entrada e sa?da por Tenant.
  - Gr?fico de pizza mostrando a divis?o de chamadas por modelo (`GPT-4o`, `Claude 3.5 Sonnet`, `Llama 3`).
- **Fila de Erros e Exce??es (Fallback Center):**
  - Lista de arquivos que apresentaram falha cr?tica no parser de IA ou de OCR.
  - Bot?o `Reprocessar com Modelo Alternativo` (muda dinamicamente o modelo de fallback de OpenAI para Anthropic).

---

## 3. Tela: Trilha de Auditoria Geral (Global Audit Trail)

Cumpre os requisitos de conformidade de seguran?a e privacidade de dados (LGPD e SOC 2), registrando de forma inalter?vel todas as modifica??es cr?ticas no banco de dados e a??es de usu?rios.

### Funcionalidades de Pesquisa e Filtragem
- **Busca Avan?ada de Seguran?a:**
  - Filtro por Usu?rio, IP de origem, A??o executada, ou Intervalo de Datas.
- **Visualizador de Diffs (Hist?rico de Altera??es):**
  - Exibe um comparativo side-by-side (formato git diff) com as altera??es efetuadas em dados sens?veis.
  - Exemplo de log de altera??o de dados banc?rios de fornecedores:
    - Vermelho (Antes): `conta_corrente: "12345-6"`
    - Verde (Depois): `conta_corrente: "98765-4"` (sinalizado com tag de alerta de alta criticidade).
