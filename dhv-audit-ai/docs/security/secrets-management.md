# Gest?o de Segredos & Chaves de Provedores (Secrets Management)

## 1. Princ?pios de Seguran?a e Governan?a de Credenciais
A seguran?a de chaves de API, credenciais de banco de dados e tokens de terceiros ? cr?tica para a plataforma **DHV Audit AI**, visto que o sistema processa informa??es financeiras, fiscais e estrat?gicas confidenciais.

- **Zero Hardcoding:** Nenhuma senha, chave privada, segredo ou token de API ? armazenado no c?digo-fonte ou em reposit?rios Git.
- **Isolamento de Ambiente:** Credenciais e configura??es diferem rigorosamente entre ambientes (Development, Staging, Production).

---

## 2. Configura??es por Vari?veis de Ambiente (`.env`)
No ambiente de desenvolvimento local, as chaves s?o lidas de um arquivo `.env` (n?o versionado e listado no `.gitignore`). O arquivo `.env.example` serve como template.

### Principais Vari?veis Obrigat?rias
- `DATABASE_URL`: String de conex?o segura com o PostgreSQL (usando TLS/SSL obrigat?rio em produ??o).
- `JWT_SECRET`: Chave secreta de alta entropia para assinatura dos tokens JWT.
- `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`: Chaves de acesso ao S3 e AWS Textract.
- `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`: Tokens para comunica??o segura com as IAs de extra??o e an?lise.
- `WEBHOOK_SECRET`: Chave sim?trica para assinatura de webhooks enviados aos clientes.

---

## 3. Gest?o de Segredos em Produ??o (AWS Secrets Manager / Vault)
Em ambientes de produ??o (Staging e Production), a plataforma consome credenciais diretamente de um cofre de segredos gerenciado:

1. **Inje??o Din?mica:** O cont?iner Docker da aplica??o busca os segredos de forma segura durante a inicializa??o (atrav?s do AWS Secrets Manager ou HashiCorp Vault), impedindo que segredos permane?am gravados em vari?veis de ambiente est?ticas do sistema operacional.
2. **Rota??o Autom?tica:** Chaves de banco de dados e tokens de API de provedores (como OpenAI e AWS) possuem pol?ticas de rota??o de chaves a cada 90 dias, automatizadas por meio de lambdas integradas ao Secrets Manager.

---

## 4. Auditoria de Acesso a Segredos
- Todas as solicita??es de leitura de segredos realizadas pelos microsservi?os ou servidores de aplica??o geram logs de auditoria imut?veis no servi?o de monitoramento central (ex: AWS CloudTrail).
- Alertas autom?ticos s?o disparados para a equipe de DevOps caso haja tentativas an?malas ou picos inesperados de acesso a segredos sens?veis de bancos de dados.
