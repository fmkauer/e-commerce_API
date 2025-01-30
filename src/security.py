import hashlib
import secrets


def _hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    # Combine password and salt
    salted = (password + salt).encode()
    # Use SHA256 for hashing
    hashed = hashlib.sha256(salted).hexdigest()
    return hashed, salt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Split the stored hash into hash and salt
    try:
        stored_hash, salt = hashed_password.split(":")
        # Hash the plain password with the same salt
        calculated_hash, _ = _hash_password(plain_password, salt)
        # Compare the hashes
        return secrets.compare_digest(stored_hash, calculated_hash)
    except ValueError:
        return False


def get_password_hash(password: str) -> str:
    # Generate a hash and salt for the password
    hashed, salt = _hash_password(password)
    # Return the combined hash:salt string
    return f"{hashed}:{salt}"
