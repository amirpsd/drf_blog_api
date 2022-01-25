from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "phone",
            "first_name",
            "last_name",
            "author",
        ]


class UserDetailUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = [
            "password",
        ]      


class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.ReadOnlyField()
    
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "phone",
            "first_name",
            "last_name",
        ]
