from src.core.error import InvalidToken
from src.core.config import settings
from src.database.db import users_data_ref
from src.model.auth_model import CreateAccountRequest, LoginRequest
from fastapi import Header
from typing import Optional
import requests
import json
from firebase_admin import auth
from datetime import datetime
from google.cloud import firestore
import uuid  
import logging

logger = logging.getLogger(__name__)

PREFIX = "Bearer"
REFRESH_TOKEN_BASE_URL = "https://securetoken.googleapis.com/v1/"
BASE_URL = "https://identitytoolkit.googleapis.com/v1/accounts"

class AuthCrud:

    def create_account(request: CreateAccountRequest):
        try:
            # Create user in Firebase Auth
            url = f"{BASE_URL}:signUp?key={settings.API_KEY}"
            headers = {"content-type": "application/json"}
            payload = {"email": request.email, "password": request.password, "returnSecureToken": True}

            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers,
            )
            response.raise_for_status()
            response_data = response.json()

            # Store user in Firestore without the raw password
            users_data_ref.document(response_data["localId"]).set({
                "email": request.email,
                "created_at": datetime.now(),
                "user_id": response_data["localId"]
            })

            return {
                "id": response_data["localId"],
                "token": response_data["idToken"]  # Return the token for immediate login
            }
        except requests.exceptions.HTTPError as e:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            return {"error": error_message.replace("_", " ").title()}
        except Exception as e:
            return {"error": "Failed to create account"}

    def login(request: LoginRequest):
        try:
            url = f"{BASE_URL}:signInWithPassword?key={settings.API_KEY}"
            headers = {"content-type": "application/json"}
            payload = {"email": request.email, "password": request.password, "returnSecureToken": True}

            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers,
            )   
            response.raise_for_status()
            response_data = response.json()
            
            return {
                "id": response_data["localId"],
                "token": response_data["idToken"],
                "refreshToken": response_data["refreshToken"]
            }
        except requests.exceptions.HTTPError as e:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            return {"error": error_message.replace("_", " ").title()}
        except Exception as e:
            return {"error": "Failed to login"}
    
    def parse_auth_token_from_header(header: str):
        if header is None:
            return InvalidToken
        if not header.startswith(PREFIX):
            return InvalidToken

        return header[len(PREFIX) :].lstrip()
    
    def verify_token(token: Optional[str] = Header(None)):
        parsed_token = AuthCrud.parse_auth_token_from_header(token)

        if parsed_token == InvalidToken:
            raise InvalidToken

        try:

            decoded_token = auth.verify_id_token(parsed_token)
            uid = decoded_token["uid"]
            return uid
        except:
            raise InvalidToken
        
    def update_user_details(user_id: str, data: dict):
        try:
            if not isinstance(user_id, str):
                raise ValueError("user_id must be a string")
            if not isinstance(data, dict):
                raise ValueError("data must be a dictionary")
            if not data:
                raise ValueError("No data provided for update")
            
            response = {"id": user_id, "message": "User details updated successfully"}
            
            # If there's an application in the data
            if 'applications' in data and data['applications'] != []:
                applications = data['applications']
                
                if not applications or not isinstance(applications, list):
                    raise ValueError("Invalid application data format")
                    
                application = applications[0]
                application_type = application.get('application_type', 'business')
                application_data = application.get('application_data', {})
                
                # Generate application_id for new applications
                application_id = str(uuid.uuid4())
                
                # Base application data structure with common fields
                base_application_data = {
                    "logo": application_data.get("logo"),
                    "primary_color": application_data.get("primary_color"),
                    "secondary_color": application_data.get("secondary_color"),
                    "twitter_handle": application_data.get("twitter_handle"),
                    "facebook_handle": application_data.get("facebook_handle"),
                    "instagram_handle": application_data.get("instagram_handle"),
                    "linkedin_handle": application_data.get("linkedin_handle"),
                    "tiktok_handle": application_data.get("tiktok_handle"),
                    "pinterest_handle": application_data.get("pinterest_handle"),
                    "youtube_handle": application_data.get("youtube_handle"),
                    "llm_memory": application_data.get("llm_memory")
                }

                # Add type-specific fields based on application_type
                if application_type == "business":
                    base_application_data.update({
                        "business_name": application_data.get("business_name"),
                        "business_description": application_data.get("business_description"),
                        "website_url": application_data.get("website_url")
                    })
                elif application_type == "event":
                    base_application_data.update({
                        "event_name": application_data.get("event_name"),
                        "event_description": application_data.get("event_description"),
                        "event_date": application_data.get("event_date"),
                        "event_location": application_data.get("event_location"),
                        "event_images": application_data.get("event_images", [])
                    })
                elif application_type == "other":
                    base_application_data.update({
                        "other_name": application_data.get("other_name"),
                        "other_description": application_data.get("other_description"),
                        "website_url": application_data.get("website_url")
                    })
                
                # Update/Create specific application
                users_data_ref.document(user_id).set({
                    "applications": {
                        application_id: {
                            "application_id": application_id,
                            "application_type": application_type,
                            "application_data": base_application_data,
                            "created_at": datetime.now().isoformat()
                        }
                    },
                    "application_ids": firestore.ArrayUnion([application_id])
                }, merge=True)
                
                response["application_id"] = application_id
                
            # Update other user details if any
            if data:
                other_data = {k: v for k, v in data.items() if k != 'applications'}
                if other_data:
                    users_data_ref.document(user_id).set(other_data, merge=True)
                
            return response
        except Exception as e:
            logger.error(f"Error in update_user_details: {str(e)}")
            return {"error": f"Failed to update user details: {str(e)}"}
                    
    def get_user_details(user_id: str):
        try:
            user_doc = users_data_ref.document(user_id).get()
            if not user_doc.exists:
                return {"error": "User not found"}
            
            user_data = user_doc.to_dict()
            
            # Process applications if they exist
            if 'applications' in user_data:
                applications_dict = user_data['applications']
                applications_list = []
                
                # Convert applications dict to list and ensure proper structure
                for app_id, app_data in applications_dict.items():
                    application = {
                        "application_id": app_id,
                        "application_type": app_data.get("application_type", "business"),
                        "application_data": app_data.get("application_data", {}),
                        "created_at": app_data.get("created_at")
                    }
                    applications_list.append(application)
                
                # Sort applications by creation date if available
                applications_list.sort(
                    key=lambda x: x.get("created_at", ""),
                    reverse=True
                )
                
                user_data['applications'] = applications_list
            
            return user_data
        except Exception as e:
            logger.error(f"Error in get_user_details: {str(e)}")
            return {"error": f"Failed to get user details: {str(e)}"}