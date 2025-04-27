import streamlit as st


def manage_db():
  st.header("Manage documents stored in DB")


def ask_question():
  st.header("Ask question about the documents")


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
