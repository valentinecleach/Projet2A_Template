from datetime import date
from typing import TYPE_CHECKING, Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials

# Model
from src.Model.api_user import APIUser
from src.Model.connected_user import ConnectedUser
from src.Model.jwt_response import JWTResponse

# Service
from src.Service.password_service import check_password_strenght, verify_password

# Webservice
from src.Webservice.init_app import jwt_service, user_dao, user_service
from src.Webservice.jwt_bearer_webservice import JWTBearer

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/creation", status_code=status.HTTP_201_CREATED)
def create_user(
    first_name: str,
    last_name: str,
    username: str,
    password: str,
    email_address: str,
    date_of_birth: date = Query(..., description="format : YYYY-MM-DD"),
    gender: int = Query(..., description="Put 1 for Man, 2 for a Woman"),
    phone_number: Optional[str] = Query(None),
) -> APIUser:
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
        user = user_service.sign_up(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            username=username,
            password=password,
            email_address=email_address,
            phone_number=phone_number,
        )
    except Exception as error:
        raise HTTPException(status_code=409, detail=str(error)) from error



# L'utilisateur se connecte en envoyant son nom d'utilisateur et son mot de passe.
# Si la combinaison est correcte, un token JWT est généré et renvoyé dans la réponse.


@user_router.post("/jwt", status_code=status.HTTP_201_CREATED)
def login(username: str, password_tried: str) -> JWTResponse:
    """
    Authenticate with username and password and obtain a token.
    """
    try:
        user = user_dao.get_user_by_name(username=username)
        if not user:
            raise HTTPException(status_code=403, detail="Invalid username")

        elif user_service.log_in(username, password_tried) is not True:
            raise HTTPException(status_code=403, detail="Invalid password")
        else:
            return(jwt_service.encode_jwt(user[0].id_user))
    except Exception as error:
        print(error)
        raise HTTPException(status_code=403) from error


@user_router.get("/me", dependencies=[Depends(JWTBearer())])
def get_user_own_profile(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]
) -> APIUser:
    """
    Get the authenticated user profile
    """
    return get_user_from_credentials(credentials)


def get_user_from_credentials(credentials: HTTPAuthorizationCredentials) -> APIUser:
    """
    Get a user from credentials
    """
    token = credentials.credentials
    print(token)
    user_id = int(jwt_service.validate_user_jwt(token))
    print(user_id)
    user: User | None = user_dao.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return APIUser(id= user_id, username=user.username)


