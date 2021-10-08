from django.urls import path

from .views import (
    BlogListApiView,
)

app_name = 'blog-api'

urlpatterns = [
    path('', BlogListApiView.as_view(),name='list'),
]   
