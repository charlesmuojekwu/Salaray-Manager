from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from .schemas import UserCreateModel, UserModel, UserLoginModel, UserAuthenticatedModel
from .service import AuthService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import verify_password, create_access_token
from ..utils.responses import success, error, paginated_response
from ..utils.base_response import SuccessResponse, PaginatedResponse
from .dependencies import RefreshTokenBearer
from datetime import datetime


auth_router = APIRouter()
auth_service = AuthService()


@auth_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=SuccessResponse[UserModel])
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await auth_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    
    new_user = await auth_service.create_user(user_data, session)
    return success(data=new_user, message="Registration successful")



@auth_router.post('/login', status_code=status.HTTP_200_OK, response_model=SuccessResponse[UserAuthenticatedModel])
async def login_user(user_login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = user_login_data.email
    password = user_login_data.password
    user = await auth_service.get_user_by_email(email, session)
    
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        
        if password_valid:
            access_token, refresh_token = await auth_service.login_user(user)
            user_logged_In = {
                    "access_token" : access_token,
                    "refresh_token" : refresh_token,
                    "user":user
                  }
            
            return success(data=user_logged_In, message="Login successful")

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email Or Password")
        

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details:dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token" : new_access_token
            }
        )
        
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
