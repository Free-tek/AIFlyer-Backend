from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum

class FlyerType(Enum):
    GENERAL = "general"
    THUMBNAIL = "thumbnail"
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

class ThumbnailSizes(Enum):
    YOUTUBE = "1280x720"
    TIKTOK = "1080x1920"

class ThumbnailType(Enum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"


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
    layout_name: str 

class ThumbnailDesignQuery(BaseModel):
    main_text: str
    highlight_text: str
    emojis: List[str]
    corner_emoji: str
    text_position: str
    thumbnail_type: ThumbnailType
    
    class Config:
        use_enum_values = True

class FlyerDesignFile(BaseModel):
    sizes: FlyerSizes
    html_content_url: str
    image_url: str

    class Config:
        use_enum_values = True

class FlyerModel(BaseModel):
    flyer_id: str
    flyer_type: FlyerType
    flyer_design_query: Optional[FlyerDesignQuery] = None
    thumbnail_design_query: Optional[ThumbnailDesignQuery] = None
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


class DeviceInfo(BaseModel):
    userAgent: str
    language: str
    platform: str
    screenResolution: str
    timezone: str

class FlyerCreate(BaseModel):
    flyer_description: Optional[str] = None
    flyer_type: FlyerType
    image_url: Optional[str] = None
    application_id: Optional[str] = None
    thumbnail_type: Optional[ThumbnailType] = None
    device_info: Optional[DeviceInfo] = None


class FlyerUpdate(BaseModel):
    feedback: Optional[str] = None
    image_url: Optional[str] = None
    flyer_id: str
    device_info: Optional[DeviceInfo] = None


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

