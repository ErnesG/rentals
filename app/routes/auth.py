from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.services.user_service import UserService
from app.core.container import get_user_service
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=User)
async def register(
    user: User,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.create_user(user)

@router.post("/login")
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
    # Return JWT token here
    return {"access_token": "token", "token_type": "bearer"} 