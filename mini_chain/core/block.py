from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from .crypto import hash_dict

@dataclass(frozen=True)
class Block:
    index: int
    timestamp: float
    transactions: List[Dict[str, Any]]
    proof: int
    previous_hash: str

    def to_dict(self) -> dict:
        return asdict(self)

def block_hash(block: "Block") -> str:
    """Hash the entire block dict (toy model)."""
    return hash_dict(block.to_dict())
