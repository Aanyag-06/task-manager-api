import bcrypt

def hash_password(password: str) -> str:
    # Converts a plain password string into a secure, random-salted hash
    # example: "hello123" → b"$2b$12$randomscrambled..."
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Checks if the plain password matches the stored hash — returns True or False
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)