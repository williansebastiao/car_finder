# Car Finder

Assistente conversacional com IA para busca de veículos. O usuário descreve em linguagem natural o carro que procura, e o agente utiliza o modelo Claude para interpretar as preferências e realizar buscas inteligentes no banco de dados.

## Tecnologias

- **Python 3.12+** com AsyncIO
- **Claude Sonnet 4.6** (Anthropic) — modelo de linguagem do agente
- **MCP (Model Context Protocol)** — integração entre agente e ferramentas
- **PostgreSQL 16** — banco de dados de veículos
- **SQLAlchemy 2.0+** com suporte assíncrono
- **Alembic** — gerenciamento de migrações
- **Pydantic v2** — validação de dados
- **Poetry** — gerenciamento de dependências
- **Docker** — infraestrutura local

## Pré-requisitos

- Python 3.12+
- Poetry
- Docker e Docker Compose
- Chave de API da Anthropic (`ANTHROPIC_API_KEY`)

## Instalação

### 1. Instale as dependências

```bash
poetry install
```

### 2. Ative o virtualenv

```bash
poetry env activate
```

### 3. Configure as variáveis de ambiente

```bash
make scaffold
```

Isso cria o arquivo `.env` a partir do `.env.example`. Edite o arquivo gerado e preencha sua `ANTHROPIC_API_KEY`:

```env
DATABASE_HOST=localhost
DATABASE_NAME=car_finder_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_PORT=5433
ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Suba o banco de dados

```bash
make start
```

### 5. Execute as migrações

```bash
make migrate
```

### 6. Popule o banco com dados de exemplo

```bash
make seed
```

Insere 150 veículos aleatórios no banco de dados.

## Uso

### Iniciar o agente

```bash
make run
```

O agente iniciará uma conversa em português. Descreva o carro que procura em linguagem natural:

```
Car Finder - Digite 'sair' ou Ctrl+C para encerrar

Agente: Olá! Estou aqui para ajudar a encontrar o carro ideal para você!
        Me conte um pouco sobre o que você está procurando.

Você: Quero um SUV da Toyota, automático, até R$ 200.000
Agente: Encontrei algumas opções que combinam com o que você busca...

Você: sair
Agente: Até mais! Boa sorte na busca pelo seu carro.
```

Para encerrar: digite `sair`, `exit`, `quit`, `q` ou pressione `Ctrl+C`.

### Filtros disponíveis

O agente pode buscar por qualquer combinação dos seguintes critérios:

| Filtro | Exemplos |
|---|---|
| Marca | Toyota, Honda, Volkswagen, Chevrolet, Fiat... |
| Modelo | Corolla, Civic, Gol, Onix, Strada... |
| Ano | faixa de ano (ex: 2020 a 2024) |
| Combustível | Flex, Gasolina, Diesel, Elétrico, Híbrido, GNV |
| Câmbio | Manual, Automático, CVT, Automatizado, Dupla Embreagem |
| Cor | Branco, Preto, Prata, Cinza, Vermelho, Azul... |
| Condição | Novo, Seminovo, Usado |
| Categoria | Hatch, Sedan, SUV, Picape, Minivan, Cupê, Conversível, Perua, Van |
| Preço | faixa de preço em reais |
| Quilometragem | máximo de km rodados |

## Comandos disponíveis

```bash
make scaffold    # Cria o .env a partir do .env.example
make start       # Inicia os containers Docker em background
make build       # Inicia os containers com rebuild de imagens
make stop        # Para e remove os containers
make migrate     # Executa as migrações pendentes
make seed        # Insere 150 veículos de exemplo no banco
make run         # Inicia o agente no terminal
make lint        # Formata o código com ruff
make tests       # Executa os testes com cobertura mínima de 80%
```

### Criar uma nova migração

```bash
make migration message="descrição da migração"
```

## Estrutura do projeto

```
car_finder/
├── src/
│   ├── agent/              # Lógica do agente com Claude
│   ├── core/               # Configurações e logging
│   ├── database/           # Sessão e scripts de seed
│   ├── integrations/       # Cliente MCP
│   ├── models/
│   │   ├── entities/       # Modelos ORM (SQLAlchemy)
│   │   ├── enums/          # Constantes e enumerações
│   │   └── schemas/        # Schemas Pydantic
│   ├── repositories/       # Camada de acesso a dados
│   ├── main.py             # Ponto de entrada do terminal
│   └── server.py           # Servidor MCP com a ferramenta de busca
├── migrations/             # Migrações Alembic
├── docker-compose.yml      # Infraestrutura PostgreSQL
├── makefile                # Comandos de desenvolvimento
└── pyproject.toml          # Dependências e configuração do projeto
```

## Arquitetura

O projeto utiliza o **Model Context Protocol (MCP)** para separar o agente da ferramenta de busca:

```
Terminal (main.py)
    └── CarFinderAgent
            └── MCPClient ──stdio──> MCP Server (server.py)
                                            └── VehicleRepository
                                                    └── PostgreSQL
```

1. O usuário digita uma mensagem no terminal
2. O `CarFinderAgent` envia o histórico da conversa para o Claude
3. O Claude decide quando chamar a ferramenta `search_vehicles` com os filtros adequados
4. O `MCPClient` repassa a chamada ao `server.py` via subprocess e stdio
5. O servidor executa a query no banco e retorna os resultados
6. O Claude formula a resposta final em linguagem natural
