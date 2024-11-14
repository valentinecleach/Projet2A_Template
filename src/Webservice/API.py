# src/Webservice/API.py
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import RedirectResponse

# DAO
from src.DAO.db_connection import DBConnector
from src.DAO.tables_creation import TablesCreation

from src.Webservice.movie_controller import movie_router
from src.Webservice.user_controller import user_router
from src.Webservice.conected_user_interaction_controller import user_interaction_router

db_connection = DBConnector()  
creation_object = TablesCreation(db_connection) # creation of all table before start


def run_app():

    app = FastAPI(title="Projet Info 2A", description="Projet info")

    @app.get("/", include_in_schema=False)  
    async def redirect_to_docs(request: Request):
        return RedirectResponse(url="/docs")

    app.include_router(user_router)
    app.include_router(movie_router)
    app.include_router(user_interaction_router)
    uvicorn.run(app, port=8000, host="localhost")



