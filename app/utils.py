from passlib.context import CryptContext

#telling the passlib to use "bcrypt" for password encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

#vrifying for Authentication method during the login attempt by user

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

    