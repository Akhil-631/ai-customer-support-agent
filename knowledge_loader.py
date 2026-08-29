from pathlib import Path


KNOWLEDGE_BASE_DIR = Path("knowledge_base")


DOCUMENT_METADATA = {
    "refund_policy.md": {
        "category": "refund",
        "document_type": "policy"
    },
    "return_policy.md": {
        "category": "return",
        "document_type": "policy"
    },
    "cancellation_policy.md": {
        "category": "cancellation",
        "document_type": "policy"
    },
    "delivery_policy.md": {
        "category": "delivery",
        "document_type": "policy"
    },
    "payment_faq.md": {
        "category": "payment",
        "document_type": "faq"
    },
    "customer_support_policy.md": {
        "category": "customer_support",
        "document_type": "policy"
    }
}


def load_documents():

    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.md"):

        metadata = DOCUMENT_METADATA.get(
            file_path.name,
            {
                "category": "general",
                "document_type": "knowledge"
            }
        )

        content = file_path.read_text(
            encoding="utf-8"
        )

        documents.append(
            {
                "content": content,
                "metadata": {
                    "source": file_path.name,
                    **metadata
                }
            }
        )

    return documents