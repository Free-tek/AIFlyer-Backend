import logging
from typing import Dict, Optional, Type, Union, Callable
from fastapi import FastAPI, exception_handlers, APIRouter
from fastapi_versioning import VersionedFastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount
from src.api.api import router
from src.core.error import exception_handlers
from src.core.config import settings
import os

environment = os.environ.get("ENVIRONMENT", "DEVELOPMENT")
logger = logging.getLogger(__name__)

def version_app(
    app: FastAPI,
    exception_handlers: Optional[Dict[Union[int, Type[Exception]], Callable]],
    **kwargs,
):
    extended_exception_handlers = {**exception_handlers}

    app = VersionedFastAPI(
        app,
        version_format="{major}",
        prefix_format=(
            f"{settings.API_ROOT_PATH}" + "/v{major}"
            if environment == "PRODUCTION"
            else "/v{major}"
        ),
        exception_handlers=extended_exception_handlers,
        **kwargs,
    )

    mounted_routes = [route for route in app.routes if isinstance(route, Mount)]

    if exception_handlers is not None:
        for mounted_route in mounted_routes:
            for exc, exc_handler in exception_handlers.items():
                mounted_route.app.add_exception_handler(exc, exc_handler)

    return app

def create_app():
    # Create the main app
    app = FastAPI(
        title=settings.API_TITLE,
        root_path=settings.API_ROOT_PATH,
        openapi_url="/openapi.json",
        docs_url="/docs",
    )

    # Include the router
    app.include_router(router)

    # Version the app
    app = version_app(app, exception_handlers=exception_handlers)

    from src.websockets.routes import ws_router
    app.include_router(ws_router)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app