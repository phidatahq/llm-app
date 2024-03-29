import streamlit as st

from app.password import check_password

st.set_page_config(
    page_title="LLM Apps",
    page_icon=":snowman:",
)


st.title(":snowman: LLM Apps")
st.markdown('<a href="https://github.com/phidatahq/phidata"><h4>by phidata</h4></a>', unsafe_allow_html=True)


def main() -> None:
    st.markdown("### Select an App:")
    st.markdown("#### 1. PDF Assistant: Chat with PDFs")
    st.markdown("#### 2. Image Assistant: Chat with Images")
    st.markdown("#### 3. Website Assistant: Chat with Website content")

    st.sidebar.success("Select App from above")


if check_password():
    main()
