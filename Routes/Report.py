from typing import List
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from Backend import Schema, ReportServer, AuthorizeServer as Auth

router = APIRouter(prefix='/services', tags=['Services'])
template = Jinja2Templates(directory="Frontend")

@router.get("/", status_code=status.HTTP_302_FOUND)
def service_home(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    pass

@router.get("/finance_report", status_code=status.HTTP_200_OK)
def finance_report(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    finance = ReportServer.Finance(current_user.username)
    return finance


@router.get("/debt_report", status_code=status.HTTP_200_OK)
def debt(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    debt = ReportServer.Debt(current_user.username)
    return debt


@router.get("/payment_history", status_code=status.HTTP_200_OK)
def history(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    transaction = ReportServer.History(current_user.username)
    return transaction