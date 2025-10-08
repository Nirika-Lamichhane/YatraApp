# dashboard/chatbot/retrieval.py

# Import models from both apps
from accounts.models import DestinationType, Destination
from dashboard.models import Place, Hotel, Food, Activity

# -----------------------
# DestinationType Retrieval
# -----------------------
def retrieve_destination_types(limit=10):
    """
    Retrieve all destination types, optionally limited
    """
    return DestinationType.objects.all()[:limit]


# -----------------------
# Destination Retrieval
# -----------------------
def retrieve_destinations(destination_type_name=None, limit=10):
    """
    Retrieve destinations optionally filtered by destination type
    """
    destinations = Destination.objects.all()
    
    if destination_type_name:
        destinations = destinations.filter(type__name__iexact=destination_type_name)
    
    return destinations.order_by('name')[:limit]


# -----------------------
# Place Retrieval
# -----------------------
def retrieve_places(destination_name=None, min_rating=None, limit=5):
    """
    Retrieve places optionally filtered by destination and minimum rating
    """
    places = Place.objects.all()
    
    if destination_name:
        places = places.filter(destination__name__iexact=destination_name)
    
    if min_rating:
        places = places.filter(avg_rating__gte=min_rating)
    
    return places.order_by('-avg_rating')[:limit]


# -----------------------
# Hotel Retrieval
# -----------------------
def retrieve_hotels(place_name=None, max_price=None, min_rating=None, limit=5):
    """
    Retrieve hotels optionally filtered by place, price, and minimum rating
    """
    hotels = Hotel.objects.all()
    
    if place_name:
        hotels = hotels.filter(place__name__iexact=place_name)
    
    if max_price:
        hotels = hotels.filter(price_range__lte=max_price)
    
    if min_rating:
        hotels = hotels.filter(avg_rating__gte=min_rating)
    
    return hotels.order_by('-avg_rating')[:limit]


# -----------------------
# Food Retrieval
# -----------------------
def retrieve_foods(place_name=None, food_type=None, min_rating=None, limit=5):
    """
    Retrieve foods optionally filtered by place, type, and minimum rating
    """
    foods = Food.objects.all()
    
    if place_name:
        foods = foods.filter(place__name__iexact=place_name)
    
    if food_type:
        foods = foods.filter(type__iexact=food_type)
    
    if min_rating:
        foods = foods.filter(avg_rating__gte=min_rating)
    
    return foods.order_by('-avg_rating')[:limit]


# -----------------------
# Activity Retrieval
# -----------------------
def retrieve_activities(place_name=None, activity_type=None, min_rating=None, limit=5):
    """
    Retrieve activities optionally filtered by place, type, and minimum rating
    """
    activities = Activity.objects.all()
    
    if place_name:
        activities = activities.filter(place__name__iexact=place_name)
    
    if activity_type:
        activities = activities.filter(type__iexact=activity_type)
    
    if min_rating:
        activities = activities.filter(avg_rating__gte=min_rating)
    
    return activities.order_by('-avg_rating')[:limit]
