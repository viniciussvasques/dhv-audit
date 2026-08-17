# Módulos M18–M23 — Inteligência Avançada

---

## M18 — Motor de Regras & Compliance Library

### Objetivo
Biblioteca centralizada de regras fiscais, operacionais e de compliance — versionadas, atualizáveis e aplicáveis por domínio.

### Arquitetura

```python
@dataclass
class Rule:
    id: str                    # "LOG-003"
    domain: str                # "logistics"
    category: str              # "cost_reduction"
    title: str
    description: str
    severity_mapping: dict     # condição → severidade
    version: str               # "2026.1"
    effective_date: date
    deprecated: bool
    cross_domain: bool         # True se cruza domínios
    related_rules: List[str]   # IDs de regras relacionadas

class RuleEngine:
    def evaluate(self, entity_graph: EntityGraph, rules: List[Rule]) -> List[Finding]: ...
```

### Biblioteca de Regras por Regulação

| Regulação | Regras | Exemplos |
|---|---|---|
| NF-e / CT-e | 45+ | CFOP inválido, valor divergente, cancelamento |
| SPED Fiscal | 30+ | EFD ICMS/IPI inconsistências |
| SPED Contribuições | 25+ | EFD PIS/COFINS créditos |
| eSocial | 20+ | Eventos obrigatórios, prazos |
| ICMS | 35+ | ST, DIFAL, créditos, alíquotas |
| ANTT | 15+ | RNTRC, tabela frete mínimo |
| CLT / Trabalhista | 25+ | Horas extras, adicional noturno |
| Lei de Licitações | 10+ | Dispensa indevida, fracionamento |

### Funcionalidades

- CRUD de regras via Admin Panel
- Versionamento (regra v2026.1 → v2026.2)
- Ativação/desativação por tenant
- Import de pacotes de regras (marketplace M27)
- Teste de regra contra dataset de exemplo

---

## M19 — Amostragem Estatística & Materialidade

### Objetivo
Aplicar metodologia estatística de auditoria profissional para extrapolação de erros.

### Funcionalidades

| Feature | Descrição |
|---|---|
| Cálculo de materialidade | Baseado em faturamento, ativos, despesas |
| Seleção de amostra | Aleatória, estratificada, por valor |
| Extrapolação | Erro na amostra → projeção para população |
| Intervalo de confiança | 95% CI para impacto total estimado |
| Amostra vs census | Decisão automática baseada em volume |

---

## M20 — Continuous Auditing

### Objetivo
Monitoramento contínuo — não apenas ciclos pontuais, mas alertas em tempo real.

### Funcionalidades

| Feature | Descrição |
|---|---|
| Ingestão contínua | Documentos processados assim que chegam |
| Alertas em tempo real | Achado crítico → notificação imediata |
| Dashboard vivo | KPIs atualizados diariamente |
| Trending | Comparativo mês a mês automático |
| Subscription model | Cliente paga mensalidade por monitoramento |

### Triggers de Alerta

```yaml
alerts:
  - rule: "BANK-002"
    condition: "transação > R$ 50.000 para CNPJ não cadastrado"
    severity: critical
    notify: ["gestor_financeiro", "consultor_dhv"]
    channel: ["email", "push", "dashboard"]

  - rule: "LOG-FIN-003"
    condition: "frete pago em duplicidade"
    severity: high
    notify: ["consultant_assigned"]
    channel: ["dashboard", "workflow"]
```

---

## M21 — Fraud Detection & Forensics

### Objetivo
Detectar padrões de fraude usando análise estatística e grafos de relacionamento.

### Técnicas

| Técnica | Aplicação |
|---|---|
| Lei de Benford | Distribuição anômala de primeiros dígitos em valores |
| Análise de grafos | Fornecedor conectado a múltiplos CNPJs do grupo |
| Duplicatas | Mesmo valor, mesma data, beneficiários diferentes |
| Outlier detection | Valores estatisticamente improváveis |
| Pattern matching | Sequências suspeitas (saque → transferência → saque) |
| Shell companies | CNPJ recém-criado, endereço compartilhado, sócio em comum |

---

## M22 — Data Analytics Engine

### Objetivo
Permitir consultores executarem análises ad-hoc sobre datasets do engagement (similar a ACL/IDEA).

### Funcionalidades

| Feature | Descrição |
|---|---|
| Query builder visual | Filtros, joins, agrupamentos sem SQL |
| Scripts Python sandbox | Análises customizadas em ambiente isolado |
| Export para Excel | Resultados exportáveis |
| Templates de análise | Análises pré-configuradas por domínio |
| Comparação de períodos | Jan/2026 vs Jan/2025 side-by-side |

---

## M23 — AI Governance & Feedback Loop

### Objetivo
Garantir que a IA melhore continuamente com feedback dos consultores.

### Funcionalidades

| Feature | Descrição |
|---|---|
| Feedback loop | Consultor valida/rejeita → ajusta modelo |
| Versionamento de prompts | Prompt v3.2 → v3.3 com changelog |
| Explicabilidade | "Por que a IA flagou isso?" com reasoning chain |
| Custo tracking | Quanto cada engagement gastou em LLM calls |
| A/B testing | Testar regra nova vs regra atual |
| Bias detection | Verificar se IA favorece/prejudica algum padrão |
| Confidence calibration | Ajustar scores baseado em histórico de acertos |

### Ciclo de Melhoria

```
IA detecta achado (confidence: 0.85)
    → Consultor valida ✅ → reforça padrão (confidence futuro: 0.92)
    → Consultor rejeita ❌ → ajusta regra (confidence futuro: 0.70)
    → Após 100 feedbacks → recalibração automática do modelo
```
