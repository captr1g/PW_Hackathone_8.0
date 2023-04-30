from fastapi import APIRouter, Depends, status, HTTPException, Request
from Backend import Schema, AuthorizeServer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter(tags=['Authentication'])
templates = Jinja2Templates(directory="Frontend")


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def Create_Account(request:Schema.Sign_up):
    exist_user = AuthorizeServer.Exist_User(request.username)
    if exist_user is not None:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username Already Exist")
    else:
        try:
            new_user = AuthorizeServer.Create_User(request)
            return str(new_user)
        except Exception as e:
            return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e)

@router.post('/login', status_code=status.HTTP_200_OK)
def Login(request:OAuth2PasswordRequestForm = Depends()):
    access_token = AuthorizeServer.Login(request)
    if access_token is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    else:
        return access_token

@router.get('/login', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def load_login_page(request:Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get('/register', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def load_login_page(request:Request):
    return templates.TemplateResponse("signup.html", {"request": request})
