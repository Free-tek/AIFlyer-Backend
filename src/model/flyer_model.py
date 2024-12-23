from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum

class FlyerType(Enum):
    GENERAL = "general"
    TIKTOK = "tiktok"
    GIF = "gif"

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"

class FlyerSizes(Enum):
    INSTAGRAM = "1080x1080"
    TWITTER = "1600x900"
    FACEBOOK = "1200x630"
    LINKEDIN = "1200x628"
    TIKTOK = "1080x1920"
    PINTEREST = "1000x1500"
    YOUTUBE = "1280x720"

class FlyerConversation(BaseModel):
    role: Role
    message: str
    message_id: str

    class Config:
        use_enum_values = True

class FlyerDesignQuery(BaseModel):
    marketing_idea: str
    designer_guidelines: str
    image_flyer_content: str

class FlyerDesignFile(BaseModel):
    sizes: FlyerSizes
    html_content_url: str
    image_url: str

    class Config:
        use_enum_values = True

class FlyerModel(BaseModel):
    flyer_id: str
    flyer_type: FlyerType
    flyer_design_query: FlyerDesignQuery
    design_image_options: List[str]
    current_design_image: Optional[str] = None
    html_content: str
    image_url: Optional[str] = None
    application_id: str
    flyer_name: str
    conversation_history: List[FlyerConversation]
    designs: Optional[List[FlyerDesignFile]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        use_enum_values = True


class FlyerCreate(BaseModel):
    flyer_description: Optional[str] = None
    flyer_type: FlyerType
    image_url: Optional[str] = None
    application_id: str


class FlyerUpdate(BaseModel):
    feedback: Optional[str] = None
    image_url: Optional[str] = None
    flyer_id: str

class FlyerDownload(BaseModel):
    url: str
    flyer_id: str

class FlyerResponse(BaseModel):
    id: int
    business_name: str
    business_info: str
    flyer_type: str
    image_url: str
    html_content: str
    user_id: int

