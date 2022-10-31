import bcrypt

def hash(password: str):
    password_binary =  bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
    return password_binary.decode('utf-8')

def verify(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf8'), hashed_password.encode('utf8'))