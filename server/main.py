from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routes.generate import generate_router
from .routes.ping import ping_router
from .routes.upload import upload_router


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ping_router)
app.include_router(upload_router)
app.include_router(generate_router)
