from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from blog.models import Blog
from blog_comment.models import Comment
from .serializers import (
    CommentListSerializer,
    CommentUpdateCreateSerializer,
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


class CommentCreateApiView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        serializer = CommentUpdateCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            blog = get_object_or_404(Blog, pk=serializer.data.get('object_id'), status='p')
            comment_for_model = ContentType.objects.get_for_model(blog)
            comment = Comment.objects.create(
                user = request.user,
                name = serializer.data.get('name'),
                content_type = comment_for_model,
                object_id = blog.id,
                body = serializer.data.get('body'),
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class CommentUpdateDeleteApiView(APIView):
    permission_classes = [IsAuthenticated,]


    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        serializer = CommentUpdateCreateSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        comment.delete()
        return Response(status.HTTP_204_NO_CONTENT)
