# Documentação Técnica — DHV Audit AI Platform

**Versão:** 2.0.0  
**Status:** Especificação Aprovada  
**Última atualização:** 2026-08-16

---

## Visão do Produto

O **DHV Audit AI** não é apenas um sistema de auditoria documental. É uma **plataforma operacional completa** que:

1. **Ingesta** dados de múltiplas fontes (documentos, ERPs, bancos, SPED, eSocial)
2. **Analisa** com IA + regras determinísticas + benchmark proprietário
3. **Cruza** informações entre domínios (RH × Financeiro × Logística × Compras)
4. **Aponta exatamente** onde agir, o que fazer, quanto economizar e como padronizar
5. **Opera** a firma de auditoria (contratos, engajamentos, workpapers, follow-up)

> **Proposta de Valor:** *"Suba os documentos e conecte suas contas. A plataforma mostra onde você perde dinheiro, o que corrigir e como padronizar — com evidência rastreável e validação humana DHV."*

---

## Índice da Documentação

### Arquitetura
| Documento | Descrição |
|---|---|
| [Visão Geral do Sistema](./architecture/system-overview.md) | Objetivos, princípios e camadas |
| [Estrutura de Pastas](./architecture/folder-structure.md) | Monorepo backend + frontend |
| [Fluxo de Dados](./architecture/data-flow.md) | Pipeline ponta a ponta |
| [Inteligência Cruzada](./architecture/cross-module-intelligence.md) | Cruzamento entre domínios |
| [Diagramas C4](./architecture/c4-diagrams.md) | Contexto, contêineres, componentes |
| [Base RAG Inteligente](./architecture/rag-knowledge-base.md) | Arquitetura RAG e busca semântica |

### Decisões Arquiteturais (ADRs)
| ADR | Decisão |
|---|---|
| [0001](./adr/0001-clean-architecture-and-fastapi-stack.md) | Clean Architecture + FastAPI |
| [0002](./adr/0002-tech-stack-and-language-decision.md) | Stack completa (Python + TypeScript) |
| [0003](./adr/0003-multi-tenant-architecture.md) | Isolamento multi-tenant |
| [0004](./adr/0004-modular-monolith-strategy.md) | Monólito modular |
| [0005](./adr/0005-boutique-high-ticket-architecture.md) | Arquitetura de deploy proprietário de elite |

### Estratégia de Negócios e Escassez
| Documento | Descrição |
|---|---|
| [Modelo Boutique & Fila de Espera](./strategy/boutique-consulting.md) | Modelo operacional de escassez, deployments privados dedicados e blindagem jurídica |
| [Apresentação Comercial de Elite](./strategy/executive-pitch-deck.md) | Apresentação executiva comercial do modelo HAQL sem exposição do código |

### Módulos Funcionais
| Documento | Módulos |
|---|---|
| [Visão Geral](./modules/modules-overview.md) | Índice de todos os módulos (M1–M28) |
| [Core Pipeline M1–M6](./modules/module-01-to-06.md) | Ingestão → Recomendações |
| [Entrega & Governança M7–M11](./modules/module-07-to-11.md) | Dashboard → LGPD |
| [Operação da Firma M12–M17](./modules/module-12-to-17-operacao-firma.md) | CRM, workflow, workpapers |
| [Inteligência Avançada M18–M23](./modules/module-18-to-23-inteligencia.md) | Regras, fraude, analytics |
| [Plataforma & Escala M24–M28](./modules/module-24-to-28-plataforma.md) | Portal, integrações, marketplace |

### Domínios de Auditoria
| Domínio | Documento |
|---|---|
| Logística & Frete | [domain-logistics.md](./modules/domains/domain-logistics.md) |
| RH & Folha | [domain-hr.md](./modules/domains/domain-hr.md) |
| Compras & Procurement | [domain-procurement.md](./modules/domains/domain-procurement.md) |
| Financeiro & Bancos | [domain-financial.md](./modules/domains/domain-financial.md) |
| Fiscal & Tributário | [domain-fiscal-tax.md](./modules/domains/domain-fiscal-tax.md) |
| Frota & TMS | [domain-fleet.md](./modules/domains/domain-fleet.md) |

### API
| Documento | Descrição |
|---|---|
| [Visão Geral da API](./api/api-overview.md) | Convenções REST, versionamento |
| [Admin API](./api/admin-api.md) | Painel administrativo |
| [Webhooks & Eventos](./api/webhooks-events.md) | Integrações assíncronas |

### Interface (UI/UX)
| Documento | Descrição |
|---|---|
| [Design System](./ui/design-system.md) | Componentes, tokens, padrões |
| [Painel Admin](./ui/admin-panel.md) | Gestão da plataforma |
| [Portal do Cliente](./ui/client-portal.md) | Self-service empresarial |
| [Workspace Consultor](./ui/consultant-workspace.md) | Operação de auditoria |

### Banco de Dados
| Documento | Descrição |
|---|---|
| [Schema Overview](./database/schema-overview.md) | Entidades principais |
| [Relacionamentos](./database/entity-relationships.md) | ERD e cardinalidades |

### Contratos & Documentos Legais
| Documento | Descrição |
|---|---|
| [Geração de Documentos](./contracts/legal-documents.md) | Contratos, NDAs, propostas |

### Metodologia de Auditoria
| Documento | Descrição |
|---|---|
| [Metodologia Zero-Waste](./methodology/zero-waste-audit.md) | Auditoria centavo a centavo, eficiência de frotas, consumíveis e motor de perfilamento de recursos (MPE-IR) |
| [Fundamentação e Literatura Científica](./methodology/literature-references.md) | Normas mundiais (COSO, ISA/NBC, Benford, Continuous Audit de Rutgers) |
| [Reestruturação e Consultoria 360](./methodology/corporate-restructuring.md) | Consultoria estratégica, retenção de talentos-chave, bônus, e simulações antes/depois |
| [Eficiência Interna da Firma (LBE-Audit)](./modules/internal-audit-operations.md) | Princípio 'Lead-by-Example', auditoria de timesheets dos consultores e bônus por savings capturados |

### Segurança
| Documento | Descrição |
|---|---|
| [Auth & RBAC](./security/auth-rbac.md) | Autenticação e permissões |
| [Gestão de Segredos](./security/secrets-management.md) | Chaves de provedores |

### Plano Mestre
| Documento | Descrição |
|---|---|
| [Master Plan](./master-plan.md) | Roadmap executivo e fases |
