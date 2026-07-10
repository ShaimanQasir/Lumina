from langchain_core.documents import Document

from config.config import Config
from langchain_chroma import Chroma
from rag.embedding import Embedding

class Indexer:
    def __init__(self, config: type[Config] = Config):
        self.persist_directory = config.CHROMA_PERSIST_DIR
        self.embedding = Embedding()
        self.embedding_model = self.embedding.embedding_model

    def add_documents(self, documents: list[Document]) -> Chroma:
        """
        Access Chroma Vector Store to add documents
        parameters:
            documents: List of documents to be added
        """
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding_model,
            persist_directory=self.persist_directory,
            collection_name="embedded_files"
        )
        return vector_store