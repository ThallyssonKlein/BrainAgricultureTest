from fastapi import APIRouter


class PingController:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/ping", self.ping, methods=["GET"], status_code=200)

    def ping(self):
        return {"message": "pong"}

    def get_router(self):
        return self.router