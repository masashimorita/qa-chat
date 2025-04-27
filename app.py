import os
import tempfile
import streamlit as st
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import pandas as pd
from utils.vector_store import (
  create_vector_store, 
  get_collection,
  format_docs,
  get_documents_from_file
)
from utils.llm import model


def register_documents(uploaded_file):
  if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
      tmp_file.write(uploaded_file.getvalue())
      tmp_file_path = tmp_file.name

    try:
      result = get_documents_from_file(tmp_file_path, uploaded_file.name)
      original_ids = result["original_ids"]
      documents = result["documents"]

      vector_store = create_vector_store()
      vector_store.add_documents(documents=documents, ids=original_ids)
      st.success(f"Documents from {uploaded_file.name} registered successfully")
    except Exception as e:
      st.error(f"Error occurred while registering documents: {e}")
    finally:
      os.remove(tmp_file_path)


def generate_answer(question):
  if question:
    try:
      prompt = hub.pull("rlm/rag-prompt")
      chain = (
        {
          "context": create_vector_store().as_retriever() | format_docs,
          "question": RunnablePassthrough(),
        }
        | prompt
        | model
        | StrOutputParser()
      )
      return chain.invoke(question)
    except Exception as e:
      st.error(f"Error occurred while generation answer: {e}")
      return None


def manage_db():
  st.header("Manage documents stored in DB")

  vector_collection = get_collection()

  st.subheader("Register documents to DB")
  uploaded_file = st.file_uploader('Upload Text File', type='txt')
  if uploaded_file:
      if st.button("Register"):
        with st.spinner('Registering file...'):
          register_documents(uploaded_file)

  st.markdown("---")

  st.subheader("ChromaDB Registered documents")
  if st.button("Show Documents"):
      with st.spinner('Retrieving data...'):
          dict_data = vector_collection.get()
          if dict_data['ids']:
              tmp_df = pd.DataFrame({
                  "IDs": dict_data['ids'],
                  "Documents": dict_data['documents'],
                  "Metadatas": dict_data['metadatas']
              })
              st.dataframe(tmp_df)
          else:
              st.info("No documents registered in DB")

  st.markdown("---")

  st.subheader("Delete all registered data in ChromaDB")
  if st.button("Delete all data"):
    with st.spinner('Deleting data...'):
      current_ids = vector_collection.get()['ids']
      if current_ids:
        vector_collection.delete(ids=current_ids)
        st.success("All registered data in DB has been deleted")
      else:
        st.info("No data to delete")


def ask_question():
  st.header("Ask question about the documents")

  question = st.text_input('Question:', placeholder='Input a brief summary of question')

  if st.button('Submit') and question:
    with st.spinner('Generating answer...'):
      answer = generate_answer(question)
      if answer:
        st.success("Answer:")
        st.info(answer)
      else:
        st.error("Failed to generate answer...")


def main():
  st.set_page_config(page_title="Q&A Chat with AI", page_icon=":shark:", layout="wide")
  st.title("Q&A Chat with AI")

  st.sidebar.title("Menu")
  page_manage_db = "Manage DB"
  page_ask = "Ask Question"
  page = st.sidebar.radio("Select a page", [page_manage_db, page_ask])

  if page == page_manage_db:
    manage_db()
  elif page == page_ask:
    ask_question()
  else:
    st.error("Invalid page")


if __name__ == "__main__":
  main()
