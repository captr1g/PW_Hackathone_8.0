from django import template
from fastapi import FastAPI, Request, status
from Routes import Authorize, Group, profile, Service
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="PayShift",
    description="PW Hackathon 8.0 Problem 6 Equishare exprense",
    version="1.0.0"
)
template=Jinja2Templates(directory="Frontend")



app.include_router(Authorize.router)
app.include_router(Group.router)
app.include_router(profile.router)
app.include_router(Service.router)

@app.get('/', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def home(request:Request):
    return template.TemplateResponse("home.html", {"request": request})