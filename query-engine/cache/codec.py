import json


def encode_data(data, timestamp):
    encoded_data = f"{timestamp}:{json.dumps(data)}".encode("utf-8")
    return encoded_data


def decode_data(encoded_data):
    if not isinstance(encoded_data, bytes):
        encoded_data = encoded_data.encode("utf-8")
    parts = encoded_data.split(b":", 1)
    if len(parts) == 2:
        timestamp, data = parts
        return json.loads(data.decode("utf-8"))
    return None
