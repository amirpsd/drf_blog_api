from django.contrib.auth import get_user_model

from rest_framework import serializers


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id", "phone",
            "first_name", "last_name",
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
    two_step_password = serializers.ReadOnlyField()

    class Meta:
        model = get_user_model()
        fields = [
            "id", "phone",
            "first_name", "last_name",
            "two_step_password",
        ]


class AuthenticationSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=12,
        min_length=12,
    )

    def validate_phone(self, value):
        from re import match

        if not match("^989\d{2}\s*?\d{3}\s*?\d{4}$", value):
            raise serializers.ValidationError("Invalid phone number.")

        return value


class OtpSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=6,
        min_length=6,
    )

    def validate_code(self, value):
        try:
            int(value)
        except ValueError as _:
            raise serializers.ValidationError("Invalid Code.")

        return value


class GetTwoStepPasswordSerializer(serializers.Serializer):
    """
        Base serializer two-step-password.
    """
    password = serializers.CharField(
        max_length=20,
    )

    confirm_password = serializers.CharField(
        max_length=20,
    )

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError(
                {"Error": "Your passwords didn't match."}
            )

        return data


class ChangeTwoStepPasswordSerializer(GetTwoStepPasswordSerializer):
    old_password = serializers.CharField(
        max_length=20,
    )
