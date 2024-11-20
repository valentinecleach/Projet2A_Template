from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Webservice.init_app import (
    recommend_service,
    user_dao,
    user_follow_dao,
    user_interaction_service,
)
from src.Webservice.jwt_bearer_webservice import JWTBearer
from src.Webservice.user_controller import get_user_from_credentials

user_interaction_router = APIRouter(
    prefix="/users_interactions", tags=["User Interactions"]
)


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
    user_to_follow_id: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
) -> str:
    """
    Allows the authenticated user to follow another user.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        user_interaction_service.follow_user(current_user.id, user_to_follow_id)
        return f"User {current_user.username} is now following user {user_to_follow_id}"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@user_interaction_router.delete(
    "/{user_id}/follow",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_204_NO_CONTENT,
)
def unfollow_user(
    user_to_unfollow_id: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
) -> None:
    """
    Allows the authenticated user to unfollow another user.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        user_interaction_service.unfollow_user(current_user.id, user_to_unfollow_id)
        return f"User {current_user.username} deosn't follow user {user_to_unfollow_id} anymore"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@user_interaction_router.post(
    "/{user_id}/favorite",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def add_favorite(
    id_movie : int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
) -> str:
    """
    Allows the authenticated user to add a film to his favorite films.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        user_interaction_service.add_favorite(current_user.id, id_movie)
        return f"User {current_user.username} is now having film {id_movie} in favorite"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@user_interaction_router.delete(
    "/{user_id}/favorite",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_favorite(
    id_movie: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
) -> None:
    """
    Allows the authenticated user to delete a film favorite.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        user_interaction_service.delete_favorite(current_user.id, id_movie)
        return f"User {current_user.username} doesn't have in favorite film {id_movie} anymore"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@user_interaction_router.post(
    "/{user_id}/recommendation_user",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def view_users(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
) -> str:
    """
    Allows the authenticated user to see a recommended list of user.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        users = recommend_service.find_users_to_follow(current_user.id)
        return users
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@user_interaction_router.post(
    "/{user_id}/recommendation_movies",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def view_movies(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
    genre: str = None,
    origin_country: str = None,
    original_language: str = None,
) -> list[Movie]:
    """
    Allows the authenticated user to see a recommended list of user.
    """
    filter = {}
    if genre:
        filter["name_genre"] = genre
    if origin_country:
        filter["origin_country"] = origin_country
    if origin_country:
        filter["original_language"] = original_language
    current_user = get_user_from_credentials(credentials)

    try:
        movies = recommend_service.find_movie_to_collect(current_user.id, filter)
        return movies
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
