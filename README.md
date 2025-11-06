# Blockchain 101 -> MiniChain — first steps toward a blockchain



A tiny, testable skeleton to learn core ideas: blocks, transactions, PoW, validation, and a simple “longest chain” consensus. This is our initial test project before bigger blockchain work.

# Layout

mini_chain/
  core/
    crypto.py        # canonical JSON + SHA256
    block.py         # Block dataclass + block_hash()
    tx.py            # Transaction + validate_tx()
    pow.py           # PoW target + mine/validate
    chain.py         # Chain state + validator
    consensus.py     # choose_longest_valid()
  io/
    storage.py       # save/load JSON
    net.py           # fetch /chain from peers
  app/
    orchestrator.py  # CLI: add-tx, mine, show, resolve
    api.py           # optional REST (Flask)
  tests/
    test_crypto.py
    test_pow.py
    test_chain.py
README.md


# Setup
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install flask requests pytest



