from django.urls import path

from .views import (
    UserListApiView,
    UserDetailUpdateDeleteApiView,
    UserProfileApiView,
    )

app_name = "account-api"

urlpatterns = [
    path("", UserListApiView.as_view(), name="list"),
    path('profile/', UserProfileApiView.as_view(), name="profile"),
    path("<username>/", UserDetailUpdateDeleteApiView.as_view(), name="detail"),
]
