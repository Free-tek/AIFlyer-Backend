from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from typing import Optional
from src.core.config import settings
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
logger = logging.getLogger(__name__)


open_ai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
claude_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

@asynccontextmanager
def get_openai_client():
    """Get the OpenAI client instance"""
    return open_ai_client

def get_claude_client():
    """Get the Claude client instance"""
    return claude_client
