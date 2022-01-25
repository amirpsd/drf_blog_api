from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    )
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserListSerializer,
    UserDetailUpdateDeleteSerializer,
    UserProfileSerializer,
    )
from permissions import IsSuperUser


class UserListApiView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsSuperUser,]
    filterset_fields = [
        'author',
    ]
    search_fields = [
        'phone',
        'first_name',
        'last_name',
    ]
    ordering_fields = (
        'id',
        'author',
    )

    def get_queryset(self):
        return get_user_model().objects.all()


class UserDetailUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailUpdateDeleteSerializer
    permission_classes = [IsSuperUser,]

    def get_object(self):
        phone = self.kwargs.get("phone")
        user = get_object_or_404(get_user_model(), phone=phone)
        return user


class UserProfileApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserProfileSerializer

    def get_object(self):
        user = get_user_model().objects.get(pk=self.request.user.pk)
        return user