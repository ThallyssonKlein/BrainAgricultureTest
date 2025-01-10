from config.config import Config
from ports.inbound.http.main import app

config = Config()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.get("host"), port=config.get("port"))