import hashlib

def verify_data_hash(data: str | bytes, expected_hash: str, algorithm: str = "sha256") -> dict:
    if isinstance(data, str):
        data_bytes = data.encode("utf-8")
    elif isinstance(data, bytes):
        data_bytes = data
    else:
        raise TypeError("Data must be string or bytes")

    algo = algorithm.lower()
    if not hasattr(hashlib, algo):
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    hasher = getattr(hashlib, algo)()
    hasher.update(data_bytes)
    calculated = hasher.hexdigest()

    return {
        "match": calculated.lower() == expected_hash.lower(),
        "calculated_hash": calculated
    }
