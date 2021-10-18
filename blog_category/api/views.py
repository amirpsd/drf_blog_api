from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from blog_category.models import Category

from .serializers import CategoryListSerializer


class CategoryListApiView(APIView):
    
    def get(self, request, slug):
        category = get_object_or_404(Category.objects.publish(), slug=slug)
        category_list = category.blogs.publish()
        serializer = CategoryListSerializer(category_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)