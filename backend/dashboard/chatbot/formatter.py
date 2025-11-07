''' 
this is necessary to change the queryset responses to the understandable and clean text form
'''
# dashboard/chatbot/formatter.py

def format_destinations(destinations):
    """
    Format a list of Destination objects into a readable message
    """
    if not destinations:
        return "No destinations found for your request."

    message = "🌍 Here are some destinations you might like:\n"
    for i, dest in enumerate(destinations, 1):
        message += f"{i}. {dest.name} — Type: {dest.type.name if dest.type else 'Unknown'}\n"
    return message


def format_places(places):
    """
    Format a list of Place objects into a user-friendly message
    """
    if not places:
        return "No places found matching your request."

    message = "🏞️ Here are some top-rated places:\n"
    for i, place in enumerate(places, 1):
        rating = f"⭐ {place.avg_rating}" if hasattr(place, 'avg_rating') else "No rating"
        message += f"{i}. {place.name} — {rating}\n"
    return message


def format_hotels(hotels):
    """
    Format hotel results into a readable string
    """
    if not hotels:
        return "No hotels found matching your request."

    message = "🏨 Recommended Hotels:\n"
    for i, hotel in enumerate(hotels, 1):
        rating = f"⭐ {hotel.avg_rating}" if hasattr(hotel, 'avg_rating') else "No rating"
        price = f"💰 Price Range: {hotel.price_range}" if hasattr(hotel, 'price_range') else ""
        message += f"{i}. {hotel.name} — {rating} {price}\n"
    return message


def format_foods(foods):
    """
    Format food recommendations into a nice readable list
    """
    if not foods:
        return "No foods found matching your request."

    message = "🍴 Popular Foods:\n"
    for i, food in enumerate(foods, 1):
        rating = f"⭐ {food.avg_rating}" if hasattr(food, 'avg_rating') else "No rating"
        message += f"{i}. {food.name} — Type: {food.type} — {rating}\n"
    return message


def format_activities(activities):
    """
    Format activity recommendations into a clean message
    """
    if not activities:
        return "No activities found matching your request."

    message = "🎯 Things to do:\n"
    for i, act in enumerate(activities, 1):
        rating = f"⭐ {act.avg_rating}" if hasattr(act, 'avg_rating') else "No rating"
        message += f"{i}. {act.name} — Type: {act.type} — {rating}\n"
    return message


def format_destination_types(types):
    """
    Format destination types (e.g., Adventure, Religious, etc.)
    """
    if not types:
        return "No destination types available."

    message = "🗺️ Destination Categories:\n"
    for i, t in enumerate(types, 1):
        message += f"{i}. {t.name}\n"
    return message

