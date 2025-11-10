from mini_chain.core.chain import Chain
from mini_chain.core.tx import Transaction
from mini_chain.core.pow import mine_proof

def test_chain_lifecycle():
    c = Chain()
    genesis_len = len(c.chain)
    c.add_tx(Transaction("alice", "bob", 5))
    c.add_mining_reward("node1")
    proof = mine_proof(c.last_block)
    b = c.new_block(proof)

    assert len(c.chain) == genesis_len + 1
    assert b.index == 2
    assert Chain.valid_chain(c.chain)
