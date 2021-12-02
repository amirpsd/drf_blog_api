from django.urls import path

from .views import CategoryListApiView

app_name = 'category-api'


urlpatterns = [
    path('<slug:slug>/', CategoryListApiView.as_view(), name="list")
]   
