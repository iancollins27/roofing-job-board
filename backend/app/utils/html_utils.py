import bleach

ALLOWED_TAGS = [
    'p', 'br', 'strong', 'b', 'i', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 
    'h5', 'h6', 'a', 'span', 'div', 'blockquote', 'pre', 'code'
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'div': ['class'],
    'span': ['class'],
}

def sanitize_html(html_content: str) -> str:
    """Sanitize HTML content to prevent XSS attacks"""
    return bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    ) 