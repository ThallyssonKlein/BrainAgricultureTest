import os
from dotenv import load_dotenv
from typing import Dict, Any

class Config:
    def __init__(self):        
        if not os.getenv('ENV'):
            raise ValueError("ENV is not defined")

        env_file = '.env.development'
        if os.getenv('ENV') == 'production':
            env_file = '.env.production'
        elif os.getenv('ENV') == 'development-docker':
            env_file = '.env.development-docker'
        elif os.getenv('ENV') == 'test':
            env_file = '.env.test'

        load_dotenv(env_file)
        
        self.config = {
            "env": os.getenv("ENV", "development"),
            "port": int(os.getenv("PORT", 8080)),
            "host": os.getenv("HOST", "localhost"),
            "db": {
                "user": os.getenv("DB_USER", "user"),
                "host": os.getenv("DB_HOST", "localhost"),
                "database": os.getenv("DB_DATABASE", "database"),
                "password": os.getenv("DB_PASSWORD", "password"),
                "port": int(os.getenv("DB_PORT", 5432)),
            },
        }

    def get(self, key: str) -> Any:
        return self.config.get(key)