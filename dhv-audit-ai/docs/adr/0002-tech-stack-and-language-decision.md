# 0002: Decisão de Stack Tecnológica e Linguagens

**Status**: Aceito  
**Data**: 2026-08-16  
**Decisores**: Equipe de Arquitetura DHV

---

## Contexto

A plataforma DHV Audit AI precisa processar documentos (OCR), executar análises com IA (LLMs), cruzar dados de múltiplos domínios, gerar relatórios e operar uma interface web completa com 3 frontends distintos (Admin, Cliente, Consultor). Precisamos definir a stack ideal para maximizar produtividade, ecossistema de IA e qualidade de engenharia.

---

## Decisão

### Backend: Python 3.11+

| Critério | Justificativa |
|---|---|
| Ecossistema IA/ML | Dominante: OpenAI SDK, LangChain, pandas, scikit-learn |
| OCR & NLP | Bibliotecas maduras: Tesseract, spaCy, PyPDF2, lxml |
| Parsing fiscal BR | XML NF-e/CT-e, SPED, eSocial — libs Python abundantes |
| FastAPI | Async nativo, Pydantic v2, OpenAPI automático |
| Produtividade | Clean Architecture bem estabelecida em Python |
| Contratação | Pool de devs Python/ML no mercado BR |

### Frontend: TypeScript + Next.js 14+ (App Router)

| Critério | Justificativa |
|---|---|
| Type Safety | TypeScript previne bugs em UI complexa |
| SSR/SSG | Performance e SEO para portal cliente |
| App Router | Layouts aninhados (admin/client/consultant) |
| Ecossistema | shadcn/ui, TanStack Query, Recharts |
| Monorepo | Compartilhar types com backend via OpenAPI codegen |

### Banco de Dados: PostgreSQL 15+

| Critério | Justificativa |
|---|---|
| Multi-tenant | Row-Level Security (RLS) nativo (camada interna para filiais de holdings) |
| JSONB | Grafo de entidades, metadados flexíveis |
| Full-text search | Busca em documentos e achados |
| Extensões | pgvector (embeddings RAG), pg_trgm (fuzzy match) |
| Maturidade | Padrão de mercado para sistemas corporativos de alta criticidade e alta alçada |

### Fila & Cache: Redis 7+

| Uso | Detalhe |
|---|---|
| Filas | Celery ou ARQ para jobs assíncronos |
| Cache | Sessions, resultados de benchmark |
| Rate limiting | Proteção de API e LLM calls |
| Pub/Sub | Eventos em tempo real (WebSocket) |

### Storage: S3-compatible (AWS S3 / MinIO)

| Uso | Detalhe |
|---|---|
| Documentos originais | Imutáveis, versionados |
| Relatórios gerados | PDF, PPTX, XLSX |
| Contratos assinados | PDF com hash de integridade |

### IA & OCR: Abstração Multi-Provedor

```
┌─────────────────────────────────┐
│     AI Provider Abstraction     │
├─────────────────────────────────┤
│  LLMProvider (interface)        │
│  ├── OpenAIProvider             │
│  ├── AnthropicProvider          │
│  └── AzureOpenAIProvider        │
│                                 │
│  OCRProvider (interface)        │
│  ├── AWSTextractProvider        │
│  ├── TesseractProvider          │
│  └── LLMVisionProvider          │
└─────────────────────────────────┘
```

Chaves gerenciadas no Admin Panel (M10), nunca hardcoded.

---

## Stack Completa

| Camada | Tecnologia | Versão |
|---|---|---|
| Linguagem Backend | Python | 3.11+ |
| Framework API | FastAPI | 0.110+ |
| Validação | Pydantic | v2 |
| ORM | SQLAlchemy | 2.0+ |
| Migrações | Alembic | 1.13+ |
| Filas | Celery + Redis | — |
| Linguagem Frontend | TypeScript | 5.0+ |
| Framework Frontend | Next.js | 14+ |
| UI Components | shadcn/ui + Tailwind CSS | — |
| State Management | TanStack Query | v5 |
| Charts | Recharts | — |
| Banco | PostgreSQL | 15+ |
| Cache/Filas | Redis | 7+ |
| Storage | AWS S3 / MinIO | — |
| Containerização | Docker + Compose | — |
| CI/CD | GitHub Actions | — |
| Lint Backend | Ruff | — |
| Type Check Backend | Mypy | — |
| Lint Frontend | ESLint + Prettier | — |
| Testes Backend | Pytest + coverage | ≥ 80% |
| Testes Frontend | Vitest + Playwright | — |
| Docs API | OpenAPI 3.1 (auto) | — |

---

## Consequências

### Positivas
- Python é a linguagem #1 para IA/ML — integração natural com LLMs e OCR
- TypeScript no frontend garante type safety em UI complexa com 3 portais
- PostgreSQL com RLS resolve multi-tenant de forma robusta
- FastAPI gera OpenAPI → codegen TypeScript automático
- Modular monolith permite evoluir para microserviços se necessário

### Negativas
- Duas linguagens (Python + TypeScript) — requer times com skills distintas
- Celery adiciona complexidade operacional (mitigado com ARQ como alternativa mais simples)
- Next.js SSR requer infra Node.js além do Python

### Mitigações
- OpenAPI codegen sincroniza types entre backend e frontend
- Docker Compose unifica ambiente de dev
- Monorepo com Makefile unifica comandos (`make dev` sobe tudo)
