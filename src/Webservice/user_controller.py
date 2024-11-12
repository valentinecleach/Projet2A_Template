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
from src.Service.user_service import follow_user

# Webservice
from src.Webservice.init_app import jwt_service, user_dao, user_service
from src.Webservice.jwt_bearer_webservice import JWTBearer

# from dotenv import load_dotenv
# load_dotenv()


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

    return APIUser(username=username)


# L'utilisateur se connecte en envoyant son nom d'utilisateur et son mot de passe.
# Si la combinaison est correcte, un token JWT est généré et renvoyé dans la réponse.


@user_router.post("/jwt", status_code=status.HTTP_201_CREATED)
def login(username: str, password: str) -> JWTResponse:
    """
    Authenticate with username and password and obtain a token.
    """
    try:
        user = user_dao.get_user_by_name(username=username)
        if not user:
            raise HTTPException(status_code=403, detail="Invalid username")

        if not password_service.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=403, detail="Invalid password")

        token = jwt_service.encode_jwt(user.id_user)

        # Retourner le token JWT dans la réponse
        return JWTResponse(access_token=token)

    except Exception as error:
        raise HTTPException(
            status_code=403, detail="Invalid username or password"
        ) from error


@user_router.post("/{username}", status_code=status.HTTP_201_CREATED)
def find_a_user(username: str) -> list:
    """
    Find aa user registerred on the API.
    """
    try:
        user = user_dao.get_user_by_name(username=username)
        if not user:
            raise HTTPException(status_code=403, detail="Invalid username")

        # Return the list with all the user matching
        return user
    except Exception as error:
        raise HTTPException(status_code=403, detail="Invalid username") from error


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
    user_id = int(jwt_service.validate_user_jwt(token))
    user: User | None = user_dao.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return APIUser(id=user.id, username=user.username)


@user_router.post(
    "/{user_id}/follow",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def follow_user(
    user_id: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
) -> str:
    """
    Allows the authenticated user to follow another user.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        user_service.follow_user(current_user.id, user_id)
        return f"User {current_user.username} is now following user {user_id}"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@user_router.delete(
    "/{user_id}/follow",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_204_NO_CONTENT,
)
def unfollow_user(
    user_id: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
) -> None:
    """
    Allows the authenticated user to unfollow another user.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        user_service.unfollow_user(current_user.id, user_id)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
