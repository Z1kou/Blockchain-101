from .crypto import sha256_hex
from .block import Block, block_hash

DIFFICULTY_PREFIX = "0000"

def valid_proof(last_proof: int, prev_hash: str, proof: int) -> bool:
    guess = f"{last_proof}{prev_hash}{proof}".encode()
    return sha256_hex(guess).startswith(DIFFICULTY_PREFIX)

def mine_proof(last_block: Block) -> int:
    """Smallest proof s.t. hash(prefix) starts with DIFFICULTY_PREFIX."""
    prev_hash = block_hash(last_block)
    proof = 0
    while not valid_proof(last_block.proof, prev_hash, proof):
        proof += 1
    return proof
