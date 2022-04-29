from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



class CustomPagination(PageNumberPagination):
    
    def get_paginated_response(self, data):
        return Response(data)