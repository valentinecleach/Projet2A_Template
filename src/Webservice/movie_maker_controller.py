from src.Model.movie_maker import MovieMaker
from fastapi import APIRouter, HTTPException, status
from src.Webservice.init_app import movie_maker_service
from typing import List

movie_maker_router = APIRouter(prefix="/movie_makers", tags=["Movie Makers"])

@movie_maker_router.get("/name/{movie_maker_name}", response_model= List[MovieMaker], status_code=status.HTTP_200_OK)
def get_movie_maker_by_name(name: str) -> List[MovieMaker]:
    """ 
    To get a list of MovieMaker by name

    Attributes
    ----------
    name : str \n
        The name of the movie maker

    Returns
    -------
    A list of movie makers
    """
    try:
        my_movie_makers = movie_maker_service.get_movie_maker_by_name(name)  
        if my_movie_makers is None:
            raise HTTPException(
                status_code=404,
                detail=f"MovieMaker with name [{name}] not found"
            )
        return my_movie_makers
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
