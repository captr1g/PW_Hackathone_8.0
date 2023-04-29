from fastapi import FastAPI
from Routes import Authorize

app = FastAPI()

app.include_router(Authorize.router)