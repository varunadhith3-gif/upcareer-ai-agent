import streamlit as st
import boto3
import sys
import os

# -- Make core/ importable from the pages/ subdirectory -------------------------
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.mentor_tools import (
    detect_career_change_intent,
    apply_career_change,
    build_mentor_system_prompt,
    SUPPORTED_ROLES,
)
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="AI Career Mentor - UpCareer AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()

# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.markdown("""
<div style='padding:2rem 0 1.4rem 0;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:1.8rem;'>
    <div style='display:inline-flex;align-items:center;gap:0.4rem;background:rgba(99,102,241,0.10);
        border:1px solid rgba(99,102,241,0.28);border-radius:20px;padding:0.22rem 0.75rem;
        font-size:0.8rem;font-weight:600;color:#818CF8;margin-bottom:0.6rem;'>
        Powered by Amazon Nova Micro
    </div>
    <div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800;color:#FFFFFF;
        letter-spacing:-0.5px;margin:0 0 0.4rem 0;'>
        AI Career Mentor
    </div>
    <div style='font-size:0.84rem;color:#888;max-width:680px;line-height:1.6;'>
        Ask anything about your career path, interview prep, or skill gaps.
        Tell the mentor to <em>switch your target role</em> and it will instantly
        update your roadmap &amp; progress tracker — no page reload needed.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Context panel (collapsible)
# ---------------------------------------------------------------------------
if st.session_state.get("analysis_complete", False):
    with st.expander("Your current profile snapshot", expanded=False):
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Target Role",  st.session_state.get("target_role", "—"))
        col_b.metric("Readiness",    f"{st.session_state.get('readiness_score', '—')}/100")
        col_c.metric("Study Budget", f"{st.session_state.get('study_bandwidth', 10)} hrs/wk")

        match_res = st.session_state.get("match_results", {})
        evaluated = match_res.get("evaluated", {})
        missing   = [s[0] if isinstance(s, (list, tuple)) else s
                     for s in evaluated.get("missing", [])]
        if missing:
            st.markdown(
                "<span style='font-size:0.8rem;color:#FF5252;font-weight:600;'>Missing skills: </span>"
                f"<span style='font-size:0.8rem;color:#AAA;'>{', '.join(missing)}</span>",
                unsafe_allow_html=True,
            )
else:
    st.info("Upload your resume on the **Resume Analysis** page first to give the mentor full context about your profile.")

# ---------------------------------------------------------------------------
# Bedrock / Nova Micro invocation (kept fully intact)
# ---------------------------------------------------------------------------
def invoke_nova_mentor(
    chat_history_messages: list[dict],
    user_input: str,
    system_prompt: str,
) -> str:
    """
    Calls Amazon Nova Micro via the Bedrock Converse API.
    The system_prompt argument injects live profile context as a system turn.
    """
    try:
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1",
        )
        model_id = "amazon.nova-micro-v1:0"

        formatted_messages: list[dict] = []

        # Add system context as the first user/assistant exchange so Nova Micro
        # sees it without needing a dedicated system field (Converse API compat).
        if system_prompt and not chat_history_messages:
            # Only inject on the very first message of the session
            formatted_messages.append({
                "role": "user",
                "content": [{"text": f"[CONTEXT FOR YOU ONLY — do not quote back]\n{system_prompt}"}],
            })
            formatted_messages.append({
                "role": "assistant",
                "content": [{"text": "Understood. I'm ready to help based on your profile."}],
            })

        for msg in chat_history_messages:
            role = "user" if msg["role"] == "user" else "assistant"
            formatted_messages.append({
                "role":    role,
                "content": [{"text": msg["content"]}],
            })

        formatted_messages.append({
            "role":    "user",
            "content": [{"text": user_input}],
        })

        response = client.converse(
            modelId=model_id,
            messages=formatted_messages,
            inferenceConfig={"maxTokens": 1024, "temperature": 0.7},
        )

        return response["output"]["message"]["content"][0]["text"]

    except Exception as e:
        return f"Error communicating with Amazon Bedrock (Nova Micro): {str(e)}"


# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
if "mentor_messages" not in st.session_state:
    st.session_state["mentor_messages"] = []

# Pending role change detected last turn — waiting for user to confirm/dismiss
if "mentor_pending_role" not in st.session_state:
    st.session_state["mentor_pending_role"] = None

# ---------------------------------------------------------------------------
# Pending role-change banner (shown at top, before chat history)
# ---------------------------------------------------------------------------
pending_role = st.session_state.get("mentor_pending_role")
if pending_role:
    st.markdown(
        f"""
        <div style='background:rgba(72,199,142,0.10);border:1px solid rgba(72,199,142,0.30);
            border-radius:12px;padding:1rem 1.2rem;margin-bottom:1.2rem;'>
            <strong style='color:#48C78E;'>Career path change detected</strong><br>
            <span style='color:#CCC;font-size:0.9rem;'>
                The mentor suggested switching your target role to
                <strong style='color:#FFC107;'>{pending_role}</strong>.
                Apply this change to sync your Roadmap &amp; Progress Tracker?
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_yes, col_no, _ = st.columns([1, 1, 4])
    with col_yes:
        if st.button("Apply change", key="apply_role_change", type="primary"):
            with st.spinner(f"Re-evaluating your profile for {pending_role}..."):
                success = apply_career_change(pending_role)
            if success:
                st.session_state["mentor_pending_role"] = None
                st.toast(
                    f"Target role updated to **{pending_role}**! "
                    "Career Roadmap & Progress Tracker are now in sync."
                )
                st.rerun()
            else:
                st.error("Could not apply the change — no resume data found. Please run Resume Analysis first.")
    with col_no:
        if st.button("Dismiss", key="dismiss_role_change"):
            st.session_state["mentor_pending_role"] = None
            st.rerun()

st.divider()

# ---------------------------------------------------------------------------
# Chat history display
# ---------------------------------------------------------------------------
for message in st.session_state["mentor_messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------------------------
# Chat input handler
# ---------------------------------------------------------------------------
if user_prompt := st.chat_input("Ask your mentor anything — or say 'Switch my role to Data Scientist'..."):

    # Show user bubble immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state["mentor_messages"].append({"role": "user", "content": user_prompt})

    # Build fresh system prompt with current profile data
    system_prompt = build_mentor_system_prompt()

    # Call Nova Micro (Bedrock Converse — unchanged)
    with st.chat_message("assistant"):
        with st.spinner("Thinking with Nova Micro..."):
            response_text = invoke_nova_mentor(
                st.session_state["mentor_messages"][:-1],
                user_prompt,
                system_prompt,
            )
        st.markdown(response_text)

    st.session_state["mentor_messages"].append({"role": "assistant", "content": response_text})

    # ------------------------------------------------------------------
    # Intent detection — runs AFTER the Bedrock response is committed
    # ------------------------------------------------------------------
    detected_role = detect_career_change_intent(user_prompt, response_text)

    if detected_role:
        # If resume data is present, auto-apply silently and notify via toast
        if st.session_state.get("resume_text", "").strip():
            with st.spinner(f"Syncing your profile to {detected_role}..."):
                success = apply_career_change(detected_role)
            if success:
                st.toast(
                    f"Career path updated to **{detected_role}**! "
                    "Roadmap & Progress Tracker are in sync."
                )
                st.rerun()
        else:
            # No resume yet — surface a banner so user can confirm manually later
            st.session_state["mentor_pending_role"] = detected_role
            st.rerun()

# ---------------------------------------------------------------------------
# Sidebar quick-actions: role chips
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        "<div style='padding-top:1.2rem;border-top:1px solid rgba(255,255,255,0.06);margin-top:1rem;'>"
        "<div style='font-size:0.75rem;font-weight:700;color:#888;text-transform:uppercase;"
        "letter-spacing:0.06em;margin-bottom:0.5rem;'>Quick role switch</div></div>",
        unsafe_allow_html=True,
    )
    for role_opt in SUPPORTED_ROLES:
        is_active = role_opt == st.session_state.get("target_role", "")
        btn_label = f"{'● ' if is_active else ''}{role_opt}"
        if st.button(
            btn_label,
            key=f"quick_role_{role_opt}",
            use_container_width=True,
            disabled=is_active,
        ):
            if st.session_state.get("resume_text", "").strip():
                with st.spinner(f"Switching to {role_opt}..."):
                    apply_career_change(role_opt)
                # Append a mentor message confirming the switch
                confirm_msg = (
                    f"I've updated your target role to **{role_opt}**. "
                    f"Your Career Roadmap and Progress Tracker have been refreshed with the new skill gaps for this role. "
                    f"Head over to the Career Roadmap page to see your updated action plan!"
                )
                st.session_state["mentor_messages"].append(
                    {"role": "assistant", "content": confirm_msg}
                )
                st.toast(f"Switched to {role_opt}.")
                st.rerun()
            else:
                st.warning("Upload your resume first to switch roles.")
