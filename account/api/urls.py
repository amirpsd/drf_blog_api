from django.urls import path

from .views import (
    UserListApiView,
    UserDetailUpdateDeleteApiView,
    )

app_name = "account-api"

urlpatterns = [
    path("", UserListApiView.as_view(), name="list"),
    path("<username>/", UserDetailUpdateDeleteApiView.as_view(), name="detail"),
]
