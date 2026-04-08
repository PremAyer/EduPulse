import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DB_DIR = "./course_chroma_db"

def get_retriever(docs=None):
    """Initializes or loads the vector database and returns a retriever."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if not os.path.exists(DB_DIR) and docs is not None:
        vector_store = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=DB_DIR
        )

    else:
        vector_store = Chroma(
            persist_directory=DB_DIR, 
            embedding_function=embeddings
        )
        
    return vector_store.as_retriever(search_kwargs={"k": 5})