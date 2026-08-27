import streamlit as st
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="UpCareer AI - AI Career Mentor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

st.title("🤖 AI Career Mentor")
st.markdown("---")
st.markdown(
    """
    <div class="premium-card">
        <h3>Coming Soon</h3>
        <p class="secondary-text">
            Chat with your personal AI career mentor for tailored advice,
            study tips, interview prep, and motivation.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
