import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_openai import ChatOpenAI

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_documents(query: str) -> str:
    for k in ("OPENAI_API_KEY", "PGVECTOR_URL"):
        if not os.getenv(k):
            raise RuntimeError(f"Variável de ambiente {k} não encontrada")
        
    openai_api_key = os.getenv("OPENAI_API_KEY")
    pgvector_url = os.getenv("PGVECTOR_URL")
    collection_name = os.getenv("PGVECTOR_COLLECTION", "gpt5_collection")
        
    try:
        embeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key,
            model="text-embedding-3-small"
        )
        
        vector_store = PGVector(
            embeddings=embeddings,
            connection=pgvector_url,
            collection_name=collection_name,
            use_jsonb=True,
        )
        
        docs = vector_store.similarity_search_with_score(query, k=3)
        
        if not docs:
            return "Não tenho informações necessárias para responder sua pergunta."
        
        contexto = "\n\n".join([doc[0].page_content for doc in docs])
        
        prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=query)
        
        llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model="gpt-5-nano",
            temperature=0
        )
        
        response = llm.invoke(prompt)
        return response.content
        
    except Exception as e:
        return f"Erro ao buscar documentos: {e}"