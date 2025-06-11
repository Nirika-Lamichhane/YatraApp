

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm  # your custom user creation form

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # use your custom form for adding users
    form = CustomUserCreationForm      # you can also use the same for editing or create a separate change form if you want

    model = CustomUser

    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_active')  # show these columns in user list
    list_filter = ('is_staff', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'profile_photo', 'citizenship_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('username', 'email', 'phone_number', 'profile_photo', 'citizenship_photo', 'password1', 'password2')}),
    )

    search_fields = ('username', 'email', 'phone_number')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
