from fastapi import APIRouter

from api.routes.status_routes import status_router
from api.routes.pdf_routes import pdf_router
from api.routes.website_routes import website_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(status_router)
v1_router.include_router(pdf_router)
v1_router.include_router(website_router)
