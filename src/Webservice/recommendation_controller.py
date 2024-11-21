from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from src.Model.movie import Movie
from src.Model.connected_user import ConnectedUser

from src.Webservice.init_app import (
    recommend_service,
    user_dao,
    user_follow_dao,
    user_interaction_service,
)
from src.Webservice.jwt_bearer_webservice import JWTBearer
from src.Webservice.user_controller import get_user_from_credentials

recommendation_router = APIRouter(
    prefix="/recommendation", tags=["Users and Movies Recommendation"]
)
@recommendation_router.get(
    "/{user_id}/recommendation_user",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def view_users(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
)-> list[ConnectedUser]:
    """
    Allows the authentificated user to see a recommended list of user.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        users = [u.to_dict() for u in recommend_service.find_users_to_follow(current_user.id_user)]
        return users
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@recommendation_router.get(
    "/{user_id}/recommendation_movies",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def view_movies(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
    genre: str = None,
    original_language: str = None,
) -> list[Movie]:
    """
    Allows the authenticated user to see a recommended list of user.
    """
    filter = {}
    if genre:
        filter["name_genre"] = genre.lower()
    if original_language:
        filter["original_language"] = original_language.lower()
    current_user = get_user_from_credentials(credentials)

    try:
        movies = recommend_service.find_movie_to_collect(current_user.id_user, filter)
        return movies
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
