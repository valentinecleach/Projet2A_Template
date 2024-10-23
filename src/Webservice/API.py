# src/Webservice/API.py
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import RedirectResponse

from src.Webservice.movie_controller import movie_router
#from src.Webservice.user_controller import user_router

app = FastAPI(title="Projet Info 2A", description="Projet info")

# Inclure les routeurs
app.include_router(movie_router)




def run_app():
    app = FastAPI(title="Projet Info 2A", description="Projet info")

    @app.get("/", include_in_schema=False)  # Ne pas inclure cette route dans la documentation
    async def redirect_to_docs(request: Request):
        return RedirectResponse(url="/docs")
    #app.include_router(user_router)

    app.include_router(movie_router)

    uvicorn.run(app, port=8000, host="localhost")

# Lancement seulement si le fichier est exécuté directement
if __name__ == "__main__":
    run_app()

