import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from .llm import embeddings


load_dotenv()


DB_PERSIST_DIRECTORY = os.getenv("DB_PERSIST_DIRECTORY", "./chroma")
DB_COLLECTION_NAME = os.getenv("DB_COLLECTION_NAME", "qa-chat")


def create_vector_store():
  vector_store = Chroma(
    collection_name=DB_COLLECTION_NAME,
    persist_directory=DB_PERSIST_DIRECTORY,
    embedding_function=embeddings,
  )
  
  return vector_store

def get_collection():
  client = Chroma.PersistentClient(path=DB_PERSIST_DIRECTORY)

  try:
    return client.get_collection(name=DB_COLLECTION_NAME)
  except Exception as e:
    return client.create_collection(name=DB_COLLECTION_NAME)


def format_docs(docs):
  return "\n\n".join(doc.page_content for doc in docs)
