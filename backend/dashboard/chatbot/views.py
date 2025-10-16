from rest_framework.decorators import api_view
from rest_framework.response import Response
from .chatbot_core import get_chatbot_response  # This is your main chatbot logic

@api_view(['POST'])
def chatbot_api(request):
    """
    API endpoint for the chatbot.
    Accepts user message and returns chatbot response.
    """
    # Get the message from the request
    user_message = request.data.get('message', '')
    
    # Pass it to your core chatbot function
    bot_response = get_chatbot_response(user_message)
    
    # Return as JSON
    return Response({"response": bot_response})

printf( " hello this is me in october 16 morning after completing some task of week 1 of module 1 of Aspire leadership.")
