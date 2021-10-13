from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from blog.models import Blog

from .pagination import BlogLimitOffsetPagination
from .serializers import (
    BlogListSerializer,
    BlogCreateSerializer,
    BlogDetailUpdateDeleteSerializer,
)
from .permissions import (
    IsSuperUserOrAuthor,
    IsSuperUserOrAuthorOrReadOnly,
)

class BlogListApiView(ListAPIView):
    serializer_class = BlogListSerializer
    pagination_class = BlogLimitOffsetPagination

    def get_queryset(self):
        return Blog.objects.publish()


class BlogCreateApiView(CreateAPIView):
    serializer_class = BlogCreateSerializer
    permission_classes = [IsSuperUserOrAuthor,]

    def get_queryset(self):
        return Blog.objects.publish()

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            return serializer.save(
                author=self.request.user,
                status='d',
                special=False,
                )
        return serializer.save(author=self.request.user)


class BlogDetailUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    serializer_class =BlogDetailUpdateDeleteSerializer
    permission_classes = [IsSuperUserOrAuthorOrReadOnly,]
    lookup_field = 'slug'

    def get_queryset(self):
        return Blog.objects.publish()