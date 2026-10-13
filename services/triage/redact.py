"""Week 9 redactor (copied from afyaplus-week9 security/redact.py): tokens, keys and
Kenya-facing identifiers are removed before anything reaches disk."""
import hashlib
import re

BEARER = re.compile(r'Bearer\s+\S+', re.I)
JWT = re.compile(r'\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*')
OPENAI_KEY = re.compile(r'\bsk-[A-Za-z0-9_-]{8,}')
EMAIL = re.compile(r'\b[\w.+-]+@[\w-]+\.[\w.-]+\b')
PHONE = re.compile(r'(?:\+?254|0)[17]\d{8}\b')                 # +2547.., 07.., 01..
MPESA = re.compile(r'\b[A-Z](?=[A-Z0-9]*\d)[A-Z0-9]{9}\b')
KENYA_ID = re.compile(r'\b\d{7,8}\b')                          # not 7-10: epochs survive


def redact(text: str) -> str:
    text = BEARER.sub('Bearer [REDACTED]', text)
    text = JWT.sub('[REDACTED_JWT]', text)
    text = OPENAI_KEY.sub('[REDACTED_KEY]', text)
    text = EMAIL.sub('[REDACTED_EMAIL]', text)
    text = PHONE.sub('[REDACTED_PHONE]', text)
    text = MPESA.sub('[REDACTED_MPESA]', text)
    text = KENYA_ID.sub('[REDACTED_ID]', text)
    return text


def redact_then_hash(payload: str) -> tuple[str, str]:
    """Hash the CLEANED text, so the digest is never a fingerprint of raw personal data."""
    cleaned = redact(payload)
    return cleaned, hashlib.sha256(cleaned.encode()).hexdigest()[:16]
