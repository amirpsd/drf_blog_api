from django.urls import path

from .views import CommentListApiView

app_name = "comment-api"

urlpatterns = [
    path('<int:pk>', CommentListApiView.as_view(), name="list")
]
