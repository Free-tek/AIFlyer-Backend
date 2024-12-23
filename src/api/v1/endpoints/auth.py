import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from src.model.auth_model import CreateAccountRequest, LoginRequest, UpdateUserDetailsRequest
from src.service.api_helper import ApiHelper
from src.crud.auth import AuthCrud

logger = logging.getLogger(__name__)

# create logger with log app
real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
LOGFILE = "src/logs/test.log"

fh = logging.FileHandler(LOGFILE)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

router = APIRouter(prefix="/auth")

api_client = ApiHelper()


@router.post("/create_account", response_model=dict)
async def create_account(request: CreateAccountRequest):
    res = AuthCrud.create_account(request)

    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    
    return {
        "success": True,
        "data": {
            "user_id": res["id"],
            "token": res["token"]
        },
        "message": "Account created successfully"
    }


@router.post("/login", response_model=dict)
async def login(request: LoginRequest):
    res = AuthCrud.login(request)

    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    
    return {
        "success": True,
        "data": {
            "user_id": res["id"],
            "token": res["token"],
            "refresh_token": res["refreshToken"]
        },
        "message": "Login successful"
    }


@router.patch("/update_user_details")
async def update_user_details(request: UpdateUserDetailsRequest, user_id: str = Depends(AuthCrud.verify_token)):
    # Convert Pydantic model to dict
    update_data = request.model_dump(exclude_unset=True)
    res = AuthCrud.update_user_details(user_id, update_data)

    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    
    return res


@router.get("/get_user_details")
async def get_user_details(user_id: str = Depends(AuthCrud.verify_token)):
    res = AuthCrud.get_user_details(user_id)

    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    
    return res