import re

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)   # collapse extra whitespace
    text = re.sub(r'\n+', '\n', text)  # normalise line breaks
    return text.strip()