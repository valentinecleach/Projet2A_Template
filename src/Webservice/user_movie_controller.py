from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.rating import Rating
from src.Webservice.init_app import (
    recommend_service,
    user_dao,
    user_follow_dao,
    user_movie_service,
)
from src.Webservice.jwt_bearer_webservice import JWTBearer
from src.Webservice.user_controller import get_user_from_credentials

rating_movie_router = APIRouter(prefix="/rating", tags=["Rating Movie"])
comment_movie_router = APIRouter(prefix="/comment", tags=["Comment Movie"])
#### Rating Section ###########

@rating_movie_router.post(
    "/{user_id}/add_or_update_movie_rating",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def add_or_update_movie_rate(
    id_movie: int,
    rate: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
):
    current_user = get_user_from_credentials(credentials)
    try:
        user_movie_service.rate_film_or_update(current_user.id_user, id_movie, rate)
        return f"User {current_user.username} put the rate : {rate} for movie with id : {id_movie}"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@rating_movie_router.get(
    "/{user_id}/get_a_user_rate",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def get_ratings_for_a_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
    id_movie: Optional[int] = None
):
    """
    Display all the ratings of the user.
    If id_movie is entered, display the rating provided by the user for this particular moovie.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        if id_movie :
            rating = user_movie_service.rating_dao.get_rating(current_user.id_user, id_movie)
            if rating:
                return f"{rating}"
            else:
                f"You haven't rated this movie yet!"
        else :
            ratings = user_movie_service.get_ratings_user(current_user.id_user)
            if ratings:
                return [f"{rating}" for rating in ratings]
            else:
                f"You haven't rated a movie yet!"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@rating_movie_router.delete(
    "/{user_id}/delete_a_movie_rate",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def delete_a_user_rating(
    id_movie : int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
):
    current_user = get_user_from_credentials(credentials)
    try:
        rating = user_movie_service.rating_dao.get_rating(current_user.id_user, id_movie)
        if rating:
            user_movie_service.delete_a_user_rating(rating)
            return f" Rating deletion for the movie with id {id_movie} completed."
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

##### Comment Section ##############

@comment_movie_router.post(
    "/{user_id}/comment",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def add_or_update_comment(
    id_movie: int,
    comment: str,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
) -> str:
    """
    Allows the authenticated user to follow another user.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        user_movie_service.add_or_update_comment(current_user.id_user, id_movie, comment)
        return "Your comment has been shared successfully"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

@comment_movie_router.get(
    "/{user_id}/get_a_user_comment",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def get_comments_for_a_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
    id_movie: Optional[int] = None
):
    """
    Display all the comments of the user.
    If id_movie is entered, display the comment provided by the user for this particular moovie.
    """
    current_user = get_user_from_credentials(credentials)
    try:
        if id_movie :
            comment = user_movie_service.comment_dao.get_comment(current_user.id_user, id_movie)
            if comment : 
                return f"{comment}"
            else:
                return f"You haven't commented this movie yet!"
        else :
            comments = user_movie_service.get_comments_user(current_user.id_user)
            if comments : 
                return [f"{c}" for c in comments]
            else:
                return f"You haven't commented a movie yet!"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

@comment_movie_router.get(
    "/{user_id}/get_last_comment",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def get_last_comments_movie(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
    id_movie: int
):
    """
    Display 10 last comments for a movie
    """
    current_user = get_user_from_credentials(credentials) # pas utile ?
    try:
        comments = user_movie_service.comment_dao.get_recent_comments_for_a_movie(id_movie = id_movie, limit = 10)
        if comments :
            return [f"{c}" for c in comments]
        else:
            return "No comments for this movie for the moment"
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@comment_movie_router.delete(
    "/{user_id}/delete_comment_for_a_movie",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
def delete_a_user_comment(
    id_movie : int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
):
    current_user = get_user_from_credentials(credentials)
    try:
        comment = user_movie_service.comment_dao.get_comment(current_user.id_user, id_movie)
        if comment:
            user_movie_service.delete_a_user_comment(comment)
            return f" Comment deletion for the movie with id {id_movie} completed."
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error