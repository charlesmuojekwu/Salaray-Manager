from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token

class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
                
        token_data = decode_token(token)
                        
        if not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
        self.verify_token_data(token_data)

        return token_data
    
    def token_valid(self, token) -> bool:
        token_data = decode_token(token)
        return True if token_data is not None else False
    
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please overide this method in child class")
    
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get("refresh"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide valid access token")


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get("refresh"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide a refresh token")


