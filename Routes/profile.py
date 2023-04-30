from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from Database import database
from Backend import Schema,Profile_backend, AuthorizeServer as Auth

router = APIRouter( prefix='/profile', tags=['Profile'])

@router.get("/", status_code=status.HTTP_200_OK)
def redirect_to_profile(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    return RedirectResponse(f'{current_user.username}')

@router.get("/{username}", status_code=status.HTTP_200_OK)
def profile_Finder(request:Request, username:str):
    if username == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User, with {username} not exist")
    current_user = Auth.get_current_user(request.cookies.get("access_token"))
    if current_user == None:
        return  Profile_backend.public_profile(username)
    else:
        data = Profile_backend.profile_Finder_backend(username)
        return data
