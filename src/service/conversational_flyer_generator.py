import os
import requests
import urllib.parse
import re
import uuid
from datetime import datetime
from src.core.model_manager import get_claude_client
from src.model.flyer_model import FlyerCreate, FlyerModel, FlyerConversation, Role, FlyerDesignQuery, FlyerDesignFile
from src.crud.flyer_generation import flyer_crud
from src.utils.prompts import generate_marketing_content_prompt, generate_image_query_prompt, generate_initial_design_prompt, generate_refine_design_prompt, classify_intent_prompt, reformat_design_size_prompt
from src.crud.auth import AuthCrud
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

        business_details = None
        user_details = AuthCrud.get_user_details(user_id)

        for application in user_details['applications']:
            if application['application_id'] == flyer_in.application_id:
                business_details = application['application_data']
                break

        if flyer_in.flyer_description:
            #generate flyer design image search query
            if not flyer_in.image_url:
                search_query = await self.generate_image_query(flyer_in.flyer_description)
            new_flyer_design_query = FlyerDesignQuery(
                marketing_idea=flyer_in.flyer_description,
                designer_guidelines=flyer_in.flyer_description,
                image_flyer_content=flyer_in.flyer_description
            )

            conversation_history = [FlyerConversation(role=Role.USER, message=flyer_in.flyer_description, message_id=str(int(datetime.now().timestamp())))]
            conversation_history.append(FlyerConversation(role=Role.ASSISTANT, message=f"Done creating this flyer for you, will you like to make any changes?", message_id=str(int(datetime.now().timestamp()))))
        else:
            flyers = await flyer_crud.get_user_flyers(user_id)
            flyer_design_query = [flyer['flyer_design_query']['image_flyer_content'] for flyer in flyers]
            
            new_flyer_design_query = await self.generate_marketing_content(str(business_details), flyer_design_query)

            if new_flyer_design_query == None:
                raise HTTPException(status_code=400, detail="Failed to generate an automatic flyer, please tell me what you'll like to design.")

            conversation_history = [FlyerConversation(role=Role.ASSISTANT, message=f"I came up with a flyer concept for you, it is centered around {new_flyer_design_query.marketing_idea}", message_id=str(int(datetime.now().timestamp())))]

            #generate flyer design image search query
            if not flyer_in.image_url:
                search_query = await self.generate_image_query(new_flyer_design_query.designer_guidelines)

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
        html_content = await self.generate_initial_design(task_description, image_url, other_images)

        timestamp = int(datetime.now().timestamp())

        

        # Create flyer record
        flyer_model = FlyerModel(
            flyer_id=str(timestamp),
            flyer_type=flyer_in.flyer_type,
            flyer_design_query=new_flyer_design_query,
            design_image_options=images,
            current_design_image=image_url,
            html_content=html_content,
            image_url=None,
            application_id=flyer_in.application_id,
            flyer_name=new_flyer_design_query.marketing_idea[:20] + "...",
            user_id=user_id,
            conversation_history=conversation_history,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        print(html_content)


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

        match = re.search(r'{\s*"marketing_idea":\s*"(.*?)",\s*"designer_guidelines":\s*"(.*?)",\s*"image_flyer_content":\s*"(.*?)"\s*}', content_idea)
        if match:
            marketing_idea = match.group(1)
            designer_guidelines = match.group(2)
            image_flyer_content = match.group(3)
            return FlyerDesignQuery(
                marketing_idea=marketing_idea,
                designer_guidelines=designer_guidelines,
                image_flyer_content=image_flyer_content
            )
        else:
            return None
        



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


    async def generate_initial_design(self, business_details, image_url, other_images):
        """Generate the initial flyer design"""
        print(business_details)
        print(image_url)
        prompt = generate_initial_design_prompt(business_details, image_url, other_images)
        
        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        current_design = response.content[0].text.strip()
        current_design_html = extract_html(current_design)
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
                    "message": "New marketing idea generated"
                }

            elif "REFINE_DESIGN" in intent:
                flyer = await self.refine_design(user_input, user_id, flyer_id)
                response_data = {
                    "flyer": flyer.model_dump() if hasattr(flyer, 'model_dump') else flyer,
                    "message": "Design refined based on feedback"
                }

            elif "UPDATE_DESIGN_IMAGE" in intent:
                flyer = await self.update_design_image(user_id, flyer_id, image_url, user_input)
                response_data = {
                    "flyer": flyer.model_dump() if hasattr(flyer, 'model_dump') else flyer,
                    "message": "Design image updated"
                }

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
            if user_details['plan_tier'] == "free":
                raise HTTPException(
                    status_code=403, 
                    detail="You're on a free plan, you can't export flyers. Please upgrade to a paid plan to export flyers"
                )
            elif user_details['plan_tier'] == "starter":
                flyer_sizes = ["1080x1080"]
            elif user_details['plan_tier'] in ["pro", "premium"]:
                flyer_sizes = ["1080x1080", "1600x900", "1200x630", "1200x628", "1080x1920", "1000x1500", "1280x720"]
            else:
                raise HTTPException(
                    status_code=403, 
                    detail="You're on a free plan, you can't export flyers. Please upgrade to a paid plan to export flyers"
                )
            
            designs = await self.save_design(flyer_data, user_id, flyer_sizes)
            return designs

        except ValidationError as e:
            logger.error(f"Validation error in export_flyer: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
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
                            
                            # Additional CSS to remove white space and container border radius only
                            await page.add_style_tag(content="""
                                body {
                                    margin: 0;
                                    padding: 0;
                                    overflow: hidden;
                                }
                                .container {
                                    margin: 0 !important;
                                    border-radius: 0 !important;
                                }
                            """)
                            
                            await page.goto(f"file://{temp_html}")
                            await page.wait_for_load_state("networkidle")
                            
                            await page.screenshot(
                                path=temp_jpg,
                                type='jpeg',
                                quality=100,
                                clip={
                                    "x": 0,
                                    "y": 0,
                                    "width": width,
                                    "height": height
                                }
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
    
    