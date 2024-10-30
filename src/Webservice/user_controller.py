from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

#from dotenv import load_dotenv
#load_dotenv()

# Model
from src.Model.api_user import APIUser 
from src.Model.jwt_response import JWTResponse
if TYPE_CHECKING:
    from src.Model.connected_user import ConnectedUser

# Service
from src.Service.password_service import check_password_strenght

# Webservice
from src.Webservice.init_app import jwt_service, user_dao, user_service
from src.Webservice.jwt_bearer_webservice import JWTBearer


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(username: str, password: str, 
                first_name: str | None, last_name: str | None, 
                email_adress: str) -> APIUser:
    """
    Performs validation on the username and password

    Parameters
    ----------
    username : str
        The username a user wants to have

    password : str
        The password...
    
    Returns
    -------
    api_user : APIUser
    """
    try:
        check_password_strength(password=password)
    except Exception:
        raise HTTPException(status_code=400, detail="Password too weak") from Exception
    try:
        user: User = user_service.sign_up(first_name = first_name, 
                                          last_name = last_name, 
                                          username = username, 
                                          password = password, 
                                          email_address = email_address)
    except Exception as error:
        raise HTTPException(status_code=409, detail="Username already exists") from error

    return APIUser(id = user.id, 
                   username = user.username, 
                   first_name = user.first_name, 
                   last_name = user.last_name, 
                   password = user.password, 
                   email_address = user.email_address)



@user_router.post("/jwt", status_code=status.HTTP_201_CREATED)
def login(username: str, password: str) -> JWTResponse:
    """
    Authenticate with username and password and obtain a token
    """
    try:
        user = user_dao.get_user_by_name(username=username)
    
    except Exception as error:
        raise HTTPException(status_code=403, detail="Invalid username and password combination") from error

    return jwt_service.encode_jwt(user.id)

@user_router.get("/me", dependencies=[Depends(JWTBearer())])
def get_user_own_profile(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]) -> APIUser:
    """
    Get the authenticated user profile
    """
    return get_user_from_credentials(credentials)


def get_user_from_credentials(credentials: HTTPAuthorizationCredentials) -> APIUser:
    """
    Get a user from credentials
    """
    token = credentials.credentials
    user_id = int(jwt_service.validate_user_jwt(token))
    user: User | None = user_dao.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return APIUser(id=user.id, username=user.username)