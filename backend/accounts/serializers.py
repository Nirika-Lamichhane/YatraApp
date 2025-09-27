from rest_framework import serializers
from .models import CustomUser, DestinationType, Destination
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import Group

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    role =serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)


      # Unique fields
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message="This email is already registered.")]
    )
    phone_number = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message="This phone number is already registered.")]
    )
    citizenship_number = serializers.CharField(
        required=False,  # Only required for guides
        allow_blank=True
    )


    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'profile_photo', 'citizenship_number', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_photo': {'required': True},
            'citizenship_number': {'required': False},
        }

    # custom validation for the role
    def validate(self, data):
        role = data.get('role')
        citizenship_number = data.get('citizenship_number')

        if role == 'guide' and not citizenship_number:
            raise serializers.ValidationError({
                'citizenship_number': 'This field is required for guides.'
            })
        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # hashes the password properly
        user.role = role
        user.save()

        # assign to group automatically based on role for permissions
        if role == 'guide':
            group = Group.objects.get(name='Tour Guide')
        else:
            group = Group.objects.get(name='Regular User')
        user.groups.add(group)
        return user


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class DestinationTypeSerializer(serializers.ModelSerializer):
    icon=serializers.ImageField(required=True)

    class Meta:
        model = DestinationType
        fields = ['id', 'name', 'icon']

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
