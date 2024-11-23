from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Webservice.init_app import movie_dao, user_dao, user_interaction_service
from src.Webservice.jwt_bearer_webservice import JWTBearer
from src.Webservice.user_controller import get_user_from_credentials

user_interaction_router = APIRouter(
    prefix="/users_interactions", tags=["User Interactions"]
)
user_favorite_router = APIRouter(
    prefix="/users_favorite", tags=["User movie's collection"]
)


@user_interaction_router.post("/{username}", status_code=status.HTTP_201_CREATED)
def find_a_user(username: str) -> list:
    """
    Find a user registerred on the API.
    """
    try:
        user = [u.to_dict() for u in user_dao.get_user_by_name(username=username)]
        if not user:
            raise HTTPException(status_code=403, detail="No user found")

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

    if user_to_follow_id in current_user.follow_list:
        return f"User {current_user.username} is already following user {user_to_follow_id}"

    try:
        user_interaction_service.follow_user(current_user.id_user, user_to_follow_id)
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
        user_interaction_service.unfollow_user(
            current_user.id_user, user_to_unfollow_id
        )
        return f"User {current_user.username} deosn't follow user {user_to_unfollow_id} anymore"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@user_interaction_router.get(
    "/{user_id}/follow_list",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def view_my_scout_list(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
):
    """
    Allows the authenticated user to view all users he follows.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        users = [
            user_dao.get_user_by_id(id).to_dict() for id in current_user.follow_list
        ]
        if users:
            return users
        else:
            return f"User {current_user.username} doesn't follow any user yet"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@user_favorite_router.post(
    "/{user_id}/favorite",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def add_favorite(
    id_movie: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
) -> str:
    """
    Allows the authenticated user to add a film to his favorite films.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        user_interaction_service.add_favorite(current_user.id_user, id_movie)
        return f"User {current_user.username} is now having film {id_movie} in favorite"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@user_favorite_router.get(
    "/{user_id}/favorite_movies",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def view_my_favorite_movies(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
):
    """
    Allows the authenticated user to view all his favorite films.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        movies = [movie_dao.get_by_id(id) for id in current_user.own_film_collection]
        if movies:
            return movies
        else:
            return f"User {current_user.username} don't have any favorite movie yet"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@user_favorite_router.delete(
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
        user_interaction_service.delete_favorite(current_user.id_user, id_movie)
        return f"User {current_user.username} doesn't have in favorite film {id_movie} anymore"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
