import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from .models import UserRegister, UserResponse, TokenResponse
from .security import create_access_token, authenticate_user, get_current_user
from .utils import get_password_hash
from ..config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(request: Request, user_data: UserRegister):
    # Check if user already exists
    existing_user = await get_user_by_email(request, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create new user
    user_dict = {
        "id": str(uuid.uuid4()),
        "email": user_data.email,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "is_active": True,
        "created_at": datetime.utcnow().isoformat(),
        "hashed_password": get_password_hash(user_data.password)
    }

    new_user = await request.app.user_container.create_item(user_dict)

    # Return user without password
    response_user = {k: v for k, v in new_user.items() if k != "hashed_password"}
    return response_user


@router.post("/login", response_model=TokenResponse)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(request, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login
    user_dict = jsonable_encoder(user)
    user_dict["last_login"] = datetime.utcnow().isoformat()
    await request.app.user_container.replace_item(user["id"], user_dict)

    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "user_id": user["id"]},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


# @router.post("/token", response_model=TokenResponse)
# async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await authenticate_user(request, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     # Update last login
#     user_dict = jsonable_encoder(user)
#     user_dict["last_login"] = datetime.utcnow().isoformat()
#     await request.app.user_container.replace_item(user["id"], user_dict)
#
#     access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user["email"], "user_id": user["id"]},
#         expires_delta=access_token_expires
#     )
#
#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#         "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
#     }


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    # Return user without password
    response_user = {k: v for k, v in current_user.items() if k != "hashed_password"}
    return response_user


# Helper function to get user by email
# async def get_user_by_email(request: Request, email: str) -> Optional[dict]:
#     query = "SELECT * FROM c WHERE c.email = @email"
#     parameters = [{"name": "@email", "value": email}]
#
#     items = []
#     async for item in request.app.user_container.query_items(
#             query=query,
#             parameters=parameters,
#             enable_cross_partition_query=True
#     ):
#         items.append(item)
#
#     return items[0] if items else None


# Helper function to get user by email
async def get_user_by_email(request: Request, email: str) -> Optional[dict]:
    query = "SELECT * FROM c WHERE c.email = @email"
    parameters = [{"name": "@email", "value": email}]

    try:
        items = []
        async for item in request.app.user_container.query_items(
                query=query,
                parameters=parameters
        ):
            items.append(item)

        return items[0] if items else None
    except Exception as e:
        print(f"Error querying user by email: {e}")
        return None
