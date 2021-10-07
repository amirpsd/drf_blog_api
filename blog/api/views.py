from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from blog.models import Blog

from .serializers import (
    BlogListSerializer,
)

class BlogListApiView(APIView):
    def get(self,request):
        blog = Blog.objects.publish()
        serializer = BlogListSerializer(blog, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)