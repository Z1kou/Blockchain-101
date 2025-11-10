import requests
from typing import Optional, Dict, Any

def get_chain(base_url: str, timeout: float = 3.0) -> Optional[Dict[str, Any]]:
    try:
        r = requests.get(base_url.rstrip("/") + "/chain", timeout=timeout)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.RequestException:
        return None
