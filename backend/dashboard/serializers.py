from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from .models import Place, Hotel, Food, Activity, Favorite, Comment

class PlaceSerializer(serializers.ModelSerializer):
    favorites_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Place
        fields = ['id', 'name', 'destination', 'description', 'image','rating', 'favorites_count', 'comments_count']

class HotelSerializer(serializers.ModelSerializer):
    favorites_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'place', 'price_range', 'rating', 'image', 'description','price_range', 'favorites_count', 'comments_count']

class FoodSerializer(serializers.ModelSerializer):
    favorites_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Food
        fields = ['id', 'name', 'place', 'type', 'image', 'rating','price_range','description', 'favorites_count', 'comments_count']

class ActivitySerializer(serializers.ModelSerializer):
    favorites_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'name', 'place', 'duration', 'image', 'rating' ,'price_range','description', 'favorites_count', 'comments_count']

class FavoriteSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'content_type', 'object_id', 'content_object', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_content_object(self, obj):
        return str(obj.content_object)

class CommentSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content_type', 'object_id', 'content_object', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_content_object(self, obj):
        return str(obj.content_object)
    
    print(" restarting after 2 days")