from rest_framework import serializers
from .models import Place, Hotel, Food, Activity, Favorite, Comment

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()  # optional: to show actual item name

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'content_type', 'object_id', 'content_object', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_content_object(self, obj):
        return str(obj.content_object)  # will return something like "Hotel Everest" or "Activity at Pokhara"
    
class CommentSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()  # optional: to show actual item name

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content_type', 'object_id', 'content_object', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_content_object(self, obj):
        return str(obj.content_object)  # will return something like "Hotel Everest" or "Activity at Pokhara"