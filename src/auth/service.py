from .model import User
from .schemas import UserCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .utils import generate_password_hash
from datetime import datetime,timedelta
from .utils import create_access_token, decode_token, verify_password
from src.config import Config
from typing import Tuple

class AuthService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user
    
    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False
    
    async def create_user(self, user_data:UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(
            **user_data_dict
        )
        new_user.password_hash = generate_password_hash(user_data_dict['password'])
        new_user.join_date = datetime.strptime(user_data_dict['join_date'], "%Y-%m-%d")

        session.add(new_user)
        await session.commit()
        return new_user
    
    async def login_user(self, user:User) -> Tuple[str, str]:
            access_token = create_access_token(
                user_data = {
                    'email': user.email,
                    'user_uid': str(user.uid)
                }
            )
            
            refresh_token = create_access_token(
                user_data = {
                    'email': user.email,
                    'user_uid': str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=Config.REFRESH_TOKEN_EXPITY)
            )
            
            return access_token, refresh_token