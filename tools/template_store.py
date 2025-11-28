import os
from typing import List, Optional
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

class TemplateStore:
    def __init__(self):
        self.persist_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "vector_db")
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma(
            persist_directory=self.persist_directory, 
            embedding_function=self.embeddings,
            collection_name="contract_clauses"
        )

    def add_documents(self, documents: List[str], metadatas: Optional[List[dict]] = None):
        if not documents:
            return
        self.vector_store.add_texts(texts=documents, metadatas=metadatas)
        print(f"Added {len(documents)} documents to TemplateStore.")

    def search(self, query: str, k: int = 3) -> List[str]:
        results = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": 3})

    def load_clauses(self, directory: str):
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return
        
        documents = []
        metadatas = []
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                filepath = os.path.join(directory, filename)
                with open(filepath, "r") as f:
                    content = f.read()
                    documents.append(content)
                    metadatas.append({"source": filename})
        
        if documents:
            self.add_documents(documents, metadatas)
            print(f"Loaded {len(documents)} clauses from {directory}")
        else:
            print(f"No text files found in {directory}")

if __name__ == "__main__":
    store = TemplateStore()
    # Test loading clauses
    clauses_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "clauses")
    store.load_clauses(clauses_dir)
    print("Search results for 'payment':")
    print(store.search("payment"))
