import streamlit as st
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from utils.vector_store import (
  create_vector_store, 
  get_collection,
  format_docs
)
from utils.llm import model


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


def ask_question():
  st.header("Ask question about the documents")

  question = st.text_input('Question:', placeholder='Input a brief summary of question')

  if st.button('Submit') and question:
    with st.spinner('Generating answer...'):
      answer = generate_answer(question)
      if answer:
        st.success("回答:")
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
