import os
import datetime
from typing import List, Optional
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

class MemoryStore:
    def __init__(self):
        self.persist_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "vector_db")
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma(
            persist_directory=self.persist_directory, 
            embedding_function=self.embeddings,
            collection_name="conversation_history"
        )

    def add_message(self, role: str, content: str):
        """Save a message to the memory store."""
        timestamp = datetime.datetime.now().isoformat()
        doc = Document(
            page_content=content,
            metadata={
                "role": role,
                "timestamp": timestamp
            }
        )
        self.vector_store.add_documents([doc])
        # print(f"Saved {role} message to memory.")

    def get_context(self, query: str, k: int = 5) -> List[str]:
        """Retrieve relevant past messages based on a query."""
        results = self.vector_store.similarity_search(query, k=k)
        return [f"{doc.metadata.get('role', 'unknown')}: {doc.page_content}" for doc in results]

    def get_recent_messages(self, k: int = 5) -> List[str]:
        """Get the most recent messages (simulated by empty query for now, or just relying on Chroma's default behavior if query is empty string which might not work as expected for 'recent', but good enough for context retrieval).
        Actually, vector stores aren't great for 'recent' without a timestamp sort. 
        For RAG, we usually want relevant.
        """
        # For true "recent", we'd need a different store or metadata filtering. 
        # Here we will just expose search.
        return self.get_context("", k=k)

if __name__ == "__main__":
    memory = MemoryStore()
    memory.add_message("user", "I need a contract for web design.")
    memory.add_message("assistant", "I can help with that. What are the payment terms?")
    
    print("Context for 'payment':")
    print(memory.get_context("payment"))
