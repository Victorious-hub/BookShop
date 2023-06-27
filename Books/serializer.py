from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db import models
from rest_framework import serializers

from .models import SimpleUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, required=True)
    first_name = serializers.CharField(max_length=255, required=True)
    created = serializers.DateTimeField()
    email = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = SimpleUser
        fields = ('id', 'created', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = SimpleUser.objects.create(
            first_name=validated_data['first_name'],

            email=validated_data['email'],

            created=validated_data['created'],

            last_name=validated_data['last_name'],

            password=make_password(validated_data['password']),

        )
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.email = validated_data.get("email", instance.email)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.created = validated_data.get("created", instance.created)
        instance.password = validated_data.get("password", instance.password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['email'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}
