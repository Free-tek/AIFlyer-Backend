import os
import logging
from fastapi import APIRouter, HTTPException, Depends, Request
from src.service.api_helper import ApiHelper
from src.crud.billing import BillingCrud
from fastapi_versioning import version


logger = logging.getLogger(__name__)

# create logger with log app
real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
LOGFILE = "src/logs/test.log"

fh = logging.FileHandler(LOGFILE)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

router = APIRouter(prefix="/billing")

api_client = ApiHelper()


@router.post("/stripe_webhook", status_code=200)
@version(1)
async def stripe_webhook(request: Request):  
    try:
        data = await request.json()
        logger.info(f"Received Stripe webhook: {data.get('type')}")
        
        billing_crud = BillingCrud()
        billing_crud.process_stripe_webhook(data)
        
        return {
            "status": "success",
            "message": "Stripe webhook processed successfully"
        }
    except Exception as e:
        logger.error(f"Error processing Stripe webhook: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing webhook: {str(e)}"
        )