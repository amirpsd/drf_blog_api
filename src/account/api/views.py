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
    RegisterSerializer,
    OtpSerializer,
)
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
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.data.get("phone")

            if get_user_model().objects.filter(phone=phone).exists():
                return Response(
                    {
                        "Bad Request": "There is already a user with this phone number, please enter a different value."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = get_user_model().objects.create_user(phone=phone)
            user.is_active = False
            user.save()
            code = otp_generator()
            context = {
                "code": code,
                # Here the otp code must later be sent to the user's phone number by a server.
            }
            request.session["phone"] = phone
            cache.set(code, request.session["phone"], 300)
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
            phone = request.session.get("phone")
            phone_in_cache = cache.get(code)

            if phone_in_cache is not None:
                if phone_in_cache == phone:
                    user = get_object_or_404(get_user_model(), phone=phone)
                    user.is_active = True
                    user.save()
                    refresh = RefreshToken.for_user(user)
                    context = {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {
                            "Bad Request": "The code entered is incorrect"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {
                        "Code expired": "The entered code has expired"
                    },
                    status=status.HTTP_408_REQUEST_TIMEOUT,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
