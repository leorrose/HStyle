import os
from fastapi import FastAPI, Request
from controllers import todo, auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


angular_project_folder = f"{os.path.dirname(__file__)}/../../client/angular/dist/angular/"

app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


templates = Jinja2Templates(directory=angular_project_folder)
app.mount("/static", StaticFiles(directory=angular_project_folder), name="static")
app.include_router(todo.router, prefix="/api/todo", tags=["todo"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
