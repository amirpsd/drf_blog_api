from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from blog.models import Blog
from ..models import Comment
from .serializers import (
    CommentListSerializer,
    CommentUpdateCreateSerializer,
)


class CommentsList(APIView):
    """
    get:
        Returns the list of comments on a particular post.

        parameters = [pk]
    """

    def get(self, request, pk):
        blog = get_object_or_404(Blog, id=pk, status="p")
        query = Comment.objects.filter_by_instance(blog)
        serializer = CommentListSerializer(query, many=True)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK,
        )


class CommentCreate(APIView):
    """
    post:
        Create a comment instnace. Returns created comment data.

        parameters: [object_id, name, parent, body,]
    """

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
                parent_id = serializer.data.get('parent'),
                body = serializer.data.get('body'),
            )
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED,
            )
        
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST,
            )
            

class CommentUpdateDelete(APIView):
    """
    put:
        Updates an existing comment. Returns updated comment data.

        parameters: [object_id, name, parent, body,]

    delete:
        Delete an existing comment.

        parameters: [pk]
    """

    permission_classes = [IsAuthenticated,]

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        serializer = CommentUpdateCreateSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST,
            )


    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,)
