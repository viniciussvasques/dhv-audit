# 0001: Adoção de Clean Architecture e FastAPI para o Core da Plataforma

**Status**: Aceito

**Contexto**:  
A Plataforma DHV Audit AI processa documentos complexos (faturas, XMLs fiscais, folhas de pagamento), executa regras de negócio rigorosas e integra modelos de IA (LLMs e OCR). Precisamos de uma arquitetura que garanta manutenibilidade, testabilidade, isolamento de domínios e facilidade de evolução sem acoplamento a frameworks externos ou bancos de dados específicos.

**Decisão**:  
1. Adotar **Clean Architecture** (camadas: Domain, Application, Interfaces, Infrastructure) com estrita regra de dependência apontando para o centro (Domain).
2. Utilizar **FastAPI** (Python 3.11+) como framework web/API pelo suporte nativo a operações assíncronas, validação rigorosa de dados via Pydantic e geração automática de documentação OpenAPI.
3. Utilizar **PostgreSQL** com isolamento multi-tenant por schema/tenant_id para dados estruturados, e **AWS S3** (ou armazenamento compativel) para arquivos originais.

**Consequências**:  
- **Positivas:** Domínio de negócio 100% isolado de detalhes de infraestrutura; testes unitários rápidos e sem dependência de banco de dados; forte tipagem e contratos claros de DTOs.
- **Negativas:** Curva inicial de boilerplate e mapeamento entre modelos de domínio, DTOs de aplicação e models ORM.
- **Mitigação:** Uso de padrões claros de repositório e injeção de dependências nativa do FastAPI.
