from typing import List

from fastapi import APIRouter, HTTPException, status

from src.Model.movie import Movie
from src.Webservice.init_app import movie_service, recommend_dao

movie_router = APIRouter(prefix="/movies", tags=["Movies"])


@movie_router.get(
    "/title/{title}", response_model=List[Movie], status_code=status.HTTP_200_OK
)
def get_movie_by_title(title: str) -> List[Movie]:
    """
    Allow a user to find a movie by its title

    Attributes
    ----------
    title : str \n
        The movie title

    Returns
    -------
    A list of movies
    """
    try:
        my_movie = movie_service.get_movie_by_title(title)
        return my_movie
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")


@movie_router.get("/id/{tmdb_id}", response_model=Movie, status_code=status.HTTP_200_OK)
def get_movie_by_id(tmdb_id: int) -> Movie:
    """
    Allow a user to find a movie by its id
    Attributes
    ----------
    tmdb_id : int \n
        The movie id

    Returns
    -------
    A movie
    """
    try:
        my_movie = movie_service.get_movie_by_id(tmdb_id)
        return my_movie
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")


@movie_router.get("/view", response_model=List[Movie], status_code=status.HTTP_200_OK)
def view_movies(
    genre: str = None,
    original_language: str = None,
) -> List[Movie]:
    """
    Allows user to see popular list of movies.

    Attributes
    ----------
    genre : str \n
        a given genre in {Comedy, Crime, Drama, Romance, Thriller, Adventure, Science Fiction, Mystery, History, Family, Fantasy, Animation, Documentary, TV Movie, Music, Horror, War, Western, Action}\n
    original_language : str \n
        a given original language in {ja, fr, da, en, pl, te, es, ko, it, zh, no, de, cn, sv}

    Returns
    -------
    A list of popular movies
    """
    filter = {}
    if genre:
        filter["name_genre"] = genre.lower()
    if original_language:
        filter["original_language"] = original_language.lower()
    try:
        my_movie = recommend_dao.get_popular_movies(filter)
        return my_movie
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
