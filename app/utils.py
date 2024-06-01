from passlib.context import CryptContext

# setting hashing algorithm for passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)
