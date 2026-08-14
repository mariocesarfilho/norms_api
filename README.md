# API de Atos Normativos da Receita Federal

API REST desenvolvida com FastAPI para coletar e gerenciar atos normativos publicados no portal da Receita Federal. A aplicação consulta a página pública por HTTP, interpreta a tabela de resultados com BeautifulSoup e persiste as normas em PostgreSQL.

O projeto oferece CRUD de normas, criação de usuários, autenticação JWT, sincronização protegida com prevenção de duplicidades por `source_id`, dashboard com filtros e documentação OpenAPI. O banco pode ser executado localmente ou junto com a API por Docker Compose.

## 1. Funcionalidades

- coleta de normas no portal público da Receita Federal;
- requisição HTTP com `urllib` e parsing com BeautifulSoup;
- persistência síncrona em PostgreSQL com SQLAlchemy e Psycopg;
- migrations de banco com Alembic;
- criação, consulta, atualização e exclusão de normas;
- criação de usuários e armazenamento de senha com hash;
- autenticação por JWT Bearer;
- proteção das operações de escrita e sincronização;
- sincronização com prevenção de duplicidades por `source_id`;
- dashboard com filtro por data de publicação e pesquisa textual;
- documentação automática em Swagger UI, ReDoc e OpenAPI;
- execução local ou com Docker e Docker Compose.

## 2. Tecnologias utilizadas

| Tecnologia | Uso no projeto |
|---|---|
| Python 3.12 | Linguagem e versão-base da imagem Docker |
| FastAPI | API REST, injeção de dependências e OpenAPI |
| Uvicorn | Servidor ASGI |
| SQLAlchemy 2 | Models, consultas e sessões síncronas |
| PostgreSQL | Banco de dados relacional |
| Psycopg 3 | Driver PostgreSQL instalado pelo projeto |
| Alembic | Controle e aplicação das migrations |
| Pydantic / pydantic-settings | Schemas e leitura do `.env` |
| PyJWT | Emissão e validação dos tokens JWT |
| pwdlib com Argon2 | Hash e verificação de senhas |
| BeautifulSoup 4 | Leitura da tabela de atos no HTML |
| urllib | Requisição HTTP ao portal da Receita Federal |
| Docker | Imagem da API baseada em `python:3.12-slim` |
| Docker Compose | Orquestração da API e do PostgreSQL 17 |

As versões e os intervalos aceitos estão em [`requirements.txt`](requirements.txt).

## 3. Estrutura do projeto

```text
norms_api/
├── app/
│   ├── api/
│   │   ├── dependencies/
│   │   │   └── auth.py
│   │   └── routes/
│   │       ├── auth_router.py
│   │       ├── dashboard_router.py
│   │       ├── norm_router.py
│   │       └── user_router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── exception_handlers.py
│   │   └── security.py
│   ├── infra/
│   │   └── database.py
│   ├── models/
│   │   ├── norm_model.py
│   │   └── user_model.py
│   ├── repositories/
│   │   ├── norm_repository.py
│   │   └── user_repository.py
│   ├── schemas/
│   │   ├── dashboard.py
│   │   ├── login.py
│   │   ├── norm.py
│   │   └── user.py
│   ├── scrapers/
│   │   └── federal_revenue_scraper.py
│   └── services/
│       ├── dashboard_service.py
│       ├── norm_service.py
│       └── user_service.py
├── alembic/
│   ├── versions/
│   └── env.py
├── .dockerignore
├── .env.example
├── alembic.ini
├── compose.yaml
├── Dockerfile
├── main.py
└── requirements.txt
```

| Diretório | Responsabilidade |
|---|---|
| `app/api` | Rotas HTTP e dependências do FastAPI |
| `app/core` | Configuração, JWT, senhas e tratamento global de erros |
| `app/infra` | Engine SQLAlchemy e ciclo de vida das sessões |
| `app/models` | Mapeamento das tabelas PostgreSQL |
| `app/repositories` | Consultas e operações de persistência |
| `app/schemas` | Contratos de entrada e saída da API |
| `app/scrapers` | Integração HTTP e parsing do portal da Receita Federal |
| `app/services` | Regras de negócio e coordenação entre camadas |
| `alembic` | Configuração e histórico de migrations |
| `.dockerignore` | Exclui arquivos locais, sensíveis e desnecessários do contexto de build Docker |

## 4. Pré-requisitos

### Execução local

- Git;
- Python 3.12 com `venv` e `pip`;
- PostgreSQL em execução;
- acesso de rede ao portal da Receita Federal para a sincronização;
- VS Code, opcionalmente, para usar o terminal integrado.

### Execução com Docker

- Git;
- Docker Desktop no Windows ou macOS; ou
- Docker Engine com o plugin Docker Compose no Linux.

Ao usar Docker Compose, não é necessário instalar PostgreSQL nem Python no host. As portas `8000` e `5432` precisam estar disponíveis porque são publicadas pelo arquivo `compose.yaml`.

Execute os comandos deste documento na raiz do repositório.

## 5. Clonando o projeto

Por HTTPS:

```bash
git clone https://github.com/mariocesarfilho/norms_api.git
cd norms_api
```

Se o acesso SSH ao GitHub já estiver configurado:

```bash
git clone git@github.com:mariocesarfilho/norms_api.git
cd norms_api
```

## 6. Configuração local sem Docker

### Windows — PowerShell

Crie o ambiente virtual:

```powershell
py -3.12 -m venv .venv
```

Ative-o:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se a política do PowerShell bloquear o script, libere a execução somente para o processo atual e tente novamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS

Com o Python 3.12 já instalado:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se `python3.12` não for reconhecido, instale o Python 3.12 antes de continuar. O projeto não depende de Anaconda.

Para confirmar o interpretador ativo em qualquer sistema:

```bash
python -c "import sys; print(sys.executable)"
```

O caminho exibido deve apontar para a pasta `.venv` deste projeto.

## 7. Variáveis de ambiente

Crie o arquivo `.env` a partir do exemplo.

No Windows:

```powershell
Copy-Item .env.example .env
```

No Linux ou macOS:

```bash
cp .env.example .env
```

Edite o novo arquivo e substitua os valores ilustrativos. Uma configuração compatível com execução local e Docker é:

```env
JWT_SECRET_KEY=substitua-por-uma-chave-longa-e-aleatoria
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE=30

DATABASE_URL=postgresql+psycopg://norms_user:troque-esta-senha@localhost:5432/norms_db

POSTGRES_USER=norms_user
POSTGRES_PASSWORD=troque-esta-senha
POSTGRES_DB=norms_db
```

Uma chave JWT pode ser gerada com a biblioteca-padrão do Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

| Variável | Uso |
|---|---|
| `DATABASE_URL` | Conexão usada pela aplicação local e pelo Alembic. É obrigatória no `Settings`; dentro do Compose ela é substituída por uma URL com hostname `db`. |
| `JWT_SECRET_KEY` | Segredo usado para assinar e validar JWTs. É obrigatório. |
| `JWT_ALGORITHM` | Algoritmo JWT. O padrão da aplicação é `HS256`, mas o Compose espera a variável preenchida. |
| `JWT_ACCESS_TOKEN_EXPIRE` | Tempo de validade do token em minutos. O padrão da aplicação é `30`, mas o Compose espera a variável preenchida. |
| `POSTGRES_USER` | Usuário criado no contêiner PostgreSQL. Usado pelo Compose. |
| `POSTGRES_PASSWORD` | Senha do usuário do PostgreSQL no Compose. |
| `POSTGRES_DB` | Banco criado pelo contêiner PostgreSQL. |

Use `postgresql+psycopg://` na `DATABASE_URL`. O projeto instala Psycopg 3; uma URL iniciada apenas por `postgresql://` pode fazer o SQLAlchemy procurar o driver `psycopg2`, que não está listado nas dependências.

O `.env` está no `.gitignore` e não deve ser commitado. O `.env.example` deve permanecer versionado apenas com valores ilustrativos. Troque `JWT_SECRET_KEY` e as senhas antes de usar a aplicação fora de um ambiente local.

## 8. PostgreSQL para execução local

Sem Docker, mantenha um servidor PostgreSQL acessível pelo endereço configurado na `DATABASE_URL`. O exemplo abaixo cria os mesmos usuário e banco usados no exemplo de `.env`:

```bash
psql -U postgres
```

No console do PostgreSQL:

```sql
CREATE USER norms_user WITH PASSWORD 'troque-esta-senha';
CREATE DATABASE norms_db OWNER norms_user;
\q
```

A URL local correspondente é:

```text
postgresql+psycopg://norms_user:troque-esta-senha@localhost:5432/norms_db
```

Usuário, senha, porta e banco podem ser diferentes, desde que a `DATABASE_URL` seja atualizada com os mesmos valores. Se a senha contiver caracteres reservados de URL, codifique-os antes de incluí-la na URL de conexão.

## 9. Alembic e migrations

Com o ambiente virtual ativo, o `.env` configurado e o PostgreSQL disponível, aplique todas as migrations:

```bash
alembic upgrade head
```

Também é possível garantir o uso do Alembic instalado na `.venv`:

```bash
python -m alembic upgrade head
```

O projeto possui a seguinte cadeia de migrations:

1. criação da tabela `norms`;
2. criação da tabela `users`;
3. adição de `source_id` à tabela `norms`, com índice único.

O `alembic/env.py` usa `DATABASE_URL` em vez do placeholder de `alembic.ini`. Como as configurações da aplicação são carregadas na inicialização, mantenha no `.env` as variáveis obrigatórias definidas em `app/core/config.py`, incluindo as configurações de banco e JWT.

Para conferir o estado atual:

```bash
python -m alembic current
python -m alembic history
```

Ao alterar os models durante o desenvolvimento:

```bash
python -m alembic revision --autogenerate -m "descricao da migration"
python -m alembic upgrade head
```

Alembic é o mecanismo adotado pelo projeto para evoluir o schema. Não é necessário chamar `Base.metadata.create_all()`.

## 10. Executando a aplicação localmente

Na raiz do projeto, com a `.venv` ativa:

```bash
uvicorn main:app --reload
```

Alternativamente:

```bash
python -m uvicorn main:app --reload
```

Endereços disponíveis:

| Recurso | URL |
|---|---|
| API | <http://127.0.0.1:8000> |
| Swagger UI | <http://127.0.0.1:8000/docs> |
| ReDoc | <http://127.0.0.1:8000/redoc> |
| OpenAPI JSON | <http://127.0.0.1:8000/openapi.json> |

Não há uma rota de health check da API no estado atual do projeto.

## 11. Execução com Docker Compose

Esta opção inicia a API e o PostgreSQL sem exigir um banco local. Crie e configure o `.env` antes do build e execute:

```bash
docker compose up --build
```

O Compose:

- inicia PostgreSQL 17 no serviço `db`;
- mantém os dados no volume `postgres_data`;
- verifica o banco com `pg_isready` a cada cinco segundos;
- aguarda o banco ficar `healthy` antes de iniciar o serviço `api`;
- executa `alembic upgrade head`;
- inicia o Uvicorn apenas se as migrations forem aplicadas com sucesso;
- publica a API na porta `8000` e o PostgreSQL na porta `5432` do host.

Para executar em segundo plano:

```bash
docker compose up --build -d
```

Para conferir os serviços:

```bash
docker compose ps
```

Para acompanhar os logs:

```bash
docker compose logs -f
```

Somente os logs da API:

```bash
docker compose logs -f api
```

Para encerrar os contêineres preservando os dados:

```bash
docker compose down
```

> **Atenção:** `docker compose down -v` remove também o volume `postgres_data` e apaga os dados do PostgreSQL executado pelo Compose.

```bash
docker compose down -v
```

O arquivo `.env` é utilizado pelo Docker Compose para interpolar as variáveis definidas no `compose.yaml`. Ele não deve ser copiado para a imagem Docker; o `.dockerignore` mantém arquivos locais e sensíveis fora do contexto de build.

## 12. Dockerfile

O `Dockerfile` realiza as seguintes etapas:

1. usa `python:3.12-slim` como imagem-base;
2. define `/app` como diretório de trabalho;
3. copia e instala `requirements.txt` sem manter cache do `pip`;
4. copia o restante do projeto;
5. define o Uvicorn na porta `8000` como comando padrão.

O comando do `compose.yaml` substitui o comando padrão da imagem para executar as migrations antes do Uvicorn. Executar apenas `docker run` não aplica migrations automaticamente.

## 13. Banco local e banco Docker

O PostgreSQL local e o PostgreSQL iniciado pelo Compose são instâncias separadas.

| Execução | Endereço visto pela API | Persistência |
|---|---|---|
| API local | `localhost:5432` na `DATABASE_URL` | Diretório de dados do PostgreSQL instalado no host |
| API no Compose | `db:5432`, montado pelo `compose.yaml` | Volume Docker `postgres_data` |

O nome `db` funciona como hostname apenas na rede interna do Compose. Dados existentes no PostgreSQL local não aparecem automaticamente no PostgreSQL Docker, e o inverso também é verdadeiro.

## 14. Fluxo inicial para testar o sistema

Após iniciar a aplicação:

1. abra <http://127.0.0.1:8000/docs>;
2. execute `POST /api/v1/users/` para criar um usuário;
3. execute `POST /api/v1/auths/` com as mesmas credenciais;
4. copie o valor de `access_token` retornado;
5. clique em **Authorize** no Swagger e cole o token;
6. execute `POST /api/v1/norms/sync` para importar normas da Receita;
7. consulte `GET /api/v1/norms/`;
8. consulte `GET /api/v1/dashboard` e teste os filtros.

O login não autoriza o Swagger automaticamente. A autorização precisa ser preenchida manualmente com o token retornado.

## 15. Autenticação JWT

O fluxo de autenticação é:

1. `POST /api/v1/users/` cria o usuário e armazena somente o hash da senha;
2. `POST /api/v1/auths/` compara a senha informada com o hash persistido;
3. a API emite um JWT contendo o ID do usuário em `sub` e a expiração UTC em `exp`;
4. as rotas protegidas recebem `Authorization: Bearer <access_token>`;
5. a assinatura e a expiração são validadas com as configurações JWT do `.env`.

Rotas protegidas:

| Método | Rota | Operação |
|---|---|---|
| `POST` | `/api/v1/norms/` | Criar norma manualmente |
| `PATCH` | `/api/v1/norms/{norm_id}` | Atualizar norma |
| `DELETE` | `/api/v1/norms/{norm_id}` | Excluir norma |
| `POST` | `/api/v1/norms/sync` | Sincronizar com a Receita Federal |

As consultas de normas e o dashboard são públicos. Não há perfis ou papéis distintos: os usuários autenticados compartilham as mesmas permissões nas rotas protegidas.

No Swagger, clique em **Authorize** e cole somente o valor de `access_token`, sem aspas. O esquema `HTTPBearer` adiciona o prefixo `Bearer` à requisição.

## 16. Web scraping

O scraper consulta o seguinte endereço público da Receita Federal:

```text
https://normas.receita.fazenda.gov.br/sijut2consulta/consulta.action
```

Fluxo implementado:

```text
Portal da Receita Federal
        ↓
GET com urllib e timeout de 30 segundos
        ↓
HTML da resposta
        ↓
BeautifulSoup com html.parser
        ↓
table#tabelaAtos
        ↓
tr.linhaResultados
        ↓
Dados Python
        ↓
Persistência no PostgreSQL
```

O scraper extrai, por posição na tabela:

- tipo do ato;
- número do ato;
- órgão ou unidade;
- publicação;
- ementa, armazenada como `summary`.

O primeiro link de cada linha é analisado para obter o `source_id` a partir do padrão `/consulta/externa/{id}`. Esse identificador externo é usado para reconhecer normas já sincronizadas. Linhas com menos de cinco colunas são descartadas; itens sem `source_id` podem ser parseados, mas são ignorados na persistência da sincronização.

Selenium não é utilizado porque a implementação atual trabalha diretamente com o HTML retornado pela requisição. Não há retry nem paginação: a sincronização processa os resultados presentes na resposta consultada.

## 17. Sincronização

Rota protegida:

```http
POST /api/v1/norms/sync
Authorization: Bearer <access_token>
```

O serviço baixa e interpreta a página antes de percorrer as normas. Para cada item:

1. se `source_id` estiver ausente, o item é ignorado;
2. se o `source_id` já existir no banco, o item é ignorado;
3. caso contrário, uma nova norma é persistida.

A deduplicação combina uma consulta prévia por `source_id` com um índice único no PostgreSQL. Cadastros manuais não recebem `source_id`.

O retorno contém:

| Campo | Significado |
|---|---|
| `found` | Quantidade de linhas de norma efetivamente parseadas |
| `created` | Quantidade de novas normas persistidas |
| `skipped` | Itens sem `source_id` ou com `source_id` já existente |

Em uma sincronização concluída sem erro, `found` corresponde à soma de `created` e `skipped`. Cada criação realiza seu próprio commit; a sincronização não é uma transação única para todo o lote.

## 18. Tratamento de falhas externas

| Status | Situação implementada |
|---|---|
| `200` | Sincronização concluída |
| `401` | Token ausente, inválido ou expirado em rota protegida |
| `502` | A resposta foi recebida, mas a tabela `tabelaAtos` não foi encontrada |
| `503` | Erro HTTP da origem, falha de conexão ou timeout ao consultar a Receita |
| `500` | Erro de banco tratado globalmente ou outra falha não normalizada |

Erros SQLAlchemy são registrados internamente e respondidos sem detalhes do banco:

```json
{
  "success": false,
  "message": "Erro interno ao acessar o banco de dados.",
  "data": null
}
```

A ausência da tabela esperada é convertida em `502`. Outros formatos inesperados, como um número de ato não conversível para inteiro, não possuem tratamento específico no scraper atual.

## 19. CRUD de normas

| Método | Rota | Autenticação | Resultado esperado |
|---|---|---|---|
| `GET` | `/api/v1/norms/` | Não | Lista de normas |
| `GET` | `/api/v1/norms/{norm_id}` | Não | Norma pelo ID ou `404` |
| `POST` | `/api/v1/norms/` | Bearer JWT | Criação manual com status `201` |
| `PATCH` | `/api/v1/norms/{norm_id}` | Bearer JWT | Atualização parcial ou `404` |
| `DELETE` | `/api/v1/norms/{norm_id}` | Bearer JWT | Exclusão ou `404` |

Corpo para criação:

```json
{
  "act_type": "Instrução Normativa",
  "act_number": 123,
  "agency_unit": "COSIT",
  "publication": "13/08/2026",
  "summary": "Exemplo curto de ementa para validação local."
}
```

Os cinco campos são obrigatórios na criação. No `PATCH`, todos são opcionais; campos omitidos ou enviados como `null` preservam o valor atual.

`source_id` é um campo interno da persistência e não faz parte dos schemas públicos de norma. A listagem atual não possui paginação nem ordenação explícita.


## 20. Dashboard

Rota pública:

```http
GET /api/v1/dashboard
```

Parâmetros opcionais:

| Parâmetro | Comportamento |
|---|---|
| `date` | Exige `DD/MM/AAAA` e compara o texto por igualdade com `publication` |
| `search` | Busca parcial e sem diferenciar maiúsculas de minúsculas |

`search` procura em `act_type`, `agency_unit`, `summary` e `act_number` convertido para texto. Não pesquisa em `publication`, `id` ou `source_id`. Quando `date` e `search` são enviados juntos, os filtros são combinados com `AND`.

Exemplos:

```http
GET /api/v1/dashboard?date=13/08/2026
GET /api/v1/dashboard?search=cosit
GET /api/v1/dashboard?date=13/08/2026&search=cosit
```

Uma data fora de `DD/MM/AAAA` retorna `422`. `publication` é armazenado como texto, não como coluna de data; depois da validação de formato, a comparação é exata.

O dashboard calcula as agregações depois dos filtros e retorna:

- `total_norms`: total de normas no recorte;
- `total_act_types`: quantidade de tipos de ato distintos;
- `total_agencies`: quantidade de órgãos ou unidades distintos;
- `by_act_type`: contagem por tipo de ato;
- `by_agency`: contagem por órgão ou unidade;
- `norms`: normas usadas no cálculo.

Não há ordenação explícita dos resultados ou dos agrupamentos.

## 21. Exemplos de respostas

### Criação de usuário

```json
{
  "id": 1,
  "email": "avaliador@example.com"
}
```

### Login

```json
{
  "access_token": "<JWT_RETORNADO_PELO_LOGIN>",
  "token": "bearer"
}
```

O nome do segundo campo é `token`, conforme o schema atual; ele não se chama `token_type`.

### Primeira sincronização

Os números abaixo são apenas ilustrativos:

```json
{
  "success": true,
  "message": "Sincronização concluída com sucesso!",
  "data": {
    "found": 19,
    "created": 19,
    "skipped": 0
  }
}
```

### Sincronização posterior sem novos atos

```json
{
  "success": true,
  "message": "Sincronização concluída com sucesso!",
  "data": {
    "found": 19,
    "created": 0,
    "skipped": 19
  }
}
```

### Lista de normas

```json
{
  "success": true,
  "message": "Normas encontradas com sucesso!",
  "data": [
    {
      "id": 1,
      "act_type": "Instrução Normativa",
      "act_number": 123,
      "agency_unit": "COSIT",
      "publication": "13/08/2026",
      "summary": "Exemplo curto de ementa."
    }
  ]
}
```

## 22. Testando via Swagger

1. acesse <http://127.0.0.1:8000/docs>;
2. abra `POST /api/v1/users/` e envie um e-mail e uma senha de teste;
3. abra `POST /api/v1/auths/` e repita as credenciais;
4. copie somente o conteúdo de `access_token`;
5. clique em **Authorize** no topo da página;
6. cole o token, sem aspas, no esquema `HTTPBearer`;
7. confirme a autorização;
8. execute uma rota protegida, como `POST /api/v1/norms/sync`.

O Swagger envia o cabeçalho:

```http
Authorization: Bearer <access_token>
```

## 23. Comandos úteis

### Aplicação local

```bash
uvicorn main:app --reload
```

### Alembic

```bash
python -m alembic upgrade head
python -m alembic current
python -m alembic history
```

### Docker Compose

```bash
docker compose up --build
docker compose up --build -d
docker compose logs -f
docker compose ps
docker compose down
```

## 24. Solução de problemas

### Porta 5432 já está em uso

Pode haver uma instalação local do PostgreSQL ou outro contêiner usando a porta publicada pelo Compose. Pare o serviço conflitante ou altere apenas a porta do host em `compose.yaml`, mantendo a porta interna do serviço em `5432`.

### Porta 8000 já está em uso

Encerre a outra aplicação que usa a porta ou inicie o Uvicorn local em outra porta:

```bash
uvicorn main:app --reload --port 8001
```

Se usar Docker, ajuste também o mapeamento de portas do serviço `api`.

### Docker daemon não está em execução

Inicie o Docker Desktop no Windows/macOS ou o Docker Engine no Linux. Depois confirme:

```bash
docker info
docker compose version
```

### Banco Docker está vazio

O banco Docker é separado do PostgreSQL local. Crie um usuário pela API, faça login e execute `POST /api/v1/norms/sync` para preencher as normas.

### `Target database is not up to date`

Aplique as migrations pendentes antes de gerar outra migration:

```bash
python -m alembic upgrade head
```

### SQLAlchemy procura `psycopg2`

Confira se `DATABASE_URL` começa com:

```text
postgresql+psycopg://
```

O projeto instala Psycopg 3, não `psycopg2`.

### Erro de configuração ao iniciar

Confirme que o `.env` existe na raiz e contém as variáveis obrigatórias definidas em `app/core/config.py`, especialmente `DATABASE_URL` e `JWT_SECRET_KEY`. Execute Uvicorn e Alembic a partir da raiz do repositório, pois o caminho do `.env` é relativo.

### Alterações em `POSTGRES_*` não aparecem no contêiner

O PostgreSQL usa as variáveis de inicialização somente ao criar o volume pela primeira vez. Um volume existente preserva usuário, senha, banco e dados anteriores. Remover o volume reinicializa o banco, mas apaga os dados.

### Falha ao baixar uma imagem Docker

Verifique a conexão com a internet, o acesso ao Docker Hub e o estado do Docker daemon. Depois tente novamente:

```bash
docker compose pull
docker compose up --build
```

## 25. Segurança

- não versione o `.env`;
- mantenha apenas valores ilustrativos no `.env.example`;
- use uma `JWT_SECRET_KEY` longa, aleatória e diferente por ambiente;
- não inclua JWTs reais em documentação, logs compartilhados ou commits;
- as senhas são persistidas como hash pelo `pwdlib`, com suporte Argon2 instalado;
- criação, atualização, exclusão e sincronização de normas exigem Bearer Token;
- restrinja o acesso ao PostgreSQL e troque as credenciais ilustrativas;
- revise as variáveis e credenciais antes de publicar a imagem em qualquer registry.

O projeto utiliza `.dockerignore` para impedir que arquivos locais ou sensíveis, como `.env`, `.git`, `.venv`, caches e bytecode Python, sejam enviados ao contexto de build ou copiados para a imagem Docker.

## 26. Observações para desenvolvimento

- atualize `requirements.txt` quando adicionar uma dependência;
- gere uma migration Alembic para cada alteração de schema;
- revise a migration autogerada antes de aplicá-la;
- mantenha os models importados em `alembic/env.py` para o autogenerate;
- considere a estrutura HTML da Receita um contrato externo sujeito a mudanças;
- atualize os seletores do scraper se `tabelaAtos` ou `linhaResultados` mudar;
- considere retry, paginação e transação de lote caso a sincronização evolua;
- a listagem atual não possui paginação nem ordenação explícita;
- não foi encontrada uma suíte automatizada de testes no repositório atual.

## 27. Fluxo arquitetural

Requisições comuns:

```text
HTTP Request
    ↓
Router
    ↓
Service
    ↓
Repository
    ↓
SQLAlchemy / Psycopg
    ↓
PostgreSQL
```

Sincronização:

```text
POST /api/v1/norms/sync
    ↓
NormService
    ↓
FederalRevenueScraper
    ↓
Portal da Receita Federal
    ↓
Dados extraídos
    ↓
NormRepository
    ↓
PostgreSQL
```

Autenticação:

```text
POST /api/v1/auths/
    ↓
UserService
    ↓
Validação da senha
    ↓
JWT com sub e exp
    ↓
HTTPBearer nas rotas protegidas
```

## 28. Estado atual do projeto

- [x] CRUD de normas
- [x] PostgreSQL e SQLAlchemy
- [x] Migrations Alembic
- [x] Criação de usuários
- [x] Hash de senhas
- [x] Autenticação JWT
- [x] Rotas de escrita protegidas
- [x] Web scraping com urllib e BeautifulSoup
- [x] Sincronização com deduplicação por `source_id`
- [x] Dashboard
- [x] Filtro por data e pesquisa textual
- [x] Swagger UI, ReDoc e OpenAPI
- [x] Dockerfile
- [x] Docker Compose com PostgreSQL e healthcheck
- [ ] Suíte automatizada de testes

## 29. Compatibilidade

As instruções contemplam:

- Windows com PowerShell;
- Linux com shell compatível com Bash;
- macOS com shell compatível com Bash ou Zsh;
- execução local com `venv` e `pip`;
- execução por Docker Compose.

Os comandos devem ser executados na raiz do projeto. As diferenças de criação e ativação da `.venv` estão separadas por sistema operacional nas seções anteriores.
