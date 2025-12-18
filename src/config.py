import os

# Telegram Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
SECRET_TOKEN = os.getenv('SECRET_TOKEN', 'default_secret_token')

# Gemini Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Webhook Configuration
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Validate required variables
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")
