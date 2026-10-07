import os
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Advanced RAG | Document Intelligence",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    .stApp {
        background: #F5F7FB;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #1F2937;
    }

    section[data-testid="stSidebar"] * {
        color: #F9FAFB;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #F9FAFB;
    }

    /* ---------- Header ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #111827 0%,
            #172554 55%,
            #1E3A8A 100%
        );

        padding: 32px 38px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 35px rgba(15, 23, 42, 0.15);
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: -0.7px;
    }

    .hero-subtitle {
        font-size: 15px;
        color: #CBD5E1;
        line-height: 1.6;
        max-width: 850px;
    }

    .badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.18);
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 12px;
        margin-bottom: 15px;
    }

    /* ---------- Section Titles ---------- */

    .section-title {
        font-size: 21px;
        font-weight: 750;
        color: #111827;
        margin-top: 25px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        font-size: 13px;
        color: #64748B;
        margin-bottom: 18px;
    }

    /* ---------- Metric Cards ---------- */

    .metric-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
    }

    .metric-icon {
        font-size: 22px;
        margin-bottom: 8px;
    }

    .metric-label {
        color: #64748B;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-value {
        color: #111827;
        font-size: 28px;
        font-weight: 800;
        margin-top: 4px;
    }

    .metric-description {
        color: #94A3B8;
        font-size: 11px;
        margin-top: 3px;
    }

    /* ---------- Pipeline ---------- */

    .pipeline-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
    }

    .pipeline-step {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 15px 10px;
        text-align: center;
        min-height: 100px;
    }

    .pipeline-icon {
        font-size: 25px;
        margin-bottom: 5px;
    }

    .pipeline-name {
        font-size: 12px;
        font-weight: 700;
        color: #1E293B;
    }

    .pipeline-desc {
        font-size: 10px;
        color: #64748B;
        margin-top: 3px;
    }

    /* ---------- Document Cards ---------- */

    .document-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 17px;
        margin-bottom: 12px;
    }

    .document-name {
        font-size: 14px;
        font-weight: 700;
        color: #1E293B;
    }

    .document-meta {
        font-size: 11px;
        color: #64748B;
        margin-top: 5px;
    }

    /* ---------- Result Cards ---------- */

    .result-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #2563EB;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 13px;
    }

    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 9px;
    }

    .result-title {
        font-size: 14px;
        font-weight: 750;
        color: #1E293B;
    }

    .score {
        background: #EFF6FF;
        color: #1D4ED8;
        border-radius: 999px;
        padding: 5px 10px;
        font-size: 11px;
        font-weight: 700;
    }

    .result-text {
        color: #475569;
        font-size: 13px;
        line-height: 1.65;
    }

    /* ---------- Answer ---------- */

    .answer-card {
        background: white;
        border: 1px solid #DCE3ED;
        border-radius: 18px;
        padding: 25px;
        box-shadow: 0 5px 20px rgba(15, 23, 42, 0.05);
    }

    .answer-label {
        font-size: 12px;
        font-weight: 700;
        color: #2563EB;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        margin-bottom: 10px;
    }

    .answer-text {
        color: #1E293B;
        font-size: 15px;
        line-height: 1.75;
    }

    /* ---------- Status ---------- */

    .status-success {
        background: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
        border-radius: 10px;
        padding: 11px 14px;
        font-size: 12px;
        font-weight: 600;
    }

    .status-warning {
        background: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
        border-radius: 10px;
        padding: 11px 14px;
        font-size: 12px;
        font-weight: 600;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        height: 45px;
        border: 1px solid #CBD5E1;
    }

    /* ---------- Input ---------- */

    .stTextInput input {
        border-radius: 11px;
        border: 1px solid #CBD5E1;
        padding: 12px;
    }

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 11px;
        padding-top: 35px;
        padding-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_documents():
    """Return PDF files available in the knowledge base."""

    knowledge_base = "knowledge_base"

    if not os.path.exists(knowledge_base):
        return []

    documents = []

    for file_name in os.listdir(knowledge_base):
        if file_name.lower().endswith(".pdf"):
            documents.append(file_name)

    return sorted(documents)


def get_file_size(file_name):
    """Return document size in MB."""

    file_path = os.path.join("knowledge_base", file_name)

    if not os.path.exists(file_path):
        return "0 MB"

    size = os.path.getsize(file_path) / (1024 * 1024)

    return f"{size:.2f} MB"


# ============================================================
# SESSION STATE
# ============================================================

if "query" not in st.session_state:
    st.session_state.query = ""

if "search_performed" not in st.session_state:
    st.session_state.search_performed = False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 10px 4px 20px 4px;">
            <div style="font-size: 27px; font-weight: 800;">
                📚 RAG Intelligence
            </div>
            <div style="font-size: 12px; color: #94A3B8; margin-top: 6px;">
                Advanced Document Q&A
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ⚙️ Retrieval Settings")

    semantic_weight = st.slider(
        "Semantic Search Weight",
        min_value=0.0,
        max_value=1.0,
        value=0.60,
        step=0.05
    )

    keyword_weight = st.slider(
        "Keyword Search Weight",
        min_value=0.0,
        max_value=1.0,
        value=0.40,
        step=0.05
    )

    top_k = st.slider(
        "Hybrid Results",
        min_value=3,
        max_value=20,
        value=10
    )

    rerank_k = st.slider(
        "Final Reranked Results",
        min_value=1,
        max_value=10,
        value=3
    )

    st.markdown("---")

    st.markdown("### 🧠 Search Strategy")

    st.markdown(
        """
        **Semantic Search**

        Finds content based on meaning and context.

        **Keyword Search**

        Finds exact terms, names, numbers and phrases.

        **Hybrid Search**

        Combines both retrieval strategies.

        **Reranking**

        Re-evaluates retrieved chunks using a Cross-Encoder.
        """
    )

    st.markdown("---")

    st.caption("Advanced RAG • Internship Project")


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="badge">
            ⚡ ADVANCED RETRIEVAL-AUGMENTED GENERATION
        </div>

        <div class="hero-title">
            Intelligent Document Q&A
        </div>

        <div class="hero-subtitle">
            Ask questions from your document knowledge base using
            semantic search, keyword retrieval, hybrid search and
            cross-encoder reranking before generating an AI-powered answer.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# KNOWLEDGE BASE
# ============================================================

documents = get_documents()

st.markdown(
    '<div class="section-title">📊 Knowledge Base Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Documents currently available for retrieval.</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">📄</div>
            <div class="metric-label">Documents</div>
            <div class="metric-value">{len(documents)}</div>
            <div class="metric-description">PDF knowledge sources</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-icon">🔎</div>
            <div class="metric-label">Retrieval</div>
            <div class="metric-value">Hybrid</div>
            <div class="metric-description">Semantic + Keyword</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-icon">🎯</div>
            <div class="metric-label">Reranking</div>
            <div class="metric-value">Active</div>
            <div class="metric-description">Cross-Encoder</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-icon">🤖</div>
            <div class="metric-label">Generation</div>
            <div class="metric-value">LLM</div>
            <div class="metric-description">Context-grounded answers</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DOCUMENT LIST
# ============================================================

with st.expander("📚 View Knowledge Base Documents", expanded=False):

    if documents:

        doc_columns = st.columns(2)

        for index, document in enumerate(documents):

            with doc_columns[index % 2]:

                st.markdown(
                    f"""
                    <div class="document-card">

                        <div class="document-name">
                            📄 {document}
                        </div>

                        <div class="document-meta">
                            PDF Document &nbsp; • &nbsp;
                            {get_file_size(document)}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.warning(
            "No PDF documents found in the knowledge_base folder."
        )


# ============================================================
# RAG PIPELINE VISUALIZATION
# ============================================================

st.markdown(
    '<div class="section-title">🔄 Retrieval Pipeline</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Every question passes through the following retrieval stages.</div>',
    unsafe_allow_html=True
)

pipeline = [
    ("📄", "Documents", "Knowledge Base"),
    ("✂️", "Chunking", "Text Segments"),
    ("🧠", "Semantic", "Vector Search"),
    ("🔤", "Keyword", "BM25 Search"),
    ("🔀", "Hybrid", "Combined Results"),
    ("🎯", "Reranking", "Cross-Encoder"),
    ("🤖", "LLM", "Final Answer")
]

pipeline_columns = st.columns(len(pipeline))

for index, (icon, name, description) in enumerate(pipeline):

    with pipeline_columns[index]:

        st.markdown(
            f"""
            <div class="pipeline-step">

                <div class="pipeline-icon">
                    {icon}
                </div>

                <div class="pipeline-name">
                    {name}
                </div>

                <div class="pipeline-desc">
                    {description}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# QUESTION AREA
# ============================================================

st.markdown(
    '<div class="section-title">💬 Ask Your Documents</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Ask a question and retrieve the most relevant information from the knowledge base.</div>',
    unsafe_allow_html=True
)

query = st.text_input(
    "Your question",
    placeholder="Example: What are the Learning Commons reservation rules?",
    label_visibility="collapsed"
)

search_col1, search_col2, search_col3 = st.columns([1, 1, 4])

with search_col1:

    search_button = st.button(
        "🔎 Search Documents",
        use_container_width=True,
        type="primary"
    )

with search_col2:

    clear_button = st.button(
        "✕ Clear",
        use_container_width=True
    )


# ============================================================
# CLEAR
# ============================================================

if clear_button:

    st.session_state.query = ""
    st.session_state.search_performed = False
    st.rerun()


# ============================================================
# SEARCH EXECUTION
# ============================================================

if search_button:

    if not query.strip():

        st.warning("Please enter a question first.")

    else:

        st.session_state.query = query
        st.session_state.search_performed = True


# ============================================================
# SEARCH RESULTS AREA
# ============================================================

if st.session_state.search_performed:

    current_query = st.session_state.query

    st.markdown(
        '<div class="section-title">🔍 Retrieval Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="answer-card">

            <div class="answer-label">
                USER QUERY
            </div>

            <div class="answer-text">
                {current_query}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # Retrieval Metrics
    # --------------------------------------------------------

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            "Semantic Candidates",
            "—",
            "Vector Search"
        )

    with metric2:
        st.metric(
            "Keyword Candidates",
            "—",
            "BM25"
        )

    with metric3:
        st.metric(
            "Hybrid Candidates",
            str(top_k),
            "Retrieved"
        )

    with metric4:
        st.metric(
            "Reranked Results",
            str(rerank_k),
            "Final Context"
        )

    # --------------------------------------------------------
    # Search tabs
    # --------------------------------------------------------

    tab1, tab2, tab3 = st.tabs(
        [
            "🧠 Semantic Search",
            "🔤 Keyword Search",
            "🔀 Hybrid + Reranking"
        ]
    )

    with tab1:

        st.markdown("### Semantic Retrieval")

        st.info(
            "Semantic search will retrieve chunks based on "
            "meaning using vector embeddings."
        )

        st.caption(
            "Backend integration: src/semantic_search.py"
        )

    with tab2:

        st.markdown("### Keyword Retrieval")

        st.info(
            "BM25 keyword search will identify documents containing "
            "important terms from the query."
        )

        st.caption(
            "Backend integration: src/keyword_search.py"
        )

    with tab3:

        st.markdown("### Hybrid Search → Reranking")

        st.markdown(
            """
            <div class="pipeline-card">

                <b>Step 1 — Hybrid Retrieval</b><br>
                Semantic and keyword results are combined.

                <br><br>

                <b>Step 2 — Candidate Selection</b><br>
                The highest-quality candidate chunks are selected.

                <br><br>

                <b>Step 3 — Cross-Encoder Reranking</b><br>
                Each question/chunk pair receives a relevance score.

                <br><br>

                <b>Step 4 — Final Context</b><br>
                Only the highest-ranked chunks are passed to the LLM.

            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # Retrieved Results
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📑 Retrieved Results</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Candidate chunks selected before final answer generation.</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Actual retrieved chunks will appear here after the retrieval modules "
        "are connected."
    )

    # --------------------------------------------------------
    # Reranking
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🎯 Reranking Results</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Cross-Encoder relevance scoring and final context selection.</div>',
        unsafe_allow_html=True
    )

    st.info(
        "The reranker will score each retrieved question/chunk pair and "
        "sort the results by relevance."
    )

    # --------------------------------------------------------
    # Final Answer
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🤖 AI Answer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="answer-card">

            <div class="answer-label">
                CONTEXT-GROUNDED RESPONSE
            </div>

            <div class="answer-text">

                The final AI-generated answer will appear here after
                the hybrid retrieval, reranking and LLM modules are
                connected.

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# EMPTY STATE
# ============================================================

else:

    st.markdown(
        """
        <div style="
            background:white;
            border:1px solid #E2E8F0;
            border-radius:18px;
            padding:45px;
            text-align:center;
            margin-top:25px;
        ">

            <div style="font-size:45px;">
                🔎
            </div>

            <div style="
                font-size:20px;
                font-weight:750;
                color:#1E293B;
                margin-top:10px;
            ">
                Ready to Search
            </div>

            <div style="
                font-size:13px;
                color:#64748B;
                max-width:600px;
                margin:10px auto 0 auto;
                line-height:1.7;
            ">
                Enter a question above to start the Advanced RAG pipeline.
                Your query will eventually pass through semantic search,
                keyword search, hybrid retrieval and reranking before
                generating the final answer.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Advanced RAG with Hybrid Search & Reranking
        &nbsp; • &nbsp;
        Document Intelligence System
    </div>
    """,
    unsafe_allow_html=True
)
