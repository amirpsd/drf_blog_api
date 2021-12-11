from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status 

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
    serializer_class =BlogDetailUpdateDeleteSerializer
    permission_classes = [IsSuperUserOrAuthorOrReadOnly,]
    lookup_field = 'slug'


    def get_object(self):
        slug = self.kwargs.get('slug')
        blog = get_object_or_404(Blog, slug=slug, status='p')
        blog.visits += 1
        blog.save()
        return blog 


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
     
    return redirect("/")


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
     
    return redirect("/")


class CategoryListApiView(APIView):
    
    def get(self, request, slug):
        category = get_object_or_404(Category.objects.active(), slug=slug)
        category_list = category.blogs.publish()
        serializer = CategoryListSerializer(category_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)