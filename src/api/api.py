from fastapi import APIRouter

from .v1 import router as v1_router

from fastapi import Request
from sse_starlette.sse import EventSourceResponse
from sh import tail
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse


router = APIRouter()

LOGFILE = "src/logs/test.log"
router.mount("/client", StaticFiles(directory="src/logs"), name="client")

# This async generator will listen to our log file in an infinite while loop (happens in the tail command)
# Anytime the generator detects a new line in the log file, it will yield it.
async def logGenerator(request):
    LOGFILE = "src/logs/test.log"
    for line in tail("-f", LOGFILE, _iter=True):
        if await request.is_disconnected():
            print("client disconnected!!!")
            break
        yield line


# This is our api endpoint. When a client subscribes to this endpoint, they will recieve SSE from our log file
@router.get("/stream-logs")
async def runStatus(request: Request):
    event_generator = logGenerator(request)
    return EventSourceResponse(event_generator)


@router.get("/")
async def get_index():
    return FileResponse("src/logs/logs.html")


router.include_router(v1_router)
