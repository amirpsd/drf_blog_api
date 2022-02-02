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


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=11,
        min_length=10,
    )

    def validate_phone(self, value):
        from re import match

        if len(value) == 10 and value[0] != "0":
            value = "0" + value
        if not match("^09\d{2}\s*?\d{3}\s*?\d{4}$", value):
            raise serializers.ValidationError("Invalid phone number.")

        return value


class OtpSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=6,
        min_length=6,
    )

    def validate_code(self, value):
        from string import ascii_letters as char

        for _ in value:
            if _ in char:
                raise serializers.ValidationError("Invalid Code.")
        return value
