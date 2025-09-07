# Ingestão e Busca Semântica com LangChain e PostgreSQL

Sistema RAG (Retrieval-Augmented Generation) que permite fazer ingestão de documentos PDF e realizar consultas semânticas usando LangChain, OpenAI e PostgreSQL com pgVector.

## Como executar

### 1. Configurar ambiente virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Subir banco de dados PostgreSQL com pgVector

```bash
docker compose up -d
```

### 4. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e configure suas chaves de API:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da OpenAI:

```env
# OpenAI API Key
OPENAI_API_KEY=sua_chave_openai_aqui

# OpenAI Model
OPENAI_MODEL=text-embedding-3-small

# PostgreSQL Vector Database URL
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag

# PGVector Collection Name
PGVECTOR_COLLECTION=gpt5_collection
```

### 5. Executar ingestão do PDF

```bash
python src/ingest.py
```

Este comando irá:

- Carregar o arquivo `document.pdf`
- Dividir o documento em chunks de 1000 caracteres com overlap de 150
- Gerar embeddings usando o modelo `text-embedding-3-small`
- Armazenar os vetores no PostgreSQL com pgVector

### 6. Iniciar o chat

```bash
python src/chat.py
```

## Exemplo de uso

```
Chat Digite 'sair' para encerrar

Faça sua pergunta:

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

---

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

---
```

## Estrutura do projeto

```
├── docker-compose.yml          # Configuração do PostgreSQL com pgVector
├── requirements.txt            # Dependências Python
├── .env.example               # Template das variáveis de ambiente
├── .env                       # Suas variáveis de ambiente (não commitado)
├── src/
│   ├── ingest.py             # Script de ingestão do PDF
│   ├── search.py             # Funções de busca semântica
│   └── chat.py               # Interface CLI para chat
├── document.pdf              # Documento PDF para ingestão
└── README.md                 # Este arquivo
```

## Tecnologias utilizadas

- **Python**: Linguagem principal
- **LangChain**: Framework para aplicações com LLM
- **OpenAI**: API para embeddings e chat completion
- **PostgreSQL + pgVector**: Banco de dados vetorial
- **Docker**: Containerização do banco de dados

## Comandos para sair do chat

- `sair`
- `exit`
- `quit`
- `Ctrl+C`

## Observações

- Certifique-se de que o Docker esteja rodando antes de executar `docker compose up -d`
- O arquivo `document.pdf` deve estar na raiz do projeto
- As respostas são baseadas exclusivamente no conteúdo do PDF ingerido
- Perguntas fora do contexto retornarão: "Não tenho informações necessárias para responder sua pergunta."
