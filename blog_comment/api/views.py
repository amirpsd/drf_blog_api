from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from blog.models import Blog
from blog_comment.models import Comment
from .serializers import (
    CommentListSerializer,
)

class CommentListApiView(APIView):
    
    def get(self, request, slug, *args, **kwargs):
        blog = Blog.objects.get(slug=slug)
        comments = Comment.objects.filter(blog=blog)
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
