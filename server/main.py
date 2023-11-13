from fastapi import FastAPI

from .routes.generate import generate_router
from .routes.ping import ping_router
from .routes.upload import upload_router


app = FastAPI()


app.include_router(ping_router)
app.include_router(upload_router)
app.include_router(generate_router)
