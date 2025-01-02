from fastapi import HTTPException
from datetime import datetime, timedelta
import uuid
from firebase_admin import firestore
from src.database.db import db
import hashlib
from src.model.flyer_model import DeviceInfo
from src.crud.flyer_generation import FlyerCRUD
from src.model.flyer_model import FlyerModel
import logging

logger = logging.getLogger(__name__)

class GuestUserService:
    def __init__(self):
        self.db = db
        self.guest_users_ref = db.collection('guest_users')
        
    async def create_guest_user(self, device_info: DeviceInfo) -> dict:
        """
        Create a temporary guest user using device fingerprint
        
        Args:
            device_info: Dict containing device fingerprint data like:
                {
                    'userAgent': str,
                    'language': str,
                    'platform': str,
                    'screenResolution': str,
                    'timezone': str
                }
        """
        # Create a unique device fingerprint
        device_info = device_info.model_dump()
        fingerprint = self._create_device_fingerprint(device_info)
        
        # Check if this device already has a guest account
        existing_guest = self.guest_users_ref.where(
            'device_fingerprint', '==', fingerprint
        ).limit(1).get()
        
        if existing_guest:
            raise HTTPException(
                status_code=403,
                detail="You've already used your free trial from this device. Please create an account to continue."
            )
        
        guest_id = f"guest_{fingerprint[:16]}"
        
        guest_user = {
            'user_id': guest_id,
            'device_fingerprint': fingerprint,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(hours=24),
            'is_guest': True,
            'design_count': 0,
            'device_info': device_info  # Store device info for reference
        }
        
        # Store guest user in Firestore
        self.guest_users_ref.document(guest_id).set(guest_user)
        
        return guest_user
    
    def _create_device_fingerprint(self, device_info: dict) -> str:
        """
        Create a unique hash from device information
        """
        # Combine all device info into a single string
        device_string = ''.join([
            str(device_info.get('userAgent', '')),
            str(device_info.get('language', '')),
            str(device_info.get('platform', '')),
            str(device_info.get('screenResolution', '')),
            str(device_info.get('timezone', ''))
        ])
        
        # Create SHA-256 hash of the device string
        return hashlib.sha256(device_string.encode()).hexdigest()
    
    async def check_design_limit(self, guest_id: str):
        """Check if guest user has exceeded design limit"""
        doc = self.guest_users_ref.document(guest_id).get()
        if not doc.exists:
            raise HTTPException(
                status_code=403,
                detail="Invalid guest session. Please try again."
            )
            
        guest_data = doc.to_dict()
        if guest_data['design_count'] >= 1:  # Limit guest users to 1 design
            raise HTTPException(
                status_code=429,
                detail={
                    "message": "You've reached the free design limit. Create an account to make more designs!",
                    "requires_auth": True,
                    "guest_id": guest_id
                }
            )
        
        # Increment design count
        self.guest_users_ref.document(guest_id).update({
            'design_count': guest_data['design_count'] + 1
        })
            
        return True 
    
    async def transfer_guest_designs(self, guest_id: str, permanent_user_id: str):
        """
        Transfer designs from guest account to permanent account
        
        Args:
            guest_id: The guest user ID
            permanent_user_id: The permanent user's ID
        """
        try:
            # Verify guest user exists
            guest_doc = self.guest_users_ref.document(guest_id).get()
            if not guest_doc.exists:
                raise HTTPException(
                    status_code=404,
                    detail="Guest session not found"
                )
            
            # Get all flyers for guest user
            flyer_crud = FlyerCRUD()
            guest_flyers = await flyer_crud.get_user_flyers(guest_id)
            
            # Transfer each flyer to the permanent user
            for flyer in guest_flyers:
                # Update the user_id and application_id
                flyer['user_id'] = permanent_user_id
                flyer['application_id'] = 'default'  # Or get from user's default application
                
                # Create new flyer under permanent user
                await flyer_crud.create_flyer(permanent_user_id, FlyerModel(**flyer))
            
            # Delete guest user data
            self.guest_users_ref.document(guest_id).delete()
            
            # Delete guest flyers
            await flyer_crud.delete_guest_flyers(guest_id)
            
            return {
                "message": "Designs transferred successfully",
                "transferred_count": len(guest_flyers)
            }
            
        except Exception as e:
            logger.error(f"Error transferring guest designs: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to transfer designs to new account"
            ) 