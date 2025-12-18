import google.generativeai as genai
from src.config import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel('gemini-pro')

def get_gemini_response(user_message, conversation_history=None):
    """
    Get response from Gemini AI
    
    Args:
        user_message: The user's message text
        conversation_history: Optional list of previous messages
    
    Returns:
        AI response text
    """
    try:
        if conversation_history:
            chat = model.start_chat(history=conversation_history)
            response = chat.send_message(user_message)
        else:
            response = model.generate_content(user_message)
        
        return response.text
    
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, I encountered an error processing your request. Please try again."
