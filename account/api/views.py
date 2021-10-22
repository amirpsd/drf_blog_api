from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListAPIView,
    )

from .serializers import (
    UserListSerializer,
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
        "author",
    )

    def get_queryset(self):
        return get_user_model().objects.all()



