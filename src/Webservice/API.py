# src/Webservice/API.py
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse

# DAO
from src.DAO.db_connection import DBConnector
from src.DAO.tables_creation import TablesCreation
from src.Webservice.conected_user_interaction_controller import user_interaction_router,user_favorite_router
from src.Webservice.recommendation_controller import recommendation_router
from src.Webservice.movie_controller import movie_router
from src.Webservice.movie_maker_controller import movie_maker_router
from src.Webservice.user_controller import user_router
from src.Webservice.user_movie_controller import rating_movie_router, comment_movie_router

db_connection = DBConnector()
creation_object = TablesCreation(db_connection)  # creation of all table before start


def run_app():

    app = FastAPI(title="Welcome on the NOCODE API", 
    description="""
    This API allows users to get information about movies, movie makers, 
    rate them, add comments and interact with other users. 
    I let you create an account for an optimal experience.""")

    @app.get("/", include_in_schema=False)
    async def redirect_to_docs(request: Request):
        return RedirectResponse(url="/docs")

    app.include_router(user_router)
    app.include_router(movie_router)
    app.include_router(user_interaction_router)
    app.include_router(user_favorite_router)
    app.include_router(recommendation_router)
    app.include_router(movie_maker_router)
    app.include_router(rating_movie_router)
    app.include_router(comment_movie_router)
    uvicorn.run(app, port=8000, host="localhost")
