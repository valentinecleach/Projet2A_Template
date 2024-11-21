from src.Model.movie_maker import MovieMaker
from fastapi import APIRouter, HTTPException, status
from src.Webservice.init_app import movie_maker_service
from typing import List

movie_maker_router = APIRouter(prefix="/movie_makers", tags=["Movie Makers"])

@movie_maker_router.get("/name/{movie_maker_name}", response_model= List[MovieMaker], status_code=status.HTTP_200_OK)
def get_movie_maker_by_name(name: str) -> List[MovieMaker]:
    """ to get a list of MovieMaker by name"""
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

# @movie_maker_router.get("/id/{id}", response_model= MovieMaker, status_code=status.HTTP_200_OK)
# def get_movie_maker_by_id(id : int) -> MovieMaker:
#     """ to get a MovieMaker by his name"""
#     try:
#         my_movie_maker = movie_maker_service.get_movie_maker_by_id(id)  
#         if my_movie_maker is None:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"MovieMaker with id [{id}] not found"
#             )
#         return my_movie_maker
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")