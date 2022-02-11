from django.shortcuts import get_object_or_404

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
    BlogsListSerializer,
    BlogCreateSerializer,
    BlogDetailUpdateDeleteSerializer,
    CategoryListSerializer,
)
from permissions import (
    IsSuperUserOrAuthor,
    IsSuperUserOrAuthorOrReadOnly,
)


class BlogsList(ListAPIView):
    """
    get:
        Returns a list of all existing blogs.
    """

    serializer_class = BlogsListSerializer
    pagination_class = BlogLimitOffsetPagination
    filterset_fields = [
        "category", "special",
    ]
    search_fields = [
        "title", "summary",
        "author__first_name",
    ]
    ordering_fields = (
        "publish", "special",
    )

    def get_queryset(self):
        return Blog.objects.publish()


class BlogCreate(CreateAPIView):
    """
    post:
        Creates a new post instance. Returns created post data.

        parameters: [title,   body,    image,   summary, 
                    category, publish, special, status,]
    """

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


class BlogDetailUpdateDelete(RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a post instance. Searches post using slug field.

    put:
        Updates an existing post. Returns updated post data.

        parameters: exclude = [user, create, updated, likes]
        ]

    delete:
        Delete an existing post.

        parameters = [slug]
    """

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


class LikeBlog(APIView):
    """
    get:
        Likes the desired blog.

        parameters = [pk]
    """

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
            status=200,
        )
     

class CategoryBlog(ListAPIView):
    """
    get:
        Returns the list of blogs on a particular category.

        parameters = [slug]
    """

    serializer_class = BlogsListSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        category = get_object_or_404(Category.objects.active(), slug=self.kwargs.get("slug"))
        queryset = category.blogs.publish()
        return queryset


class CategoryList(ListAPIView):
    """
    get:
        Returns a list of all existing category.
        
        parameters = [slug]
    """

    serializer_class = CategoryListSerializer
    lookup_field = 'slug'
    queryset = Category.objects.active()
