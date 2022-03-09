from django.urls import path

from .views import (
    CommentsList,
    CommentCreate,
    CommentUpdateDelete,
    )

app_name = "api"

urlpatterns = [
    path("<int:pk>/", CommentsList.as_view(), name="list"),
    path("create/", CommentCreate.as_view(), name="create"),
    path("update-delete/<int:pk>/", CommentUpdateDelete.as_view(), name="update-delete"),
]
