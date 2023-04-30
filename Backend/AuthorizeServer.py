from fastapi import HTTPException, status, Depends, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext
from . import Schema
from Database import database
from jose import jwt
from typing import Optional, Dict

class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")
        # print(request.cookies.get("access_token"))
        print(request.cookies.get("access_token"))
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return authorization

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
SECRET_KEY = "25b2e8d86893b06c86bc5a66bfb93ef1ff0de475bb49c7e38280b4d18dd1625a"
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login")
ALGORITHM = "HS256"

def hash_pass(password:str):
    return pwd_context.hash(password)

def verify_password(plain_pass:str, hash_pass:str):
    return pwd_context.verify(plain_pass, hash_pass)

def Exist_User(username:str, user=database.user):
    # print(user.find_one({"username": username}))
    return (user.find_one({"username": username}))

def Create_User(data:Schema.Sign_up, user=database.user):
    information = {
        "name":data.name,
        "username":data.username.lower(),
        "email":data.email,
        "phone":data.phone_number,
        "gender":data.gender,
        "dob":data.DOB,
        "password":hash_pass(data.password),
        "address":data.address,
        "payment_pref":None,
        "balance":0.0,
        "friend":[None],
        "debt":[None],
        "transaction": [None],
        "status":True
    }
    try:
        x = user.insert_one(information)
        return x.inserted_id
    except Exception as e: 
        return e

def create_access_token(data:dict):
    to_encode = data.copy()
    jwt_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return jwt_token

def get_user(username:str, user=database.user):
    info = user.find_one({"username": username}, {'_id':0, 'username':1, 'password':1})
    if info is not None:
        return {'username':info['username'], 'password':info['password']}
    else:
        return None
    

def Login(data:OAuth2PasswordRequestForm):
    user = get_user(data.username.lower())
    if not user:
        return None
    else:
        if verify_password(data.password, user['password']):
            access_token = create_access_token({"username":data.username.lower(), "password":data.password})
            # print(access_token)
            return Schema.Token(access_token=access_token, token_type='bearer')
        else:
            return None

def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials Please login to avail services /login",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try :
        
        result = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username : str = result.get("username")
        if username is None:
            return None
        data = Schema.UserData(username = username)
    except Exception as e:
        # print(e)
        raise credentials_exception
    return data