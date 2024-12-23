from fastapi import APIRouter, FastAPI

from .endpoints import (
    auth_router,
    billing_router
)

router = APIRouter()
router.include_router(auth_router, tags=["auth"])
router.include_router(billing_router, tags=["billing"])