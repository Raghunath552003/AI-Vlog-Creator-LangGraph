"""
Vlog Creator - Streamlit Web UI (v2 - with SEO Agent)
Run with: streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv
from main import build_graph

load_dotenv()

st.set_page_config(page_title="Vlog Creator AI", page_icon="🎬", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #0f0f0f; }
    .hero-title {
        font-size: 2.6rem; font-weight: 800; color: #ffffff;
        text-align: center; letter-spacing: -1px; margin-bottom: 0.2rem;
    }
    .hero-sub { font-size: 1rem; color: #888888; text-align: center; margin-bottom: 2rem; }
    .badge {
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-size: 0.78rem; font-weight: 600; margin-right: 8px; margin-bottom: 8px;
    }
    .badge-research { background:#1a2e1a; color:#4ade80; border:1px solid #166534; }
    .badge-writing  { background:#1e1a2e; color:#a78bfa; border:1px solid #4c1d95; }
    .badge-seo      { background:#2a1a10; color:#fb923c; border:1px solid #7c2d12; }
    .section-label {
        font-size: 0.75rem; font-weight: 700; letter-spacing: 2px;
        text-transform: uppercase; color: #555555;
        margin-top: 1.5rem; margin-bottom: 0.4rem;
    }
    .output-box {
        background:#1a1a1a; border:1px solid #2a2a2a; border-radius:12px;
        padding:1.2rem 1.4rem; color:#cccccc; font-size:0.92rem;
        line-height:1.7; white-space:pre-wrap; margin-bottom:1rem;
    }
    .script-box {
        background:#111827; border:1px solid #1e3a5f;
        border-left:4px solid #3b82f6; border-radius:12px;
        padding:1.4rem 1.6rem; color:#e2e8f0;
        font-size:0.93rem; line-height:1.85; white-space:pre-wrap;
    }
    .seo-box {
        background:#130f09; border:1px solid #431407;
        border-left:4px solid #f97316; border-radius:12px;
        padding:1.4rem 1.6rem; color:#fed7aa;
        font-size:0.93rem; line-height:1.85; white-space:pre-wrap;
    }
    .result-card {
        background:#161616; border:1px solid #2a2a2a; border-radius:10px;
        padding:0.8rem 1rem; margin-bottom:0.6rem; color:#aaaaaa; font-size:0.88rem;
    }
    .result-title { color:#60a5fa; font-weight:600; font-size:0.92rem; }
    .result-link  { color:#555555; font-size:0.78rem; word-break:break-all; }
    .stButton > button {
        background:#2563eb; color:white; border:none; border-radius:10px;
        padding:0.65rem 2rem; font-size:1rem; font-weight:600; width:100%;
    }
    .stButton > button:hover { background:#1d4ed8; }
    .stTextInput > div > input {
        background:#1a1a1a; border:1px solid #333333; border-radius:10px;
        color:#ffffff; font-size:1rem; padding:0.7rem 1rem;
    }
    #MainMenu, footer, header { visibility: hidden; }
    hr { border-color: #222222; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<div class="hero-title">🎬 Vlog Creator AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Three AI agents: Research → Script → SEO Package</div>', unsafe_allow_html=True)

with st.expander("How it works"):
    st.markdown("""
**Agent 1 — Research Agent**
Searches the internet (SerpAPI) or uses GPT knowledge to gather facts, trends, and insights on your topic.

**Agent 2 — Vlog Writer Agent**
Turns the research into a full vlog script — hook, intro, main segments, and outro.

**Agent 3 — SEO Optimizer Agent** *(new!)*
Takes your finished script and generates a complete YouTube SEO package:
- 3 title options
- Full video description
- 15 tags
- Thumbnail concept
    """)

st.markdown("---")

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
topic = st.text_input(
    "Vlog topic",
    placeholder="e.g. Artificial Intelligence, Best Travel Destinations 2026",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate = st.button("Generate Script + SEO")

# ---------------------------------------------------------------------------
# Run agents
# ---------------------------------------------------------------------------
if generate:
    if not topic.strip():
        st.warning("Please enter a vlog topic first.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY is missing from your .env file.")
    else:
        st.markdown("---")
        status = st.empty()
        status.markdown('<span class="badge badge-research">Research Agent running...</span>', unsafe_allow_html=True)

        try:
            app = build_graph()

            with st.spinner("All three agents are working..."):
                final_state = app.invoke({
                    "topic": topic.strip(),
                    "search_results": [],
                    "research_summary": "",
                    "vlog_script": "",
                    "seo_output": "",
                })

            status.markdown(
                '<span class="badge badge-research">Research done</span>'
                '<span class="badge badge-writing">Script done</span>'
                '<span class="badge badge-seo">SEO done</span>',
                unsafe_allow_html=True
            )

            # --- Web Sources ---
            search_results = final_state.get("search_results", [])
            if search_results:
                st.markdown('<div class="section-label">Web Sources Found</div>', unsafe_allow_html=True)
                for r in search_results:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">{r.get('title','')}</div>
                        <div style="color:#aaaaaa;margin:4px 0">{r.get('snippet','')}</div>
                        <div class="result-link">{r.get('link','')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div class="section-label">Research Summary</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="output-box">{final_state["research_summary"]}</div>', unsafe_allow_html=True)

            # --- Vlog Script ---
            st.markdown('<div class="section-label">Vlog Script</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="script-box">{final_state["vlog_script"]}</div>', unsafe_allow_html=True)

            # --- SEO Package ---
            st.markdown('<div class="section-label">SEO Package</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="seo-box">{final_state["seo_output"]}</div>', unsafe_allow_html=True)

            # --- Downloads ---
            st.markdown('<div class="section-label">Download</div>', unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(
                    label="Download Script (.txt)",
                    data=final_state["vlog_script"],
                    file_name=f"{topic.strip().replace(' ','_')}_script.txt",
                    mime="text/plain",
                )
            with col_b:
                st.download_button(
                    label="Download SEO Package (.txt)",
                    data=final_state["seo_output"],
                    file_name=f"{topic.strip().replace(' ','_')}_seo.txt",
                    mime="text/plain",
                )

        except Exception as e:
            status.empty()
            st.error(f"Something went wrong: {e}")