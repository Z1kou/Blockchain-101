import json
from pathlib import Path
from typing import Optional
from ..core.chain import Chain

def save_chain(chain: Chain, path: str) -> None:
    Path(path).write_text(json.dumps(chain.to_dict(), sort_keys=True, separators=(",", ":")))

def load_chain(path: str) -> Optional[Chain]:
    p = Path(path)
    if not p.exists():
        return None
    data = json.loads(p.read_text())
    return Chain.from_dict(data)
