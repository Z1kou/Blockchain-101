from typing import List, Dict, Any
from time import time
from .block import Block, block_hash
from .tx import Transaction, validate_tx
from .pow import valid_proof

class Chain:
    def __init__(self):
        self.chain: List[Block] = []
        self.mempool: List[Transaction] = []
        # Genesis block
        self._new_block(proof=100, previous_hash="1")

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    # ---- Transactions ----
    def add_tx(self, tx: Transaction) -> int:
        validate_tx(tx)
        self.mempool.append(tx)
        return self.last_block.index + 1

    def add_mining_reward(self, miner_id: str, amount: float = 1.0) -> None:
        self.mempool.append(Transaction(sender="0", recipient=miner_id, amount=amount))

    # ---- Blocks ----
    def new_block(self, proof: int) -> Block:
        return self._new_block(proof, block_hash(self.last_block))

    def _new_block(self, proof: int, previous_hash: str) -> Block:
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=[t.to_dict() for t in self.mempool],
            proof=proof,
            previous_hash=previous_hash,
        )
        self.mempool.clear()
        self.chain.append(block)
        return block

    # ---- Validation ----
    @staticmethod
    def valid_chain(blocks: List[Block]) -> bool:
        if not blocks:
            return False
        for i in range(1, len(blocks)):
            prev, curr = blocks[i-1], blocks[i]
            if curr.previous_hash != block_hash(prev):
                return False
            if not valid_proof(prev.proof, block_hash(prev), curr.proof):
                return False
        return True

    # ---- Serialization ----
    def to_dict(self) -> Dict[str, Any]:
        return {
            "length": len(self.chain),
            "chain": [b.to_dict() for b in self.chain],
            "mempool": [t.to_dict() for t in self.mempool],
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Chain":
        c = Chain.__new__(Chain)  # bypass __init__
        c.chain = [Block(**b) for b in d["chain"]]
        from .tx import Transaction
        c.mempool = [Transaction(**t) for t in d.get("mempool", [])]
        return c
