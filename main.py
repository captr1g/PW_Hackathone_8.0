from fastapi import FastAPI
from Routes import Authorize, profile

app = FastAPI()

app.include_router(Authorize.router)
app.include_router(profile.router)