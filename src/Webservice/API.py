import uvicorn
from fastapi import FastAPI, HTTPException, status

from src.Model.Movie import Movie
from src.Service.MovieService import MovieService


def run_app(movie_service: MovieService):
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.get("/movies/{tmdb_id}", status_code=status.HTTP_200_OK)
    def get_movie_by_id(tmdb_id: int) -> Movie:
        try:
            my_movie: Movie = movie_service.get_by_id(tmdb_id)
            return my_movie
        except FileNotFoundError:
            raise HTTPException(
                status_code=404,
                detail="Movie with id [{}] not found".format(tmdb_id),
            ) from FileNotFoundError
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid request") from Exception

    # @app.post("/login")
    uvicorn.run(app, port=8000, host="localhost")

# Lancement de l'application sur le le port 80
if __name__ == "__main__":
    run_app(None) # prend MovieService en argument normalement


