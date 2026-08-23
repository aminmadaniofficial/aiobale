from aiobale.utils import ProtoBuf
from aiobale.utils.links import extract_join_token
from aiobale.utils.int64 import decode_list


def test_protobuf_encode_decode():
    codec = ProtoBuf()
    sample_data = {
        "1": 12345,
        "2": "hello world",
        "3": {"1": "nested"},
        "4": [1, 2, 3],
    }

    encoded = codec.encode(sample_data)
    assert isinstance(encoded, (bytes, bytearray))

    decoded = codec.decode(bytes(encoded))
    assert decoded["1"] == 12345
    assert decoded["2"] == "hello world"
    assert decoded["3"]["1"] == "nested"


def test_extract_join_token():
    assert (
        extract_join_token("https://ble.ir/join/AbCdEf12345") == "AbCdEf12345"
    )
    assert extract_join_token("ble.ir/join/AbCdEf12345") == "AbCdEf12345"
    assert extract_join_token("AbCdEf12345") == "AbCdEf12345"
    assert extract_join_token("invalid link") is None


def test_decode_list():
    # Test decoding packed varints
    # varints for 1, 2, 3 in hex: "010203"
    result = decode_list("010203")
    assert result == [1, 2, 3]
