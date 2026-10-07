import os
import fitz


KNOWLEDGE_BASE_PATH = "knowledge_base"


def load_pdf_documents():
    """
    Load all PDF documents from the knowledge base
    and extract their text.
    """

    documents = []

    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        return documents

    for file_name in sorted(os.listdir(KNOWLEDGE_BASE_PATH)):

        if not file_name.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(
            KNOWLEDGE_BASE_PATH,
            file_name
        )

        try:
            pdf = fitz.open(file_path)
            pages = []

            for page_number, page in enumerate(pdf):
                page_text = page.get_text().strip()

                if page_text:
                    pages.append(
                        {
                            "page": page_number + 1,
                            "text": page_text
                        }
                    )

            pdf.close()

            full_text = "\n\n".join(
                page["text"] for page in pages
            )

            if full_text:
                documents.append(
                    {
                        "source": file_name,
                        "text": full_text,
                        "pages": pages
                    }
                )

        except Exception as error:
            print(f"Error loading {file_name}: {error}")

    return documents


def get_document_count():
    """Return the number of successfully loaded PDF documents."""
    return len(load_pdf_documents())


def get_document_names():
    """Return the names of successfully loaded PDF documents."""
    return [
        document["source"]
        for document in load_pdf_documents()
    ]
