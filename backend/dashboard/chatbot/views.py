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

print( " hello this is me in october 16 morning after completing some task of week 1 of module 1 of Aspire leadership.")
print(" this day bhugol came and the day just passed by doing nothing")
print(" it is october 17 and its 12:29pm now and we just had lunch and i also had sugarcane.")
print(" this is me at 2:13 after completing week 1 of module 1 after identifying what are my characters and how can i refine them ")
print(" i also identify my goals and how can i acheive these goals ")
print(" i texted to kec ieee and asked them about ieeextreme ")