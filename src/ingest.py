import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

def main():
    for k in ("OPENAI_API_KEY", "PGVECTOR_URL"):
        if not os.getenv(k):
            raise RuntimeError(f"Variável de ambiente {k} não encontrada")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    pgvector_url = os.getenv("PGVECTOR_URL")
    collection_name = os.getenv("PGVECTOR_COLLECTION", "gpt5_collection")
    
    pdf_path = "document.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo {pdf_path} não encontrado")
        return
    
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150, 
        add_start_index=False
    )
    chunks = text_splitter.split_documents(documents)

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in chunks
    ]    

    ids = [f"doc-{i}" for i in range(len(enriched))]
    
    embeddings = OpenAIEmbeddings(
        openai_api_key=openai_api_key,
        model="text-embedding-3-small"
    )
    
    try:
        store = PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection=pgvector_url,
            use_jsonb=True,
        )

        store.add_documents(enriched, ids=ids)
        
        print(f" Ingestão concluída! {len(chunks)} chunks armazenados na coleção '{collection_name}'")
    except Exception as e:
        print(f" Erro ao armazenar no banco: {e}")

if __name__ == "__main__":
    main()