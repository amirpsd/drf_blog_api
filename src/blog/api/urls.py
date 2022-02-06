from django.urls import path

from .views import (
    BlogListApiView,
    BlogCreateApiView,
    BlogDetailUpdateDeleteApiView,
    LikeBlogApiView,
    CategoryBlogApiView,
    CategoryListApiView,
)

app_name = 'blog-api'

urlpatterns = [
    path('', BlogListApiView.as_view(), name='list'),
    path('create/', BlogCreateApiView.as_view(), name='create'),
    path('category/list/', CategoryListApiView.as_view(), name="category-list"),
    path('category/<slug:slug>/', CategoryBlogApiView.as_view(), name="category-blog"),
    path('<slug:slug>/', BlogDetailUpdateDeleteApiView.as_view(), name='detail'),
    path('like/<int:pk>/', LikeBlogApiView.as_view(), name='like'),
]   
