from mini_chain.core.crypto import canonical_json, hash_dict

def test_canonical_json_deterministic():
    a = {"b": 1, "a": 2}
    b = {"a": 2, "b": 1}
    assert canonical_json(a) == canonical_json(b)
    assert hash_dict(a) == hash_dict(b)
