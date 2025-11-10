import argparse, sys, json
from uuid import uuid4
from typing import List
from ..core.chain import Chain
from ..core.tx import Transaction
from ..core.block import Block
from ..core.consensus import choose_longest_valid
from ..io.storage import save_chain, load_chain
from ..io.net import get_chain
from ..core.pow import mine_proof

def to_blocks(block_dicts) -> List[Block]:
    return [Block(**b) for b in block_dicts]

def main():
    parser = argparse.ArgumentParser(description="MiniChain CLI")
    parser.add_argument("--db", default="chain.json", help="path to chain json")
    parser.add_argument("--node-id", default=None, help="miner id (default random)")

    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("show", help="print chain as JSON")

    addtx = sub.add_parser("add-tx", help="queue transaction")
    addtx.add_argument("--from", dest="sender", required=True)
    addtx.add_argument("--to", dest="recipient", required=True)
    addtx.add_argument("--amount", type=float, required=True)

    mine = sub.add_parser("mine", help="mine one block (adds reward)")
    mine.add_argument("--reward", type=float, default=1.0)

    res = sub.add_parser("resolve", help="longest-valid consensus")
    res.add_argument("--peers", nargs="+", required=True, help="e.g. http://127.0.0.1:5001")

    args = parser.parse_args()
    node_id = args.node_id or str(uuid4()).replace("-", "")[:8]
    chain = load_chain(args.db) or Chain()

    if args.cmd == "show":
        print(json.dumps(chain.to_dict(), indent=2))
    elif args.cmd == "add-tx":
        idx = chain.add_tx(Transaction(sender=args.sender, recipient=args.recipient, amount=args.amount))
        save_chain(chain, args.db)
        print(f"Queued for block {idx}")
    elif args.cmd == "mine":
        chain.add_mining_reward(node_id, amount=args.reward)
        proof = mine_proof(chain.last_block)
        b = chain.new_block(proof)
        save_chain(chain, args.db)
        print(f"Mined block #{b.index} (proof={b.proof})")
    elif args.cmd == "resolve":
        neighbor_chains = []
        for peer in args.peers:
            data = get_chain(peer)
            if data:
                neighbor_chains.append(to_blocks(data["chain"]))
        replaced = choose_longest_valid(chain, neighbor_chains)
        save_chain(chain, args.db)
        print("Replaced" if replaced else "Kept local chain")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
