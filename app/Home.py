import streamlit as st

from app.password import check_password

st.set_page_config(
    page_title="LLM Apps",
    page_icon=":snowman:",
)


def main() -> None:
    st.title(":snowman: LLM Apps")
    st.markdown("## Select App from the sidebar:")
    st.markdown("1. Chat with PDFs in the data/pdfs folder")
    st.markdown("2. Chat with the Arxiv articles")
    st.markdown("3. Chat with a website")

    st.sidebar.success("Select App from above")


if check_password():
    main()
