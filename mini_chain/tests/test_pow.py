from mini_chain.core.pow import valid_proof, DIFFICULTY_PREFIX

def test_valid_proof_signature():
    # Shape and deterministic prefix assumption
    assert isinstance(valid_proof(1, "abc", 0), bool)
    assert DIFFICULTY_PREFIX.startswith("0")
