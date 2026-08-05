import re

def highlight(query: str, document_text: str) -> str:
    """Highlight exact matching of query words"""
    words = query.split()
    pattern = "|".join(map(re.escape, words))
    regex = re.compile(rf"\b({pattern})\b", re.IGNORECASE)
    highlighted = regex.sub(r"<mark>\1</mark>", document_text)
    return highlighted