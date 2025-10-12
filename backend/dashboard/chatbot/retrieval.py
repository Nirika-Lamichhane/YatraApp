# dashboard/chatbot/chatbot_core.py

from .retrieval import (
    retrieve_destination_types, retrieve_destinations,
    retrieve_places, retrieve_hotels, retrieve_foods, retrieve_activities
)
from .formatter import (
    format_destination_types, format_destinations, format_places,
    format_hotels, format_foods, format_activities
)

def chatbot_response(user_query):
    """
    Main function to handle user query and return chatbot response.
    """

    query = user_query.lower()  # simple normalization

    # -----------------------------
    # 1. Intent Detection (Basic Keyword Matching)
    # -----------------------------
    if "destination type" in query or "categories" in query:
        types = retrieve_destination_types()
        return format_destination_types(types)

    elif "destination" in query or "places" in query:
        # Extract destination type if mentioned
        dest_type = None
        for t in ["adventure", "religious", "cultural"]:  # extend as per your DB
            if t in query:
                dest_type = t
                break
        destinations = retrieve_destinations(destination_type_name=dest_type)
        return format_destinations(destinations)

    elif "place" in query or "top place" in query:
        # Extract destination name if mentioned
        dest_name = None
        for d in ["pokhara", "chitwan", "kathmandu"]:  # extend dynamically if needed
            if d in query:
                dest_name = d
                break
        # Check if user mentioned rating
        min_rating = None
        if "5 star" in query or "5 stars" in query:
            min_rating = 5.0
        elif "4 star" in query:
            min_rating = 4.0
        places = retrieve_places(destination_name=dest_name, min_rating=min_rating)
        return format_places(places)

    elif "hotel" in query or "stay" in query:
        # Extract place name and optional price/rating
        place_name = None
        for d in ["pokhara", "chitwan", "kathmandu"]:
            if d in query:
                place_name = d
                break
        max_price = None
        min_rating = None
        if "5 star" in query:
            min_rating = 5.0
        hotels = retrieve_hotels(place_name=place_name, max_price=max_price, min_rating=min_rating)
        return format_hotels(hotels)

    elif "food" in query or "eat" in query:
        place_name = None
        food_type = None
        for d in ["pokhara", "chitwan", "kathmandu"]:
            if d in query:
                place_name = d
        for ft in ["momo", "dal bhat", "chowmein"]:  # extend as per your DB
            if ft in query:
                food_type = ft
        foods = retrieve_foods(place_name=place_name, food_type=food_type)
        return format_foods(foods)

    elif "activity" in query or "things to do" in query:
        place_name = None
        activity_type = None
        for d in ["pokhara", "chitwan", "kathmandu"]:
            if d in query:
                place_name = d
        activities = retrieve_activities(place_name=place_name, activity_type=activity_type)
        return format_activities(activities)

    elif "3 day" in query or "itinerary" in query or "plan" in query:
        # Custom logic to generate 3-day plan from database
        place_name = None
        for d in ["pokhara", "chitwan", "kathmandu"]:
            if d in query:
                place_name = d
                break
        places = retrieve_places(destination_name=place_name)
        hotels = retrieve_hotels(place_name=place_name)
        activities = retrieve_activities(place_name=place_name)
        foods = retrieve_foods(place_name=place_name)
        
        # Simple 3-day plan formatting
        message = f"📅 Here’s a 3-day plan for {place_name.title()}:\n\n"
        if places:
            message += f"Day 1: Visit {places[0].name}\n"
        if activities:
            message += f"Day 2: {activities[0].name} and {activities[1].name if len(activities)>1 else ''}\n"
        if foods:
            message += f"Day 3: Try {foods[0].name} and {foods[1].name if len(foods)>1 else ''}\n"
        if hotels:
            message += f"\nRecommended stay: {hotels[0].name}\n"
        return message

    else:
        return "❌ Sorry, I can only answer travel-related questions about destinations, hotels, food, activities, and itineraries."
