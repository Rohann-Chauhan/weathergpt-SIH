from langchain_community.vectorstores import FAISS


"""class VectorStore:

    def __init__(self, embedding_model):

        self.embedding_model = embedding_model

        self.vectorstore = None

        self.retriever = None

    def create_vector_store(self, documents):

        self.vectorstore = FAISS.from_documents(
            documents,
            self.embedding_model
        )

        print(
            f"Vector store created with "
            f"{len(documents)} chunks"
        )

        return self.vectorstore
"""
     # vector_db.py
from langchain_community.vectorstores import FAISS

class VectorStore:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vectorstore = None

    def create_vector_store(self, chunks):
        if not chunks:
            raise ValueError("No chunks provided to create vector store.")

        batch_size = 32
        initial_batch = chunks[:batch_size]

        print(f"Creating vector store for {len(chunks)} chunks in batches of {batch_size}...")
        self.vectorstore = FAISS.from_documents(
            documents=initial_batch,
            embedding=self.embedding_model
        )

        for i in range(batch_size, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            self.vectorstore.add_documents(batch)
            print(f"Processed {min(i + batch_size, len(chunks))}/{len(chunks)} chunks...")

        print("Vector store created successfully!")

   # def create_retriever(self, k=3):
       # return self.vectorstore.as_retriever(search_kwargs={"k": k})
    def create_retriever(self, k=3):

        if self.vectorstore is None:
            raise ValueError(
                "Create vector store first."
            )

        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": k}
        )

        print(
            f"Retriever created with k={k}"
        )

        return self.retriever