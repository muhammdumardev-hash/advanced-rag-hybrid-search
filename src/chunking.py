import re


def chunk_documents(documents, chunk_size=900, chunk_overlap=150):
    """Create overlapping chunks while preserving source/page metadata."""
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []

    for document in documents:
        source = document.get("source", "unknown")
        pages = document.get("pages", [])
        text = document.get("text", "").strip()

        if not text:
            continue

        paragraphs = [
            re.sub(r"\s+", " ", paragraph).strip()
            for paragraph in re.split(r"\n\s*\n", text)
            if paragraph.strip()
        ]

        current = ""
        for paragraph in paragraphs:
            if len(paragraph) > chunk_size:
                if current:
                    chunks.append(_make_chunk(source, current, pages, len(chunks)))
                    current = ""

                start = 0
                while start < len(paragraph):
                    piece = paragraph[start:start + chunk_size].strip()
                    if piece:
                        chunks.append(_make_chunk(source, piece, pages, len(chunks)))
                    start += chunk_size - chunk_overlap
                continue

            candidate = f"{current} {paragraph}".strip()

            if current and len(candidate) > chunk_size:
                chunks.append(_make_chunk(source, current, pages, len(chunks)))
                overlap = current[-chunk_overlap:].strip()
                current = f"{overlap} {paragraph}".strip()
            else:
                current = candidate

        if current:
            chunks.append(_make_chunk(source, current, pages, len(chunks)))

    return chunks


def _make_chunk(source, text, pages, index):
    page_numbers = [p.get("page") for p in pages if p.get("page") is not None]

    return {
        "chunk_id": f"{source}::chunk_{index + 1}",
        "source": source,
        "page": page_numbers[0] if page_numbers else None,
        "pages": page_numbers,
        "text": text.strip(),
    }
