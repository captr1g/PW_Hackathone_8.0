from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import RedirectResponse
from Backend import Schema, AuthorizeServer

router = APIRouter(tags=['Authentication'])


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def Create_Account(request:Schema.Sign_up):
    exist_user = AuthorizeServer.Exist_User(request.username)
    if exist_user is True:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username Already Exist")
    else:
        AuthorizeServer.Create_User(request)


    