from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import RedirectResponse
from Backend import Schema, GroupServer, AuthorizeServer as Auth

router = APIRouter(prefix='/groups', tags=['Groups'])

@router.get("/", status_code=status.HTTP_302_FOUND)
def redirect_to_groups(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    return RedirectResponse('all')

@router.get("/{group_id}", response_model=Schema,status_code=status.HTTP_200_OK)
def group_detail(request:Request, group_id:str, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    group = GroupServer.get_group(current_user, group_id)