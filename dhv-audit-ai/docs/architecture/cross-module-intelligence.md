# Inteligência Cruzada — Cross-Module Analysis

## 1. Objetivo

O diferencial competitivo da plataforma DHV Audit AI está na capacidade de **cruzar dados entre domínios** para detectar inconsistências, fraudes e oportunidades de economia que nenhum módulo isolado conseguiria identificar.

---

## 2. Modelo de Grafo de Entidades

Toda informação ingerida é normalizada em um **grafo de entidades** que permite cruzamento:

```
┌──────────┐     emitiu      ┌──────────┐
│  CNPJ    │───────────────▶│ Documento │
│(Empresa) │                 │ (NF/CT-e) │
└────┬─────┘                 └────┬─────┘
     │                            │
     │ emprega                    │ referencia
     ▼                            ▼
┌──────────┐     pagou       ┌──────────┐
│Funcionário│◀───────────────│ Pagamento │
└──────────┘                 └────┬─────┘
                                  │
                                  │ debitou
                                  ▼
                            ┌──────────┐
                            │Conta     │
                            │Bancária  │
                            └──────────┘
```

### Entidades do Grafo

| Entidade | Atributos-chave | Fontes |
|---|---|---|
| **Company (CNPJ)** | razão social, filiais, setor | Cadastro, NF-e, SPED |
| **Document** | tipo, valor, data, hash | Upload, XML, OCR |
| **Payment** | valor, data, beneficiário, conta | Extrato, AP, OFX |
| **Employee** | CPF, cargo, centro custo, salário | Folha, eSocial |
| **Contract** | fornecedor, vigência, tabela preços | Upload, cadastro |
| **BankAccount** | banco, agência, conta, titular | Open Banking, OFX |
| **CostCenter** | código, departamento, budget | ERP, planilha |
| **Supplier** | CNPJ, categoria, histórico preços | NF-e, cotações |

### Relacionamentos

| Relação | De → Para | Exemplo |
|---|---|---|
| `EMITTED` | CNPJ → Document | Fornecedor emitiu NF-e |
| `PAID` | Payment → Document | Pagamento referencia NF |
| `EMPLOYS` | CNPJ → Employee | Empresa emprega funcionário |
| `DEBITED` | Payment → BankAccount | Débito em conta |
| `GOVERNS` | Contract → CNPJ | Contrato com transportadora |
| `SHIPPED` | Document(CT-e) → Document(NF-e) | Frete da nota fiscal |
| `QUOTED` | Supplier → Document | Cotação de fornecedor |
| `ALLOCATED` | Document → CostCenter | Despesa alocada |

---

## 3. Regras de Cruzamento Cross-Domain

### 3.1 Logística × Financeiro

| Regra | Descrição | Impacto |
|---|---|---|
| `LOG-FIN-001` | CT-e faturado sem NF-e vinculada | Frete fantasma |
| `LOG-FIN-002` | Pagamento de frete > valor CT-e | Pagamento a maior |
| `LOG-FIN-003` | Frete pago 2× (mesmo CT-e, contas diferentes) | Duplicidade |
| `LOG-FIN-004` | Frete pago após cancelamento CT-e | Pagamento indevido |

### 3.2 Compras × Financeiro

| Regra | Descrição | Impacto |
|---|---|---|
| `COMP-FIN-001` | NF-e de compra sem pagamento correspondente | Passivo não registrado |
| `COMP-FIN-002` | Pagamento sem NF-e (sem nota) | Risco fiscal |
| `COMP-FIN-003` | Preço pago > preço cotado | Sobrepagamento |
| `COMP-FIN-004` | Mesmo fornecedor, CNPJs diferentes, mesmos produtos | Fraude |

### 3.3 RH × Financeiro

| Regra | Descrição | Impacto |
|---|---|---|
| `RH-FIN-001` | Salário pago ≠ folha calculada | Erro folha |
| `RH-FIN-002` | Reembolso funcionário sem comprovante | Despesa irregular |
| `RH-FIN-003` | Funcionário em 2 centros de custo simultaneamente | Alocação incorreta |
| `RH-FIN-004` | Pagamento rescisão sem registro eSocial | Compliance |

### 3.4 Fiscal × Logística × Compras

| Regra | Descrição | Impacto |
|---|---|---|
| `FISC-LOG-001` | CFOP incompatível com operação de frete | Risco fiscal |
| `FISC-COMP-001` | Crédito ICMS não aproveitado em compra | Perda tributária |
| `FISC-RH-001` | Retenção IRRF/INSS não efetuada em NF serviço | Autuação |

### 3.5 Contas Bancárias × Todos

| Regra | Descrição | Impacto |
|---|---|---|
| `BANK-001` | Transação bancária sem documento fiscal | Pagamento sem lastro |
| `BANK-002` | Saque/transferência para CNPJ não cadastrado | Risco fraude |
| `BANK-003` | Conciliação bancária divergente > R$ 1.000 | Erro contábil |
| `BANK-004` | Pagamento recorrente sem contrato vigente | Despesa não autorizada |

---

## 4. Motor de Cruzamento — Arquitetura

```
┌─────────────────────────────────────────────────┐
│              Cross-Domain Analysis Engine        │
├─────────────────────────────────────────────────┤
│  1. Entity Resolution (unificar CNPJs, nomes)   │
│  2. Graph Builder (montar grafo do engagement)  │
│  3. Rule Executor (regras cross-domain)         │
│  4. Pattern Matcher (ML: anomalias em grafo)    │
│  5. Impact Calculator (R$ por achado)           │
│  6. Action Recommender (o que fazer)            │
└─────────────────────────────────────────────────┘
```

---

## 5. Output: Prescrição de Ação

Cada achado cross-domain inclui **prescrição completa**:

```yaml
finding:
  id: "CROSS-2026-00421"
  type: "cross_domain"
  domains: ["logistics", "financial"]
  rule: "LOG-FIN-003"
  title: "Frete pago em duplicidade — CT-e 123456"
  severity: critical
  financial_impact: 12500.00
  confidence: 0.98

  evidence_chain:
    - entity: "CT-e 123456"
      source: "document/cte-123456.xml"
      field: "valor_frete"
      value: 6250.00
    - entity: "Pagamento #1"
      source: "bank/extrato-jan-2026.ofx"
      date: "2026-01-15"
      value: 6250.00
      beneficiary: "Transportadora XYZ"
    - entity: "Pagamento #2"
      source: "bank/extrato-fev-2026.ofx"
      date: "2026-02-03"
      value: 6250.00
      beneficiary: "Transportadora XYZ LTDA"

  prescription:
    immediate:
      - action: "Solicitar estorno de R$ 6.250,00 à Transportadora XYZ"
        template: "contestacao_duplicidade_frete.docx"
        owner: "Gestor Financeiro"
        deadline: 10 dias
    preventive:
      - action: "Implementar conferência CT-e × pagamento antes de liberar no AP"
        process: "PROC-FIN-008"
        owner: "Controller"
        deadline: 30 dias
    standardization:
      - action: "Cadastrar regra automática: bloquear pagamento se CT-e já pago"
        module: "workflow"
        owner: "TI / ERP"
        deadline: 45 dias
```

---

## 6. Visualização para Consultor

O **Consultant Workspace** exibe o grafo interativo:

- Nós coloridos por domínio (logística=azul, financeiro=verde, RH=laranja)
- Arestas destacadas onde há achado
- Click no achado → cadeia de evidências completa
- Filtro por domínio, severidade, valor mínimo
