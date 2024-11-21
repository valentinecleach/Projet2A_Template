from typing import List
from src.Model.movie import Movie
from src.Service.movie_service import MovieService
from fastapi import APIRouter, HTTPException, status
from src.Webservice.init_app import movie_dao, movie_service,recommend_dao

movie_router = APIRouter(prefix="/movies", tags=["Movies"])

@movie_router.get("/title/{title}", response_model= List[Movie], status_code=status.HTTP_200_OK)
def get_movie_by_title(title: str) -> List[Movie]:
    try:
        my_movie = movie_service.get_movie_by_title(title)
        return my_movie
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")

@movie_router.get("/id/{tmdb_id}",response_model= Movie, status_code=status.HTTP_200_OK)
def get_movie_by_id(tmdb_id: int) -> Movie:
    try:
        my_movie = movie_service.get_movie_by_id(tmdb_id)
        return my_movie
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")

@movie_router.get("/movies", response_model= List[Movie], status_code=status.HTTP_200_OK)
def view_movies(
    genre: str = None,
    original_language: str = None,
    ) -> List[Movie]:
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

# @movie_router.get("/users", response_model= List[Movie], status_code=status.HTTP_200_OK)
# def get_movie_by_title(title: str) -> List[Movie]:
#     try:
#         my_movie = movie_service.get_movie_by_title(title)
#         return my_movie
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
