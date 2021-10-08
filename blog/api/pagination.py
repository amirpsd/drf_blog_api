from rest_framework.pagination import LimitOffsetPagination


class BlogLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 20

