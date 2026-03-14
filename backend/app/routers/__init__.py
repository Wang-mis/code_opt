"""Routers package."""
from fastapi import APIRouter
from .problems import router as problems_router
from .submissions import router as submissions_router
from .evaluate import router as evaluate_router
from .review import router as review_router

api_router = APIRouter()
api_router.include_router(problems_router)
api_router.include_router(submissions_router)
api_router.include_router(evaluate_router)
api_router.include_router(review_router)