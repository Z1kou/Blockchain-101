from flask import Flask, jsonify, request
from uuid import uuid4
from ..core.chain import Chain
from ..core.tx import Transaction
from ..core.pow import mine_proof

app = Flask(__name__)
CHAIN = Chain()
NODE_ID = str(uuid4()).replace("-", "")[:8]

@app.get("/chain")
def chain():
    return jsonify(CHAIN.to_dict()), 200

@app.post("/transactions/new")
def new_tx():
    data = request.get_json(force=True)
    t = Transaction(sender=data["sender"], recipient=data["recipient"], amount=data["amount"])
    CHAIN.add_tx(t)
    return jsonify({"queued_for": CHAIN.last_block.index + 1}), 201

@app.get("/mine")
def mine():
    CHAIN.add_mining_reward(NODE_ID, 1.0)
    proof = mine_proof(CHAIN.last_block)
    b = CHAIN.new_block(proof)
    return jsonify({"message": "mined", "index": b.index, "proof": b.proof}), 201

def serve(port=5000):
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    serve()
