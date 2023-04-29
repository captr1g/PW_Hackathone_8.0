from fastapi import FastAPI
from Routes import Authorize, Group

app = FastAPI(
    title="PayShift",
    description="PW Hackathon 8.0 Problem 6 Equishare exprense",
    version="1.0.0"
)

app.include_router(Authorize.router)
app.include_router(Group.router)