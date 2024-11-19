from typing import List
from src.Model.movie import Movie
from src.Service.movie_service import MovieService
from fastapi import APIRouter, HTTPException, status
from src.Webservice.init_app import movie_dao, movie_service

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

