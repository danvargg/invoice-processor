import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY environment variable.")

MY_API_KEY = os.getenv("MY_API_KEY")
if not MY_API_KEY:
    raise ValueError("Missing MY_API_KEY environment variable.")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)  # TODO: rename api key name


def verify_api_key(api_key: str = Depends(api_key_header)):
    """
    Verify that the X-API-Key header matches the configured key.
    Raise an HTTPException if not valid.
    """
    if not api_key or api_key != MY_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return api_key
