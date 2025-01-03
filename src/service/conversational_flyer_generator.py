import os
import requests
import urllib.parse
import re
import uuid
from datetime import datetime
from src.core.model_manager import get_claude_client
from src.model.flyer_model import FlyerCreate, FlyerModel, FlyerConversation, Role, FlyerDesignQuery, FlyerDesignFile, FlyerType, ThumbnailDesignQuery, ThumbnailType
from src.crud.flyer_generation import flyer_crud
from src.utils.prompts import generate_marketing_content_prompt, generate_image_query_prompt, generate_initial_design_prompt, generate_refine_design_prompt, classify_intent_prompt, reformat_design_size_prompt, layout_options, generate_vector_image_query_prompt, generate_thumbnail_caption_prompt, generate_thumbnail_design_prompt, generate_thumbnail_image_query_prompt, thumbnail_layout_options
from src.crud.auth import AuthCrud
from src.crud.billing import BillingCrud
from firebase_admin import storage, firestore
from playwright.async_api import async_playwright
from fastapi import HTTPException
from src.utils.llm_utils import extract_html
from typing import List
import random
import logging
from src.core.config import settings
from pydantic import ValidationError
import asyncio
from functools import wraps
from src.utils import constants
import base64
import json
from src.service.guest_user_service import GuestUserService

logger = logging.getLogger(__name__)

def async_retry(retries=3, delay=1):
    """
    Decorator for async functions to retry on failure
    
    Args:
        retries (int): Number of retries
        delay (int): Delay between retries in seconds
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < retries - 1:  # Don't sleep on the last attempt
                        logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay} seconds...")
                        await asyncio.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

def add_watermark_to_html(html_content: str) -> str:
    """
    Add a diagonal watermark overlay to the HTML design for guest users
    """
    watermark_css = """
    <style>
    .watermark-overlay {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        pointer-events: none !important;
        z-index: 1000 !important;
        background: repeating-linear-gradient(
            -45deg,
            rgba(255, 255, 255, 0.15),
            rgba(255, 255, 255, 0.15) 20px,
            rgba(255, 255, 255, 0.25) 20px,
            rgba(255, 255, 255, 0.25) 40px
        ) !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        overflow: hidden !important;
    }

    .watermark-repeat {
        position: absolute !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-around !important;
        height: 300% !important;
        width: 300% !important;
        transform: rotate(-45deg) !important;
    }

    .watermark-row {
        display: flex !important;
        justify-content: space-around !important;
        width: 100% !important;
        opacity: 0.15 !important;
    }

    .watermark-item {
        font-family: Arial, sans-serif !important;
        font-size: 24px !important;
        font-weight: bold !important;
        color: #000 !important;
        padding: 20px !important;
        white-space: nowrap !important;
    }
    </style>
    """

    watermark_html = """
    <div class="watermark-overlay">
        <div class="watermark-repeat">
            <div class="watermark-row">
                <span class="watermark-item">AIFlyer</span>
                <span class="watermark-item">AIFlyer</span>
                <span class="watermark-item">AIFlyer</span>
            </div>
            <div class="watermark-row">
                <span class="watermark-item">AIFlyer</span>
                <span class="watermark-item">AIFlyer</span>
                <span class="watermark-item">AIFlyer</span>
            </div>
            <div class="watermark-row">
                <span class="watermark-item">AIFlyer</span>
                <span class="watermark-item">AIFlyer</span>
                <span class="watermark-item">AIFlyer</span>
            </div>
        </div>
    </div>
    """

    # Add CSS to head without modifying container
    if "</head>" in html_content:
        html_content = html_content.replace("</head>", f"{watermark_css}</head>")
    else:
        html_content = f"<head>{watermark_css}</head>{html_content}"

    # Find the first div in the body and add watermark as its first child
    body_start = html_content.find("<body")
    if body_start != -1:
        body_content_start = html_content.find(">", body_start) + 1
        html_content = (
            html_content[:body_content_start] +
            watermark_html +
            html_content[body_content_start:]
        )
    else:
        # If no body tag, insert after first div
        first_div = html_content.find("<div")
        if first_div != -1:
            div_content_start = html_content.find(">", first_div) + 1
            html_content = (
                html_content[:div_content_start] +
                watermark_html +
                html_content[div_content_start:]
            )
        else:
            # If no div found, prepend to content
            html_content = watermark_html + html_content

    return html_content

class ConversationalFlyerGenerator:
    def __init__(self):
        self.client = get_claude_client()

    @async_retry(retries=3, delay=1)
    async def _get_ai_response(self, system_prompt, messages, max_tokens=4000):
        """Helper method to get AI response with retries"""
        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages
        )
        if not response or not response.content:
            print(f"this is response: {response}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get a response from the AI model"
            )
        return response

    async def generate_flyer(self, flyer_in: FlyerCreate, user_id: str):
        """
        Generate a flyer
        """
        is_guest = False
        if user_id.startswith('guest_'):
            is_guest = True
            guest_service = GuestUserService()
            await guest_service.check_design_limit(user_id)
            business_details = """This is a guest user trying to use the flyer generator feature, 
            for their business details listen to as much as they tell you about their business from the prompt"""
            flyer_design_query = []
            flyer_in.application_id = "guest_user"

        else:
            business_details = None
            user_details = AuthCrud.get_user_details(user_id)

            for application in user_details['applications']:
                if application['application_id'] == flyer_in.application_id:
                    business_details = application['application_data']
                    break

            flyers = await flyer_crud.get_user_flyers(user_id)
            flyer_design_query = [flyer['flyer_design_query']['image_flyer_content'] for flyer in flyers if flyer != None and flyer['flyer_type'] == flyer_in.flyer_type]

        print("this is the detail 0000")
        if flyer_in.flyer_type == FlyerType.THUMBNAIL:
            new_flyer_design_query = None
            
            thumbnail_design_query = await self.generate_thumbnail_caption(flyer_in.flyer_description, flyer_in.thumbnail_type)
            print(f"The flyer description is: {thumbnail_design_query}")
            flyer_name=thumbnail_design_query.main_text[:20] + "..."

            if not flyer_in.image_url:
                search_query = await self.generate_thumbnail_image_query(flyer_in.flyer_description)
                images = self.get_image(search_query)
                image_url = images[0] if images else None
            else:
                images = [flyer_in.image_url]
                image_url = flyer_in.image_url

            if flyer_in.thumbnail_type == ThumbnailType.TIKTOK:
                layout_option = random.choice(["tiktok_thumbnail_layout_1", "tiktok_thumbnail_layout_2"])
            else:
                layout_option = "youtube_thumbnail_layout_1"

            html_content = await self.generate_thumbnail_design(flyer_in.flyer_description, image_url, layout_option)
            print(html_content)

            conversation_history = [FlyerConversation(role=Role.USER, message=flyer_in.flyer_description, message_id=str(int(datetime.now().timestamp())))]
            conversation_history.append(FlyerConversation(role=Role.ASSISTANT, message=f"Done creating this thumbnail for you, will you like to make any changes?", message_id=str(int(datetime.now().timestamp()))))


        elif flyer_in.flyer_type == FlyerType.GENERAL:
            thumbnail_design_query = None
            print("this is the detail 1111")
            if flyer_in.flyer_description:
                print("this is the detail 2222")
                #generate flyer design image search query
                if not flyer_in.image_url:
                    search_query = await self.generate_image_query(flyer_in.flyer_description)

                current_context = str(business_details) + "USERS DESCRIPTION OF THE FLYER THEY WANT:" + str(flyer_in.flyer_description)
                print(f"this is current context: {current_context}")
                new_flyer_design_query = await self.generate_marketing_content(str(current_context), flyer_design_query)
                print(f"this is new flyer design query: {new_flyer_design_query}")
                
                conversation_history = [FlyerConversation(role=Role.USER, message=flyer_in.flyer_description, message_id=str(int(datetime.now().timestamp())))]
                conversation_history.append(FlyerConversation(role=Role.ASSISTANT, message=f"Done creating this flyer for you, will you like to make any changes?", message_id=str(int(datetime.now().timestamp()))))
            else:
                print("this is the detail 3333")
                new_flyer_design_query = await self.generate_marketing_content(str(business_details), flyer_design_query)

                if new_flyer_design_query == None:
                    raise HTTPException(status_code=400, detail="Failed to generate an automatic flyer, please tell me what you'll like to design.")

                conversation_history = [FlyerConversation(role=Role.ASSISTANT, message=f"I came up with a flyer concept for you, it is centered around {new_flyer_design_query.marketing_idea}", message_id=str(int(datetime.now().timestamp())))]

                #generate flyer design image search query
                if not flyer_in.image_url:
                    search_query = await self.generate_image_query(new_flyer_design_query.designer_guidelines)

            #generate vector image search query
            if new_flyer_design_query.layout_name == "vector_images_design":
                search_query = await self.generate_vector_query(new_flyer_design_query.designer_guidelines)
                vector_images = self.get_vector_images(search_query)
            else:
                vector_images = None

            if not flyer_in.image_url:
                #get image to include in flyer
                images = self.get_image(search_query)
                image_url = images[0] if images else None
            else:
                images = [flyer_in.image_url]
                image_url = flyer_in.image_url

            if len(images) > 1:
                other_images = images[1:]
            else:
                other_images = []

            # Generate initial design
            print(f"The flyer description is: {new_flyer_design_query}")
            task_description = f"Business details: {business_details}, Flyer description: {str(new_flyer_design_query)}"
            html_content = await self.generate_initial_design(task_description, image_url, other_images, new_flyer_design_query, vector_images)
            flyer_name=new_flyer_design_query.marketing_idea[:20] + "..."
            

        print(f"this is the detail 4444 :: {flyer_in.flyer_type} :: {flyer_in} :: {flyer_in.flyer_type == FlyerType.GENERAL} :: {FlyerType.GENERAL}")
        timestamp = int(datetime.now().timestamp())
        
        if is_guest:
            html_content = add_watermark_to_html(html_content)

        try:
            # Create flyer record
            flyer_model = FlyerModel(
                flyer_id=str(timestamp),
                flyer_type=flyer_in.flyer_type,
                flyer_design_query=new_flyer_design_query,
                thumbnail_design_query=thumbnail_design_query,
                design_image_options=images,
                current_design_image=image_url,
                html_content=html_content,
                image_url=None,
                application_id=flyer_in.application_id,
                flyer_name=flyer_name,
                user_id=user_id,
                conversation_history=conversation_history,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
        except Exception as e:
            print(f"this is error parsing FlyerModel: {e}")
            raise HTTPException(status_code=400, detail="Failed to generate the design, please try again.")

        print(f"The html content is: {html_content}")
            
        await flyer_crud.create_flyer(user_id, flyer_model)
        return flyer_model

    async def generate_marketing_content(self, business_info, previous_ideas):
        """
        Generate marketing content ideas
        """
        prompt = generate_marketing_content_prompt(business_info, previous_ideas)

        # Create the message and await the response
        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=350,
            messages=[{"role": "user", "content": prompt}]
        )

        # Get the content from the response
        content_idea = response.content[0].text.strip().lower()
        content_idea = content_idea.replace("\n", "").replace(" \"", "\"").replace("{ \"", "{\"")

        match = re.search(r'{\s*"marketing_idea":\s*"(.*?)",\s*"designer_guidelines":\s*"(.*?)",\s*"image_flyer_content":\s*"(.*?)",\s*"layout_name":\s*"(.*?)"\s*}', content_idea)
        if match:
            marketing_idea = match.group(1)
            designer_guidelines = match.group(2)
            image_flyer_content = match.group(3)
            layout_name = match.group(4)
            return FlyerDesignQuery(
                marketing_idea=marketing_idea,
                designer_guidelines=designer_guidelines,
                image_flyer_content=image_flyer_content,
                layout_name=layout_name
            )
        else:
            return None
        

    async def generate_thumbnail_caption(self, flyer_description, thumbnail_type):
        """Generate marketing content ideas"""
        prompt = generate_thumbnail_caption_prompt(flyer_description)

        # Create the message and await the response
        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=350,
            messages=[{"role": "user", "content": prompt}]
        )

        # Get the content from the response
        print(f"this is response: {response}")
        print(f"this is prompt: {prompt}")
        
        try:
            # Extract the JSON string from the response
            content = response.content[0].text.strip()
            # Find the JSON object between curly braces
            json_match = re.search(r'{\s*".*?}', content, re.DOTALL)
            if not json_match:
                return None
            
            json_str = json_match.group(0)
            # Parse the JSON string
            data = json.loads(json_str)
            
            # Keep emojis as a list (don't join them)
            return ThumbnailDesignQuery(
                main_text=data['main_text'],
                highlight_text=data['highlight_text'],
                emojis=data['emojis'],  # Keep as list
                corner_emoji=data['corner_emoji'],
                text_position=data['text_position'],
                thumbnail_type=thumbnail_type
            )
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing thumbnail caption response: {e}")
            return None
        
    
    async def generate_thumbnail_design(self, video_details, image_url, layout_option):
        """Generate the thumbnail design"""

        if layout_option == "tiktok_thumbnail_layout_1":
            sample_image_url = "https://firebasestorage.googleapis.com/v0/b/flyerai.firebasestorage.app/o/sandbox%20files%2FScreenshot%202024-12-26%20at%205.21.16%E2%80%AFPM.png?alt=media&token=826e745e-d159-4b59-b426-261df68c143e"
            sample_image_type = "image/png"
        elif layout_option == "tiktok_thumbnail_layout_2":
            sample_image_url = "https://firebasestorage.googleapis.com/v0/b/flyerai.firebasestorage.app/o/sandbox%20files%2FWhatsApp%20Image%202024-12-28%20at%201.22.49%20AM%20(1).jpeg?alt=media&token=77d5cd46-8822-4777-8be2-824ff4b04a42"
            sample_image_type = "image/jpeg"
        elif layout_option == "youtube_thumbnail_layout_1":
            sample_image_url = "https://firebasestorage.googleapis.com/v0/b/flyerai.firebasestorage.app/o/sandbox%20files%2FBlock-Heading-Falling-Cash-Template-youtube-thumbnail.jpg?alt=media&token=eeb12e55-77b7-48bf-8629-3b2541c2dd55"
            sample_image_type = "image/jpeg"
        elif layout_option == "youtube_thumbnail_layout_2":
            sample_image_url = "https://firebasestorage.googleapis.com/v0/b/flyerai.firebasestorage.app/o/sandbox%20files%2FBlock-Heading-Falling-Cash-Template-youtube-thumbnail.jpg?alt=media&token=eeb12e55-77b7-48bf-8629-3b2541c2dd55"
            sample_image_type = "image/jpeg"

        # Download the image and convert to base64
        image_response = requests.get(sample_image_url)
        image_response.raise_for_status()
        image_data = base64.b64encode(image_response.content).decode('utf-8')

        print(f"this is layout_option {layout_option}")


        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": generate_thumbnail_design_prompt(video_details, image_url, thumbnail_layout_options[layout_option])
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": sample_image_type,
                            "data": image_data
                        }
                    }
                ]
            }
        ]
        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            messages=messages
        )

        print(f"this is model response: {response}")

        current_design = response.content[0].text.strip()
        current_design_html = extract_html(current_design)
        return current_design_html




    async def generate_image_query(self, flyer_description):
        """
        Generate a concise image search query from flyer description

        Args:
            flyer_description (str): User's description of desired flyer

        Returns:
            str: 2-3 word search query
        """
        prompt = generate_image_query_prompt(flyer_description)

        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )

        # Clean and return the search query
        search_query =  response.content[0].text.strip().lower()
        return search_query
    

    async def generate_thumbnail_image_query(self, video_description):
        """
        Generate a concise image search query from video description

        Args:
            video_description (str): User's description of desired video

        Returns:
            str: 2-3 word search query
        """
        prompt = generate_thumbnail_image_query_prompt(video_description)

        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )

        # Clean and return the search query
        search_query =  response.content[0].text.strip().lower()
        return search_query
    
    async def generate_vector_query(self, flyer_description):
        """
        Generate a concise vectorimage search query from flyer description

        Args:
            flyer_description (str): User's description of desired flyer

        Returns:
            str: 1-2 word search query
        """
        prompt = generate_vector_image_query_prompt(flyer_description)

        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )

        # Clean and return the search query
        search_query =  response.content[0].text.strip().lower()
        return search_query

    def get_image(self, query: str) -> str:
        query = urllib.parse.quote(query.replace(" ", "+"))
        url = f"https://www.shopify.com/stock-photos/photos/search?q={query}&button="

        headers = {
            'Host': 'www.shopify.com',
            'Sec-Ch-Ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www.shopify.com/stock-photos',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cookie': '_shopify_s=605ccfa5-22c2-468d-8501-4ccce8b48bed; _shopify_y=6df19cb0-19fa-41ba-9fbe-adeb499fbe7d; master_device_id=5467b457-046e-45eb-9f0a-5b18823d88bc'
        }

        response = requests.get(url, headers=headers)
        pattern = r'<img sizes="100vw" data-srcset="(.*?)&amp;format=pjpg&amp;exif=0&amp;'
        matches = re.findall(pattern, response.text)
        return [item.replace("373", "800") for item in matches]


    def get_vector_images(self, query):
        """ Get vector images for design from the query and using freepik API"""
        
        url = constants.FREEPIK_API_URL

        querystring = {"term":query,"page":"1","per_page":"10"}
        headers = {"x-freepik-api-key": settings.FREEPIK_API_KEY}

        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            data = data["data"]
            result = []
            for icon in data:
                ic = icon["thumbnails"][0]["url"].replace("/128/", "/512/")
                result.append(ic)

            return result
        else:
            print(f"Request failed with status code {response.status_code}")
            return []



    async def generate_initial_design(self, business_details, image_url, other_images, new_flyer_design_query, vector_images = None):
        """Generate the initial flyer design"""
        print(business_details)
        print(image_url)
        print(new_flyer_design_query)
        print(vector_images)
        
        if new_flyer_design_query.layout_name == "vector_images_design":
            #TODO: Add permantely available image urls
            sample_image_url = "https://firebasestorage.googleapis.com/v0/b/flyerai.firebasestorage.app/o/sample_designs%2FGUiPy5eXkAAi3L7.jpeg?alt=media&token=62cc6c34-7d7c-488b-aa0f-bd16776fdb7b"
            sample_image_type = "image/jpeg"
        elif new_flyer_design_query.layout_name == "card_layout":
            sample_image_url = "https://firebasestorage.googleapis.com/v0/b/flyerai.firebasestorage.app/o/sample_designs%2FScreenshot%202024-12-27%20at%201.35.00%E2%80%AFPM.png?alt=media&token=ea2fcf87-b98d-49f1-896c-70ed278f3163"
            sample_image_type = "image/png"
        elif new_flyer_design_query.layout_name == "pattern_background":
            sample_image_url = "https://firebasestorage.googleapis.com/v0/b/flyerai.firebasestorage.app/o/sample_designs%2FScreenshot%202024-12-27%20at%201.40.34%E2%80%AFPM.png?alt=media&token=230f017c-88f7-40a2-9968-2c8df1cecb47"
            sample_image_type = "image/png"
        elif new_flyer_design_query.layout_name == "split_layout":
            sample_image_url = "https://firebasestorage.googleapis.com/v0/b/flyerai.firebasestorage.app/o/sample_designs%2FScreenshot%202024-12-27%20at%201.41.49%E2%80%AFPM.png?alt=media&token=060d41f0-8d4e-443c-9d70-17a1d9567685"
            sample_image_type = "image/png"
        elif new_flyer_design_query.layout_name == "full_background_image":
            sample_image_url = "https://firebasestorage.googleapis.com/v0/b/flyerai.firebasestorage.app/o/sample_designs%2FScreenshot%202024-12-28%20at%202.19.19%E2%80%AFPM.png?alt=media&token=7ece225a-d3f7-40d8-8f81-4f31e99a345e"
            sample_image_type = "image/png"

        # Download the image and convert to base64
        image_response = requests.get(sample_image_url)
        image_response.raise_for_status()
        image_data = base64.b64encode(image_response.content).decode('utf-8')
        
        # Create message with image
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": generate_initial_design_prompt(business_details, image_url, other_images, layout_options[new_flyer_design_query.layout_name], vector_images)
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": sample_image_type,
                            "data": image_data
                        }
                    }
                ]
            }
        ]
        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            messages=messages
        )

        print(f"this is model response: {response}")

        current_design = response.content[0].text.strip()
        current_design_html = extract_html(current_design)

        # Add watermark for guest users
        if business_details.startswith('guest_'):
            current_design_html = add_watermark_to_html(current_design_html)

        return current_design_html
            
        
    async def refine_design(self, user_input, user_id, flyer_id):
        try:
            """Refine the design based on user feedback"""
            refinement_prompt = generate_refine_design_prompt(user_input)

            # Get previous flyer from firestore
            flyer_data = await flyer_crud.get_flyer(user_id, flyer_id)
            if not flyer_data:
                raise HTTPException(
                    status_code=404,
                    detail="I couldn't find the flyer you're referring to, will you like me to generate a new flyer for you?"
                )

            # Format messages with system prompt
            system_prompt = "You are a professional designer. You will be given the current HTML design and user feedback. Modify the HTML design according to the user's feedback while maintaining the remaining structure and style."
            
            messages = [
                {
                    "role": "user",
                    "content": f"""Current Design:
                    {flyer_data.get('html_content')}

                    User Feedback:
                    {refinement_prompt}

                    Please update the HTML design according to the feedback while maintaining the overall structure and style."""
                }
            ]

            # Add only the last 3 conversations from history if they exist
            existing_history = flyer_data.get('conversation_history', [])
            if existing_history:
                recent_history = existing_history[-3:] if len(existing_history) > 3 else existing_history
                for conv in recent_history:
                    messages.append({
                        "role": conv['role'].lower(),
                        "content": conv['message']
                    })


            # Get AI response with retries
            print(f"this is refine prompt: {messages}")
            response = await self._get_ai_response(system_prompt, messages)

            # Create new conversation entries
            new_conversations = [
                {
                    "role": "user",
                    "message": user_input,
                    "message_id": str(int(datetime.now().timestamp()))
                },
                {
                    "role": "assistant",
                    "message": "I am done making changes to the design, here is the new design, will you like to make any more changes?",
                    "message_id": str(int(datetime.now().timestamp()))
                }
            ]

            # Update conversation history
            updated_history = existing_history + new_conversations
            
            # Extract HTML and update flyer data
            html_content = extract_html(response.content[0].text if response.content else "")
            if not html_content:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to extract HTML content from the response"
                )
            
            # Add watermark for guest users
            if user_id.startswith('guest_'):
                html_content = add_watermark_to_html(html_content)

            # Prepare update data
            updated_flyer_data = {
                **flyer_data,
                "html_content": html_content,
            }

            # Update in database using the existing API
            result = await flyer_crud.update_flyer(
                user_id=user_id,
                flyer_data=updated_flyer_data,
                conversation_history=updated_history
            )

            if not result:
                raise HTTPException(status_code=404, detail="Failed to update flyer")

            return result

        except Exception as e:
            logger.error(f"Error in refine_design: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


    async def update_design_image(self, user_id, flyer_id, image_url, user_input):
        """Update the design image"""
        try:
            # Get previous flyer from firestore
            flyer_data = await flyer_crud.get_flyer(user_id, flyer_id)
            if not flyer_data:
                raise HTTPException(
                    status_code=404,
                    detail="I couldn't find the flyer you're referring to, will you like me to generate a new flyer for you?"
                )

            design_image_options = flyer_data.get('design_image_options', [])
            current_design_image = flyer_data.get('current_design_image')
            html_content = flyer_data.get('html_content')

            # Handle image selection
            if not image_url:
                if current_design_image in design_image_options:
                    design_image_options.remove(current_design_image)
                if not design_image_options:
                    raise HTTPException(status_code=400, detail="No alternative images available")
                image_url = random.choice(design_image_options)
            else:
                if image_url in design_image_options:
                    design_image_options.remove(image_url)
                design_image_options.append(current_design_image)

            # Update HTML content with new image
            if current_design_image and html_content:
                html_content = html_content.replace(current_design_image, image_url)

            # Create new conversation entries
            new_conversations = [
                {
                    "role": "user",
                    "message": user_input,
                    "message_id": str(int(datetime.now().timestamp()))
                },
                {
                    "role": "assistant",
                    "message": "Done updating the image, here is the new design",
                    "message_id": str(int(datetime.now().timestamp()))
                }
            ]

            # Update conversation history
            existing_history = flyer_data.get('conversation_history', [])
            updated_history = existing_history + new_conversations

            if user_id.startswith("guest_"):
                html_content = add_watermark_to_html(html_content)

            # Prepare update data
            updated_flyer_data = {
                **flyer_data,
                "html_content": html_content,
                "current_design_image": image_url,
                "design_image_options": design_image_options,
                "updated_at": datetime.now().isoformat()
            }

            # Update in database using the existing API
            result = await flyer_crud.update_flyer(
                user_id=user_id,
                flyer_data=updated_flyer_data,
                conversation_history=updated_history
            )

            if not result:
                raise HTTPException(status_code=404, detail="Failed to update flyer")

            return result

        except Exception as e:
            logger.error(f"Error in update_design_image: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    

            
    async def classify_intent(self, user_input):
        """Use Claude to classify user intent"""
        intent_prompt = classify_intent_prompt(user_input)

        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=100,
            messages=[{"role": "user", "content": intent_prompt}]
        )

        return response.content[0].text.strip()

    async def process_command(self, flyer_update, user_id):
        """Process user input using AI intent classification"""
        try:
            user_input = flyer_update.feedback
            flyer_id = flyer_update.flyer_id
            image_url = flyer_update.image_url

            intent = await self.classify_intent(user_input)
            print(f"Classified intent: {intent}")

            response_data = {}

            if "CREATE_MARKETING_IDEA" in intent:

                flyer_data = await flyer_crud.get_flyer(user_id, flyer_id)
                flyer_in = FlyerCreate(
                    flyer_description=user_input,
                    application_id=flyer_data["application_id"],
                    flyer_type=flyer_data["flyer_type"],
                    image_url=flyer_data["image_url"]
                )

                flyer = await self.generate_flyer(flyer_in, user_id)
                response_data = {
                    "flyer": flyer.model_dump() if hasattr(flyer, 'model_dump') else flyer,
                    "message": "I have generated a new marketing idea for you"
                }

            elif "REFINE_DESIGN" in intent:
                flyer = await self.refine_design(user_input, user_id, flyer_id)
                response_data = {
                    "flyer": flyer.model_dump() if hasattr(flyer, 'model_dump') else flyer,
                    "message": "I have made the changes to the design based on your feedback"
                }

            elif "UPDATE_DESIGN_IMAGE" in intent:
                flyer = await self.update_design_image(user_id, flyer_id, image_url, user_input)
                response_data = {
                    "flyer": flyer.model_dump() if hasattr(flyer, 'model_dump') else flyer,
                    "message": "I have updated the design image based on your feedback"
                }

            # TODO: Add vector image to design

            elif "EXIT" in intent:
                response_data = {
                    "message": "Glad to know you liked my work, see you next time!",
                    "flyer": None
                }

            else:
                response_data = {
                    "message": """Sorry, I didn't understand your request, I can help you with any of these:
                    - Creating a new flyer: Just tell me what you want to design
                    - Making changes to the design: Describe what you want to change
                    - Updating the design image: Tell me if you want to change the image
                    - Ending the session: Just say exit
                    Please let me know what you'd like to do!""",
                    "flyer": None
                }

            return response_data

        except Exception as e:
            logger.error(f"Error in process_command: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


    async def export_flyer(self, user_id, flyer_id):
        """Export the flyer to a file"""
        try:
            # Get flyer data
            flyer_data = await flyer_crud.get_flyer(user_id, flyer_id)
            if not flyer_data:
                raise HTTPException(
                    status_code=404,
                    detail="I couldn't find the flyer you're referring to, will you like me to generate a new flyer for you?"
                )

            # Convert designs to proper format if they exist
            if 'designs' in flyer_data and flyer_data['designs']:
                designs = []
                for design in flyer_data['designs']:
                    if isinstance(design, dict) and 'size' in design:
                        # Convert 'size' to 'sizes' to match our model
                        design['sizes'] = design.pop('size')
                    designs.append(design)
                flyer_data['designs'] = designs

            # Convert conversation history roles to lowercase
            if 'conversation_history' in flyer_data and flyer_data['conversation_history']:
                for conv in flyer_data['conversation_history']:
                    conv['role'] = conv['role'].lower()

            # Convert to FlyerModel
            flyer_data = FlyerModel(**flyer_data)

            # Get user's plan type to determine flyer sizes
            user_details = AuthCrud.get_user_details(user_id)
            stripe_customers = user_details.get("stripe_customers")
            stripe_customer_id = stripe_customers.get("stripe_customer_id")
            if stripe_customer_id:
                if stripe_customers[stripe_customer_id].get("export_limit")  != None and stripe_customers[stripe_customer_id].get("export_limit") > 0:
                    pass
                else:
                    raise HTTPException(
                        status_code=403, 
                        detail="You've reached your design export limit for this billing period. Please upgrade your plan to continue creating designs."
                    )
            else:
                raise HTTPException(
                    status_code=403, 
                    detail="You're on a free plan, you can't export flyers. Please upgrade to a paid plan to export flyers"
                )


            if user_details['plan_tier'] == "free":
                raise HTTPException(
                    status_code=403, 
                    detail="You're on a free plan, you can't export flyers. Please upgrade to a paid plan to export flyers"
                )
            if flyer_data.flyer_type == "thumbnail":
                if flyer_data.thumbnail_design_query.thumbnail_type == "tiktok":
                    flyer_sizes = ["1080x1920"]
                else:
                    flyer_sizes = ["1280x720"]
            else:
                if user_details['plan_tier'] == "starter":
                    flyer_sizes = ["1080x1080"]
                elif user_details['plan_tier'] in ["pro", "premium"]:
                    flyer_sizes = ["1080x1080", "1600x900", "1200x630", "1200x628", "1080x1920", "1000x1500", "1280x720"]
                else:
                    raise HTTPException(
                        status_code=403, 
                        detail="You're on a free plan, you can't export flyers. Please upgrade to a paid plan to export flyers"
                    )
            
            designs = await self.save_design(flyer_data, user_id, flyer_sizes)
            billing_crud = BillingCrud()
            update_flyer_export_limit = billing_crud.update_flyer_export_limit(user_id)
            return designs

        except ValidationError as e:
            logger.error(f"Validation error in export_flyer: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            import traceback
            traceback.print_exc()   
            logger.error(f"Error in export_flyer: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


    async def reformat_design_size(self, size, user_id, html_content):
        """Refine the design based on user feedback"""
        refinement_prompt = reformat_design_size_prompt(size, html_content)

        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,
            messages=[{"role": "user", "content": refinement_prompt}]
        )

        
        html_content = extract_html(await response.content[0].text.strip())
        return html_content
    
    async def save_design(self, flyer_data, user_id, flyer_sizes, output_filename: str = None):
        """
        Save the current design to Firebase Storage and Firestore
        
        Args:
            flyer_data: FlyerModel containing flyer data
            user_id: User ID
            flyer_sizes: List of flyer sizes to generate
            output_filename: Optional custom filename
        
        Returns:
            list: List of FlyerDesignFile objects with URLs
        """
        try:
            # Generate base filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_filename = output_filename or f"flyer_{timestamp}"

            # Initialize Firebase clients
            bucket = storage.bucket(name=settings.STORAGE_BUCKET)
            flyer_designs = []

            for size in flyer_sizes:
                try:
                    html_content = flyer_data.html_content
                    width, height = map(int, size.split('x'))

                    
                    # Update container dimensions and styles in HTML
                    html_content = html_content.replace(
                        'width: 800px;',
                        f'width: {width}px;'
                    ).replace(
                        'height: 800px;',
                        f'height: {height}px;'
                    ).replace(
                        'margin: 20px auto;',  # Remove margin
                        'margin: 0;'
                    ).replace(
                        'border-radius: 20px;',  # Remove border radius from container
                        'border-radius: 0;'
                    )

                    flyer_id = flyer_data.flyer_id
                    html_path = f"flyers/{user_id}/{flyer_id}/{size}/{base_filename}.html"
                    jpg_path = f"flyers/{user_id}/{flyer_id}/{size}/{base_filename}.jpg"
                    
                    # Save HTML version
                    html_blob = bucket.blob(html_path)
                    html_blob.upload_from_string(
                        html_content,
                        content_type='text/html'
                    )
                    html_blob.make_public()
                    html_url = html_blob.public_url

                    # Create temporary directory
                    temp_dir = "/tmp/flyers"
                    os.makedirs(temp_dir, exist_ok=True)
                    temp_html = f"{temp_dir}/{flyer_id}_{size}.html"
                    temp_jpg = f"{temp_dir}/{flyer_id}_{size}.jpg"

                    try:
                        # Save temporary HTML file
                        with open(temp_html, 'w') as f:
                            f.write(html_content)

                        # Convert to JPG using Playwright
                        async with async_playwright() as p:
                            browser = await p.chromium.launch()
                            page = await browser.new_page()
                            
                            # Set viewport to exact size
                            await page.set_viewport_size({"width": width, "height": height})
                            
                            # Add more comprehensive CSS to remove all white space and ensure full bleed
                            await page.add_style_tag(content="""
                                * {
                                    margin: 0 !important;
                                    padding: 0 !important;
                                    box-sizing: border-box !important;
                                    border-radius: 0 !important;
                                    -webkit-border-radius: 0 !important;
                                    -moz-border-radius: 0 !important;
                                }
                                
                                html, body {
                                    margin: 0 !important;
                                    padding: 0 !important;
                                    overflow: hidden !important;
                                    width: 100% !important;
                                    height: 100% !important;
                                    background: transparent !important;
                                    display: block !important;
                                }
                                
                                .container {
                                    margin: 0 !important;
                                    padding: 0 !important;
                                    border-radius: 0 !important;
                                    position: absolute !important;
                                    top: 0 !important;
                                    left: 0 !important;
                                    right: 0 !important;
                                    bottom: 0 !important;
                                    width: 100% !important;
                                    height: 100% !important;
                                    box-shadow: none !important;
                                    overflow: hidden !important;
                                    display: flex !important;
                                }
                                
                                .content-area {
                                    padding: 60px !important;
                                    width: 42% !important;
                                    position: relative !important;
                                    z-index: 2 !important;
                                }
                                
                                .image-section {
                                    position: absolute !important;
                                    right: 0 !important;
                                    top: 0 !important;
                                    width: 60% !important;
                                    height: 100% !important;
                                    z-index: 1 !important;
                                }
                                
                                .bg-image, img {
                                    object-fit: cover !important;
                                    width: 100% !important;
                                    height: 100% !important;
                                    border-radius: 0 !important;
                                    display: block !important;
                                }
                                
                                .button, .btn, a {
                                    border-radius: 0 !important;
                                    display: inline-block !important;
                                    text-decoration: none !important;
                                }
                                
                                .social-media-bar {
                                    border-radius: 0 !important;
                                    display: flex !important;
                                    align-items: center !important;
                                }
                                
                                .logo {
                                    position: absolute !important;
                                    z-index: 3 !important;
                                }
                            """)
                            
                            await page.goto(f"file://{temp_html}")
                            await page.wait_for_load_state("networkidle")
                            
                            # Take screenshot with exact dimensions and no padding
                            await page.screenshot(
                                path=temp_jpg,
                                type='jpeg',
                                quality=100,
                                clip={
                                    "x": 0,
                                    "y": 0,
                                    "width": width,
                                    "height": height
                                },
                                omit_background=True  # This helps remove any background color
                            )
                            
                            await browser.close()

                        # Upload JPG to Firebase
                        jpg_blob = bucket.blob(jpg_path)
                        jpg_blob.upload_from_filename(temp_jpg)
                        jpg_blob.make_public()
                        jpg_url = jpg_blob.public_url

                        # Create FlyerDesignFile object
                        design_file = FlyerDesignFile(
                            sizes=size,
                            html_content_url=html_url,
                            image_url=jpg_url
                        )
                        flyer_designs.append(design_file)

                    finally:
                        # Clean up temporary files
                        for temp_file in [temp_html, temp_jpg]:
                            if os.path.exists(temp_file):
                                os.remove(temp_file)

                except Exception as e:
                    logger.error(f"Error processing size {size}: {str(e)}")
                    continue

            if not flyer_designs:
                raise HTTPException(status_code=500, detail="Failed to generate any designs")

            # Update flyer data with new designs
            updated_flyer_data = flyer_data.model_dump()
            updated_flyer_data["designs"] = [design.model_dump() for design in flyer_designs]
            updated_flyer_data["updated_at"] = datetime.now().isoformat()

            # Update in database
            await flyer_crud.update_flyer(
                user_id=user_id,
                flyer_data=updated_flyer_data
            )

            return flyer_designs

        except Exception as e:
            logger.error(f"Error in save_design: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    