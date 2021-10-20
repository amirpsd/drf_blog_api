from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = [
            "password",
            "last_login",
            "groups",
            "user_permissions",
        ]