from django.urls import path

from .views import CommentListApiView

app_name = "comment-api"

urlpatterns = [
    path('<slug:slug>', CommentListApiView.as_view(), name="list")
]
