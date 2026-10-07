# LLM question answering and out-of-scope handling
import streamlit as st
from groq import Groq


FALLBACK = "I couldn't find this information in the provided documents."


def _secret(name, default=None):
    try:
        return st.secrets[name]
    except Exception:
        return default


def generate_answer(query, reranked_chunks):
    """
    Generate an answer using only the final reranked document context.
    """

    if not reranked_chunks:
        return FALLBACK

    context = []

    for number, chunk in enumerate(reranked_chunks, start=1):
        source = chunk.get("source", "unknown")
        page = chunk.get("page", "N/A")
        text = chunk.get("text", "")

        context.append(
            f"[Context {number} | Source: {source} | Page: {page}]\n"
            f"{text}"
        )

    context_text = "\n\n".join(context)

    api_key = _secret("GROQ_API_KEY")
    model = _secret(
        "GROQ_MODEL",
        "openai/gpt-oss-120b"
    )

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. "
            "Add it to .streamlit/secrets.toml."
        )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a university document question-answering "
                    "assistant. Use ONLY the supplied document context. "
                    "Never use outside knowledge or invent facts. "
                    "If the context does not contain enough information "
                    "to answer the question, reply exactly: "
                    f"{FALLBACK} "
                    "Keep the answer concise and factual."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{query}\n\n"
                    f"Document context:\n{context_text}"
                ),
            },
        ],
    )

    answer = response.choices[0].message.content

    if not answer:
        return FALLBACK

    return answer.strip()
