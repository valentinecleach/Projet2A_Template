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
from src.Webservice.init_app import (
    jwt_service, 
    user_dao, 
    user_service,
    user_movie_service )
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
):
    """
    Performs creation of an user account.
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
        return f"User with username: {username} succesfully created."
    except Exception as error:
        raise HTTPException(status_code=409, detail=str(error)) from error



# L'utilisateur se connecte en envoyant son nom d'utilisateur et son mot de passe.
# Si la combinaison est correcte, un token JWT est généré et renvoyé dans la réponse.


@user_router.post("/login", status_code=status.HTTP_201_CREATED)
def login(username: str, password_tried: str) -> JWTResponse:
    """
    Authenticate with username and password_tried and obtain a token.
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


@user_router.put("/profile", dependencies=[Depends(JWTBearer())])
def update_user_own_profile(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
    new_email_adress : Optional[str] = None,
    new_phone_number : Optional[str] = None
):
    """
    Allow the user to update his email_adress and/or his phone_number
    """
    connected_user = get_user_from_credentials(credentials)
    if new_email_adress:
        connected_user.email_address = new_email_adress
        is_new_mail = True
    else:
        is_new_mail = False
    if new_phone_number:
        connected_user.phone_number = new_phone_number
    user_dao.update_user(connected_user, is_new_mail)
    return f"Account update successfull for user {connected_user.username}"

@user_router.get("/profile", dependencies=[Depends(JWTBearer())])
def get_user_own_profile(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]
):
    """
    Get the authenticated user profile
    """
    return get_user_from_credentials(credentials)

@user_router.delete("/delete_user", dependencies=[Depends(JWTBearer())])
def delete_own_profile(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]
):
    """
    Allow a user to delete his own profile.
    """
    current_user = get_user_from_credentials(credentials)
    user_movie_service.delete_user_and_update_ratings(current_user.id_user)
    

def get_user_from_credentials(credentials: HTTPAuthorizationCredentials) -> ConnectedUser:
    """
    Get a user from credentials
    """
    token = credentials.credentials
    user_id = int(jwt_service.validate_user_jwt(token))
    connected_user: ConnectedUser | None = user_dao.get_user_by_id(user_id)
    if not connected_user:
        raise HTTPException(status_code=404, detail="User not found")
    return connected_user # ça serait mieux de retourner un Connected USER !! POur avoir acces own_favorite ... quand on regarde le profil


