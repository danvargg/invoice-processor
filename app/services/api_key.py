from fastapi import Depends, HTTPException, status


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
