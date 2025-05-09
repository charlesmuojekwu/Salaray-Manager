import aioredis
from src.config import Config

token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti, value="", exp=Config.ACCESS_TOKEN_EXPIRY
    )
    
    
async def token_in_blocklist(jti: str) -> bool:
    pass