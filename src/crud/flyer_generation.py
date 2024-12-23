from typing import Dict, Optional, List
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from src.database.db import flyers_data_ref
from src.model.flyer_model import FlyerModel, FlyerConversation
import logging
import uuid


logger = logging.getLogger(__name__)

class FlyerCRUD:
    def __init__(self):
        self.flyers_data_ref = flyers_data_ref

    async def create_flyer(self, user_id: str, flyer_data: FlyerModel) -> Dict:
        """Create a new flyer record"""
        try:            
            flyer_doc = {
                **flyer_data.model_dump(),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
    
            # Save to Firestore
            self.flyers_data_ref.document(user_id).collection("flyers").document(flyer_data.flyer_id).set(flyer_doc)
            
            return True

        except Exception as e:
            logger.error(f"Error creating flyer: {str(e)}")
            raise

    async def get_flyer(self, user_id: str, flyer_id: str) -> Optional[Dict]:
        """Get a flyer by ID"""
        try:
            flyer_doc = self.flyers_data_ref.document(user_id).collection("flyers").document(flyer_id).get()
            
            if not flyer_doc.exists:
                return None
                
            return {**flyer_doc.to_dict(), "flyer_id": flyer_id}

        except Exception as e:
            logger.error(f"Error getting flyer: {str(e)}")
            raise

    async def update_flyer(self, user_id: str, flyer_data: dict, conversation_history: List = None) -> Optional[Dict]:
        """Update a flyer's content"""
        try:
            flyer_id = flyer_data.get('flyer_id')
            if not flyer_id:
                raise ValueError("flyer_id is required")

            flyer_doc = self.flyers_data_ref.document(user_id).collection("flyers").document(flyer_id).get()
            
            if not flyer_doc.exists:
                return None

            update_data = {
                **flyer_data,
                "updated_at": datetime.utcnow().isoformat()
            }

            if conversation_history:
                update_data['conversation_history'] = conversation_history

            self.flyers_data_ref.document(user_id).collection("flyers").document(flyer_id).update(update_data)
            
            return await self.get_flyer(user_id, flyer_id)

        except Exception as e:
            logger.error(f"Error updating flyer: {str(e)}")
            raise

    async def delete_flyer(self, user_id: str, flyer_id: str) -> bool:
        """Delete a flyer"""
        try:
            flyer_doc = self.flyers_data_ref.document(user_id).collection("flyers").document(flyer_id).get()
            
            if not flyer_doc.exists:
                return False

            self.flyers_data_ref.document(user_id).collection("flyers").document(flyer_id).delete()
            self.flyers_data_ref.document(user_id).collection("deleted_flyers").document(flyer_id).set(flyer_doc.to_dict())
            return True

        except Exception as e:
            logger.error(f"Error deleting flyer: {str(e)}")
            raise

    async def get_user_flyers(self, user_id: str) -> list:
        """Get all flyers for a user"""
        try:
            flyers = self.flyers_data_ref.document(user_id).collection("flyers").get()
            print(f"this is the flyers: {flyers}")
            
            return [{**flyer.to_dict(), "flyer_id": flyer.id} for flyer in flyers]

        except Exception as e:
            logger.error(f"Error getting user flyers: {str(e)}")
            raise

flyer_crud = FlyerCRUD()