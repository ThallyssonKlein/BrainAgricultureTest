from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config.config import Config

config = Config()

DATABASE_URL = f"postgresql+asyncpg://{config.get('db')['user']}:{config.get('db')['password']}@{config.get('db')['host']}:{config.get('db')['port']}/{config.get('db')['database']}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session