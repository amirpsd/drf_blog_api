from django.urls import path, include

app_name = "comment"

urlpatterns = [
    path("api/", include("comment.api.urls")),
]
