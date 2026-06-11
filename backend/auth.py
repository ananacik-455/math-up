import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path, override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
BYPASS_AUTH = os.getenv("BYPASS_TELEGRAM_AUTH", "false").replace('"', '').replace("'", '').strip().lower() == "true"

import hmac
import hashlib
from urllib.parse import parse_qsl
import json

def validate_telegram_data(init_data: str) -> dict | None:
    """
    Validates the data received from the Telegram Web App using the BOT_TOKEN.
    """
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Warning: BOT_TOKEN is not configured.")
        return None

    try:
        parsed_data = dict(parse_qsl(init_data, keep_blank_values=True))
        if "hash" not in parsed_data:
            print("Auth Error: No hash found in initData")
            return None
            
        hash_val = parsed_data.pop("hash")
        parsed_data.pop("signature", None) # Telegram requires stripping signature if present
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))
        
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        if calculated_hash == hash_val:
            print("Auth Success: HMAC matches!")
            return json.loads(parsed_data.get("user", "{}"))
        elif BYPASS_AUTH:
            print("Auth Warning: HMAC mismatched, but BYPASS_TELEGRAM_AUTH is active! Letting you through.")
            # We still return the real user data so your DB works natively with your real account
            return json.loads(parsed_data.get("user", "{}"))
        else:
            print(f"Auth Failed: HMAC mismatch!")
            print(f"Calculated: {calculated_hash}")
            print(f"Provided:   {hash_val}")
            
    except Exception as e:
        print(f"Auth validation exception: {e}")
        
    return None
