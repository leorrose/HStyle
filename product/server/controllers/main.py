from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from controllers import style_transfer

# define our fastapi
app: FastAPI = FastAPI()

# define origins that can call our api
origins: List[str] = [
    "*",
    "http://localhost:4200"
]

# add our origins to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# on app open redirect to docs
@app.get("/")
async def root() -> RedirectResponse:
    """
    Get the initial wep api page (doc page)

    Returns:
       RedirectResponse: redirect to doc page
    """
    response: RedirectResponse = RedirectResponse(url='/docs')
    return response

# add our style transfer end points
app.include_router(style_transfer.router, prefix="/styleTransfer", tags=["styleTransfer"])
