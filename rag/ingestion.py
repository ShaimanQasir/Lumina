from config.config import Config
from rag.chunking import Chunker
from storage.local_storage import LocalStorage
from rag.indexer import Indexer


class Ingestion:
    def __init__(self, config: type[Config] = Config):
        self.storage = LocalStorage()
        self.chunker = Chunker()
        self.indexer = Indexer()

    def run (self):
        """
        Run the ingestion process to chunk, embed, and move files.
        """
        list_files = self.storage.list_files()

        for file in list_files:
            try:
                read_files = self.storage.read_object(file)
                chunks = self.chunker.chunk(read_files)
                self.indexer.add_documents(chunks)
                self.storage.move_files(file)
            except Exception as e:
                print(f"Error processing file {file}: {e}")
                continue