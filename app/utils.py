from passlib.context import CryptContext


# Password encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def  hash(password: str):
  return pwd_context.hash(password)