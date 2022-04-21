import json
from typing import Dict

def read_json(path: str) -> Dict:

    with open(path, 'r') as f:
        return json.load(f)