from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from blog.models import Blog, Category

from .pagination import BlogLimitOffsetPagination
from .serializers import (
    BlogListSerializer,
    BlogCreateSerializer,
    BlogDetailUpdateDeleteSerializer,
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
        'special'
    ]
    search_fields = [
        'title',
        'summary',
        'author__username',
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
    lookup_field = 'slug'
    queryset = Blog.objects.publish()

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            return serializer.save(
                author=self.request.user,
                status='d',
                special=False,
                )
        return serializer.save()


@login_required
def like(request, pk):
    user = request.user
    blog = get_object_or_404(Blog, pk=pk, status='p')

    if user in blog.dislikes.all():
        blog.dislikes.remove(user)
        blog.likes.add(user)

    elif user in blog.likes.all():
        blog.likes.remove(user)

    else:
        blog.likes.add(user)
     
    return redirect("blog:blog-api:list")


@login_required
def dislike(request, pk):
    user = request.user
    blog = get_object_or_404(Blog, pk=pk, status='p')

    if user in blog.likes.all():
        blog.likes.remove(user)
        blog.dislikes.add(user)

    elif user in blog.dislikes.all():
        blog.dislikes.remove(user)

    else:
        blog.dislikes.add(user)
     
    return redirect("blog:blog-api:list")


class CategoryListApiView(ListAPIView):
    serializer_class = BlogListSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        category = get_object_or_404(Category.objects.active(), slug=self.kwargs.get("slug"))
        queryset = category.blogs.publish()
        return queryset
