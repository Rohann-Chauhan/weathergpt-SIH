from .process_pdf import pdf_loader
from .splitting_text import text_splitting
from .embedding import EmbeddingModel
from .vector_db import VectorStore
import os
class RagPipeline:
    def __init__(self):
        self.pdf_loader = pdf_loader

        self.text_splitting = text_splitting
        embedding = EmbeddingModel(
            model_name="nomic-embed-text"
        )

        self.embedding_model = embedding.load_model()
        self.vector_store = VectorStore(
            self.embedding_model
        )
    def build_pipeline(self):
       
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_folder_path = os.path.join(current_dir, "pdf_file")
        
       
        documents = self.pdf_loader(pdf_folder_path)
 
        print(f"Loaded documents count: {len(documents)}")
        if not documents:
            raise ValueError(f"No documents found at path: {pdf_folder_path}. Please check if PDFs exist inside pdf_file folder.")
        chunks = self.text_splitting(
            documents
        )
        self.vector_store.create_vector_store(
            chunks
        )

        retriever = self.vector_store.create_retriever(
            k=3
        )
        return retriever

def build_pipeline(question=None):
    pipeline = RagPipeline()
    retriever= pipeline.build_pipeline()
    if question:
        return retriever.invoke(question)
    return retriever