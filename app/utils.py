from passlib.context import CryptContext

#telling the passlib to use "bcrypt" for password encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)