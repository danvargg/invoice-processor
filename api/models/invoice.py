from typing import Optional

from pydantic import BaseModel


class Invoice(BaseModel):  # TODO: add category, desc
    date: Optional[str] = None
    supplier: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    total: float = 0.0
    federal_tax: Optional[float] = None
    provincial_tax: Optional[float] = None


def sanitize_text(text: str) -> str:  # TODO: move to services
    # Remove potentially harmful characters or instructions
    sanitized_text = re.sub(r'[^\w\s]', '', text)

    # Escape special characters
    sanitized_text = re.sub(r'([{}])', r'\\\1', sanitized_text)

    # Limit input length
    max_length = 1000  # Adjust as needed
    sanitized_text = sanitized_text[:max_length]

    # Filter specific keywords
    keywords_to_filter = ['instruction', 'command', 'execute']
    for keyword in keywords_to_filter:
        sanitized_text = sanitized_text.replace(keyword, '')

    return sanitized_text
