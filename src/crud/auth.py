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
            if 'application' in data:
                applications = data.pop('applications')  # This will be a list
                
                # Ensure we have at least one application
                if not applications or not isinstance(applications, list):
                    raise ValueError("Invalid application data format")
                    
                application = applications[0]  # Take the first application from the list
                
                # Generate application_id for new applications
                if not application.get('application_id'):
                    application['application_id'] = str(uuid.uuid4())
                    
                # Update/Create specific application using application_id as key
                users_data_ref.document(user_id).set({
                    "applications": {
                        application['application_id']: application  # Use application_id as the key
                    },
                    "application_ids": firestore.ArrayUnion([application['application_id']])  # Add to ordered list
                }, merge=True)
                
                # Add application_id to response
                response["application_id"] = application['application_id']
                
            # Update other user details if any
            if data:
                users_data_ref.document(user_id).set(data, merge=True)
                
            return response
        except Exception as e:
            return {"error": f"Failed to update user details: {str(e)}"}
                    
    def get_user_details(user_id: str):
        try:
            user_doc = users_data_ref.document(user_id).get()
            if not user_doc.exists:
                return {"error": "User not found"}
            
            user_data = user_doc.to_dict()
            
            # Debug logging
            logger.info(f"Raw user_data: {user_data}")
            
            # Convert applications from map to list if it exists
            applications = user_data.get('applications', {})
            application_ids = user_data.get('application_ids', [])
            
            # Convert the applications map to a list using application_ids for order
            applications_list = []
            for app_id in application_ids:
                if app_id in applications:
                    app_data = applications[app_id]
                    # Ensure application_id is included in the data
                    app_data['application_id'] = app_id
                    applications_list.append(app_data)
            
            # Update the applications in user_data with the ordered list
            user_data['applications'] = applications_list
            
            return user_data
        except Exception as e:
            logger.error(f"Error in get_user_details: {str(e)}")
            return {"error": f"Failed to get user details: {str(e)}"}
