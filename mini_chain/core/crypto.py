from hashlib import sha256
import json
from typing import Any

def canonical_json(obj: Any) -> bytes:
    """Deterministic JSON: sorted keys, no spaces."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()

def sha256_hex(data: bytes) -> str:
    return sha256(data).hexdigest()

def hash_dict(d: dict) -> str:
    """Hash a JSON-serializable dict deterministically."""
    return sha256_hex(canonical_json(d))
