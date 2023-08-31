import streamlit as st

from app.password import check_password

st.set_page_config(
    page_title="LLM Apps",
    page_icon="☃️",
)

def main() -> None:
    st.title("☃️ LLM Apps")
    st.markdown("### Select a Demo from the sidebar:")
    st.markdown("1. Chat with PDFs in the data/pdfs folder")
    st.markdown("2. Chat with papers from Arxiv")
    st.markdown("3. Chat with a website")

    st.sidebar.success("Select a demo from above")


if check_password():
    main()
