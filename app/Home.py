import streamlit as st

st.set_page_config(
    page_title="LLM Apps",
    page_icon="🚝",
)

st.title("☃️ LLM Apps")
st.markdown("### Select a Demo from the sidebar:")
st.markdown("1. Chat with PDF: Chat with a PDF document")
st.markdown("2. Chat with Wikipedia: Chat with a wikipedia article")
st.markdown("3. Chat with Website: Chat with a website")

st.sidebar.success("Select a demo from above")
