import os
from html import escape

import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Advanced RAG | Document Intelligence",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HTML RENDER HELPER (main fix)
# Streamlit treats lines indented by 4+ spaces as code blocks.
# This strips indentation + blank lines so HTML always renders.
# ============================================================

def render(content: str):
    cleaned = "\n".join(
        line.strip() for line in content.splitlines() if line.strip()
    )
    st.markdown(cleaned, unsafe_allow_html=True)


# ============================================================
# CSS
# ============================================================

render("""
<style>
.stApp { background: #F5F7FB; }
.main .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1450px; }

section[data-testid="stSidebar"] { background: #111827; border-right: 1px solid #1F2937; }
section[data-testid="stSidebar"] * { color: #F9FAFB; }

.hero { background: linear-gradient(135deg, #111827 0%, #172554 55%, #1E3A8A 100%);
  padding: 32px 38px; border-radius: 20px; color: white; margin-bottom: 25px;
  box-shadow: 0 10px 35px rgba(15,23,42,0.15); }
.hero-title { font-size: 34px; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.7px; }
.hero-subtitle { font-size: 15px; color: #CBD5E1; line-height: 1.6; max-width: 850px; }
.badge { display: inline-block; background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.18); padding: 6px 12px; border-radius: 999px;
  font-size: 12px; margin-bottom: 15px; }

.section-title { font-size: 21px; font-weight: 750; color: #111827; margin-top: 25px; margin-bottom: 5px; }
.section-subtitle { font-size: 13px; color: #64748B; margin-bottom: 18px; }

.metric-card { background: white; border: 1px solid #E2E8F0; border-radius: 16px;
  padding: 20px; min-height: 125px; box-shadow: 0 4px 15px rgba(15,23,42,0.04); }
.metric-icon { font-size: 22px; margin-bottom: 8px; }
.metric-label { color: #64748B; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.metric-value { color: #111827; font-size: 28px; font-weight: 800; margin-top: 4px; }
.metric-description { color: #94A3B8; font-size: 11px; margin-top: 3px; }

.pipeline-card { background: white; border: 1px solid #E2E8F0; border-radius: 18px;
  padding: 22px; margin-bottom: 20px; color: #1E293B; line-height: 1.7;
  box-shadow: 0 4px 15px rgba(15,23,42,0.04); }
.pipeline-step { background: white; border: 1px solid #E2E8F0; border-radius: 12px;
  padding: 15px 10px; text-align: center; min-height: 100px; }
.pipeline-icon { font-size: 25px; margin-bottom: 5px; }
.pipeline-name { font-size: 12px; font-weight: 700; color: #1E293B; }
.pipeline-desc { font-size: 10px; color: #64748B; margin-top: 3px; }

.document-card { background: white; border: 1px solid #E2E8F0; border-radius: 14px; padding: 17px; margin-bottom: 12px; }
.document-name { font-size: 14px; font-weight: 700; color: #1E293B; }
.document-meta { font-size: 11px; color: #64748B; margin-top: 5px; }

.answer-card { background: white; border: 1px solid #DCE3ED; border-radius: 18px;
  padding: 25px; box-shadow: 0 5px 20px rgba(15,23,42,0.05); }
.answer-label { font-size: 12px; font-weight: 700; color: #2563EB; text-transform: uppercase; letter-spacing: 0.7px; margin-bottom: 10px; }
.answer-text { color: #1E293B; font-size: 15px; line-height: 1.75; }

.empty-state { background: white; border: 1px solid #E2E8F0; border-radius: 18px;
  padding: 45px; text-align: center; margin-top: 25px; }
.empty-title { font-size: 20px; font-weight: 750; color: #1E293B; margin-top: 10px; }
.empty-text { font-size: 13px; color: #64748B; max-width: 600px; margin: 10px auto 0 auto; line-height: 1.7; }

.stButton > button { border-radius: 10px; font-weight: 700; height: 45px; border: 1px solid #CBD5E1; }
.stTextInput input { border-radius: 11px; border: 1px solid #CBD5E1; padding: 12px; }

.footer { text-align: center; color: #94A3B8; font-size: 11px; padding-top: 35px; padding-bottom: 10px; }
</style>
""")


# ============================================================
# HELPERS
# ============================================================

def get_documents():
    folder = "knowledge_base"
    if not os.path.exists(folder):
        return []
    return sorted(f for f in os.listdir(folder) if f.lower().endswith(".pdf"))


def get_file_size(file_name):
    path = os.path.join("knowledge_base", file_name)
    if not os.path.exists(path):
        return "0 MB"
    return f"{os.path.getsize(path) / (1024 * 1024):.2f} MB"


def section(title, subtitle):
    render(f"""
    <div class="section-title">{title}</div>
    <div class="section-subtitle">{subtitle}</div>
    """)


def metric_card(icon, label, value, description):
    render(f"""
    <div class="metric-card">
    <div class="metric-icon">{icon}</div>
    <div class="metric-label">{label}</div>
    <div class="metric-value">{value}</div>
    <div class="metric-description">{description}</div>
    </div>
    """)


# ============================================================
# SESSION STATE
# ============================================================

st.session_state.setdefault("query", "")
st.session_state.setdefault("search_performed", False)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    render("""
    <div style="padding: 10px 4px 20px 4px;">
    <div style="font-size: 27px; font-weight: 800;">📚 RAG Intelligence</div>
    <div style="font-size: 12px; color: #94A3B8; margin-top: 6px;">Advanced Document Q&A</div>
    </div>
    """)

    st.markdown("---")
    st.markdown("### ⚙️ Retrieval Settings")

    semantic_weight = st.slider("Semantic Search Weight", 0.0, 1.0, 0.60, 0.05)
    keyword_weight = st.slider("Keyword Search Weight", 0.0, 1.0, 0.40, 0.05)
    top_k = st.slider("Hybrid Results", 3, 20, 10)
    rerank_k = st.slider("Final Reranked Results", 1, 10, 3)

    st.markdown("---")
    st.markdown("### 🧠 Search Strategy")
    st.markdown(
        "**Semantic Search** — meaning and context.\n\n"
        "**Keyword Search** — exact terms, names, numbers.\n\n"
        "**Hybrid Search** — combines both.\n\n"
        "**Reranking** — Cross-Encoder re-scores chunks."
    )

    st.markdown("---")
    st.caption("Advanced RAG • Internship Project")


# ============================================================
# HERO
# ============================================================

render("""
<div class="hero">
<div class="badge">⚡ ADVANCED RETRIEVAL-AUGMENTED GENERATION</div>
<div class="hero-title">Intelligent Document Q&A</div>
<div class="hero-subtitle">
Ask questions from your document knowledge base using semantic search,
keyword retrieval, hybrid search and cross-encoder reranking before
generating an AI-powered answer.
</div>
</div>
""")


# ============================================================
# KNOWLEDGE BASE OVERVIEW
# ============================================================

documents = get_documents()

section("📊 Knowledge Base Overview", "Documents currently available for retrieval.")

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("📄", "Documents", len(documents), "PDF knowledge sources")
with c2:
    metric_card("🔎", "Retrieval", "Hybrid", "Semantic + Keyword")
with c3:
    metric_card("🎯", "Reranking", "Active", "Cross-Encoder")
with c4:
    metric_card("🤖", "Generation", "LLM", "Context-grounded answers")


with st.expander("📚 View Knowledge Base Documents", expanded=False):
    if documents:
        cols = st.columns(2)
        for i, doc in enumerate(documents):
            with cols[i % 2]:
                render(f"""
                <div class="document-card">
                <div class="document-name">📄 {escape(doc)}</div>
                <div class="document-meta">PDF Document &nbsp;•&nbsp; {get_file_size(doc)}</div>
                </div>
                """)
    else:
        st.warning("No PDF documents found in the knowledge_base folder.")


# ============================================================
# PIPELINE
# ============================================================

section("🔄 Retrieval Pipeline", "Every question passes through the following retrieval stages.")

pipeline = [
    ("📄", "Documents", "Knowledge Base"),
    ("✂️", "Chunking", "Text Segments"),
    ("🧠", "Semantic", "Vector Search"),
    ("🔤", "Keyword", "BM25 Search"),
    ("🔀", "Hybrid", "Combined Results"),
    ("🎯", "Reranking", "Cross-Encoder"),
    ("🤖", "LLM", "Final Answer"),
]

for col, (icon, name, desc) in zip(st.columns(len(pipeline)), pipeline):
    with col:
        render(f"""
        <div class="pipeline-step">
        <div class="pipeline-icon">{icon}</div>
        <div class="pipeline-name">{name}</div>
        <div class="pipeline-desc">{desc}</div>
        </div>
        """)


# ============================================================
# QUESTION AREA
# ============================================================

section("💬 Ask Your Documents", "Ask a question and retrieve the most relevant information from the knowledge base.")

query = st.text_input(
    "Your question",
    placeholder="Example: What are the Learning Commons reservation rules?",
    label_visibility="collapsed",
)

b1, b2, _ = st.columns([1, 1, 4])
with b1:
    search_button = st.button("🔎 Search Documents", use_container_width=True, type="primary")
with b2:
    clear_button = st.button("✕ Clear", use_container_width=True)

if clear_button:
    st.session_state.query = ""
    st.session_state.search_performed = False
    st.rerun()

if search_button:
    if not query.strip():
        st.warning("Please enter a question first.")
    else:
        st.session_state.query = query
        st.session_state.search_performed = True


# ============================================================
# RESULTS
# ============================================================

if st.session_state.search_performed:
    current_query = escape(st.session_state.query)

    section("🔍 Retrieval Analysis", "Overview of the retrieval run for your question.")

    render(f"""
    <div class="answer-card">
    <div class="answer-label">User Query</div>
    <div class="answer-text">{current_query}</div>
    </div>
    """)

    st.write("")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Semantic Candidates", "—", "Vector Search")
    m2.metric("Keyword Candidates", "—", "BM25")
    m3.metric("Hybrid Candidates", str(top_k), "Retrieved")
    m4.metric("Reranked Results", str(rerank_k), "Final Context")

    tab1, tab2, tab3 = st.tabs(
        ["🧠 Semantic Search", "🔤 Keyword Search", "🔀 Hybrid + Reranking"]
    )

    with tab1:
        st.markdown("### Semantic Retrieval")
        st.info("Semantic search will retrieve chunks based on meaning using vector embeddings.")
        st.caption("Backend integration: src/semantic_search.py")

    with tab2:
        st.markdown("### Keyword Retrieval")
        st.info("BM25 keyword search will identify chunks containing important terms from the query.")
        st.caption("Backend integration: src/keyword_search.py")

    with tab3:
        st.markdown("### Hybrid Search → Reranking")
        render("""
        <div class="pipeline-card">
        <b>Step 1 — Hybrid Retrieval</b><br>Semantic and keyword results are combined.<br><br>
        <b>Step 2 — Candidate Selection</b><br>The highest-quality candidate chunks are selected.<br><br>
        <b>Step 3 — Cross-Encoder Reranking</b><br>Each question/chunk pair receives a relevance score.<br><br>
        <b>Step 4 — Final Context</b><br>Only the highest-ranked chunks are passed to the LLM.
        </div>
        """)

    section("📑 Retrieved Results", "Candidate chunks selected before final answer generation.")
    st.info("Actual retrieved chunks will appear here after the retrieval modules are connected.")

    section("🎯 Reranking Results", "Cross-Encoder relevance scoring and final context selection.")
    st.info("The reranker will score each retrieved question/chunk pair and sort the results by relevance.")

    section("🤖 AI Answer", "Generated from the top reranked chunks.")
    render("""
    <div class="answer-card">
    <div class="answer-label">Context-Grounded Response</div>
    <div class="answer-text">
    The final AI-generated answer will appear here after the hybrid retrieval,
    reranking and LLM modules are connected.
    </div>
    </div>
    """)

else:
    render("""
    <div class="empty-state">
    <div style="font-size:45px;">🔎</div>
    <div class="empty-title">Ready to Search</div>
    <div class="empty-text">
    Enter a question above to start the Advanced RAG pipeline. Your query will
    pass through semantic search, keyword search, hybrid retrieval and reranking
    before generating the final answer.
    </div>
    </div>
    """)


# ============================================================
# FOOTER
# ============================================================

render("""
<div class="footer">
Advanced RAG with Hybrid Search &amp; Reranking &nbsp;•&nbsp; Document Intelligence System
</div>
""")
