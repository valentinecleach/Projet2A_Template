from src.Model.movie import Movie
from src.Service.movie_service import MovieService

@app.get("/movies/by_id/{id}",response_model= Movie, status_code=status.HTTP_200_OK)
def get_movie_by_id(id: int) -> Movie:
    try:
        my_movie = movie_service.get_movie_by_id(id, False)
        return my_movie
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Movie with id [{}] not found".format(id),
        ) from FileNotFoundError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request") from Exception