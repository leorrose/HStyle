"""
Main api controller for HStyle api. responsable to create the fast api
app, configuring it and adding all other api that exist.
"""


from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from server.controllers import style_transfer


# create a fastapi app
app: FastAPI = FastAPI()

# define origins that can call our api
origins: List[str] = [
    "*",
]


# add our origins to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# redirect to docs when getting root of app
@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    """
    Get the initial wep api page (doc page)

    Returns:
       RedirectResponse: redirect to doc page
    """
    response: RedirectResponse = RedirectResponse(url='/docs')
    return response

# add our style transfer api
app.include_router(style_transfer.router, prefix="/api/styleTransfer",
                   tags=["styleTransfer"])
