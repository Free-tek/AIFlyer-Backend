import os
import logging
from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from src.service.api_helper import ApiHelper
from fastapi_versioning import version
from src.crud.flyer_generation import flyer_crud
from src.model.flyer_model import FlyerCreate, FlyerUpdate, FlyerResponse, FlyerModel, FlyerDownload
from src.service.conversational_flyer_generator import ConversationalFlyerGenerator
from src.core.config import settings
from src.crud.auth import AuthCrud
import requests
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io

logger = logging.getLogger(__name__)

# create logger with log app
real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
LOGFILE = "src/logs/test.log"

fh = logging.FileHandler(LOGFILE)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

router = APIRouter(prefix="/flyer_generation")

api_client = ApiHelper()

generator = ConversationalFlyerGenerator()

@router.post("/create_flyer")
@version(1)
async def create_flyer(
    flyer_in: FlyerCreate,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(AuthCrud.verify_token),
):
    """Create a new flyer"""

    # return {'message': 'Flyer generated successfully', 'data': {'flyer': {'flyer_id': '1734746296', 'flyer_type': 'general', 'flyer_design_query': {'marketing_idea': "celebrate the changing seasons with starbucks' limited-time fall flavors. savor the warmth of a pumpkin spice latte or the comforting taste of a maple pecan latte. visit your nearest starbucks store or order through the app to enjoy these seasonal favorites before they're gone.", 'designer_guidelines': "create a visually appealing image that showcases starbucks' fall-themed beverages, such as the pumpkin spice latte and maple pecan latte. incorporate warm, autumnal colors like orange, brown, and red. include elements like fall leaves, cozy sweaters, or a starbucks store with a welcoming atmosphere. ensure the starbucks logo is prominently displayed.", 'image_flyer_content': "savor the flavors of fall with starbucks' limited-time pumpkin spice and maple pecan lattes. visit today!"}, 'design_image_options': ['https://burst.shopifycdn.com/photos/womans-hands-holding-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/woman-holding-coffee-mug.jpg?width=800', 'https://burst.shopifycdn.com/photos/cozy-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-woman-sat-with-coffee-at-the-foot-of-a-sofa.jpg?width=800', 'https://burst.shopifycdn.com/photos/business-woman-walking-in-autumn.jpg?width=800', 'https://burst.shopifycdn.com/photos/spiced-seasonal-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/friends-drinking-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/making-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/fall-preparations.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-woman-and-a-man-enjoy-a-laugh-over-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/woman-enjoying-a-cup-of-black-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/woman-reading-and-drinking-coffee-from-mug.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-close-up-of-a-woman-holding-a-coffee-cup.jpg?width=800', 'https://burst.shopifycdn.com/photos/pour-over-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-couple-chat-over-coffee-cups-on-a-sunny-day-in-a-cafe.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-woman-in-dungarees-drinks-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/who-needs-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/happy-couple-having-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/woman-walking-on-fall-city-streets.jpg?width=800', 'https://burst.shopifycdn.com/photos/purchased-favorite-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-young-woman-leans-back-on-a-couch-with-a-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/acorns-held-in-front-of-eyes.jpg?width=800', 'https://burst.shopifycdn.com/photos/woman-stands-above-fall-colored-valley.jpg?width=800', 'https://burst.shopifycdn.com/photos/woman-drinking-coffee-and-reading-an-interior-design-magazine.jpg?width=800', 'https://burst.shopifycdn.com/photos/milk-swirling-as-poured-in-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-young-couple-chat-over-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/pumpkin-and-spices.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-man-and-a-woman-share-a-smile-over-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/cozy-fall-fashion-in-field.jpg?width=800', 'https://burst.shopifycdn.com/photos/pretty-woman-sipping-coffee.jpg?width=800', 'https://burst.shopifycdn.com/photos/creamy-cold-drink-sits-on-a-wooden-table.jpg?width=800', 'https://burst.shopifycdn.com/photos/ready-set-snow.jpg?width=800', 'https://burst.shopifycdn.com/photos/incredible-balance-yoga-posing.jpg?width=800', 'https://burst.shopifycdn.com/photos/team-working-together-with-laptops.jpg?width=800', 'https://burst.shopifycdn.com/photos/blue-lake-and-rocky-mountains.jpg?width=800', 'https://burst.shopifycdn.com/photos/ripe-red-strawberries-in-a-white-bowl.jpg?width=800', 'https://burst.shopifycdn.com/photos/man-holding-shipping-box-on-red-brick.jpg?width=800', 'https://burst.shopifycdn.com/photos/person-stands-by-a-brick-wall-and-holds-a-book-open.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-minimal-yet-cosy-workspace.jpg?width=800', 'https://burst.shopifycdn.com/photos/laptop-keyboard-illuminated-in-red.jpg?width=800', 'https://burst.shopifycdn.com/photos/triangle-goat-collar.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-drop-of-pink-and-yellow-paint-in-water.jpg?width=800', 'https://burst.shopifycdn.com/photos/ice-cracks-on-a-frozen-sea.jpg?width=800', 'https://burst.shopifycdn.com/photos/woman-resting-her-feet-by-the-window.jpg?width=800', 'https://burst.shopifycdn.com/photos/person-in-a-white-shirt-sits-in-front-of-a-brick-wall.jpg?width=800', 'https://burst.shopifycdn.com/photos/large-fall-leaf-in-hand.jpg?width=800', 'https://burst.shopifycdn.com/photos/mixing-board-black-and-white.jpg?width=800', 'https://burst.shopifycdn.com/photos/long-forest-path.jpg?width=800', 'https://burst.shopifycdn.com/photos/brushes-blossoms.jpg?width=800', 'https://burst.shopifycdn.com/photos/bustling-city-street-in-india.jpg?width=800', 'https://burst.shopifycdn.com/photos/black-and-white-crosswalk.jpg?width=800', 'https://burst.shopifycdn.com/photos/lingerie-champaign-lipstick-roses.jpg?width=800', 'https://burst.shopifycdn.com/photos/glowing-night-full-moon.jpg?width=800', 'https://burst.shopifycdn.com/photos/woman-watching-beach-sunrise.jpg?width=800', 'https://burst.shopifycdn.com/photos/model-with-leather-jacket-over-shoulders.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-tattooed-hand-doing-the-sign-for-i-love-you.jpg?width=800', 'https://burst.shopifycdn.com/photos/snow-globe-in-festive-living-room.jpg?width=800', 'https://burst.shopifycdn.com/photos/person-writing-in-notebook-beside-laptop-working-from-bed.jpg?width=800', 'https://burst.shopifycdn.com/photos/office-flat-lay-on-wooden-desk-with-catch-tray.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-man-in-denim-apron-smiles-for-the-camera.jpg?width=800', 'https://burst.shopifycdn.com/photos/phone-taking-photo-of-museum.jpg?width=800', 'https://burst.shopifycdn.com/photos/the-illuminated-tiled-terminal-of-an-airport.jpg?width=800', 'https://burst.shopifycdn.com/photos/rosary-resting-on-bible.jpg?width=800', 'https://burst.shopifycdn.com/photos/banana-stand.jpg?width=800', 'https://burst.shopifycdn.com/photos/modern-archer.jpg?width=800', 'https://burst.shopifycdn.com/photos/different-colored-lollipops-on-black.jpg?width=800', 'https://burst.shopifycdn.com/photos/blue-nature.jpg?width=800', 'https://burst.shopifycdn.com/photos/butterfly-in-palm-close-up.jpg?width=800', 'https://burst.shopifycdn.com/photos/students-at-coding-workshop.jpg?width=800', 'https://burst.shopifycdn.com/photos/close-up-of-puppys-eyes.jpg?width=800', 'https://burst.shopifycdn.com/photos/wooden-path-in-dark-forest.jpg?width=800', 'https://burst.shopifycdn.com/photos/thai-elephant.jpg?width=800', 'https://burst.shopifycdn.com/photos/thick-lush-green-forest.jpg?width=800', 'https://burst.shopifycdn.com/photos/mobile-internet-upgrade-screen.jpg?width=800', 'https://burst.shopifycdn.com/photos/developer-leading-planning-session.jpg?width=800', 'https://burst.shopifycdn.com/photos/black-and-white-city-street.jpg?width=800', 'https://burst.shopifycdn.com/photos/the-sun-drops-below-the-watery-horizon.jpg?width=800', 'https://burst.shopifycdn.com/photos/gardening-flatlay.jpg?width=800', 'https://burst.shopifycdn.com/photos/doctor-holds-chart.jpg?width=800', 'https://burst.shopifycdn.com/photos/home-office-a-typewritten-message.jpg?width=800', 'https://burst.shopifycdn.com/photos/golfer-holds-golf-ball.jpg?width=800', 'https://burst.shopifycdn.com/photos/two-tone-ink-cloud.jpg?width=800', 'https://burst.shopifycdn.com/photos/wooden-craft-table-set-up-for-watercolors.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-bee-tucks-into-the-dark-centre-of-a-sunflower.jpg?width=800', 'https://burst.shopifycdn.com/photos/charcoal-ice-cream.jpg?width=800', 'https://burst.shopifycdn.com/photos/man-sits-and-laughs.jpg?width=800', 'https://burst.shopifycdn.com/photos/mens-fashion-close-up-shirt-tucked-in-leaning.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-note-just-to-say-you-are-enough.jpg?width=800', 'https://burst.shopifycdn.com/photos/a-credit-card-transaction-over-a-card-reader.jpg?width=800', 'https://burst.shopifycdn.com/photos/milkshake-on-pink.jpg?width=800', 'https://burst.shopifycdn.com/photos/blurry-abstract-photo-of-glass-bottles.jpg?width=800', 'https://burst.shopifycdn.com/photos/tanned-sand-dunes-surrounded-an-open-reservoir.jpg?width=800', 'https://burst.shopifycdn.com/photos/sunset-coloured-petals-against-green-leaves.jpg?width=800', 'https://burst.shopifycdn.com/photos/perfect-yellow-flower.jpg?width=800', 'https://burst.shopifycdn.com/photos/english-castle.jpg?width=800', 'https://burst.shopifycdn.com/photos/looking-back-through-arches-in-india.jpg?width=800', 'https://burst.shopifycdn.com/photos/kids-show-mom-some-love.jpg?width=800', 'https://burst.shopifycdn.com/photos/lensball-yellow-and-orange-lights.jpg?width=800', 'https://burst.shopifycdn.com/photos/red-foiled-hearts-on-a-pink-background.jpg?width=800', 'https://burst.shopifycdn.com/photos/hibiscus-tea.jpg?width=800', 'https://burst.shopifycdn.com/photos/small-farming-village-seen-through-branches.jpg?width=800', 'https://burst.shopifycdn.com/photos/darkest-before-the-dawn.jpg?width=800'], 'current_design_image': 'https://burst.shopifycdn.com/photos/womans-hands-holding-coffee.jpg?width=800', 'html_content': '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Starbucks Fall Flavors</title>\n    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">\n    <style>\n        @import url(\'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap\');\n        * {\n            margin: 0;\n            padding: 0;\n            box-sizing: border-box;\n        }\n        body {\n            font-family: \'Poppins\', sans-serif;\n            background: linear-gradient(135deg, #fffcfc, #0b421a);\n            display: flex;\n            align-items: center;\n            justify-content: center;\n            min-height: 100vh;\n            padding: 20px;\n        }\n        .container {\n            width: 800px;\n            height: 800px; \n            position: relative;\n            background: linear-gradient(135deg, rgba(11,66,26,0.8), rgba(255,252,252,0.8));\n            border-radius: 20px;\n            box-shadow: 0 20px 40px rgba(0,0,0,0.1);\n            overflow: hidden;\n            padding: 40px;\n        }\n        .bg-image {\n            position: absolute;\n            top: 0;\n            left: 0;\n            width: 100%;\n            height: 100%;\n            object-fit: cover;\n            object-position: center;\n            z-index: -1;\n        }\n        .overlay {\n            position: absolute;\n            top: 0;\n            left: 0;\n            width: 100%;\n            height: 100%;\n            background: linear-gradient(to bottom, rgba(0,0,0,0.4), rgba(0,0,0,0.2));\n        }\n        .logo {\n            position: absolute;\n            top: 40px;\n            right: 40px;\n            max-width: 100px;\n        }\n        .content {\n            position: relative;\n            z-index: 1;\n            color: #fff;\n            text-align: center;\n            margin-top: 60px;\n        }\n        h1 {\n            font-size: 62px;\n            font-weight: 700;\n            margin-bottom: 20px;\n            line-height: 1.2;\n            text-shadow: 0 4px 6px rgba(0,0,0,0.1);\n        }\n        p {\n            font-size: 40px;\n            margin-bottom: 60px;\n            max-width: 600px;\n            margin-left: auto;\n            margin-right: auto;\n            line-height: 1.6;\n            text-shadow: 0 2px 4px rgba(0,0,0,0.1);\n        }\n        .btn {\n            background: #fff;\n            color: #0b421a;\n            font-size: 40px;\n            font-weight: 600;\n            padding: 20px 40px;\n            border-radius: 30px;\n            text-decoration: none;\n            display: inline-block;\n            transition: transform 0.2s ease;\n        }\n        .btn:hover {\n            transform: translateY(-2px);\n        }\n        .social-media-bar {\n            position: absolute;\n            bottom: 40px;\n            left: 40px;\n            display: flex;\n            align-items: center;\n            gap: 10px;\n            padding: 10px;\n            background: rgba(255,255,255,0.2);\n            border-radius: 10px;\n        }\n        .social-icons {\n            display: flex;\n            gap: 15px;\n        }\n        .social-icons i {\n            font-size: 32px;\n            color: #fff;\n            transition: color 0.2s ease;\n        }\n        .social-icons i:hover {\n            color: #0b421a;\n        }\n        .social-handle {\n            font-size: 24px;\n            font-weight: 500;\n            color: #fff;\n        }\n    </style>\n</head>\n<body>\n    <div class="container">\n        <img src="https://burst.shopifycdn.com/photos/womans-hands-holding-coffee.jpg?width=800" alt="Starbucks Fall Flavors" class="bg-image">\n        <div class="overlay"></div>\n        <img src="https://firebasestorage.googleapis.com/v0/b/flyerai.firebasestorage.app/o/logos%2FQgFC1jlyYvb4tX8m9cMvthLyUP13%2Fstarbucks-logo-starbucks-icon-transparent-free-png.webp?alt=media&token=562aec7c-c756-47f2-962a-7bda77bdf6ba" alt="Starbucks Logo" class="logo">\n        <div class="content">\n            <h1>Fall Flavors Are Here</h1>\n            <p>Savor the flavors of fall with Starbucks\' limited-time Pumpkin Spice and Maple Pecan Lattes.</p>\n            <a href="#" class="btn">Visit Today!</a>\n        </div>\n        <div class="social-media-bar">\n            <div class="social-icons">\n                <i class="fab fa-facebook"></i>\n                <i class="fab fa-instagram"></i>\n                <i class="fab fa-twitter"></i>\n                <i class="fab fa-tiktok"></i>\n            </div>\n            <span class="social-handle">@starbucks</span>\n        </div>\n    </div>\n</body>\n</html>', 'image_url': None, 'application_id': '81b3f1e5-98b7-4f33-abe0-5bff45ca2a25', 'flyer_name': 'celebrate the changi...', 'conversation_history': [{'role': 'assistant', 'message': "I came up with a flyer concept for you, it is centered around celebrate the changing seasons with starbucks' limited-time fall flavors. savor the warmth of a pumpkin spice latte or the comforting taste of a maple pecan latte. visit your nearest starbucks store or order through the app to enjoy these seasonal favorites before they're gone.", 'message_id': '1734746242'}], 'designs': None, 'created_at': '2024-12-20T17:58:16.010466', 'updated_at': '2024-12-20T17:58:16.010478'}, 'message': "I came up with a flyer concept for you, it is centered around celebrate the changing seasons with starbucks' limited-time fall flavors. savor the warmth of a pumpkin spice latte or the comforting taste of a maple pecan latte. visit your nearest starbucks store or order through the app to enjoy these seasonal favorites before they're gone."}, 'status': 'success'}

    flyer_model = await generator.generate_flyer(flyer_in, user_id)
    if type(flyer_model) == FlyerModel:
        if flyer_in.flyer_description:
            return {"message": "Flyer generated successfully", "data": {"flyer": flyer_model.model_dump(), "message": f"Done creating this flyer for you, will you like to make any changes?"}, "status": "success"}
        else:
            result = {"message": "Flyer generated successfully", "data": {"flyer": flyer_model.model_dump(), "message": f"I came up with a flyer concept for you, it is centered around {flyer_model.flyer_design_query.marketing_idea}"}, "status": "success"}
            print(f"result: {result}")
            return {"message": "Flyer generated successfully", "data": {"flyer": flyer_model.model_dump(), "message": f"I came up with a flyer concept for you, it is centered around {flyer_model.flyer_design_query.marketing_idea}"}, "status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Failed to generate an automatic flyer, please tell me what you'll like to design.")


@router.post("/update")
async def update_flyer(
    flyer_update: FlyerUpdate,
    user_id: str = Depends(AuthCrud.verify_token),
):
    try:
        generator = ConversationalFlyerGenerator()
        result = await generator.process_command(flyer_update, user_id)
        
        # Check if result is an exception
        if isinstance(result, Exception):
            raise result
            
        # Ensure result is a dictionary
        if not isinstance(result, dict):
            result = {"flyer": result}

        print(f"result: {result}")
            
        return {
            "message": "Flyer updated successfully",
            "data": result,
            "status": "success"
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in update_flyer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/export")
@version(1)
async def export_flyer(
    flyer_id: str,
    user_id: str = Depends(AuthCrud.verify_token)
):
    """Export the flyer to a file"""
    print(f"this is export flyer id: {flyer_id}")
    response = await generator.export_flyer(user_id, flyer_id)
    if type(response) == list:
        result = {"message": "Flyer exported successfully", "data": {"flyer": [design.model_dump() for design in response]}, "status": "success"}
        print(f"this is result: {result}")
        return result
    else:
        return response

@router.get("/get_flyer/{flyer_id}")
@version(1)
async def get_flyer(
    flyer_id: str,
    user_id: str = Depends(AuthCrud.verify_token)
):
    """Get a flyer by ID"""
    flyer = await flyer_crud.get_flyer(user_id, flyer_id)
    if type(flyer) == dict:
        return {"message": "Flyer fetched successfully", "data": {"flyer": flyer}, "status": "success"}
    else:
        raise HTTPException(status_code=404, detail="Flyer not found")
    

@router.get("/get_all_flyers")
@version(1)
async def get_all_flyers(user_id: str = Depends(AuthCrud.verify_token)):
    """Get all flyers"""
    print(f"this is the user id: {user_id}")
    flyers = await flyer_crud.get_user_flyers(user_id)
    return {"message": "Flyers fetched successfully", "data": {"flyers": flyers}, "status": "success"}


@router.delete("/{flyer_id}")
@version(1)
async def delete_flyer(
    flyer_id: str,
    user_id: str = Depends(AuthCrud.verify_token)
):
    """Delete a flyer"""
    success = await flyer_crud.delete_flyer(user_id, flyer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Flyer not found")
    return {"message": "Flyer deleted successfully"}

@router.post("/download")
async def download_file(flyer_download: FlyerDownload, user_id: str = Depends(AuthCrud.verify_token)):
    try:
        # Download the file from Firebase Storage
        response = requests.get(flyer_download.url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to download file")

        # Create a byte stream from the content
        content = io.BytesIO(response.content)
        
        # Return the file content with appropriate headers
        return StreamingResponse(
            content,
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f'attachment; filename="flyer.jpg"',
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, token",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))