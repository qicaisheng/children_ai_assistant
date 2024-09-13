import uuid


def get_uuid4_no_hyphen():
    uuid_str = str(uuid.uuid4())
    uuid_str_no_hyphen = uuid_str.replace('-', '')
    return uuid_str_no_hyphen