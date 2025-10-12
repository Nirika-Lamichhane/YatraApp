# dashboard/chatbot/chatbot_core.py

from .retrieval import (
    retrieve_destination_types,
    retrieve_destinations,
    retrieve_places,
    retrieve_hotels,
    retrieve_foods,
    retrieve_activities
)
from .formatter import (
    format_destination_types,
    format_destinations,
    format_places,
    format_hotels,
    format_foods,
    format_activities
)

def generate_itinerary(place_name, days=3):
    """
    Generate a multi-day travel plan for a given place.
    Picks top-rated places, hotels, foods, and activities.
    """
    itinerary = f"🗓️ Here is a suggested {days}-day itinerary for {place_name.title()}:\n\n"
    
    # Retrieve top-rated data
    places = retrieve_places(destination_name=place_name, limit=days*2)  # extra places to distribute across days
    hotels = retrieve_hotels(place_name=place_name, limit=3)
    foods = retrieve_foods(place_name=place_name, limit=5)
    activities = retrieve_activities(place_name=place_name, limit=5)
    
    # Distribute items per day
    for day in range(1, days+1):
        itinerary += f"🌞 Day {day}:\n"
        
        if places:
            place = places[(day-1) % len(places)]
            itinerary += f"🏞️ Visit: {place.name}\n"
        
        if hotels:
            hotel = hotels[(day-1) % len(hotels)]
            itinerary += f"🏨 Stay at: {hotel.name}\n"
        
        if foods:
            food = foods[(day-1) % len(foods)]
            itinerary += f"🍴 Try: {food.name}\n"
        
        if activities:
            activity = activities[(day-1) % len(activities)]
            itinerary += f"🎯 Activity: {activity.name}\n"
        
        itinerary += "\n"
    
    return itinerary


def handle_query(query):
    """
    Main chatbot logic to handle user queries.
    Uses keyword matching to call appropriate retrieval and formatter functions.
    """
    query_lower = query.lower()
    
    # ---------- Multi-day itinerary ----------
    if "tour plan" in query_lower or "itinerary" in query_lower:
        # Example: "3-day tour plan for Pokhara"
        days = 3
        place_name = None
        words = query_lower.split()
        for i, w in enumerate(words):
            if w.isdigit():
                days = int(w)
            if w in ["pokhara", "chitwan", "kathmandu", "bandipur"]:  # add your place names
                place_name = w
        if place_name:
            return generate_itinerary(place_name, days)
        else:
            return "Please specify the place for your tour plan."
    
    # ---------- Destination types ----------
    elif "type" in query_lower or "category" in query_lower:
        types = retrieve_destination_types()
        return format_destination_types(types)
    
    # ---------- Destinations ----------
    elif "destination" in query_lower or "destinations" in query_lower or "places" in query_lower:
        dest_type = None
        # Dynamically fetch all types from DB
        all_types = [t.name.lower() for t in retrieve_destination_types(limit=50)]
        for t in all_types:
            if t in query_lower:
                dest_type = t
                break
        destinations = retrieve_destinations(destination_type_name=dest_type)
        return format_destinations(destinations)
    
    # ---------- Places ----------
    elif "place" in query_lower or "best place" in query_lower:
        place_name = None
        min_rating = None
        # You can add logic here to extract rating from query
        # For now, it will just filter by destination if mentioned
        for dest in [d.name.lower() for d in retrieve_destinations(limit=50)]:
            if dest in query_lower:
                place_name = dest
                break
        places = retrieve_places(destination_name=place_name, min_rating=min_rating)
        return format_places(places)
    
    # ---------- Hotels ----------
    elif "hotel" in query_lower:
        place_name = None
        max_price = None
        min_rating = None
        # extract place
        for dest in [d.name.lower() for d in retrieve_destinations(limit=50)]:
            if dest in query_lower:
                place_name = dest
                break
        hotels = retrieve_hotels(place_name=place_name, max_price=max_price, min_rating=min_rating)
        return format_hotels(hotels)
    
    # ---------- Foods ----------
    elif "food" in query_lower or "restaurant" in query_lower:
        place_name = None
        food_type = None
        min_rating = None
        # extract place
        for dest in [d.name.lower() for d in retrieve_destinations(limit=50)]:
            if dest in query_lower:
                place_name = dest
                break
        foods = retrieve_foods(place_name=place_name, food_type=food_type, min_rating=min_rating)
        return format_foods(foods)
    
    # ---------- Activities ----------
    elif "activity" in query_lower or "things to do" in query_lower:
        place_name = None
        activity_type = None
        min_rating = None
        for dest in [d.name.lower() for d in retrieve_destinations(limit=50)]:
            if dest in query_lower:
                place_name = dest
                break
        activities = retrieve_activities(place_name=place_name, activity_type=activity_type, min_rating=min_rating)
        return format_activities(activities)
    
    else:
        return (
        " Sorry, I couldn’t understand your request. "
        "For more information or specific queries, please contact us at "
        "support@yatraapp.com or founders@yatraapp.com."
    )
