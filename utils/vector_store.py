import os
from dotenv import load_dotenv
import chromadb
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
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
  client = chromadb.PersistentClient(path=DB_PERSIST_DIRECTORY)

  try:
    return client.get_collection(name=DB_COLLECTION_NAME)
  except Exception as e:
    return client.create_collection(name=DB_COLLECTION_NAME)


def format_docs(docs):
  return "\n\n".join(doc.page_content for doc in docs)


def get_documents_from_file(file_path: str, source: str):
  loader = TextLoader(file_path)
  raw_documents = loader.load()

  for document in raw_documents:
    document.metadata["source"] = source

  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=100,
    add_start_index=True,
    separators=["\n\n", "\n", ".", " ", ""],
  )

  documents = text_splitter.split_documents(raw_documents)

  original_ids = []
  for doc in documents:
    _source = os.path.splitext(os.path.basename(doc.metadata["source"]))[0]
    _start = doc.metadata["start_index"]
    original_ids.append(f"{_source}-{_start:08}")
  
  return {
    "original_ids": original_ids,
    "documents": documents,
  }
