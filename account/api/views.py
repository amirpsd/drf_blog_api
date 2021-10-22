from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    )

from .serializers import (
    UserListSerializer,
    UserDetailUpdateDeleteSerializer,
    )
from permissions import IsSuperUser


class UserListApiView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsSuperUser,]
    filterset_fields = [
        'author',
    ]
    search_fields = [
        'username',
        'first_name',
        'email',
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
        username = self.kwargs.get("username")
        user = get_object_or_404(get_user_model(), username=username)
        return user
    
