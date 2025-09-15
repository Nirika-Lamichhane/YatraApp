# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _  # supports the use of many languages and provides the translation of lanhuage facility

def user_profile_path(instance, filename):  # here filename is the name of the file that is uploaded and instance is the object of the class 
    
    '''
    in class custom user when someone uploads the file their name is the instance and as in class this function is defined, it is called and 
    it stores the file in the path specified in the function
    / used here are for the path to be created in the media folder
    '''
    return f"profile_photos/user_{instance.username}/{filename}"

def user_citizenship_path(instance, filename):
    return f"citizenship_photos/user_{instance.username}/{filename}"
from django.utils.translation import gettext_lazy as _

# models.py

class DestinationType(models.Model):
    name = models.CharField(max_length=100)
    icon=models.ImageField(upload_to='destination_types/icons/')

class Destination(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(DestinationType, on_delete=models.CASCADE)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), blank=True)
    phone_number = models.CharField(_('phone number'), max_length=15)
    profile_photo = models.ImageField(_('profile photo'), upload_to=user_profile_path)
    citizenship_photo = models.ImageField(_('citizenship photo'), upload_to=user_citizenship_path)
    #favorites = models.ManyToManyField(Destination, blank=True, related_name='favorited_by')
    ROLE_CHOICES=[
    (
        'user','Normal User'
    ),
    (
        'guide','Tour Guide'
    )]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')



    def __str__(self):
        return self.username