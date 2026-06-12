from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.auth_routes import (
    router as auth_router
)

from app.api.gmail_routes import (
    router as gmail_router
)

from app.api.user_routes import (
    router as user_router

)

from app.api.ai_routes import router as ai_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    user_router
)

app.include_router(
    auth_router
)

app.include_router(
    gmail_router
)

app.include_router(ai_router)