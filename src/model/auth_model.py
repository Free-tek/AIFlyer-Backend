from enum import Enum
from pydantic import BaseModel
from typing import Optional, Any, Dict, List, Union
from src.model.flyer_model import DeviceInfo

class CreateAccountRequest(BaseModel):
    email: str
    password: str
    guest_id: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str


class AccountType(Enum):
    Business = "business"
    Event = "event"
    Other = "other"

class PlanTier(Enum):
    Starter = "starter"
    Pro = "pro"
    Premium = "premium"


class BusinessApplication(BaseModel):
    business_name: str
    business_description: Optional[str] = None
    website_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    logo: Optional[str] = None
    twitter_handle: Optional[str] = None
    instagram_handle: Optional[str] = None
    facebook_handle: Optional[str] = None
    linkedin_handle: Optional[str] = None
    tiktok_handle: Optional[str] = None
    pinterest_handle: Optional[str] = None
    youtube_handle: Optional[str] = None
    application_id: Optional[str] = None
    llm_memory: Optional[str] = None

    class Config:
        use_enum_values = True

class EventApplication(BaseModel):
    event_name: str
    event_description: Optional[str] = None
    event_date: Optional[str] = None
    event_location: Optional[str] = None
    event_images: Optional[List[str]] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    logo: Optional[str] = None
    twitter_handle: Optional[str] = None
    instagram_handle: Optional[str] = None
    facebook_handle: Optional[str] = None
    linkedin_handle: Optional[str] = None
    tiktok_handle: Optional[str] = None
    pinterest_handle: Optional[str] = None
    youtube_handle: Optional[str] = None
    application_id: Optional[str] = None
    llm_memory: Optional[str] = None

    class Config:
        use_enum_values = True

class OtherApplication(BaseModel):
    other_name: str
    other_description: Optional[str] = None
    application_id: Optional[str] = None
    website_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    logo: Optional[str] = None
    twitter_handle: Optional[str] = None
    instagram_handle: Optional[str] = None
    facebook_handle: Optional[str] = None
    linkedin_handle: Optional[str] = None
    tiktok_handle: Optional[str] = None
    pinterest_handle: Optional[str] = None
    youtube_handle: Optional[str] = None
    llm_memory: Optional[str] = None

    class Config:
        use_enum_values = True


class Application(BaseModel):
    application_id: Optional[str] = None
    application_type: AccountType
    application_data: Union[BusinessApplication, EventApplication, OtherApplication]

    class Config:
        use_enum_values = True

class UpdateUserDetailsRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    applications: Optional[List[Application]] = None
    plan_tier: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    device_info: Optional[DeviceInfo] = None

    class Config:
        use_enum_values = True