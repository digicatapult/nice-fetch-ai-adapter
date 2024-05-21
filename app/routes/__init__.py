from fastapi import APIRouter
from routes import posts

router = APIRouter()
router.include_router(posts.router, tags=["posts"], prefix="/posts")
