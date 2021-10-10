from django.urls import path

from .views import (
    BlogListApiView,
    BlogCreateApiView,
    BlogDetailUpdateDeleteApiView
)

app_name = 'blog-api'

urlpatterns = [
    path('', BlogListApiView.as_view(),name='list'),
    path('create/', BlogCreateApiView.as_view(),name='create'),
    path('<slug:slug>/', BlogDetailUpdateDeleteApiView.as_view(),name='detail'),
]   
