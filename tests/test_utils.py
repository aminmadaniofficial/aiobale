from aiobale.utils.file_helper import guess_mime_type
from aiobale.utils.jwt_checker import parse_jwt
from aiobale.utils.random import generate_id
import pytest


def test_guess_mime_type():
    assert guess_mime_type(b"\xff\xd8\xff\xe0") == "image/jpeg"
    assert guess_mime_type(b"\x89PNG\r\n\x1a\n") == "image/png"
    assert guess_mime_type(b"GIF87a") == "image/gif"
    assert guess_mime_type(b"%PDF-1.5") == "application/pdf"
    assert guess_mime_type(b"\x50\x4B\x03\x04") == "application/zip"
    assert guess_mime_type(b"unknown bytes") == "application/octet-stream"


def test_generate_id():
    gid = generate_id(16)
    assert len(str(gid)) == 16
    assert isinstance(gid, int)
    with pytest.raises(ValueError):
        generate_id(0)


def test_parse_jwt():
    # Valid JWT: header={"alg":"none"}, payload={"userId":123,"payload":{"id":123}}
    # Header: eyJhbGciOiJub25lIn0 ({"alg":"none"})
    # Payload: eyJ1c2VySWQiOjEyMywicGF5bG9hZCI6eyJpZCI6MTIzfX0
    token = "eyJhbGciOiJub25lIn0.eyJ1c2VySWQiOjEyMywicGF5bG9hZCI6eyJpZCI6MTIzfX0.sig"
    result = parse_jwt(token)
    assert result is not None
    payload, header = result
    assert header["alg"] == "none"
    assert payload["userId"] == 123
    assert payload["payload"]["id"] == 123

    # Invalid token
    assert parse_jwt("invalid_jwt_token") is None
