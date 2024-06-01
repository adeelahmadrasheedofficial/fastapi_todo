from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# secret key
# Algorithm
# Expiration time

SECRET_KEY = 'AAAAB3NzaC1yc2EAAAADAQABAAABgQD0EprmbcbL4dzgOGq/pkN7x2vxipl7S3mFiqNx+g0qwFNNHZFKgsbqy45JP9m5zZom9JbLjJiDBB8dElj5/iL6ou71bSPAg/nQK9Zw2dPzuTAb2pVv4c21KR53Hhjv7Kb/i8kUrAM7gernxPjEtt7PB5U3I7b+yBbr4rhkQWLEUxLNP9VD07JpylcwPG3uQx1/7Rlc57OxNdiMks2+LuiUCRHZHtK32Lknq7grMsoYVsWbprMwhkhrjqD+k7Dnh+0L13h/fwAQoau6Um4EITKmFJ2MJCBIutI126tQF+RWWfTh44yKrN5qybw/i+RjUOZGfjmsGCiV1RDhIQlPLqqyDwHrNp1sQTdS388GXREl9hYAgWte+uZWUONe9IxdYCgxqK/TKHPL97e0tDMQdITAGGIVNDXquZ+KPBo8JB2p43NOTrGyv3WmYR0gBvTC4yvadX3YzkpAHi8X3ZBJUUWn2Bf0iKc3bLf77sVbZQYeCQcdYYL5IeUlzuGYKUvVpfE'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION = 30  # mins


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
    to_encode.update({"exp": expire})
    # method creating JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


# take the token from request
# extract the id
# verify if the taken is valid
# Work as dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
