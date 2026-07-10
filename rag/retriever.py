from langchain_core.documents import Document

from config.config import Config
from langchain_chroma import Chroma
from rag.embedding import Embedding

class Retriever:
    def __init__(self, config: type[Config] = Config):
        self.persist_directory = config.CHROMA_PERSIST_DIR
        self.embedding = Embedding()
        self.embedding_model = self.embedding.embedding_model
        self.vector_store = Chroma(
            collection_name="embedded_files",
            embedding_function=self.embedding_model,
            persist_directory=self.persist_directory
        )

    def retrieve(self, query: str, top_k: int = 5) -> list[Document]:
        """
        Retrieve documents from the vector store based on the query.
        parameters:
            query: The query string.
            top_k: The number of top matching documents to retrieve.
        """
        return self.vector_store.similarity_search(query=query, k=top_k)

