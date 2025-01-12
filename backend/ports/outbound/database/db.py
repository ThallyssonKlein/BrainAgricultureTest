from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

from config.config import Config

class DatabaseSingleton:
    __instance = None
    async_session = None

    @staticmethod
    def get_instance():
        if DatabaseSingleton.__instance is None:
            DatabaseSingleton()
        return DatabaseSingleton.__instance

    def __init__(self):
        if DatabaseSingleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            config = Config()

            DATABASE_URL = f"postgresql+asyncpg://{config.get('db')['user']}:{quote_plus(config.get('db')['password'])}@{config.get('db')['host']}:{config.get('db')['port']}/{config.get('db')['database']}"

            engine = create_async_engine(DATABASE_URL, echo=True)
            self.async_session = sessionmaker(
                bind=engine, class_=AsyncSession, expire_on_commit=False
            )

            # Atribui o objeto atual à variável de classe
            DatabaseSingleton.__instance = self

    async def get_db(self):
        async with self.async_session() as session:
            yield session
