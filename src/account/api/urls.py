from django.urls import path

from .views import (
    UsersList, UsersDetailUpdateDelete, UserProfile, 
    Login, Register, VerifyOtp,
    ChangeTwoStepPassword, CreateTwoStepPassword,
)

app_name = "account-api"

urlpatterns = [
    path("", UsersList.as_view(), name="users-list"),
    path("profile/", UserProfile.as_view(), name="profile"),
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("verify/", VerifyOtp.as_view(), name="verify-otp"),
    path("change-two-step-password/", ChangeTwoStepPassword.as_view(), name="change-two-step-password"),
    path("create-two-step-password/", CreateTwoStepPassword.as_view(), name="create-two-step-password"),
    path("users/<int:pk>/", UsersDetailUpdateDelete.as_view(), name="users-detail"),
]
