from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from accounts.models import Destination

class Place(models.Model):
    name = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    avg_rating= models.FloatField(default=0.0)
    image = models.ImageField(upload_to='places/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} in {self.destination}"

    def favorites_count(self):
        from dashboard.models import Favorite
        content_type = ContentType.objects.get_for_model(self)
        return Favorite.objects.filter(content_type=content_type, object_id=self.id).count()

    def comments_count(self):
        from dashboard.models import Comment
        content_type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(content_type=content_type, object_id=self.id).count()

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    price_range = models.FloatField(default=100.0)
    avg_rating = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    description = models.TextField(blank=True)  # Add description field for UI

    def __str__(self):
        return f"{self.name} near {self.place}"

    def favorites_count(self):
        from dashboard.models import Favorite
        content_type = ContentType.objects.get_for_model(self)
        return Favorite.objects.filter(content_type=content_type, object_id=self.id).count()

    def comments_count(self):
        from dashboard.models import Comment
        content_type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(content_type=content_type, object_id=self.id).count()

class Food(models.Model):
    name = models.CharField(max_length=100)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    price_range = models.FloatField(default=100.0)
    avg_rating = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='foods/', null=True, blank=True)
    description = models.TextField(blank=True)  # Add description field for UI

    def __str__(self):
        return f"{self.name} at {self.place}"

    def favorites_count(self):
        from dashboard.models import Favorite
        content_type = ContentType.objects.get_for_model(self)
        return Favorite.objects.filter(content_type=content_type, object_id=self.id).count()

    def comments_count(self):
        from dashboard.models import Comment
        content_type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(content_type=content_type, object_id=self.id).count()

class Activity(models.Model):
    name = models.CharField(max_length=100)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    duration = models.CharField(max_length=50)
    price_range = models.FloatField(default=100.0)
    avg_rating = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='activities/', null=True, blank=True)
    description = models.TextField(blank=True)  # Add description field for UI

    def __str__(self):
        return f"{self.name} at {self.place}"

    def favorites_count(self):
        from dashboard.models import Favorite
        content_type = ContentType.objects.get_for_model(self)
        return Favorite.objects.filter(content_type=content_type, object_id=self.id).count()

    def comments_count(self):
        from dashboard.models import Comment
        content_type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(content_type=content_type, object_id=self.id).count()

# Generic Favorite and Comment models unchanged



# ------------------------
# Generic Favorite Model
# ------------------------
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
    
    def __str__(self):
        return f"{self.user} favorited {self.content_object}"

# ------------------------
# Generic Comment Model
# ------------------------
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.content_object}"

class Rating(models.Model):

    # this is used to link the rating to a user who gave the rating 
    # the syntax settings.AUTH_USER_MODEL is used to refer to the use of the user model defined in auth_user_model of the settings.py
    # cascade means if the user is deleted then all the ratings given by that user will also be deleted

    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # generic link to place hotel food and activity
    content_type= models.ForeignKey(ContentType, on_delete=models.CASCADE) # stores the model type

    object_id= models.PositiveIntegerField()  # stores the primary key of the model instance

    content_object= GenericForeignKey('content_type', 'object_id') 

    rating= models.FloatField() # stores the actual rating value the user gave

    created_at= models.DateTimeField(auto_now_add=True) # stores the timestamp when the rating was created

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
    
    def __str__(self):
        return f"Rating by {self.user} on {self.content_object}: {self.rating}"