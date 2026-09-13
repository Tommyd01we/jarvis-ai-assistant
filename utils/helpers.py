import json
import os
from typing import Any, Dict, List

def ensure_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def load_json(filepath: str, default=None) -> Any:
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return default or {}

def save_json(filepath: str, data: Any) -> bool:
    try:
        ensure_directory(os.path.dirname(filepath))
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

def extract_keywords(text: str, count: int = 5) -> List[str]:
    words = text.lower().split()
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    return keywords[:count]
