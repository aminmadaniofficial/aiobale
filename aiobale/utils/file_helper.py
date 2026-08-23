def guess_mime_type(data: bytes) -> str:
    if data.startswith(b'\xff\xd8\xff'):
        return "image/jpeg"
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return "image/png"
    if data.startswith(b'GIF87a') or data.startswith(b'GIF89a'):
        return "image/gif"
    if data.startswith(b'BM'):
        return "image/bmp"
    if data.startswith(b'II*\x00') or data.startswith(b'MM\x00*'):
        return "image/tiff"
    if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return "image/webp"

    if data.startswith(b'%PDF'):
        return "application/pdf"
    if data.startswith(b'\x50\x4B\x03\x04'):
        return "application/zip"
    if data.startswith(b'Rar!\x1A\x07\x00') or data.startswith(b'Rar!\x1A\x07\x01\x00'):
        return "application/x-rar-compressed"
    if data.startswith(b'\x1f\x8b\x08'):
        return "application/gzip"
    if data.startswith(b'7z\xbc\xaf\x27\x1c'):
        return "application/x-7z-compressed"

    if data.startswith(b'ID3') or data[0:2] == b'\xff\xfb':
        return "audio/mpeg"
    if data[0:4] == b'RIFF' and data[8:12] == b'WAVE':
        return "audio/wav"
    if data.startswith(b'OggS'):
        if b'vorbis' in data[:64]:
            return "audio/ogg"
        if b'opus' in data[:64]:
            return "audio/opus"
        return "application/ogg"
    if data.startswith(b'fLaC'):
        return "audio/flac"
    if data[4:8] == b'ftypM4A':
        return "audio/mp4"

    if b'ftyp' in data[:12]:
        if b'ftypmp4' in data[:20] or b'ftypisom' in data[:20]:
            return "video/mp4"
        if b'ftyp3gp' in data[:20]:
            return "video/3gpp"
        if b'ftypmkv' in data[:20] or b'matroska' in data[:64]:
            return "video/x-matroska"
    if data[0:4] == b'\x00\x00\x00\x18' and b'ftyp' in data[4:12]:
        return "video/mp4"
    if data[0:4] == b'RIFF' and data[8:12] == b'AVI ':
        return "video/x-msvideo"

    return "application/octet-stream"
