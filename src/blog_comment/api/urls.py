from django.urls import path

from .views import (
    CommentListApiView,
    CommentCreateApiView,
    CommentUpdateDeleteApiView,
    )

app_name = "comment-api"

urlpatterns = [
    path('<int:pk>/', CommentListApiView.as_view(), name="list"),
    path('create/', CommentCreateApiView.as_view(), name="create"),
    path('update-delete/<int:pk>/', CommentUpdateDeleteApiView.as_view(), name="update-delete"),
]
