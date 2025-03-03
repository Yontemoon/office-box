import uuid

def stringToInt(string):
    return int(string.replace(",", "").replace("$", ""))

def uuidToString(name: str) -> str:
    generated_uuid = uuid.NAMESPACE_DNS
    return str(uuid.uuid5(generated_uuid, name))