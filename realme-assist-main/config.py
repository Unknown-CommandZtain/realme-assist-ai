"""Contains variables used throughout the project."""
import os

PORT = int(os.environ.get("PORT", 5000))

# These securely pull your secrets from Railway's Variables tab!
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///local_memory.db")
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

# Added SerpApi Key to pull from Railway Variables securely
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "") 

CONTROL_GROUP = -1001228437777
SUPPORT_GROUP = -1001374176745

# This pulls your personal ID from Railway
MY_ID = int(os.environ.get("ADMIN_ID", 0))

# You are now the ONLY Admin and the ONLY Verified User
ADMINS = (MY_ID,)
VERIFIED_USERS = {MY_ID}

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
