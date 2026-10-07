import os
from html import escape

import streamlit as st

from src.document_loader import load_pdf_documents
from src.chunking import chunk_documents
from src.semantic_search import SemanticSearch
from src.keyword_search import KeywordSearch
from src.hybrid_search import hybrid_search
from src.reranker import Reranker
from src.qa import generate_answer, FALLBACK


st.set_page_config(
    page_title="Advanced RAG | Document Intelligence",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render(content: str):
    cleaned = "\n".join(
        line.strip() for line in content.splitlines() if line.strip()
    )
    st.markdown(cleaned, unsafe_allow_html=True)


render("""
<style>
.stApp {
    background: #F5F7FB;
}

.main .stMarkdown,
.main .stMarkdown p,
.main .stMarkdown span,
.main label,
.main [data-testid="stMetricLabel"],
.main [data-testid="stMetricValue"],
.main [data-testid="stMetricDelta"],
.main [data-testid="stExpander"] summary,
.main [data-testid="stExpander"] summary span,
.main [data-baseweb="tab"] {
    color: #1E293B !important;
}

.main [data-testid="stCaptionContainer"] p {
    color: #64748B !important;
}

.main [data-testid="stAlert"] {
    color: #1E293B !important;
}

.main [data-testid="stExpander"] {
    color: #1E293B !important;
}

.main [data-testid="stTextInput"] label {
    color: #1E293B !important;
}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-baseweb="slider"] * {
    color: #F9FAFB !important;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1F2937;
}

section[data-testid="stSidebar"] * {
    color: #F9FAFB;
}

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
    box-shadow: 0 10px 35px rgba(15,23,42,0.15);
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

.metric-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 4px 15px rgba(15,23,42,0.04);
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

.pipeline-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 20px;
    color: #1E293B;
    line-height: 1.7;
    box-shadow: 0 4px 15px rgba(15,23,42,0.04);
}

.pipeline-step {
    background: white;
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

.answer-card {
    background: white;
    border: 1px solid #DCE3ED;
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 5px 20px rgba(15,23,42,0.05);
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
    white-space: pre-wrap;
}

.empty-state {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 45px;
    text-align: center;
    margin-top: 25px;
}

.empty-title {
    font-size: 20px;
    font-weight: 750;
    color: #1E293B;
    margin-top: 10px;
}

.empty-text {
    font-size: 13px;
    color: #64748B;
    max-width: 600px;
    margin: 10px auto 0 auto;
    line-height: 1.7;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
    height: 45px;
    border: 1px solid #CBD5E1;
}

.stTextInput input {
    border-radius: 11px;
    border: 1px solid #CBD5E1;
    padding: 12px;
}

.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 11px;
    padding-top: 35px;
    padding-bottom: 10px;
}

.result-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
}

.result-source {
    font-size: 12px;
    font-weight: 700;
    color: #2563EB;
    margin-bottom: 7px;
}

.result-score {
    font-size: 11px;
    color: #64748B;
    margin-bottom: 9px;
}

.result-text {
    font-size: 13px;
    color: #1E293B;
    line-height: 1.65;
}
</style>
""")


@st.cache_resource(show_spinner="Loading documents, embeddings and reranker...")
def build_rag():
    documents = load_pdf_documents()
    chunks = chunk_documents(documents)

    semantic = SemanticSearch(chunks)
    keyword = KeywordSearch(chunks)
    reranker = Reranker()

    return documents, chunks, semantic, keyword, reranker


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


def result_card(result, score_name, score_value):
    source = escape(str(result.get("source", "unknown")))
    page = result.get("page", "N/A")
    text = escape(str(result.get("text", "")))
    score = float(score_value)

    render(f"""
    <div class="result-card">
    <div class="result-source">
        📄 {source} &nbsp;•&nbsp; Page {page}
    </div>

    <div class="result-score">
        {escape(score_name)}: {score:.4f}
    </div>

    <div class="result-text">
        {text}
    </div>
    </div>
    """)


st.session_state.setdefault("search_performed", False)
st.session_state.setdefault("rag_result", None)


with st.sidebar:

    render("""
    <div style="padding: 10px 4px 20px 4px;">
        <div style="font-size: 27px; font-weight: 800;">
            📚 RAG Intelligence
        </div>

        <div style="
            font-size: 12px;
            color: #94A3B8;
            margin-top: 6px;
        ">
            Advanced Document Q&A
        </div>
    </div>
    """)

    st.markdown("---")

    st.markdown("### ⚙️ Retrieval Settings")

    semantic_weight = st.slider(
        "Semantic Search Weight",
        0.0,
        1.0,
        0.60,
        0.05
    )

    keyword_weight = st.slider(
        "Keyword Search Weight",
        0.0,
        1.0,
        0.40,
        0.05
    )

    top_k = st.slider(
        "Hybrid Results",
        3,
        20,
        10
    )

    rerank_k = st.slider(
        "Final Reranked Results",
        1,
        10,
        3
    )

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


render("""
<div class="hero">

<div class="badge">
⚡ ADVANCED RETRIEVAL-AUGMENTED GENERATION
</div>

<div class="hero-title">
Intelligent Document Q&A
</div>

<div class="hero-subtitle">
Ask questions from your document knowledge base using semantic search,
keyword retrieval, hybrid search and cross-encoder reranking before
generating an AI-powered answer.
</div>

</div>
""")


try:

    documents, chunks, semantic, keyword, reranker = build_rag()
    load_error = None

except Exception as error:

    documents = []
    chunks = []
    semantic = None
    keyword = None
    reranker = None
    load_error = str(error)


section(
    "📊 Knowledge Base Overview",
    "Documents currently available for retrieval."
)


c1, c2, c3, c4 = st.columns(4)


with c1:
    metric_card(
        "📄",
        "Documents",
        len(documents),
        "PDF knowledge sources"
    )


with c2:
    metric_card(
        "🧩",
        "Chunks",
        len(chunks),
        "Indexed text segments"
    )


with c3:
    metric_card(
        "🎯",
        "Reranking",
        "Active" if reranker else "Unavailable",
        "Cross-Encoder"
    )


with c4:
    metric_card(
        "🤖",
        "Generation",
        "Groq",
        "Context-grounded answers"
    )


with st.expander(
    "📚 View Knowledge Base Documents",
    expanded=False
):

    if documents:

        cols = st.columns(2)

        for i, document in enumerate(documents):

            with cols[i % 2]:

                name = escape(document["source"])
                pages = len(document.get("pages", []))

                render(f"""
                <div class="document-card">

                <div class="document-name">
                    📄 {name}
                </div>

                <div class="document-meta">
                    PDF &nbsp;•&nbsp;
                    {pages} pages &nbsp;•&nbsp;
                    {get_file_size(document["source"])}
                </div>

                </div>
                """)

    else:

        st.warning(
            "No PDF documents were loaded from the knowledge_base folder."
        )


section(
    "🔄 Retrieval Pipeline",
    "Every question passes through the following retrieval stages."
)


pipeline = [
    ("📄", "Documents", "Knowledge Base"),
    ("✂️", "Chunking", "Text Segments"),
    ("🧠", "Semantic", "Vector Search"),
    ("🔤", "Keyword", "BM25 Search"),
    ("🔀", "Hybrid", "Combined Results"),
    ("🎯", "Reranking", "Cross-Encoder"),
    ("🤖", "LLM", "Final Answer"),
]


for col, (icon, name, desc) in zip(
    st.columns(len(pipeline)),
    pipeline
):

    with col:

        render(f"""
        <div class="pipeline-step">

        <div class="pipeline-icon">
            {icon}
        </div>

        <div class="pipeline-name">
            {name}
        </div>

        <div class="pipeline-desc">
            {desc}
        </div>

        </div>
        """)


section(
    "💬 Ask Your Documents",
    "Ask a question and retrieve the most relevant information from the knowledge base."
)


query = st.text_input(
    "Your question",
    placeholder="Example: What are the Learning Commons reservation rules?",
    label_visibility="collapsed",
)


b1, b2, _ = st.columns([1, 1, 4])


with b1:

    search_button = st.button(
        "🔎 Search Documents",
        use_container_width=True,
        type="primary"
    )


with b2:

    clear_button = st.button(
        "✕ Clear",
        use_container_width=True
    )


if clear_button:

    st.session_state.search_performed = False
    st.session_state.rag_result = None
    st.rerun()


if search_button:

    if not query.strip():

        st.warning("Please enter a question first.")

    elif load_error:

        st.error(
            f"RAG pipeline could not start: {load_error}"
        )

    else:

        with st.spinner(
            "Running semantic search → keyword search → "
            "hybrid search → reranking → LLM..."
        ):

            try:

                semantic_results = semantic.search(
                    query,
                    top_k=top_k
                )

                keyword_results = keyword.search(
                    query,
                    top_k=top_k
                )


                hybrid_results = hybrid_search(
                    semantic_results,
                    keyword_results,
                    top_k=top_k,
                    semantic_weight=semantic_weight,
                    keyword_weight=keyword_weight,
                )


                reranked_results = reranker.rerank(
                    query,
                    hybrid_results,
                    top_k=rerank_k,
                )


                answer = generate_answer(
                    query,
                    reranked_results
                )


                st.session_state.rag_result = {
                    "query": query,
                    "semantic": semantic_results,
                    "keyword": keyword_results,
                    "hybrid": hybrid_results,
                    "reranked": reranked_results,
                    "answer": answer,
                }

                st.session_state.search_performed = True


            except Exception as error:

                st.session_state.rag_result = None

                st.error(
                    f"Search failed: {error}"
                )


result = st.session_state.rag_result


if st.session_state.search_performed and result:

    # OUT-OF-SCOPE / INFORMATION NOT AVAILABLE
    if result["answer"].strip() == FALLBACK:

        section(
            "🤖 AI Answer",
            "No supporting information was found in the document knowledge base."
        )

        render(f"""
        <div class="answer-card">

        <div class="answer-label">
            Information Not Available
        </div>

        <div class="answer-text">
            {escape(result["answer"])}
        </div>

        </div>
        """)


    # NORMAL SUCCESSFUL ANSWER
    else:

        section(
            "🔍 Retrieval Analysis",
            "Actual retrieval results from the current query."
        )


        render(f"""
        <div class="answer-card">

        <div class="answer-label">
            User Query
        </div>

        <div class="answer-text">
            {escape(result["query"])}
        </div>

        </div>
        """)


        st.write("")


        m1, m2, m3, m4 = st.columns(4)


        m1.metric(
            "Semantic Candidates",
            len(result["semantic"]),
            "Vector Search"
        )


        m2.metric(
            "Keyword Candidates",
            len(result["keyword"]),
            "BM25"
        )


        m3.metric(
            "Hybrid Candidates",
            len(result["hybrid"]),
            "Combined"
        )


        m4.metric(
            "Reranked Results",
            len(result["reranked"]),
            "Final Context"
        )


        tab1, tab2, tab3 = st.tabs(
            [
                "🧠 Semantic Search",
                "🔤 Keyword Search",
                "🔀 Hybrid + Reranking"
            ]
        )


        with tab1:

            st.markdown("### Semantic Retrieval")

            if result["semantic"]:

                for item in result["semantic"]:

                    result_card(
                        item,
                        "Semantic Score",
                        item.get("semantic_score", 0.0)
                    )

            else:

                st.info(
                    "No semantic candidates found."
                )


        with tab2:

            st.markdown("### Keyword Retrieval")

            if result["keyword"]:

                for item in result["keyword"]:

                    result_card(
                        item,
                        "BM25 Score",
                        item.get("keyword_score", 0.0)
                    )

            else:

                st.info(
                    "No keyword candidates found."
                )


        with tab3:

            st.markdown("### Hybrid Search")

            st.caption(
                "Semantic + BM25 candidates combined using the selected weights."
            )

            if result["hybrid"]:

                for rank, item in enumerate(
                    result["hybrid"],
                    start=1
                ):

                    st.markdown(
                        f"**Rank {rank}**"
                    )

                    result_card(
                        item,
                        "Hybrid Score",
                        item.get("hybrid_score", 0.0)
                    )

            else:

                st.info(
                    "No hybrid candidates found."
                )


        section(
            "📑 Retrieved Results",
            "Top hybrid candidates passed to the reranker."
        )


        if result["hybrid"]:

            for rank, item in enumerate(
                result["hybrid"],
                start=1
            ):

                with st.expander(
                    f"Candidate {rank} — "
                    f"{item.get('source', 'unknown')} | "
                    f"Hybrid: "
                    f"{item.get('hybrid_score', 0.0):.4f}"
                ):

                    st.write(
                        item.get("text", "")
                    )

                    st.caption(
                        f"Semantic: "
                        f"{item.get('semantic_score', 0.0):.4f} | "
                        f"BM25: "
                        f"{item.get('keyword_score', 0.0):.4f} | "
                        f"Page: "
                        f"{item.get('page', 'N/A')}"
                    )

        else:

            st.info(
                "No retrieved candidates were found."
            )


        section(
            "🎯 Reranking Results",
            "Cross-Encoder scores each question/chunk pair and keeps the highest-ranked context."
        )


        if result["reranked"]:

            for rank, item in enumerate(
                result["reranked"],
                start=1
            ):

                result_card(
                    item,
                    f"Rerank Score • Rank {rank}",
                    item.get("rerank_score", 0.0)
                )

        else:

            st.info(
                "No reranked results were produced."
            )


        section(
            "🤖 AI Answer",
            "Generated using only the final reranked document context."
        )


        render(f"""
        <div class="answer-card">

        <div class="answer-label">
            Context-Grounded Response
        </div>

        <div class="answer-text">
            {escape(result["answer"])}
        </div>

        </div>
        """)


else:

    render("""
    <div class="empty-state">

    <div style="font-size:45px;">
        🔎
    </div>

    <div class="empty-title">
        Ready to Search
    </div>

    <div class="empty-text">
        Enter a question above to start the Advanced RAG pipeline.
        Your query will pass through semantic search, keyword search,
        hybrid retrieval and reranking before generating the final answer.
    </div>

    </div>
    """)


render("""
<div class="footer">
Advanced RAG with Hybrid Search &amp; Reranking
&nbsp;•&nbsp;
Document Intelligence System
</div>
""")
