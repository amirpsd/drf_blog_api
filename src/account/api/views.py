from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserListSerializer,
    UserDetailUpdateDeleteSerializer,
    UserProfileSerializer,
    RegisterLoginSerializer,
    OtpSerializer,
)
from ..models import PhoneOtp 
from permissions import IsSuperUser
from extensions.code_generator import otp_generator


class UserListApiView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [
        IsSuperUser,
    ]
    filterset_fields = [
        "author",
    ]
    search_fields = [
        "phone",
        "first_name",
        "last_name",
    ]
    ordering_fields = (
        "id",
        "author",
    )

    def get_queryset(self):
        return get_user_model().objects.all()


class UserDetailUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailUpdateDeleteSerializer
    permission_classes = [
        IsSuperUser,
    ]

    def get_object(self):
        pk = self.kwargs.get("pk")
        user = get_object_or_404(get_user_model(), pk=pk)
        return user


class UserProfileApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        user = get_user_model().objects.get(pk=self.request.user.pk)
        return user


class RegisterApiView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = RegisterLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.data.get("phone")
            user_is_exists = get_user_model().objects.filter(phone=phone).values("phone").exists()

            if user_is_exists:
                return Response(
                    {
                        "User exists.": "Please enter a different phone number.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            code = otp_generator()
            user, created = PhoneOtp.objects.get_or_create(
                phone=phone,
            )
            user.otp = code
            user.count += 1
            user.save(update_fields=["otp", "count"])
            if user.count >= 8 :
                return Response(
                    {
                        "Many Request": "You requested too much.",
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )
            cache.set(phone, code, 500)
            context = {
                "code": code,
                # Here the otp code must later be sent to the user's phone number by a server.
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = RegisterLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.data.get("phone")
            user_is_exists = get_user_model().objects.filter(phone=phone).values("phone").exists()

            if not user_is_exists:
                return Response(
                    {
                        "No User exists.": "Please enter another phone number.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            code = otp_generator()
            user, created = PhoneOtp.objects.get_or_create(
                phone=phone,
            )
            user.otp = code
            user.count += 1
            user.save(update_fields=["otp", "count"])
            if user.count >= 8 :
                return Response(
                    {
                        "Many Request": "You requested too much.",
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )
            cache.set(phone, code, 500)
            context = {
                "code": code,
                # Here the otp code must later be sent to the user's phone number by a server.
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpApiView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.data.get("code")
            query = PhoneOtp.objects.filter(otp=code)

            if not query.exists():
                return Response(
                    {
                        "Incorrect code.": "The code entered is incorrect.",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

            phone = query.first()
            code_in_cache = cache.get(phone)

            if code_in_cache is not None:
                if code_in_cache == code:
                    user, created = get_user_model().objects.get_or_create(phone=phone)
                    refresh = RefreshToken.for_user(user)
                    query.delete()
                    context = {
                        "created":created,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {
                            "Incorrect code.": "The code entered is incorrect.",
                        },
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                return Response(
                    {
                        "Code expired": "The entered code has expired.",
                    },
                    status=status.HTTP_408_REQUEST_TIMEOUT,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
