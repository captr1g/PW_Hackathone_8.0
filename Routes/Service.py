from typing import List
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse
from Backend import Schema, ServiceServer, AuthorizeServer as Auth

router = APIRouter(prefix='/services', tags=['Services'])

@router.get("/", status_code=status.HTTP_302_FOUND)
def service_home(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    pass

@router.get("/add", status_code=status.HTTP_202_ACCEPTED)
def add_money(request:)