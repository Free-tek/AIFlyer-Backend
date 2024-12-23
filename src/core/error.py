from starlette.requests import Request
from starlette.responses import JSONResponse
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class InvalidRequest(Exception):
    pass

class InvalidToken(Exception):
    pass

async def bad_request_exception_handler(
    request: Request = None, exception: InvalidRequest = None
):
    return JSONResponse(
        status_code=400, content={"message": "Invalid request", "status": False}
    )

async def invalid_token_exception_handler(request: Request, exc: InvalidToken):
    return JSONResponse(
        status_code=401, content={"message": "Not authenticated, Invalid Token"}
    )



exception_handlers = {
    InvalidRequest: bad_request_exception_handler,
    InvalidToken: invalid_token_exception_handler

}

