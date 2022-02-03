from django.urls import path

from .views import (
    UserListApiView,
    UserDetailUpdateDeleteApiView,
    UserProfileApiView,
    RegisterApiView,
    VerifyOtpApiView,
)

app_name = "account-api"

urlpatterns = [
    path("", UserListApiView.as_view(), name="list"),
    path("profile/", UserProfileApiView.as_view(), name="profile"),
    path("register/", RegisterApiView.as_view(), name="register"),
    path("register/verify/", VerifyOtpApiView.as_view(), name="verify"),
    path("users/<int:pk>/", UserDetailUpdateDeleteApiView.as_view(), name="users-detail"),
]
