import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from loguru import logger

from app.config import settings

# Initialize Pinecone
pinecone.init(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENVIRONMENT)
INDEX_NAME = "clinic-assistant-index"

# Initialize Embeddings model from LangChain
embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY, model=settings.EMBEDDING_MODEL)

def get_or_create_pinecone_index():
    if INDEX_NAME not in pinecone.list_indexes():
        logger.info(f"Creating Pinecone index: {INDEX_NAME}")
        pinecone.create_index(
            name=INDEX_NAME,
            dimension=1536, # Dimension for text-embedding-3-small
            metric="cosine",
            pod_type="p1.x1" # Choose a pod type suitable for your needs
        )
    return pinecone.Index(INDEX_NAME)

index = get_or_create_pinecone_index()

def embed_and_store_document(content: str, filename: str, clinic_id: int):
    """
    Chunks, embeds, and stores a document in Pinecone.
    This is designed to be run in a background task.
    """
    logger.info(f"Processing document '{filename}' for clinic {clinic_id}")
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_text(content)
        
        vectors = []
        for i, chunk in enumerate(chunks):
            embedding = embeddings.embed_query(chunk)
            # Create a unique and descriptive ID for each vector
            vector_id = f"clinic_{clinic_id}::doc_{filename}::chunk_{i}"
            # Store clinic_id in metadata for filtering
            metadata = {"text": chunk, "clinic_id": clinic_id, "source": filename}
            vectors.append((vector_id, embedding, metadata))

        if vectors:
            index.upsert(vectors=vectors, namespace=f"clinic-{clinic_id}")
            logger.info(f"Successfully stored {len(vectors)} vectors for document '{filename}' in namespace clinic-{clinic_id}.")

    except Exception as e:
        logger.error(f"Failed to process document for clinic {clinic_id}: {e}")

async def query_vectorstore(clinic_id: int, query: str, top_k: int = 3) -> str:
    """
    Queries the vector store to find relevant context for a given query,
    searching only within the specific clinic's namespace.
    """
    try:
        query_embedding = embeddings.embed_query(query)
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            namespace=f"clinic-{clinic_id}", # Use namespace for multi-tenancy
            include_metadata=True
        )
        
        context = "\n".join([res.metadata['text'] for res in results.matches])
        logger.info(f"Retrieved RAG context for clinic {clinic_id}: {context[:200]}...")
        return context
    except Exception as e:
        logger.error(f"Failed to query Pinecone for clinic {clinic_id}: {e}")
        return ""