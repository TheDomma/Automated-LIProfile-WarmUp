import logging
from gologin import GoLogin
from config import GOLOGIN_API_TOKEN

logger = logging.getLogger(__name__)

# We keep track of active profiles here so we can close them cleanly
_active_gl_instances = {}

def start_profile(profile_id: str) -> str:
    """
    Uses the official GoLogin Python SDK to start the profile.
    """
    logger.info(f"Starting GoLogin profile via SDK: {profile_id}")
    
    # Initialize the official GoLogin wrapper
    gl = GoLogin({
        "token": GOLOGIN_API_TOKEN,
        "profile_id": profile_id,
    })
    
    # gl.start() launches the browser and returns the debugger address
    debugger_address = gl.start()
    
    if not debugger_address:
        raise ValueError("Failed to get debugger address from GoLogin")
        
    _active_gl_instances[profile_id] = gl
    
    # Playwright connects over this HTTP endpoint
    return f"http://{debugger_address}"

def stop_profile(profile_id: str) -> bool:
    """
    Stops the profile using the stored GoLogin instance.
    """
    logger.info(f"Stopping GoLogin profile: {profile_id}")
    
    gl = _active_gl_instances.get(profile_id)
    if gl:
        try:
            gl.stop()
            del _active_gl_instances[profile_id]
            return True
        except Exception as e:
            logger.error(f"Failed to stop profile {profile_id}: {e}")
            return False
    else:
        logger.error(f"No active GoLogin instance found for profile {profile_id}")
        return False