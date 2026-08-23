import base64
import json


def parse_jwt(token):
    try:
        header_b64, payload_b64, _ = token.split('.')
        
        def b64decode(data):
            rem = len(data) % 4
            if rem > 0:
                data += '=' * (4 - rem)
            return base64.urlsafe_b64decode(data)

        header = json.loads(b64decode(header_b64))
        payload = json.loads(b64decode(payload_b64))
        return payload, header
    
    except Exception:
        return None
