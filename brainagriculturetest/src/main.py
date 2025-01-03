from fastapi import FastAPI
from brainagriculturetest.src.adapters.inbound.http.example_adapter import router as http_router

# Instância da aplicação FastAPI
app = FastAPI()

# Incluindo as rotas do adaptador HTTP
app.include_router(http_router)