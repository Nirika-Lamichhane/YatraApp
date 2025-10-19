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


print( "  back with my aspire module and posted the feedback on my professional objectives. ")
print(" i am currently watching the pre master class materials for the master class which is uspposed to be at oct 23rd on the day of tihar bhaitika")
print ( " i did the pre class reading of one master class and another also but 1 topic.")