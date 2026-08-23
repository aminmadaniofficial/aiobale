import re


def extract_join_token(text: str) -> str | None:
    match = re.search(r'(?:https?://)?ble\.ir/join/([a-zA-Z0-9]+)', text)
    if match:
        return match.group(1)
    if re.fullmatch(r'[a-zA-Z0-9]+', text):
        return text
    return None
