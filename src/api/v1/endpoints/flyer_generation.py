import os
import logging
from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from src.service.api_helper import ApiHelper
from fastapi_versioning import version
from src.crud.flyer_generation import flyer_crud
from src.model.flyer_model import FlyerCreate, FlyerUpdate, FlyerResponse, FlyerModel, FlyerDownload
from src.service.conversational_flyer_generator import ConversationalFlyerGenerator
from src.service.guest_user_service import GuestUserService
from src.core.config import settings
from src.crud.auth import AuthCrud
import requests
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io

logger = logging.getLogger(__name__)

# create logger with log app
real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
LOGFILE = "src/logs/test.log"

fh = logging.FileHandler(LOGFILE)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

router = APIRouter(prefix="/flyer_generation")

api_client = ApiHelper()

generator = ConversationalFlyerGenerator()

@router.post("/create_flyer")
@version(1)
async def create_flyer(
    flyer_in: FlyerCreate,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(AuthCrud.verify_token),
):
    """Create a new flyer"""


    flyer_model = await generator.generate_flyer(flyer_in, user_id)
    if type(flyer_model) == FlyerModel:
        if flyer_in.flyer_description:
            return {"message": "Flyer generated successfully", "data": {"flyer": flyer_model.model_dump(), "message": f"Done creating this flyer for you, will you like to make any changes?"}, "status": "success"}
        else:
            result = {"message": "Flyer generated successfully", "data": {"flyer": flyer_model.model_dump(), "message": f"I came up with a flyer concept for you, it is centered around {flyer_model.flyer_design_query.marketing_idea}"}, "status": "success"}
            print(f"result: {result}")
            return {"message": "Flyer generated successfully", "data": {"flyer": flyer_model.model_dump(), "message": f"I came up with a flyer concept for you, it is centered around {flyer_model.flyer_design_query.marketing_idea}"}, "status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Failed to generate an automatic flyer, please tell me what you'll like to design.")


@router.post("/create_flyer_guest")
async def create_flyer_guest(
    flyer_in: FlyerCreate
):
    """Create a new flyer"""
    try:
        # If no user_id, create a guest session
        guest_service = GuestUserService()
        guest_user = await guest_service.create_guest_user(flyer_in.device_info)
        user_id = guest_user['user_id']

        flyer_model = await generator.generate_flyer(flyer_in, user_id)
        
        if type(flyer_model) == FlyerModel:
            if flyer_in.flyer_description:
                return {"message": "Flyer generated successfully", "data": {"flyer": flyer_model.model_dump(), "message": f"Done creating this flyer for you, will you like to make any changes?"}, "status": "success"}
            else:
                result = {"message": "Flyer generated successfully", "data": {"flyer": flyer_model.model_dump(), "message": f"I came up with a flyer concept for you, it is centered around {flyer_model.flyer_design_query.marketing_idea}"}, "status": "success"}
                print(f"result: {result}")
                return {"message": "Flyer generated successfully", "data": {"flyer": flyer_model.model_dump(), "message": f"I came up with a flyer concept for you, it is centered around {flyer_model.flyer_design_query.marketing_idea}"}, "status": "success"}
        else:
            raise HTTPException(status_code=400, detail="Failed to generate an automatic flyer, please tell me what you'll like to design.")

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in create_flyer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/update")
async def update_flyer(
    flyer_update: FlyerUpdate,
    user_id: str = Depends(AuthCrud.verify_token),
):
    try:
        generator = ConversationalFlyerGenerator()
        result = await generator.process_command(flyer_update, user_id)
        
        # Check if result is an exception
        if isinstance(result, Exception):
            raise result
            
        # Ensure result is a dictionary
        if not isinstance(result, dict):
            result = {"flyer": result}

        print(f"result: {result}")
            
        return {
            "message": "Flyer updated successfully",
            "data": result,
            "status": "success"
        }
        
    except HTTPException as he:
        raise HTTPException(status_code=500, detail="Failed to generate an automatic flyer, please tell me what you'll like to design.")
    except Exception as e:
        logger.error(f"Error in update_flyer: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate an automatic flyer, please tell me what you'll like to design.")
    

@router.post("/update_flyer_guest")
async def update_flyer_guest(
    flyer_update: FlyerUpdate
):
    # try:

    guest_service = GuestUserService()
    guest_user = guest_service.get_guest_user(flyer_update.device_info)
    user_id = guest_user['user_id']
    
    generator = ConversationalFlyerGenerator()
    result = await generator.process_command(flyer_update, user_id)
    
    # Check if result is an exception
    if isinstance(result, Exception):
        raise result
        
    # Ensure result is a dictionary
    if not isinstance(result, dict):
        result = {"flyer": result}

    print(f"result: {result}")
        
    return {
        "message": "Flyer updated successfully",
        "data": result,
        "status": "success"
    }
        
    # except HTTPException as he:
    #     raise HTTPException(status_code=500, detail="Failed to generate an automatic flyer, please tell me what you'll like to design.")
    # except Exception as e:
    #     logger.error(f"Error in update_flyer: {str(e)}")
    #     raise HTTPException(status_code=500, detail="Failed to generate an automatic flyer, please tell me what you'll like to design.")
    


@router.post("/export")
@version(1)
async def export_flyer(
    flyer_id: str,
    user_id: str = Depends(AuthCrud.verify_token)
):
    """Export the flyer to a file"""
    print(f"this is export flyer id: {flyer_id}")
    response = await generator.export_flyer(user_id, flyer_id)
    if type(response) == list:
        result = {"message": "Flyer exported successfully", "data": {"flyer": [design.model_dump() for design in response]}, "status": "success"}
        print(f"this is result: {result}")
        return result
    else:
        return response

@router.get("/get_flyer/{flyer_id}")
@version(1)
async def get_flyer(
    flyer_id: str,
    user_id: str = Depends(AuthCrud.verify_token)
):
    """Get a flyer by ID"""
    flyer = await flyer_crud.get_flyer(user_id, flyer_id)
    if type(flyer) == dict:
        return {"message": "Flyer fetched successfully", "data": {"flyer": flyer}, "status": "success"}
    else:
        raise HTTPException(status_code=404, detail="Flyer not found")
    
@router.get("/get_all_flyers")
@version(1)
async def get_all_flyers(user_id: str = Depends(AuthCrud.verify_token)):
    """Get all flyers"""
    print(f"this is the user id: {user_id}")
    flyers = await flyer_crud.get_user_flyers(user_id)
    return {"message": "Flyers fetched successfully", "data": {"flyers": flyers}, "status": "success"}

@router.delete("/{flyer_id}")
@version(1)
async def delete_flyer(
    flyer_id: str,
    user_id: str = Depends(AuthCrud.verify_token)
):
    """Delete a flyer"""
    success = await flyer_crud.delete_flyer(user_id, flyer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Flyer not found")
    return {"message": "Flyer deleted successfully"}

@router.post("/download")
async def download_file(flyer_download: FlyerDownload, user_id: str = Depends(AuthCrud.verify_token)):
    try:
        # Download the file from Firebase Storage
        response = requests.get(flyer_download.url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to download file")

        # Create a byte stream from the content
        content = io.BytesIO(response.content)
        
        # Return the file content with appropriate headers
        return StreamingResponse(
            content,
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f'attachment; filename="flyer.jpg"',
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, token",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))