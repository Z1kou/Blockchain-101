from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Transaction:
    sender: str        # "0" for reward
    recipient: str
    amount: float

    def to_dict(self) -> dict:
        return asdict(self)

def validate_tx(tx: "Transaction") -> None:
    if not tx.sender or not tx.recipient:
        raise ValueError("sender and recipient required")
    if tx.amount <= 0:
        raise ValueError("amount must be positive")
