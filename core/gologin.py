import requests
import logging
from config import GOLOGIN_API_URL

logger = logging.getLogger(__name__)

def start_profile(profile_id: str) -> str:
    """
    Calls GoLogin local API to start the profile and returns the websocket URL.
    """
    url = f"{GOLOGIN_API_URL}/browser/start-profile?profileId={profile_id}"
    logger.info(f"Starting GoLogin profile: {profile_id}")
    
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    ws_url = data.get("wsUrl")
    
    if not ws_url:
        raise ValueError("WebSocket URL not returned from GoLogin API")
        
    return ws_url

def stop_profile(profile_id: str) -> bool:
    """
    Calls GoLogin local API to stop the profile.
    """
    url = f"{GOLOGIN_API_URL}/browser/stop-profile?profileId={profile_id}"
    logger.info(f"Stopping GoLogin profile: {profile_id}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"Failed to stop profile {profile_id}: {e}")
        return False
