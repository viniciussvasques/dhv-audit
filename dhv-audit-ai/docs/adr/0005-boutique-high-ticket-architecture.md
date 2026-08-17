# 0005: Arquitetura Boutique de Alta Al?ada (High-Ticket Proprietary Deployment)

**Status**: Aceito  
**Data**: 2026-08-17

---

## Contexto

A decis?o estrat?gica do neg?cio mudou do modelo tradicional de SaaS em massa (com milhares de assinantes de baixo valor) para um modelo de **Boutique de Elite (High-Ticket)**. O `dhv-audit-ai` ser? um software propriet?rio exclusivo, atendendo a pouqu?ssimas empresas multinacionais e de grande porte por ano, organizadas em uma r?gida **fila de espera**.

Esse perfil de cliente (faturamento bilion?rio, dezenas de milhares de funcion?rios, dados banc?rios e fiscais ultra-confidenciais) exige:
1. **Segredo de Estado Comercial:** Risco zero de vazamento de dados cont?beis ou de RH para terceiros.
2. **Infosec N?vel Banc?rio:** Clientes rejeitam bancos de dados compartilhados, mesmo com Row-Level Security (RLS) l?gico.
3. **Customiza??o Profunda:** Integra??o direta com ERPs legados altamente modificados (SAP, TOTVS/Protheus) e cria??o de regras espec?ficas.

---

## Decis?o

Migrar a estrat?gia de implanta??o de "Multi-tenant L?gico Compartilhado" para uma **Arquitetura de Isolamento F?sico de Runtime e Lan?amento Controlado (Single-Tenant Containerized Architecture)**, mantendo a flexibilidade de governan?a apenas para a console de controle interno dos consultores seniores da DHV Log.

```
                  忙式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式忖
                  弛        DHV PROPRIETARY CONTROL HUB        弛
                  弛   (Console Unificada dos Consultores)     弛
                  戌式式式式式式式式式式式式式成式式式式式式式式式式式式式式成式式式式式式式式式式式式式式戎
                                弛              弛
        忙式式式式式式式式式式式式式式式式式式式式式式式戎              戌式式式式式式式式式式式式式式式式式式式式式式式忖
        ∪ (VPC Segura Cliente A)               ∪ (VPC Segura Cliente B)
忙式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式忖      忙式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式忖
弛     CONTAINER INSTANCE A      弛      弛     CONTAINER INSTANCE B      弛
弛  - Isolated Docker Container  弛      弛  - Isolated Docker Container  弛
弛  - Dedicated App Port / Env   弛      弛  - Dedicated App Port / Env   弛
戌式式式式式式式式式式式式式式式成式式式式式式式式式式式式式式式戎      戌式式式式式式式式式式式式式式式成式式式式式式式式式式式式式式式戎
                弛                                      弛
                戌式式式式式式式式式式式式式式式成式式式式式式式式式式式式式式式式式式式式式式戎
                                ∪
               忙式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式忖
               弛    POSTGRESQL DATABASE CLUSTER  弛
               弛  - Dedicated Client Schemas     弛
               弛  - Logical Separation (Phase 1) 弛
               弛  - Physical database (Phase 2)  弛
               戌式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式戎
```

### Detalhes T?cnicos do Modelo de Implanta??o de Elite

1. **Isolamento de Runtime por Container (Docker/Kubernetes):**
   - Cada cliente aceito na fila de espera possui uma inst?ncia isolada e dedicada de cont?iner da aplica??o (`dhv-audit-ai` API + Frontend).
   - **Vantagens de Estabilidade:** Se a inst?ncia do Cliente A sofrer sobrecarga por ingest?o volumosa de XMLs ou falhas de mem?ria em parsers de IA, as inst?ncias dos outros clientes permanecem intocadas de forma ass?ncrona. Atualiza??es de software e regras customizadas podem ser aplicadas de forma isolada por cont?iner sem impactar a fila de espera.
2. **Estrat?gia H?brida de Banco de Dados (Evolu??o por Fases):**
   - **Fase 1 (MVP/Lan?amento):** Para agilizar o setup de infraestrutura, consolidar custos iniciais e simplificar migra??es, utiliza-se um ?nico cluster robusto PostgreSQL (ex: AWS RDS Aurora) com **schemas l?gicos isolados por cliente** (ex: `schema_cliente_alfa`, `schema_cliente_beta`). Isso garante isolamento estrito de dados contornando os riscos de vazamento comuns de chaves simples.
   - **Fase 2 (Escala de Alta Al?ada):** Conforme o cliente avan?a para auditorias cont?nuas permanentes e exige n?veis de conformidade de infraestrutura ainda mais severos, o banco de dados ? migrado fisicamente para uma inst?ncia de banco dedicada.
3. **O Modelo "B?nico" (Consultores Exosqueleto):**
   - O software opera como uma ferramenta de uso interno propriet?rio. Os consultores seniores da DHV usam o poder da IA para processar milh?es de dados do cliente em tempo recorde, e ent?o entram na etapa humana de revis?o antes da entrega executiva final.
4. **Integra??es de ERP sob Medida:**
   - Em vez de conectores gen?ricos, cada onboarding da fila recebe **plugins de conex?o personalizados** desenvolvidos sob demanda para buscar dados direto de bancos de dados produtivos de ERPs espec?ficos.

---

## Consequ?ncias

- **Aumento do Valor do Contrato:** O modelo de boutique com fila e escassez eleva o ticket m?dio dos projetos para m?ltiplos milh?es de reais, pagando com folga o custo operacional de inst?ncias f?sicas dedicadas.
- **Risco de Data Leak Zerado:** Atende perfeitamente aos requisitos mais severos de diretores de seguran?a (CISOs) de multinacionais.
- **Desenvolvimento sob Demanda:** Permite adaptar e programar regras sob medida para o neg?cio do cliente, garantindo que o sistema encontre at? o ?ltimo centavo.
