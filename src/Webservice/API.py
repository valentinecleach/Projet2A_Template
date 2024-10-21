# src/Webservice/API.py
from typing import List
from fastapi import FastAPI, HTTPException, status
import uvicorn

from .MovieController import movie_router
from .UserController import user_router


def run_app():
    app = FastAPI(title="Projet Info 2A", description="Projet info")

    app.include_router(user_router)

    app.include_router(movie_router)

    uvicorn.run(app, port=8000, host="localhost")







"""
# @app.post("/login")
uvicorn.run(app, port=8000, host="localhost")
"""

