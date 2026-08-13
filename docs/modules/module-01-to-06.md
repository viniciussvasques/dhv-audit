# Especificação Técnica dos Módulos 1 a 6 — DHV Audit AI

## Módulo 1 — Ingestão de Documentos
- **Objetivo:** Capturar dados operacionais e financeiros brutos de diversas fontes com rastreabilidade.
- **Entradas:** PDF, imagens (PNG/JPG escaneados), XML (NF-e, CT-e, NFS-e), planilhas (XLSX, CSV), arquivos OFX de extratos bancários e arquivos compactados (.zip).
- **Funcionalidades:**
  - Upload manual via drag-and-drop na interface web com validação prévia de integridade.
  - E-mail dedicado por cliente (ex: `cliente.auditoria@dhvlog.com.br`) para recepção automática de faturas e XMLs.
  - Conectores de API para integração com ERPs (SAP, TOTVS, Sankhya) e webhooks SEFAZ.
  - Checklist dinâmico de documentos pendentes por ciclo de auditoria.

## Módulo 2 — OCR & Extração Estruturada de Dados
- **Objetivo:** Converter documentos não estruturados (PDFs escaneados, fotos) e semi-estruturados em JSON validado.
- **Funcionalidades:**
  - OCR de alta precisão (AWS Textract / Tesseract) combinado com LLM multimodal com visão.
  - Extração de campos-chave: CNPJ emitente/destinatário, valores, impostos destacados, pesos, cubagem, rotas e itens.
  - Validação cruzada automática com arquivos XML oficiais da SEFAZ (quando disponíveis).
  - Cálculo de **Score de Confiança** por campo extraído.
  - **Fila de Revisão Humana:** Itens com confiança `< 90%` são sinalizados para checagem manual por operador.

## Módulo 3 — Classificação e Padronização
- **Objetivo:** Uniformizar a taxonomia dos dados independentemente do formato ou origem do cliente.
- **Funcionalidades:**
  - Mapeamento automático de centros de custo e contas contábeis para a taxonomia padrão DHV.
  - De-duplicação de faturas e documentos por hash SHA-256 e chave de acesso NF-e/CT-e.
  - Cruzamento de dependências (ex: NF-e ↔ CT-e ↔ Comprovante de Pagamento ↔ Contrato).

## Módulo 4 — Motor de Análise e Detecção de Anomalias (Core IA)
- **Objetivo:** Identificar desvios, cobranças indevidas, riscos fiscais e ineficiências operacionais.
- **Funcionalidades:**
  - **Redução de Custos:** Identificação de fretes acima da tabela contratada, duplicidade de pagamentos, divergência de peso real vs. cubado.
  - **Compliance & Qualidade:** Verificação de CFOPs incompatíveis, ausência de retenções tributárias obrigatórias e contratos vencidos.
  - Atribuição automática de severidade (Baixa, Média, Alta, Crítica) e impacto financeiro estimado em R$.

## Módulo 5 — Benchmarking e Comparação Setorial
- **Objetivo:** Contextualizar os indicadores do cliente frente ao mercado e ao histórico DHV.
- **Funcionalidades:**
  - Base de dados comparativa segmentada por setor (varejo, farma, indústria, e-commerce) e região.
  - Cálculo do **Índice DHV** (OTIF, custo de frete por kg/km, eficiência de armazenagem).
  - Atualização contínua com base nos resultados de novos ciclos de auditoria anonimizados.

## Módulo 6 — Motor de Recomendações e Plano de Ação
- **Objetivo:** Converter achados técnicos em um plano executivo estruturado.
- **Funcionalidades:**
  - Geração automática de ações corretivas e preventivas com base na matriz Impacto x Esforço.
  - Sugestão de responsáveis, prazos e custos estimados de implementação.
  - Elaboração automática de minas de e-mail ou termos de contestação para fornecedores/transportadoras.
