import os
import json
import hashlib
from typing import Union

from core.path_utils import find_aimo_root
from core.logger import log_event  # ← ここも存在を確認しておいてください

AIMO_ROOT = find_aimo_root()

def normalize_input(data: Union[str, dict]) -> str:
    try:
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        elif isinstance(data, str):
            data_str = data
        else:
            raise ValueError("Unsupported input type")

        normalized = (
            data_str.replace('\n', ' ')
                    .replace('\t', ' ')
                    .replace('\r', ' ')
                    .strip()
        )
        log_event("Input normalized successfully", "INFO")
        return normalized

    except Exception as e:
        log_event(f"Normalization failed: {e}", "ERROR")
        return ""

def generate_hash(data: Union[str, dict], method: str = "sha256") -> str:
    try:
        normalized = normalize_input(data)

        if not normalized:
            raise ValueError("Empty normalized string. Cannot generate hash.")

        if method == "sha256":
            hash_obj = hashlib.sha256()
        elif method == "blake2b":
            hash_obj = hashlib.blake2b()
        else:
            raise ValueError(f"Unsupported hash method: {method}")

        hash_obj.update(normalized.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()

        log_event(f"Hash generated using {method}: {hash_hex}", "SUCCESS")
        return hash_hex

    except Exception as e:
        log_event(f"Hash generation failed: {e}", "ERROR")
        return ""
