from django.urls import path

from .views import (
    BlogsList,
    BlogCreate,
    BlogDetailUpdateDelete,
    LikeBlog,
    CategoryBlog,
    CategoryList,
)

app_name = "api"

urlpatterns = [
    path("", BlogsList.as_view(), name="list"),
    path("create/", BlogCreate.as_view(), name="create"),
    path("category/list/", CategoryList.as_view(), name="category-list"),
    path("category/<slug:slug>/", CategoryBlog.as_view(), name="category-blog"),
    path("<slug:slug>/", BlogDetailUpdateDelete.as_view(), name="detail"),
    path("like/<int:pk>/", LikeBlog.as_view(), name="like"),
]   
