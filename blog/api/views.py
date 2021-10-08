from rest_framework.generics import (
    ListAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from blog.models import Blog

from .pagination import BlogLimitOffsetPagination
from .serializers import (
    BlogListSerializer,
)

class BlogListApiView(ListAPIView):
    serializer_class = BlogListSerializer
    pagination_class = BlogLimitOffsetPagination

    def get_queryset(self):
        return Blog.objects.publish()