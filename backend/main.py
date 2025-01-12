from config.config import Config
from ports.inbound.http.main import app
import uvicorn

config = Config()

if __name__ == "__main__":
    uvicorn.run(app, host=config.get("host"), port=config.get("port"))