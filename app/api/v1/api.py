from fastapi import APIRouter
from app.api.v1.endpoints import (
    posts,
    users,
    auth,
    votes
)

api_router = APIRouter()
api_router.include_router(posts.router, tags=["Posts"])
api_router.include_router(users.router, tags=["Users"])
api_router.include_router(auth.router, tags=['Login'])
api_router.include_router(votes.router, tags=["Votes"])

