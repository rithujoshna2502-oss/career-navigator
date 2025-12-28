import html
import hmac
import hashlib
from typing import Iterable, List


def sanitize_text(value: str) -> str:
    """Escape HTML in a string to prevent XSS when rendering user content."""
    if value is None:
        return ''
    return html.escape(str(value))


def sanitize_list(items: Iterable) -> List[str]:
    """Sanitize each element of an iterable of strings."""
    return [sanitize_text(i) for i in items or []]


def verify_hmac_signature(secret: str, payload: bytes, signature_header: str) -> bool:
    """Verify HMAC SHA256 signature from a webhook.

    - `secret` is the shared webhook secret
    - `payload` is the raw request body (bytes)
    - `signature_header` is the header value from the request (hex digest)

    Returns True if the signature matches.
    """
    if not secret or not signature_header:
        return False
    try:
        computed = hmac.new(secret.encode('utf-8'), payload, hashlib.sha256).hexdigest()
        # Use hmac.compare_digest to avoid timing attacks
        return hmac.compare_digest(computed, signature_header)
    except Exception:
        return False


def verify_api_key(request_headers: dict, expected_key: str) -> bool:
    """Verify API key from request headers (Authorization: Bearer <key>).
    
    - `request_headers` is the headers dict from request.headers
    - `expected_key` is the valid API key string
    
    Returns True if the key is valid (timing-attack safe).
    """
    auth_header = request_headers.get('Authorization') or request_headers.get('X-API-Key', '')
    
    if auth_header.startswith('Bearer '):
        provided_key = auth_header[7:]  # Remove 'Bearer ' prefix
    else:
        provided_key = auth_header
    
    if not expected_key or not provided_key:
        return False
    
    try:
        return hmac.compare_digest(provided_key, expected_key)
    except Exception:
        return False
