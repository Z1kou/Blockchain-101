from typing import List
from .chain import Chain
from .block import Block

def choose_longest_valid(self_chain: Chain, neighbor_chains: List[List[Block]]) -> bool:
    """Adopt the longest valid chain from neighbors. Return True if replaced."""
    best = self_chain.chain
    for cand in neighbor_chains:
        if len(cand) > len(best) and Chain.valid_chain(cand):
            best = cand
    if best is not self_chain.chain:
        self_chain.chain = best
        self_chain.mempool = []  # clear pending tx to avoid dup confusion
        return True
    return False
