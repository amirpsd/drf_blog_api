from django.urls import path

from .views import (
    UserListApiView,
    UserDetailUpdateDeleteApiView,
    UserProfileApiView,
    RegisterApiView,
    LoginApiView,
    VerifyOtpApiView,
)

app_name = "account-api"

urlpatterns = [
    path("", UserListApiView.as_view(), name="list"),
    path("profile/", UserProfileApiView.as_view(), name="profile"),
    path("register/", RegisterApiView.as_view(), name="register"),
    path("login/", LoginApiView.as_view(), name="login"),
    path("verify/", VerifyOtpApiView.as_view(), name="verify-otp"),
    path("users/<int:pk>/", UserDetailUpdateDeleteApiView.as_view(), name="users-detail"),
]
