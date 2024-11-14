from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials
from src.Webservice.init_app import user_follow_dao, user_interaction_service
from src.Webservice.jwt_bearer_webservice import JWTBearer


user_interaction_router = APIRouter(prefix="/users_interactions", tags=["User Interactions"])

@user_interaction_router.post("/{username}", status_code=status.HTTP_201_CREATED)
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

@user_interaction_router.post(
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


@user_interaction_router.delete(
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