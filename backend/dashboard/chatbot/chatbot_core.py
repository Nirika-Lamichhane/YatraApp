# dashboard/chatbot/chatbot_core.py

from openai import OpenAI
from .retrieval import (
    retrieve_destination_types,
    retrieve_destinations,
    retrieve_places,
    retrieve_hotels,
    retrieve_foods,
    retrieve_activities
)
from .formatter import format_places, format_hotels, format_foods, format_activities

# Initialize LLM client (replace with your own API key if needed)
client = OpenAI(api_key="YOUR_API_KEY_HERE")


def process_user_query(user_query: str):
    """
    Main function that connects the user's message to database retrieval and LLM reasoning.
    """

    # Step 1: Send query to LLM to decide what the user is asking about
    intent_prompt = f"""
    You are an intelligent travel assistant for a Nepali travel app.
    The user has asked: "{user_query}"

    Determine what kind of information they are asking for.
    Your response must be one of the following categories:
    - "destination_type"
    - "destination"
    - "place"
    - "hotel"
    - "food"
    - "activity"
    - "general" (if not related to travel data)

    Return only the category name as output.
    """

    intent_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a classification assistant."},
                  {"role": "user", "content": intent_prompt}]
    )

    category = intent_response.choices[0].message.content.strip().lower()

    # Step 2: Retrieve data based on the predicted category
    data = None

    if category == "destination_type":
        data = retrieve_destination_types()
    elif category == "destination":
        data = retrieve_destinations()
    elif category == "place":
        data = retrieve_places()
    elif category == "hotel":
        data = retrieve_hotels()
    elif category == "food":
        data = retrieve_foods()
    elif category == "activity":
        data = retrieve_activities()
    else:
        # Fallback: Let LLM generate a general conversational response
        answer = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a friendly Nepali travel assistant."},
                {"role": "user", "content": user_query}
            ]
        )
        return answer.choices[0].message.content.strip()

    # Step 3: Format retrieved data for a user-friendly response
    if not data:
        return "Sorry, I couldn't find anything related to that."

    formatted_output = ""
    if category == "place":
        formatted_output = format_places(data)
    elif category == "hotel":
        formatted_output = format_hotels(data)
    elif category == "food":
        formatted_output = format_foods(data)
    elif category == "activity":
        formatted_output = format_activities(data)
    else:
        formatted_output = "\n".join([str(item) for item in data])

    # Step 4: Combine LLM language ability + database content
    final_prompt = f"""
    You are a chatbot helping tourists explore Nepal.
    Here is the data fetched from the database:
    {formatted_output}

    Based on this data, answer the user's question:
    "{user_query}"

    Keep the tone friendly, concise, and informative.
    """

    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a travel chatbot for Nepal."},
            {"role": "user", "content": final_prompt}
        ]
    )

    return final_response.choices[0].message.content.strip()
