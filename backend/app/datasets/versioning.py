import hashlib
import json

def dataset_hash(dataset: list[dict]) -> str:
    encoded = json.dumps(dataset, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()
