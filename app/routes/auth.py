from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_service import UserService
from app.core.container import get_user_service
from app.models.user import User
from app.utils.jwt import create_access_token
from app.core.auth import get_current_user
from typing import Dict

router = APIRouter()

@router.post("/register", response_model=User)
async def register(
    user_data: dict,
    user_service: UserService = Depends(get_user_service)
):
    # Create User object from dict, excluding password from response
    user = User(**user_data)
    created_user = await user_service.create_user(user)
    # Remove password from response
    created_user_dict = created_user.dict()
    created_user_dict.pop('password', None)
    return User(**created_user_dict)

@router.post("/login", response_model=Dict)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    # Remove password from response
    user_dict = current_user.dict()
    user_dict.pop('password', None)
    return User(**user_dict) 