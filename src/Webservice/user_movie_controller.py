from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Webservice.init_app import (
    recommend_service,
    user_dao,
    user_follow_dao,
    user_movie_service,
)
from src.Webservice.jwt_bearer_webservice import JWTBearer
from src.Webservice.user_controller import get_user_from_credentials

user_movie_router = APIRouter(prefix="/users_movie", tags=["User Movie"])


@user_movie_router.post(
    "/{user_id}/rating_movie",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def rate_movie(id_movie : int, rate:int, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],):
    current_user = get_user_from_credentials(credentials)
    try:
        user_movie_service.rate_film(current_user.id, id_movie, rate)
        return f"User {current_user.username} put the rate : {rate} for movie with id : {id_movie}"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@user_movie_router.post(
    "/{user_id}/comment",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def add_comment(
    id_movie: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
) -> str:
    """
    Allows the authenticated user to follow another user.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        user_movie_service.add_comment(current_user.id, id_movie)
        return f"Your comment has been shared successfully"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
