# Portal do Cliente (Client Portal - Self-Service)

O **Portal do Cliente** ? o ambiente voltado para os clientes corporativos da DHV Log. Projetado com foco em UX clara, executiva e altamente visual, o portal permite que gestores de log?stica, diretores financeiros e equipes de suprimentos acompanhem o andamento das auditorias, fa?am uploads, analisem os achados validados e executem o plano de a??o sugerido pela IA.

---

## 1. Tela: Dashboard Executivo (Executive Overview)

A p?gina inicial do portal apresenta uma vis?o de alto n?vel sobre a sa?de financeira e de conformidade de todas as opera??es auditadas.

### Elementos de Destaque (Cart?es e Gr?ficos)
- **Painel de Hero Cards (KPIs):**
  - **Economia Identificada (Potential Saving):** Valor total de diverg?ncias identificadas (`R$ 1.250.400,00`).
  - **Economia Capturada (Captured Saving):** Valores efetivamente recuperados ou glosados junto aos fornecedores (`R$ 840.200,00`).
  - **Percentual de Erros (Leakage Rate):** Indicador de vazamento de receita em rela??o ao total de faturamento auditado (`1.4%`).
  - **?ndice OTIF Global:** SLA m?dio de cumprimento de prazos de entrega das transportadoras contratadas (`92.3%`).
- **Gr?fico de Evolu??o Mensal (?rea):**
  - Exibe a evolu??o temporal do volume de faturamento auditado em rela??o ao total de anomalias encontradas, evidenciando a redu??o progressiva de erros conforme o cliente aplica os planos de a??o recomendados pela plataforma.
- **Gr?fico de Rosca (Diferen?a por Dom?nio):**
  - Distribui??o percentual do desperd?cio financeiro por categoria (`Log?stica`, `RH`, `Compras`, `Fiscal`, `Frota`).

---

## 2. Tela: Central de Ingest?o de Documentos (Self-Service Ingestion)

Permite ao cliente subir novos lotes de documentos fiscais e operacionais sem interagir diretamente com o consultor.

### Componentes de Intera??o
- **?rea de Drag & Drop Integrada:**
  - Suporta sele??o m?ltipla de arquivos (`.pdf`, `.xml`, `.xlsx`, `.zip`).
  - Filtro din?mico para selecionar o **Ciclo de Auditoria** ao qual os arquivos pertencem.
- **Lista Din?mica de Pend?ncias (Checklist de Documentos):**
  - Um checklist autom?tico gerado com base no faturamento do m?s:
    - `[Ok] XMLs de CT-e de Junho/2026 (1.200 arquivos processados)`
    - `[Pendente] Extratos Banc?rios OFX de Junho/2026 (Faltam 3 contas)`
    - `[Ok] eSocial Eventos S-1200 de Junho/2026`
- **Tabela de Arquivos Processados:**
  - Lista em tempo real os arquivos enviados, tamanho, data de envio e o status de extra??o e OCR (`Processado`, `Em an?lise pela IA`, `Revis?o manual`).

---

## 3. Tela: Plano de A??o & Recupera??o de Valores (Action Center)

Esta tela transforma os achados validados em tarefas acion?veis e gerencia o processo de contesta??o de cobran?as incorretas.

### Layout e Estrutura Visual
- **Fichas de A??o (Kanban ou Tabela de A??es):**
  - Cada a??o possui:
    - **T?tulo:** Ex: `Contestar cobran?a duplicada da Transportadora R?pido Rodovi?rio`.
    - **Origem (Achado):** Link para o achado correspondente na base de dados.
    - **Retorno Esperado (ROI):** Valor a ser recuperado (`R$ 5.420,00`).
    - **Esfor?o estimado:** `Baixo` / `M?dio` / `Alto`.
- **Gera??o do Kit de Contesta??o:**
  - O cliente pode clicar no bot?o `Gerar Kit de Contesta??o` para aquele fornecedor espec?fico.
  - A plataforma compila automaticamente:
    1. A minuta de e-mail personalizada escrita pela IA.
    2. O PDF com a planilha consolidada de todos os CT-es cobrados a mais.
    3. As imagens e links dos documentos f?sicos de evid?ncia do erro de cobran?a.
- **Acompanhamento de Status da Captura:**
  - O gestor atualiza o status de recupera??o: `Identificado` ? `Contestado` ? `Aprovado pelo Fornecedor` ? `Valor Recuperado (Cr?dito em Fatura/Dep?sito)`.
  - Alimenta em tempo real o KPI de **Economia Capturada** no Dashboard Executivo.
