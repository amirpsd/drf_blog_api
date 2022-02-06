from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Blog, Category
from .pagination import BlogLimitOffsetPagination
from .serializers import (
    BlogListSerializer,
    BlogCreateSerializer,
    BlogDetailUpdateDeleteSerializer,
    CategoryListSerializer,
)
from permissions import (
    IsSuperUserOrAuthor,
    IsSuperUserOrAuthorOrReadOnly,
)


class BlogListApiView(ListAPIView):
    serializer_class = BlogListSerializer
    pagination_class = BlogLimitOffsetPagination
    filterset_fields = [
        'category',
        'special',
    ]
    search_fields = [
        'title',
        'summary',
        'author__first_name',
    ]
    ordering_fields = (
        'publish',
        'special',
    )

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
    serializer_class = BlogDetailUpdateDeleteSerializer
    permission_classes = (IsSuperUserOrAuthorOrReadOnly,)
    lookup_field = "slug"

    def get_object(self):
        blog = get_object_or_404(Blog, slug=self.kwargs.get("slug"))
        return blog

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            return serializer.save(
                author=self.request.user,
                status='d',
                special=False,
                )
        return serializer.save()


class LikeBlogApiView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, pk):
        user = request.user
        blog = get_object_or_404(Blog, pk=pk, status='p')

        if user in blog.likes.all():
            blog.likes.remove(user)

        else:
            blog.likes.add(user)
        
        return Response(
            {
                "ok" : "Your request was successful.",
            },
            status=201,
        )
     

class CategoryBlogApiView(ListAPIView):
    serializer_class = BlogListSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        category = get_object_or_404(Category.objects.active(), slug=self.kwargs.get("slug"))
        queryset = category.blogs.publish()
        return queryset


class CategoryListApiView(ListAPIView):
    serializer_class = CategoryListSerializer
    lookup_field = 'slug'
    queryset = Category.objects.active()
