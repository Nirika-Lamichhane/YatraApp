from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from .models import Place, Hotel, Food, Activity, Favorite, Comment,Rating

class PlaceSerializer(serializers.ModelSerializer):
    favorites_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    average_rating= serializers.SerializerMethodField()

    
    class Meta:
        model = Place
        fields = ['id', 'name', 'destination', 'description', 'image','avg_rating','favorites_count', 'comments_count']

    def get_average_rating(self, obj):
       content_type = ContentType.objects.get_for_model(obj)
       ratings = Rating.objects.filter(content_type=content_type, object_id=obj.id)
       if ratings.exists():
        return round(ratings.aggregate(Avg('rating'))['rating__avg'], 1)
       return 0.0


class HotelSerializer(serializers.ModelSerializer):
    favorites_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'place', 'price_range', 'avg_rating', 'image', 'description','price_range', 'favorites_count', 'comments_count']

    def get_average_rating(self, obj):
          content_type = ContentType.objects.get_for_model(obj)
          ratings = Rating.objects.filter(content_type=content_type, object_id=obj.id)
          if ratings.exists():
            return round(ratings.aggregate(Avg('rating'))['rating__avg'], 1)
          return 0.0

class FoodSerializer(serializers.ModelSerializer):
    favorites_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Food
        fields = ['id', 'name', 'place', 'type', 'image', 'avg_rating','price_range','description', 'favorites_count', 'comments_count']

    def get_average_rating(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        ratings = Rating.objects.filter(content_type=content_type, object_id=obj.id)
        if ratings.exists():
            return round(ratings.aggregate(Avg('rating'))['rating__avg'], 1)
        return 0.0
    
class ActivitySerializer(serializers.ModelSerializer):
    favorites_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'name', 'place', 'duration', 'image', 'avg_rating' ,'price_range','description', 'favorites_count', 'comments_count']

    def get_average_rating(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        ratings = Rating.objects.filter(content_type=content_type, object_id=obj.id)
        if ratings.exists():
            return round(ratings.aggregate(Avg('rating'))['rating__avg'], 1)
        return 0.0
    
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