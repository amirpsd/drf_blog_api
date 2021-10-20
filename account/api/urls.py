from django.urls import path

from .views import UserListApiView

app_name = "account-api"

urlpatterns = [
    path("list/", UserListApiView.as_view(), name="list")
]   
