def clean_grpc(data: bytes):
    trailer_tag = b"grpc-status"
    idx = data.find(trailer_tag)
    if idx != -1:
        payload = data[5:idx]
    else:
        payload = data[5:]
        
    return payload


def add_header(payload: bytes):
    compressed_flag = 0x00
    length = len(payload)
    header = bytes([compressed_flag]) + length.to_bytes(4, byteorder='big')
    
    return header + payload
