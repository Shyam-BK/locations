from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import LatLong

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'firstName', 'lastName', 'phoneNumber', 'serviceProviding', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            phoneNumber=validated_data['phoneNumber'],
            serviceProviding=validated_data['serviceProviding'],
            password=validated_data['password']
        )
        return user


class LatLongSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatLong
        fields = ('id','latitude', 'longitude', 'user')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class LatLongUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatLong
        fields = ['latitude', 'longitude']