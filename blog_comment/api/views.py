from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from blog.models import Blog
from blog_comment.models import Comment
from .serializers import (
    CommentListSerializer,
)

class CommentListApiView(APIView):

    def get(self, request, pk, *args, **kwargs):
        try:
            blog = Blog.objects.get(id=pk, status='p')
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset = Comment.objects.filter_by_instance(blog)
        serializer = CommentListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
