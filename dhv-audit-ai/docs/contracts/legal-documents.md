# Gera??o de Documentos Legais & Gest?o de Contratos

## 1. Vis?o Geral
Este m?dulo gerencia a cria??o, valida??o e governan?a de todos os documentos jur?dicos e comerciais gerados pela plataforma. Ele abrange desde a fase comercial (propostas, NDAs) at? a fase operacional (contratos de auditoria, termos de contesta??o de frete e notifica??es de glosa para fornecedores).

---

## 2. Tipos de Documentos Suportados

### A. Acordo de Confidencialidade (NDA - Non-Disclosure Agreement)
*   **Finalidade:** Garantir a seguran?a jur?dica antes do compartilhamento de dados sens?veis e documentos fiscais pelo cliente.
*   **Gera??o:** Automatizada com base no CNPJ do cliente e dados dos representantes legais consultados via API da Receita Federal.

### B. Proposta Comercial de Engajamento
*   **Finalidade:** Formalizar o escopo da auditoria, prazos de execu??o, limites de amostragem e percentual de comiss?o (*success fee*) sobre os desvios financeiros identificados.
*   **Vari?veis:** M?dulos ativados, faturamento auditado, limite de escopo de datas e al?quotas de sucesso.

### C. Contrato de Presta??o de Servi?os de Auditoria
*   **Finalidade:** Contrato mestre (*Service Level Agreement* - SLA) que define responsabilidades, penalidades, regras de prote??o de dados (LGPD) e o escopo t?cnico do trabalho.

### D. Notifica??o de Glosa / Termo de Contesta??o
*   **Finalidade:** Documentos enviados aos fornecedores e transportadoras contestando cobran?as indevidas de frete ou pre?os de produtos discrepantes identificados pela IA.
*   **Funcionalidade:** Preenchimento autom?tico com a lista de notas/CT-es auditados com anomalias e c?lculo do montante glosado anexado como evid?ncia inquestion?vel.

---

## 3. Arquitetura da Camada de Gera??o de Documentos

```
忙式式式式式式式式式式式式式式式式式式式式式式式式忖      忙式式式式式式式式式式式式式式式式式式式式式式式式忖
弛     Dados do ERP /     弛      弛   Biblioteca de        弛
弛    Formul?rio Web      弛      弛 Templates (Markdown)   弛
戌式式式式式式式式式式式成式式式式式式式式式式式式戎      戌式式式式式式式式式式式成式式式式式式式式式式式式戎
            弛                               弛
            戌式式式式式式式式式式式式式式式成式式式式式式式式式式式式式式式戎
                            ∪
               忙式式式式式式式式式式式式式式式式式式式式式式式式式忖
               弛  Motor de Templates     弛
               弛  (Jinja2 / Variable Sub)弛
               戌式式式式式式式式式式式式成式式式式式式式式式式式式戎
                            ∪
               忙式式式式式式式式式式式式式式式式式式式式式式式式式忖
               弛    Conversor PDF        弛
               弛 (WeasyPrint / Playwright)弛
               戌式式式式式式式式式式式式成式式式式式式式式式式式式戎
                            ∪
               忙式式式式式式式式式式式式式式式式式式式式式式式式式忖
               弛    Assinatura Digital   弛
               弛 (DocuSign / Clicksign)  弛
               戌式式式式式式式式式式式式式式式式式式式式式式式式式戎
```

### A. Biblioteca de Templates
Todos os contratos e termos s?o mantidos em formato de markdown parametriz?vel com vari?veis no padr?o `{{variavel}}`. O sistema possui um hist?rico de vers?es de templates para garantir que contratos antigos continuem utilizando seus respectivos layouts originais.

### B. Convers?o e Gera??o de PDF
- **Tecnologia:** Uso do `WeasyPrint` ou `Playwright` para converter HTML gerado a partir do Markdown para PDFs formatados com o estilo corporativo da DHV Log (CSS Paged Media).
- **Metadados:** Inclus?o de hash SHA-256 no rodap? de todas as p?ginas para garantir a integridade documental e impedir adultera??es em PDFs assinados.

---

## 4. Integra??o de Assinatura Digital e Fluxo de Valida??o
1. **Disparo do Fluxo:** Ao concluir a revis?o de uma proposta ou contrato, o consultor clica em "Enviar para Assinatura".
2. **APIs Externas:** A plataforma consome webhooks das principais integradoras de assinatura digital (DocuSign, Clicksign ou assinatura gov.br via padr?o ICP-Brasil).
3. **Escuta de Eventos:** O sistema recebe callbacks notificando altera??es de status: `sent` (enviado), `opened` (visualizado), `signed` (assinado) e `completed` (conclu?do por todas as partes).
4. **Armazenamento Seguro:** Ap?s a conclus?o, o arquivo final assinado e o manifesto de assinaturas s?o arquivados no S3 e criptografados em repouso. O status do engajamento de auditoria avan?a automaticamente para "Ativo".

---

## 5. Auditoria de Assinaturas e Compliance (Trilha de Auditoria)
Toda intera??o em um contrato gera uma entrada imut?vel na trilha de auditoria:
- Endere?o IP do signat?rio.
- Registro de data e hora UTC.
- Dispositivo e geolocaliza??o aproximada.
- C?digo hash do documento associado ? transa??o de assinatura.
- Status de conformidade do contrato em rela??o ?s regras da LGPD (Consentimento expl?cito para processamento de dados confidenciais de terceiros).
