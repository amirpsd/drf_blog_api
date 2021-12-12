from django.urls import path

from .views import (
    BlogListApiView,
    BlogCreateApiView,
    BlogDetailUpdateDeleteApiView,
    like,
    dislike,
    CategoryListApiView
)

app_name = 'blog-api'

urlpatterns = [
    path('', BlogListApiView.as_view(), name='list'),
    path('create/', BlogCreateApiView.as_view(), name='create'),
    path('category/<slug:slug>/', CategoryListApiView.as_view(), name="category"),
    path('<slug:slug>/', BlogDetailUpdateDeleteApiView.as_view(), name='detail'),
    path('like/<int:pk>/', like, name='like'),
    path('dislike/<int:pk>/', dislike, name='dislike'),
]   
