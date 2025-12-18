import requests
from src.config import BOT_TOKEN
from src.gemini_handler import get_gemini_response

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text, reply_to_message_id=None):
    """Send message to Telegram chat"""
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def send_chat_action(chat_id, action="typing"):
    """Send chat action (typing indicator)"""
    url = f"{TELEGRAM_API}/sendChatAction"
    payload = {
        "chat_id": chat_id,
        "action": action
    }
    
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Error sending chat action: {e}")

def handle_command(message):
    """Handle bot commands"""
    text = message.get('text', '')
    command = text.split()[0].lower()
    
    commands_info = {
        '/start': """👋 *Welcome to Angel Japagenie AI Bot!*

I'm powered by Google's Gemini AI and deployed on Vercel.

*Available Commands:*
/start - Show this welcome message
/help - Get help and usage instructions
/about - Learn about this bot
/new - Start a new conversation

Just send me any message and I'll respond using Gemini AI! 🤖✨""",
        
        '/help': """🤖 *How to Use This Bot*

Simply send me any message, question, or prompt, and I'll respond using Google's Gemini AI!

*Examples:*
- "Explain quantum computing"
- "Write a Python function to sort a list"
- "What's the capital of France?"
- "Tell me a joke"

*Commands:*
/start - Welcome message
/help - This help message
/about - About the bot
/new - Clear conversation and start fresh

💡 *Tip:* I can help with coding, explanations, creative writing, and much more!""",
        
        '/about': """ℹ️ *About Angel Japagenie Bot*

🤖 *Powered by:* Google Gemini AI
⚡ *Deployed on:* Vercel (Serverless)
💻 *Built with:* Python
🔧 *Open Source:* GitHub

This bot demonstrates serverless AI integration.

Made with ❤️""",
        
        '/new': """🔄 *New Conversation Started*

Previous context cleared. Let's start fresh! 

What would you like to talk about?"""
    }
    
    return commands_info.get(command, "❓ Unknown command. Type /help to see available commands.")

def handle_message(message):
    """Handle regular text messages with Gemini AI"""
    user_message = message.get('text', '')
    user_name = message.get('from', {}).get('first_name', 'there')
    
    if not user_message:
        return "Please send me a text message!"
    
    try:
        ai_response = get_gemini_response(user_message)
        return ai_response
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        return f"Sorry {user_name}, I encountered an error. Please try again!"

def process_update(update):
    """Process incoming Telegram update"""
    try:
        if 'message' not in update:
            return {"ok": True}
        
        message = update['message']
        chat_id = message['chat']['id']
        message_id = message.get('message_id')
        
        send_chat_action(chat_id, "typing")
        
        if 'text' in message and message['text'].startswith('/'):
            response_text = handle_command(message)
        else:
            response_text = handle_message(message)
        
        send_message(chat_id, response_text, reply_to_message_id=message_id)
        
        return {"ok": True}
    
    except Exception as e:
        print(f"Error processing update: {e}")
        return {"ok": False, "error": str(e)}
