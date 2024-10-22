# src/Webservice/API.py
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, status

from .movie_controller import movie_router
from .user_controller import user_router


def run_app():
    app = FastAPI(title="Projet Info 2A", description="Projet info")

    app.include_router(user_router)

    app.include_router(movie_router)

    uvicorn.run(app, port=8000, host="localhost")


"""
# @app.post("/login")
uvicorn.run(app, port=8000, host="localhost")
"""
