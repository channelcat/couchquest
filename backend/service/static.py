from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


# Static Files
def bind_static(api: FastAPI):
    api.mount("/static", StaticFiles(directory="/api/static"), name="static")

    @api.get("/")
    def index():
        return FileResponse("/api/static/index.html")
