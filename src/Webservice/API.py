# src/Webservice/API.py
from typing import List
from fastapi import FastAPI, HTTPException, status
from src.Model.movie_maker import MovieMaker
from src.Service.movie_maker_service import MovieMakerService

app = FastAPI()

movie_maker_service = MovieMakerService() 

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/movie_maker/{name}", response_model= List[MovieMaker], status_code=status.HTTP_200_OK)
def get_movie_maker_by_name(name: str) -> MovieMaker:
    """ to get a MovieMaker by his name"""
    try:
        my_movie_makers = movie_maker_service.get_movie_maker_by_name(name , False)  
        if my_movie_makers is None:
            raise HTTPException(
                status_code=404,
                detail=f"MovieMaker with name [{name}] not found"
            )
        return my_movie_makers
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")



"""
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
"""



