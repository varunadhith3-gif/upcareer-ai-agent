import streamlit as st
import time
import google.generativeai as genai
from duckduckgo_search import DDGS
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="UpCareer AI - Autonomous AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

st.markdown("""
<div style='padding:2rem 0 1.4rem 0;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:1.8rem;'>
    <div style='display:inline-flex;align-items:center;gap:0.4rem;background:rgba(72,199,142,0.10);
        border:1px solid rgba(72,199,142,0.25);border-radius:20px;padding:0.22rem 0.75rem;
        font-size:0.8rem;font-weight:600;color:#48C78E;margin-bottom:0.6rem;'>
        ⚡ &nbsp;Autonomous Agent Mode Active (Rate-Limit Protected)
    </div>
    <div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800;color:#FFFFFF;
        letter-spacing:-0.5px;margin:0 0 0.4rem 0;'>
        AI Career Agent
    </div>
    <div style='font-size:0.84rem;color:#888;max-width:650px;line-height:1.6;'>
        This agent manages your profile and browses the live web with robust tool execution support.
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.get("analysis_complete", False):
    st.warning("⚠️ No resume profile found! Please run your analysis on the **Resume Analysis** page first.")
    st.stop()

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("❌ Missing `GEMINI_API_KEY` in your `.streamlit/secrets.toml` file.")
    st.stop()

genai.configure(api_key=api_key)

# ── Define Agent Tools ────────────────────────────────────────────────────────
def tool_update_target_role(new_role: str) -> str:
    """Updates the user's target career role in session memory."""
    st.session_state["target_role"] = new_role
    return f"Successfully updated target role to {new_role}."

def tool_graduate_skill(skill_name: str) -> str:
    """Moves a specified skill from missing/partial into mastered state and boosts readiness."""
    match_res = st.session_state.get("match_results", {})
    evaluated = match_res.get("evaluated", {"mastered": [], "partial": [], "missing": []})
    
    skill_clean = skill_name.strip().title()
    
    evaluated["missing"] = [s for s in evaluated.get("missing", []) if (str(s[0]).title() if isinstance(s, (list,tuple)) else str(s).title()) != skill_clean]
    evaluated["partial"] = [s for s in evaluated.get("partial", []) if (str(s[0]).title() if isinstance(s, (list,tuple)) else str(s).title()) != skill_clean]
    
    mastered = evaluated.get("mastered", [])
    if not any((str(s[0]).title() if isinstance(s, (list,tuple)) else str(s).title()) == skill_clean for s in mastered):
        mastered.append((skill_clean, 0.95))
        evaluated["mastered"] = mastered
        
    st.session_state["skills_present"] = len(mastered)
    st.session_state["skills_partial"] = len(evaluated["partial"])
    st.session_state["skills_missing"] = len(evaluated["missing"])
    
    current_score = st.session_state.get("readiness_score", 50)
    st.session_state["readiness_score"] = min(100, current_score + 8)
    
    return f"Skill '{skill_clean}' has been successfully graduated to Mastered! Readiness score boosted."

def tool_search_web(query: str) -> str:
    """Searches the live web using DuckDuckGo for courses, tutorials, documentation, and career resources."""
    try:
        results = DDGS().text(query, max_results=3)
        formatted = []
        for r in results:
            formatted.append(f"Title: {r.get('title')}\nURL: {r.get('href')}\nSnippet: {r.get('body')}\n")
        return "\n".join(formatted) if formatted else "No live web results found."
    except Exception as e:
        return f"Web search error: {e}"

model = genai.GenerativeModel(
    model_name="gemini-3.6-flash",
    tools=[tool_update_target_role, tool_graduate_skill, tool_search_web]
)

target_role = st.session_state.get("target_role", "Software Engineer")
readiness_score = st.session_state.get("readiness_score", 0)
evaluated = st.session_state["match_results"]["evaluated"]

def extract_skill_names(skill_list):
    return [str(s[0]).title() if isinstance(s, (tuple, list)) else str(s).title() for s in skill_list]

missing_skills = extract_skill_names(evaluated.get("missing", []))
partial_skills = extract_skill_names(evaluated.get("partial", []))

system_instruction = f"""
You are an autonomous AI Career Agent with full control over the user's application state and live web browsing tools.
Current User Context:
- Target Role: {target_role}
- Readiness Score: {readiness_score}/100
- Missing Skills: {", ".join(missing_skills) if missing_skills else "None"}
- Partial Skills: {", ".join(partial_skills) if partial_skills else "None"}

If the user asks to change target role or graduate a skill, call the tool. If they ask for learning resources to close missing skills, use `tool_search_web` to fetch real-world results and present them clearly with links.
"""

if "agent_chat" not in st.session_state:
    st.session_state["agent_chat"] = model.start_chat(enable_automatic_function_calling=True)
    try:
        st.session_state["agent_chat"].send_message(system_instruction)
    except Exception as e:
        st.toast("⚡ API quota reached during mentor initialization. Running in offline fallback mode.", icon="⚠️")

# Safe history rendering
try:
    history = st.session_state["agent_chat"].history
    for message in history[1:]: 
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            for part in message.parts:
                if part.text:
                    st.markdown(part.text)
except Exception:
    pass

if user_input := st.chat_input("Ask your agent to search the web or manage your profile..."):
    with st.chat_message("user"):
        st.markdown(user_input)
        
    with st.chat_message("assistant"):
        with st.spinner("Agent is reasoning / calling tools / searching the web..."):
            success = False
            attempts = 0
            max_attempts = 2
            response = None
            
            while not success and attempts < max_attempts:
                try:
                    response = st.session_state["agent_chat"].send_message(user_input)
                    success = True
                except Exception as e:
                    err_str = str(e)
                    if "429" in err_str or "quota" in err_str.lower():
                        attempts += 1
                        if attempts < max_attempts:
                            st.warning("⏳ Free tier rate limit hit. Pausing briefly before auto-retrying...")
                            time.sleep(15)
                        else:
                            # Graceful offline mentor fallback response when quota is fully dead
                            success = True
                            class MockResponse:
                                text = f"⚠️ **API Quota Exceeded (429)**: The Gemini free tier limit has been reached. However, I can still help you review your target role (**{target_role}**) and missing skills (**{', '.join(missing_skills[:3])}**). Try running web searches or check your Skill Gap Report for offline tracking."
                            response = MockResponse()
                    else:
                        success = True
                        class MockResponse:
                            text = f"Agent encountered an error: {e}"
                        response = MockResponse()
            
            if success and response:
                st.markdown(response.text)