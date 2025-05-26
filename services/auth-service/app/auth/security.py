from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


from .utils import verify_password
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


async def authenticate_user(request: Request, email: str, password: str):
    # Get user by email
    query = "SELECT * FROM c WHERE c.email = @email"
    parameters = [{"name": "@email", "value": email}]

    items = []
    async for item in request.app.user_container.query_items(
            query=query,
            parameters=parameters,
            #enable_cross_partition_query=True
    ):
        items.append(item)

    if not items:
        return False

    user = items[0]
    if not verify_password(password, user["hashed_password"]):
        return False

    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    from main import app  # Import here to avoid circular imports


    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Get user from database
    query = "SELECT * FROM c WHERE c.email = @email"
    parameters = [{"name": "@email", "value": email}]

    items = []
    async for item in app.user_container.query_items(
            query=query,
            parameters=parameters,
            #enable_cross_partition_query=True
    ):
        items.append(item)

    if not items:
        raise credentials_exception

    user = items[0]
    if not user.get("is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")

    return user