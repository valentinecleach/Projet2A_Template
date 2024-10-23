from src.Model.movie import Movie
from src.Service.movie_service import MovieService
from fastapi import APIRouter, HTTPException, status

movie_router = APIRouter(prefix="/movies", tags=["Movies"])


@movie_router.get("/{tmdb_id}",response_model= Movie, status_code=status.HTTP_200_OK)
def get_movie_by_id(tmdb_id: int) -> Movie:
    try:
        my_movie = MovieService().get_movie_by_id(tmdb_id)
        return my_movie
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Movie with id [{}] not found".format(tmdb_id),
        ) from FileNotFoundError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request") from Exception

@movie_router.get("/{title}",response_model= Movie, status_code=status.HTTP_200_OK)
def get_movie_by_title(title: str) -> Movie:
    try:
        my_movie = MovieService().get_movie_by_title(title)
        return my_movie
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Movie with title [{}] not found".format(name),
        ) from FileNotFoundError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request") from Exception