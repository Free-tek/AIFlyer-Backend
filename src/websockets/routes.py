from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
import logging
import json
from typing import List, Dict, Any
import asyncio
from websockets.exceptions import ConnectionClosedError
import time
from datetime import datetime
import traceback
import sys

ws_router = APIRouter()
logger = logging.getLogger(__name__)

# HTML template for testing WebSocket suggestions
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Suggestions WebSocket Test</title>
    </head>
    <body>
        <h1>WebSocket Suggestions</h1>
        <div>
            <label for="token">Token:</label>
            <input type="text" id="token" value="your-jwt-token-here"/>
        </div>
        <div>
            <label for="appId">App ID:</label>
            <input type="text" id="appId" value="your-app-id-here"/>
        </div>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" placeholder="Start typing..." autocomplete="off"/>
            <button>Get Suggestions</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            function connectWebSocket() {
                var token = document.getElementById("token").value;
                var ws = new WebSocket(`wss://y0sibc8nxuplv8-8002.proxy.runpod.net/ws/autocomplete?token=${token}&x_signature=aaaaa`);
                
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(JSON.stringify(JSON.parse(event.data), null, 2))
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                
                return ws;
            }
            
            var ws = connectWebSocket();
            
            // Reconnect if token changes
            document.getElementById("token").addEventListener("change", function() {
                ws.close();
                ws = connectWebSocket();
            });
            
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                var appId = document.getElementById("appId").value;
                ws.send(JSON.stringify({query: input.value, app_id: appId}))
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@ws_router.get("/chat")
async def get():
    return HTMLResponse(html)


# @ws_router.websocket("/ws/autocomplete")
# async def websocket_autocomplete(websocket: WebSocket, token: str, x_signature: str):
#     logger.info("WebSocket connection attempt for autocomplete")
#     connection_id = id(websocket)
#     suggestions_operations = SuggestionsOperations()
    
#     try:
#         await websocket.accept()
        
#         try:
#             auth_start = time.time()
#             # Validate token and check limits
#             data = await websocket.receive_json()
#             app_id = data.get("app_id")
            
#             if not app_id:
#                 await websocket.send_json({
#                     "status": False,
#                     "error": "missing_app_id",
#                     "message": "app_id is required"
#                 })
#                 await websocket.close(code=4000)
#                 return
            
#             # First validate the token
#             validated_user = await verify_administrator_token_and_tier_x_user(token)
            
#             # Then check search limits with the validated user
#             await verify_search_limits(app_id, validated_user)
            
#             user_details = validated_user.user_details
#             auth_time = time.time() - auth_start
            
            
#         except HTTPException as e:
#             # Handle plan limit exceeded error
#             error_response = {
#                 "status": False,
#                 "error": "plan_limit_exceeded",
#                 "message": e.detail,
#                 "code": e.status_code
#             }
#             await websocket.send_json(error_response)
#             await websocket.close(code=4029)  # Custom code for plan limit exceeded
#             logger.warning(f"Connection {connection_id} closed due to plan limits: {e.detail}")
#             return
            
#         except Exception as e:
#             # Handle other authentication errors with more detailed logging
#             error_location = traceback.extract_tb(sys.exc_info()[2])[-1]
#             error_details = (
#                 f"Error: {str(e)}\n"
#                 f"File: {error_location.filename}\n"
#                 f"Function: {error_location.name}\n"
#                 f"Line: {error_location.lineno}"
#             )
            
#             error_response = {
#                 "status": False,
#                 "error": "authentication_failed",
#                 "message": "Invalid authentication credentials",
#                 "code": 4001
#             }
#             await websocket.send_json(error_response)
#             await websocket.close(code=4001)
#             logger.error(f"Authentication failed for connection {connection_id}: {error_details}")
#             return

#         # Rest of the websocket logic...
#         while True:
#             try:
#                 # Start total execution timer
#                 total_start_time = time.time()
                
#                 # Time request parsing
#                 parse_start = time.time()
#                 data = await websocket.receive_text()
#                 request = json.loads(data)
#                 query = request.get('query', '')
#                 query_length = len(query)
#                 app_id = request.get('app_id')
#                 parse_time = time.time() - parse_start
                
#                 # Time pipeline selection
#                 selection_start = time.time()
#                 selection_time = time.time() - selection_start
                
#                 logger.info(f"Received suggestion request for query: {query}")
                
#                 # Time suggestion generation using shared function
#                 generation_start = time.time()
#                 store_description = get_store_description(app_id)   
#                 suggestions = await suggestions_operations.autocomplete_user_query(
#                     query=query,
#                     store_description=store_description
#                 )

#                 generation_time = time.time() - generation_start
                
#                 if not suggestions:
#                     await websocket.send_json({
#                         "next_word": "",
#                         "next_two_words": "",
#                         "five_sentence_suggestions": []
#                     })
#                     continue
                
#                 # Time suggestion processing
#                 processing_start = time.time()
#                 next_word = suggestions.next_word_prediction
#                 next_two_words = suggestions.next_two_words_prediction
#                 processing_time = time.time() - processing_start
                
#                 # Time response sending
#                 response_start = time.time()
#                 await websocket.send_json({
#                     "next_word": next_word,
#                     "next_two_words": next_two_words
#                 })
#                 response_time = time.time() - response_start
                
#                 # Calculate total execution time
#                 total_time = time.time() - total_start_time
                
#                 # Create timing information
#                 timing_info = {
#                     "timestamp": datetime.now().isoformat(),
#                     "connection_id": connection_id,
#                     "query_length": query_length,
#                     "timings": {
#                         "auth": f"{auth_time:.3f}s",
#                         "pipeline_initialization": f"0s",
#                         "request_parsing": f"{parse_time:.3f}s",
#                         "pipeline_selection": f"{selection_time:.3f}s",
#                         "suggestion_generation": f"{generation_time:.3f}s",
#                         "suggestion_processing": f"{processing_time:.3f}s",
#                         "response_sending": f"{response_time:.3f}s",
#                         "total_execution": f"{total_time:.3f}s"
#                     },
#                     "pipeline_used": "open-ai",
#                     "suggestions_count": 1
#                 }
                
#                 logger.info(f"Suggestion timing information: {json.dumps(timing_info, indent=2)}")
                
#             except WebSocketDisconnect:
#                 logger.info(f"WebSocket connection {connection_id} closed by client")
#                 break
#             except ConnectionClosedError:
#                 logger.info(f"WebSocket connection {connection_id} closed unexpectedly")
#                 break
#             except Exception as e:
#                 logger.error(f"Error processing message on connection {connection_id}: {str(e)}")
#                 try:
#                     await websocket.send_json({
#                         "error": "Internal server error",
#                         "details": str(e)
#                     })
#                 except Exception:
#                     logger.error("Could not send error message to client")
#                 break
    
#     except Exception as e:
#         logger.error(f"Error in WebSocket connection {connection_id}: {str(e)}")
    
#     finally:
#         cleanup_start = time.time()
#         logger.info(f"Cleaning up connection {connection_id}")
#         try:
#             await websocket.close()
#         except Exception:
#             pass
        



# @ws_router.websocket("/ws/suggestions")
# async def websocket_suggestions(websocket: WebSocket, token: str, x_signature: str):
#     logger.info("WebSocket connection attempt for suggestions")
#     connection_id = id(websocket)
#     pipelines = None
    
#     try:
#         await websocket.accept()
        
#         try:
#             auth_start = time.time()
#             # Validate token and check limits
#             data = await websocket.receive_json()
#             app_id = data.get("app_id")
            
#             if not app_id:
#                 await websocket.send_json({
#                     "status": False,
#                     "error": "missing_app_id",
#                     "message": "app_id is required"
#                 })
#                 await websocket.close(code=4000)
#                 return
            
#             # First validate the token
#             validated_user = await verify_administrator_token_and_tier_x_user(token)
            
#             # Then check search limits with the validated user
#             await verify_search_limits(app_id, validated_user)
            
#             user_details = validated_user.user_details
#             auth_time = time.time() - auth_start
            
#             # Initialize pipelines after successful authentication
#             pipeline_init_start = time.time()
#             pipelines = {
#                 'small': get_pipeline(0),   # For queries < 12 chars
#                 'medium': get_pipeline(12), # For queries 12-120 chars
#                 'large': get_pipeline(120)   # For queries > 120 chars
#             }
#             pipeline_init_time = time.time() - pipeline_init_start
#             logger.info(f"Pipeline initialization time: {pipeline_init_time:.3f}s")
            
#         except HTTPException as e:
#             # Handle plan limit exceeded error
#             error_response = {
#                 "status": False,
#                 "error": "plan_limit_exceeded",
#                 "message": e.detail,
#                 "code": e.status_code
#             }
#             await websocket.send_json(error_response)
#             await websocket.close(code=4029)  # Custom code for plan limit exceeded
#             logger.warning(f"Connection {connection_id} closed due to plan limits: {e.detail}")
#             return
            
#         except Exception as e:
#             # Handle other authentication errors with more detailed logging
#             error_location = traceback.extract_tb(sys.exc_info()[2])[-1]
#             error_details = (
#                 f"Error: {str(e)}\n"
#                 f"File: {error_location.filename}\n"
#                 f"Function: {error_location.name}\n"
#                 f"Line: {error_location.lineno}"
#             )
            
#             error_response = {
#                 "status": False,
#                 "error": "authentication_failed",
#                 "message": "Invalid authentication credentials",
#                 "code": 4001
#             }
#             await websocket.send_json(error_response)
#             await websocket.close(code=4001)
#             logger.error(f"Authentication failed for connection {connection_id}: {error_details}")
#             return

#         # Rest of the websocket logic...
#         while True:
#             try:
#                 # Start total execution timer
#                 total_start_time = time.time()
                
#                 # Time request parsing
#                 parse_start = time.time()
#                 data = await websocket.receive_text()
#                 request = json.loads(data)
#                 query = request.get('query', '')
#                 app_id = request.get('app_id')
#                 parse_time = time.time() - parse_start
                
#                 # Time pipeline selection
#                 selection_start = time.time()
#                 query_length = len(query)
#                 if query_length < 12:
#                     pipeline = pipelines['small']
#                 elif query_length < 120:
#                     pipeline = pipelines['medium']
#                 else:
#                     pipeline = pipelines['large']
#                 selection_time = time.time() - selection_start
                
#                 logger.info(f"Received suggestion request for query: {query}")
                
#                 # Time suggestion generation using shared function
#                 generation_start = time.time()
#                 suggestions = await generate_multiple_suggestions(
#                     pipeline=pipeline,
#                     query=query,
#                     app_id=app_id,
#                     num_suggestions=3
#                 )
#                 generation_time = time.time() - generation_start
                
#                 if not suggestions:
#                     await websocket.send_json({
#                         "next_word": "",
#                         "next_two_words": "",
#                         "five_sentence_suggestions": []
#                     })
#                     continue
                
#                 # Time suggestion processing
#                 processing_start = time.time()
#                 first_suggestion = suggestions[0]
#                 words = first_suggestion.strip().split()
#                 next_word = words[0] if words else ""
#                 next_two_words = " ".join(words[:2]) if len(words) >= 2 else next_word
#                 full_suggestions = [f"{query}{suggestion}" for suggestion in suggestions]
#                 processing_time = time.time() - processing_start
                
#                 # Time response sending
#                 response_start = time.time()
#                 await websocket.send_json({
#                     "next_word": next_word,
#                     "next_two_words": next_two_words,
#                     "five_sentence_suggestions": full_suggestions
#                 })
#                 response_time = time.time() - response_start
                
#                 # Calculate total execution time
#                 total_time = time.time() - total_start_time
                
#                 # Create timing information
#                 timing_info = {
#                     "timestamp": datetime.now().isoformat(),
#                     "connection_id": connection_id,
#                     "query_length": query_length,
#                     "timings": {
#                         "auth": f"{auth_time:.3f}s",
#                         "pipeline_initialization": f"{pipeline_init_time:.3f}s",
#                         "request_parsing": f"{parse_time:.3f}s",
#                         "pipeline_selection": f"{selection_time:.3f}s",
#                         "suggestion_generation": f"{generation_time:.3f}s",
#                         "suggestion_processing": f"{processing_time:.3f}s",
#                         "response_sending": f"{response_time:.3f}s",
#                         "total_execution": f"{total_time:.3f}s"
#                     },
#                     "pipeline_used": "small" if query_length < 12 else "medium" if query_length < 120 else "large",
#                     "suggestions_count": len(suggestions)
#                 }
                
#                 logger.info(f"Suggestion timing information: {json.dumps(timing_info, indent=2)}")
                
#             except WebSocketDisconnect:
#                 logger.info(f"WebSocket connection {connection_id} closed by client")
#                 break
#             except ConnectionClosedError:
#                 logger.info(f"WebSocket connection {connection_id} closed unexpectedly")
#                 break
#             except Exception as e:
#                 logger.error(f"Error processing message on connection {connection_id}: {str(e)}")
#                 try:
#                     await websocket.send_json({
#                         "error": "Internal server error",
#                         "details": str(e)
#                     })
#                 except Exception:
#                     logger.error("Could not send error message to client")
#                 break
    
#     except Exception as e:
#         logger.error(f"Error in WebSocket connection {connection_id}: {str(e)}")
    
#     finally:
#         cleanup_start = time.time()
#         logger.info(f"Cleaning up connection {connection_id}")
#         try:
#             await websocket.close()
#         except Exception:
#             pass
        
#         try:
#             for pipe in pipelines.values():
#                 if pipe:
#                     del pipe
#             cleanup_time = time.time() - cleanup_start
#             logger.info(f"Pipelines cleaned up for connection {connection_id}. Cleanup time: {cleanup_time:.3f}s")
#         except Exception as e:
#             logger.error(f"Error cleaning up pipelines for connection {connection_id}: {str(e)}")