import secrets
from string import ascii_letters, digits

from src.core.config import settings


def generate_hash(input_string: str) -> str:
    """Generate a SHA-256 hash of the input string."""
    import hashlib

    characters = ascii_letters + digits
    salt = "".join(secrets.choice(characters) for _ in range(settings.hash_salt_length))
    return hashlib.sha256((salt + input_string).encode()).hexdigest()
