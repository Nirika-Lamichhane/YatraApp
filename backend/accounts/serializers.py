from rest_framework import serializers
from .models import CustomUser, DestinationType, Destination

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'profile_photo', 'citizenship_photo', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_photo': {'required': True},
            'citizenship_photo': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # hashes the password properly
        user.save()
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
