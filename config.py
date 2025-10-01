import os

from dotenv import load_dotenv

load_dotenv()

XMLRIVER_USER_ID = os.getenv("XMLRIVER_USER_ID")
XMLRIVER_USER_KEY = os.getenv("XMLRIVER_USER_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"
