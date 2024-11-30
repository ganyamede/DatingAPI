import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(stored_hash, input_password):
    return stored_hash == hash_password(input_password)