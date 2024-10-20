# src/Webservice/API.py
from typing import List
from fastapi import FastAPI, HTTPException, status
from src.Model.movie_maker import MovieMaker
from src.Model.movie import Movie
from src.Service.movie_maker_service import MovieMakerService
from src.Service.movie_service import MovieService

app = FastAPI()

movie_maker_service = MovieMakerService() 
movie_service = MovieService(None)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/movie_maker/by_name/{name}", response_model= List[MovieMaker], status_code=status.HTTP_200_OK)
def get_movie_maker_by_name(name: str) -> List[MovieMaker]:
    """ to get a list of MovieMaker by name"""
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

@app.get("/movie_maker/by_id/{id}", response_model= MovieMaker, status_code=status.HTTP_200_OK)
def get_movie_maker_by_id(id : int) -> MovieMaker:
    """ to get a MovieMaker by his name"""
    try:
        my_movie_maker = movie_maker_service.get_movie_maker_by_id(id , False)  
        if my_movie_maker is None:
            raise HTTPException(
                status_code=404,
                detail=f"MovieMaker with name [{name}] not found"
            )
        return my_movie_maker
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")



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

"""
# @app.post("/login")
uvicorn.run(app, port=8000, host="localhost")
"""

