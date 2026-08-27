import streamlit as st
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="UpCareer AI - Profile Settings",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

st.title("⚙️ Profile Settings")
st.markdown("---")
st.markdown(
    """
    <div class="premium-card">
        <h3>Coming Soon</h3>
        <p class="secondary-text">
            Manage your profile, set your target role, configure study bandwidth,
            and update account preferences.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
