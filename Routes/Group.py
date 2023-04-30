from typing import List
from fastapi import APIRouter, Depends, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from Backend import Schema, GroupServer, AuthorizeServer as Auth

router = APIRouter(prefix='/group', tags=['Groups'])
template = Jinja2Templates(directory="Frontend")

@router.get("/", status_code=status.HTTP_302_FOUND)
def redirect_to_groups(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    return RedirectResponse('all')

@router.get("/all", response_class=HTMLResponse, status_code=status.HTTP_202_ACCEPTED)
def all_groups(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    groups = GroupServer.Get_All_Group(current_user.username)
    return template.TemplateResponse("group.html",{"request":request, "groups":groups})

@router.get("/{group_id}", response_model=Schema.GroupInfo, status_code=status.HTTP_200_OK)
def group_detail(request:Request, group_id:str, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    group = GroupServer.Get_Group(current_user.username, group_id)
    return group

@router.post("/create", status_code=status.HTTP_201_CREATED)
def new_group(request:Schema.AddGroup, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    new_group = GroupServer.Add_Group(request, current_user.username)
    return new_group

@router.get("/create/people", response_model=List[Schema.UserData], status_code=status.HTTP_200_OK)
def find_friends(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    friends = GroupServer.Find_Friend(current_user.username)
    return friends

@router.post("/{group_id}/transaction", status_code=status.HTTP_202_ACCEPTED)
def transaction(request:Schema.GroupNewTransaction, group_id:str, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    new_transaction = GroupServer.New_Transaction(request, group_id, current_user.username)
    return new_transaction